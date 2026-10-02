"""Dose tracking: taken/skipped logs per scheduled dose, history that never assumes a miss."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import httpx

from app.modules.demo.samples import SCENARIOS, build_pdf
from app.shared.queue import drain
from tests.conftest import BASE_URL, csrf
from tests.test_assistant import ask, new_thread
from tests.test_documents_flow import confirm_body, upload


def _today():
    return datetime.now(UTC).date()  # test users live in UTC


async def _medicine(client: httpx.AsyncClient, days_ago: int = 6) -> dict:
    """Confirm a prescription with one twice-daily medicine that started `days_ago` days ago."""
    doc = (await upload(client, build_pdf(SCENARIOS[0]))).json()
    await drain()
    ex = (await client.get(f"/api/documents/{doc['id']}/extraction")).json()
    body = confirm_body(ex["payload"])
    start = (_today() - timedelta(days=days_ago)).isoformat()
    body["issued_on"] = start
    body["care_actions"] = []
    body["medications"] = [
        {
            "name": "Testamol",
            "strength": "250 mg",
            "form": "tablet",
            "dose": None,
            "route": None,
            "frequency_raw": "1-0-1",
            "schedule": {"times": ["08:00", "20:00"], "period": "daily", "label": "Twice daily"},
            "start_date": start,
            "duration_days": None,
            "instructions": None,
            "source_page": 1,
        }
    ]
    resp = await client.post(
        f"/api/extractions/{ex['id']}/confirm", json=body, headers=csrf(client)
    )
    assert resp.status_code == 200, resp.text
    meds = (await client.get("/api/medications")).json()
    return next(m for m in meds if m["name"] == "Testamol")


async def log(client, med_id, day, time, status="taken") -> httpx.Response:
    return await client.put(
        "/api/doses",
        json={"medication_id": med_id, "date": str(day), "time": time, "status": status},
        headers=csrf(client),
    )


async def test_logging_shows_on_the_dashboard(auth_client: httpx.AsyncClient):
    med = await _medicine(auth_client)
    today = _today()

    resp = await log(auth_client, med["id"], today, "08:00")
    assert resp.status_code == 200, resp.text
    assert resp.json()["status"] == "taken"

    def status_of(dash, time):
        return next(
            d["status"]
            for d in dash["doses_today"]
            if d["medication_id"] == med["id"] and d["time"] == time
        )

    dash = (await auth_client.get("/api/dashboard")).json()
    assert status_of(dash, "08:00") == "taken"
    assert status_of(dash, "20:00") is None

    # Changing your mind overwrites; clearing removes the mark.
    assert (await log(auth_client, med["id"], today, "08:00", "skipped")).status_code == 200
    dash = (await auth_client.get("/api/dashboard")).json()
    assert status_of(dash, "08:00") == "skipped"
    resp = await auth_client.delete(
        "/api/doses",
        params={"medication_id": med["id"], "date": str(today), "time": "08:00"},
        headers=csrf(auth_client),
    )
    assert resp.status_code == 204
    dash = (await auth_client.get("/api/dashboard")).json()
    assert status_of(dash, "08:00") is None


async def test_only_scheduled_past_or_current_doses_can_be_logged(
    auth_client: httpx.AsyncClient,
):
    med = await _medicine(auth_client, days_ago=2)
    today = _today()
    assert (await log(auth_client, med["id"], today, "13:00")).status_code == 422
    assert (
        await log(auth_client, med["id"], today + timedelta(days=1), "08:00")
    ).status_code == 422
    before_start = today - timedelta(days=5)
    assert (await log(auth_client, med["id"], before_start, "08:00")).status_code == 422
    assert (await log(auth_client, med["id"], today, "8am")).status_code == 422
    unknown = "00000000-0000-0000-0000-000000000000"
    assert (await log(auth_client, unknown, today, "08:00")).status_code == 404
    # The evening dose can be marked early on the same day.
    assert (await log(auth_client, med["id"], today, "20:00")).status_code == 200


async def test_history_counts_without_assuming_misses(auth_client: httpx.AsyncClient):
    med = await _medicine(auth_client, days_ago=6)
    today = _today()
    days_ago = [today - timedelta(days=n) for n in range(6, 0, -1)]  # six full past days
    for day in days_ago[:4]:
        await log(auth_client, med["id"], day, "08:00")
        await log(auth_client, med["id"], day, "20:00")
    await log(auth_client, med["id"], days_ago[4], "08:00", "skipped")  # one skipped, one unlogged

    out = (await auth_client.get(f"/api/adherence/{med['id']}", params={"days": 14})).json()
    entry = out["medications"][0]
    now_hm = datetime.now(UTC).strftime("%H:%M")
    due_today = sum(t <= now_hm for t in ("08:00", "20:00"))
    assert entry["counts"] == {
        "due": 12 + due_today,
        "taken": 8,
        "skipped": 1,
        "unlogged": 3 + due_today,
    }
    assert entry["taken_rate"] == round(8 / (12 + due_today), 3)
    # The window starts at the medicine's first day; days come oldest first.
    assert entry["days"][0]["date"] == str(days_ago[0])
    assert [s["state"] for s in entry["days"][4]["doses"]] == ["skipped", "unlogged"]
    states_today = {s["state"] for s in entry["days"][-1]["doses"]}
    assert states_today <= {"unlogged", "upcoming"}
    assert entry["streak_days"] == 0  # the last two past days were not fully taken

    # Fill in the gaps: the streak runs back to the first gap.
    await log(auth_client, med["id"], days_ago[4], "08:00")
    await log(auth_client, med["id"], days_ago[4], "20:00")
    await log(auth_client, med["id"], days_ago[5], "08:00")
    await log(auth_client, med["id"], days_ago[5], "20:00")
    out = (await auth_client.get(f"/api/adherence/{med['id']}")).json()
    assert out["medications"][0]["streak_days"] == 6


async def test_stopping_keeps_history_but_ends_the_schedule(auth_client: httpx.AsyncClient):
    med = await _medicine(auth_client, days_ago=3)
    yesterday = _today() - timedelta(days=1)
    await log(auth_client, med["id"], yesterday, "08:00")
    resp = await auth_client.patch(
        f"/api/medications/{med['id']}", json={"stopped": True}, headers=csrf(auth_client)
    )
    assert resp.status_code == 200
    out = (await auth_client.get(f"/api/adherence/{med['id']}")).json()
    entry = out["medications"][0]
    assert entry["status"] == "stopped"
    assert entry["counts"]["due"] == 6  # three full days before today's stop
    assert entry["days"][-1]["date"] == str(yesterday)
    assert (await log(auth_client, med["id"], _today(), "20:00")).status_code == 422


async def test_dose_logs_are_private(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    med = next(m for m in (await client.get("/api/medications")).json() if not m["as_needed"])
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=client._transport.app), base_url=BASE_URL
    ) as other:
        await other.post(
            "/api/auth/signup",
            json={"email": "eve@example.com", "password": "long-enough-pass", "display_name": "E"},
        )
        time = med["schedule"]["times"][0]
        assert (await log(other, med["id"], _today(), time)).status_code == 404
        assert (await other.get(f"/api/adherence/{med['id']}")).status_code == 404
        assert (await other.get("/api/adherence")).json()["medications"] == []


async def test_demo_history_and_ask(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    dash = (await client.get("/api/dashboard")).json()
    assert all(d["status"] is None for d in dash["doses_today"])  # today is left to the visitor

    out = (await client.get("/api/adherence", params={"days": 28})).json()
    assert out["medications"]
    c = out["counts"]
    assert c["due"] == c["taken"] + c["skipped"] + c["unlogged"] > 0
    assert 0.7 < out["taken_rate"] < 1
    # As-needed medicines have no schedule, so there is nothing to track.
    as_needed = {m["id"] for m in (await client.get("/api/medications")).json() if m["as_needed"]}
    assert as_needed and not as_needed & {m["medication_id"] for m in out["medications"]}

    export = (await client.get("/api/me/export")).json()
    assert len(export["dose_log"]) == c["taken"] + c["skipped"]

    thread = await new_thread(client)
    res = await ask(client, thread, "Did I miss any doses this week?")
    assert any(s["title"].endswith("dose log") for s in res["sources"])
    assert "scheduled doses in the last 14 days marked taken" in res["answer"]
    res = await ask(client, thread, "What should I do if I missed a dose?")
    assert res["answer"].startswith("I can't give medical advice")
