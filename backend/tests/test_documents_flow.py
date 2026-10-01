"""End-to-end API flow: upload -> process -> review -> confirm -> records."""

from __future__ import annotations

import httpx

from app.modules.demo.samples import SCENARIOS, build_pdf, build_scan_png
from app.shared.queue import drain
from tests.conftest import BASE_URL, csrf, signup


async def upload(
    client: httpx.AsyncClient, data: bytes, name: str = "rx.pdf", **form
) -> httpx.Response:
    return await client.post(
        "/api/documents",
        files={"file": (name, data, "application/octet-stream")},
        data=form,
        headers=csrf(client),
    )


def confirm_body(payload: dict) -> dict:
    """What the review screen sends back when the user accepts the draft as-is."""
    return {
        "document_kind": payload["document_type"],
        "prescriber": payload["prescriber"],
        "issued_on": payload["issued_on"],
        "follow_up": payload["follow_up"],
        "summary": payload["summary"],
        "medications": [
            {
                k: m[k]
                for k in (
                    "name",
                    "strength",
                    "form",
                    "dose",
                    "route",
                    "frequency_raw",
                    "schedule",
                    "duration_days",
                    "instructions",
                    "source_page",
                )
            }
            for m in payload["medications"]
        ],
        "care_actions": [
            {k: a[k] for k in ("kind", "title", "due_on", "notes", "source_page")}
            for a in payload["care_actions"]
        ],
    }


async def test_full_prescription_flow(auth_client: httpx.AsyncClient):
    resp = await upload(auth_client, build_pdf(SCENARIOS[0]), "riverside_rx.pdf")
    assert resp.status_code == 202, resp.text
    doc = resp.json()
    assert doc["status"] == "queued"
    assert doc["title"] == "Riverside rx"
    assert doc["has_text_layer"] is True

    await drain()
    detail = (await auth_client.get(f"/api/documents/{doc['id']}")).json()
    assert detail["status"] == "needs_review"
    assert detail["pages"][0]["text"].startswith("Riverside Family Clinic")

    extraction = (await auth_client.get(f"/api/documents/{doc['id']}/extraction")).json()
    assert extraction["method"] == "heuristic"
    meds = {m["name"]: m for m in extraction["payload"]["medications"]}
    assert set(meds) == {"Amoxicillin", "Ibuprofen", "Cetirizine"}
    assert meds["Amoxicillin"]["schedule"]["times"] == ["08:00", "20:00"]
    assert meds["Ibuprofen"]["schedule"]["as_needed"] is True

    confirmed = await auth_client.post(
        f"/api/extractions/{extraction['id']}/confirm",
        json=confirm_body(extraction["payload"]),
        headers=csrf(auth_client),
    )
    assert confirmed.status_code == 200, confirmed.text
    prescription_id = confirmed.json()["prescription_id"]

    rx = (await auth_client.get(f"/api/prescriptions/{prescription_id}")).json()
    assert rx["prescriber_name"] == "Dr. Imani Oduya"
    assert rx["medication_count"] == 3
    amox = next(m for m in rx["medications"] if m["name"] == "Amoxicillin")
    assert amox["duration_days"] == 7
    assert amox["status"] in {"active", "completed"}
    kinds = sorted(a["kind"] for a in rx["care_actions"])
    assert kinds.count("course_completion") == 2 and "lab_test" in kinds

    doc_after = (await auth_client.get(f"/api/documents/{doc['id']}")).json()
    assert doc_after["status"] == "confirmed"

    # Confirming the same version twice is rejected.
    again = await auth_client.post(
        f"/api/extractions/{extraction['id']}/confirm",
        json=confirm_body(extraction["payload"]),
        headers=csrf(auth_client),
    )
    assert again.status_code == 409


async def test_duplicate_upload_points_to_existing(auth_client: httpx.AsyncClient):
    data = build_pdf(SCENARIOS[1])
    first = (await upload(auth_client, data)).json()
    dup = await upload(auth_client, data)
    assert dup.status_code == 409
    assert dup.json()["document_id"] == first["id"]
    await drain()


async def test_rejects_unsupported_files(auth_client: httpx.AsyncClient):
    resp = await upload(auth_client, b"just some text pretending to be a pdf", "notes.pdf")
    assert resp.status_code == 415
    assert "PDF, JPG, PNG" in resp.json()["detail"]


