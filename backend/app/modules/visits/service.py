"""Visit prep (ADR-022): the user's questions plus a live brief assembled from confirmed records.

The brief reports what the records say since a date: medicine changes, dose marks, new lab
results, open to-dos. "Prompts" are facts the user may want to raise; they are worded as
observations about the records, never as advice or interpretation.
"""

from __future__ import annotations

import uuid
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFound, Unprocessable
from app.modules.documents import service as documents
from app.modules.doses import service as doses
from app.modules.identity.models import User
from app.modules.records import service as records
from app.modules.timeline import service as timeline
from app.modules.visits.models import VisitPrep
from app.modules.visits.schemas import (
    BriefAppointment,
    BriefChange,
    BriefDocument,
    BriefDoses,
    BriefLab,
    BriefMedication,
    BriefTodo,
    Prompt,
    VisitBrief,
    VisitCreate,
    VisitOut,
    VisitUpdate,
)

DEFAULT_LOOKBACK_DAYS = 90
MAX_WINDOW_DAYS = 120


def _day(d: date) -> str:
    return f"{d:%b} {d.day}, {d.year}"


def _label(name: str, strength: str | None) -> str:
    return f"{name} {strength}".strip() if strength else name


def default_title(clinician: str | None) -> str:
    return f"Visit with {clinician}" if clinician else "Upcoming visit"


async def get_prep(session: AsyncSession, user_id: uuid.UUID, prep_id: uuid.UUID) -> VisitPrep:
    prep = await session.scalar(
        select(VisitPrep).where(VisitPrep.id == prep_id, VisitPrep.user_id == user_id)
    )
    if prep is None:
        raise NotFound("Visit prep not found.")
    return prep


async def list_preps(session: AsyncSession, user_id: uuid.UUID) -> list[VisitPrep]:
    rows = await session.scalars(
        select(VisitPrep)
        .where(VisitPrep.user_id == user_id)
        .order_by(VisitPrep.visit_date.desc().nulls_first(), VisitPrep.created_at.desc())
    )
    return list(rows.all())


def _check_since(since: date | None, user: User) -> None:
    if since is not None and since > timeline.user_today(user):
        raise Unprocessable("'Changes since' can't be in the future.")


async def create_prep(session: AsyncSession, user: User, data: VisitCreate) -> VisitPrep:
    _check_since(data.since, user)
    clinician = (data.clinician or "").strip() or None
    prep = VisitPrep(
        user_id=user.id,
        title=(data.title or "").strip() or default_title(clinician),
        visit_date=data.visit_date,
        clinician=clinician,
        since=data.since,
        questions=[],
    )
    session.add(prep)
    await session.flush()
    return prep


async def update_prep(
    session: AsyncSession, user: User, prep_id: uuid.UUID, data: VisitUpdate
) -> VisitPrep:
    prep = await get_prep(session, user.id, prep_id)
    fields = data.model_fields_set
    if "since" in fields:
        _check_since(data.since, user)
        prep.since = data.since
    if "title" in fields and data.title:
        prep.title = data.title.strip()
    if "visit_date" in fields:
        prep.visit_date = data.visit_date
    if "clinician" in fields:
        prep.clinician = (data.clinician or "").strip() or None
    if "questions" in fields and data.questions is not None:
        ids = [q.id for q in data.questions]
        if len(ids) != len(set(ids)):
            raise Unprocessable("Question ids must be unique.")
        prep.questions = [q.model_dump() for q in data.questions]
    await session.flush()
    await session.refresh(prep)
    return prep


async def delete_prep(session: AsyncSession, user_id: uuid.UUID, prep_id: uuid.UUID) -> None:
    await session.delete(await get_prep(session, user_id, prep_id))
    await session.flush()


async def effective_since(session: AsyncSession, prep: VisitPrep, today: date) -> date:
    """The chosen date, else the previous visit's date, else 90 days back."""
    if prep.since:
        return prep.since
    anchor = prep.visit_date or today
    previous = await session.scalar(
        select(VisitPrep.visit_date)
        .where(
            VisitPrep.user_id == prep.user_id,
            VisitPrep.id != prep.id,
            VisitPrep.visit_date.is_not(None),
            VisitPrep.visit_date < anchor,
            VisitPrep.visit_date <= today,
        )
        .order_by(VisitPrep.visit_date.desc())
        .limit(1)
    )
    since = previous or today - timedelta(days=DEFAULT_LOOKBACK_DAYS)
    return max(since, today - timedelta(days=MAX_WINDOW_DAYS - 1))


