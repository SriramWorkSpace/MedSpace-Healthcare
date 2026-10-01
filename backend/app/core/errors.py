"""Domain errors rendered as RFC 9457 `application/problem+json`."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("medspace.errors")

PROBLEM_JSON = "application/problem+json"


class AppError(Exception):
    status: int = 400
    code: str = "bad_request"
    title: str = "Bad request"

    def __init__(self, detail: str | None = None, *, extra: dict[str, Any] | None = None):
        super().__init__(detail or self.title)
        self.detail = detail or self.title
        self.extra = extra or {}


class NotFound(AppError):
    status, code, title = 404, "not_found", "Not found"


class Unauthorized(AppError):
    status, code, title = 401, "unauthorized", "Authentication required"


class Forbidden(AppError):
    status, code, title = 403, "forbidden", "Forbidden"


class Conflict(AppError):
    status, code, title = 409, "conflict", "Conflict"


class Unprocessable(AppError):
    status, code, title = 422, "unprocessable", "Unprocessable request"


class PayloadTooLarge(AppError):
    status, code, title = 413, "payload_too_large", "File too large"


class UnsupportedMedia(AppError):
    status, code, title = 415, "unsupported_media_type", "Unsupported file type"


class RateLimited(AppError):
    status, code, title = 429, "rate_limited", "Too many requests"


class Gone(AppError):
    status, code, title = 410, "gone", "No longer available"


class ServiceUnavailable(AppError):
    status, code, title = 503, "service_unavailable", "Service unavailable"


def _problem(status: int, code: str, title: str, detail: str, request: Request, **extra: Any):
    body = {
        "type": f"https://medspace.dev/problems/{code}",
        "title": title,
        "status": status,
        "detail": detail,
        "code": code,
        "instance": request.url.path,
        **extra,
    }
    return JSONResponse(body, status_code=status, media_type=PROBLEM_JSON)


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def _app_error(request: Request, exc: AppError):
        headers = (
            {"Retry-After": str(exc.extra["retry_after"])} if "retry_after" in exc.extra else None
        )
        resp = _problem(exc.status, exc.code, exc.title, exc.detail, request, **exc.extra)
        if headers:
            resp.headers.update(headers)
        return resp

    @app.exception_handler(RequestValidationError)
    async def _validation(request: Request, exc: RequestValidationError):
        errors = [
            {"loc": [str(p) for p in e.get("loc", ())], "msg": e.get("msg"), "type": e.get("type")}
            for e in exc.errors()
        ]
        return _problem(
            422,
            "validation_error",
            "Validation failed",
            "Some fields need attention.",
            request,
            errors=errors,
        )

    @app.exception_handler(StarletteHTTPException)
    async def _http(request: Request, exc: StarletteHTTPException):
        return _problem(exc.status_code, "http_error", str(exc.detail), str(exc.detail), request)

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception):
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        return _problem(500, "internal_error", "Something went wrong", "Unexpected error.", request)
