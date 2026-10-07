"""Demo accounts: every "Try the demo" click gets an isolated, synthetic, short-lived account.

Seeding runs the real pipeline (real PDFs -> extraction -> confirmation) in offline mode, so the
demo exercises the same code paths as a user would, without spending LLM calls.
"""

from __future__ import annotations

import logging
import secrets
from datetime import UTC, date, datetime, time, timedelta

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.db import utcnow
from app.core.errors import ServiceUnavailable
from app.modules.circle.models import CareLink
from app.modules.demo import samples
from app.modules.documents import service as documents
from app.modules.documents.models import DocumentStatus
from app.modules.doses import service as doses
from app.modules.extraction import service as extraction
from app.modules.identity import service as identity
from app.modules.identity.models import User
from app.modules.identity.schemas import SignupIn
from app.modules.records.models import CareAction, Prescription
from app.modules.supply import service as supply
from app.modules.visits import service as visits
from app.modules.visits.schemas import VisitCreate

logger = logging.getLogger("medspace.demo")

DEMO_NAMES = ("Avery Lindqvist", "Noor Haddad", "Mateo Okafor", "Priya Raman", "Jun Takeda")


async def _ingest(session: AsyncSession, user: User, filename: str, data: bytes, issued: date):
    doc = await documents.create_document(session, user_id=user.id, filename=filename, data=data)
    # Backdate the upload so the library and timeline look lived-in.
    doc.created_at = datetime.combine(issued, time(9, 30), tzinfo=UTC)
    await session.flush()
    return doc


async def seed(session: AsyncSession, user: User) -> None:
    today = date.today()
    for sc in samples.SCENARIOS:
        issued = samples.issued(sc, today)
        doc = await _ingest(
            session, user, f"rx-{sc.slug}.pdf", samples.build_pdf(sc, today), issued
        )
        texts = await _page_texts(session, doc.id)
        payload, method, model = await extraction.extract_document(
            doc, texts, user.dose_times, offline=True
        )
        draft = await extraction.save_draft(session, doc, payload, method, model)
        await extraction.confirm(session, user, draft.id, extraction.payload_to_confirm(payload))

    # Older to-dos are done; recent ones stay open.
    await session.flush()
    actions = await session.scalars(
        select(CareAction).where(CareAction.user_id == user.id, CareAction.due_on < today)
    )
    for a in actions.all():
        a.completed_at = datetime.combine(a.due_on, time(17, 0), tzinfo=UTC)

    # Lab reports run through the same offline extraction and are confirmed as read.
    for lab in samples.LAB_REPORTS:
        lab_date = today - timedelta(days=lab.days_ago)
        doc = await _ingest(
            session, user, f"lab-{lab.slug}.pdf", samples.build_lab_pdf(lab, today), lab_date
        )
        doc.title = lab.title.capitalize()
        texts = await _page_texts(session, doc.id)
        payload, method, model = await extraction.extract_document(
            doc, texts, user.dose_times, offline=True
        )
        draft = await extraction.save_draft(session, doc, payload, method, model)
        await extraction.confirm(session, user, draft.id, extraction.payload_to_confirm(payload))

    # A fresh prescription waiting in the review queue.
    pending = samples.PENDING
    doc = await _ingest(
        session, user, f"rx-{pending.slug}.pdf", samples.build_pdf(pending, today), today
    )
    texts = await _page_texts(session, doc.id)
    payload, method, model = await extraction.extract_document(
        doc, texts, user.dose_times, offline=True
    )
    await extraction.save_draft(session, doc, payload, method, model)
    documents.set_status(doc, DocumentStatus.NEEDS_REVIEW)
    await session.flush()

    await doses.seed_history(session, user)

    # Supply counts for the long-term medicines: one runs low soon, one has plenty.
    await supply.seed_demo(session, user)

    # A visit prep for the next follow-up, with two questions already written.
    follow_up = (
        await session.execute(
            select(Prescription.follow_up_on, Prescription.prescriber_name)
            .where(Prescription.user_id == user.id, Prescription.follow_up_on >= today)
            .order_by(Prescription.follow_up_on)
            .limit(1)
        )
    ).first()
    if follow_up:
        prep = await visits.create_prep(
            session, user, VisitCreate(visit_date=follow_up[0], clinician=follow_up[1])
        )
        prep.questions = [
            {"id": "demo-1", "text": "Do I need another CBC after this one?", "done": False},
            {"id": "demo-2", "text": "Can Atorvastatin move to the morning?", "done": False},
        ]

    # Ask MedSpace indexing runs in the background once this commits (jobs.index_demo_documents).


