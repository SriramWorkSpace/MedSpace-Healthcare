"""Visit prep: the user's questions plus a live, factual brief built from confirmed records."""

from __future__ import annotations

from datetime import date, timedelta

import httpx

from tests.conftest import BASE_URL, csrf


async def _demo(client: httpx.AsyncClient) -> date:
    await client.post("/api/auth/demo")
    return date.fromisoformat((await client.get("/api/dashboard")).json()["today"])


async def _create(client: httpx.AsyncClient, **body) -> dict:
    resp = await client.post("/api/visits", json=body, headers=csrf(client))
    assert resp.status_code == 201, resp.text
    return resp.json()


async def test_create_edit_and_delete(client: httpx.AsyncClient):
    today = await _demo(client)
    prep = await _create(client, clinician="Dr. Tomas Varga", visit_date=str(today + timedelta(7)))
    assert prep["title"] == "Visit with Dr. Tomas Varga"
    assert prep["questions"] == [] and prep["since"] is None

    questions = [
        {"id": "q1", "text": "  Can I take the statin in the morning?  ", "done": False},
        {"id": "q2", "text": "Next lab test date", "done": True, "prompt_key": "todo:x"},
    ]
    resp = await client.patch(
        f"/api/visits/{prep['id']}", json={"questions": questions}, headers=csrf(client)
    )
    assert resp.status_code == 200, resp.text
    saved = resp.json()["questions"]
    assert saved[0]["text"] == "Can I take the statin in the morning?"
    assert saved[1]["done"] is True

    dup = [questions[0], {**questions[0], "text": "again"}]
    bad = await client.patch(
        f"/api/visits/{prep['id']}", json={"questions": dup}, headers=csrf(client)
    )
    assert bad.status_code == 422
    future = await client.patch(
        f"/api/visits/{prep['id']}", json={"since": str(today + timedelta(1))}, headers=csrf(client)
    )
    assert future.status_code == 422
    blank = await client.patch(
        f"/api/visits/{prep['id']}",
        json={"questions": [{"id": "q", "text": "   "}]},
        headers=csrf(client),
    )
    assert blank.status_code == 422

    listed = (await client.get("/api/visits")).json()
    assert prep["id"] in {v["id"] for v in listed}
    # The demo also comes with a prep for its next follow-up, questions already written.
    seeded = next(v for v in listed if v["id"] != prep["id"])
    assert seeded["title"].startswith("Visit with Dr.") and len(seeded["questions"]) == 2
    resp = await client.delete(f"/api/visits/{prep['id']}", headers=csrf(client))
    assert resp.status_code == 204
    assert (await client.get(f"/api/visits/{prep['id']}")).status_code == 404


async def test_brief_reports_records_since_a_date(client: httpx.AsyncClient):
    today = await _demo(client)
    prep = await _create(client, visit_date=str(today + timedelta(7)))
    brief = (await client.get(f"/api/visits/{prep['id']}/brief")).json()

    assert brief["since"] == str(today - timedelta(90)) and brief["until"] == str(today)
    names = {m["name"] for m in brief["medications"]}
    assert {"Amoxicillin", "Metformin"} <= names
    assert any(c["kind"] == "started" and c["name"] == "Amoxicillin" for c in brief["changes"])
    assert brief["doses"] and all(d["due"] >= d["taken"] for d in brief["doses"])
    labs = {lab["key"]: lab for lab in brief["labs"]}
    assert labs["ldl-cholesterol"]["value_text"] == "138"
    assert labs["ldl-cholesterol"]["previous_value_text"] == "149"
    # Only medicines with marks in the period are summarized; untracked ones would read as misses.
    assert all(d["taken"] + d["skipped"] > 0 for d in brief["doses"])
    assert "Doxycycline" not in {d["name"] for d in brief["doses"]}
    assert brief["todos"] and brief["appointments"]
    assert brief["diet_notes"]

    prompts = [p["text"] for p in brief["prompts"]]
    assert any(
        p.startswith("LDL cholesterol was above the range printed on the") and "(range < 130)" in p
        for p in prompts
    )
    # Observations only: nothing tells the user what to do or what a result means.
    for p in prompts:
        assert not any(w in p.lower() for w in ("should", "risk", "normal", "concern", "worry"))

    # A shorter window drops the older lipid panel but keeps the recent diabetes panel.
    await client.patch(
        f"/api/visits/{prep['id']}",
        json={"since": str(today - timedelta(30))},
        headers=csrf(client),
    )
    brief = (await client.get(f"/api/visits/{prep['id']}/brief")).json()
    keys = {lab["key"] for lab in brief["labs"]}
    assert "hba1c" in keys and "ldl-cholesterol" not in keys


async def test_default_window_starts_at_the_previous_visit(client: httpx.AsyncClient):
    today = await _demo(client)
    await _create(client, title="Last check-up", visit_date=str(today - timedelta(20)))
    prep = await _create(client, title="Next check-up", visit_date=str(today + timedelta(5)))
    brief = (await client.get(f"/api/visits/{prep['id']}/brief")).json()
    assert brief["since"] == str(today - timedelta(20))


async def test_a_brief_can_be_shared_and_stays_private(client: httpx.AsyncClient):
    today = await _demo(client)
    prep = await _create(client, clinician="Dr. Imani Oduya", visit_date=str(today + timedelta(3)))
    await client.patch(
        f"/api/visits/{prep['id']}",
        json={"questions": [{"id": "a", "text": "Is the cough worth an X-ray?"}]},
        headers=csrf(client),
    )
    resp = await client.post(
        "/api/shares",
        json={"label": "For Dr. Oduya", "items": [{"type": "visit", "id": prep["id"]}]},
        headers=csrf(client),
    )
    assert resp.status_code in (200, 201), resp.text
    created = resp.json()
    assert created["share"]["items"][0]["title"] == "Visit brief: Visit with Dr. Imani Oduya"

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=client._transport.app), base_url=BASE_URL
    ) as other:
        public = (await other.get(f"/api/public/shares/{created['token']}")).json()
        assert (
            public["visits"][0]["visit"]["questions"][0]["text"] == "Is the cough worth an X-ray?"
        )
        assert public["visits"][0]["medications"]

        await other.post(
            "/api/auth/signup",
            json={"email": "eve@example.com", "password": "long-enough-pass", "display_name": "E"},
        )
        assert (await other.get(f"/api/visits/{prep['id']}")).status_code == 404
        assert (await other.get(f"/api/visits/{prep['id']}/brief")).status_code == 404
        steal = await other.post(
            "/api/shares",
            json={"label": "x", "items": [{"type": "visit", "id": prep["id"]}]},
            headers=csrf(other),
        )
        assert steal.status_code == 422
