from .svg import SvgAdapter
from .png import PngAdapter
from .tiff import TiffAdapter

ADAPTERS = {a.name: a for a in (SvgAdapter(), PngAdapter(), TiffAdapter())}


def get(name: str):
    return ADAPTERS[name]


def detect(data: bytes):
    for a in ADAPTERS.values():
        if a.detect(data):
            return a
    return None
