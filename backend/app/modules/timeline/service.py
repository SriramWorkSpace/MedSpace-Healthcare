"""Read models over confirmed records: the health timeline and the dashboard.

The timeline is computed at query time from source tables (no projection table to keep in sync).
Per-user data volume is small, so assembling and sorting in Python is simpler than a SQL union.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.documents.models import Document, DocumentKind, DocumentStatus
from app.modules.doses import service as doses_service
from app.modules.identity.models import User
from app.modules.records import service as records
from app.modules.records.models import CareAction, Medication, Prescription
from app.modules.supply import service as supply_service
from app.modules.timeline.schemas import (
    AsNeededOut,
    DashboardOut,
    DayLoad,
    DoseOut,
    ReviewItem,
    TimelineEvent,
    TimelinePage,
)


def user_today(user: User) -> date:
    try:
        return datetime.now(ZoneInfo(user.timezone)).date()
    except Exception:
        return date.today()


def _med_label(m: Medication) -> str:
    return f"{m.name} {m.strength}".strip() if m.strength else m.name


async def build_events(session: AsyncSession, user: User) -> list[TimelineEvent]:
    today = user_today(user)
    uid = user.id
    events: list[TimelineEvent] = []

    rows = await session.execute(
        select(Prescription, Document.title)
        .join(Document, Document.id == Prescription.document_id)
        .where(Prescription.user_id == uid)
    )
    for p, title in rows.all():
        when = p.issued_on or p.created_at.date()
        meds = ", ".join(m.name for m in p.medications[:4])
        who = p.prescriber_name or p.clinic_name or title
        events.append(
            TimelineEvent(
                id=f"rx-{p.id}",
                type="prescription",
                date=when,
                title=f"Prescription from {who}",
                subtitle=meds or p.summary,
                upcoming=when > today,
                document_id=p.document_id,
                prescription_id=p.id,
            )
        )
        if p.follow_up_on:
            events.append(
                TimelineEvent(
                    id=f"fu-{p.id}",
                    type="appointment",
                    date=p.follow_up_on,
                    title=f"Follow-up{f' with {p.prescriber_name}' if p.prescriber_name else ''}",
                    subtitle=p.clinic_name or p.follow_up_notes,
                    upcoming=p.follow_up_on >= today,
                    prescription_id=p.id,
                    document_id=p.document_id,
                )
            )
        for m in p.medications:
            events.append(
                TimelineEvent(
                    id=f"ms-{m.id}",
                    type="medication_start",
                    date=m.start_date,
                    title=f"Started {_med_label(m)}",
                    subtitle=(m.schedule or {}).get("label"),
                    upcoming=m.start_date > today,
                    prescription_id=p.id,
                    medication_id=m.id,
                )
            )
            end = m.stopped_at.date() if m.stopped_at else m.end_date
            if end:
                stopped = m.stopped_at is not None
                events.append(
                    TimelineEvent(
                        id=f"me-{m.id}",
                        type="medication_end",
                        date=end,
                        title=(
                            f"Stopped {_med_label(m)}"
                            if stopped
                            else f"{'Course ends' if end >= today else 'Finished'}: {_med_label(m)}"
                        ),
                        subtitle=f"{m.duration_days}-day course" if m.duration_days else None,
                        upcoming=end >= today and not stopped,
                        prescription_id=p.id,
                        medication_id=m.id,
                    )
                )

    actions = await session.scalars(
        select(CareAction).where(
            CareAction.user_id == uid,
            # Follow-ups are already appointments; course completions are medication_end events.
            CareAction.kind.not_in(["follow_up", "course_completion"]),
        )
    )
    for a in actions.all():
        when = a.completed_at.date() if a.completed_at else a.due_on
        if when is None:
            continue
        events.append(
            TimelineEvent(
                id=f"task-{a.id}",
                type="task",
                date=when,
                title=a.title,
                subtitle="Done" if a.completed_at else "To-do",
                upcoming=a.completed_at is None and when >= today,
                completed=a.completed_at is not None,
                prescription_id=a.prescription_id,
                care_action_id=a.id,
            )
        )

    docs = await session.scalars(
        select(Document).where(
            Document.user_id == uid,
            Document.kind != DocumentKind.PRESCRIPTION,
            Document.status == DocumentStatus.CONFIRMED,
        )
    )
    for d in docs.all():
        events.append(
            TimelineEvent(
                id=f"doc-{d.id}",
                type="document",
                date=d.document_date or d.created_at.date(),
                title=d.title,
                subtitle="Lab report" if d.kind == DocumentKind.LAB_REPORT else "Document",
                document_id=d.id,
            )
        )

    order = {"appointment": 0, "prescription": 1, "medication_start": 2, "task": 3}
    events.sort(key=lambda e: (e.date, -order.get(e.type, 5)), reverse=True)
    return events


async def timeline_page(
    session: AsyncSession,
    user: User,
    *,
    before: date | None = None,
    types: set[str] | None = None,
    limit: int = 40,
) -> TimelinePage:
    events = await build_events(session, user)
    if types:
        events = [e for e in events if e.type in types]
    if before:
        events = [e for e in events if e.date < before]
    page = events[:limit]
    more = len(events) > limit
    # Cursor is a date; include all events of the boundary day in this page to avoid splitting it.
    if more:
        boundary = page[-1].date
        page = [e for e in events if e.date >= boundary]
    next_cursor = page[-1].date.isoformat() if more and page else None
    return TimelinePage(items=page, next_cursor=next_cursor)


async def dashboard(session: AsyncSession, user: User) -> DashboardOut:
    today = user_today(user)
    uid = user.id
    rows = await session.execute(
        select(Medication).where(Medication.user_id == uid, Medication.stopped_at.is_(None))
    )
    meds = list(rows.scalars().all())

    logged = await doses_service.statuses_on(session, uid, today)
    doses = [
        DoseOut(
            time=d["time"],
            medication_id=d["medication"].id,
            name=d["medication"].name,
            strength=d["medication"].strength,
            instructions=d["medication"].instructions,
            prescription_id=d["medication"].prescription_id,
            status=logged.get((d["medication"].id, d["time"])),
        )
        for d in records.doses_on(meds, today)
    ]
    as_needed = [
        AsNeededOut(
            medication_id=m.id, name=m.name, strength=m.strength, instructions=m.instructions
        )
        for m in meds
        if m.as_needed and records.medication_status(m, today) == "active"
    ]
    week = [
        DayLoad(
            date=today + timedelta(days=i),
            doses=len(records.doses_on(meds, today + timedelta(days=i))),
        )
        for i in range(7)
    ]

    events = await build_events(session, user)
    horizon = today + timedelta(days=45)
    upcoming = sorted(
        (
            e
            for e in events
            if e.upcoming
            and e.date <= horizon
            and e.type in {"appointment", "task", "medication_end"}
        ),
        key=lambda e: e.date,
    )[:6]

    review_docs = (
        await session.scalars(
            select(Document)
            .where(Document.user_id == uid, Document.status == DocumentStatus.NEEDS_REVIEW)
            .order_by(Document.created_at.desc())
            .limit(5)
        )
    ).all()
    processing = await session.scalar(
        select(func.count())
        .select_from(Document)
        .where(
            Document.user_id == uid,
            Document.status.in_([DocumentStatus.QUEUED, DocumentStatus.PROCESSING]),
        )
    )
    doc_count = await session.scalar(
        select(func.count()).select_from(Document).where(Document.user_id == uid)
    )
    open_tasks = await session.scalar(
        select(func.count())
        .select_from(CareAction)
        .where(CareAction.user_id == uid, CareAction.completed_at.is_(None))
    )
    rx_count = await session.scalar(
        select(func.count()).select_from(Prescription).where(Prescription.user_id == uid)
    )

    low = await supply_service.running_low(session, user)

    return DashboardOut(
        today=today,
        running_low=low,
        doses_today=doses,
        as_needed=as_needed,
        upcoming=upcoming,
        needs_review=[ReviewItem(id=d.id, title=d.title, status=d.status) for d in review_docs],
        processing=processing or 0,
        week=week,
        stats={
            "active_medications": sum(
                records.medication_status(m, today) == "active" for m in meds
            ),
            "documents": doc_count or 0,
            "open_tasks": open_tasks or 0,
            "prescriptions": rx_count or 0,
        },
    )


def parse_types(raw: str | None) -> set[str] | None:
    if not raw:
        return None
    return {t.strip() for t in raw.split(",") if t.strip()}
