# summarycodec v0.1.0 — release notes

Date (UTC): 2026-10-06
Status: research-grade release accompanying the Summary Codec Gate 3
evidence freeze. Stable within the tested surface; not claimed
production-stable beyond it.

## What is in this release

- One shared core (`summarycodec.core`): recovery levels L0–L4, manifest
  schema v1 (`MANIFEST_SCHEMA.json`), canonical-JSON hashing, provenance
  chain, 9-status validation taxonomy.
- Object classes (5): `mean_sd`, `contingency`, `histogram`, `survival`
  (Kaplan–Meier), `table1`.
- Format adapters (transport-only): SVG `<metadata>` CDATA, PNG private
  ancillary chunk `scDC`, TIFF private tag 65000.
- Cryptography: Ed25519 (via `cryptography`), signing
  `SHA256(manifest_hash || payload_hash)`.
- CLI: `summarycodec encode|inspect|verify|decode|reanalyze`.

## Tested surface (evidence frozen at Gate 3)

- 101 unit/adversarial tests pass (clean `pytest tests`).
- 48/48 fresh CLI encodes VALID (4 objects × L1–L4 × 3 formats);
  84/84 Phase-1 synthetic matrix VALID.
- 168 manipulated containers: every case rejected or honestly downgraded —
  zero silent VALID.
- Insider re-sign forgery → `SEMANTIC_MISMATCH` (15/15).
- Level-contract violations → `LEVEL_NOT_SATISFIED` (12/12).
- 24/24 biomedical objects independently reproduce on a clean venv.

## Known limitations (by design, documented)

- Editor re-saves of PNG/TIFF drop the envelope → `PAYLOAD_MISSING`
  (honest failure, not silent).
- Payloads are integrity-protected, not encrypted; all payload content is
  public by design.
- Key management is demonstration-grade (self-contained keypair in
  envelope); production use needs institutional/publisher trust
  infrastructure — see `08_GATE3/KEY_MANAGEMENT_DESIGN_NOTE.md`.

## Install / verify

```bash
cd 02_SOFTWARE
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -e .
.venv/bin/python -m pytest tests -q        # 101 tests
.venv/bin/summarycodec verify <object>     # VALID / status taxonomy
```

## Tag

Release tag: `v0.1.0` (to be applied at the public mirror
`bougtoir/summary-codec` after the wip PR merge and sync).
