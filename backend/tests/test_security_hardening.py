"""Hardening for public deployment: production settings, push hosts, log redaction, upload and
image limits, demo caps."""

from __future__ import annotations

import logging
import struct

import httpx
import pytest

from app.core.config import DEV_JWT_SECRET, Settings, get_settings
from app.core.middleware import safe_path
from app.modules.documents import files
from tests.conftest import csrf
from tests.test_documents_flow import upload

GOOD_PROD = {
    "env": "prod",
    "jwt_secret": "x" * 48,
    "token_encryption_key": "k" * 44,
    "cookie_secure": True,
    "frontend_url": "https://medspace.example.org",
    "cors_origins": ["https://medspace.example.org"],
    "public_api_url": "https://medspace.example.org",
    "database_url": "postgresql+asyncpg://u:p@db.example.org:5432/postgres?ssl=require",
    "storage_provider": "s3",
    "s3_endpoint_url": "https://account.r2.cloudflarestorage.com",
    "s3_access_key": "access",
    "s3_secret_key": "secret",
    "mail_provider": "brevo",
    "brevo_api_key": "xkeysib-test",
}


# ---- 1. Production refuses unsafe settings ------------------------------------------------------


def test_safe_production_settings_start():
    assert Settings(_env_file=None, **GOOD_PROD).is_prod


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"jwt_secret": DEV_JWT_SECRET}, "JWT_SECRET"),
        ({"jwt_secret": "short"}, "JWT_SECRET"),
        ({"token_encryption_key": None}, "TOKEN_ENCRYPTION_KEY"),
        ({"cookie_secure": False}, "COOKIE_SECURE"),
        ({"frontend_url": "http://medspace.example.org"}, "FRONTEND_URL"),
        ({"cors_origins": ["*"]}, "CORS_ORIGINS"),
        ({"storage_provider": "local"}, "STORAGE_PROVIDER"),
        ({"public_api_url": "http://localhost:8000"}, "PUBLIC_API_URL"),
        ({"database_url": "postgresql+asyncpg://m:m@localhost:5432/m"}, "DATABASE_URL"),
        ({"s3_secret_key": None}, "S3_SECRET_KEY"),
        ({"s3_endpoint_url": "http://localhost:8333"}, "S3_ENDPOINT_URL"),
        ({"brevo_api_key": None}, "email isn't configured"),
        ({"mail_provider": "auto", "brevo_api_key": None}, "email isn't configured"),
        ({"mail_provider": "fake"}, "email isn't configured"),
    ],
)
def test_unsafe_production_settings_refuse_to_start(change, message):
    with pytest.raises(ValueError, match=message):
        Settings(_env_file=None, **{**GOOD_PROD, **change})


def test_development_keeps_its_convenient_defaults():
    assert not Settings(_env_file=None, env="dev").is_prod


# ---- 2. Push endpoints ---------------------------------------------------------------------------

KEYS = {
    "p256dh": "BNcRdreALRFXTkOOUHK1EtK2wtaz5Ry4YfYCA_0QTpQtUbVlUls0VJXg7A8u-Ts1Xbjhaz"
    "Akj7I99e8QcYP7DkM",
    "auth": "tBHItJI5svbpez7KI4CCXg",
}


@pytest.mark.parametrize(
    "endpoint",
    [
        "https://fcm.googleapis.com/fcm/send/abc",
        "https://updates.push.services.mozilla.com/wpush/v2/abc",
        "https://wns2-par02p.notify.windows.com/w/?token=abc",
        "https://web.push.apple.com/abc",
    ],
)
async def test_browser_push_services_are_accepted(auth_client: httpx.AsyncClient, endpoint):
    resp = await auth_client.post(
        "/api/push/subscriptions",
        json={"endpoint": endpoint, "keys": KEYS},
        headers=csrf(auth_client),
    )
    assert resp.status_code == 201, resp.text


