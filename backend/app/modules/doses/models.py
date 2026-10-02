"""Dose log: what the user marked for each scheduled dose (ADR-021)."""

from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin, utcnow


class DoseLog(IdMixin, TimestampMixin, Base):
    """One scheduled dose the user marked as taken or skipped.

    Doses with no row are simply "not logged": MedSpace never assumes a dose was missed.
    `due_date` is the calendar day in the user's timezone and `due_time` the scheduled HH:MM.
    """

    __tablename__ = "dose_logs"
    __table_args__ = (
        UniqueConstraint("medication_id", "due_date", "due_time", name="uq_dose_logs_dose"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    medication_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("medications.id", ondelete="CASCADE"), index=True
    )
    due_date: Mapped[date] = mapped_column(Date)
    due_time: Mapped[str] = mapped_column(String(5))
    status: Mapped[str] = mapped_column(String(8))  # taken | skipped
    logged_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
