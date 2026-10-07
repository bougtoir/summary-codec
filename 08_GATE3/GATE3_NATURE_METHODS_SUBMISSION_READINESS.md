# GATE 3 — NATURE METHODS SUBMISSION-LEVEL EDITORIAL READINESS

Date (UTC): 2026-10-06
Frozen evidence: Gate 1 GO · Gate 2 29/32 · T1–T7 complete ·
`03_PHASE1/E2E_TEST_RESULTS.md`. Prior gate results not rewritten.
Scope: editorial/scientific readiness only. No Phase 3/4 work performed.

## Central question

> Is Summary Codec, in its current Phase 1–2 form, strong enough to justify
> preparation of a Nature Methods submission package?

## Audits §7–§16 (evidence review)

### §7 Format independence — PASS (one architecture)

One shared manifest model, one level model, one contract system, one
semantic-validation framework, one provenance/integrity chain. Adapters
(`formats/svg|png|tiff`) contain only detect/embed/extract/visible_bytes —
transport-only, no semantics. Verified empirically: same object → identical
`displayed` and `reanalyze` outputs across all three containers.

### §8 Object generality — SUFFICIENT with a documentation fix

5 classes (mean_sd, contingency, histogram, survival KM, table1) cover the
dominant quantitative publication objects in biomedical literature and span
heterogeneous semantics (parametric summaries, discrete inference,
distributional, time-to-event, composite table). Extensibility is real:
`ScientificObject` ABC requires `analyze/displayed/secondary_queries/
canonical_dataset/equivalence_rule` — but no worked registration example
exists yet. **Decision: handle in Discussion + one cheap doc page; NOT a
blocker. Do not add classes to inflate the count.**

### §9 C2PA / provenance — DEFER INTEGRATION, state boundary