async def brief(session: AsyncSession, user: User, prep: VisitPrep) -> VisitBrief:
    today = timeline.user_today(user)
    since = await effective_since(session, prep, today)
    since = min(since, today)

    meds = await records.list_medications(session, user.id)
    current = [m for m in meds if m.status in ("active", "upcoming")]
    medications = [
        BriefMedication(
            id=m.id,
            name=m.name,
            strength=m.strength,
            schedule=m.schedule.label or ("As needed" if m.as_needed else "Schedule not set"),
            times=m.schedule.times,
            instructions=m.instructions,
            status=m.status,
            start_date=m.start_date,
            end_date=m.end_date,
            prescriber_name=m.prescriber_name,
        )
        for m in current
    ]

    changes: list[BriefChange] = []
    for m in meds:
        stopped_on = m.stopped_at.date() if m.stopped_at else None
        if since <= m.start_date <= today:
            changes.append(
                BriefChange(kind="started", date=m.start_date, name=m.name, strength=m.strength)
            )
        elif m.start_date > today:
            changes.append(
                BriefChange(kind="starts", date=m.start_date, name=m.name, strength=m.strength)
            )
        if stopped_on and since <= stopped_on <= today:
            changes.append(
                BriefChange(kind="stopped", date=stopped_on, name=m.name, strength=m.strength)
            )
        elif not stopped_on and m.end_date and since <= m.end_date < today:
            changes.append(
                BriefChange(kind="finished", date=m.end_date, name=m.name, strength=m.strength)
            )
    changes.sort(key=lambda c: c.date)

    window = min(MAX_WINDOW_DAYS, max(7, (today - since).days + 1))
    history = await doses.adherence(session, user, window)
    dose_rows = [
        BriefDoses(
            medication_id=h.medication_id,
            name=h.name,
            strength=h.strength,
            due=h.counts.due,
            taken=h.counts.taken,
            skipped=h.counts.skipped,
            unlogged=h.counts.unlogged,
        )
        for h in history.medications
        # A medicine nobody marked in this period was not tracked; "0 of 28 taken" would mislead.
        if h.counts.taken + h.counts.skipped > 0
    ]

    labs = []
    for t in await records.list_lab_trends(session, user.id):
        if t.latest.collected_on < since:
            continue
        prev = t.previous
        labs.append(
            BriefLab(
                key=t.key,
                name=t.name,
                value_text=t.latest.value_text,
                unit=t.latest.unit,
                ref_range=t.latest.ref_range,
                flag=t.latest.flag,
                collected_on=t.latest.collected_on,
                previous_value_text=prev.value_text if prev else None,
                previous_collected_on=prev.collected_on if prev else None,
            )
        )

    todos = [
        BriefTodo(id=a.id, title=a.title, due_on=a.due_on)
        for a in await records.list_care_actions(session, user.id, open_only=True)
    ][:10]

    events = await timeline.build_events(session, user)
    appointments = sorted(
        (
            BriefAppointment(date=e.date, title=e.title, subtitle=e.subtitle)
            for e in events
            if e.type == "appointment" and e.upcoming
        ),
        key=lambda a: a.date,
    )[:5]

    diet = await records.list_diet_notes(session, user.id)
    docs, _ = await documents.list_documents(session, user.id)
    new_docs = [
        BriefDocument(
            id=d.id, title=d.title, kind=d.kind, date=d.document_date or d.created_at.date()
        )
        for d in docs
        if (d.document_date or d.created_at.date()) >= since
    ][:10]

    return VisitBrief(
        visit=VisitOut.model_validate(prep),
        since=since,
        until=today,
        patient=user.display_name,
        medications=medications,
        changes=changes,
        doses=dose_rows,
        labs=labs,
        todos=todos,
        appointments=appointments,
        diet_notes=[n.text for n in diet.notes][:10],
        documents=new_docs,
        prompts=_prompts(prep, since, today, medications, dose_rows, labs, todos),
    )


def _prompts(
    prep: VisitPrep,
    since: date,
    today: date,
    medications: list[BriefMedication],
    dose_rows: list[BriefDoses],
    labs: list[BriefLab],
    todos: list[BriefTodo],
) -> list[Prompt]:
    """Observations worth raising, stated as facts from the records (no advice, no meaning)."""
    out: list[Prompt] = []
    for lab in labs:
        if lab.flag in ("high", "low"):
            where = "above" if lab.flag == "high" else "below"
            unit = f" {lab.unit}" if lab.unit else ""
            out.append(
                Prompt(
                    key=f"lab:{lab.key}:{lab.collected_on}",
                    text=(
                        f"{lab.name} was {where} the range printed on the {_day(lab.collected_on)} "
                        f"report: {lab.value_text}{unit} (range {lab.ref_range})."
                    ),
                )
            )
    for d in dose_rows:
        if d.skipped >= 2:
            out.append(
                Prompt(
                    key=f"skipped:{d.medication_id}:{since}",
                    text=(
                        f"You marked {d.skipped} {_label(d.name, d.strength)} doses as skipped "
                        f"since {_day(since)}."
                    ),
                )
            )
    horizon = (prep.visit_date or today) + timedelta(days=14)
    for m in medications:
        if m.end_date and today <= m.end_date <= horizon:
            out.append(
                Prompt(
                    key=f"ends:{m.id}:{m.end_date}",
                    text=f"{_label(m.name, m.strength)} is scheduled to end on {_day(m.end_date)}.",
                )
            )
    for t in todos:
        if t.due_on and t.due_on < today:
            out.append(
                Prompt(
                    key=f"todo:{t.id}",
                    text=f'"{t.title}" was due on {_day(t.due_on)} and is still open.',
                )
            )
    return out[:10]
