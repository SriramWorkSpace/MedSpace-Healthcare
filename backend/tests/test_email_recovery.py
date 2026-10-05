"""Email verification, password reset and security alerts (ADR-030)."""

from __future__ import annotations

import smtplib
from datetime import timedelta
from unittest import mock

import httpx
import pytest
from sqlalchemy import select, update

from app.core import totp
from app.core.db import utcnow
from app.modules.audit.models import AuditLog
from app.modules.identity.models import EmailToken, User
from app.modules.integrations.google import FakeGoogleClient, GoogleIdentity
from app.shared.mail import FakeMailer, Message, SmtpMailer
from tests.conftest import BASE_URL, confirm_email, csrf, link_token, signup
from tests.test_google_signin import google_sign_in

PASSWORD = "correct-horse-battery"
NEW_PASSWORD = "a-brand-new-password"


def subjects(box: FakeMailer, to: str) -> list[str]:
    return [m.subject for m in box.latest(to)]


async def forgot(client: httpx.AsyncClient, email: str = "ada@example.com") -> httpx.Response:
    return await client.post("/api/auth/password/forgot", json={"email": email})


def reset_token(box: FakeMailer, to: str = "ada@example.com") -> str:
    message = next(m for m in box.latest(to) if "Reset" in m.subject)
    return link_token(message.text, "/reset-password")


async def login(client: httpx.AsyncClient, password: str) -> httpx.Response:
    return await client.post(
        "/api/auth/login", json={"email": "ada@example.com", "password": password}
    )


# ---- Verification -------------------------------------------------------------------------------


async def test_signup_sends_a_confirmation_link(client: httpx.AsyncClient, mailbox: FakeMailer):
    body = await signup(client)
    assert body["user"]["email_verified"] is False
    [message] = mailbox.latest("ada@example.com")
    assert message.subject == "Confirm your email for MedSpace"
    assert "/verify-email?token=" in message.text and message.html
    assert "Ada Okonkwo" in message.text

    await confirm_email(client, "ada@example.com")
    assert (await client.get("/api/auth/me")).json()["email_verified"] is True


async def test_confirmation_links_work_once_and_resend_retires_old_ones(
    client: httpx.AsyncClient, mailbox: FakeMailer
):
    await signup(client)
    first = link_token(mailbox.latest("ada@example.com")[0].text, "/verify-email")
    resent = await client.post("/api/me/email/verification", headers=csrf(client))
    assert resent.status_code == 202
    second = link_token(mailbox.latest("ada@example.com")[0].text, "/verify-email")
    assert first != second

    stale = await client.post("/api/auth/email/verify", json={"token": first})
    assert stale.status_code == 410
    ok = await client.post("/api/auth/email/verify", json={"token": second})
    assert ok.status_code == 200
    again = await client.post("/api/auth/email/verify", json={"token": second})
    assert again.status_code == 410

    done = await client.post("/api/me/email/verification", headers=csrf(client))
    assert done.status_code == 409


async def test_confirmation_works_from_another_browser(
    client: httpx.AsyncClient, mailbox: FakeMailer
):
    await signup(client)
    token = link_token(mailbox.latest("ada@example.com")[0].text, "/verify-email")
    from app.main import app

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=BASE_URL
    ) as phone:
        assert (
            await phone.post("/api/auth/email/verify", json={"token": token})
        ).status_code == 200
    assert (await client.get("/api/auth/me")).json()["email_verified"] is True


async def test_demo_accounts_are_verified_and_never_emailed(
    client: httpx.AsyncClient, mailbox: FakeMailer
):
    await client.post("/api/auth/demo")
    me = (await client.get("/api/auth/me")).json()
    assert me["email_verified"] is True
    assert not mailbox.outbox
    invite = await client.post(
        "/api/circle/invites",
        json={"email": "someone@example.com", "role": "viewer"},
        headers=csrf(client),
    )
    assert invite.json()["emailed"] is False
    assert not mailbox.latest("someone@example.com")  # demo accounts can't be a spam relay


