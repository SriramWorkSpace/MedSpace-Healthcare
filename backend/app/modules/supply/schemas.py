from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

SupplyStatus = Literal["ok", "low", "out", "as_needed", "course_covered"]


class SupplyIn(BaseModel):
    on_hand: float = Field(ge=0, le=10000)
    unit: str = Field("tablets", min_length=1, max_length=20)
    units_per_dose: float = Field(1, gt=0, le=50)
    low_days: int = Field(7, ge=1, le=60)

    @field_validator("unit")
    @classmethod
    def _unit(cls, v: str) -> str:
        return v.strip().lower()


class RefillIn(BaseModel):
    added: float = Field(gt=0, le=10000)


class SupplyOut(BaseModel):
    medication_id: uuid.UUID
    name: str
    strength: str | None
    as_needed: bool
    unit: str
    units_per_dose: float
    low_days: int
    counted: float  # what the user counted
    counted_at: datetime
    estimated_left: float  # after scheduled doses since the count (skipped ones excluded)
    doses_left: int | None  # whole doses the estimate covers; None for as-needed
    runs_out_on: date | None  # first scheduled dose the supply can't cover
    status: SupplyStatus
