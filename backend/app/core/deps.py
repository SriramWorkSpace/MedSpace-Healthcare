"""Shared FastAPI dependencies."""

from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session, utcnow
from app.core.errors import Unauthorized
from app.core.security import ACCESS_COOKIE, decode_access_claims
from app.modules.identity.models import User


def _extract_token(request: Request) -> str | None:
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        return auth[7:].strip()
    return request.cookies.get(ACCESS_COOKIE)


ACTING_HEADER = "x-acting-for"


async def session_is_live(session: AsyncSession, session_id: uuid.UUID) -> bool:
    """A sign-in is live while its refresh-token family has an unrevoked, unexpired token."""
    from app.modules.identity.models import RefreshToken

    found = await session.scalar(
        select(RefreshToken.id)
        .where(
            RefreshToken.family_id == session_id,
            RefreshToken.revoked_at.is_(None),
            RefreshToken.expires_at > utcnow(),
        )
        .limit(1)
    )
    return found is not None


async def _authenticated(request: Request, session: AsyncSession) -> User | None:
    token = _extract_token(request)
    claims = decode_access_claims(token) if token else None
    if claims is None:
        return None
    user_id, session_id = claims
    if session_id is not None and not await session_is_live(session, session_id):
        return None  # signed out (or signed out elsewhere): the access token dies with it
    return await session.get(User, user_id)


async def get_current_user(request: Request, session: AsyncSession = Depends(get_session)) -> User:
    """The user whose records this request reads or changes.

    Normally the signed-in user. With `X-Acting-For: <owner id>`, a caregiver in the owner's care
    circle acts on the owner's records, limited to the routes their role allows (ADR-026).
    """
    user = await _authenticated(request, session)
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
    return await _authenticated(request, session)


CurrentUser = Annotated[User, Depends(get_current_user)]
OptionalUser = Annotated[User | None, Depends(get_optional_user)]
DbSession = Annotated[AsyncSession, Depends(get_session)]
