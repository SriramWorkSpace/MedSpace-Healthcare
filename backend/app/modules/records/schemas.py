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


class DietNoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    text: str
    category: str
    source_page: int | None
    document_id: uuid.UUID
    document_title: str | None = None
    prescriber_name: str | None = None
    issued_on: date | None = None
    created_at: datetime


class MedicationFoodNote(BaseModel):
    """A food or drink instruction attached to one of the user's current medicines."""

    medication_id: uuid.UUID
    name: str
    strength: str | None
    text: str
    category: str
    document_id: uuid.UUID | None
    source_page: int


class DietNotesOut(BaseModel):
    notes: list[DietNoteOut]
    medication_notes: list[MedicationFoodNote]


class LabResultOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    analyte_key: str
    value_text: str
    value: float | None
    unit: str | None
    ref_range: str | None
    ref_low: float | None
    ref_high: float | None
    flag: str | None
    collected_on: date
    source_page: int | None
    document_id: uuid.UUID
    document_title: str | None = None


class LabPoint(BaseModel):
    value: float
    collected_on: date
    flag: str | None


class LabTrendOut(BaseModel):
    """Every result for one test, newest first, with a chartable series in the latest unit."""

    key: str
    name: str
    unit: str | None
    count: int
    latest: LabResultOut
    previous: LabResultOut | None
    points: list[LabPoint]
    uncharted: int  # results in another unit, or not numeric


class LabTrendDetail(LabTrendOut):
    results: list[LabResultOut]


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
    diet_notes: list[DietNoteOut] = []


class MedicationUpdate(BaseModel):
    schedule: ScheduleModel | None = None
    instructions: str | None = Field(None, max_length=500)
    end_date: date | None = None
    stopped: bool | None = None


class CareActionUpdate(BaseModel):
    completed: bool | None = None
    due_on: date | None = None
    title: str | None = Field(None, min_length=1, max_length=200)
