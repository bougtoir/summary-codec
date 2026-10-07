# Novelty boundary

## Claimed

1. Declared **recoverability levels** (L0–L4) as enforceable, machine-verifiable
   contracts bound to a published figure or table.
2. **Semantic consistency checking**: recomputing the displayed object from
   the recovered payload under object-class equivalence rules, catching what
   signatures alone cannot (insider re-signed falsification →
   `SEMANTIC_MISMATCH`).
3. **Format-independent core**: one scientific semantics layer over SVG
   `<metadata>`, PNG private ancillary chunks, and TIFF private tags.
4. **Tables as first-class recoverable objects** (Table 1 with declared
   denominator/missingness/summary/rounding rules).
5. **Level-aware validation taxonomy** separating file integrity,
   attribution, semantic consistency, and (explicitly out-of-scope) truth.

## Explicitly not claimed

- embedding data or metadata in files;
- digital signatures, hashes, containers, provenance in general;
- image-forensic fabrication detection;
- compression or file-size wins;
- citation benefit (no evidence collected).

## Adjacent, frozen prior work (user's own corpus)

Survival Comb, Prediction Comb, residual-codec PoC — object-specific codecs
that motivated the generalization. Not modified, not claimed as the new
system, cited as exploratory prior work.
