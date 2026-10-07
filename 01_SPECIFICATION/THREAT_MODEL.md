# THREAT_MODEL — Summary Codec

## What the object proves

Given an encoded object O and its manifest public key:

- **Integrity**: any post-signing change to V, P, or M is detected
  (hash chain + signature).
- **Attribution**: Σ was produced by the holder of the signing key.
- **Declared recoverability**: the declared level's contract holds at
  validation time.
- **Semantic consistency**: the payload regenerates what V displays.

## Attack classes and expected detection

| Manipulation (post-signing) | Detection |
|---|---|
| Replace a panel / alter pixels | cryptographically detected (visible_hash) |
| Change a plotted value / table cell in V | cryptographically detected; if the payload still declares the old value also semantically detected |
| Swap payload for another object's | cryptographically detected (payload_hash, signature) |
| Strip metadata entirely | detected: `PAYLOAD_MISSING` (degrades to L0-by-absence, never misreports) |
| Re-save through an editor preserving content | survives if envelope survives; otherwise `PAYLOAD_MISSING` |
| Format conversion | new file ≠ O; re-encode required; old signature does not transfer |
| Corrupt container | `CORRUPT` / `INVALID` |

Each manipulation is classified `cryptographically detected`,
`semantically detected`, `both`, or `neither` in the Phase-1/Phase-2
manipulation suite.

## Explicit non-goals

- **No truth claim**: fabrication before signing is undetectable. Summary
  Codec binds payload to display, not display to reality.
- **No key-management product**: keys are demo-grade (Ed25519, PEM);
  institutional attestation / publisher countersignature are optional chain
  entries, not a PKI.
- **No DRM / no secrecy**: payloads are integrity-protected, not encrypted.
- **Privacy**: L3/L4 on patient-level data is a governance decision, not a
  technical one; Phase 2 uses only public/reusable data.
