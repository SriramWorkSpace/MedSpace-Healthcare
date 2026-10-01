from __future__ import annotations

import logging
import secrets
import uuid
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import APIRouter, Query, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.deps import CurrentUser, DbSession
from app.core.security import JWT_ALG, constant_time_equals
from app.modules.integrations import service
from app.modules.integrations.google import GoogleAPIError, GoogleAuthError, get_google, pkce_pair

logger = logging.getLogger("medspace.integrations")
router = APIRouter(prefix="/integrations/google", tags=["integrations"])

STATE_COOKIE = "ms_oauth"


class StatusOut(BaseModel):
    connected: bool
    status: str | None = None
    mode: str
    email: str | None = None
    connected_at: datetime | None = None


class SyncIn(BaseModel):
    prescription_id: uuid.UUID
    calendar: bool = True
    tasks: bool = True


def _settings_url(result: str) -> str:
    return f"{get_settings().frontend_url}/app/settings?google={result}#integrations"


@router.get("/status", response_model=StatusOut)
async def status(user: CurrentUser, session: DbSession):
    conn = await service.get_connection(session, user.id)
    mode = get_google().mode
    if conn is None:
        return StatusOut(connected=False, mode=mode)
    return StatusOut(
        connected=conn.status == "active",
        status=conn.status,
        mode=conn.mode,
        email=conn.account_email,
        connected_at=conn.created_at,
    )


@router.get("/connect")
async def connect(user: CurrentUser):
    """Start OAuth (PKCE). State + verifier ride in a short-lived signed, httpOnly cookie."""
    verifier, challenge = pkce_pair()
    state = secrets.token_urlsafe(24)
    s = get_settings()
    signed = jwt.encode(
        {
            "sub": str(user.id),
            "state": state,
            "verifier": verifier,
            "exp": datetime.now(UTC) + timedelta(minutes=10),
        },
        s.jwt_secret.get_secret_value(),
        algorithm=JWT_ALG,
    )
    resp = RedirectResponse(get_google().auth_url(state, challenge), status_code=302)
    resp.set_cookie(
        STATE_COOKIE,
        signed,
        max_age=600,
        httponly=True,
        secure=s.cookie_secure,
        samesite="lax",
        path="/api/integrations/google",
    )
    return resp


@router.get("/callback")
async def callback(
    request: Request,
    user: CurrentUser,
    session: DbSession,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
):
    s = get_settings()
    if error or not code:
        return RedirectResponse(_settings_url("denied" if error else "error"))
    try:
        claims = jwt.decode(
            request.cookies.get(STATE_COOKIE, ""),
            s.jwt_secret.get_secret_value(),
            algorithms=[JWT_ALG],
        )
    except jwt.PyJWTError:
        return RedirectResponse(_settings_url("expired"))
    if claims.get("sub") != str(user.id) or not constant_time_equals(claims.get("state"), state):
        return RedirectResponse(_settings_url("error"))

    google = get_google()
    try:
        tokens = await google.exchange_code(code, claims["verifier"])
        email = await google.user_email(tokens.access_token)
    except (GoogleAPIError, GoogleAuthError):
        logger.exception("google token exchange failed")
        return RedirectResponse(_settings_url("error"))
    await service.save_connection(session, user, tokens, email, request)
    await session.commit()
    resp = RedirectResponse(_settings_url("connected"))
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
