from __future__ import annotations

import logging
import secrets
import uuid
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.deps import CurrentUser, DbSession, OptionalUser
from app.core.errors import Conflict
from app.core.ratelimit import rate_limit
from app.core.security import JWT_ALG, constant_time_equals
from app.modules.audit import service as audit
from app.modules.demo import service as demo
from app.modules.identity import security as identity_security
from app.modules.identity import service as identity
from app.modules.identity.cookies import set_auth_cookies
from app.modules.integrations import service
from app.modules.integrations.google import (
    GoogleAPIError,
    GoogleAuthError,
    GoogleClient,
    client_for_mode,
    client_for_user,
    get_google,
    has_sync_scopes,
    pkce_pair,
)
from app.shared.queue import enqueue

logger = logging.getLogger("medspace.integrations")
router = APIRouter(prefix="/integrations/google", tags=["integrations"])
auth_router = APIRouter(prefix="/auth/google", tags=["auth"])

STATE_COOKIE = "ms_oauth"


class StatusOut(BaseModel):
    connected: bool
    status: str | None = None
    mode: str
    email: str | None = None
    connected_at: datetime | None = None
    # Google's OAuth app is in testing mode: only test users listed in Google Cloud can connect.
    testers_only: bool = False


class SyncIn(BaseModel):
    prescription_id: uuid.UUID
    calendar: bool = True
    tasks: bool = True


@router.get("/status", response_model=StatusOut)
async def status(user: CurrentUser, session: DbSession):
    conn = await service.get_connection(session, user.id)
    mode = conn.mode if conn else client_for_user(user).mode
    testers_only = mode == "live" and get_settings().google_oauth_testing
    if conn is None:
        return StatusOut(connected=False, mode=mode, testers_only=testers_only)
    return StatusOut(
        connected=conn.status == "active",
        status=conn.status,
        mode=conn.mode,
        email=conn.account_email,
        connected_at=conn.created_at,
        testers_only=testers_only,
    )


def _signed_state(claims: dict) -> str:
    s = get_settings()
    return jwt.encode(
        {**claims, "exp": datetime.now(UTC) + timedelta(minutes=10)},
        s.jwt_secret.get_secret_value(),
        algorithm=JWT_ALG,
    )


def _redirect_to_google(claims: dict, *, sign_in: bool, google: GoogleClient) -> RedirectResponse:
    """Start OAuth (PKCE). State, verifier, intent and the client used ride in a short-lived
    signed cookie, so the callback finishes with the same client that started."""
    verifier, challenge = pkce_pair()
    state = secrets.token_urlsafe(24)
    resp = RedirectResponse(google.auth_url(state, challenge, sign_in=sign_in), status_code=302)
    resp.set_cookie(
        STATE_COOKIE,
        _signed_state({**claims, "state": state, "verifier": verifier, "g": google.mode}),
        max_age=600,
        httponly=True,
        secure=get_settings().cookie_secure,
        samesite="lax",
        path="/api/integrations/google",
    )
    return resp


def safe_next(value: str | None) -> str:
    """Only same-site relative paths, never `//host` or absolute URLs (open-redirect guard)."""
    if not value or not value.startswith("/") or value.startswith("//") or "\\" in value:
        return "/app"
    return value


def _frontend(path: str, **params: str) -> str:
    sep = "&" if "?" in path else "?"
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{get_settings().frontend_url}{path}{sep + query if query else ''}"


@router.get("/connect")
async def connect(user: CurrentUser):
    """Connect Google to an existing MedSpace account (reminders only)."""
    return _redirect_to_google(
        {"mode": "connect", "sub": str(user.id)}, sign_in=False, google=client_for_user(user)
    )


@auth_router.get("/start", dependencies=[Depends(rate_limit("auth:google", 20, 60, by="ip"))])
async def google_sign_in(next: str | None = None):
    """Sign in (or sign up) with Google, asking for Calendar and Tasks in the same consent."""
    return _redirect_to_google(
        {"mode": "login", "next": safe_next(next)}, sign_in=True, google=get_google()
    )


@auth_router.get("/providers")
async def providers():
    mode = get_google().mode
    testers_only = mode == "live" and get_settings().google_oauth_testing
    return {"google": {"enabled": True, "mode": mode, "testers_only": testers_only}}


