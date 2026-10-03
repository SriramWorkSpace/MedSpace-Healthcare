"""Dose reminders by push notification (ADR-028).

`send_due_reminders` runs every minute (ARQ cron, or a loop in the API process in inline mode).
For each user with a subscribed device it finds scheduled doses whose reminder time (dose time
minus the user's lead) fell in the last few minutes, skips doses already marked or already
reminded, groups doses due at the same time into one notification, and sends it to every device.
Each notification carries a short-lived signed token so "Taken" / "Skip" work from the
notification itself, without the app being open or a session cookie.
"""

from __future__ import annotations

import logging
import uuid
from collections import defaultdict
from datetime import date, datetime, time, timedelta
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

import jwt
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import utcnow
from app.core.errors import NotFound, Unauthorized
from app.modules.doses import service as doses
from app.modules.doses.schemas import DoseLogIn
from app.modules.identity.models import User
from app.modules.records.models import Medication
from app.modules.reminders.models import PushSubscription, ReminderLog, ReminderSettings
from app.modules.reminders.schemas import SettingsIn, SettingsOut, SubscriptionIn, SubscriptionOut
from app.shared.push import Subscription, get_push_sender

logger = logging.getLogger("medspace.reminders")

CATCH_UP = timedelta(minutes=10)  # a late or skipped tick still reminds, but never hours later
TOKEN_TTL = timedelta(hours=12)
MAX_FAILURES = 5


# ---- Subscriptions and settings -----------------------------------------------------------------


def _out(sub: PushSubscription) -> SubscriptionOut:
    return SubscriptionOut(
        id=sub.id,
        endpoint_hint=urlparse(sub.endpoint).netloc,
        user_agent=sub.user_agent,
        created_at=sub.created_at,
        last_success_at=sub.last_success_at,
    )


async def list_subscriptions(session: AsyncSession, user_id: uuid.UUID) -> list[SubscriptionOut]:
    subs = await session.scalars(
        select(PushSubscription)
        .where(PushSubscription.user_id == user_id)
        .order_by(PushSubscription.created_at)
    )
    return [_out(s) for s in subs.all()]


async def subscribe(
    session: AsyncSession, user: User, data: SubscriptionIn, user_agent: str | None
) -> SubscriptionOut:
    """Upsert by endpoint: a browser profile has one endpoint, which follows whoever signed in."""
    endpoint = str(data.endpoint)
    sub = await session.scalar(
        select(PushSubscription).where(PushSubscription.endpoint == endpoint)
    )
    if sub is None:
        sub = PushSubscription(endpoint=endpoint, user_id=user.id)
        session.add(sub)
    sub.user_id = user.id
    sub.p256dh = data.keys.p256dh
    sub.auth = data.keys.auth
    sub.user_agent = (user_agent or "")[:200] or None
    sub.failure_count = 0
    await session.flush()
    await session.refresh(sub)
    return _out(sub)


async def unsubscribe(session: AsyncSession, user_id: uuid.UUID, endpoint: str) -> None:
    result = await session.execute(
        delete(PushSubscription).where(
            PushSubscription.user_id == user_id, PushSubscription.endpoint == endpoint
        )
    )
    if result.rowcount == 0:
        raise NotFound("This device isn't subscribed.")


async def get_settings_for(session: AsyncSession, user_id: uuid.UUID) -> SettingsOut:
    row = await session.scalar(select(ReminderSettings).where(ReminderSettings.user_id == user_id))
    return SettingsOut(enabled=row.enabled, lead_minutes=row.lead_minutes) if row else SettingsOut()


async def update_settings(
    session: AsyncSession, user_id: uuid.UUID, data: SettingsIn
) -> SettingsOut:
    row = await session.scalar(select(ReminderSettings).where(ReminderSettings.user_id == user_id))
    if row is None:
        row = ReminderSettings(user_id=user_id)
        session.add(row)
    row.enabled = data.enabled
    row.lead_minutes = data.lead_minutes
    await session.flush()
    return SettingsOut(enabled=row.enabled, lead_minutes=row.lead_minutes)


# ---- Sending ------------------------------------------------------------------------------------


async def _deliver(session: AsyncSession, user_id: uuid.UUID, payload: dict) -> tuple[int, int]:
    """Send to every device of a user. Returns (sent, removed)."""
    sender = get_push_sender()
    subs = (
        await session.scalars(select(PushSubscription).where(PushSubscription.user_id == user_id))
    ).all()
    sent = removed = 0
    for sub in subs:
        outcome = await sender.send(Subscription(sub.endpoint, sub.p256dh, sub.auth), payload)
        if outcome == "sent":
            sent += 1
            sub.last_success_at = utcnow()
            sub.failure_count = 0
        elif outcome == "gone" or sub.failure_count + 1 >= MAX_FAILURES:
            await session.delete(sub)
            removed += 1
        else:
            sub.failure_count += 1
    await session.flush()
    return sent, removed


async def send_test(session: AsyncSession, user: User) -> tuple[int, int]:
    return await _deliver(
        session,
        user.id,
        {
            "title": "Reminders are on",
            "body": "This is how MedSpace will let you know when a dose is due.",
            "tag": "medspace-test",
            "url": "/app/settings#device",
        },
    )


