"""Acquire Phase 2 biomedical datasets and persist raw copies + ledger.

Datasets (public, redistributable):
  1. GBSG2 (German Breast Cancer Study Group 2) survival cohort,
     bundled with lifelines (MIT); original: Schumacher et al. 1994.
  2. Wisconsin Diagnostic Breast Cancer (WDBC), via scikit-learn (UCI ML repo).
  3. Efron et al. diabetes progression cohort, via scikit-learn.

Raw snapshots are written to datasets/raw/ with a machine-readable
acquisition ledger (never overwrite an existing snapshot).
"""

import hashlib
import json
import os
from datetime import datetime, timezone

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
LEDGER = os.path.join(RAW, "acquisition_ledger.json")


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def save_raw(name: str, df: pd.DataFrame, source: dict):
    os.makedirs(RAW, exist_ok=True)
    path = os.path.join(RAW, f"{name}.csv")
    if os.path.exists(path):
        new = df.to_csv(index=False).encode()
        old = open(path, "rb").read()
        if sha256(new) != sha256(old):
            raise SystemExit(f"raw snapshot {name} differs from existing; "
                             "refusing to overwrite")
        return path, sha256(new), len(new)
    data = df.to_csv(index=False).encode()
    with open(path, "wb") as fh:
        fh.write(data)
    return path, sha256(data), len(data)


def acquire():
    entries = []

    from lifelines.datasets import load_gbsg2
    g = load_gbsg2()
    path, h, n = save_raw("gbsg2", g, {})
    entries.append(dict(
        dataset="gbsg2", file=os.path.relpath(path, HERE), sha256=h, bytes=n,
        source="lifelines.datasets.load_gbsg2 (bundled, MIT license)",
        origin="German Breast Cancer Study Group 2 trial; Schumacher et al., "
                "J Clin Epidemiol 1994",
        retrieved_utc=datetime.now(timezone.utc).isoformat(),
        license="public research dataset (distributed in lifelines)"))

    from sklearn.datasets import load_breast_cancer, load_diabetes
    bc = load_breast_cancer(as_frame=True)
    bdf = bc.frame
    path, h, n = save_raw("wdbc", bdf, {})
    entries.append(dict(
        dataset="wdbc", file=os.path.relpath(path, HERE), sha256=h, bytes=n,
        source="sklearn.datasets.load_breast_cancer (bundled)",
        origin="Wisconsin Diagnostic Breast Cancer, UCI ML Repository "
               "(Street, Wolberg, Mangasarian 1993)",
        retrieved_utc=datetime.now(timezone.utc).isoformat(),
        license="CC BY 4.0 (UCI)"))

    db = load_diabetes(as_frame=True)
    ddf = db.frame
    path, h, n = save_raw("diabetes", ddf, {})
    entries.append(dict(
        dataset="diabetes", file=os.path.relpath(path, HERE), sha256=h, bytes=n,
        source="sklearn.datasets.load_diabetes (bundled)",
        origin="Efron, Hastie, Johnstone, Tibshirani 2004 (LARS)",
        retrieved_utc=datetime.now(timezone.utc).isoformat(),
        license="BSD-style redistribution via scikit-learn"))

    ledger = {"created_utc": datetime.now(timezone.utc).isoformat(),
              "note": "raw snapshots; do not overwrite", "entries": entries}
    with open(LEDGER, "w") as fh:
        json.dump(ledger, fh, indent=2)
    print(json.dumps(entries, indent=2))


if __name__ == "__main__":
    acquire()
