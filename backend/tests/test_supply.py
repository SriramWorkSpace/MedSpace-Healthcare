"""Medication supply: estimates from the user's own count, the schedule and skipped marks."""

from __future__ import annotations

import uuid
from datetime import UTC, date, datetime, timedelta

import httpx

from app.modules.identity.models import User
from app.modules.records.models import Medication
from app.modules.supply.models import MedicationSupply
from app.modules.supply.service import estimate
from tests.conftest import BASE_URL, csrf
from tests.test_assistant import ask, new_thread

D = date(2026, 3, 2)
USER = User(timezone="UTC")


def _med(**kw) -> Medication:
    base = {
        "id": uuid.uuid4(),
        "name": "Testamol",
        "strength": "250 mg",
        "start_date": D - timedelta(days=30),
        "end_date": None,
        "schedule": {"times": ["08:00", "20:00"], "period": "daily"},
        "as_needed": False,
        "stopped_at": None,
    }
    return Medication(**{**base, **kw})


def _count(units: float, per: float = 1, at: datetime | None = None) -> MedicationSupply:
    return MedicationSupply(
        on_hand=units,
        unit="tablets",
        units_per_dose=per,
        low_days=7,
        counted_at=at or datetime(D.year, D.month, D.day, 7, 0, tzinfo=UTC),
    )


def _now(days: int, hour: int) -> datetime:
    return datetime(D.year, D.month, D.day, hour, 0, tzinfo=UTC) + timedelta(days=days)


def test_counts_scheduled_doses_since_the_count():
    out = estimate(_med(), _count(10), USER, set(), _now(2, 12))
    # Five doses since the 7 AM count: D 08/20, D+1 08/20, D+2 08.
    assert out.estimated_left == 5 and out.doses_left == 5
    # Remaining doses: D+2 20, D+3 08/20, D+4 08/20; the D+5 08:00 dose can't be covered.
    assert out.runs_out_on == D + timedelta(days=5)
    assert out.status == "low"


def test_skipped_doses_are_not_subtracted():
    out = estimate(_med(), _count(10), USER, {(D, "20:00")}, _now(2, 12))
    assert out.estimated_left == 6


def test_multi_unit_doses_and_running_out():
    out = estimate(_med(), _count(10, per=2), USER, set(), _now(2, 12))
    assert out.estimated_left == 0 and out.doses_left == 0
    assert out.status == "out" and out.runs_out_on == D + timedelta(days=2)


def test_enough_for_the_rest_of_the_course():
    med = _med(end_date=D + timedelta(days=3))
    out = estimate(med, _count(20), USER, set(), _now(1, 9))
    assert out.status == "course_covered" and out.runs_out_on is None


def test_plenty_left_is_ok_and_as_needed_has_no_run_out_date():
    assert estimate(_med(), _count(200), USER, set(), _now(1, 9)).status == "ok"
    prn = estimate(_med(as_needed=True), _count(12), USER, set(), _now(1, 9))
    assert prn.status == "as_needed" and prn.runs_out_on is None and prn.estimated_left == 12


async def test_count_refill_and_clear(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    meds = (await client.get("/api/medications")).json()
    cetirizine = next(m for m in meds if m["name"] == "Cetirizine")
    url = f"/api/supply/{cetirizine['id']}"

    bad = await client.put(url, json={"on_hand": -1}, headers=csrf(client))
    assert bad.status_code == 422
    early = await client.post(f"{url}/refill", json={"added": 10}, headers=csrf(client))
    assert early.status_code == 422  # count first

    resp = await client.put(
        url, json={"on_hand": 3, "unit": " Tablets ", "low_days": 5}, headers=csrf(client)
    )
    assert resp.status_code == 200, resp.text
    first = resp.json()
    assert first["unit"] == "tablets" and first["counted"] == 3

    refill = (await client.post(f"{url}/refill", json={"added": 10}, headers=csrf(client))).json()
    assert refill["counted"] == first["estimated_left"] + 10

    listed = {s["medication_id"] for s in (await client.get("/api/supply")).json()}
    assert cetirizine["id"] in listed
    assert (await client.delete(url, headers=csrf(client))).status_code == 204
    assert (await client.delete(url, headers=csrf(client))).status_code == 404


async def test_supplies_are_private(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    med = (await client.get("/api/medications")).json()[0]
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=client._transport.app), base_url=BASE_URL
    ) as other:
        await other.post(
            "/api/auth/signup",
            json={"email": "eve@example.com", "password": "long-enough-pass", "display_name": "E"},
        )
        resp = await other.put(f"/api/supply/{med['id']}", json={"on_hand": 5}, headers=csrf(other))
        assert resp.status_code == 404
        assert (await other.get("/api/supply")).json() == []


async def test_demo_running_low_everywhere(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    supplies = {s["name"]: s for s in (await client.get("/api/supply")).json()}
    assert supplies["Metformin"]["status"] in ("low", "out")
    assert supplies["Atorvastatin"]["status"] == "ok"
    assert supplies["Amoxicillin"]["status"] == "course_covered"

    dash = (await client.get("/api/dashboard")).json()
    assert [s["name"] for s in dash["running_low"]] == ["Metformin"]

    prep = (await client.get("/api/visits")).json()[0]
    brief = (await client.get(f"/api/visits/{prep['id']}/brief")).json()
    assert any(
        p["key"].startswith("supply:") and "Metformin" in p["text"] for p in brief["prompts"]
    )

    thread = await new_thread(client)
    res = await ask(client, thread, "When will my Metformin run out?")
    assert "Metformin supply" in [s["title"] for s in res["sources"]]
    assert "(estimate)" in res["answer"]
    res = await ask(client, thread, "What's left on my to-do list?")
    assert not any(s["title"].endswith(" supply") for s in res["sources"])
