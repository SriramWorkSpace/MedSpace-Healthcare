"""Email port (ADR-030): SMTP in production, an in-memory outbox in dev, demo and tests.

Sending is best effort: a mail server outage is logged and never fails the request that
triggered it (the user can ask for the email again).
"""

from __future__ import annotations

import asyncio
import logging
import smtplib
import ssl
from collections import deque
from dataclasses import dataclass, field
from email.message import EmailMessage
from email.utils import make_msgid
from typing import Protocol

from app.core.config import get_settings

logger = logging.getLogger("medspace.mail")


@dataclass(frozen=True)
class Message:
    to: str
    subject: str
    text: str
    html: str | None = None


class Mailer(Protocol):
    name: str

    async def send(self, message: Message) -> bool: ...


@dataclass
class FakeMailer:
    """Keeps the last messages in memory (the dev outbox and tests read them)."""

    name: str = "fake"
    outbox: deque[Message] = field(default_factory=lambda: deque(maxlen=200))

    async def send(self, message: Message) -> bool:
        self.outbox.append(message)
        logger.info("mail (simulated) to %s: %s", message.to, message.subject)
        return True

    def latest(self, to: str) -> list[Message]:
        """Newest first."""
        return [m for m in reversed(self.outbox) if m.to.lower() == to.lower()]


class SmtpMailer:
    name = "smtp"

    def __init__(
        self,
        host: str,
        port: int,
        username: str | None,
        password: str | None,
        sender: str,
        security: str,
    ) -> None:
        self._host, self._port = host, port
        self._username, self._password = username, password
        self._sender = sender
        self._security = security  # "starttls" | "ssl" | "none"

    def _build(self, message: Message) -> EmailMessage:
        msg = EmailMessage()
        msg["From"] = self._sender
        msg["To"] = message.to
        msg["Subject"] = message.subject
        msg["Message-ID"] = make_msgid(domain=self._sender.rsplit("@", 1)[-1].strip("> "))
        msg.set_content(message.text)
        if message.html:
            msg.add_alternative(message.html, subtype="html")
        return msg

    def _send_sync(self, message: Message) -> None:
        context = ssl.create_default_context()
        if self._security == "ssl":
            server: smtplib.SMTP = smtplib.SMTP_SSL(
                self._host, self._port, timeout=15, context=context
            )
        else:
            server = smtplib.SMTP(self._host, self._port, timeout=15)
        with server:
            if self._security == "starttls":
                server.starttls(context=context)
            if self._username and self._password:
                server.login(self._username, self._password)
            server.send_message(self._build(message))

    async def send(self, message: Message) -> bool:
        try:
            await asyncio.to_thread(self._send_sync, message)
            return True
        except (OSError, smtplib.SMTPException) as exc:
            logger.warning("mail to %s failed: %s", message.to, exc)
            return False


_mailer: Mailer | None = None


def get_mailer() -> Mailer:
    global _mailer
    if _mailer is None:
        s = get_settings()
        provider = s.mail_provider
        if provider == "auto":
            provider = "smtp" if s.smtp_host else "fake"
        if provider == "smtp":
            if not s.smtp_host:
                raise RuntimeError("MAIL_PROVIDER=smtp needs SMTP_HOST")
            _mailer = SmtpMailer(
                s.smtp_host,
                s.smtp_port,
                s.smtp_username,
                s.smtp_password.get_secret_value() if s.smtp_password else None,
                s.mail_from,
                s.smtp_security,
            )
        else:
            _mailer = FakeMailer()
    return _mailer


def set_mailer(mailer: Mailer | None) -> None:
    """Tests swap in their own mailer (None resets to the configured one)."""
    global _mailer
    _mailer = mailer
