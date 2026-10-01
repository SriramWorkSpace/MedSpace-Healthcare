from __future__ import annotations

from pathlib import Path

import httpx

from app.core.config import get_settings
from app.shared.queue import drain
from tests.conftest import csrf


async def demo(client: httpx.AsyncClient) -> dict:
    resp = await client.post("/api/auth/demo")
    assert resp.status_code == 201, resp.text
    return resp.json()["user"]


async def test_demo_account_is_seeded_with_history(client: httpx.AsyncClient):
    await demo(client)
    docs = (await client.get("/api/documents")).json()
    assert docs["counts"]["confirmed"] == 4
    assert docs["counts"]["needs_review"] == 1

    prescriptions = (await client.get("/api/prescriptions")).json()
    assert len(prescriptions) == 3
    assert prescriptions[0]["prescriber_name"] == "Dr. Imani Oduya"  # most recent first

    meds = (await client.get("/api/medications")).json()
    statuses = {m["name"]: m["status"] for m in meds}
    assert statuses["Amoxicillin"] == "active"
    assert statuses["Doxycycline"] == "completed"


async def test_dashboard_shows_today(client: httpx.AsyncClient):
    await demo(client)
    dash = (await client.get("/api/dashboard")).json()
    names = {d["name"] for d in dash["doses_today"]}
    assert {"Amoxicillin", "Metformin"} <= names
    assert dash["doses_today"] == sorted(dash["doses_today"], key=lambda d: d["time"])
    assert any(a["name"] == "Ibuprofen" for a in dash["as_needed"])
    assert [r["title"] for r in dash["needs_review"]] == ["Rx lakeside urgent"]
    assert len(dash["week"]) == 7
    assert dash["stats"]["prescriptions"] == 3
    assert all(e["upcoming"] for e in dash["upcoming"])


async def test_timeline_orders_and_filters(client: httpx.AsyncClient):
    await demo(client)
    page = (await client.get("/api/timeline?limit=200")).json()
    dates = [e["date"] for e in page["items"]]
    assert dates == sorted(dates, reverse=True)
    types = {e["type"] for e in page["items"]}
    assert {"prescription", "appointment", "medication_start", "document", "task"} <= types

    only = (await client.get("/api/timeline?types=prescription&limit=200")).json()
    assert {e["type"] for e in only["items"]} == {"prescription"}
    assert len(only["items"]) == 3


async def test_timeline_pagination_never_splits_a_day(client: httpx.AsyncClient):
    await demo(client)
    first = (await client.get("/api/timeline?limit=5")).json()
    assert first["next_cursor"]
    second = (await client.get(f"/api/timeline?limit=5&before={first['next_cursor']}")).json()
    first_ids = {e["id"] for e in first["items"]}
    assert not first_ids & {e["id"] for e in second["items"]}
    assert all(e["date"] < first["next_cursor"] for e in second["items"])


async def test_deleting_account_removes_files(client: httpx.AsyncClient):
    user = await demo(client)
    await drain()
    root = Path(get_settings().storage_local_dir)
    user_dir = root / "users" / user["id"]
    assert user_dir.exists()
    resp = await client.delete("/api/me", headers=csrf(client))
    assert resp.status_code == 204
    assert not user_dir.exists()
