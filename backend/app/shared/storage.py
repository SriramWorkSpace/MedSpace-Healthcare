"""Object storage port with filesystem and S3-compatible adapters."""

from __future__ import annotations

import asyncio
import shutil
from functools import lru_cache
from pathlib import Path
from typing import Protocol

from app.core.config import get_settings


class ObjectStorage(Protocol):
    async def put(self, key: str, data: bytes, content_type: str) -> None: ...
    async def get(self, key: str) -> bytes: ...
    async def delete(self, key: str) -> None: ...
    async def delete_prefix(self, prefix: str) -> None: ...


class LocalStorage:
    """Stores objects under a directory. Used for tests and keyless local runs."""

    def __init__(self, root: str) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        path = (self.root / key).resolve()
        if self.root not in path.parents:
            raise ValueError("Invalid storage key")
        return path

    async def put(self, key: str, data: bytes, content_type: str) -> None:
        path = self._path(key)
        await asyncio.to_thread(path.parent.mkdir, parents=True, exist_ok=True)
        await asyncio.to_thread(path.write_bytes, data)

    async def get(self, key: str) -> bytes:
        return await asyncio.to_thread(self._path(key).read_bytes)

    async def delete(self, key: str) -> None:
        await asyncio.to_thread(self._path(key).unlink, True)

    async def delete_prefix(self, prefix: str) -> None:
        path = self._path(prefix.rstrip("/"))
        await asyncio.to_thread(shutil.rmtree, path, True)


class S3Storage:
    """Any S3-compatible store (MinIO, Cloudflare R2, AWS S3). boto3 calls run in a thread."""

    def __init__(self) -> None:
        import boto3
        from botocore.config import Config

        s = get_settings()
        self.bucket = s.s3_bucket
        self.client = boto3.client(
            "s3",
            endpoint_url=s.s3_endpoint_url,
            aws_access_key_id=s.s3_access_key,
            aws_secret_access_key=s.s3_secret_key.get_secret_value() if s.s3_secret_key else None,
            region_name=s.s3_region,
            config=Config(signature_version="s3v4", retries={"max_attempts": 3}),
        )

    async def put(self, key: str, data: bytes, content_type: str) -> None:
        await asyncio.to_thread(
            self.client.put_object, Bucket=self.bucket, Key=key, Body=data, ContentType=content_type
        )

    async def get(self, key: str) -> bytes:
        obj = await asyncio.to_thread(self.client.get_object, Bucket=self.bucket, Key=key)
        return await asyncio.to_thread(obj["Body"].read)

    async def delete(self, key: str) -> None:
        await asyncio.to_thread(self.client.delete_object, Bucket=self.bucket, Key=key)

    async def delete_prefix(self, prefix: str) -> None:
        def _purge() -> None:
            paginator = self.client.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
                keys = [{"Key": o["Key"]} for o in page.get("Contents", [])]
                if keys:
                    self.client.delete_objects(Bucket=self.bucket, Delete={"Objects": keys})

        await asyncio.to_thread(_purge)


@lru_cache
def get_storage() -> ObjectStorage:
    settings = get_settings()
    if settings.storage_provider == "s3":
        return S3Storage()
    return LocalStorage(settings.storage_local_dir)
