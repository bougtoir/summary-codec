"""contingency object: 2x2 table with derived metrics."""

from __future__ import annotations

import numpy as np
from scipy import stats

from ..base import ScientificObject, _esc


class Contingency(ScientificObject):
    """inputs: {"cells": [[a, b], [c, d]], "row_labels": [r1, r2],
    "col_labels": [c1, c2]}. a/b = exposed row (event/non-event)."""

    object_class = "contingency"
    equivalence_rule = "all cell counts exactly equal; derived metrics match under rounding rule"

    def cells(self) -> np.ndarray:
        return np.asarray(self.inputs["cells"], dtype=int)

    def analyze(self) -> dict:
        (a, b), (c, d) = self.cells().tolist()
        risk1 = a / (a + b) if a + b else float("nan")
        risk2 = c / (c + d) if c + d else float("nan")
        rr = risk1 / risk2 if risk2 else float("inf")
        orr = (a * d) / (b * c) if b * c else float("inf")
        chi2, p_chi2, _, _ = stats.chi2_contingency(self.cells(), correction=False)
        _, p_fisher = stats.fisher_exact(self.cells())
        return {"risk1": risk1, "risk2": risk2, "rr": rr, "or": orr,
                "chi2": float(chi2), "p_chi2": float(p_chi2),
                "p_fisher": float(p_fisher)}

    def displayed(self, results: dict) -> dict:
        (a, b), (c, d) = self.cells().tolist()
        r, cl = self.inputs.get("row_labels", ["row1", "row2"]), \
            self.inputs.get("col_labels", ["col1", "col2"])
        d = {
            f"{r[0]}|{cl[0]}": str(a), f"{r[0]}|{cl[1]}": str(b),
            f"{r[1]}|{cl[0]}": str(c), f"{r[1]}|{cl[1]}": str(d),
        }
        d["risk1"] = self.fmt(results["risk1"])
        d["risk2"] = self.fmt(results["risk2"])
        d["rr"] = self.fmt(results["rr"])
        d["or"] = self.fmt(results["or"])
        d["p_fisher"] = self.fmt(results["p_fisher"])
        return d

    def secondary_queries(self) -> dict:
        def odds_ratio_recomputed():
            (a, b), (c, d) = self.cells().tolist()
            return {"or": (a * d) / (b * c) if b * c else float("inf")}

        def attributable_risk():
            (a, b), (c, d) = self.cells().tolist()
            return {"ar": a / (a + b) - c / (c + d)}

        return {"odds_ratio_recomputed": odds_ratio_recomputed,
                "attributable_risk": attributable_risk}

    def draw_figure(self, ax, displayed):
        ax.axis("off")
        r = self.inputs.get("row_labels", ["row1", "row2"])
        c = self.inputs.get("col_labels", ["col1", "col2"])
        (a, b), (cc, dd) = self.cells().tolist()
        tbl = [["", c[0], c[1]], [r[0], a, b], [r[1], cc, dd]]
        ax.table(cellText=tbl, loc="center", cellLoc="center")
        ax.set_title(self.title)

    def svg_body(self, displayed):
        r = self.inputs.get("row_labels", ["row1", "row2"])
        c = self.inputs.get("col_labels", ["col1", "col2"])
        cells = self.cells().tolist()
        out = [f'<text x="320" y="25" font-size="15" text-anchor="middle">{_esc(self.title)}</text>']
        x0, y0, cw, ch = 140, 80, 120, 40
        hdr = ["", c[0], c[1]]
        for j, htxt in enumerate(hdr):
            out.append(f'<text x="{x0+j*cw+cw//2}" y="{y0-10}" font-size="13" '
                       f'text-anchor="middle" font-weight="bold">{_esc(htxt)}</text>')
        for i in range(2):
            out.append(f'<text x="{x0-10}" y="{y0+i*ch+ch//2+5}" font-size="13" '
                       f'text-anchor="end" font-weight="bold">{_esc(r[i])}</text>')
            for j in range(2):
                out.append(f'<rect x="{x0+j*cw}" y="{y0+i*ch}" width="{cw}" height="{ch}" '
                           f'fill="none" stroke="black"/>')
                out.append(f'<text x="{x0+j*cw+cw//2}" y="{y0+i*ch+ch//2+5}" '
                           f'font-size="14" text-anchor="middle">{cells[i][j]}</text>')
        res = self.analyze()
        out.append(f'<text x="320" y="240" font-size="12" text-anchor="middle">'
                   f'RR={self.fmt(res["rr"])}  OR={self.fmt(res["or"])}  '
                   f'p(Fisher)={self.fmt(res["p_fisher"])}</text>')
        return "".join(out)
