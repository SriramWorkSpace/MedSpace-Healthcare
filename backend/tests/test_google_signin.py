"""Optional "Continue with Google" sign-in (simulation mode), ADR-017."""

from __future__ import annotations

from urllib.parse import parse_qs, urlparse

import httpx
import pytest
from sqlalchemy import select

from app.modules.identity.models import User
from app.modules.integrations.google import FakeGoogleClient, GoogleIdentity
from app.modules.integrations.models import OAuthConnection
from tests.conftest import confirm_email, csrf, signup


async def google_sign_in(
    client: httpx.AsyncClient, *, code: str | None = None, next: str | None = None
) -> httpx.Response:
    """Run start -> (simulated consent) -> callback. Returns the final redirect."""
    url = "/api/auth/google/start" + (f"?next={next}" if next else "")
    start = await client.get(url, follow_redirects=False)
    assert start.status_code == 302
    location = start.headers["location"]
    if code:
        q = parse_qs(urlparse(location).query)
        location = f"/api/integrations/google/callback?code={code}&state={q['state'][0]}"
    resp = await client.get(location, follow_redirects=False)
    assert resp.status_code in (302, 307)
    return resp


def query(resp: httpx.Response) -> dict[str, str]:
    return {k: v[0] for k, v in parse_qs(urlparse(resp.headers["location"]).query).items()}


async def test_sign_in_creates_account_and_connects_reminders(client: httpx.AsyncClient, session):
    resp = await google_sign_in(client, next="/app/medications")
    assert urlparse(resp.headers["location"]).path == "/app/medications"
    assert query(resp) == {"google": "signed_in", "reminders": "connected"}

    me = (await client.get("/api/auth/session")).json()["user"]
    assert me["google_linked"] is True
    assert me["has_password"] is False
    assert me["is_demo"] is True  # simulated Google accounts expire like demos

    status = (await client.get("/api/integrations/google/status")).json()
    assert status["connected"] is True
    # Simulated sign-ins get the seeded demo records.
    assert len((await client.get("/api/prescriptions")).json()) == 3
    actions = [a["action"] for a in (await client.get("/api/audit")).json()["items"]]
    assert "auth.google_signup" in actions


async def test_sign_in_without_calendar_scopes_connects_later(client: httpx.AsyncClient):
    resp = await google_sign_in(client, code="sim-abc123def0-identityonly")
    assert query(resp)["reminders"] == "later"
    assert (await client.get("/api/auth/session")).json()["user"] is not None
    status = (await client.get("/api/integrations/google/status")).json()
    assert status["connected"] is False

    # Later, from Settings, the user connects reminders on the same account.
    start = await client.get("/api/integrations/google/connect", follow_redirects=False)
    done = await client.get(start.headers["location"], follow_redirects=False)
    assert "google=connected" in done.headers["location"]
    assert (await client.get("/api/integrations/google/status")).json()["connected"] is True


async def test_returning_google_user_gets_the_same_account(client: httpx.AsyncClient, session):
    await google_sign_in(client, code="sim-returning01")
    first = (await client.get("/api/auth/session")).json()["user"]["id"]
    client.cookies.clear()
    await google_sign_in(client, code="sim-returning01")
    second = (await client.get("/api/auth/session")).json()["user"]["id"]
    assert first == second
    assert len((await session.scalars(select(User))).all()) == 1


async def test_verified_google_email_links_existing_password_account(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
):
    await signup(client, email="ada@example.com")
    await confirm_email(client, "ada@example.com")
    original_id = (await client.get("/api/auth/me")).json()["id"]
    client.cookies.clear()

    async def verified(self, access_token):
        return GoogleIdentity(
            sub="google-ada", email="Ada@Example.com", email_verified=True, name="Ada"
        )

    monkeypatch.setattr(FakeGoogleClient, "user_info", verified)
    await google_sign_in(client)
    me = (await client.get("/api/auth/me")).json()
    assert me["id"] == original_id
    assert me["google_linked"] is True and me["has_password"] is True


async def test_unverified_google_email_never_takes_over_an_account(
    client: httpx.AsyncClient, monkeypatch: pytest.MonkeyPatch
):
    await signup(client, email="ada@example.com")
    client.cookies.clear()

    async def unverified(self, access_token):
        return GoogleIdentity(
            sub="attacker", email="ada@example.com", email_verified=False, name="X"
        )

    monkeypatch.setattr(FakeGoogleClient, "user_info", unverified)
    resp = await google_sign_in(client)
    assert urlparse(resp.headers["location"]).path == "/login"
    assert query(resp) == {"google": "email_taken"}
    assert (await client.get("/api/auth/session")).json()["user"] is None


async def test_google_only_accounts_cannot_use_password_login(client: httpx.AsyncClient, session):
    await google_sign_in(client, code="sim-nopassword1")
    email = (await client.get("/api/auth/session")).json()["user"]["email"]
    client.cookies.clear()
    resp = await client.post(
        "/api/auth/login", json={"email": email, "password": "anything-at-all"}
    )
    assert resp.status_code == 401


async def test_next_parameter_cannot_redirect_off_site(client: httpx.AsyncClient):
    for evil in ("//evil.example", "https://evil.example", "/\\evil.example"):
        client.cookies.clear()
        resp = await google_sign_in(client, next=evil)
        assert urlparse(resp.headers["location"]).path == "/app"
        assert "evil" not in resp.headers["location"]


async def test_callback_without_state_cookie_is_rejected(client: httpx.AsyncClient):
    resp = await client.get(
        "/api/integrations/google/callback?code=sim-x&state=y", follow_redirects=False
    )
    assert "google=expired" in resp.headers["location"]


async def test_providers_endpoint_reports_simulation(client: httpx.AsyncClient):
    assert (await client.get("/api/auth/google/providers")).json() == {
        "google": {"enabled": True, "mode": "simulation"}
    }


async def test_google_tokens_are_encrypted_for_signin_connections(
    client: httpx.AsyncClient, session
):
    await google_sign_in(client, code="sim-encrypted01")
    conn = await session.scalar(select(OAuthConnection))
    assert conn is not None and not conn.access_token_enc.startswith("sim-")
    # And signing out works like any other session.
    assert (await client.post("/api/auth/logout", headers=csrf(client))).status_code == 204
