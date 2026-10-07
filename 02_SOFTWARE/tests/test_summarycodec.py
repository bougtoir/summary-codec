"""Independent tests of the Summary Codec architecture."""

import io
import json
import os
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from summarycodec.objects import make, REGISTRY
from summarycodec.core.codec import encode
from summarycodec.core import Level, Status
from summarycodec.validators import validate
from summarycodec.decoders import decode, detect_and_extract
from summarycodec import crypto, formats

RNG = np.random.default_rng(42)

SPECS = {
    "mean_sd": {"groups": {"A": RNG.normal(5, 1, 25).tolist(),
                           "B": RNG.normal(6, 1.3, 30).tolist()}},
    "contingency": {"cells": [[40, 60], [15, 85]],
                    "row_labels": ["T", "C"], "col_labels": ["E", "N"]},
    "histogram": {"x": RNG.gamma(2, 2, 400).tolist(), "bins": 12},
    "survival": {"time": RNG.exponential(10, 60).tolist(),
                 "event": RNG.binomial(1, .7, 60).tolist()},
    "table1": {"records": [{"age": float(a), "sex": s, "arm": g}
                           for a, s, g in zip(RNG.normal(60, 10, 50),
                                              RNG.choice(["F", "M"], 50),
                                              RNG.choice(["T", "C"], 50))],
               "variables": [
                   {"name": "age", "kind": "continuous", "summary": "mean_sd",
                    "label": "Age"},
                   {"name": "sex", "kind": "categorical", "label": "Sex"}],
               "group_by": "arm"},
}
FORMATS = ["svg", "png", "tiff"]


@pytest.fixture(params=list(SPECS), ids=list(SPECS))
def obj(request):
    return make(request.param, SPECS[request.param], title="t")


@pytest.mark.parametrize("fmt", FORMATS)
@pytest.mark.parametrize("level", [Level.L1, Level.L2, Level.L3, Level.L4])
def test_roundtrip_valid(obj, fmt, level, tmp_path):
    p = str(tmp_path / f"o.{fmt}")
    encode(obj, fmt, level, p)
    assert validate(p).status == Status.VALID


@pytest.mark.parametrize("fmt", FORMATS)
def test_envelope_absent_is_payload_missing(obj, fmt, tmp_path):
    p = tmp_path / f"o.{fmt}"
    if fmt == "svg":
        p.write_bytes(obj.render_svg(obj.displayed(obj.analyze())))
    else:
        arr = obj.render_pixels(obj.displayed(obj.analyze()))
        if fmt == "png":
            from PIL import Image
            Image.fromarray(arr).save(p)
        else:
            import tifffile
            tifffile.imwrite(p, arr)
    assert validate(str(p)).status == Status.PAYLOAD_MISSING


def test_pixel_identity_png_tiff(obj, tmp_path):
    arr = obj.render_pixels(obj.displayed(obj.analyze()))
    for fmt in ("png", "tiff"):
        p = str(tmp_path / f"o.{fmt}")
        encode(obj, fmt, Level.L4, p)
        data = open(p, "rb").read()
        ad = formats.detect(data)
        stored = np.frombuffer(ad.visible_bytes(data),
                               dtype=np.uint8).reshape(arr.shape)
        assert (stored == arr).all()


def test_tampered_payload_rejected(tmp_path):
    obj = make("contingency", SPECS["contingency"])
    p = str(tmp_path / "o.svg")
    encode(obj, "svg", Level.L2, p)
    data = open(p, "rb").read()
    ad = formats.detect(data)
    env = json.loads(ad.extract(data))
    env["payload"]["displayed"]["risk1"] = "0.99"
    from summarycodec.formats.svg import META_RE
    tampered = ad.embed(META_RE.sub(b"", data), json.dumps(env).encode())
    open(p, "wb").write(tampered)
    assert validate(p).status == Status.SIGNATURE_INVALID


def test_level_enforcement_no_queries(tmp_path, monkeypatch):
    obj = make("mean_sd", SPECS["mean_sd"])
    monkeypatch.setattr(type(obj), "secondary_queries", lambda self: {})
    with pytest.raises(ValueError):
        encode(obj, "svg", Level.L3, str(tmp_path / "o.svg"))


def test_decode_recovers_displayed(tmp_path):
    obj = make("contingency", SPECS["contingency"])
    p = str(tmp_path / "o.png")
    encode(obj, "png", Level.L4, p)
    payload = decode(p)
    assert payload["displayed"]["treated|event" if "treated|event" in
           payload["displayed"] else "T|E"] == "40"


def test_cross_format_same_displayed(tmp_path):
    obj = make("histogram", SPECS["histogram"])
    disp = []
    for fmt in FORMATS:
        p = str(tmp_path / f"o.{fmt}")
        encode(obj, fmt, Level.L4, p)
        disp.append(decode(p)["displayed"])
    assert disp[0] == disp[1] == disp[2]


def test_signature_keypair_roundtrip():
    priv, pub = crypto.generate_keypair()
    sig = crypto.sign(priv, "sha256:" + "a" * 64, "sha256:" + "b" * 64)
    assert crypto.verify(pub, "sha256:" + "a" * 64, "sha256:" + "b" * 64, sig)
    assert not crypto.verify(pub, "sha256:" + "a" * 64, "sha256:" + "c" * 64,
                             sig)


