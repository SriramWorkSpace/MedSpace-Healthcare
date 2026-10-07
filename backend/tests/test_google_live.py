"""Real Google OAuth 2.0 (GOOGLE_PROVIDER=google), with Google's HTTP endpoints mocked.

The simulation is covered in test_integrations.py; here the production client builds the real
requests (PKCE, offline access, token refresh, Calendar and Tasks calls) and the routing keeps
demo accounts on the simulation and real accounts on Google.
"""

from __future__ import annotations

import json
from urllib.parse import parse_qs, urlparse

import httpx
import pytest
from sqlalchemy import select

from app.core.config import Settings, get_settings
from app.core.security import decrypt
from app.modules.demo import service as demo
from app.modules.identity.models import User
from app.modules.integrations import google
from app.modules.integrations.google import (
    SCOPES,
    TOKEN_URL,
    USERINFO_URL,
    GoogleAuthError,
    HttpGoogleClient,
)
from app.modules.integrations.models import OAuthConnection
from tests.conftest import csrf
from tests.test_security_hardening import GOOD_PROD


class FakeGoogleHTTP:
    """Records every request and answers like Google's OAuth, Calendar and Tasks endpoints."""

    def __init__(self) -> None:
        self.calls: list[httpx.Request] = []
        self.refresh_fails = False
        self.events = 0
        self.tasks = 0

    def __call__(self, req: httpx.Request) -> httpx.Response:
        self.calls.append(req)
        url = str(req.url)
        if url == TOKEN_URL:
            form = parse_qs(req.content.decode())
            if form["grant_type"] == ["refresh_token"] and self.refresh_fails:
                return httpx.Response(400, json={"error": "invalid_grant"})
            return httpx.Response(
                200,
                json={
                    "access_token": "live-access",
                    "refresh_token": "live-refresh",
                    "expires_in": 3600,
                    "scope": " ".join(SCOPES),
                },
            )
        if url.startswith(USERINFO_URL):
            if req.headers["authorization"] != "Bearer live-access":
                return httpx.Response(401)
            return httpx.Response(
                200, json={"sub": "g-1", "email": "tester@gmail.com", "email_verified": True}
            )
        if "oauth2.googleapis.com/revoke" in url:
            return httpx.Response(200)
        if "/calendar/v3/" in url and req.method == "POST":
            self.events += 1
            return httpx.Response(200, json={"id": f"evt{self.events}"})
        if "/tasks/v1/users/@me/lists" in url and req.method == "POST":
            return httpx.Response(200, json={"id": "list1"})
        if "/tasks/v1/lists/" in url and req.method == "POST":
            self.tasks += 1
            return httpx.Response(200, json={"id": f"task{self.tasks}"})
        if req.method == "DELETE":
            return httpx.Response(204)
        return httpx.Response(404)

    def to(self, part: str) -> list[httpx.Request]:
        return [c for c in self.calls if part in str(c.url)]


@pytest.fixture
def live(monkeypatch) -> FakeGoogleHTTP:
    """Configure real Google OAuth, with Google's servers replaced by FakeGoogleHTTP."""
    s = get_settings()
    monkeypatch.setattr(s, "google_provider", "google")
    monkeypatch.setattr(s, "google_client_id", "client-123.apps.googleusercontent.com")
    monkeypatch.setattr(s, "google_client_secret", type(s.jwt_secret)("shh-client-secret"))
    google._live.cache_clear()
    fake = FakeGoogleHTTP()
    google._live().http = httpx.AsyncClient(transport=httpx.MockTransport(fake))
    yield fake
    google._live.cache_clear()


async def connect_live(client: httpx.AsyncClient) -> str:
    start = await client.get("/api/integrations/google/connect", follow_redirects=False)
    location = start.headers["location"]
    assert location.startswith("https://accounts.google.com/o/oauth2/v2/auth?")
    state = parse_qs(urlparse(location).query)["state"][0]
    done = await client.get(
        f"/api/integrations/google/callback?code=auth-code&state={state}", follow_redirects=False
    )
    return done.headers["location"]


# ---- The production client builds correct OAuth requests ---------------------------------------


def test_auth_url_uses_pkce_offline_access_and_least_scopes():
    c = HttpGoogleClient("cid", "secret", "https://site.example/api/integrations/google/callback")
    q = parse_qs(urlparse(c.auth_url("st", "challenge")).query)
    assert q["client_id"] == ["cid"]
    assert q["redirect_uri"] == ["https://site.example/api/integrations/google/callback"]
    assert q["code_challenge_method"] == ["S256"] and q["code_challenge"] == ["challenge"]
    assert q["access_type"] == ["offline"]  # a refresh token, so reminders sync later
    assert q["prompt"] == ["consent"]
    assert set(q["scope"][0].split()) == {
        "openid",
        "email",
        "profile",
        "https://www.googleapis.com/auth/calendar.events",  # events only, not all calendars
        "https://www.googleapis.com/auth/tasks",
    }
    assert "secret" not in c.auth_url("st", "challenge")


