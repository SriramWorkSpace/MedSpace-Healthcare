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
from app.core.errors import Conflict, Forbidden, Gone, Unprocessable
from app.core.security import hash_password, new_opaque_token, sha256_hex, verify_password
from app.modules.audit import service as audit
from app.modules.identity import security
from app.modules.identity.models import EmailToken, User

VERIFY_HOURS = 48
RESET_MINUTES = 30
CHANGE_HOURS = 24
_EXPIRED = "This link has expired or was already used. Ask for a new one."


@dataclass(frozen=True)
class Outgoing:
    """An email to send once the transaction has committed."""

    to: str
    name: str
    token: str


async def _issue(
    session: AsyncSession, user: User, purpose: str, ttl: timedelta, email: str | None = None
) -> str:
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
            email=email or user.email,
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


async def reset_link_is_valid(session: AsyncSession, raw: str) -> bool:
    """Whether a reset link still works, without using it (so the page can say so up front)."""
    row = await session.scalar(
        select(EmailToken).where(
            EmailToken.token_hash == sha256_hex(raw), EmailToken.purpose == "reset"
        )
    )
    return row is not None and row.used_at is None and row.expires_at > utcnow()


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


# ---- Changing the account email -----------------------------------------------------------------


@dataclass(frozen=True)
class EmailChange:
    """What to send once committed: a link to the new address, a heads-up to the old one."""

    old_email: str
    new_email: str
    name: str
    token: str


async def start_email_change(
    session: AsyncSession,
    user: User,
    new_email: str,
    password: str | None,
    code: str | None,
    request: Request,
) -> EmailChange:
    """Needs fresh proof (password, plus a code with two-step on) and a link to the new address.

    Nothing changes until that link is opened, and the current address hears about it first.
    """
    new_email = new_email.strip().lower()
    if user.is_demo:
        raise Forbidden("Demo accounts can't change their email address.")
    if not user.has_password:
        raise Unprocessable("Add a password in Security first, then change your email.")
    if not (password and verify_password(user.password_hash, password)):
        raise Forbidden("That password isn't right.")
    if user.mfa_enabled:
        await security.check_second_factor(session, user, code, None, Forbidden)
    if new_email == user.email:
        raise Unprocessable("That's already your email address.")
    taken = await session.scalar(select(User.id).where(User.email == new_email))
    if taken:
        raise Conflict("Another account already uses that address.")
    token = await _issue(session, user, "change", timedelta(hours=CHANGE_HOURS), email=new_email)
    await audit.record(
        session,
        action="auth.email_change_requested",
        user_id=user.id,
        request=request,
        meta={"new_email": new_email},
    )
    return EmailChange(user.email, new_email, user.display_name, token)


async def pending_email_change(session: AsyncSession, user: User) -> str | None:
    row = await session.scalar(
        select(EmailToken)
        .where(
            EmailToken.user_id == user.id,
            EmailToken.purpose == "change",
            EmailToken.used_at.is_(None),
            EmailToken.expires_at > utcnow(),
        )
        .order_by(EmailToken.created_at.desc())
        .limit(1)
    )
    return row.email if row else None


async def cancel_email_change(session: AsyncSession, user: User, request: Request) -> None:
    result = await session.execute(
        update(EmailToken)
        .where(
            EmailToken.user_id == user.id,
            EmailToken.purpose == "change",
            EmailToken.used_at.is_(None),
        )
        .values(used_at=utcnow())
    )
    if result.rowcount:
        await audit.record(
            session, action="auth.email_change_cancelled", user_id=user.id, request=request
        )


async def confirm_email_change(
    session: AsyncSession, raw: str, request: Request
) -> tuple[User, str]:
    """Open the link sent to the new address: the account moves to it. Returns (user, old)."""
    row = await session.scalar(
        select(EmailToken).where(
            EmailToken.token_hash == sha256_hex(raw), EmailToken.purpose == "change"
        )
    )
    if row is None or row.used_at is not None or row.expires_at <= utcnow():
        raise Gone(_EXPIRED)
    user = await session.get(User, row.user_id)
    if user is None:
        raise Gone(_EXPIRED)
    taken = await session.scalar(select(User.id).where(User.email == row.email, User.id != user.id))
    if taken:  # someone registered it while the link was waiting
        raise Conflict("Another account now uses that address. Try a different one.")
    old = user.email
    row.used_at = utcnow()
    user.email = row.email
    user.email_verified_at = utcnow()  # opening the link proved this inbox
    # Links sent to the old address (confirm, reset) no longer match the account: they're void.
    await session.execute(
        update(EmailToken)
        .where(EmailToken.user_id == user.id, EmailToken.used_at.is_(None))
        .values(used_at=utcnow())
    )
    await audit.record(
        session,
        action="auth.email_changed",
        user_id=user.id,
        request=request,
        meta={"old_email": old, "new_email": user.email},
    )
    return user, old