C2PA already provides signed authorship/edit-history at the file level.
Summary Codec provides what C2PA does not: declared recoverability levels,
per-level mandatory validation, semantic recompute (V'≡V), and a
level-enforcement status taxonomy. The systems are **complementary**, not
competing — a C2PA manifest can reference `object_hash`; the codec envelope
could be carried as a C2PA custom assertion. A compatibility proof is
feasible later (embed envelope as C2PA assertion) and is deferred to future
work; the paper must carry the boundary statement from
`05_NOVELTY_AUDIT/provenance_standards.md` so it does not appear to
reinvent provenance infrastructure.

### §10 Key management — DEMO-GRADE ACCEPTABLE if scoped + design note

Current model: self-contained envelope (public key travels in manifest +
signature); attribution/integrity demonstrated *under that key model*.
Gaps: no discovery/revocation/rotation/institutional signing. **Decision:
demo-grade is sufficient for the paper provided (a) the manuscript states
signatures prove attribution+integrity under the carried key, not truth;
(b) a short production-oriented design note is added (publisher/institution
as co-signers, key registry or C2PA binding, rotation = re-issue new
object). No PKI implementation needed — NOT a blocker.**

### §11 Biomedical relevance — PASS

GBSG2 KM-by-hormone-therapy is the compelling example: from the published
figure alone, a stranger recomputes the log-rank test (p=0.0034), RMST,
landmark survival, and subgroup Table-1 statistics. Real cohorts, real
statistics, no author contact — understandable to an editor in one figure.

### §12 Post-publication reuse — PASS

The KM reanalysis is scientifically meaningful (survival-model comparisons
are standard), prespecified via `secondary_queries`, enabled by L3/L4, and
uses only the published object. Supports "publication need not terminate
future computational use". No citation-growth claims made.

### §13 Manipulation claims — PASS (boundary maintained)

Claimed: post-signing modification, payload substitution, visible-object
substitution, semantic mismatch, envelope loss — all demonstrated. Never
claimed: fraud prevention, pre-signing fabrication detection, truth proof,
universal forensic detection.

### §14 Failure modes — PASS

Disclosed: editor re-save stripping (PNG/TIFF → PAYLOAD_MISSING), format
conversion, native-vs-derivative, privacy boundary (payload is public),
5-class scope, demo key management, C2PA non-integration, canonical-hash
recovery vs byte identity, SVG reserialize nuance. No known silent failure.

### §15 Software/repository readiness — MOSTLY PASS, 3 cheap gaps

Present: clean install (T1), full CLI, package structure, CODEC_VERSION +
schema version, 101 tests, deterministic fixtures, example objects,
ARCHITECTURE + spec docs, independent verify path. **Gaps: no LICENSE file,
no release tag, no CI workflow.** All trivial fixes.

### §16 Reproducibility bundle — PASS

`07_REPRODUCIBILITY_BUNDLE/` + frozen specs, fixtures, E2E results,
adversarial scripts, dataset ledger + hashes, exact commands, pinned
requirements, reproduction logs, Gate 1–2 reports. Failed intermediate
tests that changed the implementation are disclosed (T6/T7 → empty-L3
bypass + L4 KeyError, fixed and documented).

## Scorecard (§21, max 40)

| # | Criterion | Score | Basis |
|---|---|---|---|
| 1 | novelty boundary | 2 | contract framework claim survives neighbor audit; conservatively scoped |
| 2 | methodological significance | 1 | real but infrastructure-level method, not a measurement method |
| 3 | Nature Methods fit | 1 | defensible only via biomedical-first framing; R5/R11 live |
| 4 | headline claim clarity | 2 | single claim, preferred form, fully supported |
| 5 | evidence completeness | 2 | every abstract claim maps to a test (claim-evidence matrix) |
| 6 | adversarial validation strength | 2 | T6/T7 central; found 2 real defects pre-submission |
| 7 | cross-format generality | 2 | one core, transport-only adapters, proven |
| 8 | object-class generality | 1 | 5 heterogeneous classes + extensible interface; no worked example yet |
| 9 | semantic validation rigor | 2 | 15/15 forged envelopes rejected semantically |
| 10 | provenance/integrity rigor | 1 | crypto solid; C2PA complementarity deferred; provenance chain minimal |
| 11 | biomedical relevance | 2 | real cohorts; immediately compelling KM example |
| 12 | independent reproducibility | 2 | 24/24 clean-machine reproduction |
| 13 | post-publication reuse value | 2 | log-rank/RMST/landmark/SMD from figure alone |
| 14 | software maturity | 1 | install/CLI/tests/docs solid; no LICENSE/tag/CI |
| 15 | failure-mode transparency | 2 | all known modes disclosed incl. adversarial-suite-found defects |
| 16 | citation ecology | 1 | neighborhoods mapped; no reference list yet |
| 17 | manuscript story | 1 | architecture plan exists, unvalidated by drafting |
| 18 | figure story | 1 | plan exists; T6/T7 foregrounded; unproduced |
| 19 | adoption feasibility | 1 | CLI easy but requires author/publisher behavior change |
| 20 | editorial risk control | 1 | risks enumerated w/ mitigations; residual risk on R1/R5/R9 |

**Total: 30 / 40**

## Mandatory conditions (§21)

- novelty clearly exceeds embedding/attachment — **YES** (contract+level
  enforcement demonstrated; boundary conservatively stated)
- semantic validation central and demonstrated — **YES** (T6, 15/15)
- level contracts enforceable — **YES** (T7, 12/12; encode-time refusal)
- SVG/PNG/TIFF share one architecture — **YES** (§7)
- independent biomedical reproduction — **YES** (24/24)
- no known silent-failure mode — **YES** (all tested manipulations rejected
  or honestly downgraded)
- NM relevance statable in one compelling paragraph — **YES**
  (`NATURE_METHODS_FIT.md`)

## DECISION

**REVISE BEFORE SUBMISSION**

## Minimum required actions (small, no new experiments)

1. `02_SOFTWARE/LICENSE` + tag `v0.1.0` + minimal CI (pytest on push). [R13]
2. Key-management design note (publisher co-signing, key registry/C2PA
   binding, rotation-by-reissue) — 1 page in `01_SPECIFICATION/`. [R12]
3. One worked "register a new object class" example doc in
   `02_SOFTWARE/docs/`. [criterion 8]
4. Citation scaffold (~30 refs) per `CITATION_ECOLOGY_AUDIT.md` skeleton.
   [criterion 16]
5. C2PA boundary paragraph + complementarity diagram (text-level now,
   figure at package build). [R3]
6. Draft the one-paragraph NM relevance statement + cover-letter framing
   (biomedical-first). [R5/R11]

After these six, re-score: expected 34–36/40 → GO TO SUBMISSION PACKAGE.
No action requires new experiments, new datasets, or new object classes.
