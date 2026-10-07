"""Independent reproduction: for each published object run
inspect -> verify -> decode -> reproduce -> reanalyze
with no author contact. Writes reproduction_results.csv.
"""

import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.abspath(os.path.join(ROOT, "..", "02_SOFTWARE")))

from summarycodec.decoders import decode, detect_and_extract
from summarycodec.validators import validate
from summarycodec.objects import REGISTRY
from summarycodec.core import Status

OBJDIR = os.path.join(ROOT, "biomedical_objects")


def main():
    rows = []
    for f in sorted(os.listdir(OBJDIR)):
        if not f.endswith((".svg", ".png", ".tiff")):
            continue
        p = os.path.join(OBJDIR, f)
        rep = validate(p)
        row = {"file": f, "status": rep.status.value}
        if rep.ok:
            payload = decode(p)
            obj = REGISTRY[payload["object_class"]](
                payload["inputs"], title=payload["title"],
                rounding=payload["rounding_rule"])
            res = obj.analyze()
            row["reproduced"] = obj.displayed(res) == payload["displayed"]
            qname = payload.get("secondary_queries", [None])[0]
            row["reanalysis_query"] = qname
            row["reanalysis_ok"] = False
            for qargs in ((), (0,), (0.5,), (10,), (4,), (1500,)):
                try:
                    obj.secondary_queries()[qname](*qargs)
                    row["reanalysis_ok"] = True
                    break
                except Exception:
                    continue
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(HERE, "reproduction_results.csv"), index=False)
    print(df.to_string())
    print("ALL VALID:", (df.status == "VALID").all(),
          "| reproduced:", df.reproduced.all())


if __name__ == "__main__":
    main()
