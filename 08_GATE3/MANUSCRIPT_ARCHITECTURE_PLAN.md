# MANUSCRIPT ARCHITECTURE PLAN (Gate 3, §18)

Date (UTC): 2026-10-06. Plan only — no drafting per stop rule.

## Proposed Results structure (matches §18 preferred order)

1. **Summary Codec architecture and recoverability contracts**
   O=(V,P,M,C,Σ); envelope {manifest,payload,signature}; manifest schema;
   the level→mandatory-checks table (paper Table 1). Leads with the
   *contract*, not the embedding.
2. **Level-aware semantic validation**
   V'≡V equivalence rules; the 9-status taxonomy; the four-way distinction
   (crypto / semantic / level / truth). Include the insider re-sign
   demonstration (T6) here.
3. **Cross-format SVG / PNG / TIFF implementation**
   One core + transport-only adapters; byte-level mechanics per format;
   48/48 + 84/84 equivalence.
4. **Cross-object validation**
   The 5 object classes; per-class equivalence rules; extension interface
   (`ScientificObject` ABC — show registration of a new class is ~4 methods).
5. **Adversarial testing**
   T3 matrix (168 conditions), T6 (15 forged envelopes), T7 (12 contract
   violations); the finding that adversarial tests caught 2 real verifier
   defects pre-submission — presented as the test suite *working*.
6. **Biomedical independent reproduction**
   3 frozen cohorts, 24 objects, 24/24 reproduction on a clean machine.
7. **Post-publication reanalysis**
   The KM example: log-rank, RMST, landmark survival, Table-1 SMDs from the
   published object alone. This is the Nature Methods hook.
8. **Provenance / manipulation tests**
   Detection matrix (crypto vs semantic channels); re-signed forgery.
9. **Failure modes**
   Envelope stripping on editor re-save; format conversion; native vs
   derivative; privacy boundary; object-class scope; key-management scope.

## Legacy material policy (§18)

Compression/residual-coding content from prior comb projects: **excluded**
except at most one sentence of provenance ("object-specific codecs
motivated the generalization"). Prior Survival Comb / Prediction Comb are
frozen external references — the new paper must stand alone.

## Discussion beats

- deployment models: journal-side encode at acceptance, author-side
  preprint encode, repository deposit of decoded payload;
- C2PA complementarity (one paragraph, per §9 decision);
- governance: who signs, what level is publishable;
- honest limitations section (failure modes carried verbatim).
