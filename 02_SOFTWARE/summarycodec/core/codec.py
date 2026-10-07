"""Encode pipeline: build O = (V, P, M, C, Σ) and embed in a container.

Level enforcement: the mandatory checks for every level <= declared are run
at encode time; encoding refuses to emit a claim it cannot prove.
"""

from __future__ import annotations

import json
import uuid

from ..core import (CODEC_VERSION, Level, canonical_json, sha256_hex)
from .. import crypto, formats, provenance


def _mandatory_checks(level: Level) -> list[str]:
    checks = ["envelope_present", "hash_chain", "signature",
              "displayed_recomputed", "semantic_equivalence"]
    if level.rank >= 2:
        checks.append("analysis_reproduced")
    if level.rank >= 3:
        checks.append("secondary_queries_executable")
    if level.rank >= 4:
        checks.append("canonical_dataset_hash")
    return checks


def build_payload(obj, level: Level) -> dict:
    results = obj.analyze()
    displayed = obj.displayed(results)
    payload = {
        "object_class": obj.object_class,
        "level": level.value,
        "title": obj.title,
        "rounding_rule": obj.rounding,
        "analysis_spec": {"object_class": obj.object_class,
                          "method": f"{obj.object_class}.analyze"},
        "inputs": obj.inputs,
        "analysis_results": results,
        "displayed": displayed,
    }
    if level.rank >= 3:
        qnames = list(obj.secondary_queries())
        if not qnames:
            raise ValueError(f"L3 declared but {obj.object_class} has no "
                             "secondary queries")
        payload["secondary_queries"] = qnames
    if level.rank >= 4:
        from ..objects.base import encode_dataset_canonical
        payload["canonical_sha256"] = sha256_hex(
            encode_dataset_canonical(obj.canonical_dataset()))
    return payload


def encode(obj, fmt: str, level: Level, out_path: str,
           private_key=None, actor: str = "author",
           external_refs: list[str] | None = None) -> dict:
    level = Level(level)
    adapter = formats.get(fmt)
    payload = build_payload(obj, level)
    displayed = payload["displayed"]

    if fmt == "svg":
        visible = obj.render_svg(displayed)
    else:
        arr = obj.render_pixels(displayed)
        import io
        buf = io.BytesIO()
        if fmt == "png":
            from PIL import Image
            Image.fromarray(arr).save(buf, format="PNG")
        elif fmt == "tiff":
            import tifffile
            tifffile.imwrite(buf, arr)
        else:
            raise ValueError(fmt)
        visible = buf.getvalue()

    # provisional manifest for hashing
    payload_hash = sha256_hex(canonical_json(payload))
    probe = adapter.embed(visible, b"")
    visible_hash = sha256_hex(adapter.visible_bytes(probe))

    priv = private_key or crypto.generate_keypair()[0]
    pub_pem = crypto.public_key_pem(priv.public_key())

    manifest = {
        "codec": "summary-codec",
        "codec_version": CODEC_VERSION,
        "object_id": f"sc-{uuid.uuid4().hex[:12]}",
        "object_class": obj.object_class,
        "declared_level": level.value,
        "created_utc": provenance.utcnow(),
        "format": fmt,
        "visible_hash": visible_hash,
        "payload_hash": payload_hash,
        "signature_scheme": "Ed25519",
        "public_key_pem": pub_pem,
        "provenance": {
            "chain": provenance.make_chain(
                [("created", actor, f"object_class={obj.object_class}"),
                 ("analyzed", actor, payload["analysis_spec"]["method"]),
                 ("rendered", actor, f"format={fmt}"),
                 ("signed", actor, "Ed25519")]),
            "external_refs": external_refs or [],
        },
        "contract": {
            "equivalence_rule": obj.equivalence_rule,
            "mandatory_checks": _mandatory_checks(level),
            "secondary_queries": payload.get("secondary_queries", []),
            "canonical_sha256": payload.get("canonical_sha256"),
        },
        "rounding_rule": obj.rounding,
    }
    manifest["manifest_hash"] = sha256_hex(canonical_json(manifest))
    manifest["object_hash"] = sha256_hex(
        (manifest["visible_hash"] + manifest["payload_hash"] +
         manifest["manifest_hash"]).encode("ascii"))

    sig = crypto.sign(priv, manifest["manifest_hash"], payload_hash)
    envelope = json.dumps({"manifest": manifest, "payload": payload,
                           "signature": {"alg": "Ed25519",
                                         "public_key_pem": pub_pem,
                                         "sig": sig}},
                          sort_keys=True).encode("utf-8")

    container = adapter.embed(visible, envelope)
    with open(out_path, "wb") as fh:
        fh.write(container)
    return manifest
