"""Import every module's jobs so the registry in `app.shared.queue.JOBS` is complete."""

from app.modules.demo import jobs as demo_jobs  # noqa: F401
from app.modules.extraction import jobs as extraction_jobs  # noqa: F401
