# EDITORIAL RISK REGISTER (Gate 3, §20)

Date (UTC): 2026-10-06. Ranked by likelihood × severity (H/M/L).

| # | Risk ("a reviewer says…") | Likelihood | Severity | Current mitigation | Residual | Required action before submission |
|---|---|---|---|---|---|---|
| R1 | "This is only metadata embedding" | H | H | T6/T7 + contract enforcement + taxonomy; novelty boundary rewritten to claim the *contract*, not the transport | M | Lead abstract/Results with enforcement + semantic detection, not embedding mechanics |
| R2 | "This is only figure + CSV in one file" | M | H | negative-controls capability matrix; binding is cryptographic *and* semantic | L | Show the matrix as a main table |
| R3 | "C2PA already solves this" | M | H | C2PA covers authorship/history, not recoverability semantics; boundary statement drafted | M | Include explicit integrate-vs-duplicate paragraph + one figure panel mapping responsibilities |
| R4 | "The recovery levels are arbitrary" | M | M | levels keyed to actual reuse tasks (display/analysis/secondary/canonical); T7 shows they *bite* | L | Define each level by the task it enables; Table 1 of the paper = level→task→mandatory checks |
| R5 | "Too publishing-oriented for Nature Methods" | M | H | biomedical-first demo (KM reanalysis without author contact); fit paragraph drafted | M | Cover letter + abstract must lead with life-science reuse, not infrastructure |
| R6 | "Biomedical validation too narrow" | M | M | 3 public cohorts, 24 objects, real statistics | M | Acceptable at demo scale; optionally add 1 cancer-imaging TIFF object (cheap) |
| R7 | "Cryptographic layer is over-engineered" | L | M | signing is minimal (Ed25519, standard lib); complexity is in semantics not crypto | L | One sentence: crypto is the plumbing, contracts are the contribution |
| R8 | "The method does not prevent fraud" | M | M | threat model + claims boundary already state we detect post-signing tampering only | L | Keep boundary wording verbatim in manuscript |
| R9 | "Journals strip raster metadata" | H | M | honestly disclosed; native-vs-derivative distinction; C2PA integration path identified | M | State it as a property of *all* embedded-credential systems (incl. C2PA); propose server-side deposit as complementary |
| R10 | "Why not just use repositories?" | M | M | repos are detachable companions; codec binds guarantee *inside* the published artifact; complementary not competing | L | Frame explicitly as complement to repositories |
| R11 | "Why a life-science methods journal?" | M | H | readers routinely need data behind figures; post-publication reanalysis is a methods capability | M | Same as R5 — narrative choice, not new experiments |
| R12 | "Key management is demo-grade" | M | L | scoped honestly; production PKI out of scope | L | Add short production-oriented design note (§10 decision) |
| R13 | "Software not mature (no CI/release)" | L | L | 101 tests, clean install, pinned deps | L | Add LICENSE, tag v0.1.0, minimal CI (pytest) — cheap fix |

## Aggregate

No blocker identified. R1, R3, R5, R9 are the real editorial exposures;
all are mitigable through framing + the boundary statements drafted in
this Gate — none requires new experiments.
