"""Care circle: people a user lets see (or help with) their records (ADR-026)."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin


class CareLink(IdMixin, TimestampMixin, Base):
    """An invitation and, once accepted, a grant from `owner` to `caregiver`.

    Invitations are bound to an email address and carry a one-time token; only its hash is stored
    (like share links). status: pending -> active -> revoked (or pending -> revoked).
    """

    __tablename__ = "care_links"
    __table_args__ = (Index("ix_care_links_caregiver_owner", "caregiver_id", "owner_id"),)

    owner_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    caregiver_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    invite_email: Mapped[str] = mapped_column(String(254))
    role: Mapped[str] = mapped_column(String(16))  # viewer | helper
    status: Mapped[str] = mapped_column(String(16), default="pending")
    token_hash: Mapped[str | None] = mapped_column(String(64), unique=True)
    token_hint: Mapped[str | None] = mapped_column(String(8))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # Caregiver's choice (ADR-032): None = no dose alerts, 0 = when a dose is due,
    # 30 / 60 = if it isn't ticked that many minutes after it was due.
    alert_minutes: Mapped[int | None] = mapped_column(Integer)
