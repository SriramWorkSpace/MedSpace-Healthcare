"""Dose tracking: log scheduled doses as taken or skipped, and summarize the history (ADR-021).

Schedules come from confirmed medications. History is a read model built from the schedule plus
the log; a dose nobody marked is "unlogged", never "missed", because MedSpace cannot know.
"""

from __future__ import annotations

import random
import uuid
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import and_, delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import utcnow
from app.core.errors import NotFound, Unprocessable
from app.modules.doses.models import DoseLog
from app.modules.doses.schemas import (
    AdherenceDay,
    AdherenceOut,
    Counts,
    DoseLogIn,
    DoseLogOut,
    DoseSlot,
    MedicationAdherence,
)
from app.modules.identity.models import User
from app.modules.records import service as records
from app.modules.records.models import Medication


def local_now(user: User) -> datetime:
    try:
        return datetime.now(ZoneInfo(user.timezone))
    except Exception:  # an unknown zone name should never break the dashboard
        return datetime.now(ZoneInfo("UTC"))


def _stop_day(m: Medication, user: User) -> date | None:
    if m.stopped_at is None:
        return None
    try:
        return m.stopped_at.astimezone(ZoneInfo(user.timezone)).date()
    except Exception:
        return m.stopped_at.date()


def times_due(m: Medication, day: date, user: User) -> list[str]:
    """Scheduled HH:MM times for one medicine on one day; a stopped medicine stops counting
    from the day it was stopped (in the user's timezone)."""
    stop = _stop_day(m, user)
    if stop is not None and day >= stop:
        return []
    return records.times_on(m, day)


async def _medication(session: AsyncSession, user_id: uuid.UUID, med_id: uuid.UUID) -> Medication:
    med = await session.scalar(
        select(Medication).where(Medication.id == med_id, Medication.user_id == user_id)
    )
    if med is None:
        raise NotFound("Medication not found.")
    return med


async def log_dose(session: AsyncSession, user: User, data: DoseLogIn) -> DoseLogOut:
    med = await _medication(session, user.id, data.medication_id)
    if data.date > local_now(user).date():
        raise Unprocessable("Doses can't be logged for a future day.")
    if data.time not in times_due(med, data.date, user):
        raise Unprocessable("That dose isn't on this medicine's schedule for that day.")
    now = utcnow()
    stmt = (
        insert(DoseLog)
        .values(
            id=uuid.uuid4(),
            user_id=user.id,
            medication_id=med.id,
            due_date=data.date,
            due_time=data.time,
            status=data.status,
            logged_at=now,
        )
        .on_conflict_do_update(
            constraint="uq_dose_logs_dose",
            set_={"status": data.status, "logged_at": now, "updated_at": now},
        )
    )
    await session.execute(stmt)
    await session.flush()
    return DoseLogOut(
        medication_id=med.id,
        due_date=data.date,
        due_time=data.time,
        status=data.status,
        logged_at=now,
    )


async def clear_dose(
    session: AsyncSession, user: User, med_id: uuid.UUID, day: date, time: str
) -> None:
    await _medication(session, user.id, med_id)
    await session.execute(
        delete(DoseLog).where(
            DoseLog.user_id == user.id,
            DoseLog.medication_id == med_id,
            DoseLog.due_date == day,
            DoseLog.due_time == time,
        )
    )
    await session.flush()


async def statuses_on(
    session: AsyncSession, user_id: uuid.UUID, day: date
) -> dict[tuple[uuid.UUID, str], str]:
    rows = await session.execute(
        select(DoseLog.medication_id, DoseLog.due_time, DoseLog.status).where(
            DoseLog.user_id == user_id, DoseLog.due_date == day
        )
    )
    return {(m, t): s for m, t, s in rows.all()}


def _state(day: date, time: str, logged: str | None, today: date, now_hm: str) -> str:
    if logged:
        return logged
    if day > today or (day == today and time > now_hm):
        return "upcoming"
    return "unlogged"


