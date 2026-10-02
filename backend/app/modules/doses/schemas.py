from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

DoseStatus = Literal["taken", "skipped"]
# How a scheduled dose looks in history. "unlogged" is deliberately not called "missed".
DoseState = Literal["taken", "skipped", "unlogged", "upcoming"]


class DoseLogIn(BaseModel):
    medication_id: uuid.UUID
    date: date
    time: str = Field(pattern=r"^([01]\d|2[0-3]):[0-5]\d$")
    status: DoseStatus


class DoseLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    medication_id: uuid.UUID
    due_date: date
    due_time: str
    status: DoseStatus
    logged_at: datetime


class DoseSlot(BaseModel):
    time: str
    state: DoseState


class AdherenceDay(BaseModel):
    date: date
    doses: list[DoseSlot]


class Counts(BaseModel):
    due: int = 0  # scheduled doses whose time has passed
    taken: int = 0
    skipped: int = 0
    unlogged: int = 0

    @property
    def rate(self) -> float | None:
        return round(self.taken / self.due, 3) if self.due else None


class MedicationAdherence(BaseModel):
    medication_id: uuid.UUID
    name: str
    strength: str | None
    schedule_label: str
    status: str
    counts: Counts
    taken_rate: float | None
    streak_days: int  # consecutive recent days with every due dose taken
    days: list[AdherenceDay]  # oldest first; only days with a scheduled dose


class AdherenceOut(BaseModel):
    start: date
    end: date
    counts: Counts
    taken_rate: float | None
    medications: list[MedicationAdherence]