def _clock(hhmm: str) -> str:
    h, m = (int(x) for x in hhmm.split(":"))
    suffix = "AM" if h < 12 else "PM"
    return f"{(h % 12) or 12}:{m:02d} {suffix}"


def action_token(user_id: uuid.UUID, items: list[tuple[uuid.UUID, date, str]]) -> str:
    """Signed, short-lived permission to mark exactly these doses for this user."""
    now = utcnow()
    return jwt.encode(
        {
            "typ": "dose-action",
            "sub": str(user_id),
            "doses": [[str(m), d.isoformat(), t] for m, d, t in items],
            "iat": now,
            "exp": now + TOKEN_TTL,
        },
        get_settings().jwt_secret.get_secret_value(),
        algorithm="HS256",
    )


def _tz(user: User) -> ZoneInfo:
    try:
        return ZoneInfo(user.timezone)
    except Exception:
        return ZoneInfo("UTC")


async def send_due_reminders(session: AsyncSession, now: datetime | None = None) -> int:
    """One scheduler tick. Returns the number of notifications sent (per dose time, not device)."""
    now = now or utcnow()
    rows = (
        await session.execute(
            select(User, ReminderSettings)
            .join(PushSubscription, PushSubscription.user_id == User.id)
            .outerjoin(ReminderSettings, ReminderSettings.user_id == User.id)
            .distinct()
        )
    ).all()
    notifications = 0
    for user, prefs in rows:
        if prefs is not None and not prefs.enabled:
            continue
        lead = timedelta(minutes=prefs.lead_minutes if prefs else 0)
        notifications += await _remind_user(session, user, now, lead)
    return notifications


async def _remind_user(session: AsyncSession, user: User, now: datetime, lead: timedelta) -> int:
    tz = _tz(user)
    local = now.astimezone(tz)
    meds = (
        await session.scalars(
            select(Medication).where(
                Medication.user_id == user.id,
                Medication.stopped_at.is_(None),
                Medication.as_needed.is_(False),
            )
        )
    ).all()
    due: dict[tuple[date, str], list[Medication]] = defaultdict(list)
    for day in sorted({local.date(), (local + lead).date()}):
        marked = await doses.statuses_on(session, user.id, day)
        for m in meds:
            for t in doses.times_due(m, day, user):
                h, mi = (int(x) for x in t.split(":"))
                remind_at = datetime.combine(day, time(h, mi), tzinfo=tz) - lead
                if local - CATCH_UP < remind_at <= local and (m.id, t) not in marked:
                    due[(day, t)].append(m)

    sent = 0
    for (day, t), group in sorted(due.items()):
        # Claim each dose atomically; another worker (or an earlier tick) may already have.
        claimed: list[Medication] = []
        for m in group:
            result = await session.execute(
                insert(ReminderLog)
                .values(
                    id=uuid.uuid4(), user_id=user.id, medication_id=m.id, due_date=day, due_time=t
                )
                .on_conflict_do_nothing(constraint="uq_reminder_logs_dose")
                .returning(ReminderLog.id)
            )
            if result.scalar_one_or_none():
                claimed.append(m)
        if not claimed:
            continue
        labels = [f"{m.name} {m.strength}".strip() if m.strength else m.name for m in claimed]
        notes = [m.instructions for m in claimed if m.instructions]
        body = ", ".join(labels) + (
            f". {notes[0][:1].upper()}{notes[0][1:]}." if len(notes) == 1 else ""
        )
        payload = {
            "title": f"Time for your {_clock(t)} dose{'s' if len(claimed) > 1 else ''}",
            "body": body,
            "tag": f"dose-{day.isoformat()}-{t}",
            "url": "/app",
            "token": action_token(user.id, [(m.id, day, t) for m in claimed]),
            "actions": [
                {"action": "taken", "title": "Taken"},
                {"action": "skipped", "title": "Skip"},
            ],
        }
        delivered, _ = await _deliver(session, user.id, payload)
        sent += 1 if delivered else 0
    return sent


# ---- Actions from a notification -----------------------------------------------------------------


async def apply_action(session: AsyncSession, token: str, action: str) -> int:
    try:
        claims = jwt.decode(
            token, get_settings().jwt_secret.get_secret_value(), algorithms=["HS256"]
        )
    except jwt.PyJWTError as exc:
        raise Unauthorized("This reminder has expired. Open MedSpace to mark the dose.") from exc
    if claims.get("typ") != "dose-action":
        raise Unauthorized("This reminder has expired. Open MedSpace to mark the dose.")
    user = await session.get(User, uuid.UUID(claims["sub"]))
    if user is None:
        raise Unauthorized("This reminder has expired. Open MedSpace to mark the dose.")
    updated = 0
    for med_id, day, t in claims.get("doses", []):
        try:
            await doses.log_dose(
                session,
                user,
                DoseLogIn(
                    medication_id=med_id, date=date.fromisoformat(day), time=t, status=action
                ),
            )
            updated += 1
        except NotFound:
            continue  # the medicine was removed since the reminder went out
    return updated
