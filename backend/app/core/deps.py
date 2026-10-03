"""Shared FastAPI dependencies."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from app.core.errors import Unauthorized
from app.core.security import ACCESS_COOKIE, decode_access_token
from app.modules.identity.models import User


def _extract_token(request: Request) -> str | None:
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        return auth[7:].strip()
    return request.cookies.get(ACCESS_COOKIE)


ACTING_HEADER = "x-acting-for"


async def get_current_user(request: Request, session: AsyncSession = Depends(get_session)) -> User:
    """The user whose records this request reads or changes.

    Normally the signed-in user. With `X-Acting-For: <owner id>`, a caregiver in the owner's care
    circle acts on the owner's records, limited to the routes their role allows (ADR-026).
    """
    token = _extract_token(request)
    user_id = decode_access_token(token) if token else None
    if user_id is None:
        raise Unauthorized()
    user = await session.get(User, user_id)
    if user is None:
        raise Unauthorized()
    owner_ref = request.headers.get(ACTING_HEADER)
    if owner_ref:
        from app.modules.circle import service as circle

        return await circle.resolve_acting(session, request, user, owner_ref)
    return user


async def get_optional_user(
    request: Request, session: AsyncSession = Depends(get_session)
) -> User | None:
    token = _extract_token(request)
    user_id = decode_access_token(token) if token else None
    return await session.get(User, user_id) if user_id else None


CurrentUser = Annotated[User, Depends(get_current_user)]
OptionalUser = Annotated[User | None, Depends(get_optional_user)]
DbSession = Annotated[AsyncSession, Depends(get_session)]
