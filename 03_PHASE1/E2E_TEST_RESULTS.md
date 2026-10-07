# E2E TEST RESULTS — Summary Codec

Date (UTC): 2026-10-06
Frozen specification: `/home/ubuntu/summary_codec_test_plan.md` (T1–T5 +
families T6/T7 added on user instruction 2026-10-06).
Environment: clean `python3 -m venv` on Python 3.10; CLI only.
Project: `/home/ubuntu/repos/wip/summary_codec` (branch
`devin/1791325011-summary-codec`).

## Result summary

| Suite | Outcome |
|---|---|
| T1 fresh install | PASS |
| T2 encode/verify roundtrip (4 objects × L1–L4 × SVG/PNG/TIFF) | PASS — 48/48 VALID |
| T3 tamper scenarios | PASS — all exact statuses |
| T4 independent reproduction (24 biomedical objects) | PASS — 24/24 VALID + reproduced + reanalysis_ok |
| T5 pytest regression | PASS — 101/101 |
| T6 SEMANTIC_MISMATCH (insider re-sign forgery) | PASS — 3/3 formats |
| T7 recovery-level contract violations | PASS — 12/12 cases |

## T1 — fresh-environment install

```
python3 -m venv /tmp/sc_venv
/tmp/sc_venv/bin/pip install -r requirements.txt -e .   # exit 0
/tmp/sc_venv/bin/summarycodec --help                    # encode/inspect/verify/decode/reanalyze
```
Pinned deps (cryptography 3.4.8, lifelines 0.30.0, pillow 12.3.0,
tifffile 2025.5.10, numpy 2.2.6, scipy 1.15.3) install cleanly.

## T2 — encode roundtrip

`summarycodec encode` over 4 object inputs (contingency, mean_sd,
histogram, survival) × {L1,L2,L3,L4} × {svg,png,tiff} = 48 files;
`summarycodec verify` → **48/48 VALID**. Per-level check suites verified:
L2 adds `analysis_reproduced`, L3 adds `secondary_queries_executable`,
L4 adds `canonical_dataset_hash`.

## T3 — tamper scenarios (full matrix in `corruption_tests/results.csv`)

168 manipulated containers across 8 conditions:

| condition | observed |
|---|---|
| native, copied | VALID (42) |
| metadata_stripped, format_converted, re_saved(png/tiff) | PAYLOAD_MISSING (56) |
| payload_swapped, visible_altered, re_saved(svg), corrupted(non-fatal) | PARTIALLY_VERIFIABLE (55) |
| corrupted | CORRUPT (15) |

Targeted cases: PNG re-saved via PIL → `PAYLOAD_MISSING`; SVG `<metadata>`
removed → `PAYLOAD_MISSING`; payload byte-edit inside envelope →
`SIGNATURE_INVALID`; pixel repaint (PNG & TIFF) → `PARTIALLY_VERIFIABLE`;
random non-image bytes → `FORMAT_UNSUPPORTED`. **No manipulation silently
validates.**

## T4 — independent reproduction

`04_PHASE2/independent_reproduction/reproduce.py` on the 24 published
objects: **24/24 VALID, 24/24 reproduced=True, 24/24 reanalysis_ok=True**.
CLI cross-container check: `reanalyze ... survival_at [1500]` returns
identical values across SVG/PNG/TIFF of `gbsg2_km_horth`
(S=0.5082 no / 0.6265 yes).

## T5 — pytest regression

`pytest 02_SOFTWARE/tests` → **101 passed** (86 prior + 15 new
adversarial tests: 5 cases × 3 formats).

## T6 — SEMANTIC_MISMATCH (new family)

Forgery: edit a `displayed` value, recompute payload_hash + manifest_hash,
replace public key, re-sign with fresh attacker Ed25519 key. All crypto
checks pass; only the semantic contract can catch it.

- `03_PHASE1/adversarial/adversarial_results.csv`: **3/3 formats →
  SEMANTIC_MISMATCH**, failed check `semantic_equivalence`.
- Same attack on 12 Phase-2 objects (`re_signed_semantic`): 12/12
  semantically detected (`manipulation_results.csv`).

## T7 — recovery-level contract violations (new family)

All forged envelopes re-signed validly; verifier must reject the claimed
level. Results: **12/12 LEVEL_NOT_SATISFIED**:

| case | expected | observed | failed check |
|---|---|---|---|
| L3, `secondary_queries` stripped | LEVEL_NOT_SATISFIED | LEVEL_NOT_SATISFIED | `secondary_queries_executable`: "payload carries no secondary_queries data" |
| L3, unknown query declared | LEVEL_NOT_SATISFIED | LEVEL_NOT_SATISFIED | `secondary_queries_executable`: "prespecified family not covered" |
| L4, manifest contract + payload hash removed | LEVEL_NOT_SATISFIED | LEVEL_NOT_SATISFIED | `canonical_dataset_hash`: manifest=None payload=None |
| L4, wrong canonical_sha256 | LEVEL_NOT_SATISFIED | LEVEL_NOT_SATISFIED | `canonical_dataset_hash`: recomputed≠manifest=payload |

No case returned VALID, SIGNATURE_INVALID, or crashed. (Required
hardening committed in `validators/__init__.py`: absent L3 query data now
rejects instead of trivially passing; absent L4 contract rejects instead
of raising KeyError.)

## Evidence artifacts

- `03_PHASE1/object_class_tests/results.csv` (84/84 VALID)
- `03_PHASE1/corruption_tests/results.csv` (168 rows)
- `03_PHASE1/semantic_validation/results.csv`
- `03_PHASE1/format_tests/results.csv`
- `03_PHASE1/benchmarks/{performance,negative_controls}.csv`
- `03_PHASE1/adversarial/adversarial_results.csv` (15/15)
- `04_PHASE2/independent_reproduction/reproduction_results.csv` (24/24)
- `04_PHASE2/manipulation_tests/manipulation_results.csv`
- `04_PHASE2/reanalysis_demo/reanalysis_results.{json,md}`
