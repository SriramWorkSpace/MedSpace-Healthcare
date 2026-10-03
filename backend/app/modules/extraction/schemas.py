"""Extraction payload: what the AI read, plus deterministic normalization, pending user review."""

from __future__ import annotations

import datetime as dt
import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.extraction import labs
from app.modules.extraction.labs import LabFlag

CareActionKind = Literal[
    "lab_test", "follow_up", "course_completion", "upload_report", "prepare_documents", "other"
]


class ScheduleModel(BaseModel):
    times: list[str] = Field(default_factory=list)
    period: str = "daily"
    as_needed: bool = False
    interval_hours: int | None = None
    label: str = ""
    needs_attention: bool = False

    @field_validator("times")
    @classmethod
    def _valid_times(cls, v: list[str]) -> list[str]:
        import re

        for t in v:
            if not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", t):
                raise ValueError(f"'{t}' is not a valid HH:MM time")
        return sorted(set(v))


class Prescriber(BaseModel):
    name: str | None = None
    specialty: str | None = None
    clinic: str | None = None
    contact: str | None = None


class FollowUp(BaseModel):
    date: dt.date | None = None
    notes: str | None = None


class ExtractedMedication(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    strength: str | None = None
    form: str | None = None
    dose: str | None = None
    route: str | None = None
    frequency_raw: str | None = None
    duration_raw: str | None = None
    duration_days: int | None = Field(None, ge=1, le=3650)
    instructions: str | None = None
    as_needed: bool = False
    source_page: int = Field(1, ge=1)
    confidence: float = Field(0.8, ge=0, le=1)
    uncertain_fields: list[str] = Field(default_factory=list)
    schedule: ScheduleModel | None = None


class ExtractedCareAction(BaseModel):
    kind: CareActionKind = "other"
    title: str = Field(min_length=1, max_length=200)
    due_on: date | None = None
    notes: str | None = None
    source_page: int = Field(1, ge=1)
    confidence: float = Field(0.8, ge=0, le=1)


DietCategory = Literal["avoid", "limit", "include", "timing", "general"]


class ExtractedDietNote(BaseModel):
    """A diet, food or drink instruction written on the document (copied, never invented)."""

    text: str = Field(min_length=1, max_length=300)
    category: DietCategory = "general"
    source_page: int = Field(1, ge=1)
    confidence: float = Field(0.8, ge=0, le=1)


class ExtractedLabResult(BaseModel):
    """One test result, copied as printed: the value, its unit and the report's reference range."""

    name: str = Field(min_length=1, max_length=120)
    value: str = Field(min_length=1, max_length=40)
    unit: str | None = Field(None, max_length=30)
    ref_range: str | None = Field(None, max_length=60)
    flag: LabFlag | None = None
    source_page: int = Field(1, ge=1)
    confidence: float = Field(0.8, ge=0, le=1)


class ExtractionPayload(BaseModel):
    document_type: Literal["prescription", "lab_report", "other"] = "prescription"
    prescriber: Prescriber | None = None
    patient_name: str | None = None
    issued_on: date | None = None
    follow_up: FollowUp | None = None
    medications: list[ExtractedMedication] = Field(default_factory=list)
    care_actions: list[ExtractedCareAction] = Field(default_factory=list)
    diet_notes: list[ExtractedDietNote] = Field(default_factory=list)
    lab_results: list[ExtractedLabResult] = Field(default_factory=list)
    summary: str | None = None
    overall_confidence: float = Field(0.8, ge=0, le=1)
    warnings: list[str] = Field(default_factory=list)


class ExtractionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    document_id: uuid.UUID
    version: int
    status: str
    method: str
    model: str | None
    payload: ExtractionPayload
    overall_confidence: float
    created_at: datetime
    confirmed_at: datetime | None
    prescription_id: uuid.UUID | None


# ---- Confirmation (the user's reviewed, possibly edited, version) -----------------------------


class ConfirmMedication(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    strength: str | None = Field(None, max_length=60)
    form: str | None = Field(None, max_length=40)
    dose: str | None = Field(None, max_length=60)
    route: str | None = Field(None, max_length=40)
    frequency_raw: str | None = Field(None, max_length=120)
    schedule: ScheduleModel
    start_date: date | None = None
    duration_days: int | None = Field(None, ge=1, le=3650)
    instructions: str | None = Field(None, max_length=500)
    source_page: int = Field(1, ge=1)


class ConfirmCareAction(BaseModel):
    kind: CareActionKind = "other"
    title: str = Field(min_length=1, max_length=200)
    due_on: date | None = None
    notes: str | None = Field(None, max_length=500)
    source_page: int | None = None


class ConfirmDietNote(BaseModel):
    text: str = Field(min_length=1, max_length=300)
    category: DietCategory = "general"
    source_page: int | None = None


class ConfirmLabResult(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    value: str = Field(min_length=1, max_length=40)
    unit: str | None = Field(None, max_length=30)
    ref_range: str | None = Field(None, max_length=60)
    flag: LabFlag | None = None  # as printed on the report; the printed range takes precedence
    source_page: int | None = None

    def normalized(self) -> dict:
        """Columns derived deterministically from what the user confirmed."""
        ref = labs.parse_range(self.ref_range)
        return {
            "analyte_key": labs.analyte_key(self.name),
            "value": labs.parse_value(self.value),
            "ref_low": ref.low if ref else None,
            "ref_high": ref.high if ref else None,
            "flag": labs.resolve_flag(self.value, self.ref_range, self.flag),
        }


class ConfirmIn(BaseModel):
    document_kind: Literal["prescription", "lab_report", "other"] = "prescription"
    prescriber: Prescriber | None = None
    issued_on: date | None = None
    follow_up: FollowUp | None = None
    medications: list[ConfirmMedication] = Field(default_factory=list, max_length=40)
    care_actions: list[ConfirmCareAction] = Field(default_factory=list, max_length=40)
    diet_notes: list[ConfirmDietNote] = Field(default_factory=list, max_length=30)
    lab_results: list[ConfirmLabResult] = Field(default_factory=list, max_length=80)
    summary: str | None = Field(None, max_length=2000)


class EvidenceSpot(BaseModel):
    page: int
    boxes: list[list[float]]  # [x0, y0, x1, y1] as fractions of the page


class EvidenceOut(BaseModel):
    """Where each field of the latest extraction is printed. Keys are review-form paths
    ("medications.0.strength"); `items` holds one spot per item ("medications.0")."""

    extraction_id: uuid.UUID
    available: bool
    reason: str | None = None  # "no_text": a photo or scan, nothing to search
    fields: dict[str, EvidenceSpot]
    items: dict[str, EvidenceSpot]
