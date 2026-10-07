"""ScientificObject: abstract recoverable-object interface.

A subclass implements the scientific content only; transport, hashing,
signing, and level enforcement live in the shared core.
"""

from __future__ import annotations

import io
import json
import zlib

import numpy as np


class ScientificObject:
    #: registry key, matches MANIFEST_SCHEMA object_class enum
    object_class: str = ""
    #: human-readable equivalence rule used in the manifest contract
    equivalence_rule: str = ""

    def __init__(self, inputs: dict, title: str = "", rounding: str = "2"):
        self.inputs = inputs
        self.title = title or self.object_class
        self.rounding = rounding  # decimals for displayed numeric values

    # -- analysis ---------------------------------------------------------
    def analyze(self) -> dict:
        """Recompute the reported analysis from `self.inputs`."""
        raise NotImplementedError

    def displayed(self, results: dict) -> dict:
        """Map analysis results to the exact values rendered in V.

        Keys are stable cell labels; values are the post-rounding strings or
        numbers a reader sees.
        """
        raise NotImplementedError

    # -- secondary analysis (L3) -----------------------------------------
    def secondary_queries(self) -> dict:
        """Named zero-argument callables executed against the inputs."""
        return {}

    # -- canonical dataset (L4) ------------------------------------------
    def canonical_dataset(self) -> dict:
        """The canonical dataset that must be byte-identically recoverable."""
        return self.inputs

    # -- rendering --------------------------------------------------------
    def draw_figure(self, ax, displayed: dict) -> None:
        """Matplotlib drawing of the visible representation."""
        raise NotImplementedError

    def svg_body(self, displayed: dict) -> str:
        """SVG inner markup (shapes/text) for the visible representation."""
        raise NotImplementedError

    def render_svg(self, displayed: dict) -> bytes:
        body = self.svg_body(displayed)
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:sc="https://example.org/summary-codec" '
            'width="640" height="400" viewBox="0 0 640 400">'
            f'<title>{_esc(self.title)}</title>'
            f'<rect width="640" height="400" fill="white"/>'
            f"{body}</svg>"
        )
        return svg.encode("utf-8")

    def render_pixels(self, displayed: dict) -> np.ndarray:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=100)
        self.draw_figure(ax, displayed)
        fig.tight_layout()
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        from PIL import Image
        return np.asarray(Image.open(buf).convert("RGB"))

    # -- helpers ----------------------------------------------------------
    def fmt(self, x: float) -> str:
        return f"{float(x):.{int(self.rounding)}f}"


def _esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def encode_dataset_canonical(dataset: dict) -> bytes:
    """Canonical byte form of a recoverable dataset (L4)."""
    from ..core import canonical_json
    return canonical_json(dataset)


def compress_blob(obj) -> str:
    """Deflate+base64 blob for embedding (payload stays JSON inside)."""
    from ..core import canonical_json
    return zlib.compress(canonical_json(obj), 9).hex()


def decompress_blob(hexstr: str):
    return json.loads(zlib.decompress(bytes.fromhex(hexstr)).decode("utf-8"))
