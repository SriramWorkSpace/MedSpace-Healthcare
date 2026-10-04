"""Records: confirmed prescriptions, medications and care actions."""

from __future__ import annotations

import re
import uuid
from datetime import date, timedelta

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import utcnow
from app.core.errors import NotFound
from app.modules.documents.models import Document
from app.modules.extraction.schemas import ConfirmIn
from app.modules.records.models import CareAction, DietNote, LabResult, Medication, Prescription
from app.modules.records.schemas import (
    CareActionOut,
    CareActionUpdate,
    DietNoteOut,
    DietNotesOut,
    LabPoint,
    LabResultOut,
    LabTrendDetail,
    LabTrendOut,
    MedicationFoodNote,
    MedicationOut,
    MedicationUpdate,
    PrescriptionOut,
    PrescriptionSummary,
)


def medication_status(med: Medication, today: date | None = None) -> str:
    today = today or date.today()
    if med.stopped_at is not None:
        return "stopped"
    if med.start_date > today:
        return "upcoming"
    if med.end_date is not None and med.end_date < today:
        return "completed"
    return "active"


def to_medication_out(
    med: Medication,
    *,
    today: date | None = None,
    document_id: uuid.UUID | None = None,
    prescriber_name: str | None = None,
) -> MedicationOut:
    today = today or date.today()
    out = MedicationOut.model_validate(med)
    out.status = medication_status(med, today)
    if out.status == "active" and med.duration_days:
        out.day_of_course = (today - med.start_date).days + 1
    out.document_id = document_id
    out.prescriber_name = prescriber_name
    return out


async def replace_for_document(
    session: AsyncSession,
    *,
    user_id: uuid.UUID,
    document: Document,
    extraction_id: uuid.UUID,
    data: ConfirmIn,
) -> Prescription | None:
    """Create records from a confirmed review, replacing earlier confirmations of the document.

    Documents that are not prescriptions and carry no medications or to-dos (a lab report, a
    letter) are confirmed without creating a prescription record.
    """
    await session.execute(
        delete(Prescription).where(
            Prescription.document_id == document.id, Prescription.user_id == user_id
        )
    )
    await session.execute(
        delete(DietNote).where(DietNote.document_id == document.id, DietNote.user_id == user_id)
    )
    await session.execute(
        delete(LabResult).where(LabResult.document_id == document.id, LabResult.user_id == user_id)
    )
    collected_on = data.issued_on or document.document_date or document.created_at.date()
    for position, r in enumerate(data.lab_results):
        session.add(
            LabResult(
                user_id=user_id,
                document_id=document.id,
                name=r.name.strip(),
                value_text=r.value.strip(),
                unit=(r.unit or "").strip() or None,
                ref_range=(r.ref_range or "").strip() or None,
                collected_on=collected_on,
                position=position,
                source_page=r.source_page,
                source_ref=r.source_ref,
                **r.normalized(),
            )
        )

    def add_diet_notes(prescription_id: uuid.UUID | None) -> None:
        for n in data.diet_notes:
            session.add(
                DietNote(
                    user_id=user_id,
                    document_id=document.id,
                    prescription_id=prescription_id,
                    text=n.text.strip(),
                    category=n.category,
                    source_page=n.source_page,
                    source_ref=n.source_ref,
                )
            )

    if data.document_kind != "prescription" and not data.medications and not data.care_actions:
        add_diet_notes(None)
        await session.flush()
        return None
    p = data.prescriber
    fu = data.follow_up
    prescription = Prescription(
        user_id=user_id,
        document_id=document.id,
        extraction_id=extraction_id,
        prescriber_name=p.name if p else None,
        prescriber_specialty=p.specialty if p else None,
        clinic_name=p.clinic if p else None,
        prescriber_contact=p.contact if p else None,
        issued_on=data.issued_on,
        follow_up_on=fu.date if fu else None,
        follow_up_notes=fu.notes if fu else None,
        summary=data.summary,
        medications=[],
        care_actions=[],
    )
    default_start = data.issued_on or date.today()
    for m in data.medications:
        start = m.start_date or default_start
        schedule = m.schedule.model_copy()
        if schedule.as_needed:
            schedule.times = []
        prescription.medications.append(
            Medication(
                user_id=user_id,
                name=m.name.strip(),
                strength=m.strength,
                form=m.form,
                dose=m.dose,
                route=m.route,
                frequency_raw=m.frequency_raw,
                schedule=schedule.model_dump(),
                as_needed=schedule.as_needed,
                start_date=start,
                end_date=start + timedelta(days=m.duration_days - 1) if m.duration_days else None,
                duration_days=m.duration_days,
                instructions=m.instructions,
                source_page=m.source_page,
                source_ref=m.source_ref,
            )
        )
    for a in data.care_actions:
        prescription.care_actions.append(
            CareAction(
                user_id=user_id,
                kind=a.kind,
                title=a.title.strip(),
                notes=a.notes,
                due_on=a.due_on,
                source_page=a.source_page,
                source_ref=a.source_ref,
            )
        )
    session.add(prescription)
    await session.flush()
    add_diet_notes(prescription.id)
    await session.flush()
    return prescription


