from __future__ import annotations

import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    original_filename: str
    kind: str
    mime_type: str
    size_bytes: int
    page_count: int
    has_text_layer: bool
    status: str
    error: str | None
    document_date: date | None
    processed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class DocumentPageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    page_no: int
    text: str


class DocumentDetail(DocumentOut):
    pages: list[DocumentPageOut] = Field(default_factory=list)


class DocumentList(BaseModel):
    items: list[DocumentOut]
    counts: dict[str, int]


class DocumentUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    kind: str | None = Field(None, pattern="^(prescription|lab_report|other)$")
