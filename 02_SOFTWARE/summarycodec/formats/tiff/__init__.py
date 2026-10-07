"""TIFF adapter: envelope in private tag 65000.

- Unchanged pixel array: tag is metadata, image data is byte-identical.
- Metadata-loss detection: tag absence -> PAYLOAD_MISSING.
"""

from __future__ import annotations

import io

import numpy as np
import tifffile

from ..base import Adapter

TAG = 65000  # private tag for the Summary Codec envelope


class TiffAdapter(Adapter):
    name = "tiff"

    def detect(self, data: bytes) -> bool:
        return data[:4] in (b"II*\x00", b"MM\x00*", b"II+\x00", b"MM\x00+")

    def embed(self, visible_bytes: bytes, envelope: bytes) -> bytes:
        arr = tifffile.imread(io.BytesIO(visible_bytes))
        buf = io.BytesIO()
        tifffile.imwrite(buf, arr,
                         extratags=[(TAG, "B", len(envelope), envelope, True)])
        return buf.getvalue()

    def extract(self, container: bytes) -> bytes | None:
        try:
            with tifffile.TiffFile(io.BytesIO(container)) as tf:
                tag = tf.pages[0].tags.get(TAG)
                if tag is None:
                    return None
                v = tag.value
                return bytes(v) if not isinstance(v, bytes) else v
        except Exception:
            return None

    def visible_bytes(self, container: bytes) -> bytes:
        arr = tifffile.imread(io.BytesIO(container))
        return np.asarray(arr).tobytes()
