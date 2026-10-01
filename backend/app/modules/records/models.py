"""Confirmed health records: the source of truth for schedules, timeline, sync and reports."""

from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base, IdMixin, TimestampMixin


class Prescription(IdMixin, TimestampMixin, Base):
    __tablename__ = "prescriptions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True, unique=True
    )
    extraction_id: Mapped[uuid.UUID | None]
    prescriber_name: Mapped[str | None] = mapped_column(String(120))
    prescriber_specialty: Mapped[str | None] = mapped_column(String(120))
    clinic_name: Mapped[str | None] = mapped_column(String(160))
    prescriber_contact: Mapped[str | None] = mapped_column(String(160))
    issued_on: Mapped[date | None] = mapped_column(Date, index=True)
    follow_up_on: Mapped[date | None] = mapped_column(Date)
    follow_up_notes: Mapped[str | None] = mapped_column(Text)
    summary: Mapped[str | None] = mapped_column(Text)

    medications: Mapped[list[Medication]] = relationship(
        back_populates="prescription",
        cascade="all, delete-orphan",
        order_by="Medication.created_at",
        lazy="selectin",
    )
    care_actions: Mapped[list[CareAction]] = relationship(
        back_populates="prescription",
        cascade="all, delete-orphan",
        order_by="CareAction.due_on",
        lazy="selectin",
    )


class Medication(IdMixin, TimestampMixin, Base):
    __tablename__ = "medications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    prescription_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("prescriptions.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(120))
    strength: Mapped[str | None] = mapped_column(String(60))
    form: Mapped[str | None] = mapped_column(String(40))
    dose: Mapped[str | None] = mapped_column(String(60))
    route: Mapped[str | None] = mapped_column(String(40))
    frequency_raw: Mapped[str | None] = mapped_column(String(120))
    schedule: Mapped[dict] = mapped_column(JSONB, default=dict)
    as_needed: Mapped[bool] = mapped_column(Boolean, default=False)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date | None] = mapped_column(Date)
    duration_days: Mapped[int | None] = mapped_column(Integer)
    instructions: Mapped[str | None] = mapped_column(Text)
    source_page: Mapped[int] = mapped_column(Integer, default=1)
    stopped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    prescription: Mapped[Prescription] = relationship(back_populates="medications")


class CareAction(IdMixin, TimestampMixin, Base):
    __tablename__ = "care_actions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    prescription_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("prescriptions.id", ondelete="CASCADE"), index=True
    )
    kind: Mapped[str] = mapped_column(String(32))
    title: Mapped[str] = mapped_column(String(200))
    notes: Mapped[str | None] = mapped_column(Text)
    due_on: Mapped[date | None] = mapped_column(Date, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    source_page: Mapped[int | None] = mapped_column(Integer)

    prescription: Mapped[Prescription | None] = relationship(back_populates="care_actions")
