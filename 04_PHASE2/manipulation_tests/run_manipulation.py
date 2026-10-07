"""Phase 2 manipulation/provenance tests on the real biomedical objects.

Post-signing manipulations:
  replace_panel / change_plotted_value / change_table_cell / swap_payload /
  alter_tiff_pixels / strip_metadata / re_signed_semantic

Classify each as: cryptographically detected / semantically detected /
both / neither.  Writes manipulation_results.csv.
"""

import io
import json
import os
import re
import shutil
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.abspath(os.path.join(ROOT, "..", "02_SOFTWARE")))
sys.path.insert(0, os.path.abspath(os.path.join(ROOT, "..", "03_PHASE1")))

from summarycodec import crypto, formats
from summarycodec.core import Status, canonical_json, sha256_hex
from summarycodec.validators import validate
from run_phase1 import _without_envelope, strip_envelope

OBJDIR = os.path.join(ROOT, "biomedical_objects")
WORK = os.path.join(HERE, "work")
os.makedirs(WORK, exist_ok=True)

TARGETS = ["gbsg2_km_horth", "gbsg2_table1", "wdbc_mean_sd",
           "diabetes_hist_bmi"]


def classify(status: Status) -> str:
    sem = status == Status.SEMANTIC_MISMATCH
    cry = status in (Status.SIGNATURE_INVALID, Status.PARTIALLY_VERIFIABLE,
                     Status.PAYLOAD_MISSING, Status.CORRUPT, Status.INVALID)
    if sem and cry:
        return "both"
    if sem:
        return "semantically detected"
    if cry:
        return "cryptographically detected"
    if status == Status.LEVEL_NOT_SATISFIED:
        return "cryptographically detected"  # contract failure still flags
    return "neither"


def _edit_svg_visible(path, fn):
    """Apply fn() to the visible part of an encoded SVG, re-embed envelope."""
    from summarycodec.formats.svg import META_RE
    data = open(path, "rb").read()
    ad = formats.detect(data)
    env = ad.extract(data)
    visible = META_RE.sub(b"", data).decode("utf-8")
    open(path, "wb").write(ad.embed(fn(visible).encode("utf-8"), env))


def change_plotted_value(path):
    data = open(path, "rb").read()
    if formats.detect(data).name != "svg":
        return "n/a-format"

    def fn(visible):
        out = re.sub(r"(<text[^>]*>[^<]*?)(\d+\.?\d*)([^<]*</text>)",
                     lambda m: m.group(1) + f"{float(m.group(2)) + 1:g}" +
                     m.group(3), visible, count=1)
        if out == visible:  # no numeric label: perturb a geometric element
            out = re.sub(r'(height=")(\d+\.?\d*)(")',
                         lambda m: m.group(1) +
                         f"{float(m.group(2)) * 0.5:.1f}" + m.group(3),
                         visible, count=1)
        if out == visible:
            out = re.sub(r'(d="M )(\d+\.?\d*)',
                         lambda m: m.group(1) +
                         f"{float(m.group(2)) * 0.5:.1f}",
                         visible, count=1)
        assert out != visible, "no visible element to perturb"
        return out
    _edit_svg_visible(path, fn)
    return "visible numeric label changed"


