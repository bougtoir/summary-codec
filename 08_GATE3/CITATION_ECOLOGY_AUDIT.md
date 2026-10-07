# CITATION ECOLOGY AUDIT (Gate 3, §17)

Date (UTC): 2026-10-06. Mapping only — no reference list built yet; every
citation below must support a concrete statement or boundary.

## Neighborhoods and role

| neighborhood | role in the manuscript | representative anchors (to verify at drafting) |
|---|---|---|
| reproducible research | core motivation: published figures as endpoints vs re-usable objects | reproducibility-crisis & computational-reproducibility reviews; journal source-data policies (Nature/EMBO/eLife) |
| scientific visualization | object-class equivalence rules; figures as data presentations | graphical-perception / figure-reconstruction literature |
| machine-readable publishing | the publication as machine-actionable artifact | semantic-publishing, nanopublication, FAIR papers |
| provenance | boundary vs C2PA/PROV-O: history vs recoverability | PROV-O; C2PA/Content Credentials spec; signing-of-science literature |
| research objects | boundary: bundle-level vs object-level | Research Objects, RO-Crate, FAIR Digital Objects |
| biomedical informatics | reuse demo cohorts + Table-1 conventions | GBSG2 (Schumacher 1994), WDBC (UCI), Efron diabetes; STROBE-adjacent reporting standards |
| image integrity | explicit non-claim: we do not screen fabrication | image-forensic screening tools (duplication/manipulation detection) |
| data standards | level contract as a kind of data-accessibility contract | FAIR principles; data-availability statements |
| open science / FAIR | frame: Findable/Accessible/Interoperable/**Reusable** — codec serves R directly | FAIR paper (Wilkinson 2016) |
| statistical methodology | semantic recompute for mean/SD, 2×2, KM, Table 1 | KM estimation, log-rank, RMST references |

## Gaps / skews identified

- **Overrepresented risk**: provenance literature (easy to over-cite). Keep
  to the minimum needed for the C2PA/PROV-O boundary.
- **Missing foundational neighbor**: machine-readable/semantic-publishing
  work (nanopublications, executable articles) — must be present or the
  novelty claim looks naive.
- **Must NOT add**: citations only because they appeared in Nature Methods;
  generic reproducibility filler; our own prior comb codecs beyond one
  provenance sentence (frozen external references).

## Minimum citation skeleton for drafting

~25–35 refs expected: FAIR + research-object + semantic-publishing cluster
(~8), provenance/C2PA (~5), reproducibility context (~5), methods citations
for object classes (~6), biomedical demo datasets (~3), software/crypto
(~3), image-integrity boundary (~2).

## Final balance (after scaffold build, see CITATION_SCAFFOLD.md — 30 refs)

- reproducibility/open science 7 · semantic publishing 4 · research
  objects/packaging 4 · provenance/C2PA 3 · executable papers 3 ·
  image integrity 2 · biomedical methods+datasets 6 · policy 1.
- **Overrepresented (watch)**: reproducibility manifestos — trim at
  drafting if a sentence doesn't need them.
- **Previously missing, now added**: machine-readable/semantic-publishing
  cluster (Shotton, nanopublications, micropublications, Kuhn-Dumontier),
  executable-papers cluster — without these the novelty claim looked naive.
- Every scaffold entry has DOI/stable ID + relevance + manuscript location.
