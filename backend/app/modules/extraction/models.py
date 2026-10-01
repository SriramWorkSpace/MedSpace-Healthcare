from __future__ import annotations

import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, utcnow


class ExtractionStatus(StrEnum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    DISCARDED = "discarded"
    SUPERSEDED = "superseded"


class Extraction(IdMixin, Base):
    """One AI reading of a document. Versioned; only a confirmed version becomes records."""

    __tablename__ = "extractions"

    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(16), default=ExtractionStatus.DRAFT)
    method: Mapped[str] = mapped_column(String(32))  # heuristic | groq-text | groq-vision | none
    model: Mapped[str | None] = mapped_column(String(80))
    payload: Mapped[dict] = mapped_column(JSONB)
    overall_confidence: Mapped[float] = mapped_column(Float, default=0)
    prescription_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("prescriptions.id", ondelete="SET NULL", use_alter=True)
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), default=utcnow
    )
    confirmed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
