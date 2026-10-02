"""Ask MedSpace: source-grounded Q&A over the user's own records (RAG).

Pipeline: question -> intent guardrail -> hybrid retrieval (pgvector cosine + Postgres full-text,
fused with Reciprocal Rank Fusion, always filtered by user_id) + confirmed medication records ->
numbered sources -> answer (Groq stream, or an extractive offline composer) with [n] citations.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
import uuid
from collections.abc import AsyncIterator
from dataclasses import asdict, dataclass, field

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.errors import NotFound
from app.modules.assistant.models import ChatMessage, ChatThread, DocumentChunk
from app.modules.documents.models import Document, DocumentStatus
from app.modules.records.models import Medication, Prescription
from app.modules.records.service import medication_status
from app.shared.embeddings import HashEmbedder, get_embedder
from app.shared.llm import LLMError, get_llm

logger = logging.getLogger("medspace.assistant")

CHUNK_SIZE = 700
CHUNK_OVERLAP = 120
TOP_K = 6
RRF_K = 60

_GENERAL = (
    "a an and are as at be by can could did do does for from had has have how i if in is it "
    "its me my of on or our should so that the their them then there these they this to was "
    "what when where which who why will with would you your am been being take taking took "
    "tell show list about please any all "
).split()
# Domain words present in nearly every document: they add noise, not signal.
_DOMAIN = (
    "prescription prescriptions prescribed document documents record records report reports "
    "doctor dr last latest did say says said according mention mentioned "
).split()
STOPWORDS = frozenset(_GENERAL + _DOMAIN)

ADVICE = re.compile(
    r"\b(should i (?:take|stop|start|skip|increase|decrease|double|switch|keep)|"
    r"is it (?:safe|ok|okay|dangerous|bad)|can i (?:take|mix|drink|stop|skip|double|combine)|"
    r"diagnos\w*|what(?:'s| is) wrong with me|do i have|am i (?:sick|ill)|"
    r"(?:increase|decrease|change|adjust|lower|raise) (?:my )?(?:dose|dosage)|"
    r"side effects? (?:of|from)|interact\w*|overdose|instead of|"
    r"is (?:my|this|that)(?: [a-z0-9]+){1,4} (?:bad|good|normal|high|low|ok|okay|dangerous|healthy|"
    r"worrying|concerning)|what does (?:my|this|that|it) [a-z0-9 ]{0,30}mean)\b",
    re.IGNORECASE,
)
MEDS_LIST = re.compile(
    r"\b(what|which|list|all|current\w*)\b.*\b(medications?|medicines?|meds|pills|drugs?)\b|"
    r"\bwhat am i (?:on|taking)\b",
    re.IGNORECASE,
)

DIET = re.compile(
    r"\b(diet|food|foods|eat|eating|drink|drinks|drinking|salt|sodium|sugar|sugary|alcohol|"
    r"caffeine|coffee|meal|meals|dairy|milk|grapefruit|fluids?|water|potassium|protein|"
    r"nutrition|nutrients?|snack|snacks|fried|fatty)\b",
    re.IGNORECASE,
)

LABS = re.compile(
    r"\b(labs?|lab results?|test results?|results?|blood ?work|blood tests?|cholesterol|ldl|hdl|"
    r"triglycerides?|lipids?|hba1c|a1c|glucose|sugar levels?|creatinine|tsh|thyroid|"
    r"vitamin [a-z0-9]+|ha?emoglobin|reference range)\b",
    re.IGNORECASE,
)
_LAB_ALIASES = {"a1c": "hba1c", "sugar": "glucose", "lipid": "cholesterol", "lipids": "cholesterol"}
_LAB_GENERIC = {"total", "fasting", "serum", "random", "level"}

ADVICE_REPLY = (
    "I can't give medical advice, diagnose, or suggest changing a medication or dose. "
    "That's a conversation for your prescriber or pharmacist. "
    "Here's what your records say that might help you prepare for it:"
)
NOT_FOUND_REPLY = (
    "I couldn't find that in your records. I only answer from documents you've uploaded, so if it "
    "lives on paper somewhere, uploading it will let me help."
)

SYSTEM_PROMPT = """You are Ask MedSpace, an assistant that answers questions using ONLY the \
user's own medical records, provided below as numbered sources.

