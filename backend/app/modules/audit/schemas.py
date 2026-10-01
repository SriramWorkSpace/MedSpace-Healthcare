from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    actor: str
    action: str
    entity_type: str | None
    entity_id: uuid.UUID | None
    ip: str | None
    user_agent: str | None
    meta: dict
    created_at: datetime


class AuditPage(BaseModel):
    items: list[AuditLogOut]
    next_cursor: str | None
