"""Post-publication reuse demonstration.

From the published gbsg2_km_horth object (L4) alone — no contact with the
original authors, no external dataset — perform a secondary analysis not
required for the original figure:

  1. log-rank test comparing the two hormonal-therapy arms;
  2. restricted mean survival time (RMST) to 1500 days per arm;
  3. landmark survival S(1000d) per arm;
  4. standardized mean differences on the Table 1 object payload.

Writes reanalysis_results.json and reanalysis_results.md.
"""

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.abspath(os.path.join(ROOT, "..", "02_SOFTWARE")))

from summarycodec.decoders import decode
from summarycodec.objects import REGISTRY

OBJDIR = os.path.join(ROOT, "biomedical_objects")


def load(name):
    payload = decode(os.path.join(OBJDIR, name))
    return payload


def main():
    out = {}

    # ---- 1-3. survival secondary analyses from the published KM object ----
    payload = load("gbsg2_km_horth.svg")
    time = np.asarray(payload["inputs"]["time"], float)
    event = np.asarray(payload["inputs"]["event"], int)
    grp = np.asarray(payload["inputs"]["groups"])

    from lifelines.statistics import logrank_test
    groups = sorted(set(grp.tolist()))
    m = {g: (time[grp == g], event[grp == g]) for g in groups}
    lr = logrank_test(m[groups[0]][0], m[groups[1]][0],
                      m[groups[0]][1], m[groups[1]][1])
    out["logrank"] = {"groups": groups, "chi2": float(lr.test_statistic),
                      "p": float(lr.p_value)}

    from lifelines import KaplanMeierFitter
    rmst, landmark = {}, {}
    for g in groups:
        kmf = KaplanMeierFitter().fit(*m[g], label=g)
        t_grid = np.linspace(0, 1500, 1501)
        s = kmf.survival_function_at_times(t_grid).values
        rmst[g] = float(np.trapz(s, t_grid))
        landmark[g] = float(kmf.survival_function_at_times([1000]).iloc[0])
    out["rmst_1500d"] = rmst
    out["landmark_S1000d"] = landmark

    # ---- 4. standardized mean differences from the Table 1 object ---------
    payload = load("gbsg2_table1.svg")
    recs = pd.DataFrame(payload["inputs"]["records"])
    smd = {}
    for col in ["age", "tsize", "pnodes"]:
        a = recs.loc[recs["arm"] == "yes", col]
        b = recs.loc[recs["arm"] == "no", col]
        sp = np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
        smd[col] = float((a.mean() - b.mean()) / sp) if sp else 0.0
    out["table1_smd_by_arm"] = smd

    with open(os.path.join(HERE, "reanalysis_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)

    md = ["# Post-publication reanalysis — gbsg2_km_horth (L4)",
          "",
          "Performed entirely from the published Summary Codec object;",
          "no author contact, no external dataset.", ""]
    md.append(f"- log-rank (horTh yes vs no): chi2={out['logrank']['chi2']:.3f}, "
              f"p={out['logrank']['p']:.4f}")
    md.append(f"- RMST to 1500 d: " +
              ", ".join(f"{g}={v:.1f} d" for g, v in rmst.items()))
    md.append("- landmark S(1000 d): " +
              ", ".join(f"{g}={v:.3f}" for g, v in landmark.items()))
    md.append("- Table 1 SMDs by arm: " +
              ", ".join(f"{k}={v:.3f}" for k, v in smd.items()))
    with open(os.path.join(HERE, "reanalysis_results.md"), "w") as fh:
        fh.write("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
