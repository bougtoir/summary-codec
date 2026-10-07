# NOVELTY BOUNDARY — FINAL (Gate 3, §2)

Date (UTC): 2026-10-06. Supersedes the Phase-2 scoping statement in
`05_NOVELTY_AUDIT/novelty_boundary.md` for submission purposes.

## Neighbor audit (all reviewed)

| neighbor | what it provides | what it lacks vs Summary Codec |
|---|---|---|
| embedded data in SVG (`<metadata>`, RDF) | transport for arbitrary XML/JSON | no level model, no contract, no semantic recompute |
| TIFF private tags / XMP | arbitrary metadata carriage | same |
| PNG ancillary chunks (tEXt/iTXt/caNv) | arbitrary metadata carriage | same |
| self-describing / machine-readable figures | human- or machine-readable labels | no declared, *verifiable* recovery guarantee |
| data-embedded scientific graphics | data travel with figure | no enforcement of *what is recoverable* |
| executable papers / notebooks (Code Ocean, Wolfram, eLife ERA) | reproducible *documents* | not per-object contracts inside static figure files |
| FAIR Digital Objects | object identity + typed metadata at package level | no visible↔payload semantic contract |
| RO-Crate | bundle packaging + provenance | bundle ≠ published figure; no recompute contract |
| Research Objects / PROV-O | workflow provenance graphs | no per-object verification |
| C2PA / Content Credentials | signed authorship/edit-history manifest | authenticity, not recoverability semantics; stripping problem identical to ours |
| scientific image provenance / forensics | fabrication screening | orthogonal; we do not detect pre-signing fraud |
| crypto signatures / checksums in workflows | integrity of transmitted artifacts | integrity ≠ recoverability level enforcement |
| supplementary CSV/ZIP | recoverable data beside the figure | detachable, unverifiable, undeclared level |
| reproducible figure pipelines | code that can redraw the figure | no artifact-bound guarantee for the *published* file |

## NOT claimed (unchanged)

Embedding data, metadata, checksums, signatures, provenance, containers,
compression, fabrication detection, scientific-truth certification.

## Final defensible novelty statement

> Summary Codec's defensible novelty is a **format-independent recoverability
> standard**: an author *declares* a recovery level (L0–L4) for a published
> figure or table, and that declaration becomes a machine-verifiable contract
> linking (i) the visible object, (ii) a recoverable payload, (iii) analysis
> semantics via object-class equivalence rules, (iv) provenance, and
> (v) integrity — such that a verifier can *enforce* the level
> (`LEVEL_NOT_SATISFIED`), detect semantic falsification invisible to
> signatures (`SEMANTIC_MISMATCH`), and classify post-signing modification.

### Is this still (1) novel enough and (2) accurately supported?

1. **Novel enough — YES, conservatively.** Each ingredient exists; the
   *combination as a standard* — declared level + mandatory per-level
   validation suite + semantic equivalence contract + status taxonomy —
   was not found in any neighbor audited. The claim is deliberately
   bounded: we claim the *contract framework*, not the transports.
2. **Accurately supported — YES.** Every element of the statement maps to
   demonstrated behavior: levels enforced (T7, 12/12), semantic contract
   catches validly-signed forgery (T6, 15/15), one core across 3 formats
   (T2 48/48; T4 24/24), taxonomy distinct (T3, 168 cases).

## Remaining boundary risk

The *narrowest* surviving reading ("a level system over embedded JSON") is
the one a hostile reviewer will use. Mitigation: lead Results with the
contract/enforcement evidence (T6/T7), not with the embedding mechanics.
