"""Identity: accounts, credentials and refresh-token rotation."""

from __future__ import annotations

import uuid
from datetime import timedelta

from fastapi import Request
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import utcnow, uuid7
from app.core.errors import Conflict, Unauthorized
from app.core.ratelimit import client_ip
from app.core.security import (
    create_access_token,
    hash_password,
    needs_rehash,
    new_opaque_token,
    sha256_hex,
    verify_password,
)
from app.modules.audit import service as audit
from app.modules.identity.models import RefreshToken, User
from app.modules.identity.schemas import ProfileUpdate, SignupIn

# Verifying against a real hash when the user is unknown keeps login timing uniform.
_DUMMY_HASH = hash_password("timing-equalizer-not-a-real-password")


class IssuedSession:
    def __init__(self, user: User, access_token: str, refresh_token: str) -> None:
        self.user = user
        self.access_token = access_token
        self.refresh_token = refresh_token


async def get_user(session: AsyncSession, user_id: uuid.UUID) -> User | None:
    return await session.get(User, user_id)


async def create_user(
    session: AsyncSession,
    data: SignupIn,
    *,
    is_demo: bool = False,
) -> User:
    exists = await session.scalar(select(User.id).where(User.email == data.email))
    if exists:
        raise Conflict("An account with this email already exists.")
    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        display_name=data.display_name,
        timezone=data.timezone,
        is_demo=is_demo,
    )
    session.add(user)
    await session.flush()
    return user


async def authenticate(session: AsyncSession, email: str, password: str) -> User:
    user = await session.scalar(select(User).where(User.email == email.lower()))
    if user is None:
        verify_password(_DUMMY_HASH, password)
        raise Unauthorized("That email and password combination doesn't match our records.")
    if user.password_hash is None:
        # Google-only account: keep the response identical to a wrong password.
        verify_password(_DUMMY_HASH, password)
        raise Unauthorized("That email and password combination doesn't match our records.")
    if not verify_password(user.password_hash, password):
        raise Unauthorized("That email and password combination doesn't match our records.")
    if needs_rehash(user.password_hash):
        user.password_hash = hash_password(password)
    return user


async def login_with_google(
    session: AsyncSession,
    *,
    sub: str,
    email: str,
    email_verified: bool,
    name: str | None,
    is_demo: bool = False,
) -> tuple[User, str]:
    """Find or create the account for a Google identity.

    Returns (user, outcome) where outcome is "signed_in", "linked" or "created".
    An existing password account is linked only when Google has verified the email address;
    otherwise the email stays with its current owner (prevents account takeover).
    """
    user = await session.scalar(select(User).where(User.google_sub == sub))
    if user:
        return user, "signed_in"

    email = email.lower()
    existing = await session.scalar(select(User).where(User.email == email))
    if existing:
        if not email_verified or existing.google_sub is not None:
            raise Conflict("An account with this email already exists. Sign in with your password.")
        existing.google_sub = sub
        await session.flush()
        return existing, "linked"

    user = User(
        email=email,
        password_hash=None,
        google_sub=sub,
        display_name=(name or email.split("@")[0]).strip()[:80] or "MedSpace user",
        is_demo=is_demo,
    )
    session.add(user)
    await session.flush()
    return user, "created"


async def issue_session(
    session: AsyncSession,
    user: User,
    request: Request | None,
    *,
    family_id: uuid.UUID | None = None,
) -> IssuedSession:
    settings = get_settings()
    raw = new_opaque_token()
    family = family_id or uuid7()
    session.add(
        RefreshToken(
            user_id=user.id,
            family_id=family,
            token_hash=sha256_hex(raw),
            expires_at=utcnow() + timedelta(days=settings.refresh_token_ttl_days),
            ip=client_ip(request) if request else None,
            user_agent=(request.headers.get("user-agent") or "")[:256] if request else None,
        )
    )
    user.last_login_at = utcnow()
    await session.flush()
    return IssuedSession(user, create_access_token(user.id, family), raw)


async def rotate_refresh_token(
    session: AsyncSession, raw_token: str | None, request: Request
) -> IssuedSession:
    """Exchange a refresh token for a new pair. Presenting a used token revokes its family."""
    if not raw_token:
        raise Unauthorized("Session expired. Please sign in again.")
    token = await session.scalar(
        select(RefreshToken).where(RefreshToken.token_hash == sha256_hex(raw_token))
    )
    if token is None:
        raise Unauthorized("Session expired. Please sign in again.")

    now = utcnow()
    if token.revoked_at is not None:
        await session.execute(
            update(RefreshToken)
            .where(RefreshToken.family_id == token.family_id, RefreshToken.revoked_at.is_(None))
            .values(revoked_at=now)
        )
        await audit.record(
            session,
            action="auth.refresh_reuse_detected",
            user_id=token.user_id,
            request=request,
            actor="system",
            meta={"family_id": str(token.family_id)},
        )
        await session.commit()
        raise Unauthorized("Session expired. Please sign in again.")

    if token.expires_at <= now:
        raise Unauthorized("Session expired. Please sign in again.")

    user = await session.get(User, token.user_id)
    if user is None:
        raise Unauthorized("Session expired. Please sign in again.")

    issued = await issue_session(session, user, request, family_id=token.family_id)
    new_token = await session.scalar(
        select(RefreshToken).where(RefreshToken.token_hash == sha256_hex(issued.refresh_token))
    )
    token.revoked_at = now
    token.replaced_by = new_token.id if new_token else None
    return issued


async def revoke_refresh_token(session: AsyncSession, raw_token: str | None) -> None:
    if not raw_token:
        return
    token = await session.scalar(
        select(RefreshToken).where(RefreshToken.token_hash == sha256_hex(raw_token))
    )
    if token is not None:
        await session.execute(
            update(RefreshToken)
            .where(RefreshToken.family_id == token.family_id, RefreshToken.revoked_at.is_(None))
            .values(revoked_at=utcnow())
        )


async def update_profile(session: AsyncSession, user: User, data: ProfileUpdate) -> User:
    if data.display_name is not None:
        user.display_name = data.display_name.strip()
    if data.timezone is not None:
        user.timezone = data.timezone
    if data.dose_times is not None:
        user.dose_times = {**user.dose_times, **data.dose_times}
    await session.flush()
    return user


async def delete_user(session: AsyncSession, user: User) -> None:
    await session.delete(user)
