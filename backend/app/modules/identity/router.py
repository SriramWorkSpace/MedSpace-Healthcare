from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response, status
from pydantic import BaseModel

from app.core.deps import CurrentUser, DbSession
from app.core.ratelimit import rate_limit
from app.core.security import ACCESS_COOKIE, REFRESH_COOKIE, decode_access_token
from app.modules.audit import service as audit
from app.modules.identity import service
from app.modules.identity.cookies import clear_auth_cookies, set_auth_cookies
from app.modules.identity.schemas import LoginIn, ProfileUpdate, SignupIn, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])
profile_router = APIRouter(prefix="/me", tags=["profile"])


class SessionOut(BaseModel):
    user: UserOut
    csrf_token: str


@router.post(
    "/signup",
    response_model=SessionOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit("auth:signup", 5, 60))],
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
    response_model=SessionOut,
    dependencies=[Depends(rate_limit("auth:login", 10, 60))],
)
async def login(data: LoginIn, request: Request, response: Response, session: DbSession):
    user = await service.authenticate(session, data.email, data.password)
    issued = await service.issue_session(session, user, request)
    await audit.record(session, action="auth.login", user_id=user.id, request=request)
    await session.commit()
    csrf = set_auth_cookies(response, issued.access_token, issued.refresh_token)
    return SessionOut(user=UserOut.model_validate(user), csrf_token=csrf)


@router.post(
    "/refresh",
    response_model=SessionOut,
    dependencies=[Depends(rate_limit("auth:refresh", 30, 60))],
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
async def session_state(request: Request, session: DbSession):
    """Who am I, without a 401 for anonymous visitors (the SPA calls this on boot)."""
    token = request.cookies.get(ACCESS_COOKIE)
    user_id = decode_access_token(token) if token else None
    user = await service.get_user(session, user_id) if user_id else None
    return SessionState(user=UserOut.model_validate(user) if user else None)


@router.get("/me", response_model=UserOut)
async def me(user: CurrentUser):
    return user


@profile_router.patch("", response_model=UserOut)
async def update_profile(data: ProfileUpdate, user: CurrentUser, session: DbSession):
    await service.update_profile(session, user, data)
    await session.commit()
    return user


@profile_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(user: CurrentUser, response: Response, session: DbSession):
    await service.delete_user(session, user)
    await session.commit()
    clear_auth_cookies(response)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response
