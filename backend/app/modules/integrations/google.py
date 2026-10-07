"""Google OAuth + Calendar v3 + Tasks v1 behind a small port, with an in-memory simulation.

`GOOGLE_PROVIDER=fake` (default) lets every demo visitor "connect" a simulated account, so the
whole sync flow is explorable without Google credentials or consent-screen verification.
"""

from __future__ import annotations

import base64
import hashlib
import secrets
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from functools import lru_cache
from typing import Any, Protocol
from urllib.parse import urlencode

import httpx

from app.core.config import get_settings

IDENTITY_SCOPES = ["openid", "email", "profile"]
SYNC_SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/tasks",
]
SCOPES = IDENTITY_SCOPES + SYNC_SCOPES


def has_sync_scopes(granted: str) -> bool:
    """True when the user left both Calendar and Tasks ticked on Google's consent screen."""
    have = set(granted.split())
    return all(scope in have for scope in SYNC_SCOPES)


AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"  # noqa: S105 (URL, not a secret)
REVOKE_URL = "https://oauth2.googleapis.com/revoke"
USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
CAL = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
TASKS = "https://tasks.googleapis.com/tasks/v1"


class GoogleAuthError(Exception):
    """Consent was revoked or the refresh token is no longer valid."""


class GoogleAPIError(Exception):
    pass


@dataclass
class GoogleIdentity:
    sub: str
    email: str
    email_verified: bool
    name: str | None


@dataclass
class Tokens:
    access_token: str
    refresh_token: str | None
    expires_at: datetime
    scope: str


def pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=")
    return verifier, challenge.decode()


class GoogleClient(Protocol):
    mode: str

    def auth_url(self, state: str, code_challenge: str, *, sign_in: bool = False) -> str: ...
    async def exchange_code(self, code: str, verifier: str) -> Tokens: ...
    async def user_info(self, access_token: str) -> GoogleIdentity: ...
    async def refresh(self, refresh_token: str) -> Tokens: ...
    async def revoke(self, token: str) -> None: ...
    async def user_email(self, access_token: str) -> str | None: ...
    async def upsert_event(self, access: str, event_id: str | None, body: dict) -> str: ...
    async def delete_event(self, access: str, event_id: str) -> None: ...
    async def ensure_tasklist(self, access: str, tasklist_id: str | None, title: str) -> str: ...
    async def upsert_task(
        self, access: str, tasklist: str, task_id: str | None, body: dict
    ) -> str: ...
    async def delete_task(self, access: str, tasklist: str, task_id: str) -> None: ...
    async def task_completed(self, access: str, tasklist: str, task_id: str) -> bool | None: ...


def _tokens(payload: dict[str, Any], refresh_token: str | None = None) -> Tokens:
    return Tokens(
        access_token=payload["access_token"],
        refresh_token=payload.get("refresh_token") or refresh_token,
        expires_at=datetime.now(UTC) + timedelta(seconds=int(payload.get("expires_in", 3600))),
        scope=payload.get("scope", " ".join(SCOPES)),
    )