def test_cli_encode_verify_decode(tmp_path):
    from summarycodec.cli import main
    inputs = tmp_path / "in.json"
    inputs.write_text(json.dumps(SPECS["contingency"]))
    out = tmp_path / "fig.svg"
    assert main(["encode", "--object", "contingency", "--format", "svg",
                 "--level", "L2", "--inputs", str(inputs),
                 "--out", str(out)]) == 0
    assert main(["verify", str(out)]) == 0
    assert main(["decode", str(out)]) == 0
    assert main(["reanalyze", str(out), "--query", "odds_ratio_recomputed"]) == 0


def _re_sign(env):
    """Forge a validly signed envelope after editing payload/manifest."""
    from summarycodec.core import canonical_json, sha256_hex
    priv, pub = crypto.generate_keypair()
    env["manifest"]["public_key_pem"] = crypto.public_key_pem(pub)
    env["manifest"]["payload_hash"] = sha256_hex(
        canonical_json(env["payload"]))
    env["manifest"]["manifest_hash"] = sha256_hex(canonical_json(
        {k: v for k, v in env["manifest"].items()
         if k not in ("manifest_hash", "object_hash")}))
    env["signature"]["public_key_pem"] = env["manifest"]["public_key_pem"]
    env["signature"]["sig"] = crypto.sign(
        priv, env["manifest"]["manifest_hash"],
        sha256_hex(canonical_json(env["payload"])))
    return env


def _rewrite(path, edit_fn):
    data = open(path, "rb").read()
    ad = formats.detect(data)
    env = _re_sign(edit_fn(json.loads(ad.extract(data))))
    from summarycodec.formats.svg import META_RE
    if ad.name == "svg":
        visible = META_RE.sub(b"", data)
    elif ad.name == "png":
        from summarycodec.formats.png import _chunks, PNG_SIG
        visible = bytearray(PNG_SIG)
        for pos, ctype, payload in _chunks(data):
            if ctype == b"scDC":
                continue
            visible += data[pos:pos + 12 + len(payload)]
        visible = bytes(visible)
    else:
        import tifffile
        arr = tifffile.imread(path)
        buf = io.BytesIO()
        tifffile.imwrite(buf, arr)
        visible = buf.getvalue()
    open(path, "wb").write(ad.embed(visible, json.dumps(env).encode()))


@pytest.mark.parametrize("fmt", FORMATS)
def test_semantic_mismatch_re_signed(tmp_path, fmt):
    """Insider forgery: valid signature + intact hashes, wrong displayed
    value. Only the semantic contract can catch this."""
    obj = make("contingency", SPECS["contingency"])
    p = str(tmp_path / f"o.{fmt}")
    encode(obj, fmt, Level.L4, p)

    def edit(env):
        k = sorted(env["payload"]["displayed"])[0]
        env["payload"]["displayed"][k] = "9999.99"
        return env
    _rewrite(p, edit)
    rep = validate(p)
    assert rep.status == Status.SEMANTIC_MISMATCH, rep.to_dict()


@pytest.mark.parametrize("fmt", FORMATS)
def test_l3_missing_query_data_rejected(tmp_path, fmt):
    obj = make("mean_sd", SPECS["mean_sd"])
    p = str(tmp_path / f"o.{fmt}")
    encode(obj, fmt, Level.L3, p)

    def edit(env):
        env["payload"].pop("secondary_queries", None)
        return env
    _rewrite(p, edit)
    rep = validate(p)
    assert rep.status == Status.LEVEL_NOT_SATISFIED
    assert any(c["check"] == "secondary_queries_executable" and not c["ok"]
               for c in rep.checks)


@pytest.mark.parametrize("fmt", FORMATS)
def test_l3_unknown_query_rejected(tmp_path, fmt):
    obj = make("mean_sd", SPECS["mean_sd"])
    p = str(tmp_path / f"o.{fmt}")
    encode(obj, fmt, Level.L3, p)

    def edit(env):
        env["payload"]["secondary_queries"] = ["nonexistent_query_xyz"]
        return env
    _rewrite(p, edit)
    assert validate(p).status == Status.LEVEL_NOT_SATISFIED


@pytest.mark.parametrize("fmt", FORMATS)
def test_l4_missing_contract_rejected(tmp_path, fmt):
    obj = make("histogram", SPECS["histogram"])
    p = str(tmp_path / f"o.{fmt}")
    encode(obj, fmt, Level.L4, p)

    def edit(env):
        env["manifest"].pop("contract", None)
        env["payload"].pop("canonical_sha256", None)
        return env
    _rewrite(p, edit)
    rep = validate(p)
    assert rep.status == Status.LEVEL_NOT_SATISFIED
    assert any(c["check"] == "canonical_dataset_hash" and not c["ok"]
               for c in rep.checks)


@pytest.mark.parametrize("fmt", FORMATS)
def test_l4_wrong_canonical_hash_rejected(tmp_path, fmt):
    obj = make("histogram", SPECS["histogram"])
    p = str(tmp_path / f"o.{fmt}")
    encode(obj, fmt, Level.L4, p)

    def edit(env):
        env["manifest"].setdefault("contract", {})[
            "canonical_sha256"] = "sha256:" + "0" * 64
        env["payload"]["canonical_sha256"] = "sha256:" + "0" * 64
        return env
    _rewrite(p, edit)
    assert validate(p).status == Status.LEVEL_NOT_SATISFIED
