"""Medication supply: what the user counted on hand, so MedSpace can estimate when it runs out."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, IdMixin, TimestampMixin


class MedicationSupply(IdMixin, TimestampMixin, Base):
    """One count per medicine (ADR-023). Estimates are derived from this count, the schedule and
    any doses marked skipped since the count; nothing here is a prescription fact."""

    __tablename__ = "medication_supplies"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    medication_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("medications.id", ondelete="CASCADE"), unique=True
    )
    on_hand: Mapped[float] = mapped_column(Float)  # units counted at counted_at
    unit: Mapped[str] = mapped_column(String(20), default="tablets")
    units_per_dose: Mapped[float] = mapped_column(Float, default=1.0)
    low_days: Mapped[int] = mapped_column(Integer, default=7)  # "running low" threshold
    counted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
