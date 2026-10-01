from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin


class OAuthConnection(IdMixin, TimestampMixin, Base):
    """A connected Google account. Tokens are Fernet-encrypted at rest (ADR-008)."""

    __tablename__ = "oauth_connections"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    provider: Mapped[str] = mapped_column(String(16), default="google")
    mode: Mapped[str] = mapped_column(String(16), default="live")  # live | simulation
    account_email: Mapped[str | None] = mapped_column(String(320))
    scopes: Mapped[str] = mapped_column(Text, default="")
    access_token_enc: Mapped[str] = mapped_column(Text)
    refresh_token_enc: Mapped[str | None] = mapped_column(Text)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    tasklist_id: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(16), default="active")  # active | revoked

    __table_args__ = (UniqueConstraint("user_id", "provider", name="uq_oauth_user_provider"),)


class SyncLink(IdMixin, TimestampMixin, Base):
    """Maps a MedSpace entity (one dose slot, an appointment, a to-do) to its remote copy."""

    __tablename__ = "sync_links"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    prescription_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("prescriptions.id", ondelete="CASCADE"), index=True
    )
    target: Mapped[str] = mapped_column(String(24))  # google_calendar | google_tasks
    entity_type: Mapped[str] = mapped_column(String(24))  # dose | appointment | care_action
    entity_id: Mapped[uuid.UUID]
    slot: Mapped[str] = mapped_column(String(16), default="")  # dose time, e.g. "08:00"
    external_id: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(String(255), default="")
    meta: Mapped[dict] = mapped_column(JSONB, default=dict)

    __table_args__ = (
        UniqueConstraint(
            "user_id", "target", "entity_type", "entity_id", "slot", name="uq_sync_link_entity"
        ),
    )