async def seed_family(session: AsyncSession, user: User, handle: str) -> None:
    """A fictional family member who added the demo user to her care circle as a helper.

    Lighter than the main seed: her diabetes prescription, two lab panels, dose history and a
    supply count, so the profile switcher has something real to show.
    """
    family = await identity.create_user(
        session,
        SignupIn(
            email=f"demo-{handle}-family@demo.medspace.dev",
            password=secrets.token_urlsafe(24),
            display_name="Rosa Lindqvist",
            timezone=user.timezone,
        ),
        is_demo=True,
    )
    today = date.today()
    sc = samples.SCENARIOS[1]
    doc = await _ingest(
        session,
        family,
        f"rx-{sc.slug}.pdf",
        samples.build_pdf(sc, today),
        samples.issued(sc, today),
    )
    texts = await _page_texts(session, doc.id)
    payload, method, model = await extraction.extract_document(
        doc, texts, family.dose_times, offline=True
    )
    draft = await extraction.save_draft(session, doc, payload, method, model)
    await extraction.confirm(session, family, draft.id, extraction.payload_to_confirm(payload))
    for lab in [r for r in samples.LAB_REPORTS if "diabetes" in r.slug]:
        lab_date = today - timedelta(days=lab.days_ago)
        doc = await _ingest(
            session, family, f"lab-{lab.slug}.pdf", samples.build_lab_pdf(lab, today), lab_date
        )
        doc.title = lab.title.capitalize()
        texts = await _page_texts(session, doc.id)
        payload, method, model = await extraction.extract_document(
            doc, texts, family.dose_times, offline=True
        )
        draft = await extraction.save_draft(session, doc, payload, method, model)
        await extraction.confirm(session, family, draft.id, extraction.payload_to_confirm(payload))
    await doses.seed_history(session, family)
    await supply.seed_demo(session, family)
    session.add(
        CareLink(
            owner_id=family.id,
            caregiver_id=user.id,
            invite_email=user.email,
            role="helper",
            status="active",
            expires_at=utcnow(),
            accepted_at=utcnow(),
        )
    )
    await session.flush()


async def seed_quietly(session: AsyncSession, user: User) -> None:
    """Seed demo records for a new simulated account; never let seeding block a sign-in."""
    try:
        async with session.begin_nested():
            await seed(session, user)
    except Exception:
        logger.exception("demo seeding failed for %s", user.id)


async def _page_texts(session: AsyncSession, doc_id) -> list[str]:
    doc = await documents.get_document_by_id(session, doc_id)
    return [p.text for p in doc.pages] if doc else []


async def create_demo_account(session: AsyncSession) -> User:
    live = await session.scalar(
        select(func.count()).select_from(User).where(User.is_demo.is_(True))
    )
    if (live or 0) >= get_settings().demo_max_accounts:
        raise ServiceUnavailable(
            "The demo is busy right now. Try again later, or create a free account."
        )
    handle = secrets.token_hex(5)
    user = await identity.create_user(
        session,
        SignupIn(
            email=f"demo-{handle}@demo.medspace.dev",
            password=secrets.token_urlsafe(24),
            display_name=secrets.choice(DEMO_NAMES),
            timezone="America/New_York",
        ),
        is_demo=True,
    )
    try:
        async with session.begin_nested():
            await seed(session, user)
    except Exception:  # an empty demo is better than no demo
        logger.exception("demo seeding failed for %s", user.id)
    try:
        async with session.begin_nested():
            await seed_family(session, user, handle)
    except Exception:
        logger.exception("demo family seeding failed for %s", user.id)
    return user


async def purge_expired_demo_accounts(session: AsyncSession) -> int:
    cutoff = utcnow() - timedelta(hours=get_settings().demo_ttl_hours)
    expired = list(
        (
            await session.scalars(
                select(User.id).where(User.is_demo.is_(True), User.created_at < cutoff)
            )
        ).all()
    )
    if not expired:
        return 0
    await session.execute(delete(User).where(User.id.in_(expired)))
    await session.commit()
    for user_id in expired:
        await documents.purge_user_files(user_id)
    return len(expired)