@pytest.mark.parametrize(
    "endpoint",
    [
        "https://evil.example.net/collect",
        "https://169.254.169.254/latest/meta-data",
        "https://localhost/admin",
        "https://fcm.googleapis.com.evil.net/x",
        "https://notify.windows.com.evil.net/x",
    ],
)
async def test_arbitrary_hosts_are_refused(auth_client: httpx.AsyncClient, endpoint):
    resp = await auth_client.post(
        "/api/push/subscriptions",
        json={"endpoint": endpoint, "keys": KEYS},
        headers=csrf(auth_client),
    )
    assert resp.status_code == 422


def test_test_push_host_is_refused_in_production(monkeypatch):
    from app.modules.reminders.schemas import SubscriptionIn

    monkeypatch.setattr(get_settings(), "env", "prod")
    with pytest.raises(ValueError):
        SubscriptionIn(endpoint="https://push.example.com/x", keys=KEYS)


# ---- 3. Tokens never reach the logs --------------------------------------------------------------


def test_token_paths_are_redacted():
    assert safe_path("/api/public/shares/abcDEF123_-xyz") == "/api/public/shares/<token>"
    assert (
        safe_path("/api/public/shares/abc123/documents/1/file")
        == "/api/public/shares/<token>/documents/1/file"
    )
    assert safe_path("/api/circle/invites/tok_123") == "/api/circle/invites/<token>"
    assert safe_path("/api/documents/123") == "/api/documents/123"


async def test_request_log_never_contains_a_share_token(
    client: httpx.AsyncClient, caplog: pytest.LogCaptureFixture
):
    caplog.set_level(logging.INFO)
    await client.get("/api/public/shares/super-secret-token-value-123")
    server_lines = " | ".join(
        r.getMessage() for r in caplog.records if r.name.startswith("medspace")
    )  # the test's own HTTP client logs URLs too; only the server's logs matter here
    assert "/api/public/shares/<token>" in server_lines
    assert "super-secret-token-value-123" not in server_lines


# ---- 4. Image limits -----------------------------------------------------------------------------


def png_header(w: int, h: int) -> bytes:
    ihdr = struct.pack(">II", w, h) + b"\x08\x02\x00\x00\x00"
    return b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + ihdr + b"\x00" * 4


def webp(chunk: bytes, payload: bytes) -> bytes:
    body = chunk + struct.pack("<I", len(payload)) + payload
    return b"RIFF" + struct.pack("<I", 4 + len(body)) + b"WEBP" + body


def test_image_sizes_are_read_from_headers():
    assert files.image_size(png_header(1234, 567), files.PNG) == (1234, 567)
    jpeg = (
        b"\xff\xd8\xff\xe0" + struct.pack(">H", 16) + b"JFIF\x00" + b"\x00" * 9
        + b"\xff\xc0" + struct.pack(">HBHH", 17, 8, 567, 1234) + b"\x03" + b"\x00" * 9
    )  # fmt: skip
    assert files.image_size(jpeg, files.JPEG) == (1234, 567)
    lossless = webp(b"VP8L", b"\x2f" + struct.pack("<I", (1234 - 1) | ((567 - 1) << 14)))
    assert files.image_size(lossless, files.WEBP) == (1234, 567)
    extended = webp(
        b"VP8X",
        b"\x00\x00\x00\x00" + (1234 - 1).to_bytes(3, "little") + (567 - 1).to_bytes(3, "little"),
    )
    assert files.image_size(extended, files.WEBP) == (1234, 567)
    lossy = webp(b"VP8 ", b"\x00\x00\x00\x9d\x01\x2a" + struct.pack("<HH", 1234, 567))
    assert files.image_size(lossy, files.WEBP) == (1234, 567)
    assert files.image_size(b"\x89PNG\r\n\x1a\n", files.PNG) is None


async def test_decompression_bombs_are_refused(auth_client: httpx.AsyncClient):
    resp = await upload(auth_client, png_header(50_000, 50_000), "bomb.png")
    assert resp.status_code == 422
    assert "too large in pixels" in resp.json()["detail"]
    tall = await upload(auth_client, png_header(800, 20_000), "tall.png")
    assert tall.status_code == 422


