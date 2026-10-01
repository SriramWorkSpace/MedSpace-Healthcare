from __future__ import annotations

from datetime import timedelta

import httpx
from sqlalchemy import select, update

from app.core.db import utcnow
from app.core.security import sha256_hex
from app.modules.sharing.models import ShareLink
from tests.conftest import BASE_URL, csrf


async def setup_share(client: httpx.AsyncClient, **overrides) -> dict:
    await client.post("/api/auth/demo")
    rx = (await client.get("/api/prescriptions")).json()[0]
    docs = (await client.get("/api/documents?status=confirmed")).json()["items"]
    lab = next(d for d in docs if d["kind"] == "lab_report")
    body = {
        "label": "For Dr. Reyes",
        "expires_in_days": 7,
        "items": [{"type": "prescription", "id": rx["id"]}, {"type": "document", "id": lab["id"]}],
        **overrides,
    }
    resp = await client.post("/api/shares", json=body, headers=csrf(client))
    assert resp.status_code == 201, resp.text
    return {"created": resp.json(), "rx": rx, "lab": lab}


def anon(client: httpx.AsyncClient) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=client._transport.app), base_url=BASE_URL
    )


async def test_create_returns_token_once_and_stores_only_hash(client: httpx.AsyncClient, session):
    ctx = await setup_share(client)
    created = ctx["created"]
    token = created["token"]
    assert created["url"].endswith(f"/s/{token}")
    assert created["share"]["status"] == "active"
    assert {i["type"] for i in created["share"]["items"]} == {"prescription", "document"}

    stored = await session.scalar(select(ShareLink))
    assert stored.token_hash == sha256_hex(token)
    assert token not in str(stored.__dict__.values())

    listing = (await client.get("/api/shares")).json()
    assert "token" not in listing[0]
    assert listing[0]["token_hint"] == token[-6:]


async def test_public_view_returns_scoped_bundle_and_audits(client: httpx.AsyncClient):
    ctx = await setup_share(client)
    token = ctx["created"]["token"]
    async with anon(client) as visitor:
        resp = await visitor.get(
            f"/api/public/shares/{token}", headers={"User-Agent": "Mozilla/5.0"}
        )
        assert resp.status_code == 200
        assert resp.headers["cache-control"] == "no-store"
        bundle = resp.json()
        assert bundle["label"] == "For Dr. Reyes"
        assert len(bundle["prescriptions"]) == 1
        assert bundle["prescriptions"][0]["medications"]
        assert [d["id"] for d in bundle["documents"]] == [ctx["lab"]["id"]]

        # The shared prescription's source document is viewable; unrelated documents are not.
        rx_doc = ctx["rx"]["document_id"]
        ok = await visitor.get(f"/api/public/shares/{token}/documents/{rx_doc}/pages/1/preview")
        assert ok.status_code == 200 and ok.headers["content-type"] == "image/png"
        all_docs = (await client.get("/api/documents")).json()["items"]
        other = next(d for d in all_docs if d["id"] not in {rx_doc, ctx["lab"]["id"]})
        blocked = await visitor.get(
            f"/api/public/shares/{token}/documents/{other['id']}/pages/1/preview"
        )
        assert blocked.status_code == 404

    views = (await client.get("/api/audit?action=share.viewed")).json()["items"]
    assert len(views) == 1 and views[0]["actor"] == "public"
    assert (await client.get("/api/shares")).json()[0]["view_count"] == 1


async def test_view_limit_is_enforced(client: httpx.AsyncClient):
    ctx = await setup_share(client, max_views=2)
    token = ctx["created"]["token"]
    async with anon(client) as visitor:
        codes = [(await visitor.get(f"/api/public/shares/{token}")).status_code for _ in range(3)]
    assert codes == [200, 200, 410]
    assert (await client.get("/api/shares")).json()[0]["status"] == "exhausted"


async def test_revoked_links_stop_working_immediately(client: httpx.AsyncClient):
    ctx = await setup_share(client)
    created = ctx["created"]
    resp = await client.delete(f"/api/shares/{created['share']['id']}", headers=csrf(client))
    assert resp.json()["status"] == "revoked"
    async with anon(client) as visitor:
        gone = await visitor.get(f"/api/public/shares/{created['token']}")
        assert gone.status_code == 410
        assert gone.json()["reason"] == "revoked"
        preview = await visitor.get(
            f"/api/public/shares/{created['token']}/documents/{ctx['lab']['id']}/pages/1/preview"
        )
        assert preview.status_code == 410


async def test_expired_links_are_gone(client: httpx.AsyncClient, session):
    ctx = await setup_share(client)
    await session.execute(update(ShareLink).values(expires_at=utcnow() - timedelta(minutes=1)))
    await session.commit()
    async with anon(client) as visitor:
        resp = await visitor.get(f"/api/public/shares/{ctx['created']['token']}")
    assert resp.status_code == 410
    assert resp.json()["reason"] == "expired"


async def test_unknown_tokens_404(client: httpx.AsyncClient):
    async with anon(client) as visitor:
        assert (await visitor.get("/api/public/shares/not-a-real-token")).status_code == 404


async def test_cannot_share_someone_elses_records(client: httpx.AsyncClient):
    await client.post("/api/auth/demo")
    victim_rx = (await client.get("/api/prescriptions")).json()[0]
    async with anon(client) as attacker:
        await attacker.post("/api/auth/demo")
        resp = await attacker.post(
            "/api/shares",
            json={"label": "steal", "items": [{"type": "prescription", "id": victim_rx["id"]}]},
            headers=csrf(attacker),
        )
        assert resp.status_code == 422
        # Nor revoke someone else's link.
        ctx_link = await client.post(
            "/api/shares",
            json={"label": "mine", "items": [{"type": "prescription", "id": victim_rx["id"]}]},
            headers=csrf(client),
        )
        link_id = ctx_link.json()["share"]["id"]
        assert (
            await attacker.delete(f"/api/shares/{link_id}", headers=csrf(attacker))
        ).status_code == 404
