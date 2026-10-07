from __future__ import annotations

import httpx

from app.shared.queue import drain
from tests.conftest import BASE_URL


async def search(client: httpx.AsyncClient, q: str) -> dict:
    resp = await client.get("/api/search", params={"q": q})
    assert resp.status_code == 200, resp.text
    return resp.json()


async def test_partial_names_find_medications(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    res = await search(client, "amox")
    meds = res["groups"]["medications"]
    assert meds[0]["title"] == "Amoxicillin 500 mg"
    assert meds[0]["href"].startswith("/app/medications?focus=")
    assert "Twice daily" in meds[0]["subtitle"]


async def test_prescribers_and_clinics(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    res = await search(client, "varga")
    rx = res["groups"]["prescriptions"]
    assert rx[0]["title"] == "Prescription from Dr. Tomas Varga"
    assert rx[0]["href"].startswith("/app/prescriptions/")


async def test_document_text_matches_with_snippets(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    await drain()  # demo documents are indexed in the background after sign-in
    res = await search(client, "triglycerides")
    docs = res["groups"]["documents"]
    assert docs and docs[0]["title"] == "Lipid profile results"
    assert "<<Triglycerides>>" in docs[0]["snippet"]
    assert "?page=1" in docs[0]["href"]


async def test_to_dos_and_diet_notes(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    assert (await search(client, "cbc"))["groups"]["to_dos"][0]["title"] == "Get CBC test"
    diet = (await search(client, "alcohol"))["groups"]["diet_notes"]
    assert diet[0]["title"] == "Avoid alcohol while on antibiotics."


async def test_no_matches_and_validation(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    res = await search(client, "zzzz-no-such-thing")
    assert res == {"query": "zzzz-no-such-thing", "groups": {}, "total": 0}
    assert (await client.get("/api/search", params={"q": "a"})).status_code == 422
    # LIKE wildcards are matched literally, not as patterns.
    assert (await search(client, "%%"))["total"] == 0


async def test_search_is_private(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=client._transport.app), base_url=BASE_URL
    ) as other:
        await other.post(
            "/api/auth/signup",
            json={
                "email": "eve@example.com",
                "password": "long-enough-pass",
                "display_name": "Eve",
            },
        )
        assert (await search(other, "amox"))["total"] == 0
        assert (await search(other, "triglycerides"))["total"] == 0


async def test_search_requires_auth(client: httpx.AsyncClient):
    assert (await client.get("/api/search", params={"q": "amox"})).status_code == 401
