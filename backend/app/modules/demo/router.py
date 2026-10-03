from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Response, status

from app.core.config import get_settings
from app.core.deps import DbSession
from app.core.errors import NotFound
from app.core.ratelimit import rate_limit
from app.modules.audit import service as audit
from app.modules.demo import service
from app.modules.identity import service as identity
from app.modules.identity.cookies import set_auth_cookies
from app.modules.identity.router import SessionOut
from app.modules.identity.schemas import UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/demo",
    response_model=SessionOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit("auth:demo", 5, 60, by="ip"))],
)
async def demo_login(request: Request, response: Response, session: DbSession):
    if not get_settings().demo_enabled:
        raise NotFound("The demo is switched off on this server.")
    user = await service.create_demo_account(session)
    issued = await identity.issue_session(session, user, request)
    await audit.record(session, action="auth.demo_login", user_id=user.id, request=request)
    await session.commit()
    csrf = set_auth_cookies(response, issued.access_token, issued.refresh_token)
    return SessionOut(user=UserOut.model_validate(user), csrf_token=csrf)
