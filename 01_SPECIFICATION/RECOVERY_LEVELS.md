# RECOVERY_LEVELS — Declared Recoverability Levels

A Summary Codec object carries one declared level. The declaration is a
*guarantee claim*: validation must be able to prove it. A file may not claim a
level whose mandatory checks fail — `encode` refuses, and `validate` reports
`LEVEL_NOT_SATISFIED`.

## L0 — Visual only
No recovery guarantee. A Summary Codec manifest may still carry provenance and
integrity, but no payload contract is asserted.

## L1 — Display-recoverable
Displayed values are recoverable and machine-verifiable.
Payload MUST contain `displayed` (the values as rendered in V, post-rounding)
plus the analysis inputs sufficient to recompute them.

## L2 — Analysis-reproducible
The reported analysis can be reproduced from the payload. Includes where
applicable: estimates, SEs, 95% CIs, p-values, model statistics.
Payload MUST contain the analysis inputs (raw observations or documented
sufficient statistics) and the analysis specification (method, parameters).
`reproduce()` recomputation must match `displayed` under the rounding rule.

## L3 — Secondary-analysis capable
A prespecified secondary-query family can be executed on the payload.
Payload MUST declare `secondary_queries` (a closed list of named, typed
queries, e.g. `subgroup_mean`, `odds_ratio_recomputed`, `km_median`,
`reaggregate_histogram`) and the implementation must execute each declared
query against the recovered inputs.

## L4 — Canonical data recoverable
The underlying canonical dataset is exactly reconstructable and
hash-verifiable. Payload MUST contain the full canonical dataset and
`canonical_sha256`; decode must reproduce the byte-identical canonical
serialization.

## Level implication

L4 ⊃ L3 ⊃ L2 ⊃ L1: encoding at level N runs the mandatory suite for all
levels ≤ N. Higher is not always better — see the privacy boundary: publish
the *highest scientifically useful* level within legal/ethical/consent limits.
Never embed identifiable patient-level data in public objects.
