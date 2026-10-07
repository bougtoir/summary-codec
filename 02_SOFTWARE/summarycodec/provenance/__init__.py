"""Provenance chain model.

Ordered list of events (created / analyzed / rendered / signed /
attested / countersigned). Complementary to external provenance standards
(C2PA, RO-Crate): those track content history; this chain records the
scientific-object lifecycle only.
"""

from __future__ import annotations

from datetime import datetime, timezone


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def make_chain(events: list[tuple[str, str, str | None]] | None = None) -> list[dict]:
    chain = []
    for event, actor, detail in (events or []):
        chain.append({"event": event, "actor": actor, "at_utc": utcnow(),
                      "detail": detail or ""})
    return chain


def append(chain: list[dict], event: str, actor: str,
           detail: str | None = None) -> list[dict]:
    chain.append({"event": event, "actor": actor, "at_utc": utcnow(),
                  "detail": detail or ""})
    return chain
