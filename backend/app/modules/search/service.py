"""Global search: one query across medications, prescriptions, documents, to-dos and diet notes.

A read model like the timeline (no tables of its own). Names use case-insensitive substring
matching; document contents use Postgres full-text search with prefix matching, so "amox"
finds "Amoxicillin" as the user types. Every query is scoped by user_id.
"""

from __future__ import annotations

import re
import uuid

from pydantic import BaseModel
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.assistant.models import DocumentChunk
from app.modules.documents.models import Document
from app.modules.records.models import CareAction, DietNote, Medication, Prescription
from app.modules.records.service import medication_status

PER_GROUP = 5
_WORD = re.compile(r"[a-z0-9]+")


class SearchHit(BaseModel):
    type: str  # medication | prescription | document | care_action | diet_note
    id: uuid.UUID
    title: str
    subtitle: str | None = None
    snippet: str | None = None
    href: str


class SearchResults(BaseModel):
    query: str
    groups: dict[str, list[SearchHit]]
    total: int


def _like(q: str) -> str:
    escaped = q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{escaped}%"


def _prefix_tsquery(q: str) -> str | None:
    """'amox 500' -> 'amox:* & 500:*' (sanitized; None when nothing searchable remains)."""
    words = _WORD.findall(q.lower())
    return " & ".join(f"{w}:*" for w in words[:6]) or None


async def search(session: AsyncSession, user_id: uuid.UUID, q: str) -> SearchResults:
    q = q.strip()[:100]
    like = _like(q)
    groups: dict[str, list[SearchHit]] = {}

    meds = (
        await session.execute(
            select(Medication, Prescription.prescriber_name)
            .join(Prescription, Prescription.id == Medication.prescription_id)
            .where(
                Medication.user_id == user_id,
                or_(Medication.name.ilike(like), Medication.strength.ilike(like)),
            )
            .order_by(Medication.start_date.desc())
            .limit(PER_GROUP)
        )
    ).all()
    groups["medications"] = [
        SearchHit(
            type="medication",
            id=m.id,
            title=f"{m.name} {m.strength}".strip() if m.strength else m.name,
            subtitle=" · ".join(
                filter(None, [(m.schedule or {}).get("label"), medication_status(m).title(), who])
            ),
            href=f"/app/medications?focus={m.id}",
        )
        for m, who in meds
    ]

    rxs = (
        await session.execute(
            select(Prescription, Document.title)
            .join(Document, Document.id == Prescription.document_id)
            .where(
                Prescription.user_id == user_id,
                or_(
                    Prescription.prescriber_name.ilike(like),
                    Prescription.clinic_name.ilike(like),
                    Prescription.prescriber_specialty.ilike(like),
                    Document.title.ilike(like),
                ),
            )
            .order_by(Prescription.issued_on.desc().nulls_last())
            .limit(PER_GROUP)
        )
    ).all()
    groups["prescriptions"] = [
        SearchHit(
            type="prescription",
            id=p.id,
            title=f"Prescription from {p.prescriber_name or p.clinic_name or title}",
            subtitle=" · ".join(
                filter(
                    None,
                    [
                        p.clinic_name,
                        p.issued_on and f"{p.issued_on:%b} {p.issued_on.day}, {p.issued_on.year}",
                    ],
                )
            ),
            href=f"/app/prescriptions/{p.id}",
        )
        for p, title in rxs
    ]

    # Documents: title matches first, then full-text matches inside the pages.
    docs: dict[uuid.UUID, SearchHit] = {}
    for d in (
        await session.scalars(
            select(Document)
            .where(Document.user_id == user_id, Document.title.ilike(like))
            .order_by(Document.created_at.desc())
            .limit(PER_GROUP)
        )
    ).all():
        docs[d.id] = SearchHit(
            type="document",
            id=d.id,
            title=d.title,
            subtitle=d.kind.replace("_", " ").capitalize(),
            href=f"/app/documents/{d.id}",
        )
    tsq_text = _prefix_tsquery(q)
    if tsq_text and len(docs) < PER_GROUP:
        tsq = func.to_tsquery("english", tsq_text)
        headline = func.ts_headline(
            "english",
            DocumentChunk.content,
            tsq,
            "StartSel=<<,StopSel=>>,MaxWords=18,MinWords=6,MaxFragments=1",
        )
        rows = (
            await session.execute(
                select(DocumentChunk.document_id, DocumentChunk.page_no, Document.title, headline)
                .join(Document, Document.id == DocumentChunk.document_id)
                .where(DocumentChunk.user_id == user_id, DocumentChunk.tsv.op("@@")(tsq))
                .order_by(func.ts_rank_cd(DocumentChunk.tsv, tsq).desc())
                .limit(PER_GROUP * 3)
            )
        ).all()
        for doc_id, page_no, title, snippet in rows:
            if doc_id in docs or len(docs) >= PER_GROUP:
                continue
            docs[doc_id] = SearchHit(
                type="document",
                id=doc_id,
                title=title,
                subtitle=f"Page {page_no}",
                snippet=" ".join(snippet.split()),
                href=f"/app/documents/{doc_id}?page={page_no}",
            )
    groups["documents"] = list(docs.values())

    actions = (
        await session.scalars(
            select(CareAction)
            .where(CareAction.user_id == user_id, CareAction.title.ilike(like))
            .order_by(CareAction.completed_at.is_not(None), CareAction.due_on.asc().nulls_last())
            .limit(PER_GROUP)
        )
    ).all()
    groups["to_dos"] = [
        SearchHit(
            type="care_action",
            id=a.id,
            title=a.title,
            subtitle="Done"
            if a.completed_at
            else (f"Due {a.due_on:%b} {a.due_on.day}" if a.due_on else "To-do"),
            href=f"/app/prescriptions/{a.prescription_id}"
            if a.prescription_id
            else "/app/timeline",
        )
        for a in actions
    ]

    notes = (
        await session.scalars(
            select(DietNote)
            .where(DietNote.user_id == user_id, DietNote.text.ilike(like))
            .limit(PER_GROUP)
        )
    ).all()
    groups["diet_notes"] = [
        SearchHit(
            type="diet_note",
            id=n.id,
            title=n.text,
            subtitle=f"Diet note · {n.category}",
            href="/app/diet",
        )
        for n in notes
    ]

    groups = {k: v for k, v in groups.items() if v}
    return SearchResults(query=q, groups=groups, total=sum(len(v) for v in groups.values()))
