"""Generate deterministic synthetic datasets for Phase 1 objects."""

import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def make_all(seed: int = 20261006) -> dict:
    rng = np.random.default_rng(seed)
    out = {}

    out["mean_sd_small"] = {
        "object_class": "mean_sd", "title": "Synthetic mean/SD (small)",
        "inputs": {"groups": {
            "control": rng.normal(5.0, 1.0, 12).tolist(),
            "treated": rng.normal(6.2, 1.1, 14).tolist()},
            "ylabel": "response"},
    }
    out["mean_sd_large"] = {
        "object_class": "mean_sd", "title": "Synthetic mean/SD (large)",
        "inputs": {"groups": {
            f"g{i}": rng.normal(5 + i, 1 + 0.1 * i, 400).tolist()
            for i in range(6)}, "ylabel": "response"},
    }
    out["contingency"] = {
        "object_class": "contingency", "title": "Synthetic 2x2",
        "inputs": {"cells": [[42, 158], [19, 181]],
                   "row_labels": ["treated", "control"],
                   "col_labels": ["event", "no event"]},
    }
    out["histogram_small"] = {
        "object_class": "histogram", "title": "Synthetic histogram",
        "inputs": {"x": rng.gamma(2.0, 2.0, 300).tolist(), "bins": 15},
    }
    out["histogram_large"] = {
        "object_class": "histogram", "title": "Synthetic histogram (large)",
        "inputs": {"x": rng.gamma(2.0, 2.0, 20000).tolist(), "bins": 40},
    }
    t = rng.exponential(14, 120)
    out["survival"] = {
        "object_class": "survival", "title": "Synthetic Kaplan-Meier",
        "inputs": {"time": t.tolist(),
                   "event": rng.binomial(1, 0.65, 120).tolist(),
                   "groups": rng.choice(["A", "B"], 120).tolist()},
    }
    out["table1"] = {
        "object_class": "table1", "title": "Synthetic Table 1",
        "inputs": {
            "records": [{
                "age": float(a), "sex": s, "bmi": float(b), "arm": g}
                for a, s, b, g in zip(
                    rng.normal(62, 11, 90),
                    rng.choice(["F", "M"], 90),
                    rng.normal(26, 4, 90),
                    rng.choice(["T", "C"], 90))],
            "variables": [
                {"name": "age", "kind": "continuous", "summary": "mean_sd",
                 "label": "Age, y"},
                {"name": "bmi", "kind": "continuous",
                 "summary": "median_iqr", "label": "BMI"},
                {"name": "sex", "kind": "categorical", "label": "Sex"}],
            "group_by": "arm", "missingness": "exclude"},
    }
    return out


if __name__ == "__main__":
    specs = make_all()
    for name, spec in specs.items():
        with open(os.path.join(HERE, f"{name}.json"), "w") as fh:
            json.dump(spec, fh, indent=1)
        print("wrote", name)
