"""HTTP middleware: security headers, CSRF double-submit check, request logging."""

from __future__ import annotations

import logging
import re
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
    "/api/push/actions",  # notification buttons: a signed token, never cookies
    "/api/auth/login",
    "/api/auth/signup",
    "/api/auth/demo",
    "/api/auth/password/",  # forgot (anyone may ask) and reset (the emailed token is the proof)
    "/api/auth/email/verify",  # the emailed token is the proof
    "/api/auth/email/change/confirm",  # likewise
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


# Path segments that are credentials: share links and care circle invitations.
_TOKEN_PATHS = re.compile(r"^(/api/public/shares/|/api/circle/invites/)[^/]+")


def safe_path(path: str) -> str:
    """The request path with secret tokens replaced, for logs."""
    return _TOKEN_PATHS.sub(r"\1<token>", path)


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
            safe_path(request.url.path),
            response.status_code,
            elapsed_ms,
            request_id,
        )
        return response


class _BodyTooLarge(Exception):
    pass


class BodySizeLimitMiddleware:
    """Reject request bodies over `max_bytes` as they stream in, before anything buffers them
    (multipart parsing would otherwise spool a huge upload to disk first)."""

    def __init__(self, app, max_bytes: int) -> None:
        self.app = app
        self.max_bytes = max_bytes

    async def _too_large(self, send) -> None:
        body = (
            b'{"type":"about:blank","title":"File too large","status":413,'
            b'"detail":"That request is too large.","code":"payload_too_large"}'
        )
        await send(
            {
                "type": "http.response.start",
                "status": 413,
                "headers": [(b"content-type", b"application/problem+json")],
            }
        )
        await send({"type": "http.response.body", "body": body})

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        declared = dict(scope.get("headers") or []).get(b"content-length")
        if declared and declared.isdigit() and int(declared) > self.max_bytes:
            return await self._too_large(send)
        received = 0
        started = False
        tripped = False
        replaced = False

        async def limited_receive():
            nonlocal received, tripped
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > self.max_bytes:
                    tripped = True
                    raise _BodyTooLarge
            return message

        async def guarded_send(message):
            # Body parsers may catch the overflow and answer 400 themselves; once the limit has
            # tripped, the client gets the honest 413 instead of whatever the app says.
            nonlocal started, replaced
            if message["type"] == "http.response.start":
                started = True
                if tripped:
                    replaced = True
                    await self._too_large(send)
                    return
            elif replaced:
                return
            await send(message)

        try:
            await self.app(scope, limited_receive, guarded_send)
        except _BodyTooLarge:
            if not started:
                await self._too_large(send)