def test_rendering_is_capped_for_huge_pages():
    import pymupdf

    doc = pymupdf.open()
    doc.new_page(width=14_400, height=14_400)  # a 200-inch page
    data = doc.tobytes()
    [png] = files.render_pages_png(data, files.PDF, dpi=144)
    pix = pymupdf.Pixmap(png)
    assert max(pix.width, pix.height) <= files.MAX_RENDER_SIDE


# ---- 5. Request size -----------------------------------------------------------------------------


async def test_oversized_bodies_are_refused_before_buffering(auth_client: httpx.AsyncClient):
    limit = (get_settings().max_upload_mb + 1) * 1024 * 1024
    resp = await auth_client.post(
        "/api/documents",
        content=b"x" * (limit + 1),
        headers={**csrf(auth_client), "Content-Type": "application/octet-stream"},
    )
    assert resp.status_code == 413


async def test_chunked_bodies_are_counted_too(auth_client: httpx.AsyncClient):
    limit = (get_settings().max_upload_mb + 1) * 1024 * 1024

    async def chunks():  # a well-formed part whose file never ends
        yield (
            b'--xyz\r\nContent-Disposition: form-data; name="file"; filename="big.pdf"\r\n'
            b"Content-Type: application/pdf\r\n\r\n"
        )
        for _ in range(limit // (1024 * 1024) + 2):
            yield b"x" * (1024 * 1024)

    resp = await auth_client.post(
        "/api/documents",
        content=chunks(),  # no Content-Length: only counting the stream can stop it
        headers={**csrf(auth_client), "Content-Type": "multipart/form-data; boundary=xyz"},
    )
    assert resp.status_code == 413


# ---- 6. Demo caps ------------------------------------------------------------------------------


async def test_demo_is_capped_overall(client: httpx.AsyncClient, monkeypatch):
    monkeypatch.setattr(get_settings(), "demo_max_accounts", 2)
    first = await client.post("/api/auth/demo")  # creates the demo user and its family member
    assert first.status_code == 201
    client.cookies.clear()
    busy = await client.post("/api/auth/demo")
    assert busy.status_code == 503
    assert "busy" in busy.json()["detail"]


# ---- 7. Database pool fits a hosted pooler's limit ----------------------------------------------


def test_database_pool_size_comes_from_settings():
    from app.core.db import engine

    s = get_settings()
    assert engine.pool.size() == s.db_pool_size
    assert engine.pool._max_overflow == s.db_max_overflow
    small = Settings(_env_file=None, db_pool_size=5, db_max_overflow=5)
    assert small.db_pool_size + small.db_max_overflow <= 15  # Supabase free session pooler


# ---- 8. Storage works with a least-privilege, object-only token --------------------------------


class _StubS3:
    def __init__(self, head_status: int) -> None:
        self.head_status = head_status
        self.created = False
        self.put = False

    def head_bucket(self, Bucket):
        from botocore.exceptions import ClientError

        raise ClientError(
            {
                "Error": {"Code": str(self.head_status)},
                "ResponseMetadata": {"HTTPStatusCode": self.head_status},
            },
            "HeadBucket",
        )

    def create_bucket(self, Bucket):
        self.created = True

    def put_object(self, **kwargs):
        self.put = True


@pytest.mark.parametrize(("head_status", "creates"), [(403, False), (404, True)])
async def test_bucket_is_created_only_when_missing(head_status, creates):
    from app.shared.storage import S3Storage

    store = S3Storage.__new__(S3Storage)
    store.bucket, store._bucket_ready = "medspace-documents", False
    store.client = _StubS3(head_status)
    await store.put("users/x/doc.pdf", b"%PDF", "application/pdf")
    assert store.client.created is creates  # a 403 means "exists, not yours to inspect"
    assert store.client.put


def test_production_accepts_smtp_or_auto_mail_too():
    assert Settings(_env_file=None, **{**GOOD_PROD, "mail_provider": "auto"}).is_prod
    smtp = {**GOOD_PROD, "mail_provider": "smtp", "brevo_api_key": None, "smtp_host": "smtp.x.org"}
    assert Settings(_env_file=None, **smtp).is_prod