def _summary(p: Prescription, title: str | None) -> PrescriptionSummary:
    today = date.today()
    out = PrescriptionSummary.model_validate(p)
    out.document_title = title
    out.medication_count = len(p.medications)
    out.active_count = sum(medication_status(m, today) == "active" for m in p.medications)
    return out


async def list_prescriptions(
    session: AsyncSession, user_id: uuid.UUID
) -> list[PrescriptionSummary]:
    rows = await session.execute(
        select(Prescription, Document.title)
        .join(Document, Document.id == Prescription.document_id)
        .where(Prescription.user_id == user_id)
        .order_by(Prescription.issued_on.desc().nulls_last(), Prescription.created_at.desc())
    )
    return [_summary(p, title) for p, title in rows.all()]


async def get_prescription(
    session: AsyncSession, user_id: uuid.UUID, prescription_id: uuid.UUID
) -> PrescriptionOut:
    row = (
        await session.execute(
            select(Prescription, Document.title)
            .join(Document, Document.id == Prescription.document_id)
            .where(Prescription.id == prescription_id, Prescription.user_id == user_id)
        )
    ).first()
    if row is None:
        raise NotFound("Prescription not found.")
    p, title = row
    base = _summary(p, title).model_dump()
    return PrescriptionOut(
        **base,
        prescriber_contact=p.prescriber_contact,
        follow_up_notes=p.follow_up_notes,
        summary=p.summary,
        medications=[
            to_medication_out(m, document_id=p.document_id, prescriber_name=p.prescriber_name)
            for m in p.medications
        ],
        care_actions=[CareActionOut.model_validate(a) for a in p.care_actions],
        diet_notes=[
            _diet_out(n, title, p.prescriber_name, p.issued_on)
            for n in await _notes_for_document(session, user_id, p.document_id)
        ],
    )


async def get_prescription_for_document(
    session: AsyncSession, user_id: uuid.UUID, document_id: uuid.UUID
) -> uuid.UUID | None:
    return await session.scalar(
        select(Prescription.id).where(
            Prescription.document_id == document_id, Prescription.user_id == user_id
        )
    )


async def list_medications(
    session: AsyncSession, user_id: uuid.UUID, *, status: str | None = None
) -> list[MedicationOut]:
    rows = await session.execute(
        select(Medication, Prescription.document_id, Prescription.prescriber_name)
        .join(Prescription, Prescription.id == Medication.prescription_id)
        .where(Medication.user_id == user_id)
        .order_by(Medication.start_date.desc(), Medication.name)
    )
    out = []
    for med, document_id, prescriber in rows.all():
        item = to_medication_out(med, document_id=document_id, prescriber_name=prescriber)
        if status is None or item.status == status:
            out.append(item)
    return out


async def get_medication(
    session: AsyncSession, user_id: uuid.UUID, med_id: uuid.UUID
) -> Medication:
    med = await session.scalar(
        select(Medication).where(Medication.id == med_id, Medication.user_id == user_id)
    )
    if med is None:
        raise NotFound("Medication not found.")
    return med