Rules:
- Use only the sources. Cite every factual sentence with its source number in square brackets, \
e.g. [2]. Never cite a number that is not listed.
- If the sources don't contain the answer, say you couldn't find it in their records.
- Never diagnose, never recommend starting, stopping or changing a medication or dose, and never \
give medical advice. For such questions, state what the documents say and suggest asking their \
prescriber or pharmacist.
- If a source is marked UNCONFIRMED, mention that the user hasn't reviewed it yet.
- Be concise: at most about 120 words, plain language, bullet points for lists. No preamble."""


# --------------------------------------------------------------------------- indexing


def chunk_pages(pages: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Split page text into overlapping chunks on line boundaries; chunks never span pages."""
    out: list[tuple[int, str]] = []
    for page_no, text in pages:
        buf = ""
        for line in (ln.strip() for ln in text.splitlines()):
            if not line:
                continue
            if buf and len(buf) + len(line) + 1 > CHUNK_SIZE:
                out.append((page_no, buf))
                tail = buf[-CHUNK_OVERLAP:]
                buf = tail[tail.find(" ") + 1 :] if " " in tail else ""
            buf = f"{buf}\n{line}".strip()
        if buf:
            out.append((page_no, buf))
    return out


async def index_document(session: AsyncSession, document_id: uuid.UUID) -> int:
    doc = await session.scalar(select(Document).where(Document.id == document_id))
    if doc is None:
        return 0
    from app.modules.documents.models import DocumentPage

    pages = (
        await session.execute(
            select(DocumentPage.page_no, DocumentPage.text)
            .where(DocumentPage.document_id == document_id)
            .order_by(DocumentPage.page_no)
        )
    ).all()
    chunks = chunk_pages([(p, t) for p, t in pages])
    await session.execute(delete(DocumentChunk).where(DocumentChunk.document_id == document_id))
    if not chunks:
        return 0
    vectors = await get_embedder().embed_documents([f"{doc.title}\n{c}" for _, c in chunks])
    session.add_all(
        DocumentChunk(
            document_id=doc.id,
            user_id=doc.user_id,
            page_no=page_no,
            chunk_index=i,
            content=content,
            embedding=vec,
        )
        for i, ((page_no, content), vec) in enumerate(zip(chunks, vectors, strict=True))
    )
    await session.flush()
    return len(chunks)


# --------------------------------------------------------------------------- retrieval


@dataclass
class Source:
    n: int
    kind: str  # document | record
    title: str
    page_no: int | None
    snippet: str
    document_id: str | None
    confirmed: bool
    text: str  # full text given to the model (not sent to the client)
    medication: Medication | None = field(default=None, repr=False, compare=False)

    def public(self) -> dict:
        return {k: v for k, v in asdict(self).items() if k not in ("text", "medication")}


