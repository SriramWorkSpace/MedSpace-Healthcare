"""Google sync (ADR-005): dose reminders and follow-ups -> Calendar, one-off to-dos -> Tasks.

Only confirmed records are synced. Every remote object is tracked in `sync_links`, so syncing is
idempotent (re-sync updates in place), edits propagate, and removal cleans up remotely.
"""

from __future__ import annotations

import contextlib
import logging
import uuid
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta

from fastapi import Request
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import utcnow
from app.core.errors import Conflict, NotFound
from app.core.security import decrypt, encrypt
from app.modules.audit import service as audit
from app.modules.identity.models import User
from app.modules.integrations.google import (
    GoogleAPIError,
    GoogleAuthError,
    Tokens,
    get_google,
)
from app.modules.integrations.models import OAuthConnection, SyncLink
from app.modules.records.models import CareAction, Medication, Prescription

logger = logging.getLogger("medspace.integrations")

TASKLIST_TITLE = "MedSpace"
DOSE_MINUTES = 15
FOOTER = (
    "Added by MedSpace from a confirmed record. MedSpace organizes your documents; always "
    "follow your prescriber's instructions."
)


# --------------------------------------------------------------------------- connection


async def get_connection(session: AsyncSession, user_id: uuid.UUID) -> OAuthConnection | None:
    return await session.scalar(
        select(OAuthConnection).where(
            OAuthConnection.user_id == user_id, OAuthConnection.provider == "google"
        )
    )


async def save_connection(
    session: AsyncSession, user: User, tokens: Tokens, email: str | None, request: Request | None
) -> OAuthConnection:
    conn = await get_connection(session, user.id) or OAuthConnection(user_id=user.id)
    conn.mode = get_google().mode
    conn.account_email = email
    conn.scopes = tokens.scope
    conn.access_token_enc = encrypt(tokens.access_token)
    if tokens.refresh_token:
        conn.refresh_token_enc = encrypt(tokens.refresh_token)
    conn.expires_at = tokens.expires_at
    conn.status = "active"
    session.add(conn)
    await audit.record(
        session,
        action="integration.connected",
        user_id=user.id,
        request=request,
        meta={"provider": "google", "mode": conn.mode},
    )
    await session.flush()
    return conn


async def access_token(session: AsyncSession, conn: OAuthConnection) -> str:
    """A valid access token, refreshing when it is about to expire."""
    if conn.status != "active":
        raise Conflict("Google access was revoked. Reconnect to keep syncing.")
    token = decrypt(conn.access_token_enc)
    fresh = conn.expires_at and conn.expires_at > datetime.now(UTC) + timedelta(seconds=60)
    if token and fresh:
        return token
    refresh = decrypt(conn.refresh_token_enc) if conn.refresh_token_enc else None
    if not refresh:
        conn.status = "revoked"
        await session.commit()
        raise Conflict("Google access expired. Reconnect to keep syncing.")
    try:
        tokens = await get_google().refresh(refresh)
    except GoogleAuthError as exc:
        conn.status = "revoked"
        await session.commit()
        raise Conflict("Google access was revoked. Reconnect to keep syncing.") from exc
    conn.access_token_enc = encrypt(tokens.access_token)
    conn.expires_at = tokens.expires_at
    await session.flush()
    return tokens.access_token


async def _require(session: AsyncSession, user_id: uuid.UUID) -> tuple[OAuthConnection, str]:
    conn = await get_connection(session, user_id)
    if conn is None:
        raise Conflict("Connect Google first.")
    return conn, await access_token(session, conn)


# --------------------------------------------------------------------------- builders


def _rrule(med: Medication) -> list[str]:
    period = (med.schedule or {}).get("period", "daily")
    if period == "once":
        return []
    rule = {"weekly": "FREQ=WEEKLY", "alternate_days": "FREQ=DAILY;INTERVAL=2"}.get(
        period, "FREQ=DAILY"
    )
    if med.end_date:
        rule += f";UNTIL={med.end_date:%Y%m%d}T235959Z"
    return [f"RRULE:{rule}"]


def _clock(hhmm: str) -> str:
    h, m = (int(x) for x in hhmm.split(":"))
    return f"{h % 12 or 12}:{m:02d} {'PM' if h >= 12 else 'AM'}"


def dose_event(med: Medication, time: str, tz: str, link_key: str) -> dict:
    start = datetime.fromisoformat(f"{med.start_date.isoformat()}T{time}:00")
    end = start + timedelta(minutes=DOSE_MINUTES)
    name = f"{med.name} {med.strength}".strip() if med.strength else med.name
    details = [d for d in (med.dose, med.instructions) if d]
    return {
        "summary": f"Take {name}",
        "description": "\n".join([*details, "", FOOTER]).strip(),
        "start": {"dateTime": start.isoformat(), "timeZone": tz},
        "end": {"dateTime": end.isoformat(), "timeZone": tz},
        "recurrence": _rrule(med),
        "reminders": {"useDefault": False, "overrides": [{"method": "popup", "minutes": 0}]},
        "colorId": "10",
        "extendedProperties": {"private": {"medspace_link": link_key}},
    }


