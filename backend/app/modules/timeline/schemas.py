from __future__ import annotations

import uuid
from datetime import date
from typing import Literal

from pydantic import BaseModel

EventType = Literal[
    "prescription", "medication_start", "medication_end", "appointment", "task", "document"
]


class TimelineEvent(BaseModel):
    id: str
    type: EventType
    date: date
    title: str
    subtitle: str | None = None
    upcoming: bool = False
    completed: bool | None = None
    document_id: uuid.UUID | None = None
    prescription_id: uuid.UUID | None = None
    medication_id: uuid.UUID | None = None
    care_action_id: uuid.UUID | None = None


class TimelinePage(BaseModel):
    items: list[TimelineEvent]
    next_cursor: str | None


class DoseOut(BaseModel):
    time: str
    medication_id: uuid.UUID
    name: str
    strength: str | None
    instructions: str | None
    prescription_id: uuid.UUID
    status: str | None = None  # taken | skipped, when the user logged it


class AsNeededOut(BaseModel):
    medication_id: uuid.UUID
    name: str
    strength: str | None
    instructions: str | None


class ReviewItem(BaseModel):
    id: uuid.UUID
    title: str
    status: str


class DayLoad(BaseModel):
    date: date
    doses: int


class DashboardOut(BaseModel):
    today: date
    doses_today: list[DoseOut]
    as_needed: list[AsNeededOut]
    upcoming: list[TimelineEvent]
    needs_review: list[ReviewItem]
    processing: int
    week: list[DayLoad]
    stats: dict[str, int]