def _summarize(
    m: Medication, user: User, logs: dict, start: date, end: date, today: date, now_hm: str
) -> MedicationAdherence:
    counts = Counts()
    days: list[AdherenceDay] = []
    day = max(start, m.start_date)
    while day <= end:
        due = times_due(m, day, user)
        if due:
            slots = [
                DoseSlot(time=t, state=_state(day, t, logs.get((m.id, day, t)), today, now_hm))
                for t in due
            ]
            for s in slots:
                if s.state == "upcoming":
                    continue
                counts.due += 1
                setattr(counts, s.state, getattr(counts, s.state) + 1)
            days.append(AdherenceDay(date=day, doses=slots))
        day += timedelta(days=1)

    # Streak: walk back from the newest day; today counts only once its due doses are all taken.
    streak = 0
    for d in reversed(days):
        past = [s for s in d.doses if s.state != "upcoming"]
        if not past:
            continue
        if all(s.state == "taken" for s in past):
            streak += 1
        elif d.date == today:
            continue  # today is still in progress
        else:
            break

    return MedicationAdherence(
        medication_id=m.id,
        name=m.name,
        strength=m.strength,
        schedule_label=(m.schedule or {}).get("label") or "",
        status=records.medication_status(m, today),
        counts=counts,
        taken_rate=counts.rate,
        streak_days=streak,
        days=days,
    )


async def adherence(
    session: AsyncSession,
    user: User,
    days: int = 30,
    medication_id: uuid.UUID | None = None,
) -> AdherenceOut:
    now = local_now(user)
    today, now_hm = now.date(), now.strftime("%H:%M")
    start = today - timedelta(days=days - 1)

    query = select(Medication).where(
        Medication.user_id == user.id,
        Medication.as_needed.is_(False),
        Medication.start_date <= today,
        (Medication.end_date.is_(None)) | (Medication.end_date >= start),
    )
    if medication_id is not None:
        await _medication(session, user.id, medication_id)
        query = query.where(Medication.id == medication_id)
    meds = list((await session.scalars(query.order_by(Medication.start_date.desc()))).all())

    rows = await session.execute(
        select(DoseLog.medication_id, DoseLog.due_date, DoseLog.due_time, DoseLog.status).where(
            and_(DoseLog.user_id == user.id, DoseLog.due_date >= start, DoseLog.due_date <= today)
        )
    )
    logs = {(m, d, t): s for m, d, t, s in rows.all()}

    summaries = [_summarize(m, user, logs, start, today, today, now_hm) for m in meds]
    summaries = [s for s in summaries if s.days] if medication_id is None else summaries
    total = Counts()
    for s in summaries:
        for field in ("due", "taken", "skipped", "unlogged"):
            setattr(total, field, getattr(total, field) + getattr(s.counts, field))
    return AdherenceOut(
        start=start,
        end=today,
        counts=total,
        taken_rate=total.rate,
        medications=summaries,
    )


async def list_logs(session: AsyncSession, user_id: uuid.UUID) -> list[DoseLogOut]:
    rows = await session.scalars(
        select(DoseLog)
        .where(DoseLog.user_id == user_id)
        .order_by(DoseLog.due_date.desc(), DoseLog.due_time.desc())
    )
    return [DoseLogOut.model_validate(r) for r in rows.all()]


async def seed_history(session: AsyncSession, user: User, days: int = 28) -> int:
    """Demo only: a believable recent history (mostly taken, a few skips and gaps).

    Seeded by the user id so a demo account looks the same on every reload. Today is left
    unlogged so visitors can tick doses off themselves.
    """
    rng = random.Random(user.id.int)  # noqa: S311 (synthetic demo data, not security)
    today = local_now(user).date()
    meds = (
        await session.scalars(
            select(Medication).where(Medication.user_id == user.id, Medication.as_needed.is_(False))
        )
    ).all()
    added = 0
    for m in meds:
        day = max(m.start_date, today - timedelta(days=days - 1))
        while day < today:
            for t in times_due(m, day, user):
                roll = rng.random()
                if roll < 0.08:
                    continue  # not logged
                status = "skipped" if roll < 0.12 else "taken"
                session.add(
                    DoseLog(
                        user_id=user.id,
                        medication_id=m.id,
                        due_date=day,
                        due_time=t,
                        status=status,
                    )
                )
                added += 1
            day += timedelta(days=1)
    await session.flush()
    return added
