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


MAX_IMAGE_PIXELS = 40_000_000  # ~ a 48 MP phone photo is fine; decompression bombs aren't
MAX_IMAGE_SIDE = 12_000
MAX_RENDER_SIDE = 4_000  # pixels on the longest side of any rendered page


def image_size(data: bytes, mime: str) -> tuple[int, int] | None:
    """(width, height) read from the file header, without decoding the image."""
    try:
        if mime == PNG and data[12:16] == b"IHDR":
            return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
        if mime == JPEG:
            i = 2
            while i + 9 < len(data):
                if data[i] != 0xFF:
                    return None
                marker = data[i + 1]
                length = int.from_bytes(data[i + 2 : i + 4], "big")
                # Start-of-frame markers carry the size (not DHT C4, JPG C8 or DAC CC).
                if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                    h = int.from_bytes(data[i + 5 : i + 7], "big")
                    w = int.from_bytes(data[i + 7 : i + 9], "big")
                    return w, h
                i += 2 + length
            return None
        if mime == WEBP:
            chunk = data[12:16]
            if chunk == b"VP8X":
                return int.from_bytes(data[24:27], "little") + 1, int.from_bytes(
                    data[27:30], "little"
                ) + 1
            if chunk == b"VP8L":
                bits = int.from_bytes(data[21:25], "little")
                return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
            if chunk == b"VP8 ":
                return int.from_bytes(data[26:28], "little") & 0x3FFF, int.from_bytes(
                    data[28:30], "little"
                ) & 0x3FFF
    except (IndexError, ValueError):
        return None
    return None


def _matrix(rect: pymupdf.Rect, dpi: int) -> pymupdf.Matrix:
    """Render at `dpi`, but never past MAX_RENDER_SIDE pixels (oversized pages can't exhaust
    memory)."""
    zoom = dpi / 72
    longest = max(rect.width, rect.height) or 1
    zoom = min(zoom, MAX_RENDER_SIDE / longest)
    return pymupdf.Matrix(zoom, zoom)


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
            page = img_doc[0]
            return [page.get_pixmap(matrix=_matrix(page.rect, dpi)).tobytes("png")]
    out: list[bytes] = []
    with pymupdf.open(stream=data, filetype="pdf") as doc:
        for i, page in enumerate(doc):
            if i >= max_pages:
                break
            out.append(page.get_pixmap(matrix=_matrix(page.rect, dpi)).tobytes("png"))
    return out
