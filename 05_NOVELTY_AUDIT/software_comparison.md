# Software comparison (benchmark, Phase 1 negative controls)

Capability matrix measured on generated artifacts
(`03_PHASE1/benchmarks/negative_controls.csv`):

| comparator | recoverable | declared level | machine-verified guarantee | semantic validation | tamper evidence | provenance | secondary analysis |
|---|---|---|---|---|---|---|---|
| ordinary figure | – | none | – | – | – | – | – |
| figure + CSV | ✓ | implicit-raw | – | – | – | – | ✓ |
| figure + ZIP | ✓ | implicit-raw | – | – | – | – | ✓ |
| embedded data, no contract | ✓ | undeclared | – | – | – | – | ✓ |
| **Summary Codec L4** | ✓ | **L4 (declared)** | **✓** | **✓** | **✓** | **✓** | **✓** |

Measured on the real manipulation suite: corrupted object, swapped payload,
modified figure + old payload, and invalid-signature objects are all rejected
by `summarycodec verify`; the figure+CSV/ZIP and no-contract controls have no
notion of rejection at all (nothing to verify against).

Additional dimensions scored:

- **discoverability**: payload travels inside the file (highest for codec and
  no-contract embedding; lowest for ZIP/CSV companions that can be detached);
- **linkage**: codec binds V↔P cryptographically and semantically; companions
  rely on naming/packaging;
- **user effort**: encode/decode/verify are single CLI commands; recovery from
  companions requires manual reconciliation;
- **portability**: decoding needs only this package + its pinned deps.

No straw-man baselines: figure+CSV is the current community-standard
fallback and scored honestly (recoverable, re-analyzable, but unverifiable).
