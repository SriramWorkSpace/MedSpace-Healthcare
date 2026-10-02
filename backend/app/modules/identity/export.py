"""Account data export: one JSON document with every record the user owns.

Assembled through each module's public service functions; secrets (password hash, refresh and
OAuth tokens, share-token hashes) are never included.
"""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.assistant import service as assistant
from app.modules.audit import service as audit
from app.modules.documents import service as documents
from app.modules.documents.schemas import DocumentOut
from app.modules.doses import service as doses
from app.modules.identity.models import User
from app.modules.identity.schemas import UserOut
from app.modules.records import service as records
from app.modules.records.schemas import CareActionOut
from app.modules.sharing import service as sharing


async def build_export(session: AsyncSession, user: User) -> dict:
    docs, _ = await documents.list_documents(session, user.id)
    prescriptions = [
        await records.get_prescription(session, user.id, p.id)
        for p in await records.list_prescriptions(session, user.id)
    ]
    standalone_actions = [
        CareActionOut.model_validate(a)
        for a in await records.list_care_actions(session, user.id)
        if a.prescription_id is None
    ]
    threads = []
    for t in await assistant.list_threads(session, user.id):
        messages = await assistant.thread_messages(session, t.id)
        threads.append(
            {
                "title": t.title,
                "created_at": t.created_at,
                "messages": [
                    {
                        "role": m.role,
                        "content": m.content,
                        "citations": m.citations,
                        "at": m.created_at,
                    }
                    for m in messages
                ],
            }
        )
    shares = [
        await sharing.to_out(session, link) for link in await sharing.list_links(session, user.id)
    ]
    activity, cursor = [], None
    while True:
        rows, cursor = await audit.list_for_user(session, user.id, limit=200, cursor=cursor)
        activity.extend(
            {"action": r.action, "at": r.created_at, "ip": r.ip, "meta": r.meta} for r in rows
        )
        if not cursor:
            break

    return jsonable_encoder(
        {
            "exported_at": datetime.now(UTC),
            "format": "medspace-export/v1",
            "notice": "Synthetic demo data only. Download original files from each document.",
            "profile": UserOut.model_validate(user),
            "documents": [DocumentOut.model_validate(d) for d in docs],
            "prescriptions": prescriptions,
            "other_to_dos": standalone_actions,
            "diet_notes": (await records.list_diet_notes(session, user.id)).notes,
            "lab_results": await records.list_lab_results(session, user.id),
            "dose_log": await doses.list_logs(session, user.id),
            "conversations": threads,
            "share_links": shares,
            "activity": activity,
        }
    )
