"""Medication supply (ADR-023): estimate what's left from the user's own count.

estimated left = counted - units_per_dose x (scheduled doses since the count that weren't marked
skipped). The run-out date is the first future scheduled dose the estimate can't cover. These are
estimates from the user's numbers, labelled as such in the UI; nothing is inferred about refills.
"""

from __future__ import annotations

import math
import uuid
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import utcnow
from app.core.errors import NotFound, Unprocessable
from app.modules.doses import service as doses
from app.modules.identity.models import User
from app.modules.records import service as records
from app.modules.records.models import Medication
from app.modules.supply.models import MedicationSupply
from app.modules.supply.schemas import RefillIn, SupplyIn, SupplyOut

PROJECTION_DAYS = 400
EPS = 1e-9


def _tz(user: User) -> ZoneInfo:
    try:
        return ZoneInfo(user.timezone)
    except Exception:
        return ZoneInfo("UTC")


def _at(day: date, hhmm: str, tz: ZoneInfo) -> datetime:
    h, m = (int(x) for x in hhmm.split(":"))
    return datetime.combine(day, time(h, m), tzinfo=tz)


def estimate(
    m: Medication,
    supply: MedicationSupply,
    user: User,
    skipped: set[tuple[date, str]],
    now: datetime,
) -> SupplyOut:
    """Pure: the estimate for one medicine at `now` (an aware datetime in the user's zone)."""
    tz = _tz(user)
    counted_at = supply.counted_at.astimezone(tz)
    per = supply.units_per_dose

    used = 0.0
    day = counted_at.date()
    while day <= now.date():
        for t in doses.times_due(m, day, user):
            when = _at(day, t, tz)
            if counted_at < when <= now and (day, t) not in skipped:
                used += per
        day += timedelta(days=1)
    left = max(0.0, supply.on_hand - used)

    base = {
        "medication_id": m.id,
        "name": m.name,
        "strength": m.strength,
        "as_needed": m.as_needed,
        "unit": supply.unit,
        "units_per_dose": per,
        "low_days": supply.low_days,
        "counted": supply.on_hand,
        "counted_at": supply.counted_at,
        "estimated_left": round(left, 2),
    }
    if m.as_needed:
        return SupplyOut(**base, doses_left=None, runs_out_on=None, status="as_needed")

    doses_left = math.floor(left / per + EPS)
    remaining = left
    runs_out: date | None = None
    course_covered = False
    day = now.date()
    for _ in range(PROJECTION_DAYS):
        if m.end_date and day > m.end_date:
            course_covered = True
            break
        for t in doses.times_due(m, day, user):
            if _at(day, t, tz) <= now:
                continue
            if remaining + EPS < per:
                runs_out = day
                break
            remaining -= per
        if runs_out:
            break
        day += timedelta(days=1)

    today = now.date()
    if runs_out is None and course_covered:
        status = "course_covered"
    elif left + EPS < per:
        status = "out"
    elif runs_out is not None and runs_out <= today + timedelta(days=supply.low_days):
        status = "low"
    else:
        status = "ok"
    return SupplyOut(**base, doses_left=doses_left, runs_out_on=runs_out, status=status)


async def _supply_for(
    session: AsyncSession, user_id: uuid.UUID, med_id: uuid.UUID
) -> MedicationSupply | None:
    return await session.scalar(
        select(MedicationSupply).where(
            MedicationSupply.medication_id == med_id, MedicationSupply.user_id == user_id
        )
    )


async def _out(session: AsyncSession, user: User, m: Medication, s: MedicationSupply) -> SupplyOut:
    tz = _tz(user)
    since = s.counted_at.astimezone(tz).date()
    skipped = await doses.skipped_since(session, user.id, m.id, since)
    return estimate(m, s, user, skipped, datetime.now(tz))


async def set_supply(
    session: AsyncSession, user: User, med_id: uuid.UUID, data: SupplyIn
) -> SupplyOut:
    m = await records.get_medication(session, user.id, med_id)
    s = await _supply_for(session, user.id, med_id)
    if s is None:
        s = MedicationSupply(user_id=user.id, medication_id=m.id)
        session.add(s)
    s.on_hand = data.on_hand
    s.unit = data.unit
    s.units_per_dose = data.units_per_dose
    s.low_days = data.low_days
    s.counted_at = utcnow()
    await session.flush()
    return await _out(session, user, m, s)


async def refill(session: AsyncSession, user: User, med_id: uuid.UUID, data: RefillIn) -> SupplyOut:
    """Add a refill to today's estimate and restart counting from now."""
    m = await records.get_medication(session, user.id, med_id)
    s = await _supply_for(session, user.id, med_id)
    if s is None:
        raise Unprocessable("Count what you have first, then add refills to it.")
    current = await _out(session, user, m, s)
    s.on_hand = round(current.estimated_left + data.added, 2)
    s.counted_at = utcnow()
    await session.flush()
    return await _out(session, user, m, s)


async def clear_supply(session: AsyncSession, user: User, med_id: uuid.UUID) -> None:
    await records.get_medication(session, user.id, med_id)
    s = await _supply_for(session, user.id, med_id)
    if s is None:
        raise NotFound("No supply is being tracked for this medicine.")
    await session.delete(s)
    await session.flush()


async def list_supplies(session: AsyncSession, user: User) -> list[SupplyOut]:
    """Supplies for current (not stopped, not finished) medicines, soonest to run out first."""
    rows = await session.execute(
        select(Medication, MedicationSupply)
        .join(MedicationSupply, MedicationSupply.medication_id == Medication.id)
        .where(Medication.user_id == user.id, Medication.stopped_at.is_(None))
    )
    out = []
    for m, s in rows.all():
        if records.medication_status(m) == "completed":
            continue
        out.append(await _out(session, user, m, s))
    order = {"out": 0, "low": 1, "ok": 2, "course_covered": 3, "as_needed": 4}
    return sorted(out, key=lambda x: (order[x.status], x.runs_out_on or date.max, x.name))


async def running_low(session: AsyncSession, user: User) -> list[SupplyOut]:
    return [s for s in await list_supplies(session, user) if s.status in ("low", "out")]


# (name, units counted, days before today the count was made, unit)
_DEMO_COUNTS = [
    ("Metformin", 30, 10, "tablets"),
    ("Atorvastatin", 40, 12, "tablets"),
    ("Amoxicillin", 14, 4, "capsules"),
]


async def seed_demo(session: AsyncSession, user: User) -> None:
    """Demo only: counts made at 7 AM on past days, before that day's first dose."""
    tz = _tz(user)
    today = datetime.now(tz).date()
    meds = {
        m.name: m
        for m in (
            await session.scalars(select(Medication).where(Medication.user_id == user.id))
        ).all()
    }
    for name, units, days_ago, unit in _DEMO_COUNTS:
        m = meds.get(name)
        if m is None:
            continue
        day = max(m.start_date, today - timedelta(days=days_ago))
        session.add(
            MedicationSupply(
                user_id=user.id,
                medication_id=m.id,
                on_hand=units,
                unit=unit,
                units_per_dose=1,
                low_days=7,
                counted_at=datetime.combine(day, time(7, 0), tzinfo=tz),
            )
        )
    await session.flush()
