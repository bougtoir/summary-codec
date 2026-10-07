# Summary Codec

A format-independent scientific-object framework in which authors declare a
**recoverability level** (L0–L4) for a published figure or table, and that
level carries explicit, machine-verifiable guarantees about what can be
recovered, reproduced, or reanalyzed.

Object: `O = (V, P, M, C, Σ)` — visible representation, recoverable payload,
manifest, validation contract, integrity/provenance signature.

Formats: SVG (`<metadata>` CDATA), PNG (private ancillary chunk `scDC`),
TIFF (private tag 65000). Object classes: mean/SD, 2×2 contingency,
histogram, Kaplan–Meier, Table 1.

## Quick start

```bash
cd 02_SOFTWARE && pip install -r requirements.txt && pip install -e .
summarycodec encode --object contingency --format svg --level L2 \
    --inputs inputs.json --out figure.svg --title "2x2"
summarycodec verify figure.svg
summarycodec decode figure.svg
summarycodec reanalyze figure.svg --query odds_ratio_recomputed
```

## Layout

- `00_PROJECT_BOOTSTRAP/` — separation check
- `01_SPECIFICATION/` — spec, levels, contracts, manifest schema, threat model
- `02_SOFTWARE/` — `summarycodec` package, tests (86), docs, examples
- `03_PHASE1/` — synthetic matrix + GATE1 (decision: **GO**)
- `04_PHASE2/` — real biomedical demonstration + GATE2 (**29/32**)
- `05_NOVELTY_AUDIT/` — literature/software/provenance audit, novelty boundary
- `06_MANUSCRIPT/` — deferred to a later phase (Nature Methods package)
- `07_REPRODUCIBILITY_BUNDLE/` — third-party verification path
