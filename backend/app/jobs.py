"""Import every module's jobs so the registry in `app.shared.queue.JOBS` is complete."""

from app.modules.extraction import jobs as extraction_jobs  # noqa: F401
