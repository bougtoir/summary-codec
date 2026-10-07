"""Portable decoder: detect format, extract envelope, reconstruct payload."""

from __future__ import annotations

import json

from .. import formats
from ..core import Status


def detect_and_extract(path: str):
    """Return (adapter, envelope_dict) or (adapter_or_None, None)."""
    with open(path, "rb") as fh:
        data = fh.read()
    adapter = formats.detect(data)
    if adapter is None:
        return None, None
    env = adapter.extract(data)
    if env is None:
        return adapter, None
    try:
        return adapter, json.loads(env.decode("utf-8"))
    except Exception:
        return adapter, {"__corrupt__": True}


def decode(path: str) -> dict:
    """Return the payload of an encoded object."""
    adapter, env = detect_and_extract(path)
    if adapter is None:
        raise ValueError(Status.FORMAT_UNSUPPORTED.value)
    if env is None:
        raise ValueError(Status.PAYLOAD_MISSING.value)
    if env.get("__corrupt__"):
        raise ValueError(Status.CORRUPT.value)
    return env["payload"]


def visible_bytes(path: str) -> bytes:
    with open(path, "rb") as fh:
        data = fh.read()
    adapter = formats.detect(data)
    if adapter is None:
        raise ValueError(Status.FORMAT_UNSUPPORTED.value)
    return adapter.visible_bytes(data)
