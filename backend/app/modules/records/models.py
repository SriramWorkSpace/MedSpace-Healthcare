"""Confirmed health records: the source of truth for schedules, timeline, sync and reports."""

from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Index, Integer, String, Text
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
    # Item of the confirmed reading it came from ("medications.2"), for highlights (ADR-031).
    source_ref: Mapped[str | None] = mapped_column(String(32))
    stopped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    prescription: Mapped[Prescription] = relationship(back_populates="medications")


class DietNote(IdMixin, TimestampMixin, Base):
    """A diet, food or drink instruction copied from a confirmed document.

    Tied to the document (not only the prescription) so letters and reports can carry notes too.
    """

    __tablename__ = "diet_notes"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True
    )
    prescription_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("prescriptions.id", ondelete="SET NULL"), index=True
    )
    text: Mapped[str] = mapped_column(String(300))
    category: Mapped[str] = mapped_column(String(16), default="general")
    source_page: Mapped[int | None] = mapped_column(Integer)
    # Item of the confirmed reading it came from ("medications.2"), for highlights (ADR-031).
    source_ref: Mapped[str | None] = mapped_column(String(32))


class LabResult(IdMixin, TimestampMixin, Base):
    """One test result copied from a confirmed lab report (ADR-020).

    value_text and ref_range are exactly as printed; value, ref_low, ref_high and flag are parsed
    from them deterministically so results can be charted. The flag only ever compares a value
    with the range printed on the same report.
    """

    __tablename__ = "lab_results"
    __table_args__ = (Index("ix_lab_results_user_analyte", "user_id", "analyte_key"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(120))
    analyte_key: Mapped[str] = mapped_column(String(80))
    value_text: Mapped[str] = mapped_column(String(40))
    value: Mapped[float | None] = mapped_column(Float)
    unit: Mapped[str | None] = mapped_column(String(30))
    ref_range: Mapped[str | None] = mapped_column(String(60))
    ref_low: Mapped[float | None] = mapped_column(Float)
    ref_high: Mapped[float | None] = mapped_column(Float)
    flag: Mapped[str | None] = mapped_column(String(8))
    collected_on: Mapped[date] = mapped_column(Date)
    position: Mapped[int] = mapped_column(Integer, default=0)
    source_page: Mapped[int | None] = mapped_column(Integer)
    # Item of the confirmed reading it came from ("medications.2"), for highlights (ADR-031).
    source_ref: Mapped[str | None] = mapped_column(String(32))


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
    # Item of the confirmed reading it came from ("medications.2"), for highlights (ADR-031).
    source_ref: Mapped[str | None] = mapped_column(String(32))

    prescription: Mapped[Prescription | None] = relationship(back_populates="care_actions")