class HttpGoogleClient:
    mode = "live"

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.http = httpx.AsyncClient(timeout=20)

    def auth_url(self, state: str, code_challenge: str, *, sign_in: bool = False) -> str:
        return (
            AUTH_URL
            + "?"
            + urlencode(
                {
                    "client_id": self.client_id,
                    "redirect_uri": self.redirect_uri,
                    "response_type": "code",
                    "scope": " ".join(SCOPES),
                    "access_type": "offline",
                    # Sign-in lets people pick an account; consent guarantees a refresh token.
                    "prompt": "select_account consent" if sign_in else "consent",
                    "include_granted_scopes": "true",
                    "state": state,
                    "code_challenge": code_challenge,
                    "code_challenge_method": "S256",
                }
            )
        )

    async def _token_request(self, data: dict[str, str]) -> dict:
        resp = await self.http.post(
            TOKEN_URL,
            data={**data, "client_id": self.client_id, "client_secret": self.client_secret},
        )
        if resp.status_code == 400 and "invalid_grant" in resp.text:
            raise GoogleAuthError("Google access was revoked.")
        if resp.status_code >= 400:
            raise GoogleAPIError(f"Token endpoint returned {resp.status_code}")
        return resp.json()

    async def exchange_code(self, code: str, verifier: str) -> Tokens:
        payload = await self._token_request(
            {
                "code": code,
                "code_verifier": verifier,
                "grant_type": "authorization_code",
                "redirect_uri": self.redirect_uri,
            }
        )
        return _tokens(payload)

    async def refresh(self, refresh_token: str) -> Tokens:
        payload = await self._token_request(
            {"refresh_token": refresh_token, "grant_type": "refresh_token"}
        )
        return _tokens(payload, refresh_token)

    async def revoke(self, token: str) -> None:
        await self.http.post(REVOKE_URL, params={"token": token})

    async def _call(
        self, method: str, url: str, access: str, json: dict | None = None
    ) -> dict | None:
        resp = await self.http.request(
            method, url, json=json, headers={"Authorization": f"Bearer {access}"}
        )
        if resp.status_code == 401:
            raise GoogleAuthError("Google rejected the access token.")
        if resp.status_code == 404 and method in ("DELETE", "GET"):
            return None
        if resp.status_code == 410 and method == "DELETE":  # already deleted
            return None
        if resp.status_code >= 400:
            raise GoogleAPIError(
                f"Google API {method} {url} -> {resp.status_code}: {resp.text[:200]}"
            )
        return resp.json() if resp.content else None

    async def user_info(self, access_token: str) -> GoogleIdentity:
        data = await self._call("GET", USERINFO_URL, access_token)
        if not data or not data.get("sub") or not data.get("email"):
            raise GoogleAPIError("Google did not return an identity.")
        return GoogleIdentity(
            sub=str(data["sub"]),
            email=data["email"],
            email_verified=bool(data.get("email_verified")),
            name=data.get("name"),
        )

    async def user_email(self, access_token: str) -> str | None:
        return (await self.user_info(access_token)).email

    async def upsert_event(self, access: str, event_id: str | None, body: dict) -> str:
        if event_id:
            data = await self._call("PUT", f"{CAL}/{event_id}", access, body)
            if data:
                return data["id"]
        data = await self._call("POST", CAL, access, body)
        return data["id"]

    async def delete_event(self, access: str, event_id: str) -> None:
        await self._call("DELETE", f"{CAL}/{event_id}", access)

    async def ensure_tasklist(self, access: str, tasklist_id: str | None, title: str) -> str:
        if tasklist_id and await self._call(
            "GET", f"{TASKS}/users/@me/lists/{tasklist_id}", access
        ):
            return tasklist_id
        data = await self._call("POST", f"{TASKS}/users/@me/lists", access, {"title": title})
        return data["id"]

    async def upsert_task(self, access: str, tasklist: str, task_id: str | None, body: dict) -> str:
        if task_id:
            data = await self._call(
                "PATCH", f"{TASKS}/lists/{tasklist}/tasks/{task_id}", access, body
            )
            if data:
                return data["id"]
        data = await self._call("POST", f"{TASKS}/lists/{tasklist}/tasks", access, body)
        return data["id"]

    async def delete_task(self, access: str, tasklist: str, task_id: str) -> None:
        await self._call("DELETE", f"{TASKS}/lists/{tasklist}/tasks/{task_id}", access)

    async def task_completed(self, access: str, tasklist: str, task_id: str) -> bool | None:
        data = await self._call("GET", f"{TASKS}/lists/{tasklist}/tasks/{task_id}", access)
        return None if data is None else data.get("status") == "completed"


