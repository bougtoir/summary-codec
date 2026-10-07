"""PNG adapter: envelope in a private ancillary chunk 'scDC'.

- Exact pixel identity: ancillary chunks are invisible to renderers.
- Ordinary viewer compatibility: unknown ancillary chunks are skipped.
- Metadata-loss detection: chunk absence -> PAYLOAD_MISSING.
"""

from __future__ import annotations

import binascii
import io
import struct

import numpy as np

from ..base import Adapter

PNG_SIG = b"\x89PNG\r\n\x1a\n"
CHUNK_TYPE = b"scDC"  # ancillary(1) private(c) reserved-ok(D) safe-to-copy(C)


def _chunk(ctype: bytes, data: bytes) -> bytes:
    return (struct.pack(">I", len(data)) + ctype + data +
            struct.pack(">I", binascii.crc32(ctype + data) & 0xFFFFFFFF))


def _chunks(data: bytes):
    pos = len(PNG_SIG)
    while pos < len(data):
        (ln,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        yield pos, ctype, data[pos + 8:pos + 8 + ln]
        pos += 12 + ln


class PngAdapter(Adapter):
    name = "png"

    def detect(self, data: bytes) -> bool:
        return data.startswith(PNG_SIG)

    def embed(self, visible_bytes: bytes, envelope: bytes) -> bytes:
        out = bytearray(PNG_SIG)
        for pos, ctype, payload in _chunks(visible_bytes):
            if ctype == b"IEND":
                out += _chunk(CHUNK_TYPE, envelope)
            ln = len(payload)
            out += visible_bytes[pos:pos + 12 + ln]
        return bytes(out)

    def extract(self, container: bytes) -> bytes | None:
        if not self.detect(container):
            return None
        for pos, ctype, payload in _chunks(container):
            if ctype == CHUNK_TYPE:
                return payload
        return None

    def visible_bytes(self, container: bytes) -> bytes:
        from PIL import Image
        img = Image.open(io.BytesIO(container)).convert("RGB")
        return np.asarray(img).tobytes()
