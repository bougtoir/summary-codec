"""survival object: Kaplan-Meier curve with censor marks and risk table."""

from __future__ import annotations

import numpy as np

from ..base import ScientificObject, _esc


class Survival(ScientificObject):
    """inputs: {"time": [...], "event": [...], "groups"?: [...]}.

    event=1 observed event, 0 censored. Optional per-subject group label;
    when present, curves are fit per group.
    """

    object_class = "survival"
    equivalence_rule = "KM step coordinates exact; risk table counts exact; summaries under rounding rule"

    # -- KM machinery ------------------------------------------------------
    @staticmethod
    def km(time: np.ndarray, event: np.ndarray) -> dict:
        order = np.argsort(time)
        t, e = time[order], event[order]
        ut = np.unique(t)
        n = len(t)
        surv, times, at_risk, n_events, n_cens = [], [], [], [], []
        s = 1.0
        surv.append(1.0); times.append(0.0)
        for u in ut:
            mask = t == u
            d = int(e[mask].sum())
            c = int(mask.sum() - d)
            nr = int((t >= u).sum())
            at_risk.append(nr); n_events.append(d); n_cens.append(c)
            if d:
                s *= (1 - d / nr)
            surv.append(s); times.append(float(u))
        return {"times": times, "surv": surv, "at_risk": at_risk,
                "event_times": ut.tolist(), "n_events": n_events,
                "n_censored": n_cens}

    def _groups(self):
        t = np.asarray(self.inputs["time"], dtype=float)
        e = np.asarray(self.inputs["event"], dtype=int)
        g = self.inputs.get("groups")
        if g is None:
            return {"all": (t, e)}
        g = np.asarray(g)
        return {lab: (t[g == lab], e[g == lab]) for lab in sorted(set(g.tolist()))}

    def analyze(self) -> dict:
        out = {"groups": {}}
        for name, (t, e) in self._groups().items():
            km = self.km(t, e)
            med = next((tt for tt, s in zip(km["times"], km["surv"])
                        if s <= 0.5), None)
            out["groups"][name] = {**km, "median": med,
                                   "n": int(t.size),
                                   "n_events_total": int(e.sum())}
        return out

    def displayed(self, results: dict) -> dict:
        d = {}
        for name, g in results["groups"].items():
            d[f"{name}|n"] = str(g["n"])
            d[f"{name}|events"] = str(g["n_events_total"])
            d[f"{name}|median"] = "NA" if g["median"] is None else self.fmt(g["median"])
            for i, (tt, nr) in enumerate(zip(g["event_times"], g["at_risk"])):
                d[f"{name}|risk@{self.fmt(tt)}"] = str(nr)
        return d

    def secondary_queries(self) -> dict:
        def survival_at(tq: float):
            res = self.analyze()
            out = {}
            for name, g in res["groups"].items():
                s = 1.0
                for tt, ss in zip(g["times"], g["surv"]):
                    if tt <= tq:
                        s = ss
                out[name] = {"t": tq, "S": s}
            return out

        def km_median():
            res = self.analyze()
            return {n: g["median"] for n, g in res["groups"].items()}

        return {"survival_at": survival_at, "km_median": km_median}

    # -- rendering ---------------------------------------------------------
    COLORS = ["#4C72B0", "#C44E52", "#55A868", "#8172B2"]

    def draw_figure(self, ax, displayed):
        for i, (name, (t, e)) in enumerate(self._groups().items()):
            km = self.km(t, e)
            xs = np.array(km["times"]); ys = np.array(km["surv"])
            ax.step(xs, ys, where="post", color=self.COLORS[i % 4],
                    label=name)
            cens = t[e == 0]
            for ct in cens:
                s = ys[xs <= ct][-1] if (xs <= ct).any() else 1.0
                ax.plot([ct], [s], marker="+", color=self.COLORS[i % 4])
        ax.set_ylim(0, 1.05)
        ax.set_xlabel("time"); ax.set_ylabel("S(t)")
        ax.set_title(self.title); ax.legend()

    def svg_body(self, displayed):
        res = self.analyze()
        tmax = max((max(g["times"]) for g in res["groups"].values()), default=1)
        left, base, plot_w, plot_h = 70, 340, 500, 280
        out = [f'<text x="320" y="25" font-size="15" text-anchor="middle">{_esc(self.title)}</text>',
               f'<line x1="{left}" y1="{base}" x2="{left+plot_w}" y2="{base}" stroke="black"/>',
               f'<line x1="{left}" y1="{base}" x2="{left}" y2="{base-plot_h}" stroke="black"/>']
        for i, (name, g) in enumerate(res["groups"].items()):
            col = self.COLORS[i % 4]
            pts = []
            for tt, ss in zip(g["times"], g["surv"]):
                pts.append((left + tt / tmax * plot_w, base - ss * plot_h))
            path = f'M {pts[0][0]:.1f} {pts[0][1]:.1f} '
            for j in range(1, len(pts)):
                x0, y0 = pts[j - 1]; x1, y1 = pts[j]
                path += f"L {x1:.1f} {y0:.1f} L {x1:.1f} {y1:.1f} "
            out.append(f'<path d="{path}" fill="none" stroke="{col}" stroke-width="2"/>')
            out.append(f'<text x="{left+plot_w+5}" y="{base- i*15 -5}" '
                       f'font-size="11" fill="{col}">{_esc(name)}</text>')
        return "".join(out)