async def test_circle_invitations_are_emailed_and_need_a_confirmed_address(
    client: httpx.AsyncClient, mailbox: FakeMailer
):
    await signup(client)
    invite = await client.post(
        "/api/circle/invites",
        json={"email": "eve@example.com", "role": "helper"},
        headers=csrf(client),
    )
    assert invite.json()["emailed"] is True
    [message] = mailbox.latest("eve@example.com")
    assert "Ada Okonkwo invited you" in message.subject
    assert invite.json()["url"] in message.text

    from app.main import app

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL) as eve:
        await signup(eve, email="eve@example.com", name="Eve")
        token = invite.json()["token"]
        blocked = await eve.post("/api/circle/accept", json={"token": token}, headers=csrf(eve))
        assert blocked.status_code == 403
        assert blocked.json()["reason"] == "email_unverified"
        await confirm_email(eve, "eve@example.com")
        ok = await eve.post("/api/circle/accept", json={"token": token}, headers=csrf(eve))
        assert ok.status_code == 200


# ---- Password reset -----------------------------------------------------------------------------


async def test_forgot_password_answers_the_same_for_unknown_addresses(
    client: httpx.AsyncClient, mailbox: FakeMailer
):
    await signup(client)
    client.cookies.clear()
    mailbox.outbox.clear()
    known = await forgot(client)
    unknown = await forgot(client, "nobody@example.com")
    assert known.status_code == unknown.status_code == 202
    assert known.json() == unknown.json()
    assert subjects(mailbox, "ada@example.com") == ["Reset your MedSpace password"]
    assert not mailbox.latest("nobody@example.com")


async def test_reset_sets_the_password_and_signs_out_everywhere(
    client: httpx.AsyncClient, mailbox: FakeMailer, session
):
    await signup(client)
    assert (await client.get("/api/auth/me")).status_code == 200
    await forgot(client)
    token = reset_token(mailbox)

    resp = await client.post(
        "/api/auth/password/reset", json={"token": token, "new_password": NEW_PASSWORD}
    )
    assert resp.status_code == 200
    assert (await client.get("/api/auth/me")).status_code == 401  # the old session is gone
    assert (await login(client, PASSWORD)).status_code == 401
    assert (await login(client, NEW_PASSWORD)).status_code == 200
    me = (await client.get("/api/auth/me")).json()
    assert me["email_verified"] is True  # reading the inbox proved the address

    assert "Your MedSpace password was reset" in subjects(mailbox, "ada@example.com")
    reused = await client.post(
        "/api/auth/password/reset", json={"token": token, "new_password": "yet-another-pass"}
    )
    assert reused.status_code == 410
    actions = set((await session.scalars(select(AuditLog.action))).all())
    assert {"auth.password_reset_requested", "auth.password_reset"} <= actions


async def test_only_the_newest_reset_link_works_and_links_expire(
    client: httpx.AsyncClient, mailbox: FakeMailer, session
):
    await signup(client)
    await forgot(client)
    older = reset_token(mailbox)
    await forgot(client)
    newer = reset_token(mailbox)
    body = {"new_password": NEW_PASSWORD}
    stale = await client.post("/api/auth/password/reset", json={"token": older, **body})
    assert stale.status_code == 410

    await session.execute(update(EmailToken).values(expires_at=utcnow() - timedelta(minutes=1)))
    await session.commit()
    expired = await client.post("/api/auth/password/reset", json={"token": newer, **body})
    assert expired.status_code == 410


async def test_reset_requests_are_quietly_limited_per_account(
    client: httpx.AsyncClient, mailbox: FakeMailer
):
    await signup(client)
    mailbox.outbox.clear()
    for _ in range(5):
        assert (await forgot(client)).status_code == 202
    assert len(mailbox.latest("ada@example.com")) == 3


async def test_reset_does_not_bypass_two_step_verification(
    client: httpx.AsyncClient, mailbox: FakeMailer
):
    await signup(client)
    setup = (await client.post("/api/me/mfa/setup", headers=csrf(client))).json()
    code = totp.code_at(setup["secret"], totp.current_step())
    await client.post("/api/me/mfa/enable", json={"code": code}, headers=csrf(client))
    assert "Two-step verification is on" in subjects(mailbox, "ada@example.com")

    await forgot(client)
    await client.post(
        "/api/auth/password/reset",
        json={"token": reset_token(mailbox), "new_password": NEW_PASSWORD},
    )
    second = (await login(client, NEW_PASSWORD)).json()
    assert second["mfa_required"] is True and second["user"] is None


