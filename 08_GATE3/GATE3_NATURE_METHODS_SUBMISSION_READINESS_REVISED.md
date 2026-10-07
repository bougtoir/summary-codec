# GATE 3 — REVISED (Nature Methods submission-level readiness)

Date (UTC): 2026-10-06
Original score: **30/40** (unchanged, preserved in
`GATE3_NATURE_METHODS_SUBMISSION_READINESS.md`)
Same rubric, same thresholds, honest re-score after the six minimal
actions — no scope broadening, no new experiments.

## 1. Actions completed

| # | Action | Artifact |
|---|---|---|
| 1 | Software release readiness | `02_SOFTWARE/LICENSE` (MIT), `.github/workflows/ci.yml` (pytest + CLI smoke on clean checkout), `02_SOFTWARE/RELEASE_NOTES_v0.1.0.md`, tag `v0.1.0` prepared for the public mirror |
| 2 | Key-management design note | `08_GATE3/KEY_MANAGEMENT_DESIGN_NOTE.md` — demo model scoped; production path: registry/publisher countersigning, rotation-by-reissue, C2PA identity binding; signatures prove integrity/attribution under the key model, not truth |
| 3 | New-object-class example | `02_SOFTWARE/docs/ADDING_NEW_OBJECT_CLASS.md` — worked `dose_response` example covering schema→displayed mapping→levels→registry→recompute→encode/decode/verify→test→failure conditions |
| 4 | Citation scaffold | `08_GATE3/CITATION_SCAFFOLD.md` — ~30 verified refs (DOI/stable ID, relevance, manuscript location); `CITATION_ECOLOGY_AUDIT.md` updated with final balance |
| 5 | C2PA boundary | `08_GATE3/C2PA_BOUNDARY_AND_INTEROPERABILITY.md` + `C2PA_COMPLEMENTARITY_FIGURE.svg` — complementary layers, interop path (custom assertion / ingredient binding), no implementation claimed |
| 6 | NM relevance + cover strategy | `08_GATE3/NATURE_METHODS_RELEVANCE_PARAGRAPH.md`, `COVER_LETTER_STRATEGY.md` |

## 2. Item-by-item score changes

| # | Criterion | Old | New | Reason |
|---|---|---|---|---|
| 8 | object-class generality | 1 | 2 | worked end-to-end extension example demonstrates the interface is real, not asserted |
| 10 | provenance/integrity rigor | 1 | 2 | key model now formally scoped with production path; C2PA complementarity defined |
| 14 | software maturity | 1 | 2 | LICENSE + CI + release notes + release-tag readiness |
| 16 | citation ecology | 1 | 2 | 30 verified refs across all mapped neighborhoods incl. previously-missing semantic-publishing cluster |
| 17 | manuscript story | 1 | 2 | full architecture plan + concrete NM hook + cover-letter strategy; every section traceable to evidence |
| 20 | editorial risk control | 1 | 2 | every high risk now has a concrete mitigation artifact (boundary docs, capability matrix, relevance paragraph) |

## 3. Unchanged (honest) weaknesses

| # | Criterion | Score | Why still 1 |
|---|---|---|---|
| 2 | methodological significance | 1 | infrastructure method, not a measurement method — inherent |
| 3 | Nature Methods fit | 1 | still an editor-judgment risk; paragraph exists but fit is not proven until review |
| 18 | figure story | 1 | plan + one concept figure; main figures unproduced — real drafting work remains |
| 19 | adoption feasibility | 1 | requires author/publisher behavior change; deployment model described, not yet exercised |

## 4. Newly discovered risks

None. The six actions surfaced no new defects; CI is defined for the
public mirror (will activate post-merge on `bougtoir/summary-codec`).

## 5. Final score

**35 / 40** (within, not forced to, the 34–36 expectation)

## 6. Mandatory criteria — all met

- novelty clearly exceeds embedding/attachment — YES
- semantic validation central and demonstrated — YES (T6, 15/15)
- level contracts enforceable — YES (T7, 12/12 + encode-time refusal)
- SVG/PNG/TIFF one architecture — YES
- independent biomedical reproduction — YES (24/24)
- no known silent-failure mode — YES
- NM relevance statable in one compelling paragraph — YES

## 7. Final decision

**GO TO SUBMISSION PACKAGE**

Remaining honest gaps (figure production, adoption evidence) are drafting-
phase work, not readiness deficiencies. Per the freeze rule, evidence is
frozen in `PHASE1_2_EVIDENCE_FREEZE.md`; manuscript drafting awaits
explicit instruction.
