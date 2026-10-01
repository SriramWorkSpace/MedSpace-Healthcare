"""File inspection: type sniffing by magic bytes, PDF text extraction and page rendering."""

from __future__ import annotations

from dataclasses import dataclass

import pymupdf

PDF = "application/pdf"
PNG = "image/png"
JPEG = "image/jpeg"
WEBP = "image/webp"
ALLOWED_TYPES = {PDF, PNG, JPEG, WEBP}

# A page needs at least this many characters of embedded text to skip the vision path.
TEXT_LAYER_MIN_CHARS = 40


def sniff_mime(data: bytes) -> str | None:
    """Identify the real file type from its leading bytes; never trust the client's claim."""
    if data.startswith(b"%PDF-"):
        return PDF
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return PNG
    if data.startswith(b"\xff\xd8\xff"):
        return JPEG
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return WEBP
    return None


@dataclass(slots=True)
class Inspection:
    page_count: int
    page_texts: list[str]
    has_text_layer: bool


class UnreadableFile(Exception):
    pass


def inspect(data: bytes, mime: str) -> Inspection:
    if mime != PDF:
        return Inspection(page_count=1, page_texts=[""], has_text_layer=False)
    try:
        with pymupdf.open(stream=data, filetype="pdf") as doc:
            if doc.needs_pass:
                raise UnreadableFile("This PDF is password protected.")
            texts = [page.get_text("text").strip() for page in doc]
    except UnreadableFile:
        raise
    except Exception as exc:  # corrupt or truncated PDF
        raise UnreadableFile("This PDF could not be opened. It may be damaged.") from exc
    has_text = bool(texts) and all(len(t) >= TEXT_LAYER_MIN_CHARS for t in texts)
    return Inspection(page_count=len(texts), page_texts=texts, has_text_layer=has_text)


def render_pages_png(data: bytes, mime: str, *, dpi: int = 144, max_pages: int = 30) -> list[bytes]:
    """PNG bytes per page for the vision model. Images are passed through (re-encoded as PNG)."""
    if mime != PDF:
        with pymupdf.open(stream=data) as img_doc:
            pix = img_doc[0].get_pixmap(dpi=dpi)
            return [pix.tobytes("png")]
    out: list[bytes] = []
    with pymupdf.open(stream=data, filetype="pdf") as doc:
        for i, page in enumerate(doc):
            if i >= max_pages:
                break
            out.append(page.get_pixmap(dpi=dpi).tobytes("png"))
    return out
