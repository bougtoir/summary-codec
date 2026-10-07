# KEY-MANAGEMENT DESIGN NOTE (Gate 3, minimal revision item 2)

Date (UTC): 2026-10-06. Scope: 1 page. **Demonstration-grade by design —
no production PKI built or claimed.**

## Current signing model (as implemented)

- One Ed25519 keypair per encode; private key used once and not stored
  by the codec.
- The public key travels *inside the object*: `manifest.public_key_pem`
  and `signature.public_key_pem` must match.
- Signature covers `SHA256(manifest_hash) || SHA256(payload_hash)`; hash
  failure → `SIGNATURE_INVALID` regardless of signature validity.

## What the signature proves — and does not

| notion | does a valid signature prove it? |
|---|---|
| integrity (bytes unchanged post-signing) | yes — hash chain |
| attribution (who signed) | only *key possession* — the key is self-asserted inside the object; no binding to a human/institution |
| provenance (history chain) | partially — ordered provenance events recorded, but self-asserted |
| semantic consistency (V'≡V) | **no** — checked independently of the signature (T6: valid signature + falsified displayed → `SEMANTIC_MISMATCH`) |
| scientific truth | **never** — out of scope |

## Author-key assumptions (demo model)

Author generates a keypair at encode; key custody, backup, and identity
binding are out of scope. A lost key does **not** break verification of
existing objects (public key travels with them) — it only prevents signing
new objects under the same identity.

## Production-oriented design (not implemented)

- **Public-key discovery**: publisher/registry-hosted key record
  (publisher domain, ORCID-linked, or transparency log); the manifest gains
  a `key_reference` URI. Verification resolves the key externally, removing
  the self-assertion gap in attribution.
- **Institutional signing**: institution countersigns the author's
  signature block — adds "the institution stands behind this identity",
  not "the science is true".
- **Publisher countersigning**: at acceptance, the journal signs
  `object_hash`, binding the object to the published version
  (publication-version binding) and its DOI.
- **Rotation**: re-issue = encode a new object generation with the new key;
  the provenance chain records `rotated_from`. Old objects stay verifiable.
- **Revocation**: a registry-level revocation list consulted at verify
  time; the codec treats revoked-key objects as `SIGNATURE_INVALID`
  only if revocation predates verification policy — versioned policy,
  not retroactive erasure.
- **Alternative**: bind the codec `object_hash` into a C2PA manifest/
  assertion and let C2PA's trust framework carry identity
  (see `C2PA_BOUNDARY_AND_INTEROPERABILITY.md`).

## Deployment statement

Current key handling is **demonstration-grade** and sufficient for the
method paper because the contributions (level contracts, semantic
validation, taxonomy) are orthogonal to identity infrastructure.
Production deployment should integrate institutional/publisher trust
infrastructure or C2PA's identity framework rather than a bespoke PKI.
