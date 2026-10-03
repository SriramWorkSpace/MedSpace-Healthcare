"""Dose reminders by push notification (ADR-028)."""

from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin, utcnow


class PushSubscription(IdMixin, TimestampMixin, Base):
    """One browser (or installed app) that agreed to receive notifications."""

    __tablename__ = "push_subscriptions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    endpoint: Mapped[str] = mapped_column(Text, unique=True)
    p256dh: Mapped[str] = mapped_column(String(200))
    auth: Mapped[str] = mapped_column(String(100))
    user_agent: Mapped[str | None] = mapped_column(String(200))
    last_success_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    failure_count: Mapped[int] = mapped_column(Integer, default=0)


class ReminderSettings(IdMixin, TimestampMixin, Base):
    __tablename__ = "reminder_settings"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    lead_minutes: Mapped[int] = mapped_column(Integer, default=0)


class ReminderLog(IdMixin, Base):
    """A scheduled dose that was already reminded about, so it is never sent twice."""

    __tablename__ = "reminder_logs"
    __table_args__ = (
        UniqueConstraint("medication_id", "due_date", "due_time", name="uq_reminder_logs_dose"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    medication_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("medications.id", ondelete="CASCADE")
    )
    due_date: Mapped[date] = mapped_column(Date)
    due_time: Mapped[str] = mapped_column(String(5))
    sent_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
