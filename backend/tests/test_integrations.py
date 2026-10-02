"""Google Calendar/Tasks sync against the in-memory simulation (GOOGLE_PROVIDER=fake)."""

from __future__ import annotations

from datetime import date

import httpx
from sqlalchemy import select

from app.core.security import decrypt
from app.modules.integrations.google import FakeGoogleClient
from app.modules.integrations.models import OAuthConnection
from app.modules.integrations.service import dose_event
from tests.conftest import csrf


async def connect(client: httpx.AsyncClient) -> None:
    start = await client.get("/api/integrations/google/connect", follow_redirects=False)
    assert start.status_code == 302
    location = start.headers["location"]
    assert "state=" in location
    callback = await client.get(location, follow_redirects=False)
    assert callback.status_code in (302, 307)
    assert "google=connected" in callback.headers["location"]


async def first_prescription(client: httpx.AsyncClient) -> dict:
    rx_list = (await client.get("/api/prescriptions")).json()
    return next(r for r in rx_list if r["prescriber_name"] == "Dr. Imani Oduya")


def bucket_for(token: str) -> dict:
    return FakeGoogleClient.store[token.removeprefix("sim-access-")]


async def test_connect_flow_stores_encrypted_tokens(client: httpx.AsyncClient, session):
    await client.post("/api/auth/demo")
    status = (await client.get("/api/integrations/google/status")).json()
    assert status == {**status, "connected": False, "mode": "simulation"}

    await connect(client)
    status = (await client.get("/api/integrations/google/status")).json()
    assert status["connected"] is True
    assert status["email"].endswith("@gmail.simulated")

    conn = await session.scalar(select(OAuthConnection))
    assert not conn.access_token_enc.startswith("sim-")  # stored encrypted
    assert decrypt(conn.access_token_enc).startswith("sim-access-")


async def test_callback_rejects_forged_state(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    start = await client.get("/api/integrations/google/connect", follow_redirects=False)
    forged = start.headers["location"].replace("state=", "state=x")
    resp = await client.get(forged, follow_redirects=False)
    assert "google=error" in resp.headers["location"]


async def test_sync_is_idempotent_and_reversible(client: httpx.AsyncClient, session):
    await client.post("/api/auth/demo")
    await connect(client)
    rx = await first_prescription(client)

    preview = (
        await client.get(f"/api/integrations/google/preview?prescription_id={rx['id']}")
    ).json()
    summaries = [e["summary"] for e in preview["events"]]
    # Amoxicillin twice daily, Cetirizine at bedtime, a follow-up. PRN Ibuprofen never syncs.
    assert summaries.count("Take Amoxicillin 500 mg") == 2
    assert not any("Ibuprofen" in s for s in summaries)
    assert any(s.startswith("Follow-up with Dr. Imani Oduya") for s in summaries)
    assert not any(t["summary"].startswith("Follow-up") for t in preview["tasks"])

    body = {"prescription_id": rx["id"], "calendar": True, "tasks": True}
    first = (
        await client.post("/api/integrations/google/sync", json=body, headers=csrf(client))
    ).json()
    assert first["events"] == len(preview["events"]) and first["tasks"] == len(preview["tasks"])

    conn = await session.scalar(select(OAuthConnection))
    remote = bucket_for(decrypt(conn.access_token_enc))
    assert len(remote["events"]) == first["events"]
    assert next(iter(remote["lists"].values()))["title"] == "MedSpace"

    # Re-sync updates in place: no duplicates.
    await client.post("/api/integrations/google/sync", json=body, headers=csrf(client))
    assert len(remote["events"]) == first["events"]

    synced = (
        await client.get(f"/api/integrations/google/preview?prescription_id={rx['id']}")
    ).json()
    assert all(e["synced"] for e in synced["events"])

    removed = await client.delete(
        f"/api/integrations/google/sync?prescription_id={rx['id']}", headers=csrf(client)
    )
    assert removed.json()["removed"] == first["events"] + first["tasks"]
    assert remote["events"] == {}


async def test_completed_tasks_flow_back(client: httpx.AsyncClient, session):
    await client.post("/api/auth/demo")
    await connect(client)
    rx = await first_prescription(client)
    await client.post(
        "/api/integrations/google/sync",
        json={"prescription_id": rx["id"], "calendar": False, "tasks": True},
        headers=csrf(client),
    )
    conn = await session.scalar(select(OAuthConnection))
    remote = bucket_for(decrypt(conn.access_token_enc))
    for task in remote["tasks"].values():
        task["status"] = "completed"  # the user ticks them off in Google Tasks
    pulled = (await client.post("/api/integrations/google/pull", headers=csrf(client))).json()
    assert pulled["updated"] == len(remote["tasks"])


async def test_sync_requires_connection(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    rx = await first_prescription(client)
    resp = await client.post(
        "/api/integrations/google/sync", json={"prescription_id": rx["id"]}, headers=csrf(client)
    )
    assert resp.status_code == 409


async def test_disconnect_removes_connection_and_links(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    await connect(client)
    rx = await first_prescription(client)
    await client.post(
        "/api/integrations/google/sync", json={"prescription_id": rx["id"]}, headers=csrf(client)
    )
    resp = await client.delete("/api/integrations/google?remove_items=true", headers=csrf(client))
    assert resp.status_code == 204
    assert (await client.get("/api/integrations/google/status")).json()["connected"] is False
    audit = (await client.get("/api/audit?action=integration.")).json()["items"]
    assert [a["action"] for a in audit][:3] == [
        "integration.disconnected",
        "integration.synced",
        "integration.connected",
    ]


def test_dose_event_shape():
    class Med:
        name, strength, dose, instructions = "Metformin", "500 mg", None, "after meals"
        start_date = date(2026, 3, 1)
        end_date = date(2026, 5, 29)
        schedule = {"period": "daily", "times": ["08:00"]}
        id = "x"

    body = dose_event(Med, "08:00", "America/New_York", "dose:x:08:00")
    assert body["start"] == {"dateTime": "2026-03-01T08:00:00", "timeZone": "America/New_York"}
    assert body["end"]["dateTime"] == "2026-03-01T08:15:00"
    assert body["recurrence"] == ["RRULE:FREQ=DAILY;UNTIL=20260529T235959Z"]
    assert "follow your prescriber" in body["description"]
