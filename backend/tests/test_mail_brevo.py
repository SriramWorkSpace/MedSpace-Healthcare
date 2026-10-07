"""Brevo's HTTPS email API (ADR-039): for hosts that block outbound SMTP ports."""

from __future__ import annotations

import json
import logging

import httpx
import pytest

from app.core.config import get_settings
from app.shared import mail
from app.shared.mail import BREVO_URL, BrevoMailer, Message

KEY = "xkeysib-test-key-never-logged"


def mailer(handler) -> tuple[BrevoMailer, list[httpx.Request]]:
    calls: list[httpx.Request] = []

    def record(req: httpx.Request) -> httpx.Response:
        calls.append(req)
        return handler(req)

    http = httpx.AsyncClient(transport=httpx.MockTransport(record))
    return BrevoMailer(KEY, "MedSpace <medspace.mail@gmail.com>", http), calls


async def test_sends_over_https_with_the_verified_sender():
    m, calls = mailer(lambda r: httpx.Response(201, json={"messageId": "<1@brevo>"}))
    ok = await m.send(Message("ada@example.com", "Confirm your email", "Hi", "<p>Hi</p>"))
    assert ok
    [req] = calls
    assert str(req.url) == BREVO_URL and req.url.scheme == "https"
    assert req.headers["api-key"] == KEY
    body = json.loads(req.content)
    assert body["sender"] == {"name": "MedSpace", "email": "medspace.mail@gmail.com"}
    assert body["to"] == [{"email": "ada@example.com"}]
    assert body["subject"] == "Confirm your email"
    assert body["textContent"] == "Hi" and body["htmlContent"] == "<p>Hi</p>"


async def test_failures_are_logged_without_the_key(caplog):
    caplog.set_level(logging.DEBUG)
    m, _ = mailer(lambda r: httpx.Response(401, json={"code": "unauthorized"}))
    assert await m.send(Message("ada@example.com", "Reset", "Hi")) is False
    assert "Brevo 401 unauthorized" in caplog.text
    assert KEY not in caplog.text

    def down(req):
        raise httpx.ConnectError("boom")

    m, _ = mailer(down)
    assert await m.send(Message("ada@example.com", "Reset", "Hi")) is False  # never raises


@pytest.mark.parametrize(
    ("brevo", "smtp", "expected"),
    [
        (KEY, None, "brevo"),
        (KEY, "smtp.example.com", "brevo"),
        (None, "smtp.example.com", "smtp"),
        (None, None, "fake"),
    ],
)
def test_auto_picks_brevo_then_smtp_then_the_outbox(monkeypatch, brevo, smtp, expected):
    s = get_settings()
    monkeypatch.setattr(s, "mail_provider", "auto")
    monkeypatch.setattr(s, "brevo_api_key", type(s.jwt_secret)(brevo) if brevo else None)
    monkeypatch.setattr(s, "smtp_host", smtp)
    monkeypatch.setattr(s, "mail_from", "MedSpace <medspace.mail@gmail.com>")
    mail.set_mailer(None)
    try:
        assert mail.get_mailer().name == expected
    finally:
        mail.set_mailer(None)
