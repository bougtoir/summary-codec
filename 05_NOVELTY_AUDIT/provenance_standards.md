# Provenance standards: integrate vs duplicate (sec. 21)

## Existing provenance systems

- **C2PA / Content Credentials**: signed manifest of content history,
  authorship, edits. Solves attribution/authenticity for the *file*. Known
  weakness: manifest stripping by platforms/editors — identical to what our
  manipulation suite measures (`PAYLOAD_MISSING` on naive re-save).
- **PROV-O / RO-Crate**: workflow/package-level provenance graphs; not bound
  to a single rendered object, no semantic recompute.
- **Signed source-data deposits** (journal source-data files, OSF DOIs):
  versioning + citation, no per-object validation contract.

## Summary Codec vs those systems

| existing provenance systems | Summary Codec |
|---|---|
| authorship, content history, authenticity, modification events | declared recoverability level |
| says *who made this file* and *what happened to it* | says *what you can recompute from it*, and proves it |
| no notion of analysis semantics | payload→visible consistency under object-class equivalence |
| external by design | embedded in the published object itself |

## Decision

Do not duplicate. The codec envelope is complementary to C2PA: a C2PA
manifest *about* a Summary Codec object would record authorship/history,
while the codec manifest records the scientific contract. Integration path:
embed the envelope inside a C2PA `caBv`/custom assertion, or reference the
codec `object_hash` from a C2PA ingredient. Recommended for Phase 3+; not
implemented here (recorded in Gate 2, criterion 10).
