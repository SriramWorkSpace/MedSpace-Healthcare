"""Care circle: invitations bound to an email, role-limited access to someone else's records."""

from __future__ import annotations

from contextlib import asynccontextmanager

import httpx

from tests.conftest import BASE_URL, confirm_email, csrf


@asynccontextmanager
async def person(
    client: httpx.AsyncClient, email: str, name: str = "Eve Example", *, verified: bool = True
):
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=client._transport.app), base_url=BASE_URL
    ) as other:
        resp = await other.post(
            "/api/auth/signup",
            json={"email": email, "password": "long-enough-pass", "display_name": name},
        )
        assert resp.status_code in (200, 201), resp.text
        if verified:
            await confirm_email(other, email)
        yield other


async def _owner(client: httpx.AsyncClient) -> str:
    await client.post("/api/auth/demo")
    return (await client.get("/api/auth/session")).json()["user"]["id"]


async def _invite(client: httpx.AsyncClient, email: str, role: str = "viewer") -> dict:
    resp = await client.post(
        "/api/circle/invites", json={"email": email, "role": role}, headers=csrf(client)
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


def acting(owner_id: str, other: httpx.AsyncClient | None = None) -> dict:
    headers = {"X-Acting-For": owner_id}
    if other is not None:
        headers.update(csrf(other))
    return headers


async def test_invite_accept_and_read_as_viewer(client: httpx.AsyncClient):
    owner_id = await _owner(client)
    created = await _invite(client, "eve@example.com")
    assert created["url"].endswith(f"/app/circle/accept/{created['token']}")
    assert created["link"]["status"] == "pending"

    async with person(client, "eve@example.com") as eve:
        preview = (await eve.get(f"/api/circle/invites/{created['token']}")).json()
        assert preview["role"] == "viewer" and preview["status"] == "pending"
        resp = await eve.post(
            "/api/circle/accept", json={"token": created["token"]}, headers=csrf(eve)
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["status"] == "active"

        circle = (await eve.get("/api/circle")).json()
        assert [c["person"]["id"] for c in circle["caring_for"]] == [owner_id]

        # Reading the owner's records works; her own (empty) records are untouched.
        theirs = (await eve.get("/api/medications", headers=acting(owner_id))).json()
        mine = (await eve.get("/api/medications")).json()
        assert {m["name"] for m in theirs} >= {"Metformin", "Amoxicillin"} and mine == []
        assert (await eve.get("/api/labs/hba1c", headers=acting(owner_id))).status_code == 200
        dash = (await eve.get("/api/dashboard", headers=acting(owner_id))).json()
        assert dash["doses_today"]

        # A viewer can't change anything.
        dose = dash["doses_today"][0]
        body = {
            "medication_id": dose["medication_id"],
            "date": dash["today"],
            "time": dose["time"],
            "status": "taken",
        }
        resp = await eve.put("/api/doses", json=body, headers=acting(owner_id, eve))
        assert resp.status_code == 403
        assert "viewer" in resp.json()["detail"]

        # Personal routes ignore the header: the session is still Eve's.
        me = (await eve.get("/api/auth/session", headers=acting(owner_id))).json()["user"]
        assert me["email"] == "eve@example.com"

    owners_view = (await client.get("/api/circle")).json()["caregivers"]
    assert owners_view[0]["person"]["name"] == "Eve Example"
    assert owners_view[0]["status"] == "active"


async def test_helpers_can_tick_doses_and_owners_see_it(client: httpx.AsyncClient):
    owner_id = await _owner(client)
    created = await _invite(client, "sam@example.com", role="helper")
    async with person(client, "sam@example.com", "Sam Helper") as sam:
        await sam.post("/api/circle/accept", json={"token": created["token"]}, headers=csrf(sam))
        dash = (await sam.get("/api/dashboard", headers=acting(owner_id))).json()
        dose = dash["doses_today"][0]
        body = {
            "medication_id": dose["medication_id"],
            "date": dash["today"],
            "time": dose["time"],
            "status": "taken",
        }
        resp = await sam.put("/api/doses", json=body, headers=acting(owner_id, sam))
        assert resp.status_code == 200, resp.text

    owner_dash = (await client.get("/api/dashboard")).json()
    assert any(d["status"] == "taken" for d in owner_dash["doses_today"])
    events = (await client.get("/api/audit")).json()
    items = events["items"] if isinstance(events, dict) else events
    change = next(e for e in items if e["action"] == "caregiver.change")
    assert change["meta"]["caregiver"] == "Sam Helper"
    assert change["meta"]["path"] == "/doses"


async def test_everything_else_is_out_of_bounds(client: httpx.AsyncClient):
    owner_id = await _owner(client)
    created = await _invite(client, "sam@example.com", role="helper")
    async with person(client, "sam@example.com") as sam:
        await sam.post("/api/circle/accept", json={"token": created["token"]}, headers=csrf(sam))
        h = acting(owner_id, sam)
        assert (await sam.get("/api/shares", headers=h)).status_code == 403
        assert (await sam.get("/api/assistant/threads", headers=h)).status_code == 403
        upload = await sam.post(
            "/api/documents",
            files={"file": ("x.pdf", b"%PDF-1.4", "application/pdf")},
            headers=h,
        )
        assert upload.status_code == 403
        visits = (await sam.get("/api/visits", headers=h)).json()
        resp = await sam.patch(f"/api/visits/{visits[0]['id']}", json={"title": "x"}, headers=h)
        assert resp.status_code == 403

    async with person(client, "mallory@example.com") as mallory:
        resp = await mallory.get("/api/medications", headers=acting(owner_id))
        assert resp.status_code == 403
        assert (
            await mallory.get("/api/medications", headers=acting("nonsense"))
        ).status_code == 403


async def test_invitations_are_bound_to_one_email_and_one_use(client: httpx.AsyncClient):
    await _owner(client)
    me = (await client.get("/api/auth/session")).json()["user"]["email"]
    own = await client.post(
        "/api/circle/invites", json={"email": me, "role": "viewer"}, headers=csrf(client)
    )
    assert own.status_code == 422
    created = await _invite(client, "eve@example.com")
    dup = await client.post(
        "/api/circle/invites", json={"email": "EVE@example.com"}, headers=csrf(client)
    )
    assert dup.status_code == 409

    async with person(client, "mallory@example.com") as mallory:
        resp = await mallory.post(
            "/api/circle/accept", json={"token": created["token"]}, headers=csrf(mallory)
        )
        assert resp.status_code == 403
        assert "eve@example.com" in resp.json()["detail"]
    async with person(client, "eve@example.com") as eve:
        ok = await eve.post(
            "/api/circle/accept", json={"token": created["token"]}, headers=csrf(eve)
        )
        assert ok.status_code == 200
        again = await eve.post(
            "/api/circle/accept", json={"token": created["token"]}, headers=csrf(eve)
        )
        assert again.status_code == 404  # the token is one-time


async def test_revoking_ends_access(client: httpx.AsyncClient):
    owner_id = await _owner(client)
    created = await _invite(client, "eve@example.com")
    async with person(client, "eve@example.com") as eve:
        await eve.post("/api/circle/accept", json={"token": created["token"]}, headers=csrf(eve))
        assert (await eve.get("/api/medications", headers=acting(owner_id))).status_code == 200
        link_id = (await client.get("/api/circle")).json()["caregivers"][0]["id"]
        resp = await client.delete(f"/api/circle/{link_id}", headers=csrf(client))
        assert resp.status_code == 204
        assert (await eve.get("/api/medications", headers=acting(owner_id))).status_code == 403
        assert (await eve.get("/api/circle")).json()["caring_for"] == []


async def test_demo_accounts_help_a_family_member(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    circle = (await client.get("/api/circle")).json()
    rosa = circle["caring_for"][0]
    assert rosa["person"]["name"] == "Rosa Lindqvist" and rosa["role"] == "helper"
    meds = (await client.get("/api/medications", headers=acting(rosa["person"]["id"]))).json()
    assert {m["name"] for m in meds} == {"Metformin", "Atorvastatin", "Cholecalciferol"}
    supply = (await client.get("/api/supply", headers=acting(rosa["person"]["id"]))).json()
    assert supply[0]["name"] == "Metformin"
