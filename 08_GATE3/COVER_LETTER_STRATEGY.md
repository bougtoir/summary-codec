# COVER LETTER STRATEGY (Gate 3, minimal revision item 6)

Date (UTC): 2026-10-06. Strategy only — no full letter drafted.

## Novelty sentence

> We introduce the first recoverability *standard* for published
> scientific objects: an author declares a recovery level for a figure or
> table, and that declaration becomes a machine-verifiable contract —
> enforced, not assumed — across SVG, PNG, and TIFF.

## Why now

- Journals increasingly require source data, yet the published figure
  itself remains a dead end; verification relies on trust in companion
  files. Provenance infrastructure (C2PA) now exists for *authorship*,
  but nothing enforces *scientific recoverability* — this gap is newly
  visible and addressable.

## Why Nature Methods

- The readers who most need this are life-science researchers re-using
  published quantitative results; the demonstration is biomedical-first
  (breast-cancer survival object → independent reanalysis). It is a
  method for *using* scientific objects, not a publishing format.

## Strongest validation results (lead with these)

- Insider forgery with a *validly re-signed* envelope is caught by
  semantic recompute (`SEMANTIC_MISMATCH`, 15/15) — proof the guarantee
  is more than cryptography.
- Declared levels are enforced: forged L3/L4 claims rejected
  (`LEVEL_NOT_SATISFIED`, 12/12).
- 24/24 real biomedical objects independently reproduced on a clean
  machine; post-publication reanalysis (log-rank, RMST, landmark
  survival, Table-1 SMDs) from the published object alone.
- Zero silent VALID across 168+ tested manipulations.

## Deliberately NOT claimed (state in letter)

- fraud prevention or pre-signing fabrication detection; scientific
  truth; C2PA replacement; production-grade key infrastructure.

## Likely editor objections → concise answers

- "It's metadata embedding" → the embedding is the transport; the
  contribution is the enforceable contract + semantic layer (T6/T7).
- "C2PA solves this" → C2PA = identity/history; codec = recoverability
  semantics; explicitly complementary (boundary doc + figure).
- "Too publishing-oriented" → the capability demonstrated is life-science
  reanalysis without author contact — a methods outcome.
- "Metadata gets stripped" → detected honestly (`PAYLOAD_MISSING`), a
  shared limitation of all embedded credentials including C2PA;
  registry/deposit path is complementary, not a workaround.
- "Levels are arbitrary" → each level is keyed to a concrete reuse task
  and bites in enforcement (T7).
- "Key management is naive" → scoped demo model + production design note
  (registry/publisher countersigning); deliberately not a bespoke PKI.
