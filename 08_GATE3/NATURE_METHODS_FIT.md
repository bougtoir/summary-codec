# NATURE METHODS FIT AUDIT (Gate 3, §3)

Date (UTC): 2026-10-06.

## Dimension-by-dimension

| dimension | assessment |
|---|---|
| methodological novelty | Moderate-strong: a *contract* abstraction over publication objects — new to this journal's space, but it is research-infrastructure methodology, not a measurement method |
| breadth of life-science relevance | Broad: every life-science paper publishes figures/tables; survival curves, 2×2 tables, histograms, Table 1 are ubiquitous in clinical and biomedical literature |
| validation strength | Strong: 168 manipulation cases, 15 forged-envelope cases, 24 real objects, all adversarial families passed |
| generality | Format-independent architecture proven on 3 carriers; 5 object classes (moderate) |
| software maturity | Adequate for a methods paper: clean install, CLI, 101 tests, spec + schema; no CI/release yet |
| biomedical usefulness | Demonstrated: GBSG2/WDBC/diabetes reproduction + KM reanalysis demo |
| reproducibility | Strong: deterministic canonical encoding, frozen data + ledger, one-command reproduction |
| adoption potential | Moderate: requires author behavior change; fits into existing "source data" submission workflows |

## The required concrete answer

> **Why should Nature Methods readers care about this method rather than
> treating it as a scientific-publishing utility?**

Because Summary Codec changes *what a published figure is* in a way that is
directly usable by life-science researchers, not only by publishers: it turns
a static figure/table into a scientific object whose own file carries a
verifiable guarantee of what can be recovered — from redisplaying the
numbers (L1), to re-running the analysis (L2), to answering new questions
(L3), to recovering the canonical dataset (L4). The demonstration is
biomedical-first: a Kaplan–Meier figure from a real breast-cancer cohort
carries enough verified content for a stranger to recompute the log-rank
test, restricted mean survival time, and subgroup summaries without
contacting the authors. For a journal whose readers routinely digitize or
request data behind published figures, a method that makes the *figure
itself* self-verifying and re-analyzable is a methods contribution — the
artifact is the method's output, not its subject.

## Fit verdict

Fit is **defensible but not automatic**. The risk that an editor classifies
it as "publishing tooling" is the top editorial risk (see risk register,
R5/R11) and must be pre-empted in the cover letter and abstract by leading
with the reanalysis-capability claim, not the provenance claim.
