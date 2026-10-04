"""Dose alerts for caregivers (ADR-032): opt-in per person, on time or "not ticked yet"."""

from __future__ import annotations

import contextlib
import uuid

import httpx
from sqlalchemy import select

from app.modules.audit.models import AuditLog
from app.modules.doses.models import DoseLog
from tests.conftest import BASE_URL, confirm_email, csrf
from tests.test_doses import _medicine, _today
from tests.test_reminders import SUB, at, tick

EVE_SUB = {**SUB, "endpoint": "https://push.example.com/send/eve-device"}


@contextlib.asynccontextmanager
async def caregiver(owner: httpx.AsyncClient, role: str = "helper"):
    """Eve, confirmed, in Ada's care circle with `role`, with a subscribed device."""
    from app.main import app

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL) as eve:
        await eve.post(
            "/api/auth/signup",
            json={
                "email": "eve@example.com",
                "password": "long-enough-pass",
                "display_name": "Eve",
            },
        )
        await confirm_email(eve, "eve@example.com")
        invite = await owner.post(
            "/api/circle/invites",
            json={"email": "eve@example.com", "role": role},
            headers=csrf(owner),
        )
        token = invite.json()["token"]
        link = (
            await eve.post("/api/circle/accept", json={"token": token}, headers=csrf(eve))
        ).json()
        resp = await eve.post("/api/push/subscriptions", json=EVE_SUB, headers=csrf(eve))
        assert resp.status_code == 201
        eve.link_id = link["id"]
        yield eve


async def alerts(eve: httpx.AsyncClient, minutes: int | None) -> httpx.Response:
    return await eve.put(
        f"/api/circle/{eve.link_id}/alerts", json={"minutes": minutes}, headers=csrf(eve)
    )


def to_eve(sender) -> list[dict]:
    return [payload for sub, payload in sender.sent if sub.endpoint == EVE_SUB["endpoint"]]


async def owner_with_medicine(client: httpx.AsyncClient) -> str:
    await client.post(
        "/api/auth/signup",
        json={"email": "ada@example.com", "password": "long-enough-pass", "display_name": "Ada Ok"},
    )
    await _medicine(client, days_ago=2)  # Testamol 250 mg at 08:00 and 20:00
    return (await client.get("/api/auth/me")).json()["id"]


async def test_alerts_are_off_until_the_caregiver_asks(client: httpx.AsyncClient, sender):
    await owner_with_medicine(client)
    async with caregiver(client):
        assert await tick(at("08:03")) == 0
        assert to_eve(sender) == []


async def test_alert_when_due_with_actions_for_helpers(client: httpx.AsyncClient, sender, session):
    owner_id = await owner_with_medicine(client)
    async with caregiver(client) as eve:
        assert (await alerts(eve, 0)).json()["alert_minutes"] == 0
        assert await tick(at("08:03")) == 1
        [payload] = to_eve(sender)
        assert payload["title"] == "Ada's 8:00 AM dose is due"
        assert payload["body"] == "Testamol 250 mg"
        assert payload["url"] == f"/app?for={owner_id}"
        assert [a["action"] for a in payload["actions"]] == ["taken", "skipped"]
        assert await tick(at("08:05")) == 0  # once per dose

        # Taken, straight from the notification: marks Ada's dose and shows in her activity.
        resp = await eve.post(
            "/api/push/actions", json={"token": payload["token"], "action": "taken"}
        )
        assert resp.status_code == 200, resp.text
        logged = (
            await session.scalars(select(DoseLog).where(DoseLog.user_id == uuid.UUID(owner_id)))
        ).all()
        assert [(d.due_time, d.status) for d in logged] == [("08:00", "taken")]


async def test_not_ticked_yet_alerts_wait_and_skip_ticked_doses(client: httpx.AsyncClient, sender):
    await owner_with_medicine(client)
    async with caregiver(client, role="viewer") as eve:
        await alerts(eve, 30)
        assert await tick(at("08:03")) == 0  # not yet: Ada still has time
        # Ada ticks her morning dose; nobody needs to hear about it.
        meds = (await client.get("/api/medications")).json()
        await client.put(
            "/api/doses",
            json={
                "medication_id": meds[0]["id"],
                "date": _today().isoformat(),
                "time": "08:00",
                "status": "taken",
            },
            headers=csrf(client),
        )
        assert await tick(at("08:33")) == 0
        # The evening dose stays unticked: Eve hears about it half an hour later.
        assert await tick(at("20:31")) == 1
        [payload] = to_eve(sender)
        assert payload["title"] == "Ada's 8:00 PM dose not ticked yet"
        assert "actions" not in payload and "token" not in payload  # viewers can't tick


async def test_revoking_access_stops_alerts_and_disables_sent_buttons(
    client: httpx.AsyncClient, sender, session
):
    await owner_with_medicine(client)
    async with caregiver(client) as eve:
        await alerts(eve, 0)
        await tick(at("08:03"))
        [payload] = to_eve(sender)

        circle = (await client.get("/api/circle")).json()
        link = circle["caregivers"][0]
        assert link["alert_minutes"] == 0  # Ada can see Eve gets alerts
        await client.delete(f"/api/circle/{link['id']}", headers=csrf(client))

        resp = await eve.post(
            "/api/push/actions", json={"token": payload["token"], "action": "taken"}
        )
        assert resp.status_code == 401
        assert await tick(at("20:03")) == 0
        assert len(to_eve(sender)) == 1

    actions = (await session.scalars(select(AuditLog.action))).all()
    assert "circle.alerts_changed" in actions


async def test_helper_actions_are_audited_for_the_owner(client: httpx.AsyncClient, sender, session):
    owner_id = await owner_with_medicine(client)
    async with caregiver(client) as eve:
        await alerts(eve, 0)
        await tick(at("08:03"))
        [payload] = to_eve(sender)
        await eve.post("/api/push/actions", json={"token": payload["token"], "action": "skipped"})
    row = await session.scalar(
        select(AuditLog).where(
            AuditLog.action == "caregiver.change", AuditLog.meta["via"].astext == "notification"
        )
    )
    assert str(row.user_id) == owner_id
    assert row.meta["caregiver"] == "Eve" and row.meta["status"] == "skipped"


async def test_only_the_caregiver_sets_alerts(client: httpx.AsyncClient, sender):
    await owner_with_medicine(client)
    async with caregiver(client) as eve:
        assert (await alerts(eve, 15)).status_code == 422
        owner_try = await client.put(
            f"/api/circle/{eve.link_id}/alerts", json={"minutes": 0}, headers=csrf(client)
        )
        assert owner_try.status_code == 404
        assert (await alerts(eve, None)).json()["alert_minutes"] is None


async def test_caregivers_who_switch_notifications_off_get_none(client: httpx.AsyncClient, sender):
    await owner_with_medicine(client)
    async with caregiver(client) as eve:
        await alerts(eve, 0)
        await eve.put(
            "/api/push/settings", json={"enabled": False, "lead_minutes": 0}, headers=csrf(eve)
        )
        assert await tick(at("08:03")) == 0
        assert to_eve(sender) == []
