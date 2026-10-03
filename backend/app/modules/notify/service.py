"""Transactional email (ADR-030): what MedSpace says, and to whom. Delivery is the mail port's job.

Every message has a plain-text body (the source of truth) and a small HTML version. Emails never
contain health information: only account events and links back to the app.
Demo accounts never trigger real email (anyone can create one, so they must not be a relay).
"""

from __future__ import annotations

from html import escape

from app.core.config import get_settings
from app.shared.mail import Message, get_mailer

DEMO_DOMAIN = "@demo.medspace.dev"


def app_url(path: str) -> str:
    return f"{get_settings().frontend_url}{path}"


def _html(heading: str, paragraphs: list[str], button: tuple[str, str] | None = None) -> str:
    body = "".join(
        f'<p style="margin:0 0 14px;line-height:1.55">{escape(p)}</p>' for p in paragraphs
    )
    cta = ""
    if button:
        label, href = button
        cta = (
            f'<p style="margin:22px 0"><a href="{escape(href, quote=True)}" '
            'style="background:#1f7a5c;color:#ffffff;text-decoration:none;padding:11px 18px;'
            f'border-radius:999px;font-weight:600;display:inline-block">{escape(label)}</a></p>'
            '<p style="margin:0 0 14px;font-size:13px;color:#5b6660">Or paste this link into '
            f'your browser:<br><span style="word-break:break-all">{escape(href)}</span></p>'
        )
    return (
        '<div style="font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;'
        'max-width:520px;margin:0 auto;padding:24px;color:#1b231f">'
        '<p style="font-size:20px;font-weight:700;margin:0 0 20px;letter-spacing:.5px">'
        '<span style="color:#c00000">Med</span><span style="color:#111111">Space</span></p>'
        f'<h1 style="font-size:20px;margin:0 0 14px">{escape(heading)}</h1>{body}{cta}'
        '<p style="margin:28px 0 0;font-size:12px;color:#8a948f">You received this because of '
        "activity on your MedSpace account. MedSpace never sends health details by email.</p>"
        "</div>"
    )


def _text(heading: str, paragraphs: list[str], button: tuple[str, str] | None = None) -> str:
    lines = [heading, "", *[p + "\n" for p in paragraphs]]
    if button:
        lines += [f"{button[0]}: {button[1]}", ""]
    lines.append("MedSpace never sends health details by email.")
    return "\n".join(lines)


async def _send(
    to: str,
    subject: str,
    heading: str,
    paragraphs: list[str],
    button: tuple[str, str] | None = None,
) -> bool:
    if to.lower().endswith(DEMO_DOMAIN):
        return False
    return await get_mailer().send(
        Message(
            to=to,
            subject=subject,
            text=_text(heading, paragraphs, button),
            html=_html(heading, paragraphs, button),
        )
    )


# ---- Account ------------------------------------------------------------------------------------


async def send_verification(to: str, name: str, token: str) -> bool:
    return await _send(
        to,
        "Confirm your email for MedSpace",
        f"Hi {name}, confirm your email",
        [
            "Confirming your address lets you reset your password and accept care circle "
            "invitations. The link works once and expires in 48 hours.",
            "If you didn't create a MedSpace account, you can ignore this email.",
        ],
        ("Confirm email", app_url(f"/verify-email?token={token}")),
    )


async def send_password_reset(to: str, name: str, token: str) -> bool:
    return await _send(
        to,
        "Reset your MedSpace password",
        f"Hi {name}, reset your password",
        [
            "Someone asked to reset the password for this account. If it was you, choose a new "
            "one below. The link works once and expires in 30 minutes.",
            "Resetting signs you out on every device. If two-step verification is on, you'll "
            "still need a code to sign in.",
            "If you didn't ask for this, ignore this email. Your password stays the same.",
        ],
        ("Choose a new password", app_url(f"/reset-password?token={token}")),
    )


_ALERTS = {
    "password_reset": (
        "Your MedSpace password was reset",
        "Your password was reset",
        "Your password was changed using a reset link, and every device was signed out.",
    ),
    "password_changed": (
        "Your MedSpace password was changed",
        "Your password was changed",
        "Your password was changed from Settings. Other devices were signed out.",
    ),
    "mfa_enabled": (
        "Two-step verification is on",
        "Two-step verification is on",
        "Signing in to MedSpace now needs a code from your authenticator app.",
    ),
    "mfa_disabled": (
        "Two-step verification was turned off",
        "Two-step verification was turned off",
        "Your password alone is now enough to sign in to MedSpace.",
    ),
}


async def send_security_alert(to: str, name: str, kind: str) -> bool:
    subject, heading, what = _ALERTS[kind]
    return await _send(
        to,
        subject,
        f"Hi {name}. {heading}",
        [
            what,
            "If this wasn't you, reset your password now and review the devices signed in to "
            "your account in Settings, Security.",
        ],
        ("Open security settings", app_url("/app/settings#security")),
    )


# ---- Care circle --------------------------------------------------------------------------------

_ROLE_TEXT = {
    "viewer": "see their medicines, schedule, lab results, documents and visit preps",
    "helper": "see their records and help by ticking doses, to-dos and refills",
}


async def send_circle_invite(to: str, owner_name: str, role: str, url: str) -> bool:
    return await _send(
        to,
        f"{owner_name} invited you to their MedSpace care circle",
        f"{owner_name} invited you to their care circle",
        [
            f"As a {role}, you'll be able to {_ROLE_TEXT.get(role, 'see their records')}.",
            "Accept with a MedSpace account that uses this email address. The invitation works "
            "once and expires in 7 days.",
            "If you don't know this person, you can ignore this email.",
        ],
        ("View invitation", url),
    )
