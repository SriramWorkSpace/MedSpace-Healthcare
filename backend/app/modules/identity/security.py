"""Account security (ADR-029): two-step verification, active sessions, password changes.

Sessions are refresh-token families (one per sign-in on a device). Access tokens carry their
family id, so revoking a family signs that device out on its next request rather than when its
access token expires.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from datetime import datetime

import segno
from fastapi import Request
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import totp
from app.core.db import utcnow
from app.core.errors import AppError, Conflict, Forbidden, NotFound, Unauthorized, Unprocessable
from app.core.security import (
    create_purpose_token,
    decode_purpose_token,
    decrypt,
    encrypt,
    hash_password,
    sha256_hex,
    verify_password,
)
from app.modules.audit import service as audit
from app.modules.identity.models import RecoveryCode, RefreshToken, User

MFA_TOKEN_MINUTES = 5
MFA_PURPOSE = "mfa"


# ---- Two-step verification ----------------------------------------------------------------------


@dataclass
class Setup:
    secret: str
    otpauth_uri: str
    qr_svg: str  # data: URI


async def begin_setup(session: AsyncSession, user: User) -> Setup:
    if user.mfa_enabled:
        raise Conflict("Two-step verification is already on.")
    secret = totp.new_secret()
    user.totp_pending_enc = encrypt(secret)
    await session.flush()
    uri = totp.provisioning_uri(secret, user.email)
    return Setup(secret, uri, segno.make(uri, error="m").svg_data_uri(scale=5, border=2))


async def _new_recovery_codes(session: AsyncSession, user: User) -> list[str]:
    await session.execute(
        update(RecoveryCode)
        .where(RecoveryCode.user_id == user.id, RecoveryCode.used_at.is_(None))
        .values(used_at=utcnow())
    )
    codes = totp.new_recovery_codes()
    for code in codes:
        session.add(RecoveryCode(user_id=user.id, code_hash=sha256_hex(code)))
    await session.flush()
    return codes


async def enable(
    session: AsyncSession, user: User, code: str, keep_session: uuid.UUID | None, request: Request
) -> list[str]:
    if user.mfa_enabled:
        raise Conflict("Two-step verification is already on.")
    secret = decrypt(user.totp_pending_enc) if user.totp_pending_enc else None
    if not secret:
        raise Unprocessable("Start the setup again: scan the QR code, then enter a code.")
    step = totp.verify(secret, code)
    if step is None:
        raise Unprocessable("That code didn't match. Check the time on your phone and try again.")
    user.totp_secret_enc = encrypt(secret)
    user.totp_pending_enc = None
    user.totp_enabled_at = utcnow()
    user.totp_last_step = step
    codes = await _new_recovery_codes(session, user)
    revoked = await revoke_other_sessions(session, user, keep_session)
    await audit.record(
        session,
        action="mfa.enabled",
        user_id=user.id,
        request=request,
        meta={"other_sessions_signed_out": revoked},
    )
    return codes


async def check_second_factor(
    session: AsyncSession,
    user: User,
    code: str | None,
    recovery_code: str | None,
    error: type[AppError] = Unauthorized,
) -> str:
    """Verify a TOTP code or an unused recovery code. Returns which one was used.

    Signed-in re-checks raise 403 rather than 401, so the client doesn't treat a mistyped code
    as an expired session."""
    if code:
        secret = decrypt(user.totp_secret_enc) if user.totp_secret_enc else None
        step = totp.verify(secret, code, last_step=user.totp_last_step) if secret else None
        if step is not None:
            user.totp_last_step = step
            return "totp"
    if recovery_code:
        row = await session.scalar(
            select(RecoveryCode).where(
                RecoveryCode.user_id == user.id,
                RecoveryCode.code_hash == sha256_hex(totp.normalize_recovery_code(recovery_code)),
                RecoveryCode.used_at.is_(None),
            )
        )
        if row is not None:
            row.used_at = utcnow()
            return "recovery"
    raise error("That code didn't work. Codes change every 30 seconds.")


async def disable(
    session: AsyncSession,
    user: User,
    password: str | None,
    code: str | None,
    recovery_code: str | None,
    request: Request,
) -> None:
    if not user.mfa_enabled:
        raise Conflict("Two-step verification is already off.")
    if user.has_password and not (password and verify_password(user.password_hash, password)):
        raise Forbidden("That password isn't right.")
    await check_second_factor(session, user, code, recovery_code, Forbidden)
    await clear_second_factor(session, user)
    await audit.record(session, action="mfa.disabled", user_id=user.id, request=request)


async def clear_second_factor(session: AsyncSession, user: User) -> None:
    user.totp_secret_enc = None
    user.totp_pending_enc = None
    user.totp_enabled_at = None
    user.totp_last_step = None
    await session.execute(
        update(RecoveryCode)
        .where(RecoveryCode.user_id == user.id, RecoveryCode.used_at.is_(None))
        .values(used_at=utcnow())
    )


async def regenerate_codes(
    session: AsyncSession, user: User, code: str, request: Request
) -> list[str]:
    if not user.mfa_enabled:
        raise Conflict("Turn on two-step verification first.")
    await check_second_factor(session, user, code, None, Forbidden)
    codes = await _new_recovery_codes(session, user)
    await audit.record(
        session, action="mfa.recovery_codes_regenerated", user_id=user.id, request=request
    )
    return codes


async def recovery_codes_left(session: AsyncSession, user: User) -> int:
    return (
        await session.scalar(
            select(func.count())
            .select_from(RecoveryCode)
            .where(RecoveryCode.user_id == user.id, RecoveryCode.used_at.is_(None))
        )
        or 0
    )


def mfa_challenge(user: User, next_path: str | None = None) -> str:
    """The token a first-factor success hands back instead of a session."""
    extra = {"next": next_path} if next_path else {}
    return create_purpose_token(user.id, MFA_PURPOSE, MFA_TOKEN_MINUTES, **extra)


async def finish_mfa(
    session: AsyncSession, token: str, code: str | None, recovery_code: str | None, request: Request
) -> tuple[User, str | None]:
    claims = decode_purpose_token(token, MFA_PURPOSE)
    if claims is None:
        raise Unauthorized("That sign-in took too long. Please start again.")
    user = await session.get(User, uuid.UUID(claims["sub"]))
    if user is None or not user.mfa_enabled:
        raise Unauthorized("That sign-in took too long. Please start again.")
    used = await check_second_factor(session, user, code, recovery_code)
    await audit.record(
        session, action="auth.login_mfa", user_id=user.id, request=request, meta={"factor": used}
    )
    return user, claims.get("next")


# ---- Sessions -----------------------------------------------------------------------------------


@dataclass
class DeviceSession:
    id: uuid.UUID
    device: str
    ip: str | None
    signed_in_at: datetime
    last_active_at: datetime
    current: bool


_BROWSERS = (
    ("Edg/", "Edge"),
    ("OPR/", "Opera"),
    ("Firefox/", "Firefox"),
    ("Chrome/", "Chrome"),
    ("Safari/", "Safari"),
)
_SYSTEMS = (
    ("iPhone", "iPhone"),
    ("iPad", "iPad"),
    ("Android", "Android"),
    ("Windows", "Windows"),
    ("Mac OS X", "macOS"),
    ("Linux", "Linux"),
)


def describe_device(user_agent: str | None) -> str:
    """'Chrome on Windows' from a user-agent string (good enough to recognise your devices)."""
    ua = user_agent or ""
    browser = next((name for key, name in _BROWSERS if key in ua), None)
    system = next((name for key, name in _SYSTEMS if key in ua), None)
    if re.search(r"python-httpx|curl|python-requests", ua):
        return "API client"
    if browser and system:
        return f"{browser} on {system}"
    return browser or system or "Unknown device"


async def list_sessions(
    session: AsyncSession, user: User, current: uuid.UUID | None
) -> list[DeviceSession]:
    rows = (
        await session.execute(
            select(
                RefreshToken.family_id,
                func.min(RefreshToken.created_at),
                func.max(RefreshToken.created_at),
            )
            .where(RefreshToken.user_id == user.id)
            .group_by(RefreshToken.family_id)
            .having(
                func.count().filter(
                    (RefreshToken.revoked_at.is_(None)) & (RefreshToken.expires_at > utcnow())
                )
                > 0
            )
        )
    ).all()
    out = []
    for family, first, last in rows:
        latest = await session.scalar(
            select(RefreshToken)
            .where(RefreshToken.family_id == family)
            .order_by(RefreshToken.created_at.desc())
            .limit(1)
        )
        out.append(
            DeviceSession(
                id=family,
                device=describe_device(latest.user_agent),
                ip=latest.ip,
                signed_in_at=first,
                last_active_at=last,
                current=family == current,
            )
        )
    return sorted(out, key=lambda s: (not s.current, -s.last_active_at.timestamp()))


async def revoke_session(
    session: AsyncSession, user: User, family_id: uuid.UUID, request: Request | None = None
) -> None:
    result = await session.execute(
        update(RefreshToken)
        .where(
            RefreshToken.user_id == user.id,
            RefreshToken.family_id == family_id,
            RefreshToken.revoked_at.is_(None),
        )
        .values(revoked_at=utcnow())
    )
    if result.rowcount == 0:
        raise NotFound("That session has already ended.")
    await audit.record(
        session,
        action="auth.session_revoked",
        user_id=user.id,
        request=request,
        meta={"session": str(family_id)},
    )


async def revoke_other_sessions(session: AsyncSession, user: User, keep: uuid.UUID | None) -> int:
    stmt = (
        update(RefreshToken)
        .where(RefreshToken.user_id == user.id, RefreshToken.revoked_at.is_(None))
        .values(revoked_at=utcnow())
    )
    if keep is not None:
        stmt = stmt.where(RefreshToken.family_id != keep)
    result = await session.execute(stmt)
    families = result.rowcount or 0
    return families


async def change_password(
    session: AsyncSession,
    user: User,
    current: str | None,
    new: str,
    keep_session: uuid.UUID | None,
    request: Request,
) -> int:
    if user.has_password and not (current and verify_password(user.password_hash, current)):
        raise Forbidden("Your current password isn't right.")
    if user.has_password and verify_password(user.password_hash, new):
        raise Unprocessable("Choose a password you haven't been using.")
    user.password_hash = hash_password(new)
    signed_out = await revoke_other_sessions(session, user, keep_session)
    await audit.record(
        session,
        action="auth.password_changed",
        user_id=user.id,
        request=request,
        meta={"other_sessions_signed_out": signed_out},
    )
    return signed_out
