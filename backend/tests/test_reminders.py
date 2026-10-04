"""Dose reminders by push: who gets reminded, when, once, and acting from the notification."""

from __future__ import annotations

from datetime import UTC, datetime, time, timedelta

import httpx

from app.core.db import SessionLocal
from app.modules.reminders import service as reminders
from tests.conftest import BASE_URL, csrf
from tests.test_doses import _medicine, _today

SUB = {
    "endpoint": "https://push.example.com/send/abc123",
    "keys": {
        "p256dh": (
            "BNcRdreALRFXTkOOUHK1EtK2wtaz5Ry4YfYCA_0QTpQtUbVlUls0VJXg7A8u-Ts1Xbjha"
            "zAkj7I99e8QcYP7DkM"
        ),
        "auth": "tBHItJI5svbpez7KI4CCXg",
    },
}


async def _subscribe(client: httpx.AsyncClient, sub: dict = SUB) -> dict:
    resp = await client.post("/api/push/subscriptions", json=sub, headers=csrf(client))
    assert resp.status_code == 201, resp.text
    return resp.json()


async def tick(at: datetime) -> int:
    async with SessionLocal() as session:
        sent = await reminders.send_due_reminders(session, now=at)
        await session.commit()
        return sent


def at(hhmm: str, days: int = 0) -> datetime:
    h, m = (int(x) for x in hhmm.split(":"))
    return datetime.combine(_today() + timedelta(days=days), time(h, m), tzinfo=UTC)


async def test_devices_subscribe_privately(auth_client: httpx.AsyncClient, sender):
    out = await _subscribe(auth_client)
    assert out["endpoint_hint"] == "push.example.com"  # never echo the full capability URL
    insecure = {**SUB, "endpoint": "http://push.example.com/x"}
    assert (
        await auth_client.post("/api/push/subscriptions", json=insecure, headers=csrf(auth_client))
    ).status_code == 422

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=auth_client._transport.app), base_url=BASE_URL
    ) as other:
        await other.post(
            "/api/auth/signup",
            json={"email": "eve@example.com", "password": "long-enough-pass", "display_name": "E"},
        )
        resp = await other.delete(
            "/api/push/subscriptions", params={"endpoint": SUB["endpoint"]}, headers=csrf(other)
        )
        assert resp.status_code == 404
        assert (await other.get("/api/push/subscriptions")).json() == []
    assert len((await auth_client.get("/api/push/subscriptions")).json()) == 1
    config = (await auth_client.get("/api/push/config")).json()
    assert config["provider"] == "fake" and len(config["public_key"]) > 80


async def test_a_due_dose_is_reminded_exactly_once(auth_client: httpx.AsyncClient, sender):
    await _medicine(auth_client, days_ago=2)
    await _subscribe(auth_client)

    assert await tick(at("07:55")) == 0  # not yet
    assert await tick(at("08:03")) == 1
    _, payload = sender.sent[-1]
    assert payload["title"] == "Time for your 8:00 AM dose"
    assert payload["body"].startswith("Testamol 250 mg")
    assert [a["action"] for a in payload["actions"]] == ["taken", "skipped"]
    assert await tick(at("08:04")) == 0  # never twice
    assert await tick(at("20:45")) == 0  # far past the catch-up window: no stale reminder


async def test_marked_doses_lead_time_and_switching_off(auth_client: httpx.AsyncClient, sender):
    med = await _medicine(auth_client, days_ago=2)
    await _subscribe(auth_client)
    await auth_client.put(
        "/api/doses",
        json={
            "medication_id": med["id"],
            "date": str(_today()),
            "time": "08:00",
            "status": "taken",
        },
        headers=csrf(auth_client),
    )
    assert await tick(at("08:02")) == 0  # already taken

    resp = await auth_client.put(
        "/api/push/settings", json={"enabled": True, "lead_minutes": 15}, headers=csrf(auth_client)
    )
    assert resp.status_code == 200
    assert await tick(at("19:46")) == 1  # 15 minutes before 20:00
    assert sender.sent[-1][1]["title"] == "Time for your 8:00 PM dose"

    bad = await auth_client.put(
        "/api/push/settings", json={"enabled": True, "lead_minutes": 7}, headers=csrf(auth_client)
    )
    assert bad.status_code == 422
    await auth_client.put(
        "/api/push/settings", json={"enabled": False, "lead_minutes": 0}, headers=csrf(auth_client)
    )
    assert await tick(at("08:01", days=1)) == 0


