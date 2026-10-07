"""SVG adapter: envelope in a non-rendering <metadata> block.

- No visible change: <metadata> does not render in any conforming viewer.
- Metadata stripping is detected by envelope absence.
"""

from __future__ import annotations

import re

from ..base import Adapter

META_RE = re.compile(
    rb'<metadata\s+id="summary-codec"\s*>\s*<!\[CDATA\[(.*?)\]\]>\s*</metadata>',
    re.DOTALL)


class SvgAdapter(Adapter):
    name = "svg"

    def detect(self, data: bytes) -> bool:
        head = data.lstrip()[:400]
        return b"<svg" in head or head.startswith(b"<?xml")

    def embed(self, visible_bytes: bytes, envelope: bytes) -> bytes:
        if b"]]>" in envelope:
            raise ValueError("envelope contains CDATA terminator")
        doc = visible_bytes
        block = (b'<metadata id="summary-codec"><![CDATA[' + envelope +
                 b']]></metadata>')
        m = re.search(rb"<svg\b[^>]*>", doc)
        if not m:
            raise ValueError("not an SVG document")
        return doc[:m.end()] + block + doc[m.end():]

    def extract(self, container: bytes) -> bytes | None:
        m = META_RE.search(container)
        return m.group(1) if m else None

    def visible_bytes(self, container: bytes) -> bytes:
        return META_RE.sub(b"", container)