def keywords(question: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", question.lower())
    return [w for w in dict.fromkeys(words) if w not in STOPWORDS and len(w) > 1]


async def _hybrid_chunk_ids(
    session: AsyncSession, user_id: uuid.UUID, question: str, terms: list[str]
) -> tuple[list[uuid.UUID], bool]:
    """Return fused chunk ids and whether the keyword leg found anything."""
    qvec = await get_embedder().embed_query(question)
    dist = DocumentChunk.embedding.cosine_distance(qvec)
    vec_rows = (
        await session.execute(
            select(DocumentChunk.id, dist.label("d"))
            .where(DocumentChunk.user_id == user_id)
            .order_by(dist)
            .limit(20)
        )
    ).all()

    kw_ids: list[uuid.UUID] = []
    if terms:
        tsq = func.to_tsquery("english", " | ".join(terms))
        kw_ids = list(
            (
                await session.scalars(
                    select(DocumentChunk.id)
                    .where(DocumentChunk.user_id == user_id, DocumentChunk.tsv.op("@@")(tsq))
                    .order_by(func.ts_rank_cd(DocumentChunk.tsv, tsq).desc())
                    .limit(20)
                )
            ).all()
        )

    semantic = not isinstance(get_embedder(), HashEmbedder)
    vec_ids = [cid for cid, d in vec_rows if not semantic or (1 - d) >= 0.55]

    scores: dict[uuid.UUID, float] = {}
    for ranking in (vec_ids, kw_ids):
        for rank, cid in enumerate(ranking):
            scores[cid] = scores.get(cid, 0.0) + 1.0 / (RRF_K + rank + 1)
    fused = sorted(scores, key=scores.get, reverse=True)
    # Offline hash vectors are lexical noise without a keyword hit; never treat them as evidence.
    if not semantic and not kw_ids:
        fused = []
    return fused[:TOP_K], bool(kw_ids)


def _record_line(m: Medication, doc_title: str) -> str:
    sched = m.schedule or {}
    times = ", ".join(sched.get("times", []))
    parts = [f"{m.name}{f' {m.strength}' if m.strength else ''}{f' {m.form}' if m.form else ''}"]
    parts.append(sched.get("label") or (m.frequency_raw or "schedule not set"))
    if times:
        parts.append(f"at {times}")
    if m.duration_days:
        parts.append(f"for {m.duration_days} days ({m.start_date} to {m.end_date})")
    else:
        parts.append(f"from {m.start_date}, no end date")
    if m.instructions:
        parts.append(m.instructions)
    parts.append(f"status: {medication_status(m)}")
    return f"{', '.join(parts)}. Source: {doc_title} page {m.source_page}."


async def gather_sources(
    session: AsyncSession, user_id: uuid.UUID, question: str, *, include_all_meds: bool
) -> list[Source]:
    terms = keywords(question)
    chunk_ids, _ = await _hybrid_chunk_ids(session, user_id, question, terms)
    sources: list[Source] = []

    # Confirmed records first: they are the reviewed truth.
    rows = (
        await session.execute(
            select(Medication, Document.title, Document.id)
            .join(Prescription, Prescription.id == Medication.prescription_id)
            .join(Document, Document.id == Prescription.document_id)
            .where(Medication.user_id == user_id)
            .order_by(Medication.start_date.desc())
        )
    ).all()
    mentioned = [
        (m, title, did)
        for m, title, did in rows
        if include_all_meds or m.name.lower() in question.lower()
    ]
    if include_all_meds:
        mentioned = [
            r for r in mentioned if medication_status(r[0]) in ("active", "upcoming")
        ] or mentioned
    for m, title, did in mentioned[:10]:
        line = _record_line(m, title)
        sources.append(
            Source(
                n=len(sources) + 1,
                kind="record",
                title=f"{m.name} (confirmed record)",
                page_no=m.source_page,
                snippet=line[:220],
                document_id=str(did),
                confirmed=True,
                text=line,
                medication=m,
            )
        )

    # Diet questions: the care team's written diet notes and food rules on current medicines.
    if DIET.search(question):
        from app.modules.records import service as records

        diet = await records.list_diet_notes(session, user_id)
        for note in diet.notes[:10]:
            where = f"{note.document_title} page {note.source_page or 1}"
            sources.append(
                Source(
                    n=len(sources) + 1,
                    kind="record",
                    title=f"Diet note: {note.document_title}",
                    page_no=note.source_page,
                    snippet=note.text,
                    document_id=str(note.document_id),
                    confirmed=True,
                    text=f"{note.text} Source: {where}.",
                )
            )
        for food in diet.medication_notes[:8]:
            label = f"{food.name} {food.strength}".strip() if food.strength else food.name
            sources.append(
                Source(
                    n=len(sources) + 1,
                    kind="record",
                    title=f"{food.name} instructions",
                    page_no=food.source_page,
                    snippet=f"{label}: {food.text.lower()}",
                    document_id=str(food.document_id) if food.document_id else None,
                    confirmed=True,
                    text=f"Take {label} {food.text.lower()}.",
                )
            )

    # Lab questions: confirmed results with the range printed on each report. No interpretation.
    if LABS.search(question):
        from app.modules.records import service as records

        trends = await records.list_lab_trends(session, user_id)
        words = set(re.findall(r"[a-z0-9]+", question.lower()))
        words |= {_LAB_ALIASES[w] for w in words if w in _LAB_ALIASES}
        specific = [t for t in trends if (set(t.key.split("-")) - _LAB_GENERIC) & words]
        for t in (specific or trends)[:10]:
            sources.append(_lab_source(len(sources) + 1, t))

    if chunk_ids:
        chunk_rows = (
            await session.execute(
                select(DocumentChunk, Document.title, Document.status)
                .join(Document, Document.id == DocumentChunk.document_id)
                .where(DocumentChunk.id.in_(chunk_ids), DocumentChunk.user_id == user_id)
            )
        ).all()
        by_id = {c.id: (c, t, s) for c, t, s in chunk_rows}
        for cid in chunk_ids:
            if cid not in by_id:
                continue
            chunk, title, status = by_id[cid]
            sources.append(
                Source(
                    n=len(sources) + 1,
                    kind="document",
                    title=title,
                    page_no=chunk.page_no,
                    snippet=_best_snippet(chunk.content, terms),
                    document_id=str(chunk.document_id),
                    confirmed=status == DocumentStatus.CONFIRMED,
                    text=chunk.content,
                )
            )
    return sources


def _best_snippet(text: str, terms: list[str], width: int = 220) -> str:
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return text[:width]
    best = max(lines, key=lambda ln: sum(t in ln.lower() for t in terms))
    return best[:width]


# --------------------------------------------------------------------------- answering


def classify(question: str) -> str:
    if ADVICE.search(question):
        return "advice"
    if MEDS_LIST.search(question):
        return "meds"
    return "lookup"


def _clock(hhmm: str) -> str:
    h, m = (int(x) for x in hhmm.split(":"))
    return f"{h % 12 or 12}:{m:02d} {'PM' if h >= 12 else 'AM'}"


def _day(d) -> str:
    return f"{d:%b} {d.day}"


def describe_medication(m: Medication) -> str:
    """Plain-language sentence for one confirmed medication (used by the offline composer)."""
    sched = m.schedule or {}
    name = f"{m.name}{f' {m.strength}' if m.strength else ''}"
    if m.as_needed:
        how = "only as needed"
    else:
        how = (sched.get("label") or "on a schedule").lower()
        times = [_clock(t) for t in sched.get("times", [])]
        if times:
            joined = times[0] if len(times) == 1 else f"{', '.join(times[:-1])} and {times[-1]}"
            how += f" at {joined}"
    if m.duration_days and m.end_date:
        span = f" for {m.duration_days} days ({_day(m.start_date)} to {_day(m.end_date)})"
    else:
        span = f", ongoing since {_day(m.start_date)}"
    extra = f", {m.instructions}" if m.instructions else ""
    return f"{name}: {how}{span}{extra}"


def _lab_source(n: int, t) -> Source:
    """t: a records LabTrendOut. States the value and the printed range, nothing more."""
    r = t.latest
    unit = f" {r.unit}" if r.unit else ""
    line = f"{t.name}: {r.value_text}{unit} on {_day(r.collected_on)}, {r.collected_on.year}"
    if r.ref_range:
        where = {"high": "above", "low": "below", "normal": "within"}.get(r.flag or "")
        marked = f", {where} that range" if where else ""
        line += f" (range printed on the report: {r.ref_range}{marked})"
    line += "."
    if p := t.previous:
        p_unit = f" {p.unit}" if p.unit else ""
        line += (
            f" Previous: {p.value_text}{p_unit} on {_day(p.collected_on)}, {p.collected_on.year}."
        )
    return Source(
        n=n,
        kind="record",
        title=f"{t.name} (lab result)",
        page_no=r.source_page,
        snippet=line[:220],
        document_id=str(r.document_id),
        confirmed=True,
        text=f"{line} Source: {r.document_title} page {r.source_page or 1}.",
    )


def compose_offline(question: str, intent: str, sources: list[Source]) -> str:
    """Extractive answer for keyless mode: plain sentences from records, quotes from documents."""
    terms = keywords(question)
    records = [s for s in sources if s.kind == "record"]
    docs = [s for s in sources if s.kind == "document"]
    out: list[str] = []

    if intent == "advice":
        out.append(ADVICE_REPLY)
    if records:
        if intent == "meds":
            plural = "s" if len(records) != 1 else ""
            out.append(f"You have {len(records)} current medication{plural} on record:")
        for s in records[:8]:
            text = (
                describe_medication(s.medication) if s.medication else s.text.split(" Source:")[0]
            )
            out.append(f"- {text} [{s.n}]")

    picked: list[tuple[str, Source]] = []
    if docs and intent != "meds":
        scored = []
        for s in docs:
            for ln in s.text.splitlines():
                score = sum(t in ln.lower() for t in terms)
                if score:
                    scored.append((score, ln.strip(), s))
        scored.sort(key=lambda x: -x[0])
        seen: set[str] = set()
        for _, ln, s in scored:
            if ln not in seen:
                seen.add(ln)
                picked.append((ln, s))
        picked = picked[: 2 if records else 4]
    if picked:
        out.append(
            "As written in your documents:" if records else "Here's what your documents say:"
        )
        out.extend(f'- "{ln}" [{s.n}]' for ln, s in picked)
        if any(not s.confirmed for _, s in picked):
            out.append("Part of this comes from a document you haven't reviewed yet.")

    if len(out) <= (1 if intent == "advice" else 0):
        return NOT_FOUND_REPLY
    return "\n".join(out)


def build_prompt(question: str, sources: list[Source], history: list[ChatMessage]) -> list[dict]:
    blocks = []
    for s in sources:
        flag = "" if s.confirmed else " UNCONFIRMED"
        where = f", page {s.page_no}" if s.page_no else ""
        blocks.append(f"[{s.n}] {s.title}{where}{flag}\n{s.text}")
    context = "\n\n".join(blocks) if blocks else "(no matching records)"
    messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in history[-6:]:
        messages.append({"role": m.role, "content": m.content[:1500]})
    messages.append({"role": "user", "content": f"Sources:\n{context}\n\nQuestion: {question}"})
    return messages


async def answer_stream(
    question: str, intent: str, sources: list[Source], history: list[ChatMessage]
) -> AsyncIterator[str]:
    llm = get_llm()
    if llm is None:
        text = compose_offline(question, intent, sources)
        # Reveal in small slices so the offline demo reads like the live model.
        for i in range(0, len(text), 12):
            yield text[i : i + 12]
            await asyncio.sleep(0.012)
        return
    if not sources:
        yield NOT_FOUND_REPLY
        return
    try:
        async for delta in llm.stream_text(
            model=get_settings().groq_chat_model, messages=build_prompt(question, sources, history)
        ):
            yield delta
    except LLMError:
        logger.exception("assistant stream failed; falling back to extractive answer")
        yield "\n\n" + compose_offline(question, intent, sources)


def used_citations(answer: str, sources: list[Source]) -> list[dict]:
    cited = {int(n) for n in re.findall(r"\[(\d{1,2})\]", answer)}
    return [s.public() for s in sources if s.n in cited]


# --------------------------------------------------------------------------- threads


async def create_thread(session: AsyncSession, user_id: uuid.UUID, title: str | None) -> ChatThread:
    thread = ChatThread(user_id=user_id, title=(title or "New conversation")[:120])
    session.add(thread)
    await session.flush()
    return thread


async def get_thread(session: AsyncSession, user_id: uuid.UUID, thread_id: uuid.UUID) -> ChatThread:
    thread = await session.scalar(
        select(ChatThread).where(ChatThread.id == thread_id, ChatThread.user_id == user_id)
    )
    if thread is None:
        raise NotFound("Conversation not found.")
    return thread


async def list_threads(session: AsyncSession, user_id: uuid.UUID) -> list[ChatThread]:
    return list(
        (
            await session.scalars(
                select(ChatThread)
                .where(ChatThread.user_id == user_id)
                .order_by(ChatThread.updated_at.desc())
                .limit(50)
            )
        ).all()
    )


async def thread_messages(session: AsyncSession, thread_id: uuid.UUID) -> list[ChatMessage]:
    return list(
        (
            await session.scalars(
                select(ChatMessage)
                .where(ChatMessage.thread_id == thread_id)
                .order_by(ChatMessage.created_at)
            )
        ).all()
    )


def sse(event: str, data: dict | str) -> str:
    payload = data if isinstance(data, str) else json.dumps(data, default=str)
    return f"event: {event}\ndata: {payload}\n\n"
