# VALIDATION_CONTRACTS — Level-aware validation

`validate(O)` returns a `ValidationReport` with one status and a per-check
trace. Validation distinguishes four independent channels:

1. **file integrity** — container parseable, envelope intact, hashes match;
2. **attribution** — signature verifies under the manifest public key;
3. **semantic consistency** — recomputed `V' ≡ V`;
4. **scientific truth** — out of scope; never claimed.

## Statuses

```
VALID                  all mandatory checks pass
INVALID                a mandatory check failed (generic)
PARTIALLY_VERIFIABLE   payload/attribution OK but visible object altered
PAYLOAD_MISSING        no envelope (metadata stripped / never encoded)
SIGNATURE_INVALID      signature or hash verification failed
SEMANTIC_MISMATCH      V' ≢ V under the object equivalence rule
LEVEL_NOT_SATISFIED    declared level's mandatory checks cannot be proven
FORMAT_UNSUPPORTED     container format has no adapter
CORRUPT                container cannot be parsed at all
```

## Mandatory suite per level

| Check | L1 | L2 | L3 | L4 |
|---|---|---|---|---|
| envelope present, parses | ✓ | ✓ | ✓ | ✓ |
| signature + hash chain | ✓ | ✓ | ✓ | ✓ |
| `displayed` recomputed from inputs | ✓ | ✓ | ✓ | ✓ |
| semantic equivalence `V' ≡ V` | ✓ | ✓ | ✓ | ✓ |
| `reproduce()` analysis re-run | | ✓ | ✓ | ✓ |
| all declared secondary queries execute | | | ✓ | ✓ |
| canonical dataset hash-verified | | | | ✓ |

## Object-class equivalence rules

### mean_sd
Recompute n, mean, SD from payload inputs; compare to each displayed string
under the payload's rounding rule (`displayed` is compared as rendered text
after identical formatting).

### contingency (2×2)
Recompute all cell counts and displayed derived metrics (risk ratio, odds
ratio, χ²/Fisher p where shown) from payload cells; exact integer equality for
cells, rounding-rule equality for derived metrics.

### histogram
Recompute bin edges and counts/densities from payload data under the declared
binning rule; edge equality to machine precision, count equality exact.

### survival (Kaplan–Meier)
Where declared: recompute the step coordinates, risk table, censor marks, and
reported summary quantities (median survival, survival at t) from payload
time/event arrays; step coordinates exact, summaries under rounding rule.

### table1
Recompute each displayed cell from payload source variables under the declared
denominator rule, missingness rule, summary rule, and rounding rule.
