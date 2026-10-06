"""Every route that takes an ID refuses another account's IDs, and leaves that data untouched.

A demo account (Ada, plenty of data) owns everything; a separate account (Bo) tries every
ID-taking route with Ada's real IDs and valid bodies. Nothing may succeed, and Ada's records must
be byte-for-byte the same afterwards. The route list is checked against the API schema, so a new
ID route without a case here fails the test instead of slipping through.
"""

from __future__ import annotations

import httpx

from app.main import app
from app.shared.queue import drain
from tests.conftest import BASE_URL, csrf, signup

SKIP = {
    # Token routes: the token is the credential (tested in their own suites), not an owned ID.
    ("GET", "/api/circle/invites/{token}"),
}


async def owner_ids(ada: httpx.AsyncClient) -> dict[str, str]:
    get = lambda path: ada.get(path)  # noqa: E731
    docs = (await get("/api/documents")).json()["items"]
    draft = next(d for d in docs if d["status"] == "needs_review")
    confirmed = next(d for d in docs if d["status"] == "confirmed")
    extraction = (await get(f"/api/documents/{draft['id']}/extraction")).json()
    meds = (await get("/api/medications")).json()
    actions = (await get("/api/care-actions")).json()
    notes = (await get("/api/diet-notes")).json()["notes"]
    labs = (await get("/api/labs")).json()
    lab = (await get(f"/api/labs/{labs[0]['key']}")).json()
    rx = (await get("/api/prescriptions")).json()
    visits = (await get("/api/visits")).json()
    circle = (await get("/api/circle")).json()
    session_id = (await get("/api/me/security")).json()["sessions"][0]["id"]
    share = await ada.post(
        "/api/shares",
        json={"label": "Doctor", "items": [{"type": "prescription", "id": rx[0]["id"]}]},
        headers=csrf(ada),
    )
    thread = await ada.post("/api/assistant/threads", json={}, headers=csrf(ada))
    return {
        "doc_id": confirmed["id"],
        "draft_doc_id": draft["id"],
        "extraction_id": extraction["id"],
        "medication_id": meds[0]["id"],
        "med_id": meds[0]["id"],
        "action_id": actions[0]["id"],
        "note_id": notes[0]["id"],
        "result_id": lab["results"][0]["id"],
        "key": labs[0]["key"],
        "prescription_id": rx[0]["id"],
        "prep_id": visits[0]["id"],
        "link_id": circle["caring_for"][0]["id"],
        "share_id": share.json()["share"]["id"],
        "thread_id": thread.json()["id"],
        "session_id": session_id,
        "page_no": "1",
    }


BODIES = {
    ("PATCH", "/api/documents/{doc_id}"): {"title": "Taken over"},
    ("POST", "/api/extractions/{extraction_id}/confirm"): {
        "document_kind": "prescription",
        "medications": [],
        "care_actions": [],
    },
    ("PATCH", "/api/medications/{med_id}"): {"stopped": True},
    ("PATCH", "/api/care-actions/{action_id}"): {"completed": True},
    ("PATCH", "/api/visits/{prep_id}"): {"title": "Taken over"},
    ("PUT", "/api/supply/{medication_id}"): {"on_hand": 1},
    ("POST", "/api/supply/{medication_id}/refill"): {"added": 5},
    ("PATCH", "/api/circle/{link_id}"): {"role": "helper"},
    ("PUT", "/api/circle/{link_id}/alerts"): {"minutes": 0},
    ("POST", "/api/assistant/threads/{thread_id}/messages"): {"content": "What do I take?"},
}


def fill(path: str, ids: dict[str, str]) -> str:
    out = path
    for name, value in ids.items():
        out = out.replace("{" + name + "}", value)
    if "/extractions/" in path:  # a draft can still be confirmed or discarded
        out = out.replace(ids["extraction_id"], ids["extraction_id"])
    if path == "/api/shares/{link_id}":
        out = path.replace("{link_id}", ids["share_id"])
    return out


async def snapshot(ada: httpx.AsyncClient, ids: dict[str, str]) -> dict:
    paths = [
        "/api/documents",
        f"/api/documents/{ids['doc_id']}",
        f"/api/documents/{ids['draft_doc_id']}/extraction",
        "/api/medications",
        "/api/care-actions",
        "/api/diet-notes",
        f"/api/labs/{ids['key']}",
        "/api/visits",
        f"/api/visits/{ids['prep_id']}",
        "/api/shares",
        "/api/supply",
        "/api/circle",
        f"/api/assistant/threads/{ids['thread_id']}",
    ]
    out = {}
    for p in paths:
        resp = await ada.get(p)
        assert resp.status_code == 200, (p, resp.status_code)  # the owner can read all of it
        out[p] = resp.json()
    return out


async def test_no_route_accepts_another_accounts_ids(client: httpx.AsyncClient):
    ada = client
    await ada.post("/api/auth/demo")
    await drain()
    ids = await owner_ids(ada)
    before = await snapshot(ada, ids)

    spec = app.openapi()
    routes = sorted(
        (method.upper(), path)
        for path, ops in spec["paths"].items()
        for method in ops
        if "{" in path and not path.startswith(("/api/public", "/api/dev"))
    )
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL) as bo:
        await signup(bo, email="bo@example.com", name="Bo")
        attempts = []
        for method, path in routes:
            if (method, path) in SKIP:
                continue
            url = fill(path, ids)
            assert "{" not in url, f"no ID for {path}: add one to owner_ids()"
            resp = await bo.request(method, url, json=BODIES.get((method, path)), headers=csrf(bo))
            attempts.append((method, path, resp.status_code))
        allowed = [a for a in attempts if a[2] < 400 or a[2] == 422]
        assert not allowed, (
            f"another account's IDs were accepted (or body rejected first): {allowed}"
        )
        assert all(code in (403, 404) for _, _, code in attempts), attempts
        assert len(attempts) == len(routes) - len(SKIP)

    after = await snapshot(ada, ids)
    assert after == before
