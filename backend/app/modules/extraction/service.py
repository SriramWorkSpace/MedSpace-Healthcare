"""Extraction pipeline: read the document, validate, normalize, store a reviewable draft."""

from __future__ import annotations

import asyncio
import base64
import logging
import uuid
from datetime import timedelta
from typing import Any

from fastapi import Request
from pydantic import ValidationError
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import utcnow
from app.core.errors import Conflict, NotFound
from app.modules.audit import service as audit
from app.modules.documents import files
from app.modules.documents import service as documents
from app.modules.documents.models import Document, DocumentStatus
from app.modules.extraction import evidence, heuristic, prompts
from app.modules.extraction.models import Extraction, ExtractionStatus
from app.modules.extraction.normalize import normalize_frequency, parse_duration_days
from app.modules.extraction.schemas import (
    ConfirmCareAction,
    ConfirmDietNote,
    ConfirmIn,
    ConfirmLabResult,
    ConfirmMedication,
    ExtractedCareAction,
    ExtractionPayload,
    ScheduleModel,
)
from app.modules.identity.models import User
from app.modules.records import service as records
from app.shared.llm import LLMError, LLMProvider, get_llm

logger = logging.getLogger("medspace.extraction")

VISION_BATCH = 3  # Groq vision accepts at most 3 images per request
SCAN_WARNING = (
    "This looks like a scan or photo. Offline mode can't read images, so the fields are blank "
    "for you to fill in. Set LLM_PROVIDER=groq to enable vision extraction."
)


class ExtractionFailed(Exception):
    """User-presentable failure reason."""


# --------------------------------------------------------------------------- LLM helpers


def _coerce(value: Any) -> Any:
    """Tidy common LLM quirks before validation: '' -> None, 0-100 confidences -> 0-1."""
    if isinstance(value, dict):
        out = {k: _coerce(v) for k, v in value.items()}
        for key in ("confidence", "overall_confidence"):
            if isinstance(out.get(key), int | float) and out[key] > 1:
                out[key] = min(1.0, out[key] / 100)
        return out
    if isinstance(value, list):
        return [_coerce(v) for v in value]
    if isinstance(value, str) and value.strip() in {"", "null", "None", "N/A", "n/a"}:
        return None
    return value


async def _validate_or_repair(
    llm: LLMProvider, raw: dict, messages: list[dict], model: str, schema: dict | None
) -> ExtractionPayload:
    try:
        return ExtractionPayload.model_validate(_coerce(raw))
    except ValidationError as exc:
        logger.info("extraction failed validation, attempting one repair")
        repair_messages = [
            *messages,
            {"role": "assistant", "content": str(raw)[:6000]},
            {"role": "user", "content": prompts.repair_prompt(str(exc)[:3000])},
        ]
        fixed = await llm.complete_json(model=model, messages=repair_messages, schema=schema)
        try:
            return ExtractionPayload.model_validate(_coerce(fixed))
        except ValidationError as exc2:
            raise ExtractionFailed(
                "The AI response couldn't be validated. Try reprocessing."
            ) from exc2


def _merge(parts: list[ExtractionPayload]) -> ExtractionPayload:
    if len(parts) == 1:
        return parts[0]
    base = parts[0].model_copy(deep=True)
    seen = {(m.name.lower(), (m.strength or "").lower()) for m in base.medications}
    for p in parts[1:]:
        base.prescriber = base.prescriber or p.prescriber
        base.issued_on = base.issued_on or p.issued_on
        base.follow_up = base.follow_up or p.follow_up
        base.patient_name = base.patient_name or p.patient_name
        for m in p.medications:
            key = (m.name.lower(), (m.strength or "").lower())
            if key not in seen:
                seen.add(key)
                base.medications.append(m)
        base.care_actions.extend(p.care_actions)
        base.diet_notes.extend(p.diet_notes)
        base.lab_results.extend(p.lab_results)
    confs = [p.overall_confidence for p in parts]
    base.overall_confidence = round(sum(confs) / len(confs), 2)
    return base


async def _extract_text(llm: LLMProvider, pages: list[str]) -> ExtractionPayload:
    model = get_settings().groq_text_model
    messages = [
        {"role": "system", "content": prompts.SYSTEM_PROMPT},
        {"role": "user", "content": prompts.text_user_prompt(pages)},
    ]
    raw = await llm.complete_json(
        model=model, messages=messages, schema=prompts.EXTRACTION_SCHEMA, schema_name="prescription"
    )
    return await _validate_or_repair(llm, raw, messages, model, prompts.EXTRACTION_SCHEMA)


