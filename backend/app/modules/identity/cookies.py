"""Auth cookie helpers shared by the identity and demo routers."""

from __future__ import annotations

from fastapi import Response

from app.core.config import get_settings
from app.core.security import ACCESS_COOKIE, CSRF_COOKIE, REFRESH_COOKIE, new_opaque_token

REFRESH_PATH = "/api/auth"


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> str:
    """Set access, refresh and CSRF cookies. Returns the CSRF token (also echoed in the body)."""
    settings = get_settings()
    common = {"secure": settings.cookie_secure, "domain": settings.cookie_domain, "samesite": "lax"}
    response.set_cookie(
        ACCESS_COOKIE,
        access_token,
        max_age=settings.access_token_ttl_minutes * 60,
        httponly=True,
        path="/",
        **common,
    )
    response.set_cookie(
        REFRESH_COOKIE,
        refresh_token,
        max_age=settings.refresh_token_ttl_days * 86400,
        httponly=True,
        path=REFRESH_PATH,
        **common,
    )
    csrf = new_opaque_token(24)
    response.set_cookie(
        CSRF_COOKIE,
        csrf,
        max_age=settings.refresh_token_ttl_days * 86400,
        httponly=False,
        path="/",
        **common,
    )
    return csrf


def clear_auth_cookies(response: Response) -> None:
    settings = get_settings()
    response.delete_cookie(ACCESS_COOKIE, path="/", domain=settings.cookie_domain)
    response.delete_cookie(REFRESH_COOKIE, path=REFRESH_PATH, domain=settings.cookie_domain)
    response.delete_cookie(CSRF_COOKIE, path="/", domain=settings.cookie_domain)
