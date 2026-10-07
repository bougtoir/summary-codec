# C2PA BOUNDARY AND INTEROPERABILITY (Gate 3, minimal revision item 5)

Date (UTC): 2026-10-06. **C2PA boundary and interoperability path
defined. C2PA is NOT implemented and NOT superseded.**

## What C2PA / Content Credentials provides

- signed provenance manifest bound to a media file (claims + assertions);
- authorship and attribution claims;
- provenance events: creation, edits, ingredient relations;
- authenticity / modification chain with industry trust infrastructure
  (CA-served signing certs, transparency direction).

## What Summary Codec provides that C2PA does not

- a **declared scientific recoverability level** (L0–L4);
- **level-specific scientific validation** — mandatory check suites per
  declared level;
- **payload→visible-result semantic consistency** (V'≡V recompute under
  object-class equivalence rules) → `SEMANTIC_MISMATCH`;
- **secondary-analysis guarantees** (L3 prespecified query family must
  execute) → `LEVEL_NOT_SATISFIED`;
- **canonical-data recovery guarantees** (L4 byte-level dataset hash) →
  `LEVEL_NOT_SATISFIED`.

## Boundary statement (for the manuscript)

> Summary Codec does not replace C2PA; it adds scientific recoverability
> and analysis-specific validation semantics that provenance standards do
> not by themselves define. C2PA answers "who made this file and what
> happened to it"; Summary Codec answers "what can a stranger recompute
> from it, and is that answer still true".

## Interoperability path (deferred to future work)

- Embed the codec envelope as a **C2PA custom assertion** on the same
  asset: C2PA carries identity/history, the assertion carries the
  scientific contract.
- Reference `object_hash` from a C2PA **ingredient** binding the figure to
  its source manuscript/dataset.
- Publisher/institution attestation: the publisher's C2PA signature plus
  the author's codec signature gives two orthogonal guarantees on one file.
- Shared limitation, stated honestly: both C2PA manifests and codec
  envelopes are stripped by naive re-saving platforms — resilience belongs
  to the ecosystem (registries, deposits), not to either format alone.

## Manuscript wording rules

Allowed: "C2PA boundary and interoperability path defined",
"complementary layers", "integration deferred to future work".
Forbidden: "C2PA integration completed", "Summary Codec supersedes C2PA",
"provenance problem solved".

Companion figure: `C2PA_COMPLEMENTARITY_FIGURE.svg`.
