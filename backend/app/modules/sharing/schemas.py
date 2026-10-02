from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.modules.records.schemas import PrescriptionOut
from app.modules.visits.schemas import VisitBrief

ShareStatus = Literal["active", "expired", "revoked", "exhausted"]


class ShareItemIn(BaseModel):
    type: Literal["document", "prescription", "visit"]
    id: uuid.UUID


class ShareCreate(BaseModel):
    label: str = Field(min_length=1, max_length=120)
    expires_in_days: int = Field(7, ge=1, le=30)
    max_views: int | None = Field(None, ge=1, le=100)
    items: list[ShareItemIn] = Field(min_length=1, max_length=20)


class ShareItemOut(BaseModel):
    type: str
    id: uuid.UUID
    title: str


class ShareOut(BaseModel):
    id: uuid.UUID
    label: str
    token_hint: str
    status: ShareStatus
    expires_at: datetime
    revoked_at: datetime | None
    max_views: int | None
    view_count: int
    last_viewed_at: datetime | None
    created_at: datetime
    items: list[ShareItemOut]


class ShareCreated(BaseModel):
    share: ShareOut
    url: str
    token: str


class PublicDocument(BaseModel):
    id: uuid.UUID
    title: str
    kind: str
    page_count: int
    document_date: date | None


class PublicShare(BaseModel):
    label: str
    shared_by: str
    expires_at: datetime
    views_left: int | None
    prescriptions: list[PrescriptionOut]
    documents: list[PublicDocument]
    visits: list[VisitBrief] = []