async def test_notification_buttons_mark_doses_without_a_session(
    auth_client: httpx.AsyncClient, sender
):
    await _medicine(auth_client, days_ago=2)
    await _subscribe(auth_client)
    await tick(at("08:01"))
    token = sender.sent[-1][1]["token"]

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=auth_client._transport.app), base_url=BASE_URL
    ) as worker:  # the service worker: no cookies, no CSRF header
        resp = await worker.post("/api/push/actions", json={"token": token, "action": "taken"})
        assert resp.status_code == 200, resp.text
        assert resp.json() == {"updated": 1}
        tampered = token[:-4] + ("AAAA" if not token.endswith("AAAA") else "BBBB")
        bad = await worker.post("/api/push/actions", json={"token": tampered, "action": "taken"})
        assert bad.status_code == 401
        # A session token is not a dose-action token.
        session_token = auth_client.cookies.get("ms_access")
        wrong = await worker.post(
            "/api/push/actions", json={"token": session_token, "action": "taken"}
        )
        assert wrong.status_code == 401

    dash = (await auth_client.get("/api/dashboard")).json()
    assert any(d["time"] == "08:00" and d["status"] == "taken" for d in dash["doses_today"])


async def test_test_notifications_and_expired_devices(auth_client: httpx.AsyncClient, sender):
    await _subscribe(auth_client)
    resp = await auth_client.post("/api/push/test", headers=csrf(auth_client))
    assert resp.json() == {"sent": 1, "removed": 0}
    assert sender.sent[-1][1]["title"] == "Reminders are on"

    sender.gone_endpoints.add(
        SUB["endpoint"]
    )  # the browser unsubscribed or the push service expired it
    resp = await auth_client.post("/api/push/test", headers=csrf(auth_client))
    assert resp.json() == {"sent": 0, "removed": 1}
    assert (await auth_client.get("/api/push/subscriptions")).json() == []


async def test_real_sender_signs_and_encrypts(monkeypatch):
    """The webpush sender works with our VAPID key format and a real browser key pair."""
    import base64
    import os

    import pywebpush
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

    from app.shared.push import Subscription, WebPushSender, generate_vapid_keys

    browser = ec.generate_private_key(ec.SECP256R1()).public_key()
    p256dh = base64.urlsafe_b64encode(
        browser.public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)
    ).rstrip(b"=")
    auth = base64.urlsafe_b64encode(os.urandom(16)).rstrip(b"=")
    sub = Subscription("https://push.example.com/send/xyz", p256dh.decode(), auth.decode())

    calls = []

    class Resp:
        def __init__(self, status):
            self.status_code = status
            self.text = ""
            self.headers = {}
            self.reason = ""

    def fake_post(url, data=None, headers=None, timeout=None, **_):
        calls.append(headers)
        return Resp(status)

    monkeypatch.setattr(pywebpush.requests, "post", fake_post)
    sender = WebPushSender(generate_vapid_keys(), "mailto:test@example.com")
    status = 201
    assert await sender.send(sub, {"title": "x"}) == "sent"
    assert calls[-1]["Authorization"].startswith("vapid t=")  # signed with our key
    assert calls[-1]["Content-Encoding"] == "aes128gcm"  # encrypted for the browser key
    status = 410
    assert await sender.send(sub, {"title": "x"}) == "gone"
    status = 500
    assert await sender.send(sub, {"title": "x"}) == "failed"
