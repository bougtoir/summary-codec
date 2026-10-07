"""Core types: levels, validation statuses, canonical serialization, hashing."""

from __future__ import annotations

import enum
import hashlib
import json
from dataclasses import dataclass, field

CODEC_VERSION = "0.1.0"


class Level(str, enum.Enum):
    L0 = "L0"  # visual only
    L1 = "L1"  # display-recoverable
    L2 = "L2"  # analysis-reproducible
    L3 = "L3"  # secondary-analysis capable
    L4 = "L4"  # canonical data recoverable

    @property
    def rank(self) -> int:
        return int(self.value[1])


class Status(str, enum.Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    PARTIALLY_VERIFIABLE = "PARTIALLY_VERIFIABLE"
    PAYLOAD_MISSING = "PAYLOAD_MISSING"
    SIGNATURE_INVALID = "SIGNATURE_INVALID"
    SEMANTIC_MISMATCH = "SEMANTIC_MISMATCH"
    LEVEL_NOT_SATISFIED = "LEVEL_NOT_SATISFIED"
    FORMAT_UNSUPPORTED = "FORMAT_UNSUPPORTED"
    CORRUPT = "CORRUPT"


@dataclass
class ValidationReport:
    status: Status
    object_id: str | None = None
    declared_level: str | None = None
    checks: list[dict] = field(default_factory=list)

    def add(self, name: str, ok: bool, detail: str = "") -> bool:
        self.checks.append({"check": name, "ok": bool(ok), "detail": detail})
        return ok

    @property
    def ok(self) -> bool:
        return self.status == Status.VALID

    def to_dict(self) -> dict:
        return {
            "status": self.status.value,
            "object_id": self.object_id,
            "declared_level": self.declared_level,
            "checks": self.checks,
        }


def canonical_json(obj) -> bytes:
    """Deterministic JSON serialization used for all hashes/signatures."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()
