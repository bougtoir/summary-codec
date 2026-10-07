"""Format adapter interface: transport/embedding only."""

from __future__ import annotations


class Adapter:
    name: str = ""

    def detect(self, data: bytes) -> bool:
        raise NotImplementedError

    def embed(self, visible_bytes: bytes, envelope: bytes) -> bytes:
        """Return container bytes carrying the envelope."""
        raise NotImplementedError

    def extract(self, container: bytes) -> bytes | None:
        """Return the embedded envelope bytes, or None if absent."""
        raise NotImplementedError

    def visible_bytes(self, container: bytes) -> bytes:
        """Bytes hashed as the visible representation V.

        SVG: the document with the codec metadata block removed.
        PNG/TIFF: the decoded pixel array.
        """
        raise NotImplementedError
