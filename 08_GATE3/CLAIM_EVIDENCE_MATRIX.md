# CLAIM ↔ EVIDENCE MATRIX (Gate 3, §4–§6, §11–§14)

Date (UTC): 2026-10-06. Every abstract-level claim must appear here.

## Primary claim

> **Declared recoverability levels can be made into enforceable,
> machine-verifiable scientific contracts across heterogeneous figure/table
> formats.**

Supported: every Results strand maps below.

## Traceability table

| Claim | Evidence | Test / benchmark | Object classes | Formats | Levels | Independent? | Limitation | Verdict |
|---|---|---|---|---|---|---|---|---|
| Signed objects install & verify for a fresh user | clean venv install + CLI | T1 | all | all | L0–L4 | yes | none known | supported |
| Envelopes roundtrip losslessly | 48/48 VALID CLI + 84/84 synthetic matrix | T2, object_class_tests | 4–5 | svg/png/tiff | L1–L4 | yes | — | supported |
| Post-signing manipulation never silently validates | 168-condition taxonomy, 0 silent VALID | T3 | all | all | all | yes | editor re-save strips raster envelope → PAYLOAD_MISSING (disclosed) | supported |
| Independent reproduction from the published file alone | 24/24 VALID + reproduced + reanalysis_ok | T4, reproduce.py | survival, table1, 2×2, mean_sd, histogram | all | L4 | yes (bundled public datasets) | 3 datasets — demonstration scale | supported |
| Internal consistency of the implementation | 101/101 pytest | T5 | 5 | all | L1–L4 | yes | — | supported |
| Crypto-valid objects can fail semantic consistency | re-signed forgery → SEMANTIC_MISMATCH | T6 | km, mean_sd, hist, 2×2 | all | L3/L4 | yes | detects *falsified displayed values*, not all fabrication | supported |
| Declared levels are enforced, not self-asserted | missing queries/contract → LEVEL_NOT_SATISFIED | T7 | mean_sd, hist | all | L3, L4 | yes | enforceable only for declared contract surface | supported |
| One architecture across formats | one core; adapters transport-only | §7 audit | all | svg/png/tiff | all | yes | — | supported |
| Post-publication reuse without author contact | log-rank p=0.0034; RMST-1500d 1108/1217 d; landmark S(1000) 0.621/0.723; Table-1 SMDs | reanalysis_demo | survival, table1 | all | L3/L4 | yes | reuse bounded by payload scope | supported |
| Re-signing insider forgery is detectable | 12/12 Phase-2 objects semantically detected | manipulation_results | 4 | all | L4 | yes | — | supported |
| Envelope loss is detected honestly | PNG/TIFF editor re-save → PAYLOAD_MISSING | T3, re_saved | all | png/tiff | all | yes | *the central disclosed limitation* | supported (as limitation) |
| Distinction from figure+CSV/ZIP | capability matrix; controls have nothing to verify | negative_controls | mean_sd | png | L4 | yes | — | supported |

## Adversarial representation check (§5, §6)

T6/T7 are **central evidence**, not buried:

1. cryptographically valid objects can still fail semantic consistency —
   T6 demonstrates it (signature verifies, semantics reject);
2. recovery-level claims are enforced — T7 shows encode-time refusal AND
   validate-time rejection of four distinct violation types;
3. L3/L4 contract violations detected — named failed checks
   (`secondary_queries_executable`, `canonical_dataset_hash`) with human-
   readable details;
4. zero silent VALID across all 168+15+24 tested manipulations.

Adversarial tests also *found real defects* pre-submission (empty-L3
trivial pass; L4 missing-contract KeyError) — reported as evidence of
adversarial-test value in GATE1 §carry-overs and E2E_TEST_RESULTS §T7.

## Claims boundary (§13)

**May claim**: detection of post-signing modification, payload substitution,
visible-object substitution, semantic mismatch, and envelope loss where
tested.
**Must NOT claim**: fraud prevention generally; detection of fabrication
pre-dating signing; proof underlying data are true; forensic detection of
all image manipulation. Current docs comply — threat model + GATE2 wording
already scoped this way. Manuscript must preserve this scoping verbatim.

## Semantic-vs-crypto distinction required in manuscript (§6)

Four distinct notions, never conflated: **cryptographic validity**
(hashes/signature), **semantic validity** (V'≡V recompute),
**recoverability-level validity** (declared contract satisfiable),
**scientific truth** (out of scope entirely). The status taxonomy
implements exactly this separation.
