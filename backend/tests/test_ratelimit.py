"""Rate limiting: sliding windows, honest client IPs, per-user and per-account keys (ADR-027)."""

from __future__ import annotations

import httpx
import pytest

from app.core import ratelimit
from app.core.config import get_settings
from app.core.ratelimit import MemoryStore
from tests.conftest import BASE_URL, csrf


@pytest.fixture
def settings(monkeypatch):
    s = get_settings()
    monkeypatch.setattr(s, "rate_limit_enabled", True)
    monkeypatch.setattr(s, "rate_limit_scale", 1.0)
    monkeypatch.setattr(s, "trusted_proxy_hops", 0)
    return s


@pytest.fixture
def fake_clock(monkeypatch):
    now = {"t": 1_000_040.0}  # 20 s into a 60 s window (1_000_020 is a boundary)
    store = MemoryStore(clock=lambda: now["t"])
    monkeypatch.setattr(ratelimit, "_store", store)
    return now


async def test_sliding_window_smooths_the_boundary(settings, fake_clock):
    for _ in range(10):
        assert (await ratelimit.check("t", "k", 10, 60)).allowed
    denied = await ratelimit.check("t", "k", 10, 60)
    assert not denied.allowed
    assert denied.reset == 40

    # Just after the boundary a fixed window would allow 10 more at once; the previous window
    # still counts in proportion to its overlap (11 hits x 0.95 = 10.45 > 10).
    fake_clock["t"] = 1_000_083.0
    assert not (await ratelimit.check("t", "k", 10, 60)).allowed
    # Half-way through, roughly half of the old window has rolled off.
    fake_clock["t"] = 1_000_110.0
    results = [(await ratelimit.check("t", "k", 10, 60)).allowed for _ in range(6)]
    assert results.count(True) >= 3 and results[-1] is False


def _login(client, email="nobody@example.com", ip=None):
    headers = {"X-Forwarded-For": ip} if ip else {}
    return client.post(
        "/api/auth/login", json={"email": email, "password": "wrong-password-123"}, headers=headers
    )


async def test_spoofed_forwarded_for_does_not_reset_limits(client: httpx.AsyncClient, settings):
    # No trusted proxy: the header is the client's own claim and is ignored.
    codes = [
        (await _login(client, f"u{i}@example.com", ip=f"10.0.0.{i}")).status_code for i in range(12)
    ]
    assert codes[:10] == [401] * 10
    assert codes[10] == 429


async def test_trusted_proxy_uses_the_address_it_saw(
    client: httpx.AsyncClient, settings, monkeypatch
):
    monkeypatch.setattr(settings, "trusted_proxy_hops", 1)
    # The client can prepend anything; only the right-most entry (added by our proxy) counts.
    for i in range(10):
        assert (
            await _login(client, f"a{i}@example.com", ip=f"6.6.6.{i}, 203.0.113.7")
        ).status_code == 401
    assert (
        await _login(client, "a-last@example.com", ip="1.2.3.4, 203.0.113.7")
    ).status_code == 429
    assert (await _login(client, "b@example.com", ip="203.0.113.8")).status_code == 401


async def test_one_account_is_protected_across_many_addresses(
    client: httpx.AsyncClient, settings, monkeypatch
):
    monkeypatch.setattr(settings, "trusted_proxy_hops", 1)
    target = "victim@example.com"
    codes = [(await _login(client, target, ip=f"198.51.100.{i}")).status_code for i in range(11)]
    assert codes[:10] == [401] * 10
    last = await _login(client, target, ip="198.51.100.200")
    assert last.status_code == 429
    assert "this account" in last.json()["detail"]
    assert int(last.headers["Retry-After"]) > 0
    # Other accounts from a fresh address are unaffected.
    assert (
        await _login(client, "someone-else@example.com", ip="198.51.100.201")
    ).status_code == 401


async def test_signed_in_limits_are_per_user_not_per_address(client: httpx.AsyncClient, settings):
    await client.post("/api/auth/demo")
    codes = [(await client.get("/api/me/export")).status_code for _ in range(6)]
    assert codes == [200] * 5 + [429]
    blocked = await client.get("/api/me/export")
    assert blocked.headers["content-type"].startswith("application/problem+json")
    assert blocked.json()["code"] == "rate_limited" and "Retry-After" in blocked.headers

    # A second user behind the same address has their own budget.
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=client._transport.app), base_url=BASE_URL
    ) as other:
        await other.post(
            "/api/auth/signup",
            json={"email": "eve@example.com", "password": "long-enough-pass", "display_name": "E"},
        )
        assert (await other.get("/api/me/export")).status_code == 200


async def test_headers_scale_and_disable(client: httpx.AsyncClient, settings, monkeypatch):
    await client.post("/api/auth/demo")
    resp = await client.get("/api/medications")
    assert int(resp.headers["RateLimit-Limit"]) == ratelimit.BASELINE_READS[0]
    assert int(resp.headers["RateLimit-Remaining"]) < ratelimit.BASELINE_READS[0]

    monkeypatch.setattr(settings, "rate_limit_scale", 2.0)
    assert [(await client.get("/api/me/export")).status_code for _ in range(10)] == [200] * 10

    monkeypatch.setattr(settings, "rate_limit_enabled", False)
    assert (await client.get("/api/me/export")).status_code == 200


async def test_baseline_budget_covers_every_route(client: httpx.AsyncClient, settings, monkeypatch):
    await client.post("/api/auth/demo")
    monkeypatch.setattr(ratelimit, "BASELINE_READS", (3, 60))
    monkeypatch.setattr(ratelimit, "BASELINE_WRITES", (2, 60))
    codes = [(await client.get("/api/timeline")).status_code for _ in range(5)]
    assert codes[:3] == [200, 200, 200] and codes[-1] == 429
    blocked = await client.get("/api/labs")
    assert blocked.status_code == 429 and blocked.headers["RateLimit-Remaining"] == "0"
    # Health checks are never limited.
    assert (await client.get("/api/health")).status_code == 200
    # Writes have their own, smaller budget.
    w = [
        (await client.post("/api/visits", json={}, headers=csrf(client))).status_code
        for _ in range(4)
    ]
    assert w[:2] == [201, 201] and w[-1] == 429


async def test_the_limiter_fails_open(client: httpx.AsyncClient, settings, monkeypatch):
    class Broken:
        async def hit(self, key, window):
            raise ConnectionError("redis is down")

    monkeypatch.setattr(ratelimit, "_store", Broken())
    assert (await _login(client)).status_code == 401  # served, not a 500 or a lockout
