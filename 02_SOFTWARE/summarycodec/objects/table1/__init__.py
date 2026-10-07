"""table1 object: publication-style Table 1 (baseline characteristics).

inputs:
{
  "records": [{var: value, ...}, ...],
  "variables": [
     {"name": "age", "kind": "continuous", "summary": "mean_sd"|"median_iqr",
      "label": "Age, y"},
     {"name": "sex", "kind": "categorical", "label": "Sex"}
  ],
  "group_by": "arm"            # optional; else single 'Overall' column
  "missingness": "exclude"     # only documented rule supported: complete-case
}
"""

from __future__ import annotations

import numpy as np

from ..base import ScientificObject, _esc


class Table1(ScientificObject):
    object_class = "table1"
    equivalence_rule = ("each displayed cell recomputed from source variables under "
                        "denominator, missingness, summary, and rounding rules")

    def _columns(self):
        recs = self.inputs["records"]
        gb = self.inputs.get("group_by")
        if not gb:
            return {"Overall": recs}
        cols = {}
        for r in recs:
            cols.setdefault(str(r.get(gb)), []).append(r)
        return dict(sorted(cols.items()))

    def analyze(self) -> dict:
        miss_rule = self.inputs.get("missingness", "exclude")
        if miss_rule != "exclude":
            raise ValueError(f"unsupported missingness rule: {miss_rule}")
        cols = self._columns()
        rows = []
        for var in self.inputs["variables"]:
            name, kind = var["name"], var["kind"]
            cells = {}
            for col, recs in cols.items():
                vals = [r.get(name) for r in recs]
                n_miss = sum(v is None for v in vals)
                vals = [v for v in vals if v is not None]  # complete-case
                if kind == "continuous":
                    x = np.asarray(vals, dtype=float)
                    if var.get("summary", "mean_sd") == "median_iqr":
                        cells[col] = {"value": float(np.median(x)),
                                      "q1": float(np.quantile(x, .25)),
                                      "q3": float(np.quantile(x, .75)),
                                      "n": int(x.size), "n_missing": n_miss}
                    else:
                        cells[col] = {"value": float(x.mean()),
                                      "sd": float(x.std(ddof=1)) if x.size > 1 else 0.0,
                                      "n": int(x.size), "n_missing": n_miss}
                else:  # categorical -> counts per level
                    levels = {}
                    for v in vals:
                        levels[str(v)] = levels.get(str(v), 0) + 1
                    cells[col] = {"levels": levels, "n": len(vals),
                                  "n_missing": n_miss}
            rows.append({"variable": var, "cells": cells})
        return {"columns": list(cols), "rows": rows}

    def displayed(self, results: dict) -> dict:
        d = {}
        for row in results["rows"]:
            var = row["variable"]
            label = var.get("label", var["name"])
            for col, cell in row["cells"].items():
                if var["kind"] == "continuous":
                    if var.get("summary", "mean_sd") == "median_iqr":
                        d[f"{label}|{col}"] = (f"{self.fmt(cell['value'])} "
                                               f"[{self.fmt(cell['q1'])}, {self.fmt(cell['q3'])}]")
                    else:
                        d[f"{label}|{col}"] = (f"{self.fmt(cell['value'])} ± "
                                               f"{self.fmt(cell['sd'])}")
                else:
                    denom = cell["n"]
                    for lvl, cnt in sorted(cell["levels"].items()):
                        pct = 100 * cnt / denom if denom else 0.0
                        d[f"{label}={lvl}|{col}"] = f"{cnt} ({self.fmt(pct)}%)"
                d[f"{label}|{col}|n_missing"] = str(cell["n_missing"])
        return d

    def secondary_queries(self) -> dict:
        def subgroup_table1(group_var: str):
            """Recompute the table stratified by another observed variable."""
            recs = self.inputs["records"]
            return {name: len([r for r in recs if str(r.get(group_var)) == str(name)])
                    for name in sorted({str(r.get(group_var)) for r in recs})}

        def cell_count():
            return {"n_records": len(self.inputs["records"]),
                    "n_variables": len(self.inputs["variables"])}

        return {"subgroup_table1": subgroup_table1, "cell_count": cell_count}

    # -- rendering ---------------------------------------------------------
    def _table_text(self, results):
        """Lines of the visible table: (label, {col: text})."""
        cols = results["columns"]
        lines = []
        for row in results["rows"]:
            var = row["variable"]
            label = var.get("label", var["name"])
            if var["kind"] == "continuous":
                lines.append((label,
                              {c: self._cont_text(var, row["cells"][c]) for c in cols}))
            else:
                for lvl in sorted({l for c in cols for l in row["cells"][c]["levels"]}):
                    lines.append((f"  {label}={lvl}",
                                  {c: self._cat_text(row["cells"][c], lvl) for c in cols}))
        return lines

    def _cont_text(self, var, cell):
        if var.get("summary", "mean_sd") == "median_iqr":
            return f"{self.fmt(cell['value'])} [{self.fmt(cell['q1'])}, {self.fmt(cell['q3'])}]"
        return f"{self.fmt(cell['value'])} ± {self.fmt(cell['sd'])}"

    def _cat_text(self, cell, lvl):
        cnt = cell["levels"].get(lvl, 0)
        pct = 100 * cnt / cell["n"] if cell["n"] else 0.0
        return f"{cnt} ({self.fmt(pct)}%)"

    def draw_figure(self, ax, displayed):
        res = self.analyze()
        cols = ["", *res["columns"]]
        celltext = [cols]
        for label, cells in self._table_text(res):
            celltext.append([label, *[cells[c] for c in res["columns"]]])
        ax.axis("off")
        ax.table(cellText=celltext, loc="center", cellLoc="center")
        ax.set_title(self.title)

    def svg_body(self, displayed):
        res = self.analyze()
        cols = res["columns"]
        x0, y0, rh, cw = 60, 70, 24, 130
        out = [f'<text x="320" y="25" font-size="15" text-anchor="middle">{_esc(self.title)}</text>']
        for j, c in enumerate(cols):
            out.append(f'<text x="{x0+180+j*cw+cw//2}" y="{y0}" font-size="12" '
                       f'font-weight="bold" text-anchor="middle">{_esc(c)}</text>')
        out.append(f'<line x1="{x0}" y1="{y0+6}" x2="{x0+180+len(cols)*cw}" '
                   f'y2="{y0+6}" stroke="black"/>')
        for i, (label, cells) in enumerate(self._table_text(res)):
            y = y0 + (i + 1) * rh
            out.append(f'<text x="{x0}" y="{y}" font-size="11">{_esc(label)}</text>')
            for j, c in enumerate(cols):
                out.append(f'<text x="{x0+180+j*cw+cw//2}" y="{y}" font-size="11" '
                           f'text-anchor="middle">{_esc(cells[c])}</text>')
        return "".join(out)
