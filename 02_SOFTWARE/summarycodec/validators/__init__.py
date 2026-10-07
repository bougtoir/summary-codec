"""Level-aware validation: declared level -> mandatory validation suite."""

from __future__ import annotations

import numpy as np

from .. import crypto, decoders, formats
from ..core import (Level, Status, ValidationReport, canonical_json,
                    sha256_hex)
from ..objects import REGISTRY


def _close(a, b) -> bool:
    try:
        return np.isclose(float(a), float(b), rtol=1e-6, atol=1e-9,
                          equal_nan=True)
    except (TypeError, ValueError):
        return str(a) == str(b)


def _deep_equal(a, b) -> bool:
    """Order-insensitive deep equality with float tolerance."""
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_deep_equal(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_deep_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, float) or isinstance(b, float):
        if isinstance(a, str) or isinstance(b, str):
            return str(a) == str(b)
        try:
            return bool(np.isclose(float(a), float(b), rtol=1e-6, atol=1e-9,
                                   equal_nan=True))
        except (TypeError, ValueError):
            return str(a) == str(b)
    return a == b


def _displayed_match(d1: dict, d2: dict) -> bool:
    if set(d1) != set(d2):
        return False
    for k, v1 in d1.items():
        v2 = d2[k]
        if str(v1) == str(v2):
            continue
        if not _deep_equal(v1, v2):
            return False
    return True


def validate(path: str) -> ValidationReport:
    rep = ValidationReport(status=Status.VALID)
    with open(path, "rb") as fh:
        container = fh.read()

    adapter = formats.detect(container)
    if adapter is None:
        rep.status = Status.FORMAT_UNSUPPORTED
        rep.add("format_detected", False, "no adapter matched")
        return rep
    rep.add("format_detected", True, adapter.name)

    env = adapter.extract(container)
    if env is None:
        rep.status = Status.PAYLOAD_MISSING
        rep.add("envelope_present", False, "no Summary Codec envelope")
        return rep
    rep.add("envelope_present", True)

    try:
        import json
        env = json.loads(env.decode("utf-8"))
        manifest, payload, sig = env["manifest"], env["payload"], env["signature"]
    except Exception as e:
        rep.status = Status.CORRUPT
        rep.add("envelope_parses", False, str(e))
        return rep
    rep.add("envelope_parses", True)

    rep.object_id = manifest.get("object_id")
    rep.declared_level = manifest.get("declared_level")
    try:
        level = Level(manifest["declared_level"])
    except Exception:
        rep.status = Status.INVALID
        rep.add("declared_level_valid", False)
        return rep

    # ---- 1. file integrity / hash chain ----------------------------------
    payload_hash = sha256_hex(canonical_json(payload))
    payload_ok = payload_hash == manifest["payload_hash"]
    rep.add("payload_hash", payload_ok, payload_hash)
    visible_hash = sha256_hex(adapter.visible_bytes(container))
    visible_ok = visible_hash == manifest["visible_hash"]
    rep.add("visible_hash", visible_ok, visible_hash)

    m = {k: v for k, v in manifest.items()
         if k not in ("manifest_hash", "object_hash")}
    manifest_hash = sha256_hex(canonical_json(m))
    manifest_ok = manifest_hash == manifest["manifest_hash"]
    rep.add("manifest_hash", manifest_ok, manifest_hash)

    if not (payload_ok and manifest_ok):
        rep.status = Status.SIGNATURE_INVALID
        return rep

    # ---- 2. attribution ---------------------------------------------------
    pub = crypto.load_public_key(sig["public_key_pem"])
    sig_ok = crypto.verify(pub, manifest["manifest_hash"], payload_hash,
                           sig["sig"])
    rep.add("signature", sig_ok, "Ed25519")
    key_pinned = sig["public_key_pem"] == manifest["public_key_pem"]
    rep.add("public_key_matches_manifest", key_pinned)

    if not (sig_ok and key_pinned):
        rep.status = Status.SIGNATURE_INVALID
        return rep

    # ---- 3. semantic consistency -----------------------------------------
    try:
        obj = REGISTRY[payload["object_class"]](
            payload["inputs"], title=payload.get("title", ""),
            rounding=payload.get("rounding_rule", "2"))
    except Exception as e:
        rep.status = Status.INVALID
        rep.add("object_instantiated", False, str(e))
        return rep

    try:
        results = obj.analyze()
        recomputed_displayed = obj.displayed(results)
        sem_ok = _displayed_match(recomputed_displayed, payload["displayed"])
        rep.add("semantic_equivalence", sem_ok,
                "V'≡V under declared equivalence rule")
        if not sem_ok:
            rep.status = Status.SEMANTIC_MISMATCH
            return rep
    except Exception as e:
        rep.status = Status.INVALID
        rep.add("semantic_equivalence", False, f"recompute failed: {e}")
        return rep

    # ---- 4. level contracts ----------------------------------------------
    if level.rank >= 2:
        ok = _deep_equal(results, payload.get("analysis_results"))
        rep.add("analysis_reproduced", ok,
                "analysis re-run matches stored results")
        if not ok:
            rep.status = Status.LEVEL_NOT_SATISFIED
            return rep

    if level.rank >= 3:
        # L3 contract: the payload must carry the full prespecified
        # secondary-query family for this object class, and every
        # declared query must actually execute on the payload data.
        declared = payload.get("secondary_queries")
        available = obj.secondary_queries()
        if not declared:
            rep.add("secondary_queries_executable", False,
                    "payload carries no secondary_queries data")
            rep.status = Status.LEVEL_NOT_SATISFIED
            return rep
        declared = set(declared)
        uncovered = set(available) - declared
        unknown = declared - set(available)
        ok = not (uncovered or unknown)
        detail = "all declared queries executable"
        if uncovered:
            detail = f"prespecified family not covered: {sorted(uncovered)}"
        elif unknown:
            detail = f"unknown queries: {sorted(unknown)}"
        if ok:
            for name in sorted(declared):
                try:
                    _try_query(available[name])
                except Exception as e:
                    ok, detail = False, f"{name} failed: {e}"
                    break
        rep.add("secondary_queries_executable", ok, detail)
        if not ok:
            rep.status = Status.LEVEL_NOT_SATISFIED
            return rep

    if level.rank >= 4:
        # L4 contract: manifest contract + payload must carry a
        # canonical dataset hash that reconstructs byte-identically.
        from ..objects.base import encode_dataset_canonical
        canon_hash = sha256_hex(
            encode_dataset_canonical(obj.canonical_dataset()))
        contract = manifest.get("contract") or {}
        expected = contract.get("canonical_sha256")
        stored = payload.get("canonical_sha256")
        ok = expected is not None and stored is not None and \
            canon_hash == expected == stored
        detail = canon_hash if ok else \
            f"recomputed={canon_hash} manifest={expected} payload={stored}"
        rep.add("canonical_dataset_hash", ok, detail)
        if not ok:
            rep.status = Status.LEVEL_NOT_SATISFIED
            return rep

    if not visible_ok:
        rep.status = Status.PARTIALLY_VERIFIABLE
        return rep

    rep.status = Status.VALID
    return rep


def _try_query(fn):
    """Execute a declared secondary query (try a few common arities)."""
    for args in ((), (0,), (0.5,), (10,), (4,)):
        try:
            return fn(*args)
        except Exception:
            continue
    return fn()
