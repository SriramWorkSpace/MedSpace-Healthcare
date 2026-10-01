from __future__ import annotations

import httpx
from sqlalchemy import select

from app.modules.audit.models import AuditLog
from app.modules.identity.models import RefreshToken
from tests.conftest import BASE_URL, csrf, signup


async def test_signup_sets_cookies_and_returns_user(client: httpx.AsyncClient):
    body = await signup(client)
    assert body["user"]["email"] == "ada@example.com"
    assert body["user"]["dose_times"]["morning"] == "08:00"
    assert body["csrf_token"] == client.cookies["ms_csrf"]
    assert "ms_access" in client.cookies

    me = await client.get("/api/auth/me")
    assert me.status_code == 200
    assert me.json()["display_name"] == "Ada Okonkwo"


async def test_signup_rejects_duplicate_email_case_insensitively(client: httpx.AsyncClient):
    await signup(client)
    resp = await client.post(
        "/api/auth/signup",
        json={"email": "ADA@example.com", "password": "another-long-pass", "display_name": "A"},
    )
    assert resp.status_code == 409
    assert resp.headers["content-type"].startswith("application/problem+json")


async def test_signup_validates_password_length(client: httpx.AsyncClient):
    resp = await client.post(
        "/api/auth/signup",
        json={"email": "x@example.com", "password": "short", "display_name": "X"},
    )
    assert resp.status_code == 422
    assert resp.json()["code"] == "validation_error"


async def test_login_wrong_password_is_generic(client: httpx.AsyncClient):
    await signup(client)
    client.cookies.clear()
    bad = await client.post(
        "/api/auth/login", json={"email": "ada@example.com", "password": "nope-nope-nope"}
    )
    unknown = await client.post(
        "/api/auth/login", json={"email": "who@example.com", "password": "nope-nope-nope"}
    )
    assert bad.status_code == unknown.status_code == 401
    assert bad.json()["detail"] == unknown.json()["detail"]


async def test_me_requires_auth(client: httpx.AsyncClient):
    resp = await client.get("/api/auth/me")
    assert resp.status_code == 401


async def test_refresh_rotates_token(client: httpx.AsyncClient, session):
    await signup(client)
    old_refresh = client.cookies.get("ms_refresh")
    resp = await client.post("/api/auth/refresh", headers=csrf(client))
    assert resp.status_code == 200, resp.text
    assert client.cookies.get("ms_refresh") != old_refresh

    tokens = (await session.scalars(select(RefreshToken))).all()
    assert len(tokens) == 2
    assert sum(t.revoked_at is not None for t in tokens) == 1


async def test_refresh_reuse_revokes_family(client: httpx.AsyncClient, session):
    await signup(client)
    stolen = client.cookies.get("ms_refresh")
    assert (await client.post("/api/auth/refresh", headers=csrf(client))).status_code == 200

    # An attacker replays the old token from another client.
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=client._transport.app), base_url=BASE_URL
    ) as attacker:
        attacker.cookies.set("ms_refresh", stolen, path="/api/auth")
        attacker.cookies.set("ms_csrf", "t")
        replay = await attacker.post("/api/auth/refresh", headers={"X-CSRF-Token": "t"})
    assert replay.status_code == 401

    # The legitimate session's current token is now revoked as well.
    again = await client.post("/api/auth/refresh", headers=csrf(client))
    assert again.status_code == 401

    actions = (await session.scalars(select(AuditLog.action))).all()
    assert "auth.refresh_reuse_detected" in actions


async def test_unsafe_requests_require_csrf(auth_client: httpx.AsyncClient):
    no_token = await auth_client.patch("/api/me", json={"display_name": "Ada L."})
    assert no_token.status_code == 403
    assert no_token.json()["code"] == "csrf_failed"

    ok = await auth_client.patch(
        "/api/me", json={"display_name": "Ada L."}, headers=csrf(auth_client)
    )
    assert ok.status_code == 200
    assert ok.json()["display_name"] == "Ada L."


async def test_profile_rejects_bad_dose_time(auth_client: httpx.AsyncClient):
    resp = await auth_client.patch(
        "/api/me", json={"dose_times": {"morning": "25:00"}}, headers=csrf(auth_client)
    )
    assert resp.status_code == 422


async def test_logout_revokes_session(auth_client: httpx.AsyncClient):
    resp = await auth_client.post("/api/auth/logout", headers=csrf(auth_client))
    assert resp.status_code == 204
    assert "ms_access" not in auth_client.cookies
    assert (await auth_client.get("/api/auth/me")).status_code == 401


async def test_login_is_rate_limited(client: httpx.AsyncClient):
    payload = {"email": "ada@example.com", "password": "wrong-password-x"}
    codes = [(await client.post("/api/auth/login", json=payload)).status_code for _ in range(12)]
    assert codes[-1] == 429


async def test_demo_login_creates_isolated_demo_user(client: httpx.AsyncClient):
    resp = await client.post("/api/auth/demo")
    assert resp.status_code == 201
    user = resp.json()["user"]
    assert user["is_demo"] is True
    assert user["email"].endswith("@demo.medspace.dev")


async def test_audit_trail_lists_own_events(auth_client: httpx.AsyncClient):
    resp = await auth_client.get("/api/audit")
    assert resp.status_code == 200
    assert [i["action"] for i in resp.json()["items"]] == ["auth.signup"]


async def test_security_headers_present(client: httpx.AsyncClient):
    resp = await client.get("/api/health")
    assert resp.headers["x-content-type-options"] == "nosniff"
    assert resp.headers["x-frame-options"] == "DENY"
