"""HTTP middleware: security headers, CSRF double-submit check, request logging."""

from __future__ import annotations

import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.config import get_settings
from app.core.errors import PROBLEM_JSON
from app.core.security import ACCESS_COOKIE, CSRF_COOKIE, CSRF_HEADER, constant_time_equals

logger = logging.getLogger("medspace.http")

UNSAFE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
# Routes that establish a session (no CSRF cookie yet) or are public/token-authenticated.
CSRF_EXEMPT_PREFIXES = (
    "/api/auth/login",
    "/api/auth/signup",
    "/api/auth/demo",
    "/api/public/",
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault(
            "Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=()"
        )
        if not request.url.path.startswith(("/docs", "/redoc", "/openapi.json")):
            response.headers.setdefault(
                "Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'"
            )
        if get_settings().is_prod:
            response.headers.setdefault(
                "Strict-Transport-Security", "max-age=63072000; includeSubDomains"
            )
        return response


class CSRFMiddleware(BaseHTTPMiddleware):
    """Double-submit cookie check for cookie-authenticated unsafe requests.

    Requests authenticated with an `Authorization: Bearer` header (API clients, tests)
    are not vulnerable to CSRF and skip the check.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path
        if (
            request.method in UNSAFE_METHODS
            and path.startswith("/api/")
            and not path.startswith(CSRF_EXEMPT_PREFIXES)
            and not request.headers.get("authorization")
            and (request.cookies.get(ACCESS_COOKIE) or path.startswith("/api/auth/"))
        ):
            cookie = request.cookies.get(CSRF_COOKIE)
            header = request.headers.get(CSRF_HEADER)
            if not constant_time_equals(cookie, header):
                return JSONResponse(
                    {
                        "type": "https://medspace.dev/problems/csrf_failed",
                        "title": "CSRF check failed",
                        "status": 403,
                        "detail": "Missing or invalid CSRF token.",
                        "code": "csrf_failed",
                        "instance": path,
                    },
                    status_code=403,
                    media_type=PROBLEM_JSON,
                )
        return await call_next(request)


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get("x-request-id") or uuid.uuid4().hex[:12]
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "%s %s -> %s (%.1fms) rid=%s",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
            request_id,
        )
        return response
