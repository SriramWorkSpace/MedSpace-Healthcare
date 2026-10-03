"""Account security (ADR-029): two-step verification, active sessions, password changes."""

from __future__ import annotations

import time

import httpx
from sqlalchemy import select

from app.core import totp
from app.core.security import create_access_token
from app.modules.audit.models import AuditLog
from app.modules.identity.models import RecoveryCode, User
from tests.conftest import BASE_URL, csrf, signup
from tests.test_google_signin import google_sign_in, query

PASSWORD = "correct-horse-battery"


def code_for(secret: str, offset: int = 0) -> str:
    return totp.code_at(secret, totp.current_step() + offset)


async def turn_on_mfa(client: httpx.AsyncClient) -> tuple[str, list[str]]:
    setup = await client.post("/api/me/mfa/setup", headers=csrf(client))
    assert setup.status_code == 200, setup.text
    body = setup.json()
    assert body["otpauth_uri"].startswith("otpauth://totp/MedSpace")
    assert body["qr_svg"].startswith("data:image/svg+xml")
    secret = body["secret"]
    enabled = await client.post(
        "/api/me/mfa/enable", json={"code": code_for(secret)}, headers=csrf(client)
    )
    assert enabled.status_code == 200, enabled.text
    return secret, enabled.json()["codes"]


async def new_client() -> httpx.AsyncClient:
    from app.main import app

    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL)


# ---- TOTP primitives -----------------------------------------------------------------------------


