"""histogram object: binned distribution."""

from __future__ import annotations

import numpy as np

from ..base import ScientificObject, _esc


class Histogram(ScientificObject):
    """inputs: {"x": [...], "bins": int|list, "density": bool}."""

    object_class = "histogram"
    equivalence_rule = "bin edges equal to machine precision; bin counts/densities match under declared binning"

    def _hist(self):
        x = np.asarray(self.inputs["x"], dtype=float)
        bins = self.inputs.get("bins", 10)
        density = bool(self.inputs.get("density", False))
        counts, edges = np.histogram(x, bins=bins, density=density)
        return counts.tolist(), edges.tolist()

    def analyze(self) -> dict:
        counts, edges = self._hist()
        x = np.asarray(self.inputs["x"], dtype=float)
        return {"bin_edges": edges, "counts": counts,
                "density": bool(self.inputs.get("density", False)),
                "n": int(x.size), "mean": float(x.mean()),
                "sd": float(x.std(ddof=1))}

    def displayed(self, results: dict) -> dict:
        d = {"n": str(results["n"]),
             "mean": self.fmt(results["mean"]), "sd": self.fmt(results["sd"]),
             "nbins": str(len(results["counts"]))}
        for i, (e0, e1, c) in enumerate(zip(results["bin_edges"][:-1],
                                            results["bin_edges"][1:],
                                            results["counts"])):
            d[f"bin{i}"] = f"[{self.fmt(e0)},{self.fmt(e1)}):{self.fmt(c)}"
        return d

    def secondary_queries(self) -> dict:
        def reaggregate_histogram(nbins: int):
            x = np.asarray(self.inputs["x"], dtype=float)
            counts, edges = np.histogram(x, bins=nbins)
            return {"counts": counts.tolist(), "edges": edges.tolist()}

        def quantile(q: float):
            x = np.asarray(self.inputs["x"], dtype=float)
            return {"q": q, "value": float(np.quantile(x, q))}

        return {"reaggregate_histogram": reaggregate_histogram,
                "quantile": quantile}

    def draw_figure(self, ax, displayed):
        x = np.asarray(self.inputs["x"], dtype=float)
        ax.hist(x, bins=self.inputs.get("bins", 10),
                density=bool(self.inputs.get("density", False)),
                color="#4C72B0", edgecolor="black")
        ax.set_title(self.title)

    def svg_body(self, displayed):
        counts, edges = self._hist()
        cmax = max(counts) or 1
        e0, e1 = edges[0], edges[-1]
        base, top, plot_h, left, plot_w = 340, 40, 280, 70, 500
        out = [f'<text x="320" y="25" font-size="15" text-anchor="middle">{_esc(self.title)}</text>']
        for i, c in enumerate(counts):
            x = left + i * plot_w / len(counts)
            w = plot_w / len(counts)
            h = c / cmax * plot_h
            out.append(f'<rect x="{x:.1f}" y="{base-h:.1f}" width="{w:.1f}" '
                       f'height="{h:.1f}" fill="#4C72B0" stroke="black"/>')
        out.append(f'<text x="{left}" y="365" font-size="11" text-anchor="middle">{self.fmt(e0)}</text>')
        out.append(f'<text x="{left+plot_w}" y="365" font-size="11" text-anchor="middle">{self.fmt(e1)}</text>')
        return "".join(out)