async def _extract_vision(llm: LLMProvider, data: bytes, mime: str) -> ExtractionPayload:
    settings = get_settings()
    model = settings.groq_vision_model
    pngs = await asyncio.to_thread(files.render_pages_png, data, mime, max_pages=settings.max_pages)
    parts: list[ExtractionPayload] = []
    for start in range(0, len(pngs), VISION_BATCH):
        batch = pngs[start : start + VISION_BATCH]
        content: list[dict[str, Any]] = [
            {"type": "text", "text": prompts.vision_user_prompt(start + 1, len(batch))}
        ]
        content += [
            {
                "type": "image_url",
                "image_url": {"url": "data:image/png;base64," + base64.b64encode(png).decode()},
            }
            for png in batch
        ]
        messages = [
            {"role": "system", "content": prompts.SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ]
        raw = await llm.complete_json(model=model, messages=messages)
        parts.append(await _validate_or_repair(llm, raw, messages, model, None))
    return _merge(parts)


# --------------------------------------------------------------------------- normalization


def post_process(
    payload: ExtractionPayload, *, dose_times: dict[str, str], page_count: int
) -> ExtractionPayload:
    """Deterministic clean-up applied to every extraction regardless of where it came from."""
    p = payload.model_copy(deep=True)
    start = p.issued_on
    for med in p.medications:
        sched = normalize_frequency(med.frequency_raw, dose_times)
        if med.as_needed and not sched.as_needed:
            sched.as_needed, sched.times, sched.period, sched.label = (
                True,
                [],
                "as_needed",
                "As needed",
            )
        med.as_needed = sched.as_needed
        med.schedule = ScheduleModel(**sched.to_dict())
        med.duration_days = med.duration_days or parse_duration_days(med.duration_raw)
        med.source_page = min(max(1, med.source_page), page_count)
        if sched.needs_attention and "frequency_raw" not in med.uncertain_fields:
            med.uncertain_fields.append("frequency_raw")
            med.confidence = min(med.confidence, 0.6)

        if med.duration_days and med.duration_days <= 30 and not med.as_needed:
            title = f"Finish the {med.name} course"
            if not any(a.title.lower() == title.lower() for a in p.care_actions):
                due = start + timedelta(days=med.duration_days - 1) if start else None
                p.care_actions.append(
                    ExtractedCareAction(
                        kind="course_completion",
                        title=title,
                        due_on=due,
                        source_page=med.source_page,
                        confidence=med.confidence,
                    )
                )

    seen_notes: set[str] = set()
    notes = []
    for note in p.diet_notes:
        key = note.text.strip().lower()
        if key and key not in seen_notes:
            seen_notes.add(key)
            note.source_page = min(max(1, note.source_page), page_count)
            notes.append(note)
    p.diet_notes = notes

    seen_results: set[tuple[str, int]] = set()
    results = []
    for r in p.lab_results:
        r.name = r.name.strip().rstrip(":").strip()
        r.source_page = min(max(1, r.source_page), page_count)
        key = (r.name.lower(), r.source_page)
        if r.name and key not in seen_results:
            seen_results.add(key)
            results.append(r)
    p.lab_results = results

    deduped: dict[tuple[str, str], ExtractedCareAction] = {}
    for action in p.care_actions:
        action.source_page = min(max(1, action.source_page), page_count)
        deduped.setdefault((action.kind, action.title.strip().lower()), action)
    p.care_actions = list(deduped.values())
    return p


async def extract_document(
    doc: Document, pages: list[str], dose_times: dict[str, str], *, offline: bool = False
):
    """Returns (payload, method, model). Raises ExtractionFailed with a user-facing reason.

    `offline=True` forces the heuristic path (demo seeding never spends LLM calls).
    """
    llm = None if offline else get_llm()
    settings = get_settings()
    has_text = doc.has_text_layer or any(len(t) >= files.TEXT_LAYER_MIN_CHARS for t in pages)

    if llm is None:
        if has_text:
            payload, method, model = heuristic.extract(pages), "heuristic", None
        else:
            payload = ExtractionPayload(
                document_type="other", overall_confidence=0, warnings=[SCAN_WARNING]
            )
            method, model = "none", None
    else:
        try:
            if doc.has_text_layer:
                payload = await _extract_text(llm, pages)
                method, model = "groq-text", settings.groq_text_model
            else:
                data = await documents.read_original(doc)
                payload = await _extract_vision(llm, data, doc.mime_type)
                method, model = "groq-vision", settings.groq_vision_model
        except LLMError as exc:
            logger.warning("LLM extraction failed: %s", exc)
            raise ExtractionFailed(
                "The AI service didn't respond. Your file is safe; try reprocessing in a minute."
            ) from exc

    payload = post_process(payload, dose_times=dose_times, page_count=doc.page_count)
    return payload, method, model


async def extract_text_pages(
    pages: list[str], dose_times: dict[str, str], *, offline: bool = True
) -> tuple[ExtractionPayload, str]:
    """Text pages in, normalized payload out: the text path without a stored document.

    Used by the evaluation harness so it measures exactly what uploads go through.
    Returns (payload, method).
    """
    llm = None if offline else get_llm()
    if llm is None:
        payload, method = heuristic.extract(pages), "heuristic"
    else:
        payload, method = await _extract_text(llm, pages), "groq-text"
    return post_process(payload, dose_times=dose_times, page_count=max(1, len(pages))), method


# --------------------------------------------------------------------------- persistence


async def save_draft(
    session: AsyncSession, doc: Document, payload: ExtractionPayload, method: str, model: str | None
) -> Extraction:
    current = await session.scalar(
        select(func.max(Extraction.version)).where(Extraction.document_id == doc.id)
    )
    await session.execute(
        update(Extraction)
        .where(Extraction.document_id == doc.id, Extraction.status == ExtractionStatus.DRAFT)
        .values(status=ExtractionStatus.SUPERSEDED)
    )
    extraction = Extraction(
        document_id=doc.id,
        user_id=doc.user_id,
        version=(current or 0) + 1,
        status=ExtractionStatus.DRAFT,
        method=method,
        model=model,
        payload=payload.model_dump(mode="json"),
        overall_confidence=payload.overall_confidence,
    )
    session.add(extraction)
    if payload.issued_on:
        doc.document_date = payload.issued_on
    await session.flush()
    return extraction


async def latest_for_document(
    session: AsyncSession, user_id: uuid.UUID, doc_id: uuid.UUID
) -> Extraction:
    extraction = await session.scalar(
        select(Extraction)
        .where(
            Extraction.document_id == doc_id,
            Extraction.user_id == user_id,
            Extraction.status.in_([ExtractionStatus.DRAFT, ExtractionStatus.CONFIRMED]),
        )
        .order_by(Extraction.version.desc())
        .limit(1)
    )
    if extraction is None:
        raise NotFound("No extraction yet for this document.")
    return extraction


async def evidence_for_document(
    session: AsyncSession, user_id: uuid.UUID, doc_id: uuid.UUID, *, confirmed: bool = False
) -> tuple[Extraction, dict]:
    """Field locations for the latest extraction, computed once per extraction (ADR-031).

    `confirmed`: use the reading the records came from, even if the document was read again
    since (records' `source_ref` points into that one).
    """
    if confirmed:
        extraction = await session.scalar(
            select(Extraction)
            .where(
                Extraction.document_id == doc_id,
                Extraction.user_id == user_id,
                Extraction.status == ExtractionStatus.CONFIRMED,
            )
            .order_by(Extraction.version.desc())
            .limit(1)
        )
        if extraction is None:
            raise NotFound("No confirmed reading for this document.")
    else:
        extraction = await latest_for_document(session, user_id, doc_id)
    cached = extraction.evidence
    if cached and cached.get("version") == evidence.VERSION:
        return extraction, cached
    doc = await documents.get_document(session, user_id, doc_id)
    data = await documents.read_original(doc)
    payload = ExtractionPayload.model_validate(extraction.payload)
    found = await asyncio.to_thread(evidence.locate, data, doc.mime_type, payload)
    extraction.evidence = found
    await session.flush()
    return extraction, found


async def get_extraction(
    session: AsyncSession, user_id: uuid.UUID, extraction_id: uuid.UUID
) -> Extraction:
    extraction = await session.scalar(
        select(Extraction).where(Extraction.id == extraction_id, Extraction.user_id == user_id)
    )
    if extraction is None:
        raise NotFound("Extraction not found.")
    return extraction


async def confirm(
    session: AsyncSession,
    user: User,
    extraction_id: uuid.UUID,
    data: ConfirmIn,
    request: Request | None = None,
) -> Extraction:
    extraction = await get_extraction(session, user.id, extraction_id)
    if extraction.status != ExtractionStatus.DRAFT:
        raise Conflict("This version has already been reviewed.")
    doc = await documents.get_document(session, user.id, extraction.document_id)

    prescription = await records.replace_for_document(
        session, user_id=user.id, document=doc, extraction_id=extraction.id, data=data
    )
    extraction.status = ExtractionStatus.CONFIRMED
    extraction.confirmed_at = utcnow()
    extraction.prescription_id = prescription.id if prescription else None
    await session.execute(
        update(Extraction)
        .where(
            Extraction.document_id == doc.id,
            Extraction.id != extraction.id,
            Extraction.status == ExtractionStatus.CONFIRMED,
        )
        .values(status=ExtractionStatus.SUPERSEDED)
    )
    doc.kind = data.document_kind
    doc.document_date = data.issued_on or doc.document_date
    documents.set_status(doc, DocumentStatus.CONFIRMED)
    await audit.record(
        session,
        action="extraction.confirmed",
        user_id=user.id,
        request=request,
        entity_type="document",
        entity_id=doc.id,
        meta={
            "version": extraction.version,
            "medications": len(data.medications),
            "care_actions": len(data.care_actions),
            "lab_results": len(data.lab_results),
        },
    )
    await session.flush()
    return extraction


async def discard(
    session: AsyncSession, user: User, extraction_id: uuid.UUID, request: Request | None = None
) -> Extraction:
    extraction = await get_extraction(session, user.id, extraction_id)
    if extraction.status != ExtractionStatus.DRAFT:
        raise Conflict("Only drafts can be discarded.")
    extraction.status = ExtractionStatus.DISCARDED
    doc = await documents.get_document(session, user.id, extraction.document_id)
    has_confirmed = await session.scalar(
        select(Extraction.id).where(
            Extraction.document_id == doc.id, Extraction.status == ExtractionStatus.CONFIRMED
        )
    )
    if has_confirmed:
        documents.set_status(doc, DocumentStatus.CONFIRMED)
    else:
        documents.set_status(
            doc, DocumentStatus.FAILED, "You discarded the draft. Reprocess to read it again."
        )
    await audit.record(
        session,
        action="extraction.discarded",
        user_id=user.id,
        request=request,
        entity_type="document",
        entity_id=extraction.document_id,
    )
    await session.flush()
    return extraction


def payload_to_confirm(payload: ExtractionPayload) -> ConfirmIn:
    """Accept a draft exactly as extracted (used by demo seeding and tests)."""
    return ConfirmIn(
        document_kind=payload.document_type,
        prescriber=payload.prescriber,
        issued_on=payload.issued_on,
        follow_up=payload.follow_up,
        summary=payload.summary,
        medications=[
            ConfirmMedication(
                name=m.name,
                strength=m.strength,
                form=m.form,
                dose=m.dose,
                route=m.route,
                frequency_raw=m.frequency_raw,
                schedule=m.schedule or ScheduleModel(period="unknown"),
                duration_days=m.duration_days,
                instructions=m.instructions,
                source_page=m.source_page,
                source_ref=f"medications.{i}",
            )
            for i, m in enumerate(payload.medications)
        ],
        care_actions=[
            ConfirmCareAction(
                kind=a.kind,
                title=a.title,
                due_on=a.due_on,
                notes=a.notes,
                source_page=a.source_page,
                source_ref=f"care_actions.{i}",
            )
            for i, a in enumerate(payload.care_actions)
        ],
        diet_notes=[
            ConfirmDietNote(
                text=n.text,
                category=n.category,
                source_page=n.source_page,
                source_ref=f"diet_notes.{i}",
            )
            for i, n in enumerate(payload.diet_notes)
        ],
        lab_results=[
            ConfirmLabResult(
                name=r.name,
                value=r.value,
                unit=r.unit,
                ref_range=r.ref_range,
                flag=r.flag,
                source_page=r.source_page,
                source_ref=f"lab_results.{i}",
            )
            for i, r in enumerate(payload.lab_results)
        ],
    )