async def test_token_exchange_sends_the_verifier_and_refresh_detects_revocation(live):
    c = google._live()
    tokens = await c.exchange_code("auth-code", "the-verifier")
    form = parse_qs(live.to("oauth2.googleapis.com/token")[0].content.decode())
    assert form["code_verifier"] == ["the-verifier"]
    assert form["grant_type"] == ["authorization_code"]
    assert tokens.refresh_token == "live-refresh"
    live.refresh_fails = True
    with pytest.raises(GoogleAuthError):
        await c.refresh("live-refresh")


# ---- Real accounts use real Google; demo accounts stay simulated -------------------------------


async def test_real_account_connects_to_real_google(auth_client, session, live):
    providers = (await auth_client.get("/api/auth/google/providers")).json()["google"]
    assert providers == {"enabled": True, "mode": "live", "testers_only": True}

    assert "google=connected" in await connect_live(auth_client)
    status = (await auth_client.get("/api/integrations/google/status")).json()
    assert status["connected"] and status["mode"] == "live" and status["testers_only"]
    assert status["email"] == "tester@gmail.com"

    conn = await session.scalar(select(OAuthConnection))
    assert conn.mode == "live"
    assert decrypt(conn.refresh_token_enc) == "live-refresh"
    assert "live-refresh" not in conn.refresh_token_enc  # encrypted at rest


async def test_confirmed_prescription_syncs_to_google_calendar_and_tasks(
    auth_client, session, live
):
    user = await session.scalar(select(User).where(User.email == "ada@example.com"))
    await demo.seed(session, user)
    await session.commit()
    await connect_live(auth_client)

    rx = next(
        r
        for r in (await auth_client.get("/api/prescriptions")).json()
        if r["prescriber_name"] == "Dr. Imani Oduya"
    )
    resp = await auth_client.post(
        "/api/integrations/google/sync",
        json={"prescription_id": rx["id"]},
        headers=csrf(auth_client),
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["events"] == live.events > 0
    assert resp.json()["tasks"] == live.tasks > 0

    event = json.loads(live.to("/calendar/v3/calendars/primary/events")[0].content)
    assert event["summary"].startswith("Take ")
    assert event["recurrence"][0].startswith("RRULE:")
    assert event["start"]["timeZone"]
    for call in live.to("googleapis.com/calendar") + live.to("tasks.googleapis.com"):
        assert call.headers["authorization"] == "Bearer live-access"


async def test_demo_accounts_stay_on_the_simulation(client, session, live):
    await client.post("/api/auth/demo")
    status = (await client.get("/api/integrations/google/status")).json()
    assert status["mode"] == "simulation" and not status["testers_only"]
    start = await client.get("/api/integrations/google/connect", follow_redirects=False)
    assert start.headers["location"].startswith("/api/integrations/google/callback?code=sim-")
    await client.get(start.headers["location"], follow_redirects=False)
    conn = await session.scalar(select(OAuthConnection))
    assert conn.mode == "simulation"
    assert not live.calls  # nothing reached Google


async def test_an_expired_grant_asks_to_reconnect(auth_client, session, live):
    await connect_live(auth_client)
    conn = await session.scalar(select(OAuthConnection))
    conn.expires_at = None  # force a refresh
    conn.tasklist_id = "list1"  # something was synced before
    await session.commit()
    live.refresh_fails = True  # testing-mode grants expire after 7 days
    resp = await auth_client.post("/api/integrations/google/pull", headers=csrf(auth_client))
    assert resp.status_code == 409
    status = (await auth_client.get("/api/integrations/google/status")).json()
    assert status["status"] == "revoked" and not status["connected"]


async def test_deleting_the_account_revokes_google_access(auth_client, live):
    await connect_live(auth_client)
    resp = await auth_client.delete("/api/me", headers=csrf(auth_client))
    assert resp.status_code == 204
    revokes = live.to("oauth2.googleapis.com/revoke")
    assert len(revokes) == 1 and revokes[0].url.params["token"] == "live-refresh"


async def test_live_connections_never_fall_back_to_the_simulation(
    auth_client, session, live, monkeypatch
):
    await connect_live(auth_client)
    conn = await session.scalar(select(OAuthConnection))
    conn.tasklist_id = "list1"
    await session.commit()
    monkeypatch.setattr(get_settings(), "google_provider", "fake")  # credentials removed
    resp = await auth_client.post("/api/integrations/google/pull", headers=csrf(auth_client))
    assert resp.status_code == 409
    assert "isn't available" in resp.json()["detail"]


def test_production_requires_google_credentials_when_google_is_on():
    with pytest.raises(ValueError, match="GOOGLE_CLIENT_ID"):
        Settings(_env_file=None, **GOOD_PROD, google_provider="google")
    ok = Settings(
        _env_file=None,
        **GOOD_PROD,
        google_provider="google",
        google_client_id="cid",
        google_client_secret="secret",
    )
    assert ok.google_provider == "google"