async def test_password_change_sends_an_alert(client: httpx.AsyncClient, mailbox: FakeMailer):
    await signup(client)
    resp = await client.post(
        "/api/me/password",
        json={"current_password": PASSWORD, "new_password": NEW_PASSWORD},
        headers=csrf(client),
    )
    assert resp.status_code == 200
    [alert] = [m for m in mailbox.latest("ada@example.com") if "changed" in m.subject]
    assert "/app/settings#security" in alert.text


# ---- Google sign-in reclaims an unconfirmed account ---------------------------------------------


async def test_google_owner_reclaims_an_account_someone_else_registered(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch, session
):
    """Pre-hijack: an attacker signs up with the victim's address and sets a password."""
    await signup(client, email="ada@example.com", password="attackers-password")
    from app.main import app

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=BASE_URL
    ) as victim:

        async def verified(self, access_token):
            return GoogleIdentity(
                sub="google-ada", email="ada@example.com", email_verified=True, name="Ada"
            )

        monkeypatch.setattr(FakeGoogleClient, "user_info", verified)
        await google_sign_in(victim)
        me = (await victim.get("/api/auth/me")).json()
        assert me["google_linked"] is True and me["email_verified"] is True
        assert me["has_password"] is False

    # The attacker's password and session no longer work.
    assert (await client.get("/api/auth/me")).status_code == 401
    assert (await login(client, "attackers-password")).status_code == 401
    user = await session.scalar(select(User))
    assert user.password_hash is None
    meta = (
        await session.scalars(select(AuditLog.meta).where(AuditLog.action == "auth.google_login"))
    ).one()
    assert meta["reclaimed"] is True


# ---- Mail port ----------------------------------------------------------------------------------


async def test_smtp_mailer_builds_a_multipart_message_and_uses_starttls():
    mailer = SmtpMailer(
        "smtp.example.com", 587, "user", "pass", "MedSpace <a@b.example>", "starttls"
    )
    with mock.patch("smtplib.SMTP") as smtp:
        server = smtp.return_value
        ok = await mailer.send(Message("ada@example.com", "Hi", "plain body", "<p>html</p>"))
    assert ok is True
    smtp.assert_called_once_with("smtp.example.com", 587, timeout=15)
    server.starttls.assert_called_once()
    server.login.assert_called_once_with("user", "pass")
    sent = server.send_message.call_args.args[0]
    assert sent["To"] == "ada@example.com" and sent["Subject"] == "Hi"
    assert sent.is_multipart()


async def test_smtp_failures_are_reported_not_raised():
    mailer = SmtpMailer("smtp.example.com", 587, None, None, "a@b.example", "starttls")
    with mock.patch("smtplib.SMTP", side_effect=smtplib.SMTPConnectError(421, b"busy")):
        assert await mailer.send(Message("ada@example.com", "Hi", "body")) is False


async def test_dev_outbox_shows_simulated_mail(client: httpx.AsyncClient):
    await signup(client)
    resp = await client.get("/api/dev/outbox", params={"to": "ada@example.com"})
    assert resp.status_code == 200
    [message] = resp.json()
    assert message["links"][0].startswith("http://localhost:5173/verify-email?token=")


async def test_reset_links_can_be_checked_without_using_them(
    client: httpx.AsyncClient, mailbox: FakeMailer
):
    await signup(client)
    await forgot(client)
    token = reset_token(mailbox)

    async def check(t: str) -> bool:
        resp = await client.post("/api/auth/password/reset/check", json={"token": t})
        assert resp.status_code == 200
        return resp.json()["valid"]

    assert await check(token) is True
    assert await check(token) is True  # checking doesn't use it up
    assert await check("x" * 40) is False
    await client.post(
        "/api/auth/password/reset", json={"token": token, "new_password": NEW_PASSWORD}
    )
    assert await check(token) is False
