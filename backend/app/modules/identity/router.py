from __future__ import annotations

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.deps import CurrentUser, DbSession, OptionalUser
from app.core.errors import RateLimited
from app.core.ratelimit import check, rate_limit
from app.core.security import (
    ACCESS_COOKIE,
    REFRESH_COOKIE,
    decode_access_claims,
    decode_purpose_token,
)
from app.modules.audit import service as audit
from app.modules.documents import service as documents
from app.modules.identity import security, service
from app.modules.identity.cookies import clear_auth_cookies, set_auth_cookies
from app.modules.identity.schemas import (
    CodeIn,
    DeviceSessionOut,
    LoginIn,
    LoginResult,
    MfaDisableIn,
    MfaLoginIn,
    MfaSetupOut,
    PasswordChangeIn,
    ProfileUpdate,
    RecoveryCodesOut,
    SecurityOut,
    SignedOut,
    SignupIn,
    UserOut,
)

router = APIRouter(prefix="/auth", tags=["auth"])
profile_router = APIRouter(prefix="/me", tags=["profile"])


class SessionOut(BaseModel):
    user: UserOut
    csrf_token: str


@router.post(
    "/signup",
    response_model=SessionOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(rate_limit("auth:signup", 5, 60, by="ip")),
        Depends(rate_limit("auth:signup-hour", 20, 3600, by="ip")),
    ],
)
async def signup(data: SignupIn, request: Request, response: Response, session: DbSession):
    user = await service.create_user(session, data)
    issued = await service.issue_session(session, user, request)
    await audit.record(session, action="auth.signup", user_id=user.id, request=request)
    await session.commit()
    csrf = set_auth_cookies(response, issued.access_token, issued.refresh_token)
    return SessionOut(user=UserOut.model_validate(user), csrf_token=csrf)


@router.post(
    "/login",
    response_model=LoginResult,
    dependencies=[Depends(rate_limit("auth:login", 10, 60, by="ip"))],
)
async def login(data: LoginIn, request: Request, response: Response, session: DbSession):
    # Per account as well as per IP: guessing one password from many addresses still slows down.
    attempt = await check("auth:login-account", data.email.strip().lower(), 10, 900)
    if not attempt.allowed:
        raise RateLimited(
            "Too many sign-in attempts for this account. Try again in a few minutes.",
            extra={"retry_after": attempt.reset},
        )
    user = await service.authenticate(session, data.email, data.password)
    if user.mfa_enabled:
        # Password was right; the session waits for the second factor (ADR-029).
        await audit.record(
            session, action="auth.login_mfa_pending", user_id=user.id, request=request
        )
        await session.commit()
        return LoginResult(mfa_required=True, mfa_token=security.mfa_challenge(user))
    issued = await service.issue_session(session, user, request)
    await audit.record(session, action="auth.login", user_id=user.id, request=request)
    await session.commit()
    csrf = set_auth_cookies(response, issued.access_token, issued.refresh_token)
    return LoginResult(user=UserOut.model_validate(user), csrf_token=csrf)


@router.post(
    "/login/mfa",
    response_model=LoginResult,
    dependencies=[Depends(rate_limit("auth:mfa", 10, 60, by="ip"))],
)
async def login_mfa(data: MfaLoginIn, request: Request, response: Response, session: DbSession):
    claims = decode_purpose_token(data.mfa_token, security.MFA_PURPOSE)
    if claims:  # five tries per account per five minutes, wherever they come from
        attempt = await check("auth:mfa-user", claims["sub"], 5, 300)
        if not attempt.allowed:
            raise RateLimited(
                "Too many codes tried. Wait a few minutes, then sign in again.",
                extra={"retry_after": attempt.reset},
            )
    user, next_path = await security.finish_mfa(
        session, data.mfa_token, data.code, data.recovery_code, request
    )
    issued = await service.issue_session(session, user, request)
    await session.commit()
    csrf = set_auth_cookies(response, issued.access_token, issued.refresh_token)
    return LoginResult(user=UserOut.model_validate(user), csrf_token=csrf, next=next_path)


@router.post(
    "/refresh",
    response_model=SessionOut,
    dependencies=[Depends(rate_limit("auth:refresh", 30, 60, by="ip"))],
)
async def refresh(request: Request, response: Response, session: DbSession):
    try:
        issued = await service.rotate_refresh_token(
            session, request.cookies.get(REFRESH_COOKIE), request
        )
    except Exception:
        clear_auth_cookies(response)
        raise
    await session.commit()
    csrf = set_auth_cookies(response, issued.access_token, issued.refresh_token)
    return SessionOut(user=UserOut.model_validate(issued.user), csrf_token=csrf)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request, response: Response, session: DbSession):
    await service.revoke_refresh_token(session, request.cookies.get(REFRESH_COOKIE))
    await session.commit()
    clear_auth_cookies(response)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


