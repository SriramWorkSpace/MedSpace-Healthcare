from __future__ import annotations

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Question(BaseModel):
    id: str = Field(min_length=1, max_length=40)
    text: str = Field(min_length=1, max_length=300)
    done: bool = False
    prompt_key: str | None = Field(None, max_length=80)

    @field_validator("text")
    @classmethod
    def _strip(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Write the question or remove it")
        return v


class VisitCreate(BaseModel):
    title: str | None = Field(None, max_length=120)
    visit_date: date | None = None
    clinician: str | None = Field(None, max_length=120)
    since: date | None = None


class VisitUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=120)
    visit_date: date | None = None
    clinician: str | None = Field(None, max_length=120)
    since: date | None = None
    questions: list[Question] | None = Field(None, max_length=30)


class VisitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    visit_date: date | None
    clinician: str | None
    since: date | None
    questions: list[Question]
    created_at: datetime
    updated_at: datetime


# ---- The brief (read model) --------------------------------------------------------------------


class BriefMedication(BaseModel):
    id: uuid.UUID
    name: str
    strength: str | None
    schedule: str
    times: list[str]
    instructions: str | None
    status: str
    start_date: date
    end_date: date | None
    prescriber_name: str | None


class BriefChange(BaseModel):
    kind: str  # started | stopped | finished | starts
    date: date
    name: str
    strength: str | None


class BriefDoses(BaseModel):
    medication_id: uuid.UUID
    name: str
    strength: str | None
    due: int
    taken: int
    skipped: int
    unlogged: int


class BriefLab(BaseModel):
    key: str
    name: str
    value_text: str
    unit: str | None
    ref_range: str | None
    flag: str | None
    collected_on: date
    previous_value_text: str | None = None
    previous_collected_on: date | None = None


class BriefTodo(BaseModel):
    id: uuid.UUID
    title: str
    due_on: date | None


class BriefAppointment(BaseModel):
    date: date
    title: str
    subtitle: str | None


class BriefDocument(BaseModel):
    id: uuid.UUID
    title: str
    kind: str
    date: date


class Prompt(BaseModel):
    """A fact from the records the user may want to raise. Never advice, never interpretation."""

    key: str
    text: str


class VisitBrief(BaseModel):
    visit: VisitOut
    since: date
    until: date
    patient: str
    medications: list[BriefMedication]
    changes: list[BriefChange]
    doses: list[BriefDoses]
    labs: list[BriefLab]
    todos: list[BriefTodo]
    appointments: list[BriefAppointment]
    diet_notes: list[str]
    documents: list[BriefDocument]
    prompts: list[Prompt]
