from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.core.config import get_settings

LEAD_CHOICES = (0, 5, 10, 15, 30)


class SubscriptionKeys(BaseModel):
    p256dh: str = Field(min_length=10, max_length=200)
    auth: str = Field(min_length=8, max_length=100)


# Chrome, Edge, Opera, Samsung (FCM); Firefox; Edge on Windows (WNS); Safari (Apple).
PUSH_HOSTS = (
    "fcm.googleapis.com",
    "updates.push.services.mozilla.com",
    ".notify.windows.com",
    ".push.apple.com",
)


class SubscriptionIn(BaseModel):
    endpoint: HttpUrl
    keys: SubscriptionKeys

    @field_validator("endpoint")
    @classmethod
    def _https(cls, v: HttpUrl) -> HttpUrl:
        if v.scheme != "https":
            raise ValueError("Push endpoints must use https")
        # The server POSTs to this URL every minute: only browsers' push services, never an
        # arbitrary (or internal) host. push.example.com is a reserved test domain, dev only.
        host = (v.host or "").lower()
        allowed = PUSH_HOSTS + (() if get_settings().is_prod else ("push.example.com",))
        if not any(host == h or (h.startswith(".") and host.endswith(h)) for h in allowed):
            raise ValueError("That isn't a browser push service")
        return v


class SubscriptionOut(BaseModel):
    id: uuid.UUID
    endpoint_hint: str  # host only; the full endpoint is a capability, don't echo it back
    user_agent: str | None
    created_at: datetime
    last_success_at: datetime | None


class SettingsIn(BaseModel):
    enabled: bool = True
    lead_minutes: int = 0

    @field_validator("lead_minutes")
    @classmethod
    def _lead(cls, v: int) -> int:
        if v not in LEAD_CHOICES:
            raise ValueError(f"Choose one of {', '.join(map(str, LEAD_CHOICES))} minutes")
        return v


class SettingsOut(SettingsIn):
    pass


class PushConfig(BaseModel):
    public_key: str
    provider: str  # webpush | fake


class TestResult(BaseModel):
    sent: int
    removed: int


class ActionIn(BaseModel):
    token: str = Field(min_length=20, max_length=2000)
    action: Literal["taken", "skipped"]


class ActionResult(BaseModel):
    updated: int