@router.get("/callback")
async def callback(
    request: Request,
    user: OptionalUser,
    session: DbSession,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
):
    s = get_settings()
    try:
        claims = jwt.decode(
            request.cookies.get(STATE_COOKIE, ""),
            s.jwt_secret.get_secret_value(),
            algorithms=[JWT_ALG],
        )
    except jwt.PyJWTError:
        claims = {}
    mode = claims.get("mode", "connect")
    fail_page = "/login" if mode == "login" else "/app/settings"

    def fail(reason: str) -> RedirectResponse:
        resp = RedirectResponse(_frontend(fail_page, google=reason))
        resp.delete_cookie(STATE_COOKIE, path="/api/integrations/google")
        return resp

    if error:
        return fail("denied")
    if not claims:
        return fail("expired")
    if not code or not constant_time_equals(claims.get("state"), state):
        return fail("error")

    try:
        google = client_for_mode(claims.get("g") or get_google().mode)
        tokens = await google.exchange_code(code, claims["verifier"])
        who = await google.user_info(tokens.access_token)
    except (GoogleAPIError, GoogleAuthError):
        logger.exception("google token exchange failed")
        return fail("error")
    sync_granted = has_sync_scopes(tokens.scope)

    if mode == "login":
        try:
            account, outcome = await identity.login_with_google(
                session,
                sub=who.sub,
                email=who.email,
                email_verified=who.email_verified,
                name=who.name,
                is_demo=google.mode == "simulation",
            )
        except Conflict:
            return fail("email_taken")
        seeded = outcome == "created" and google.mode == "simulation"
        if seeded:
            await demo.seed_quietly(session, account)  # simulated sign-ins get the demo records
        if account.mfa_enabled:
            # Google proved the first factor; the account's own second factor still applies.
            await session.commit()
            if seeded:
                await enqueue("index_demo_documents", str(account.id))
            resp = RedirectResponse(
                _frontend(
                    "/login",
                    mfa=identity_security.mfa_challenge(account, claims.get("next") or "/app"),
                )
            )
            resp.delete_cookie(STATE_COOKIE, path="/api/integrations/google")
            return resp
        issued = await identity.issue_session(session, account, request)
        await audit.record(
            session,
            action="auth.google_signup" if outcome == "created" else "auth.google_login",
            user_id=account.id,
            request=request,
            meta={
                "linked": outcome in ("linked", "reclaimed"),
                "reclaimed": outcome == "reclaimed",
                "reminders": sync_granted,
            },
        )
        if sync_granted:
            await service.save_connection(
                session, account, tokens, who.email, request, mode=google.mode
            )
        await session.commit()
        if seeded:
            await enqueue("index_demo_documents", str(account.id))
        resp = RedirectResponse(
            _frontend(
                claims.get("next") or "/app",
                google="signed_in",
                reminders="connected" if sync_granted else "later",
            )
        )
        set_auth_cookies(resp, issued.access_token, issued.refresh_token)
        resp.delete_cookie(STATE_COOKIE, path="/api/integrations/google")
        return resp

    # mode == "connect": attach Google to the signed-in account.
    if user is None or claims.get("sub") != str(user.id):
        return fail("error")
    if google.mode != client_for_user(user).mode:  # e.g. a demo account never links real Google
        return fail("error")
    if not sync_granted:
        return fail("scopes")
    await service.save_connection(session, user, tokens, who.email, request, mode=google.mode)
    await session.commit()
    resp = RedirectResponse(_frontend("/app/settings", google="connected") + "#integrations")
    resp.delete_cookie(STATE_COOKIE, path="/api/integrations/google")
    return resp


@router.delete("", status_code=204)
async def disconnect(
    request: Request,
    user: CurrentUser,
    session: DbSession,
    remove_items: bool = Query(False, description="Also delete synced events and tasks"),
):
    await service.disconnect(session, user, remove_items=remove_items, request=request)
    await session.commit()


@router.get("/preview")
async def preview(prescription_id: uuid.UUID, user: CurrentUser, session: DbSession):
    return await service.preview(session, user, prescription_id)


@router.post("/sync")
async def sync(data: SyncIn, request: Request, user: CurrentUser, session: DbSession):
    counts = await service.sync_prescription(
        session,
        user,
        data.prescription_id,
        calendar=data.calendar,
        tasks=data.tasks,
        request=request,
    )
    await session.commit()
    return counts


@router.delete("/sync")
async def unsync(
    prescription_id: uuid.UUID, request: Request, user: CurrentUser, session: DbSession
):
    removed = await service.unsync_prescription(session, user, prescription_id, request)
    await session.commit()
    return {"removed": removed}


@router.post("/pull")
async def pull(user: CurrentUser, session: DbSession):
    updated = await service.pull_task_status(session, user)
    await session.commit()
    return {"updated": updated}
