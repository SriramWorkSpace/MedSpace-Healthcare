"""Application settings, loaded from environment variables (and `.env` in development)."""

from __future__ import annotations

import base64
import hashlib
import json
from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

# Development only: production refuses to start with it (see _safe_in_production).
DEV_JWT_SECRET = "dev-only-secret-change-me-please-0123456789"  # noqa: S105


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- App -----------------------------------------------------------------
    env: Literal["dev", "test", "prod"] = "dev"
    app_name: str = "MedSpace"
    log_level: str = "INFO"
    frontend_url: str = "http://localhost:5173"
    public_api_url: str = "http://localhost:8000"
    cors_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:5173"]
    )

    # --- Data ----------------------------------------------------------------
    database_url: str = "postgresql+asyncpg://medspace:medspace@localhost:5432/medspace"
    # Connections per API process. Keep pool + overflow under the database's limit (Supabase's free
    # session pooler allows about 15 clients): production uses 5 + 5.
    db_pool_size: int = 10
    db_max_overflow: int = 10
    redis_url: str = "redis://localhost:6379/0"
    queue_mode: Literal["inline", "arq"] = "inline"

    # --- Auth ----------------------------------------------------------------
    jwt_secret: SecretStr = SecretStr(DEV_JWT_SECRET)
    access_token_ttl_minutes: int = 15
    refresh_token_ttl_days: int = 14
    cookie_secure: bool = False
    cookie_domain: str | None = None
    token_encryption_key: SecretStr | None = None
    rate_limit_enabled: bool = True
    # memory: one process only. redis: shared by every API process (use it in production).
    rate_limit_backend: Literal["auto", "memory", "redis"] = "auto"
    # Multiplies every limit; >1 loosens limits for local e2e runs, never set below 1 in prod.
    rate_limit_scale: float = 1.0
    # Reverse proxies we run in front of the API (nginx = 1). 0 ignores X-Forwarded-For.
    trusted_proxy_hops: int = 0

    # --- Push reminders (ADR-028) ---------------------------------------------
    # auto: webpush when VAPID keys are set, otherwise a simulated sender (dev, demo, CI).
    push_provider: Literal["auto", "fake", "webpush"] = "auto"
    vapid_public_key: str | None = None
    vapid_private_key: SecretStr | None = None
    vapid_subject: str = "mailto:privacy@medspace.example"
    # Inline mode has no worker: run the once-a-minute reminder tick inside the API process.
    reminder_loop_enabled: bool = True

    # --- Email (ADR-030) ------------------------------------------------------
    # auto: Brevo with BREVO_API_KEY, SMTP with SMTP_HOST, else an in-memory outbox (dev, demo,
    # CI). Brevo sends over HTTPS, for hosts that block outbound SMTP ports (Render's free plan).
    mail_provider: Literal["auto", "fake", "smtp", "brevo"] = "auto"
    brevo_api_key: SecretStr | None = None
    mail_from: str = "MedSpace <no-reply@medspace.example>"
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: SecretStr | None = None
    smtp_security: Literal["starttls", "ssl", "none"] = "starttls"
    # Dev and CI only: GET /api/dev/outbox shows simulated emails (never enabled in prod).
    dev_outbox_enabled: bool = True

    # --- Storage -------------------------------------------------------------
    storage_provider: Literal["local", "s3"] = "local"
    storage_local_dir: str = ".data/storage"
    s3_endpoint_url: str | None = None
    s3_access_key: str | None = None
    s3_secret_key: SecretStr | None = None
    s3_bucket: str = "medspace-documents"
    s3_region: str = "us-east-1"
    max_upload_mb: int = 15
    max_pages: int = 30

    # --- AI ------------------------------------------------------------------
    llm_provider: Literal["fake", "groq"] = "fake"
    groq_api_key: SecretStr | None = None
    groq_text_model: str = "openai/gpt-oss-120b"
    groq_vision_model: str = "qwen/qwen3.8-27b"
    groq_chat_model: str = "openai/gpt-oss-120b"
    embedding_provider: Literal["hash", "fastembed"] = "hash"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    embedding_dim: int = 384

    # --- Google --------------------------------------------------------------
    google_provider: Literal["fake", "google"] = "fake"
    google_client_id: str | None = None
    google_client_secret: SecretStr | None = None
    # True while the OAuth consent screen is in Google's "Testing" status: only listed test users
    # can connect, and Google expires their refresh tokens after 7 days (they reconnect).
    google_oauth_testing: bool = True

    # --- Demo ----------------------------------------------------------------
    demo_enabled: bool = True
    demo_ttl_hours: int = 24
    # Live demo users at most (each demo is two users: the account and its family member), so a
    # public demo can't exhaust a free database or bucket between purges.
    demo_max_accounts: int = 400

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: object) -> object:
        if isinstance(value, str):
            if value.strip().startswith("["):
                return json.loads(value)
            return [o.strip() for o in value.split(",") if o.strip()]
        return value

    @model_validator(mode="after")
    def _safe_in_production(self) -> Settings:
        """Refuse to start in production with settings that would quietly be unsafe."""
        if self.env != "prod":
            return self
        problems = []
        secret = self.jwt_secret.get_secret_value()
        if secret == DEV_JWT_SECRET or len(secret) < 32:
            problems.append("JWT_SECRET must be a random value of at least 32 characters")
        if not (self.token_encryption_key and self.token_encryption_key.get_secret_value()):
            problems.append("TOKEN_ENCRYPTION_KEY must be set (a Fernet key)")
        if not self.cookie_secure:
            problems.append("COOKIE_SECURE must be true")
        if not self.frontend_url.startswith("https://"):
            problems.append("FRONTEND_URL must use https")
        if any(o == "*" or not o.startswith("https://") for o in self.cors_origins):
            problems.append("CORS_ORIGINS must list https origins only (no *)")
        if self.google_provider == "google" and not (
            self.google_client_id
            and self.google_client_secret
            and self.google_client_secret.get_secret_value()
        ):
            problems.append("GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET are required for Google")
        if not self.public_api_url.startswith("https://"):
            problems.append("PUBLIC_API_URL must use https (Google's redirect is built from it)")
        if any(h in self.database_url for h in ("@localhost", "@127.0.0.1")):
            problems.append("DATABASE_URL points at localhost: set the hosted database")
        if self.storage_provider != "s3":
            problems.append("STORAGE_PROVIDER must be s3: local disk loses files on redeploy")
        elif not (
            self.s3_access_key and self.s3_secret_key and self.s3_secret_key.get_secret_value()
        ):
            problems.append("S3_ACCESS_KEY and S3_SECRET_KEY must be set")
        elif self.s3_endpoint_url and not self.s3_endpoint_url.startswith("https://"):
            problems.append("S3_ENDPOINT_URL must use https")
        mail_ready = (
            self.mail_provider == "brevo"
            and self.brevo_api_key
            and self.brevo_api_key.get_secret_value()
        ) or (self.mail_provider == "smtp" and self.smtp_host)
        auto_ready = self.mail_provider == "auto" and (
            (self.brevo_api_key and self.brevo_api_key.get_secret_value()) or self.smtp_host
        )
        if not (mail_ready or auto_ready):
            problems.append(
                "email isn't configured (BREVO_API_KEY, or SMTP_HOST): without it resets and "
                "confirmations would silently go nowhere"
            )
        if problems:
            raise ValueError("Unsafe production settings: " + "; ".join(problems))
        return self

    @property
    def is_prod(self) -> bool:
        return self.env == "prod"

    @property
    def google_redirect_uri(self) -> str:
        return f"{self.public_api_url}/api/integrations/google/callback"

    @property
    def fernet_key(self) -> bytes:
        """Key for encrypting OAuth tokens at rest. Derived from JWT secret outside prod."""
        if self.token_encryption_key and self.token_encryption_key.get_secret_value():
            return self.token_encryption_key.get_secret_value().encode()
        digest = hashlib.sha256(self.jwt_secret.get_secret_value().encode()).digest()
        return base64.urlsafe_b64encode(digest)


@lru_cache
def get_settings() -> Settings:
    return Settings()