def appointment_event(p: Prescription, link_key: str) -> dict:
    who = p.prescriber_name or p.clinic_name or "your prescriber"
    return {
        "summary": f"Follow-up with {who}",
        "location": p.clinic_name or "",
        "description": "\n".join(filter(None, [p.follow_up_notes, "", FOOTER])),
        "start": {"date": p.follow_up_on.isoformat()},
        "end": {"date": (p.follow_up_on + timedelta(days=1)).isoformat()},
        "extendedProperties": {"private": {"medspace_link": link_key}},
    }


def task_body(a: CareAction) -> dict:
    body = {
        "title": a.title,
        "notes": "\n".join(filter(None, [a.notes, FOOTER])),
        "status": "completed" if a.completed_at else "needsAction",
    }
    if a.due_on:
        body["due"] = f"{a.due_on.isoformat()}T00:00:00.000Z"  # Tasks keeps the date only
    return body


@dataclass
class Planned:
    target: str
    entity_type: str
    entity_id: uuid.UUID
    slot: str
    summary: str
    when: str
    repeat: str | None
    body: dict


async def _load_prescription(
    session: AsyncSession, user_id: uuid.UUID, prescription_id: uuid.UUID
) -> Prescription:
    p = await session.scalar(
        select(Prescription).where(
            Prescription.id == prescription_id, Prescription.user_id == user_id
        )
    )
    if p is None:
        raise NotFound("Prescription not found.")
    return p


def plan_items(p: Prescription, tz: str, *, calendar: bool, tasks: bool) -> list[Planned]:
    items: list[Planned] = []
    today = date.today()
    if calendar:
        for m in p.medications:
            if m.as_needed or m.stopped_at or (m.end_date and m.end_date < today):
                continue
            label = (m.schedule or {}).get("label") or "Scheduled"
            until = f" until {m.end_date:%b} {m.end_date.day}" if m.end_date else ", ongoing"
            for t in (m.schedule or {}).get("times", []):
                key = f"dose:{m.id}:{t}"
                body = dose_event(m, t, tz, key)
                items.append(
                    Planned(
                        "google_calendar",
                        "dose",
                        m.id,
                        t,
                        body["summary"],
                        _clock(t),
                        f"{label}{until}",
                        body,
                    )
                )
        if p.follow_up_on and p.follow_up_on >= today:
            key = f"appointment:{p.id}"
            body = appointment_event(p, key)
            items.append(
                Planned(
                    "google_calendar",
                    "appointment",
                    p.id,
                    "",
                    body["summary"],
                    f"{p.follow_up_on:%a, %b} {p.follow_up_on.day}",
                    None,
                    body,
                )
            )
    if tasks:
        for a in p.care_actions:
            if a.kind == "follow_up" or a.completed_at:
                continue  # follow-ups live on the calendar; finished to-dos stay finished
            when = f"Due {a.due_on:%b} {a.due_on.day}" if a.due_on else "No due date"
            items.append(
                Planned("google_tasks", "care_action", a.id, "", a.title, when, None, task_body(a))
            )
    return items


# --------------------------------------------------------------------------- sync


async def preview(session: AsyncSession, user: User, prescription_id: uuid.UUID) -> dict:
    p = await _load_prescription(session, user.id, prescription_id)
    items = plan_items(p, user.timezone, calendar=True, tasks=True)
    linked = await _links(session, user.id, prescription_id)
    keys = {(lk.target, lk.entity_type, lk.entity_id, lk.slot) for lk in linked}
    out = {"events": [], "tasks": []}
    for it in items:
        entry = {
            "summary": it.summary,
            "when": it.when,
            "repeat": it.repeat,
            "synced": (it.target, it.entity_type, it.entity_id, it.slot) in keys,
        }
        out["events" if it.target == "google_calendar" else "tasks"].append(entry)
    return out


async def _links(session: AsyncSession, user_id: uuid.UUID, prescription_id: uuid.UUID):
    return list(
        (
            await session.scalars(
                select(SyncLink).where(
                    SyncLink.user_id == user_id, SyncLink.prescription_id == prescription_id
                )
            )
        ).all()
    )


