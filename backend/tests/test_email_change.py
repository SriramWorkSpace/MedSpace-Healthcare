"""Changing the account email (ADR-033): proof, confirmation by the new inbox, notices."""

from __future__ import annotations

from datetime import timedelta

import httpx
from sqlalchemy import select, update

from app.core import totp
from app.core.db import utcnow
from app.modules.audit.models import AuditLog
from app.modules.identity.models import EmailToken, User
from app.shared.mail import FakeMailer
from tests.conftest import BASE_URL, confirm_email, csrf, link_token, signup

PASSWORD = "correct-horse-battery"
NEW = "ada.new@example.com"


async def change(client: httpx.AsyncClient, **body) -> httpx.Response:
    return await client.post(
        "/api/me/email/change",
        json={"new_email": NEW, "password": PASSWORD, **body},
        headers=csrf(client),
    )


def change_token(box: FakeMailer, to: str = NEW) -> str:
    message = next(m for m in box.latest(to) if "new email" in m.subject)
    return link_token(message.text, "/confirm-email-change")


async def confirm(client: httpx.AsyncClient, token: str) -> httpx.Response:
    return await client.post("/api/auth/email/change/confirm", json={"token": token})


async def test_change_happens_only_when_the_new_inbox_confirms(
    client: httpx.AsyncClient, mailbox: FakeMailer, session
):
    await signup(client)
    mailbox.outbox.clear()
    resp = await change(client)
    assert resp.status_code == 202, resp.text

    # Nothing has changed yet; the old address was told, the new one got the link.
    assert (await client.get("/api/auth/me")).json()["email"] == "ada@example.com"
    assert (await client.get("/api/me/security")).json()["pending_email"] == NEW
    [notice] = mailbox.latest("ada@example.com")
    assert notice.subject == "Someone asked to change your MedSpace email" and NEW in notice.text

    ok = await confirm(client, change_token(mailbox))
    assert ok.status_code == 200
    me = (await client.get("/api/auth/me")).json()
    assert me["email"] == NEW and me["email_verified"] is True
    assert (await client.get("/api/me/security")).json()["pending_email"] is None
    assert "Your MedSpace email was changed" in [
        m.subject for m in mailbox.latest("ada@example.com")
    ]

    # Sign-in now uses the new address.
    client.cookies.clear()
    old = await client.post(
        "/api/auth/login", json={"email": "ada@example.com", "password": PASSWORD}
    )
    assert old.status_code == 401
    new = await client.post("/api/auth/login", json={"email": NEW, "password": PASSWORD})
    assert new.status_code == 200

    actions = set((await session.scalars(select(AuditLog.action))).all())
    assert {"auth.email_change_requested", "auth.email_changed"} <= actions


async def test_change_needs_the_password_and_a_code_with_two_step_on(
    client: httpx.AsyncClient, mailbox: FakeMailer
):
    await signup(client)
    assert (await change(client, password="not-my-password")).status_code == 403
    setup = (await client.post("/api/me/mfa/setup", headers=csrf(client))).json()
    code = totp.code_at(setup["secret"], totp.current_step())
    await client.post("/api/me/mfa/enable", json={"code": code}, headers=csrf(client))
    assert (await change(client)).status_code == 403  # no code
    next_code = totp.code_at(setup["secret"], totp.current_step() + 1)
    assert (await change(client, code=next_code)).status_code == 202


async def test_addresses_already_in_use_and_unchanged_ones_are_refused(
    client: httpx.AsyncClient, mailbox: FakeMailer
):
    await signup(client)
    from app.main import app

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL) as bo:
        await signup(bo, email=NEW, name="Bo")
    assert (await change(client)).status_code == 409
    same = await change(client, new_email="ADA@example.com")
    assert same.status_code == 422


async def test_someone_taking_the_address_meanwhile_blocks_the_change(
    client: httpx.AsyncClient, mailbox: FakeMailer
):
    await signup(client)
    await change(client)
    token = change_token(mailbox)
    from app.main import app

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL) as bo:
        await signup(bo, email=NEW, name="Bo")
    assert (await confirm(client, token)).status_code == 409
    assert (await client.get("/api/auth/me")).json()["email"] == "ada@example.com"


async def test_links_work_once_expire_and_can_be_cancelled(
    client: httpx.AsyncClient, mailbox: FakeMailer, session
):
    await signup(client)
    await change(client)
    first = change_token(mailbox)
    cancelled = await client.delete("/api/me/email/change", headers=csrf(client))
    assert cancelled.status_code == 204
    assert (await confirm(client, first)).status_code == 410

    await change(client)
    second = change_token(mailbox)
    await session.execute(update(EmailToken).values(expires_at=utcnow() - timedelta(minutes=1)))
    await session.commit()
    assert (await confirm(client, second)).status_code == 410
    assert (await client.get("/api/me/security")).json()["pending_email"] is None


async def test_old_links_die_with_the_old_address(client: httpx.AsyncClient, mailbox: FakeMailer):
    await signup(client)  # a confirmation link was sent to the old address
    old_verify = link_token(mailbox.latest("ada@example.com")[-1].text, "/verify-email")
    await change(client)
    assert (await confirm(client, change_token(mailbox))).status_code == 200
    stale = await client.post("/api/auth/email/verify", json={"token": old_verify})
    assert stale.status_code == 410
    # A reset link now goes to the new address only.
    await client.post("/api/auth/password/forgot", json={"email": NEW})
    assert any("Reset" in m.subject for m in mailbox.latest(NEW))


async def test_confirming_works_from_another_browser(client: httpx.AsyncClient, mailbox):
    await signup(client)
    await confirm_email(client, "ada@example.com")
    await change(client)
    token = change_token(mailbox)
    from app.main import app

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url=BASE_URL
    ) as phone:
        assert (await confirm(phone, token)).status_code == 200
    assert (await client.get("/api/auth/me")).json()["email"] == NEW


async def test_demo_accounts_and_accounts_without_a_password(
    client: httpx.AsyncClient, mailbox: FakeMailer, session
):
    await client.post("/api/auth/demo")
    assert (await change(client)).status_code == 403
    client.cookies.clear()

    # A Google-only account (no password yet) is asked to add one first.
    await signup(client)
    await session.execute(update(User).values(password_hash=None))
    await session.commit()
    no_password = await change(client, password=None)
    assert no_password.status_code == 422
    assert "Add a password" in no_password.json()["detail"]
