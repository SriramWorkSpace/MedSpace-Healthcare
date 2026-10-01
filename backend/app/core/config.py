"""Application settings, loaded from environment variables (and `.env` in development)."""

from __future__ import annotations

import base64
import hashlib
import json
from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


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
    redis_url: str = "redis://localhost:6379/0"
    queue_mode: Literal["inline", "arq"] = "inline"

    # --- Auth ----------------------------------------------------------------
    jwt_secret: SecretStr = SecretStr("dev-only-secret-change-me-please-0123456789")
    access_token_ttl_minutes: int = 15
    refresh_token_ttl_days: int = 14
    cookie_secure: bool = False
    cookie_domain: str | None = None
    token_encryption_key: SecretStr | None = None
    rate_limit_enabled: bool = True

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

    # --- Demo ----------------------------------------------------------------
    demo_enabled: bool = True
    demo_ttl_hours: int = 24

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value: object) -> object:
        if isinstance(value, str):
            if value.strip().startswith("["):
                return json.loads(value)
            return [o.strip() for o in value.split(",") if o.strip()]
        return value

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
