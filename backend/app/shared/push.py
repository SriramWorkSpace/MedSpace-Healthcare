"""Web Push port (ADR-028): a real sender (pywebpush + VAPID) and a fake for dev, demo and tests.

Senders return an outcome per subscription so callers can drop subscriptions the push service
says are gone (404/410) and keep the rest.
"""

from __future__ import annotations

import asyncio
import base64
import json
import logging
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Literal, Protocol

from app.core.config import get_settings

logger = logging.getLogger("medspace.push")

Outcome = Literal["sent", "gone", "failed"]


@dataclass(frozen=True)
class Subscription:
    endpoint: str
    p256dh: str
    auth: str


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


@dataclass(frozen=True)
class VapidKeys:
    public_key: str  # base64url uncompressed P-256 point: what browsers need to subscribe
    private_key: str  # base64url raw 32-byte scalar: what pywebpush signs with


def generate_vapid_keys() -> VapidKeys:
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

    key = ec.generate_private_key(ec.SECP256R1())
    public = key.public_key().public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)
    private = key.private_numbers().private_value.to_bytes(32, "big")
    return VapidKeys(public_key=_b64url(public), private_key=_b64url(private))


@lru_cache
def vapid_keys() -> VapidKeys:
    """Configured keys, or (fake provider only) a throwaway pair for this process."""
    s = get_settings()
    if s.vapid_public_key and s.vapid_private_key:
        return VapidKeys(s.vapid_public_key, s.vapid_private_key.get_secret_value())
    return generate_vapid_keys()


class PushSender(Protocol):
    name: str

    async def send(self, sub: Subscription, payload: dict) -> Outcome: ...


@dataclass
class FakePushSender:
    """Records what would have been sent. `gone_endpoints` simulates expired subscriptions."""

    name: str = "fake"
    sent: list[tuple[Subscription, dict]] = field(default_factory=list)
    gone_endpoints: set[str] = field(default_factory=set)

    async def send(self, sub: Subscription, payload: dict) -> Outcome:
        if sub.endpoint in self.gone_endpoints:
            return "gone"
        self.sent.append((sub, payload))
        logger.info("push (simulated) to %s: %s", sub.endpoint[:48], payload.get("title"))
        return "sent"


class WebPushSender:
    name = "webpush"

    def __init__(self, keys: VapidKeys, subject: str) -> None:
        self._keys = keys
        self._subject = subject

    async def send(self, sub: Subscription, payload: dict) -> Outcome:
        from pywebpush import WebPushException, webpush

        def _send() -> Outcome:
            try:
                webpush(
                    subscription_info={
                        "endpoint": sub.endpoint,
                        "keys": {"p256dh": sub.p256dh, "auth": sub.auth},
                    },
                    data=json.dumps(payload),
                    vapid_private_key=self._keys.private_key,
                    vapid_claims={"sub": self._subject},
                    ttl=60 * 30,  # a dose reminder is stale after half an hour
                    timeout=10,
                )
                return "sent"
            except WebPushException as exc:
                status = getattr(exc.response, "status_code", None)
                if status in (404, 410):
                    return "gone"
                logger.warning("push failed (%s): %s", status, exc)
                return "failed"

        return await asyncio.to_thread(_send)


_sender: PushSender | None = None


def get_push_sender() -> PushSender:
    global _sender
    if _sender is None:
        s = get_settings()
        provider = s.push_provider
        if provider == "auto":
            provider = "webpush" if s.vapid_public_key and s.vapid_private_key else "fake"
        if provider == "webpush":
            if not (s.vapid_public_key and s.vapid_private_key):
                raise RuntimeError(
                    "PUSH_PROVIDER=webpush needs VAPID_PUBLIC_KEY and VAPID_PRIVATE_KEY"
                )
            _sender = WebPushSender(vapid_keys(), s.vapid_subject)
        else:
            _sender = FakePushSender()
    return _sender


def set_push_sender(sender: PushSender | None) -> None:
    """Tests swap in their own sender (None resets to the configured one)."""
    global _sender
    _sender = sender


if __name__ == "__main__":  # python -m app.shared.push  -> print a fresh key pair for .env
    keys = generate_vapid_keys()
    print(f"VAPID_PUBLIC_KEY={keys.public_key}\nVAPID_PRIVATE_KEY={keys.private_key}")