async def test_scans_without_llm_need_manual_review(auth_client: httpx.AsyncClient):
    resp = await upload(auth_client, build_scan_png(SCENARIOS[0]), "photo.png")
    assert resp.status_code == 202
    await drain()
    doc_id = resp.json()["id"]
    extraction = (await auth_client.get(f"/api/documents/{doc_id}/extraction")).json()
    assert extraction["method"] == "none"
    assert extraction["payload"]["medications"] == []
    assert extraction["payload"]["warnings"]

    preview = await auth_client.get(f"/api/documents/{doc_id}/pages/1/preview")
    assert preview.status_code == 200
    assert preview.headers["content-type"] == "image/png"


async def test_documents_are_private(auth_client: httpx.AsyncClient):
    doc = (await upload(auth_client, build_pdf(SCENARIOS[2]))).json()
    await drain()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=auth_client._transport.app), base_url=BASE_URL
    ) as other:
        await signup(other, email="mallory@example.com")
        assert (await other.get(f"/api/documents/{doc['id']}")).status_code == 404
        assert (await other.get(f"/api/documents/{doc['id']}/file")).status_code == 404
        assert (await other.get(f"/api/documents/{doc['id']}/extraction")).status_code == 404
        listing = (await other.get("/api/documents")).json()
        assert listing["items"] == []


async def test_reprocess_versions_and_discard(auth_client: httpx.AsyncClient):
    doc = (await upload(auth_client, build_pdf(SCENARIOS[0]))).json()
    await drain()
    v1 = (await auth_client.get(f"/api/documents/{doc['id']}/extraction")).json()

    resp = await auth_client.post(
        f"/api/documents/{doc['id']}/reprocess", headers=csrf(auth_client)
    )
    assert resp.status_code == 202
    await drain()
    v2 = (await auth_client.get(f"/api/documents/{doc['id']}/extraction")).json()
    assert v2["version"] == v1["version"] + 1

    stale = await auth_client.post(
        f"/api/extractions/{v1['id']}/confirm",
        json=confirm_body(v1["payload"]),
        headers=csrf(auth_client),
    )
    assert stale.status_code == 409

    discarded = await auth_client.post(
        f"/api/extractions/{v2['id']}/discard", headers=csrf(auth_client)
    )
    assert discarded.status_code == 200
    doc_after = (await auth_client.get(f"/api/documents/{doc['id']}")).json()
    assert doc_after["status"] == "failed"
    assert "discarded" in doc_after["error"]


async def test_delete_document_cascades(auth_client: httpx.AsyncClient):
    doc = (await upload(auth_client, build_pdf(SCENARIOS[0]))).json()
    await drain()
    ex = (await auth_client.get(f"/api/documents/{doc['id']}/extraction")).json()
    await auth_client.post(
        f"/api/extractions/{ex['id']}/confirm",
        json=confirm_body(ex["payload"]),
        headers=csrf(auth_client),
    )
    resp = await auth_client.delete(f"/api/documents/{doc['id']}", headers=csrf(auth_client))
    assert resp.status_code == 204
    assert (await auth_client.get("/api/medications")).json() == []
    assert (await auth_client.get("/api/prescriptions")).json() == []


async def test_medication_and_task_updates(auth_client: httpx.AsyncClient):
    doc = (await upload(auth_client, build_pdf(SCENARIOS[1]))).json()
    await drain()
    ex = (await auth_client.get(f"/api/documents/{doc['id']}/extraction")).json()
    await auth_client.post(
        f"/api/extractions/{ex['id']}/confirm",
        json=confirm_body(ex["payload"]),
        headers=csrf(auth_client),
    )
    meds = (await auth_client.get("/api/medications?status=active")).json()
    metformin = next(m for m in meds if m["name"] == "Metformin")
    assert metformin["day_of_course"] >= 1

    new_sched = {**metformin["schedule"], "times": ["07:30", "19:30"]}
    upd = await auth_client.patch(
        f"/api/medications/{metformin['id']}",
        json={"schedule": new_sched},
        headers=csrf(auth_client),
    )
    assert upd.json()["schedule"]["times"] == ["07:30", "19:30"]

    stopped = await auth_client.patch(
        f"/api/medications/{metformin['id']}", json={"stopped": True}, headers=csrf(auth_client)
    )
    assert stopped.json()["status"] == "stopped"

    tasks = (await auth_client.get("/api/care-actions?open_only=true")).json()
    done = await auth_client.patch(
        f"/api/care-actions/{tasks[0]['id']}", json={"completed": True}, headers=csrf(auth_client)
    )
    assert done.json()["completed_at"] is not None
    remaining = (await auth_client.get("/api/care-actions?open_only=true")).json()
    assert len(remaining) == len(tasks) - 1
