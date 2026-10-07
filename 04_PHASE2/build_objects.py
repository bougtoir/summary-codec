"""Phase 2: build publication-style Summary Codec objects from the three
frozen biomedical datasets at L3/L4 across SVG/PNG/TIFF.

Outputs biomedical_objects/*.{svg,png,tiff} + manifests/objects_index.csv
"""

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "02_SOFTWARE")))

from summarycodec.objects import make
from summarycodec.core.codec import encode
from summarycodec.core import Level

RAW = os.path.join(HERE, "datasets", "raw")
OBJDIR = os.path.join(HERE, "biomedical_objects")
MANI = os.path.join(HERE, "manifests")
os.makedirs(OBJDIR, exist_ok=True)
os.makedirs(MANI, exist_ok=True)


def build_specs():
    specs = {}

    g = pd.read_csv(os.path.join(RAW, "gbsg2.csv"))
    # KM by hormonal therapy
    specs["gbsg2_km_horth"] = dict(
        object_class="survival", title="GBSG2: recurrence-free survival by hormonal therapy",
        inputs={"time": g["time"].tolist(), "event": g["cens"].tolist(),
                "groups": g["horTh"].tolist()})
    # Table 1 by horTh
    g2 = g.copy()
    g2["tgrade_bin"] = g2["tgrade"].map(lambda t: "G1" if t == "I" else "G2+")
    specs["gbsg2_table1"] = dict(
        object_class="table1", title="GBSG2 baseline characteristics",
        inputs={"records": g2[["age", "tsize", "pnodes", "menostat",
                               "tgrade_bin", "horTh"]].rename(
                    columns={"horTh": "arm"}).to_dict("records"),
                "variables": [
                    {"name": "age", "kind": "continuous", "summary": "mean_sd",
                     "label": "Age, y"},
                    {"name": "tsize", "kind": "continuous",
                     "summary": "median_iqr", "label": "Tumor size, mm"},
                    {"name": "pnodes", "kind": "continuous",
                     "summary": "median_iqr", "label": "Positive nodes"},
                    {"name": "menostat", "kind": "categorical",
                     "label": "Menopausal status"},
                    {"name": "tgrade_bin", "kind": "categorical",
                     "label": "Grade"}],
                "group_by": "arm", "missingness": "exclude"})
    # 2x2: horTh x 3-year recurrence
    e3 = ((g["cens"] == 1) & (g["time"] <= 365 * 3))
    tt = pd.crosstab(g["horTh"], e3)
    specs["gbsg2_2x2"] = dict(
        object_class="contingency", title="GBSG2: 3-year recurrence x hormonal therapy",
        inputs={"cells": [[int(tt.loc["yes", True]), int(tt.loc["yes", False])],
                          [int(tt.loc["no", True]), int(tt.loc["no", False])]],
                "row_labels": ["hormonal", "no hormonal"],
                "col_labels": ["recurrence<=3y", "other"]})

    w = pd.read_csv(os.path.join(RAW, "wdbc.csv"))
    specs["wdbc_mean_sd"] = dict(
        object_class="mean_sd", title="WDBC: mean radius by diagnosis",
        inputs={"groups": {
            "malignant": w.loc[w["target"] == 0, "mean radius"].tolist(),
            "benign": w.loc[w["target"] == 1, "mean radius"].tolist()},
            "ylabel": "mean radius"})
    specs["wdbc_hist_area"] = dict(
        object_class="histogram", title="WDBC: distribution of mean area",
        inputs={"x": w["mean area"].tolist(), "bins": 20})
    big = w["mean radius"] > w["mean radius"].median()
    ct = pd.crosstab(w["target"].map({0: "malignant", 1: "benign"}), big)
    specs["wdbc_2x2"] = dict(
        object_class="contingency",
        title="WDBC: diagnosis x radius above median",
        inputs={"cells": [[int(ct.loc["malignant", True]), int(ct.loc["malignant", False])],
                          [int(ct.loc["benign", True]), int(ct.loc["benign", False])]],
                "row_labels": ["malignant", "benign"],
                "col_labels": ["radius>median", "radius<=median"]})

    d = pd.read_csv(os.path.join(RAW, "diabetes.csv"))
    specs["diabetes_hist_bmi"] = dict(
        object_class="histogram", title="Diabetes cohort: BMI distribution",
        inputs={"x": d["bmi"].tolist(), "bins": 18})
    specs["diabetes_mean_sd"] = dict(
        object_class="mean_sd", title="Diabetes cohort: BMI by sex",
        inputs={"groups": {
            "female": d.loc[d["sex"] < 0, "bmi"].tolist(),
            "male": d.loc[d["sex"] >= 0, "bmi"].tolist()},
            "ylabel": "BMI"})
    return specs


def main():
    specs = build_specs()
    idx = []
    for name, spec in specs.items():
        for fmt in ("svg", "png", "tiff"):
            level = Level.L4
            obj = make(spec["object_class"], spec["inputs"],
                       title=spec["title"])
            out = os.path.join(OBJDIR, f"{name}.{fmt}")
            m = encode(obj, fmt, level, out, actor="phase2-build")
            idx.append(dict(object=name, dataset=name.split("_")[0],
                            object_class=spec["object_class"], format=fmt,
                            level="L4", object_id=m["object_id"],
                            object_hash=m["object_hash"],
                            file=os.path.basename(out),
                            bytes=os.path.getsize(out)))
    df = pd.DataFrame(idx)
    df.to_csv(os.path.join(MANI, "objects_index.csv"), index=False)
    print(df.groupby(["object_class", "format"]).size())
    print("objects:", len(df))


if __name__ == "__main__":
    main()
