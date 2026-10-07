# summarycodec architecture

```
                ┌─────────────────────────────────────────────┐
                │              Summary Codec Core              │
                │  levels · contracts · payload · manifest ·   │
                │  semantic mapping · provenance · crypto ·    │
                │  decoder                                     │
                └──────┬──────────────────┬───────────┬────────┘
                       │                  │           │
                  svg adapter        png adapter  tiff adapter
                  (<metadata>        (private     (private
                   CDATA)            chunk scDC)  tag 65000)
```

- `objects/` — the five `ScientificObject` classes. Each implements
  `analyze()`, `displayed()`, `secondary_queries()`, `canonical_dataset()`,
  `render_svg()`/`render_pixels()`, plus its equivalence rule.
- `core/codec.py` — `encode()` builds O=(V,P,M,C,Σ): renders V, builds the
  payload, computes the SHA-256 hash chain, signs with Ed25519, embeds the
  envelope via the adapter. Encode refuses a level it cannot prove.
- `validators/` — `validate(path)`: format detect → envelope → hash chain →
  signature → semantic equivalence → level contract suite → status.
- `decoders/` — format sniffing + envelope extraction + `decode()`.
- `cli/` — `summarycodec encode|inspect|verify|decode|reanalyze`.

## Invariants

- Canonical JSON (sorted keys, compact separators) for every hash.
- `visible_hash` never covers the envelope: SVG = doc minus the metadata
  block; PNG/TIFF = decoded pixels. So pixels are provably untouched and
  metadata stripping is separately detectable.
- The signature covers `SHA256(manifest_hash || payload_hash)`; a valid
  signature over a *wrong* payload is still caught by recomputing the
  payload hash.
- SEMANTIC_MISMATCH is reachable: a re-signed insider forgery passes
  cryptography and fails the semantic contract.