def test_totp_matches_rfc6238_vectors():
    secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"  # b"12345678901234567890"
    assert totp.code_at(secret, 59 // 30) == "287082"
    assert totp.code_at(secret, 1111111109 // 30) == "081804"
    assert totp.code_at(secret, 1234567890 // 30) == "005924"


def test_totp_accepts_drift_and_refuses_replay():
    secret = totp.new_secret()
    now = time.time()
    step = totp.current_step(now)
    assert totp.verify(secret, totp.code_at(secret, step - 1), now=now) == step - 1
    assert totp.verify(secret, totp.code_at(secret, step - 3), now=now) is None
    assert totp.verify(secret, totp.code_at(secret, step), last_step=step, now=now) is None
    assert totp.verify(secret, "12 34 5", now=now) is None


def test_recovery_codes_are_readable_and_normalised():
    codes = totp.new_recovery_codes()
    assert len(codes) == len(set(codes)) == 10
    assert all(len(c) == 9 and c[4] == "-" for c in codes)
    assert totp.normalize_recovery_code(" ABCD efgh ") == "abcd-efgh"


# ---- Setting up two-step verification ------------------------------------------------------------


async def test_enable_requires_a_matching_code(client: httpx.AsyncClient):
    await signup(client)
    await client.post("/api/me/mfa/setup", headers=csrf(client))
    bad = await client.post("/api/me/mfa/enable", json={"code": "000000"}, headers=csrf(client))
    assert bad.status_code == 422
    state = (await client.get("/api/me/security")).json()
    assert state["mfa_enabled"] is False


async def test_enable_returns_codes_once_and_reports_status(client: httpx.AsyncClient, session):
    await signup(client)
    _secret, codes = await turn_on_mfa(client)
    assert len(codes) == 10
    state = (await client.get("/api/me/security")).json()
    assert state["mfa_enabled"] is True and state["recovery_codes_left"] == 10
    assert (await client.get("/api/auth/me")).json()["mfa_enabled"] is True
    stored = (await session.scalars(select(RecoveryCode.code_hash))).all()
    assert codes[0] not in stored  # only hashes at rest
    again = await client.post("/api/me/mfa/setup", headers=csrf(client))
    assert again.status_code == 409


# ---- Signing in with a second factor -------------------------------------------------------------


async def login(client: httpx.AsyncClient) -> dict:
    resp = await client.post(
        "/api/auth/login", json={"email": "ada@example.com", "password": PASSWORD}
    )
    assert resp.status_code == 200, resp.text
    return resp.json()


async def test_password_alone_does_not_sign_in_once_mfa_is_on(client: httpx.AsyncClient):
    await signup(client)
    secret, _ = await turn_on_mfa(client)
    client.cookies.clear()

    first = await login(client)
    assert first["mfa_required"] is True and first["user"] is None
    assert "ms_access" not in client.cookies
    assert (await client.get("/api/auth/me")).status_code == 401

    done = await client.post(
        "/api/auth/login/mfa", json={"mfa_token": first["mfa_token"], "code": code_for(secret, 1)}
    )
    assert done.status_code == 200, done.text
    assert done.json()["user"]["email"] == "ada@example.com"
    assert (await client.get("/api/auth/me")).status_code == 200


async def test_a_code_cannot_be_used_twice(client: httpx.AsyncClient):
    await signup(client)
    secret, _ = await turn_on_mfa(client)  # consumed the current step
    client.cookies.clear()
    token = (await login(client))["mfa_token"]
    replay = await client.post(
        "/api/auth/login/mfa", json={"mfa_token": token, "code": code_for(secret)}
    )
    assert replay.status_code == 401


async def test_recovery_code_works_exactly_once(client: httpx.AsyncClient):
    await signup(client)
    _secret, codes = await turn_on_mfa(client)
    client.cookies.clear()

    token = (await login(client))["mfa_token"]
    ok = await client.post(
        "/api/auth/login/mfa", json={"mfa_token": token, "recovery_code": codes[0].upper()}
    )
    assert ok.status_code == 200
    assert (await client.get("/api/me/security")).json()["recovery_codes_left"] == 9

    client.cookies.clear()
    token = (await login(client))["mfa_token"]
    reused = await client.post(
        "/api/auth/login/mfa", json={"mfa_token": token, "recovery_code": codes[0]}
    )
    assert reused.status_code == 401


async def test_mfa_token_must_be_genuine(client: httpx.AsyncClient, session):
    await signup(client)
    secret, _ = await turn_on_mfa(client)
    client.cookies.clear()
    forged = await client.post(
        "/api/auth/login/mfa", json={"mfa_token": "x" * 40, "code": code_for(secret, 1)}
    )
    assert forged.status_code == 401
    # An access token is not an MFA token, even for the right user.
    me = (await session.scalars(select(User))).one()
    wrong_kind = create_access_token(me.id)
    resp = await client.post(
        "/api/auth/login/mfa", json={"mfa_token": wrong_kind, "code": code_for(secret, 1)}
    )
    assert resp.status_code == 401


async def test_mfa_attempts_are_limited_per_account(client: httpx.AsyncClient):
    await signup(client)
    secret, _ = await turn_on_mfa(client)
    client.cookies.clear()
    token = (await login(client))["mfa_token"]
    for _ in range(5):
        resp = await client.post("/api/auth/login/mfa", json={"mfa_token": token, "code": "000000"})
        assert resp.status_code == 401
    blocked = await client.post(
        "/api/auth/login/mfa", json={"mfa_token": token, "code": code_for(secret, 1)}
    )
    assert blocked.status_code == 429


async def test_google_sign_in_also_asks_for_the_second_factor(client: httpx.AsyncClient):
    await google_sign_in(client, code="sim-returning02")  # a Google-only account
    secret, _ = await turn_on_mfa(client)
    client.cookies.clear()

    resp = await google_sign_in(client, code="sim-returning02")
    q = query(resp)
    assert resp.headers["location"].split("?")[0].endswith("/login")
    assert "mfa" in q and "google" not in q
    assert (await client.get("/api/auth/me")).status_code == 401

    done = await client.post(
        "/api/auth/login/mfa", json={"mfa_token": q["mfa"], "code": code_for(secret, 1)}
    )
    assert done.status_code == 200


# ---- Turning it off, new codes -------------------------------------------------------------------


async def test_disable_needs_password_and_a_code(client: httpx.AsyncClient, session):
    await signup(client)
    secret, codes = await turn_on_mfa(client)
    no_pw = await client.post(
        "/api/me/mfa/disable", json={"code": code_for(secret, 1)}, headers=csrf(client)
    )
    assert no_pw.status_code == 403
    no_code = await client.post(
        "/api/me/mfa/disable", json={"password": PASSWORD}, headers=csrf(client)
    )
    assert no_code.status_code == 403
    ok = await client.post(
        "/api/me/mfa/disable",
        json={"password": PASSWORD, "recovery_code": codes[3]},
        headers=csrf(client),
    )
    assert ok.status_code == 204
    state = (await client.get("/api/me/security")).json()
    assert state["mfa_enabled"] is False and state["recovery_codes_left"] == 0
    actions = (await session.scalars(select(AuditLog.action))).all()
    assert "mfa.enabled" in actions and "mfa.disabled" in actions

    client.cookies.clear()
    assert (await login(client))["mfa_required"] is False


async def test_regenerating_codes_retires_the_old_ones(client: httpx.AsyncClient):
    await signup(client)
    secret, old = await turn_on_mfa(client)
    resp = await client.post(
        "/api/me/mfa/recovery-codes", json={"code": code_for(secret, 1)}, headers=csrf(client)
    )
    assert resp.status_code == 200
    new = resp.json()["codes"]
    assert set(new).isdisjoint(old)
    client.cookies.clear()
    token = (await login(client))["mfa_token"]
    stale = await client.post(
        "/api/auth/login/mfa", json={"mfa_token": token, "recovery_code": old[0]}
    )
    assert stale.status_code == 401


# ---- Sessions ------------------------------------------------------------------------------------


async def test_sessions_list_marks_this_device(client: httpx.AsyncClient):
    await signup(client)
    other = await new_client()
    async with other:
        await other.post(
            "/api/auth/login",
            json={"email": "ada@example.com", "password": PASSWORD},
            headers={"User-Agent": "Mozilla/5.0 (iPhone) Safari/604.1"},
        )
        sessions = (await client.get("/api/me/security")).json()["sessions"]
        assert len(sessions) == 2
        assert sessions[0]["current"] is True
        assert sessions[1]["device"] == "Safari on iPhone"


async def test_revoking_a_session_signs_that_device_out_immediately(client: httpx.AsyncClient):
    await signup(client)
    other = await new_client()
    async with other:
        await other.post("/api/auth/login", json={"email": "ada@example.com", "password": PASSWORD})
        assert (await other.get("/api/auth/me")).status_code == 200

        sessions = (await client.get("/api/me/security")).json()["sessions"]
        target = next(s for s in sessions if not s["current"])
        resp = await client.delete(f"/api/me/sessions/{target['id']}", headers=csrf(client))
        assert resp.status_code == 204

        # Its access token is still within its TTL, but the session behind it is gone.
        assert (await other.get("/api/auth/me")).status_code == 401
        assert (await other.get("/api/auth/session")).json()["user"] is None
        refresh = await other.post("/api/auth/refresh", headers=csrf(other))
        assert refresh.status_code == 401
        assert (await client.get("/api/auth/me")).status_code == 200

        again = await client.delete(f"/api/me/sessions/{target['id']}", headers=csrf(client))
        assert again.status_code == 404


async def test_cannot_revoke_someone_elses_session(client: httpx.AsyncClient):
    await signup(client)
    mine = (await client.get("/api/me/security")).json()["sessions"][0]["id"]
    other = await new_client()
    async with other:
        await signup(other, email="bo@example.com")
        resp = await other.delete(f"/api/me/sessions/{mine}", headers=csrf(other))
        assert resp.status_code == 404
    assert (await client.get("/api/auth/me")).status_code == 200


async def test_sign_out_everywhere_else(client: httpx.AsyncClient):
    await signup(client)
    others = [await new_client() for _ in range(2)]
    for c in others:
        await c.post("/api/auth/login", json={"email": "ada@example.com", "password": PASSWORD})
    resp = await client.post("/api/me/sessions/sign-out-others", headers=csrf(client))
    assert resp.json() == {"signed_out": 2}
    for c in others:
        assert (await c.get("/api/auth/me")).status_code == 401
        await c.aclose()
    assert (await client.get("/api/auth/me")).status_code == 200


# ---- Password ------------------------------------------------------------------------------------


async def test_change_password_signs_out_other_devices(client: httpx.AsyncClient):
    await signup(client)
    other = await new_client()
    async with other:
        await other.post("/api/auth/login", json={"email": "ada@example.com", "password": PASSWORD})
        wrong = await client.post(
            "/api/me/password",
            json={"current_password": "not-my-password", "new_password": "a-brand-new-pass"},
            headers=csrf(client),
        )
        assert wrong.status_code == 403
        same = await client.post(
            "/api/me/password",
            json={"current_password": PASSWORD, "new_password": PASSWORD},
            headers=csrf(client),
        )
        assert same.status_code == 422
        ok = await client.post(
            "/api/me/password",
            json={"current_password": PASSWORD, "new_password": "a-brand-new-pass"},
            headers=csrf(client),
        )
        assert ok.json() == {"signed_out": 1}
        assert (await other.get("/api/auth/me")).status_code == 401
    assert (await client.get("/api/auth/me")).status_code == 200

    client.cookies.clear()
    old = await client.post(
        "/api/auth/login", json={"email": "ada@example.com", "password": PASSWORD}
    )
    assert old.status_code == 401
    new = await client.post(
        "/api/auth/login", json={"email": "ada@example.com", "password": "a-brand-new-pass"}
    )
    assert new.status_code == 200


async def test_google_only_account_can_set_a_first_password(client: httpx.AsyncClient):
    await google_sign_in(client)
    state = (await client.get("/api/me/security")).json()
    assert state["has_password"] is False
    resp = await client.post(
        "/api/me/password", json={"new_password": "my-first-password"}, headers=csrf(client)
    )
    assert resp.status_code == 200
    assert (await client.get("/api/me/security")).json()["has_password"] is True
