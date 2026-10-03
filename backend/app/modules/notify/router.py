"""Dev-only outbox: read simulated emails (local testing and e2e). Never mounted in prod."""

from __future__ import annotations

import re

from fastapi import APIRouter, Query

from app.core.errors import NotFound
from app.shared.mail import FakeMailer, get_mailer

dev_router = APIRouter(prefix="/dev", tags=["dev"])

_LINK = re.compile(r"https?://\S+")


@dev_router.get("/outbox")
async def outbox(to: str = Query(min_length=3, max_length=320), limit: int = Query(5, le=50)):
    mailer = get_mailer()
    if not isinstance(mailer, FakeMailer):
        raise NotFound("The outbox only exists when email is simulated.")
    return [
        {"to": m.to, "subject": m.subject, "text": m.text, "links": _LINK.findall(m.text)}
        for m in mailer.latest(to)[:limit]
    ]
