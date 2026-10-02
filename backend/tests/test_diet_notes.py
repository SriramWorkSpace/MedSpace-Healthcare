"""Diet notes from your care team: extracted, reviewed, confirmed, never invented."""

from __future__ import annotations

import httpx
import pytest

from app.modules.demo.samples import SCENARIOS, build_pdf
from app.modules.extraction.heuristic import _diet_notes, diet_category
from app.shared.queue import drain
from tests.conftest import BASE_URL, csrf
from tests.test_assistant import ask, new_thread
from tests.test_documents_flow import confirm_body, upload


@pytest.mark.parametrize(
    ("text", "category"),
    [
        ("Avoid alcohol while on antibiotics", "avoid"),
        ("Low salt diet", "limit"),
        ("Reduce sugar", "limit"),
        ("Drink plenty of fluids", "include"),
        ("Include more vegetables", "include"),
        ("Diet as tolerated", "general"),
    ],
)
def test_diet_categories(text, category):
    assert diet_category(text) == category


def test_advice_lines_split_into_separate_notes():
    notes = _diet_notes("Diet: Low salt, low sugar diet. Avoid sugary drinks. Walk daily.", 2)
    assert [n.text for n in notes] == ["Low salt, low sugar diet.", "Avoid sugary drinks."]
    assert all(n.source_page == 2 for n in notes)


async def test_review_then_confirm_creates_notes(auth_client: httpx.AsyncClient):
    doc = (await upload(auth_client, build_pdf(SCENARIOS[1]))).json()
    await drain()
    ex = (await auth_client.get(f"/api/documents/{doc['id']}/extraction")).json()
    texts = [n["text"] for n in ex["payload"]["diet_notes"]]
    assert "Avoid sugary drinks." in texts

    body = confirm_body(ex["payload"])
    body["diet_notes"] = [
        {"text": n["text"], "category": n["category"], "source_page": n["source_page"]}
        for n in ex["payload"]["diet_notes"]
        if "vegetables" not in n["text"]  # the reviewer removes one
    ] + [{"text": "Limit coffee to one cup a day.", "category": "limit", "source_page": 1}]
    resp = await auth_client.post(
        f"/api/extractions/{ex['id']}/confirm", json=body, headers=csrf(auth_client)
    )
    assert resp.status_code == 200, resp.text

    diet = (await auth_client.get("/api/diet-notes")).json()
    texts = {n["text"] for n in diet["notes"]}
    assert "Limit coffee to one cup a day." in texts
    assert not any("vegetables" in t for t in texts)
    note = next(n for n in diet["notes"] if n["text"] == "Avoid sugary drinks.")
    assert note["category"] == "avoid"
    assert note["prescriber_name"] == "Dr. Tomas Varga"

    # Food rules attached to current medicines ("after meals", "with milk") come along too.
    foods = {(m["name"], m["text"]) for m in diet["medication_notes"]}
    assert ("Metformin", "After meals") in foods
    assert ("Cholecalciferol", "With milk") in foods

    # The prescription report carries the notes for its document.
    rx = (await auth_client.get(f"/api/prescriptions/{resp.json()['prescription_id']}")).json()
    assert len(rx["diet_notes"]) == len(body["diet_notes"])


async def test_reconfirming_replaces_notes_and_delete_works(auth_client: httpx.AsyncClient):
    doc = (await upload(auth_client, build_pdf(SCENARIOS[0]))).json()
    await drain()
    ex = (await auth_client.get(f"/api/documents/{doc['id']}/extraction")).json()
    await auth_client.post(
        f"/api/extractions/{ex['id']}/confirm",
        json=confirm_body(ex["payload"]) | {"diet_notes": []},
        headers=csrf(auth_client),
    )
    assert (await auth_client.get("/api/diet-notes")).json()["notes"] == []

    await auth_client.post(f"/api/documents/{doc['id']}/reprocess", headers=csrf(auth_client))
    await drain()
    ex2 = (await auth_client.get(f"/api/documents/{doc['id']}/extraction")).json()
    body = confirm_body(ex2["payload"])
    body["diet_notes"] = [
        {"text": n["text"], "category": n["category"], "source_page": n["source_page"]}
        for n in ex2["payload"]["diet_notes"]
    ]
    await auth_client.post(
        f"/api/extractions/{ex2['id']}/confirm", json=body, headers=csrf(auth_client)
    )
    notes = (await auth_client.get("/api/diet-notes")).json()["notes"]
    assert len(notes) == 2

    gone = await auth_client.delete(f"/api/diet-notes/{notes[0]['id']}", headers=csrf(auth_client))
    assert gone.status_code == 204
    assert len((await auth_client.get("/api/diet-notes")).json()["notes"]) == 1


async def test_demo_has_diet_notes_and_they_are_private(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    diet = (await client.get("/api/diet-notes")).json()
    assert len(diet["notes"]) >= 5
    assert {n["category"] for n in diet["notes"]} >= {"avoid", "limit", "include"}

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=client._transport.app), base_url=BASE_URL
    ) as other:
        await other.post("/api/auth/demo")
        mine = {n["id"] for n in diet["notes"]}
        theirs = {n["id"] for n in (await other.get("/api/diet-notes")).json()["notes"]}
        assert not mine & theirs
        victim = next(iter(mine))
        resp = await other.delete(f"/api/diet-notes/{victim}", headers=csrf(other))
        assert resp.status_code == 404


async def test_ask_medspace_answers_diet_questions_from_notes(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    tid = await new_thread(client)
    result = await ask(client, tid, "What did my doctors say about food and drinks?")
    titles = [s["title"] for s in result["sources"]]
    assert any(t.startswith("Diet note") for t in titles)
    assert "Avoid alcohol while on antibiotics." in result["answer"]
    assert "[" in result["answer"]  # cited
