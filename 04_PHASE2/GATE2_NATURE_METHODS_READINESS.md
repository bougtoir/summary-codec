# GATE2 — NATURE METHODS READINESS

Date (UTC): 2026-10-06 (re-scored after frozen E2E suite T1–T7,
`03_PHASE1/E2E_TEST_RESULTS.md`)
Datasets (frozen before final analysis): GBSG2 survival cohort (lifelines-bundled,
Schumacher 1994), WDBC diagnostic cohort (UCI, CC BY 4.0), Efron diabetes
cohort. Acquisition ledger: `datasets/raw/acquisition_ledger.json`.

## Scorecard (0–2 each, max 32)

| # | Criterion | Score | Basis |
|---|---|---|---|
| 1 | conceptual novelty | 2 | recoverability *levels* as machine-verifiable contracts — not data embedding itself (see novelty audit) |
| 2 | distinction from metadata embedding | 2 | embedded-no-contract object fails the contract (`CORRUPT`); capability matrix |
| 3 | distinction from figure + CSV | 2 | no declared guarantee, no semantic check, no tamper evidence in controls |
| 4 | cross-format generality | 2 | single core; SVG+PNG+TIFF byte-level adapters |
| 5 | cross-object generality | 1 | 5 classes covering common publication objects; arbitrary object classes not yet supported |
| 6 | recovery-level rigor | 2 | L1–L4 mandatory suites enforced at encode AND validate time; forged L3/L4 claims rejected `LEVEL_NOT_SATISFIED` (12/12, T7) |
| 7 | validation rigor | 2 | 9-check pipeline; 9-status taxonomy; absent contract data treated as violation, not trivially-true |
| 8 | semantic consistency | 2 | `V'≡V` per-class equivalence rules; validly re-signed insider forgery → `SEMANTIC_MISMATCH` 15/15 (T6) |
| 9 | cryptographic integrity | 2 | SHA-256 chain + Ed25519 via `cryptography` |
| 10 | provenance utility | 1 | lifecycle chain works; C2PA/RO-Crate integration evaluated but not implemented (recommended, see audit) |
| 11 | biomedical relevance | 2 | real survival/diagnostic/clinical cohorts; TIFF imaging path exercised |
| 12 | independent reproducibility | 2 | `reproduce.py` runs inspect→verify→decode→reproduce→reanalyze on all 24 objects: 24/24 VALID, 24/24 reproduced |
| 13 | practical usability | 1 | CLI complete; key management demo-grade; no packaged release yet |
| 14 | software quality | 2 | 101 unit tests; deterministic canonical serialization |
| 15 | failure-mode transparency | 2 | statuses honest; editor re-save stripping documented as limitation |
| 16 | post-publication reuse | 2 | log-rank, RMST-1500d, landmark S(1000d), and Table-1 SMDs executed solely from published objects |

**Total: 29 / 32 → proceed to Nature Methods submission package.**

## Mandatory conditions (all met)

- semantic validation works — yes (`SEMANTIC_MISMATCH` demonstrated)
- recovery contracts enforceable — yes (encode refuses unprovable claims)
- SVG + TIFF + PNG all work — yes (24/24 objects VALID)
- independent biomedical reproduction succeeds — yes
- demonstrably more than embedding/attachment — yes (negative controls)

## Honest weaknesses to disclose in the manuscript

1. Editor re-saves strip PNG ancillary chunks and private TIFF tags
   (`PAYLOAD_MISSING`); resilience would need format-level fingerprinting or
   content-bound credentials — candidate C2PA integration point.
2. Cross-object generality currently covers 5 declarative classes; new classes
   require implementing the `ScientificObject` interface.
3. No secrecy: payloads are integrity-protected, not encrypted; governance
   decides publishable level.
4. Level-contract hardening was itself an adversarial-suite finding
   (empty `secondary_queries` trivially passed L3; missing `contract`
   raised KeyError at L4) — fixed in `validators/__init__.py` and locked
   by 15 regression tests.

## Phase 2 artifacts

- objects: `04_PHASE2/biomedical_objects/` (24 files)
- index: `04_PHASE2/manifests/objects_index.csv`
- reproduction: `04_PHASE2/independent_reproduction/reproduction_results.csv`
- reanalysis: `04_PHASE2/reanalysis_demo/reanalysis_results.{json,md}`
- manipulation: `04_PHASE2/manipulation_tests/manipulation_results.csv`
- adversarial: `03_PHASE1/adversarial/adversarial_results.csv`
- E2E: `03_PHASE1/E2E_TEST_RESULTS.md`