class FakeGoogleClient:
    """In-memory Google for demos and tests. State is per access token and per process.

    Each simulated consent produces a distinct Google account (encoded in the code), so demo
    visitors never share an identity. A code ending in "-identityonly" simulates a user who
    unticked Calendar and Tasks on the consent screen.
    """

    mode = "simulation"
    store: dict[str, dict[str, dict]] = {}

    def auth_url(self, state: str, code_challenge: str, *, sign_in: bool = False) -> str:
        return f"/api/integrations/google/callback?code=sim-{uuid.uuid4().hex[:10]}&state={state}"

    async def exchange_code(self, code: str, verifier: str) -> Tokens:
        identity_only = code.endswith("-identityonly")
        account = code.removeprefix("sim-").removesuffix("-identityonly") or uuid.uuid4().hex[:10]
        return Tokens(
            access_token=f"sim-access-{account}",
            refresh_token=f"sim-refresh-{account}",
            expires_at=datetime.now(UTC) + timedelta(hours=1),
            scope=" ".join(IDENTITY_SCOPES if identity_only else SCOPES),
        )

    async def user_info(self, access_token: str) -> GoogleIdentity:
        account = access_token.removeprefix("sim-access-")
        return GoogleIdentity(
            sub=f"sim-{account}",
            email=f"you.{account[:8]}@gmail.simulated",
            email_verified=True,
            name="Sam Rivera",
        )

    async def refresh(self, refresh_token: str) -> Tokens:
        if refresh_token.startswith("sim-revoked"):
            raise GoogleAuthError("Simulated revocation.")
        account = refresh_token.removeprefix("sim-refresh-")
        return Tokens(
            f"sim-access-{account}",
            refresh_token,
            datetime.now(UTC) + timedelta(hours=1),
            " ".join(SCOPES),
        )

    async def revoke(self, token: str) -> None:
        return None

    def _bucket(self, access: str) -> dict[str, dict]:
        account = access.removeprefix("sim-access-")
        return self.store.setdefault(account, {"events": {}, "lists": {}, "tasks": {}})

    async def user_email(self, access_token: str) -> str | None:
        return (await self.user_info(access_token)).email

    async def upsert_event(self, access: str, event_id: str | None, body: dict) -> str:
        events = self._bucket(access)["events"]
        event_id = event_id if event_id in events else f"evt_{uuid.uuid4().hex[:12]}"
        events[event_id] = body
        return event_id

    async def delete_event(self, access: str, event_id: str) -> None:
        self._bucket(access)["events"].pop(event_id, None)

    async def ensure_tasklist(self, access: str, tasklist_id: str | None, title: str) -> str:
        lists = self._bucket(access)["lists"]
        if tasklist_id in lists:
            return tasklist_id
        new_id = f"list_{uuid.uuid4().hex[:8]}"
        lists[new_id] = {"title": title}
        return new_id

    async def upsert_task(self, access: str, tasklist: str, task_id: str | None, body: dict) -> str:
        tasks = self._bucket(access)["tasks"]
        task_id = task_id if task_id in tasks else f"task_{uuid.uuid4().hex[:12]}"
        tasks[task_id] = {**tasks.get(task_id, {}), **body, "tasklist": tasklist}
        return task_id

    async def delete_task(self, access: str, tasklist: str, task_id: str) -> None:
        self._bucket(access)["tasks"].pop(task_id, None)

    async def task_completed(self, access: str, tasklist: str, task_id: str) -> bool | None:
        task = self._bucket(access)["tasks"].get(task_id)
        return None if task is None else task.get("status") == "completed"


def live_configured() -> bool:
    s = get_settings()
    return bool(
        s.google_provider == "google"
        and s.google_client_id
        and s.google_client_secret
        and s.google_client_secret.get_secret_value()
    )


@lru_cache
def _live() -> HttpGoogleClient:
    s = get_settings()
    return HttpGoogleClient(
        s.google_client_id, s.google_client_secret.get_secret_value(), s.google_redirect_uri
    )


@lru_cache
def _simulation() -> FakeGoogleClient:
    return FakeGoogleClient()


def get_google() -> GoogleClient:
    """The server's Google: real OAuth when configured, else the simulation (development)."""
    return _live() if live_configured() else _simulation()


def client_for_mode(mode: str) -> GoogleClient:
    """The client that issued a connection's tokens: a simulated connection never reaches real
    Google, and a live one never falls back to the simulation."""
    if mode == "simulation":
        return _simulation()
    if not live_configured():
        raise GoogleAPIError("Google OAuth isn't configured on this server.")
    return _live()


def client_for_user(user: Any) -> GoogleClient:
    """Demo accounts always use the simulation: their data is synthetic and deleted within a day,
    and in OAuth testing mode Google would block them anyway."""
    return _simulation() if getattr(user, "is_demo", False) else get_google()