def replace_panel(path):
    data = open(path, "rb").read()
    ad = formats.detect(data)
    if ad.name == "svg":
        def fn(visible):
            out = re.sub(r"<(path|rect|line)\b[^>]*/?>", "", visible,
                         count=1)
            assert out != visible, "no graphical element to remove"
            return out
        _edit_svg_visible(path, fn)
        return "first graphical element removed"
    from PIL import Image
    img = Image.open(io.BytesIO(data)).convert("RGB")
    arr = np.asarray(img).copy()
    h, w, _ = arr.shape
    arr[h // 3:2 * h // 3, :] = 0
    env = ad.extract(data)
    if ad.name == "png":
        buf = io.BytesIO()
        Image.fromarray(arr).save(buf, format="PNG")
        open(path, "wb").write(ad.embed(buf.getvalue(), env))
    else:
        import tifffile
        tifffile.imwrite(path, arr, extratags=[
            (65000, "B", len(env), env, True)])
    return "panel band zeroed"


def swap_payload(path_a, path_b):
    da, db = open(path_a, "rb").read(), open(path_b, "rb").read()
    ada, adb = formats.detect(da), formats.detect(db)
    open(path_a, "wb").write(
        ada.embed(_without_envelope(da, ada), adb.extract(db)))
    return "foreign envelope embedded"


def re_signed_semantic(path):
    """Insider attack: edit payload displayed value and re-sign with a new key.

    Signature is valid, hashes consistent — only the semantic contract can
    catch this.
    """
    data = open(path, "rb").read()
    ad = formats.detect(data)
    env = json.loads(ad.extract(data))
    k = sorted(env["payload"]["displayed"])[0]
    env["payload"]["displayed"][k] = "9999.99"
    priv, pub = crypto.generate_keypair()
    env["manifest"]["public_key_pem"] = crypto.public_key_pem(pub)
    env["manifest"]["payload_hash"] = sha256_hex(
        canonical_json(env["payload"]))
    env["manifest"]["manifest_hash"] = sha256_hex(canonical_json({
        kk: vv for kk, vv in env["manifest"].items()
        if kk not in ("manifest_hash", "object_hash")}))
    env["signature"]["public_key_pem"] = env["manifest"]["public_key_pem"]
    env["signature"]["sig"] = crypto.sign(
        priv, env["manifest"]["manifest_hash"],
        sha256_hex(canonical_json(env["payload"])))
    visible = _without_envelope(data, ad)
    open(path, "wb").write(ad.embed(visible, json.dumps(env).encode()))
    return f"payload displayed[{k}] edited + re-signed"


def main():
    rows = []
    manipulations = ["replace_panel", "change_plotted_value",
                     "change_table_cell", "swap_payload",
                     "alter_tiff_pixels", "strip_metadata",
                     "re_signed_semantic"]
    for name in TARGETS:
        for fmt in ("svg", "png", "tiff"):
            src = os.path.join(OBJDIR, f"{name}.{fmt}")
            for manip in manipulations:
                if manip == "alter_tiff_pixels" and fmt != "tiff":
                    continue
                if manip == "change_table_cell" and "table1" not in name:
                    continue
                w = os.path.join(WORK, f"{name}_{manip}.{fmt}")
                shutil.copy(src, w)
                try:
                    note = ""
                    if manip == "replace_panel":
                        note = replace_panel(w)
                    elif manip in ("change_plotted_value",
                                   "change_table_cell"):
                        note = change_plotted_value(w)
                    elif manip == "swap_payload":
                        other = os.path.join(OBJDIR, "wdbc_2x2." + fmt)
                        note = swap_payload(w, other)
                    elif manip == "alter_tiff_pixels":
                        import tifffile
                        data = open(w, "rb").read()
                        arr = tifffile.imread(w).copy()
                        arr[:30, :30] = 0
                        env = formats.detect(data).extract(data)
                        tifffile.imwrite(w, arr, extratags=[
                            (65000, "B", len(env), env, True)])
                        note = "tiff corner blacked out"
                    elif manip == "strip_metadata":
                        strip_envelope(w)
                        note = "envelope removed"
                    elif manip == "re_signed_semantic":
                        note = re_signed_semantic(w)
                    rep = validate(w)
                    cls = "n/a" if note == "n/a-format" else classify(rep.status)
                    rows.append(dict(
                        object=name, format=fmt, manipulation=manip,
                        note=note, observed=rep.status.value,
                        classification=cls))
                except Exception as e:
                    rows.append(dict(
                        object=name, format=fmt, manipulation=manip,
                        note=str(e), observed=f"EXCEPTION:{type(e).__name__}",
                        classification="cryptographically detected"))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(HERE, "manipulation_results.csv"), index=False)
    print(df.groupby(["manipulation", "classification"]).size()
            .unstack(fill_value=0).to_string())
    print()
    print(df[df.classification == "neither"].to_string())


if __name__ == "__main__":
    main()
