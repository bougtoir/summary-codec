# SUMMARY_CODEC_SPEC — Summary Codec Specification v0.1

## 1. Scope

Summary Codec is a format-independent scientific-object framework. An author
declares a **recoverability level** for a published figure or table; that level
carries explicit, machine-verifiable guarantees about what can be recovered,
reproduced, or reanalyzed from the published object alone.

It is not steganography, not a compression scheme, not a supplementary ZIP,
and not an object-specific residual codec.

## 2. Recoverable Scientific Object

```
O = (V, P, M, C, Σ)
```

- **V** — visible scientific representation (the SVG graphic, TIFF/PNG pixels,
  or rendered table that a reader sees).
- **P** — recoverable scientific payload (canonical JSON: analysis inputs,
  displayed values, analysis specification).
- **M** — machine-readable manifest (JSON Schema `MANIFEST_SCHEMA.json`).
- **C** — validation contract implied by the declared level.
- **Σ** — integrity/provenance signature (SHA-256 hashes + Ed25519 signature).

A conventional figure communicates what is displayed. A Summary Codec object
additionally declares what is guaranteed recoverable and proves whether the
guarantee holds.

## 3. Architecture

One logical **Summary Codec Core** + thin **format adapters** (SVG, TIFF, PNG).

- Adapters solve transport/embedding only.
- Scientific semantics (levels, contracts, payload schema, semantic mapping,
  provenance, integrity, decode interface) live in the shared core.

Core layers:

```
manifest schema · recovery levels · validation contracts · payload schema
semantic mapping · provenance model · cryptographic integrity · decoder interface
```

## 4. Envelope

Every encoded container embeds one envelope:

```json
{
  "manifest":  { ... },        // M
  "payload":   { ... },        // P (canonical JSON)
  "signature": { "alg": "Ed25519", "public_key_pem": "...", "sig": "base64" }
}
```

`signature.sig` signs `SHA256(canonical(manifest)) || SHA256(canonical(payload))`.

## 5. Hash model

- `visible_hash` — SHA-256 of the visible representation:
  - SVG: the SVG document **with the codec `<metadata>` block removed**.
  - PNG/TIFF: the decoded pixel array bytes.
- `payload_hash`, `manifest_hash` — SHA-256 of canonical serializations.
- `object_hash` — SHA-256 over `visible_hash || payload_hash || manifest_hash`.

Metadata stripping is detected by envelope absence (`PAYLOAD_MISSING`);
pixel/visible alteration by `visible_hash` mismatch; semantic tampering by
contract failure — distinct channels, see `THREAT_MODEL.md`.

## 6. Semantic consistency

For payload P and visible object V, the renderer defines
`P --analysis/rendering--> V'`. Validation checks `V' ≡ V` under the
object-class equivalence rule in `VALIDATION_CONTRACTS.md`. Equivalence is
defined on scientific content (displayed values, bin edges, step coordinates,
cell counts), not on byte-level rendering.

## 7. What Summary Codec does NOT claim

- It does not prove scientific truth; fabrication before signing is
  undetectable by design.
- It does not claim novelty for data embedding, metadata, hashes, signatures,
  or containers per se.
- File size is secondary; compression is not the claim.