async def update_medication(
    session: AsyncSession, user_id: uuid.UUID, med_id: uuid.UUID, data: MedicationUpdate
) -> Medication:
    med = await get_medication(session, user_id, med_id)
    if data.schedule is not None:
        med.schedule = data.schedule.model_dump()
        med.as_needed = data.schedule.as_needed
    if data.instructions is not None:
        med.instructions = data.instructions
    if data.end_date is not None:
        med.end_date = data.end_date
    if data.stopped is not None:
        med.stopped_at = utcnow() if data.stopped else None
    await session.flush()
    return med


async def list_care_actions(
    session: AsyncSession, user_id: uuid.UUID, *, open_only: bool = False
) -> list[CareAction]:
    stmt = select(CareAction).where(CareAction.user_id == user_id)
    if open_only:
        stmt = stmt.where(CareAction.completed_at.is_(None))
    stmt = stmt.order_by(CareAction.completed_at.is_not(None), CareAction.due_on.asc().nulls_last())
    return list((await session.scalars(stmt)).all())


async def update_care_action(
    session: AsyncSession, user_id: uuid.UUID, action_id: uuid.UUID, data: CareActionUpdate
) -> CareAction:
    action = await session.scalar(
        select(CareAction).where(CareAction.id == action_id, CareAction.user_id == user_id)
    )
    if action is None:
        raise NotFound("Task not found.")
    if data.completed is not None:
        action.completed_at = utcnow() if data.completed else None
    if data.due_on is not None:
        action.due_on = data.due_on
    if data.title is not None:
        action.title = data.title.strip()
    await session.flush()
    return action


# ---- Diet notes -----------------------------------------------------------------------------

_FOOD = re.compile(
    r"(after (?:food|meals?|breakfast|lunch|dinner)|before (?:food|meals?|breakfast|bed)|"
    r"with (?:food|meals?|milk|water)|on an empty stomach|empty stomach|avoid [a-z ]+|"
    r"no alcohol|without food)",
    re.IGNORECASE,
)


def _diet_out(n: DietNote, title, prescriber, issued_on) -> DietNoteOut:
    out = DietNoteOut.model_validate(n)
    out.document_title, out.prescriber_name, out.issued_on = title, prescriber, issued_on
    return out


async def _notes_for_document(session: AsyncSession, user_id: uuid.UUID, document_id: uuid.UUID):
    return (
        await session.scalars(
            select(DietNote)
            .where(DietNote.user_id == user_id, DietNote.document_id == document_id)
            .order_by(DietNote.created_at)
        )
    ).all()


def medication_food_notes(meds_with_doc: list[tuple[Medication, uuid.UUID | None]]):
    """Food/drink instructions attached to current medicines, e.g. "after food", "with milk"."""
    out = []
    for med, document_id in meds_with_doc:
        if medication_status(med) not in ("active", "upcoming") or not med.instructions:
            continue
        for match in _FOOD.finditer(med.instructions):
            phrase = match.group(0)
            out.append(
                MedicationFoodNote(
                    medication_id=med.id,
                    name=med.name,
                    strength=med.strength,
                    text=phrase[:1].upper() + phrase[1:],
                    category="avoid" if phrase.lower().startswith(("avoid", "no ")) else "timing",
                    document_id=document_id,
                    source_page=med.source_page,
                    source_ref=med.source_ref,
                )
            )
    return out


async def list_diet_notes(session: AsyncSession, user_id: uuid.UUID) -> DietNotesOut:
    rows = await session.execute(
        select(DietNote, Document.title, Prescription.prescriber_name, Prescription.issued_on)
        .join(Document, Document.id == DietNote.document_id)
        .outerjoin(Prescription, Prescription.id == DietNote.prescription_id)
        .where(DietNote.user_id == user_id)
        .order_by(Prescription.issued_on.desc().nulls_last(), DietNote.created_at)
    )
    notes = [_diet_out(n, title, who, issued) for n, title, who, issued in rows.all()]
    med_rows = await session.execute(
        select(Medication, Prescription.document_id)
        .join(Prescription, Prescription.id == Medication.prescription_id)
        .where(Medication.user_id == user_id)
        .order_by(Medication.name)
    )
    return DietNotesOut(notes=notes, medication_notes=medication_food_notes(list(med_rows.all())))