class SessionState(BaseModel):
    user: UserOut | None


@router.get("/session", response_model=SessionState)
async def session_state(user: OptionalUser):
    """Who am I, without a 401 for anonymous visitors (the SPA calls this on boot).
    A signed-out device's still-unexpired access token counts as anonymous."""
    return SessionState(user=UserOut.model_validate(user) if user else None)


@router.get("/me", response_model=UserOut)
async def me(user: CurrentUser):
    return user


@profile_router.patch("", response_model=UserOut)
async def update_profile(data: ProfileUpdate, user: CurrentUser, session: DbSession):
    await service.update_profile(session, user, data)
    await session.commit()
    return user


@profile_router.get("/export", dependencies=[Depends(rate_limit("me:export", 5, 600))])
async def export_data(user: CurrentUser, session: DbSession):
    """Everything this account holds, as one JSON file (tokens and secrets excluded)."""
    from app.modules.identity.export import build_export

    payload = await build_export(session, user)
    filename = f"medspace-export-{datetime.now(UTC):%Y%m%d}.json"
    return JSONResponse(
        payload,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-store",
        },
    )


@profile_router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limit("me:delete", 3, 3600))],
)
async def delete_account(user: CurrentUser, response: Response, session: DbSession):
    user_id = user.id
    await service.delete_user(session, user)
    await session.commit()
    await documents.purge_user_files(user_id)
    clear_auth_cookies(response)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


# ---- Account security (ADR-029) ----------------------------------------------------------------


def _current_session(request: Request) -> uuid.UUID | None:
    token = request.cookies.get(ACCESS_COOKIE)
    claims = decode_access_claims(token) if token else None
    return claims[1] if claims else None


async def _security_out(session, user, request: Request) -> SecurityOut:
    sessions = await security.list_sessions(session, user, _current_session(request))
    return SecurityOut(
        mfa_enabled=user.mfa_enabled,
        recovery_codes_left=await security.recovery_codes_left(session, user),
        has_password=user.has_password,
        sessions=[DeviceSessionOut(**vars(s)) for s in sessions],
    )


@profile_router.get("/security", response_model=SecurityOut)
async def get_security(request: Request, user: CurrentUser, session: DbSession):
    return await _security_out(session, user, request)


@profile_router.post("/mfa/setup", response_model=MfaSetupOut)
async def mfa_setup(user: CurrentUser, session: DbSession):
    setup = await security.begin_setup(session, user)
    await session.commit()
    return MfaSetupOut(secret=setup.secret, otpauth_uri=setup.otpauth_uri, qr_svg=setup.qr_svg)


@profile_router.post(
    "/mfa/enable",
    response_model=RecoveryCodesOut,
    dependencies=[Depends(rate_limit("me:mfa", 10, 300))],
)
async def mfa_enable(data: CodeIn, request: Request, user: CurrentUser, session: DbSession):
    codes = await security.enable(session, user, data.code, _current_session(request), request)
    await session.commit()
    return RecoveryCodesOut(codes=codes)


@profile_router.post(
    "/mfa/disable", status_code=204, dependencies=[Depends(rate_limit("me:mfa", 10, 300))]
)
async def mfa_disable(data: MfaDisableIn, request: Request, user: CurrentUser, session: DbSession):
    await security.disable(session, user, data.password, data.code, data.recovery_code, request)
    await session.commit()


@profile_router.post(
    "/mfa/recovery-codes",
    response_model=RecoveryCodesOut,
    dependencies=[Depends(rate_limit("me:mfa", 10, 300))],
)
async def mfa_new_codes(data: CodeIn, request: Request, user: CurrentUser, session: DbSession):
    codes = await security.regenerate_codes(session, user, data.code, request)
    await session.commit()
    return RecoveryCodesOut(codes=codes)


@profile_router.delete("/sessions/{session_id}", status_code=204)
async def end_session(
    session_id: uuid.UUID, request: Request, user: CurrentUser, session: DbSession
):
    await security.revoke_session(session, user, session_id, request)
    await session.commit()


@profile_router.post("/sessions/sign-out-others", response_model=SignedOut)
async def end_other_sessions(request: Request, user: CurrentUser, session: DbSession):
    count = await security.revoke_other_sessions(session, user, _current_session(request))
    await audit.record(
        session,
        action="auth.other_sessions_revoked",
        user_id=user.id,
        request=request,
        meta={"count": count},
    )
    await session.commit()
    return SignedOut(signed_out=count)


@profile_router.post(
    "/password",
    response_model=SignedOut,
    dependencies=[Depends(rate_limit("me:password", 5, 600))],
)
async def change_password(
    data: PasswordChangeIn, request: Request, user: CurrentUser, session: DbSession
):
    count = await security.change_password(
        session, user, data.current_password, data.new_password, _current_session(request), request
    )
    await session.commit()
    return SignedOut(signed_out=count)
