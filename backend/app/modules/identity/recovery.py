"""Email verification and password reset (ADR-030).

Links carry a random token; only its SHA-256 is stored, it works once, expires, and is pinned to
the address it was sent to. Issuing a new link retires older ones of the same kind. Sending is
the caller's job (routers queue it as a background task after the response, so a reset request
takes the same time whether or not the account exists).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from fastapi import Request
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import utcnow
from app.core.errors import Conflict, Gone
from app.core.security import hash_password, new_opaque_token, sha256_hex
from app.modules.audit import service as audit
from app.modules.identity import security
from app.modules.identity.models import EmailToken, User

VERIFY_HOURS = 48
RESET_MINUTES = 30
_EXPIRED = "This link has expired or was already used. Ask for a new one."


@dataclass(frozen=True)
class Outgoing:
    """An email to send once the transaction has committed."""

    to: str
    name: str
    token: str


async def _issue(session: AsyncSession, user: User, purpose: str, ttl: timedelta) -> str:
    await session.execute(
        update(EmailToken)
        .where(
            EmailToken.user_id == user.id,
            EmailToken.purpose == purpose,
            EmailToken.used_at.is_(None),
        )
        .values(used_at=utcnow())
    )
    raw = new_opaque_token(32)
    session.add(
        EmailToken(
            user_id=user.id,
            purpose=purpose,
            email=user.email,
            token_hash=sha256_hex(raw),
            expires_at=utcnow() + ttl,
        )
    )
    await session.flush()
    return raw


async def _consume(session: AsyncSession, raw: str, purpose: str) -> User:
    row = await session.scalar(
        select(EmailToken).where(
            EmailToken.token_hash == sha256_hex(raw), EmailToken.purpose == purpose
        )
    )
    if row is None or row.used_at is not None or row.expires_at <= utcnow():
        raise Gone(_EXPIRED)
    user = await session.get(User, row.user_id)
    if user is None or user.email.lower() != row.email.lower():
        raise Gone(_EXPIRED)
    row.used_at = utcnow()
    return user


# ---- Verification -------------------------------------------------------------------------------


async def start_verification(session: AsyncSession, user: User) -> Outgoing:
    if user.email_verified:
        raise Conflict("Your email address is already confirmed.")
    token = await _issue(session, user, "verify", timedelta(hours=VERIFY_HOURS))
    return Outgoing(user.email, user.display_name, token)


async def verify_email(session: AsyncSession, raw: str, request: Request) -> User:
    user = await _consume(session, raw, "verify")
    if not user.email_verified:
        user.email_verified_at = utcnow()
        await audit.record(session, action="auth.email_verified", user_id=user.id, request=request)
    return user


# ---- Password reset -----------------------------------------------------------------------------


async def request_reset(session: AsyncSession, email: str, request: Request) -> Outgoing | None:
    """None when there's nothing to send; the caller answers identically either way."""
    user = await session.scalar(select(User).where(User.email == email.strip().lower()))
    if user is None or user.is_demo:
        return None
    token = await _issue(session, user, "reset", timedelta(minutes=RESET_MINUTES))
    await audit.record(
        session, action="auth.password_reset_requested", user_id=user.id, request=request
    )
    return Outgoing(user.email, user.display_name, token)


async def reset_password(
    session: AsyncSession, raw: str, new_password: str, request: Request
) -> User:
    user = await _consume(session, raw, "reset")
    user.password_hash = hash_password(new_password)
    if not user.email_verified:
        user.email_verified_at = utcnow()  # the link proved they read this inbox
    signed_out = await security.revoke_other_sessions(session, user, None)
    await audit.record(
        session,
        action="auth.password_reset",
        user_id=user.id,
        request=request,
        meta={"sessions_signed_out": signed_out},
    )
    return user