async def delete_diet_note(session: AsyncSession, user_id: uuid.UUID, note_id: uuid.UUID) -> None:
    note = await session.scalar(
        select(DietNote).where(DietNote.id == note_id, DietNote.user_id == user_id)
    )
    if note is None:
        raise NotFound("Diet note not found.")
    await session.delete(note)
    await session.flush()


# ---- Lab results (ADR-020) ----------------------------------------------------------------------


def _lab_out(r: LabResult, title: str | None) -> LabResultOut:
    out = LabResultOut.model_validate(r)
    out.document_title = title
    return out


def _trend(results: list[LabResultOut]) -> LabTrendOut:
    """results: one test, newest first."""
    latest = results[0]
    unit = (latest.unit or "").lower()
    charted = [r for r in results if r.value is not None and (r.unit or "").lower() == unit]
    return LabTrendOut(
        key=latest.analyte_key,
        name=latest.name,
        unit=latest.unit,
        count=len(results),
        latest=latest,
        previous=results[1] if len(results) > 1 else None,
        points=[
            LabPoint(value=r.value, collected_on=r.collected_on, flag=r.flag)
            for r in reversed(charted)
        ],
        uncharted=len(results) - len(charted),
    )


async def _lab_results(
    session: AsyncSession, user_id: uuid.UUID, key: str | None = None
) -> dict[str, list[LabResultOut]]:
    query = (
        select(LabResult, Document.title)
        .join(Document, Document.id == LabResult.document_id)
        .where(LabResult.user_id == user_id)
        .order_by(LabResult.collected_on.desc(), Document.created_at.desc(), LabResult.position)
    )
    if key is not None:
        query = query.where(LabResult.analyte_key == key)
    grouped: dict[str, list[LabResultOut]] = {}
    for r, title in (await session.execute(query)).all():
        grouped.setdefault(r.analyte_key, []).append(_lab_out(r, title))
    return grouped


async def list_lab_results(session: AsyncSession, user_id: uuid.UUID) -> list[LabResultOut]:
    return [r for group in (await _lab_results(session, user_id)).values() for r in group]


async def list_lab_trends(session: AsyncSession, user_id: uuid.UUID) -> list[LabTrendOut]:
    """One entry per test; tests from the most recent report first, in report order."""
    # Grouping keeps insertion order, which already follows each test's newest result.
    return [_trend(results) for results in (await _lab_results(session, user_id)).values()]


async def get_lab_trend(session: AsyncSession, user_id: uuid.UUID, key: str) -> LabTrendDetail:
    results = (await _lab_results(session, user_id, key)).get(key)
    if not results:
        raise NotFound("No results for this test.")
    return LabTrendDetail(**_trend(results).model_dump(), results=results)


async def delete_lab_result(
    session: AsyncSession, user_id: uuid.UUID, result_id: uuid.UUID
) -> None:
    result = await session.scalar(
        select(LabResult).where(LabResult.id == result_id, LabResult.user_id == user_id)
    )
    if result is None:
        raise NotFound("Lab result not found.")
    await session.delete(result)
    await session.flush()


def times_on(m: Medication, day: date) -> list[str]:
    """Scheduled HH:MM times for one medicine on one day, by its schedule and course dates.

    Ignores stopped_at on purpose: callers decide whether a stopped medicine still counts
    (today's schedule: no; history before the stop: yes).
    """
    if m.as_needed or m.start_date > day or (m.end_date and m.end_date < day):
        return []
    period = (m.schedule or {}).get("period", "daily")
    if period == "weekly" and (day - m.start_date).days % 7:
        return []
    if period == "alternate_days" and (day - m.start_date).days % 2:
        return []
    if period == "once" and day != m.start_date:
        return []
    return sorted((m.schedule or {}).get("times", []))


def doses_on(meds: list[Medication], day: date) -> list[dict]:
    """Scheduled doses for a calendar day (as-needed and stopped meds excluded), sorted by time."""
    out = [
        {"time": t, "medication": m} for m in meds if m.stopped_at is None for t in times_on(m, day)
    ]
    return sorted(out, key=lambda d: d["time"])
