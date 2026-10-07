# GATE1 — SUMMARY CODEC TECHNICAL FEASIBILITY

Date (UTC): 2026-10-06 (re-scored after frozen E2E suite incl. adversarial
families T6–T7; see `03_PHASE1/E2E_TEST_RESULTS.md`)
Scope: Phase 1 (synthetic objects, all formats, all levels, manipulation matrix)

## DECISION: **GO**

Frozen E2E spec (T1–T7): all suites PASS — T1 clean-venv install, T2
48/48 VALID, T3 tamper taxonomy exact, T4 24/24 reproduction, T5 101/101
pytest, T6 SEMANTIC_MISMATCH 3/3, T7 contract violations 12/12.

| GO criterion | Result | Evidence |
|---|---|---|
| Common architecture across SVG/TIFF/PNG | PASS — one `summarycodec` core; adapters do transport only | `02_SOFTWARE/summarycodec/` |
| ≥4 object classes | PASS — 5 (mean_sd, contingency, histogram, survival, table1) | `objects/` |
| Enforceable recovery levels | PASS — encode-time refusal of unprovable claims + validate-time rejection: L3 without query data, L3 unknown query, L4 missing/wrong canonical contract all → `LEVEL_NOT_SATISFIED` (12/12) | `adversarial/adversarial_results.csv`, `validators/` |
| Working semantic validation | PASS — `V'≡V` recomputation per object-class equivalence rule; insider re-signed payload (valid signature, falsified `displayed`) yields `SEMANTIC_MISMATCH` in 15/15 forged files | `adversarial/adversarial_results.csv`, `semantic_validation/results.csv`, `04_PHASE2/manipulation_tests` |
| Working integrity verification | PASS — SHA-256 hash chain + Ed25519 signature; payload/manifest/visible hashes verified independently | `validators/__init__.py` |
| No visible/pixel degradation | PASS — pixel identity 14/14 (PNG+TIFF, all classes); SVG metadata non-rendering | `format_tests/results.csv` |
| Successful negative controls | PASS — see below | `benchmarks/negative_controls.csv` |
| Portable decoder | PASS — `summarycodec decode` recovers payload from all formats | `decoders/`, CLI |
| Clear distinction from simple metadata embedding | PASS — embedded-without-contract file parses as `CORRUPT` against the contract schema; capability matrix shows guarantee/validation/provenance gap | `benchmarks/negative_controls.csv` |

## Test matrix results

- Object grid: 84 encodings (7 datasets × L1–L4 × SVG/PNG/TIFF) — **84/84 VALID**.
- Cross-format equivalence: identical `displayed` maps across SVG/PNG/TIFF for
  all 7 logical objects.
- Unit suite: 101 pytest tests pass (incl. 15 adversarial regression tests).

## Manipulation matrix (21 cases/condition; observed status)

| condition | VALID | CORRUPT | PARTIALLY_VERIFIABLE | PAYLOAD_MISSING |
|---|---|---|---|---|
| native | 21 | | | |
| copied | 21 | | | |
| re_saved | | | 7 (svg reserialize) | 14 (png/tiff chunk/tag loss) |
| metadata_stripped | | | | 21 |
| payload_swapped | | | 21 | |
| visible_altered | | | 21 | |
| format_converted | | | | 21 |
| corrupted | | 15 | 6 | |

Every post-signing manipulation is detected; none silently validates.

## Performance (mean, seconds)

- encode: svg 0.005 / png 0.078 / tiff 0.071 — dominated by figure rasterization
- decode: ~0.001; verify: ~0.006
- file-size overhead is payload-dominated (full inputs embedded at L4);
  secondary metric, not optimized by design.

## Semantic validation behavior

- true-valid acceptance: 7/7 accepted (`VALID`)
- tampered displayed value + forged signature: 7/7 rejected (`SIGNATURE_INVALID`)
- insider re-signed payload (valid signature, falsified `displayed`):
  `SEMANTIC_MISMATCH` — 3/3 synthetic + 12/12 real objects.

## Recovery-level contract enforcement (T7, new)

Forged-but-validly-signed objects claiming a level they cannot satisfy
are rejected at validation with a named failed check, never `VALID`:
L3 missing query data, L3 unknown query, L4 missing contract, L4 wrong
canonical hash → `LEVEL_NOT_SATISFIED` (12/12 cases). Details in
`E2E_TEST_RESULTS.md` and `adversarial/adversarial_results.csv`.

## Carry-overs into Phase 2

- Editors that strip ancillary PNG chunks / private TIFF tags degrade the
  object to `PAYLOAD_MISSING` — honest failure, must be described as a
  limitation.
- Group-ordered statistics must be computed in sorted key order (canonical
  JSON re-sorts); fixed in `mean_sd.analyze`.
- Level contracts must treat *absent* contract data as violation, not
  trivially-true emptiness — hardened in `validators/__init__.py`
  (L3 empty `secondary_queries` rejected; L4 missing `contract` rejected
  instead of KeyError).