async def sync_prescription(
    session: AsyncSession,
    user: User,
    prescription_id: uuid.UUID,
    *,
    calendar: bool,
    tasks: bool,
    request: Request | None = None,
) -> dict:
    p = await _load_prescription(session, user.id, prescription_id)
    conn, token = await _require(session, user.id)
    google = get_google()
    items = plan_items(p, user.timezone, calendar=calendar, tasks=tasks)
    existing = {
        (lk.target, lk.entity_type, lk.entity_id, lk.slot): lk
        for lk in await _links(session, user.id, prescription_id)
    }

    if tasks and any(it.target == "google_tasks" for it in items):
        conn.tasklist_id = await google.ensure_tasklist(token, conn.tasklist_id, TASKLIST_TITLE)

    counts = {"events": 0, "tasks": 0, "removed": 0}
    wanted: set[tuple] = set()
    try:
        for it in items:
            key = (it.target, it.entity_type, it.entity_id, it.slot)
            wanted.add(key)
            link = existing.get(key)
            if it.target == "google_calendar":
                ext = await google.upsert_event(token, link.external_id if link else None, it.body)
                counts["events"] += 1
            else:
                ext = await google.upsert_task(
                    token, conn.tasklist_id, link.external_id if link else None, it.body
                )
                counts["tasks"] += 1
            if link is None:
                link = SyncLink(
                    user_id=user.id,
                    prescription_id=p.id,
                    target=it.target,
                    entity_type=it.entity_type,
                    entity_id=it.entity_id,
                    slot=it.slot,
                    external_id=ext,
                )
                session.add(link)
            link.external_id = ext
            link.summary = it.summary[:255]
            link.meta = {"when": it.when, "repeat": it.repeat}
            link.updated_at = utcnow()

        # Remove remote copies of things that no longer exist (a dose time deleted, a med stopped).
        targets = {t for t, on in (("google_calendar", calendar), ("google_tasks", tasks)) if on}
        for key, link in existing.items():
            if key[0] in targets and key not in wanted:
                await _delete_remote(google, token, conn, link)
                await session.delete(link)
                counts["removed"] += 1
    except GoogleAuthError as exc:
        conn.status = "revoked"
        await session.commit()
        raise Conflict("Google access was revoked. Reconnect to keep syncing.") from exc
    except GoogleAPIError as exc:
        await session.rollback()
        raise Conflict("Google didn't accept the update. Please try again.") from exc

    await audit.record(
        session,
        action="integration.synced",
        user_id=user.id,
        request=request,
        entity_type="prescription",
        entity_id=p.id,
        meta={**counts, "mode": conn.mode},
    )
    await session.flush()
    return counts


async def _delete_remote(google, token: str, conn: OAuthConnection, link: SyncLink) -> None:
    if link.target == "google_calendar":
        await google.delete_event(token, link.external_id)
    elif conn.tasklist_id:
        await google.delete_task(token, conn.tasklist_id, link.external_id)


async def unsync_prescription(
    session: AsyncSession, user: User, prescription_id: uuid.UUID, request: Request | None = None
) -> int:
    await _load_prescription(session, user.id, prescription_id)
    links = await _links(session, user.id, prescription_id)
    if not links:
        return 0
    conn, token = await _require(session, user.id)
    google = get_google()
    for link in links:
        with contextlib.suppress(GoogleAPIError):  # already gone remotely; drop our link anyway
            await _delete_remote(google, token, conn, link)
        await session.delete(link)
    await audit.record(
        session,
        action="integration.unsynced",
        user_id=user.id,
        request=request,
        entity_type="prescription",
        entity_id=prescription_id,
        meta={"removed": len(links)},
    )
    await session.flush()
    return len(links)


async def pull_task_status(session: AsyncSession, user: User) -> int:
    """Mirror to-dos completed in Google Tasks back into MedSpace."""
    conn = await get_connection(session, user.id)
    if conn is None or conn.status != "active" or not conn.tasklist_id:
        return 0
    token = await access_token(session, conn)
    google = get_google()
    links = (
        await session.scalars(
            select(SyncLink).where(SyncLink.user_id == user.id, SyncLink.target == "google_tasks")
        )
    ).all()
    updated = 0
    for link in links:
        done = await google.task_completed(token, conn.tasklist_id, link.external_id)
        action = await session.get(CareAction, link.entity_id)
        if action and done and action.completed_at is None:
            action.completed_at = utcnow()
            updated += 1
    await session.flush()
    return updated


async def disconnect(
    session: AsyncSession, user: User, *, remove_items: bool, request: Request | None = None
) -> None:
    conn = await get_connection(session, user.id)
    if conn is None:
        return
    google = get_google()
    links = (await session.scalars(select(SyncLink).where(SyncLink.user_id == user.id))).all()
    if remove_items and conn.status == "active":
        try:
            token = await access_token(session, conn)
            for link in links:
                await _delete_remote(google, token, conn, link)
        except (Conflict, GoogleAPIError, GoogleAuthError):
            pass
    try:
        token_for_revoke = decrypt(conn.refresh_token_enc or conn.access_token_enc)
        if token_for_revoke:
            await google.revoke(token_for_revoke)
    except Exception:  # revocation is best-effort
        logger.warning("google token revocation failed", exc_info=True)
    await session.execute(delete(SyncLink).where(SyncLink.user_id == user.id))
    await session.delete(conn)
    await audit.record(
        session,
        action="integration.disconnected",
        user_id=user.id,
        request=request,
        meta={"provider": "google", "removed_items": remove_items},
    )
    await session.flush()


async def links_for(session: AsyncSession, user_id: uuid.UUID, prescription_id: uuid.UUID):
    return await _links(session, user_id, prescription_id)
