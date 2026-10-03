from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field

Role = Literal["viewer", "helper"]


class InviteIn(BaseModel):
    email: EmailStr
    role: Role = "viewer"


class RoleIn(BaseModel):
    role: Role


class AcceptIn(BaseModel):
    token: str = Field(min_length=20, max_length=200)


class Person(BaseModel):
    id: uuid.UUID | None
    name: str
    email: str


class CareLinkOut(BaseModel):
    id: uuid.UUID
    role: Role
    status: str  # pending | active | expired | revoked
    person: Person  # the other side of the link
    created_at: datetime
    accepted_at: datetime | None
    expires_at: datetime


class CircleOut(BaseModel):
    caregivers: list[CareLinkOut]  # people with access to my records
    caring_for: list[CareLinkOut]  # people whose records I can open


class InviteCreated(BaseModel):
    link: CareLinkOut
    url: str
    token: str
    emailed: bool = False  # also sent to their inbox (never from demo accounts)


class InvitePreview(BaseModel):
    owner_name: str
    role: Role
    email: str
    status: str
    expires_at: datetime
