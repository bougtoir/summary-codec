"""mean_sd object: group means with SD error bars."""

from __future__ import annotations

import numpy as np
from scipy import stats

from ..base import ScientificObject, _esc


class MeanSD(ScientificObject):
    object_class = "mean_sd"
    equivalence_rule = "displayed n/mean/SD recomputed from payload inputs match rendered strings under rounding rule"

    def analyze(self) -> dict:
        groups = {}
        for name, vals in self.inputs["groups"].items():
            x = np.asarray(vals, dtype=float)
            n = x.size
            mean = float(x.mean())
            sd = float(x.std(ddof=1))
            se = sd / np.sqrt(n)
            tcrit = float(stats.t.ppf(0.975, n - 1)) if n > 1 else float("nan")
            groups[name] = {
                "n": n, "mean": mean, "sd": sd, "se": se,
                "ci95": [mean - tcrit * se, mean + tcrit * se],
            }
        out = {"groups": groups}
        if len(groups) == 2:
            # deterministic order: canonical JSON re-sorts keys
            (n1, g1), (n2, g2) = sorted(groups.items())
            t, p = stats.ttest_ind(self.inputs["groups"][n1],
                                   self.inputs["groups"][n2], equal_var=False)
            out["welch_t"] = float(t)
            out["welch_p"] = float(p)
        return out

    def displayed(self, results: dict) -> dict:
        d = {}
        for name, g in results["groups"].items():
            d[f"{name}|n"] = str(g["n"])
            d[f"{name}|mean"] = self.fmt(g["mean"])
            d[f"{name}|sd"] = self.fmt(g["sd"])
            d[f"{name}|ci95"] = f"[{self.fmt(g['ci95'][0])}, {self.fmt(g['ci95'][1])}]"
        if "welch_p" in results:
            d["welch_p"] = self.fmt(results["welch_p"])
        return d

    def secondary_queries(self) -> dict:
        groups = self.inputs["groups"]
        names = list(groups)

        def subgroup_mean(idx: int):
            name = names[idx]
            return {"group": name, "mean": float(np.mean(groups[name]))}

        def pooled_mean():
            allx = np.concatenate([np.asarray(v, float) for v in groups.values()])
            return {"pooled_mean": float(allx.mean()), "pooled_n": int(allx.size)}

        return {"subgroup_mean": subgroup_mean, "pooled_mean": pooled_mean}

    # -- rendering --------------------------------------------------------
    def _bars(self):
        res = self.analyze()
        return [(n, g["mean"], g["sd"]) for n, g in res["groups"].items()]

    def draw_figure(self, ax, displayed):
        bars = self._bars()
        xs = np.arange(len(bars))
        ax.bar(xs, [b[1] for b in bars], yerr=[b[2] for b in bars],
               capsize=5, color="#4C72B0", edgecolor="black")
        ax.set_xticks(xs, [b[0] for b in bars])
        ax.set_title(self.title)
        ax.set_ylabel(self.inputs.get("ylabel", "value"))

    def svg_body(self, displayed):
        bars = self._bars()
        ymax = max(m + s for _, m, s in bars) * 1.15 or 1.0
        base, top, plot_h = 340, 40, 280
        w = 500 // max(len(bars), 1)
        out = []
        for i, (name, mean, sd) in enumerate(bars):
            x = 80 + i * w
            h = mean / ymax * plot_h
            hs = sd / ymax * plot_h
            out.append(f'<rect x="{x}" y="{base-h:.1f}" width="{w*0.6:.0f}" '
                       f'height="{h:.1f}" fill="#4C72B0" stroke="black"/>')
            out.append(f'<line x1="{x+w*0.3:.0f}" y1="{base-h-hs:.1f}" '
                       f'x2="{x+w*0.3:.0f}" y2="{base-h+hs:.1f}" stroke="black" stroke-width="2"/>')
            out.append(f'<text x="{x+w*0.3:.0f}" y="365" font-size="13" '
                       f'text-anchor="middle">{_esc(name)}</text>')
            out.append(f'<text x="{x+w*0.3:.0f}" y="{base-h-hs-6:.0f}" font-size="11" '
                       f'text-anchor="middle">{self.fmt(mean)}±{self.fmt(sd)}</text>')
        out.append(f'<text x="320" y="25" font-size="15" text-anchor="middle">{_esc(self.title)}</text>')
        return "".join(out)
