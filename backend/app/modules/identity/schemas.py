from __future__ import annotations

import re
import uuid
from datetime import datetime
from zoneinfo import available_timezones

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

_TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")
DOSE_SLOTS = ("morning", "afternoon", "evening", "bedtime")


class SignupIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)
    display_name: str = Field(min_length=1, max_length=80)
    timezone: str = "UTC"

    @field_validator("email")
    @classmethod
    def _lower(cls, v: str) -> str:
        return v.lower()

    @field_validator("display_name")
    @classmethod
    def _strip(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be blank")
        return v

    @field_validator("timezone")
    @classmethod
    def _tz(cls, v: str) -> str:
        return v if v in available_timezones() else "UTC"


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def _lower(cls, v: str) -> str:
        return v.lower()


class ProfileUpdate(BaseModel):
    display_name: str | None = Field(None, min_length=1, max_length=80)
    timezone: str | None = None
    dose_times: dict[str, str] | None = None

    @field_validator("timezone")
    @classmethod
    def _tz(cls, v: str | None) -> str | None:
        if v is not None and v not in available_timezones():
            raise ValueError("Unknown timezone")
        return v

    @field_validator("dose_times")
    @classmethod
    def _times(cls, v: dict[str, str] | None) -> dict[str, str] | None:
        if v is None:
            return v
        for slot, value in v.items():
            if slot not in DOSE_SLOTS:
                raise ValueError(f"Unknown dose slot '{slot}'")
            if not _TIME_RE.match(value):
                raise ValueError(f"'{value}' is not a valid HH:MM time")
        return v


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    display_name: str
    timezone: str
    dose_times: dict[str, str]
    is_demo: bool
    has_password: bool = True
    google_linked: bool = False
    created_at: datetime
