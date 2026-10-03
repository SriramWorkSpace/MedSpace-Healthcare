from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin, utcnow

DEFAULT_DOSE_TIMES = {
    "morning": "08:00",
    "afternoon": "14:00",
    "evening": "20:00",
    "bedtime": "22:00",
}


class User(IdMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    # Null for accounts created through "Continue with Google" (no password set).
    password_hash: Mapped[str | None] = mapped_column(String(256))
    google_sub: Mapped[str | None] = mapped_column(String(64), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(80))
    timezone: Mapped[str] = mapped_column(String(64), default="UTC")
    dose_times: Mapped[dict] = mapped_column(JSONB, default=lambda: dict(DEFAULT_DOSE_TIMES))
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # Two-step verification (ADR-029). Secrets are Fernet-encrypted at rest.
    totp_secret_enc: Mapped[str | None] = mapped_column(Text)
    totp_pending_enc: Mapped[str | None] = mapped_column(Text)  # set up but not yet confirmed
    totp_enabled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    totp_last_step: Mapped[int | None] = mapped_column(Integer)  # replay protection

    @property
    def has_password(self) -> bool:
        return self.password_hash is not None

    @property
    def google_linked(self) -> bool:
        return self.google_sub is not None

    @property
    def mfa_enabled(self) -> bool:
        return self.totp_enabled_at is not None


class RefreshToken(IdMixin, Base):
    """Opaque refresh token, stored hashed. Rotated on every use; reuse revokes the family."""

    __tablename__ = "refresh_tokens"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    family_id: Mapped[uuid.UUID] = mapped_column(index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    replaced_by: Mapped[uuid.UUID | None]
    ip: Mapped[str | None] = mapped_column(String(64))
    user_agent: Mapped[str | None] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=utcnow
    )


class RecoveryCode(IdMixin, Base):
    """One-time backup codes for two-step verification; only hashes are stored."""

    __tablename__ = "recovery_codes"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    code_hash: Mapped[str] = mapped_column(String(64))
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
