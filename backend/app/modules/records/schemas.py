from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.modules.extraction.schemas import ScheduleModel

MedicationStatus = Literal["active", "upcoming", "completed", "stopped"]


class MedicationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    prescription_id: uuid.UUID
    name: str
    strength: str | None
    form: str | None
    dose: str | None
    route: str | None
    frequency_raw: str | None
    schedule: ScheduleModel
    as_needed: bool
    start_date: date
    end_date: date | None
    duration_days: int | None
    instructions: str | None
    source_page: int
    stopped_at: datetime | None
    status: MedicationStatus = "active"
    day_of_course: int | None = None
    document_id: uuid.UUID | None = None
    prescriber_name: str | None = None


class CareActionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    prescription_id: uuid.UUID | None
    kind: str
    title: str
    notes: str | None
    due_on: date | None
    completed_at: datetime | None
    source_page: int | None


class PrescriptionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    document_id: uuid.UUID
    document_title: str | None = None
    prescriber_name: str | None
    prescriber_specialty: str | None
    clinic_name: str | None
    issued_on: date | None
    follow_up_on: date | None
    medication_count: int = 0
    active_count: int = 0
    created_at: datetime


class PrescriptionOut(PrescriptionSummary):
    prescriber_contact: str | None
    follow_up_notes: str | None
    summary: str | None
    medications: list[MedicationOut]
    care_actions: list[CareActionOut]


class MedicationUpdate(BaseModel):
    schedule: ScheduleModel | None = None
    instructions: str | None = Field(None, max_length=500)
    end_date: date | None = None
    stopped: bool | None = None


class CareActionUpdate(BaseModel):
    completed: bool | None = None
    due_on: date | None = None
    title: str | None = Field(None, min_length=1, max_length=200)
