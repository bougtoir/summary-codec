# PHASE 1–2 EVIDENCE FREEZE (Gate 3 §8 — GO issued)

Date (UTC): 2026-10-06
Freeze-triggering decision: revised Gate 3 = **GO TO SUBMISSION PACKAGE**
(35/40).

## Evidence state

| item | value |
|---|---|
| Phase 1 | complete — 84/84 encodings VALID; 168-condition manipulation matrix; negative controls |
| Gate 1 | GO |
| Phase 2 | complete — 24 objects, 24/24 independent reproduction, reanalysis demo, manipulation suite |
| Gate 2 | 29/32 → proceed eligible |
| Gate 3 original | 30/40 — REVISE BEFORE SUBMISSION |
| Gate 3 revised | **35/40 — GO TO SUBMISSION PACKAGE** |
| Evidence commit | `9b65862ef` (wip branch `devin/1791325011-summary-codec`); the freeze doc itself lands in the immediately following commit |
| Software version | summarycodec 0.1.0 (`CODEC_VERSION = "0.1.0"`, tag `v0.1.0` prepared) |
| Schema version | manifest schema v1 (`01_SPECIFICATION/MANIFEST_SCHEMA.json`, draft-07) |
| Tests | 101 unit/adversarial pytest tests — all pass |
| Datasets (frozen) | GBSG2 (lifelines-bundled), WDBC (UCI, CC BY 4.0), Efron diabetes; ledger `04_PHASE2/datasets/acquisition_ledger.json` with SHA-256 |
| Supported formats | SVG (`<metadata>` CDATA), PNG (`scDC` ancillary chunk), TIFF (tag 65000) |
| Supported object classes | mean_sd, contingency (2×2), histogram, survival (Kaplan–Meier), table1 |
| Recovery levels | L0–L4, enforced at encode and validate time |

## Known limitations (frozen with evidence)

1. Editor re-saves strip PNG `scDC` chunks / TIFF tag 65000 →
   `PAYLOAD_MISSING` (honest failure; ecosystem/registry mitigation).
2. Object generality = 5 classes; new classes implement
   `ScientificObject` (`docs/ADDING_NEW_OBJECT_CLASS.md`).
3. Payloads integrity-protected, not encrypted; all content public.
4. Key management demonstration-grade; production path documented, not
   implemented.
5. C2PA complementarity defined, not implemented.

## Unresolved future-work items

- C2PA assertion/ingredient integration proof.
- Publisher countersigning / key registry binding.
- Additional object classes (e.g. dose-response, forest plots) on demand.
- Journal-side encode pilot.
- Phase 3 literature information-loss audit (separate project stream).
- Phase 4 Recoverable Scientific Reporting framework paper.

## Freeze rule

After this freeze, Phase 1–2 evidence-generating results must not be
altered to improve manuscript narrative. Any future correction that
changes a result must be explicitly versioned (new commit + note in this
file).
