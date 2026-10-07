# Novelty audit — literature scan (2026-10-06)

Scoped search areas from the bootstrap prompt. This is a working audit for
Gate 2, not a formal systematic review.

## Fields searched

- **Data-embedded / recoverable scientific figures.** Prior art embeds data in
  figures (e.g., per-figure supplemental files, `ggplot2`/`matplotlib` metadata
  fields, journal "source data" requirements — Nature/EMBO/eLife request
  underlying data per panel). Existing practice gives implicit, unverified
  linkage: the reader trusts the file pairing.
- **Executable papers / research objects.** Wolfram notebooks, Code Ocean
  capsules, eLife executable research articles: reproducible *documents*, not
  per-object guarantees inside a static figure file.
- **FAIR Digital Objects, RO-Crate, Research Objects.** Package-level
  metadata+data envelopes; they describe the bundle, not a per-object
  contract that recomputes what the picture shows.
- **Provenance standards (PROV-O, C2PA/Content Credentials).** Authorship and
  modification history; no analysis-semantics checking. C2PA manifest
  durability across platform stripping is a known hard problem — the same
  limitation Summary Codec has on PNG/TIFF.
- **SVG/TIFF/PNG metadata mechanisms.** SVG `<metadata>`/RDF, PNG ancillary
  chunks (e.g., `iTXt`, `caNv` used by C2PA), TIFF private tags/XMP.
  Well-established transports — deliberately reused, not reinvented.
- **Scientific image integrity.** Forensic duplication screening
  (e.g., ImageTwin/Proofig-style detection) is about fabrication detection —
  orthogonal; Summary Codec does not claim truth.

## What is NOT claimed novel

Data embedding, metadata, digital signatures, hashes, containers, or
provenance in general.

## Novelty statement (as scoped)

> Summary Codec does not introduce data embedding itself. It introduces a
> format-independent recoverability standard in which each declared recovery
> level carries an explicit machine-verifiable scientific contract linking
> the visible object, recoverable payload, analysis semantics, provenance,
> and integrity.

Closest prior work within the user's own corpus: object-specific "comb"
codecs (Survival Comb, Prediction Comb, residual-codec PoC) — treated as
frozen exploratory prior work demonstrating the demand for object-bound
recovery but lacking: selectable levels, level-keyed contracts, semantic
validation, cross-format generality, and tables as first-class objects.
