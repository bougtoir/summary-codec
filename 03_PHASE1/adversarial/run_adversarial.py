"""Adversarial families T6 (SEMANTIC_MISMATCH) and T7 (level-contract
violations).

Each case forges a *validly signed* envelope — attacker generates a fresh
Ed25519 keypair, edits the payload/manifest, updates both hashes, and
re-signs — so only the semantic contract or the level contract can catch
it. Writes adversarial_results.csv and prints a summary table.
"""

import io
import json
import os
import shutil
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.abspath(os.path.join(ROOT, "..", "02_SOFTWARE")))
sys.path.insert(0, ROOT)

from summarycodec import crypto, formats
from summarycodec.core import Status, canonical_json, sha256_hex
from summarycodec.validators import validate
from run_phase1 import _without_envelope

OBJDIR = os.path.join(ROOT, "..", "04_PHASE2", "biomedical_objects")
WORK = os.path.join(HERE, "work")
os.makedirs(WORK, exist_ok=True)


def _re_sign(env):
    """Re-hash + re-sign an edited envelope with a fresh attacker key."""
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


def _rewrite(src, dst, edit_fn):
    """Extract envelope, apply edit_fn(env), re-sign, re-embed."""
    data = open(src, "rb").read()
    ad = formats.detect(data)
    env = json.loads(ad.extract(data))
    env = _re_sign(edit_fn(env))
    open(dst, "wb").write(
        ad.embed(_without_envelope(data, ad), json.dumps(env).encode()))
    return dst


def edit_semantic(env):
    """T6: change a displayed value; hashes/signature stay consistent."""
    k = sorted(env["payload"]["displayed"])[0]
    env["payload"]["displayed"][k] = "9999.99"
    return env


def edit_l3_no_queries(env):
    """T7a: declare L3 but strip secondary query data."""
    env["manifest"]["declared_level"] = "L3"
    env["payload"].pop("secondary_queries", None)
    return env


def edit_l3_unknown_query(env):
    """T7b: declare L3 with a query outside the prespecified family."""
    env["manifest"]["declared_level"] = "L3"
    env["payload"]["secondary_queries"] = ["nonexistent_query_xyz"]
    return env


def edit_l4_no_contract(env):
    """T7c-i: declare L4 but remove the canonical-dataset contract."""
    env["manifest"]["declared_level"] = "L4"
    env["manifest"].pop("contract", None)
    env["payload"].pop("canonical_sha256", None)
    return env


def edit_l4_wrong_hash(env):
    """T7c-ii: declare L4 with a wrong canonical_sha256."""
    env["manifest"]["declared_level"] = "L4"
    env["manifest"].setdefault("contract", {})[
        "canonical_sha256"] = "sha256:" + "0" * 64
    env["payload"]["canonical_sha256"] = "sha256:" + "0" * 64
    return env


CASES = [
    ("T6_semantic_mismatch", "gbsg2_km_horth", "L4", edit_semantic,
     Status.SEMANTIC_MISMATCH),
    ("T7a_l3_missing_query_data", "wdbc_mean_sd", "L3",
     edit_l3_no_queries, Status.LEVEL_NOT_SATISFIED),
    ("T7b_l3_unknown_query", "wdbc_mean_sd", "L3",
     edit_l3_unknown_query, Status.LEVEL_NOT_SATISFIED),
    ("T7c_l4_missing_contract", "wdbc_mean_sd", "L4",
     edit_l4_no_contract, Status.LEVEL_NOT_SATISFIED),
    ("T7c_l4_wrong_canonical_hash", "diabetes_hist_bmi", "L4",
     edit_l4_wrong_hash, Status.LEVEL_NOT_SATISFIED),
]


def main():
    rows = []
    for case, name, _, edit_fn, expected in CASES:
        for fmt in ("svg", "png", "tiff"):
            src = os.path.join(OBJDIR, f"{name}.{fmt}")
            w = os.path.join(WORK, f"{case}.{fmt}")
            try:
                _rewrite(src, w, edit_fn)
                rep = validate(w)
                failed = [f"{c['check']}: {c['detail']}"
                          for c in rep.checks if not c["ok"]]
                rows.append(dict(case=case, format=fmt,
                                 expected=expected.value,
                                 observed=rep.status.value,
                                 failed_checks=";".join(failed) or "-",
                                 result="PASS" if rep.status == expected
                                 else "FAIL"))
            except Exception as e:
                rows.append(dict(case=case, format=fmt,
                                 expected=expected.value,
                                 observed=f"EXCEPTION:{type(e).__name__}",
                                 failed_checks=str(e), result="FAIL"))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(HERE, "adversarial_results.csv"), index=False)
    print(df.to_string(index=False))
    n_fail = int((df.result == "FAIL").sum())
    print(f"\n{len(df) - n_fail}/{len(df)} PASS, {n_fail} FAIL")
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
