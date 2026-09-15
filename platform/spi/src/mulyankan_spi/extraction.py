"""Extraction SPI: text, embedded images, and a thumbnail out of a document.

Consumer: the ingestion pipeline (`mulyankan_platform.ingestion`).

Extraction reads what a document already carries — it never recognises,
infers, or generates. A page with no text layer yields an empty string and
says so through `PageExtraction.has_text_layer`; recovering that page is the
`ocr` SPI's job, not this one. Keeping the two apart is what lets the
deterministic path stay deterministic (ADR-0003): providers here declare
`deterministic=True` and the conformance suite holds them to it.

The provider is handed the document as bytes and returns a session, so a
multi-hundred-page book is opened once rather than per page. Nothing in this
interface knows where the bytes came from; storage is the platform's concern.

No implementation here may log, or place in an exception message, any text it
extracts — source material is Restricted (DAT-01, DAT-03).
"""

from __future__ import annotations

from dataclasses import dataclass
from types import TracebackType
from typing import Protocol, Self, runtime_checkable

from mulyankan_spi.descriptor import ProviderDescriptor


@dataclass(frozen=True)
class OutlineEntry:
    """One entry of a document's own table of contents."""

    level: int  # 1 = top level
    title: str
    start_page: int  # 1-based


@dataclass(frozen=True)
class DocumentInfo:
    """What the document declares about itself, before any page is read."""

    page_count: int
    outline: tuple[OutlineEntry, ...]


@dataclass(frozen=True)
class ExtractedImage:
    """One raster image embedded in a page, in the document's own encoding."""

    index: int  # 0-based, in page order
    width: int
    height: int
    media_type: str  # e.g. "image/png"
    data: bytes


@dataclass(frozen=True)
class PageExtraction:
    """Everything one page carries.

    `has_text_layer` is the honest signal the pipeline routes on: False means
    the page has no extractable text, not that the page is blank.
    """

    page: int  # 1-based
    text: str
    images: tuple[ExtractedImage, ...]

    @property
    def character_count(self) -> int:
        return len(self.text)

    @property
    def has_text_layer(self) -> bool:
        return bool(self.text.strip())


@dataclass(frozen=True)
class Thumbnail:
    """A rasterised page, deliberately lossy — a preview, not a reproduction."""

    width: int
    height: int
    media_type: str
    data: bytes


#: The encodings an embedded image may arrive in, mapped to the media type
#: the artefact is stored and served as. Lives in the SPI because the set is
#: part of the contract between provider and platform: the provider reports
#: `media_type`, the platform stores bytes under an extension derived from
#: it, and `mimetypes.guess_extension` cannot be trusted for the rarer ones
#: (`image/x-jb2` has no entry on Python 3.12 and would become `.bin`).
MEDIA_TYPE_EXTENSIONS: dict[str, str] = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jp2": ".jp2",
    "image/x-jb2": ".jb2",
    "image/bmp": ".bmp",
    "image/gif": ".gif",
    "image/tiff": ".tiff",
    "image/webp": ".webp",
}

_EXTENSION_MEDIA_TYPES = {ext: mt for mt, ext in MEDIA_TYPE_EXTENSIONS.items()}


def extension_for_media_type(media_type: str) -> str:
    """The file extension for a reported image media type.

    Unknown types map to `.bin` — an honest name for bytes the platform
    cannot classify, rather than a guess.
    """
    return MEDIA_TYPE_EXTENSIONS.get(media_type.lower(), ".bin")


def media_type_for_extension(extension: str) -> str:
    """The media type for a stored artefact's extension; `.bin` stays opaque."""
    return _EXTENSION_MEDIA_TYPES.get(extension.lower(), "application/octet-stream")


@runtime_checkable
class ExtractionSession(Protocol):
    """An open document. Close it, or use it as a context manager."""

    def info(self) -> DocumentInfo:
        """Page count and the document's own outline, if it has one."""
        ...

    def extract_page(self, page: int) -> PageExtraction:
        """Return the text and embedded images of `page` (1-based)."""
        ...

    def render_thumbnail(self, page: int, *, max_edge: int, quality: int) -> Thumbnail:
        """Rasterise `page` scaled to fit `max_edge`, lossily at `quality`.

        `max_edge` bounds the longer side in pixels and `quality` is 1-100.
        A preview is never rendered at source resolution: it exists to be
        shown on a card, so the provider must downscale rather than return
        the page at its natural size.
        """
        ...

    def close(self) -> None:
        """Release the document. Calling twice is not an error."""
        ...

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...


@runtime_checkable
class ExtractionProvider(Protocol):
    """Opens documents; holds no state between calls."""

    def describe(self) -> ProviderDescriptor:
        """Return the provider descriptor (name, version, data handling)."""
        ...

    def open(self, document: bytes) -> ExtractionSession:
        """Open `document`; raises `UnreadableDocument` if it cannot be read."""
        ...


class UnreadableDocument(Exception):
    """The bytes are not a document this provider can open.

    Carries no content — the message may name the format and the failure, and
    nothing the document says.
    """
