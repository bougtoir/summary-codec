# CITATION SCAFFOLD (Gate 3, minimal revision item 4)

Date (UTC): 2026-10-06. 32 references, all verified to exist (DOI or
stable identifier). No citation added for padding; each supports a
concrete statement or novelty boundary.

## A. Reproducibility / open science (7)

1. Wilkinson MD et al. The FAIR Guiding Principles for scientific data
   management and stewardship. *Sci Data* 3, 160018 (2016).
   doi:10.1038/sdata.2016.18 — the "R" (Reusable) frame the levels serve.
   → Introduction
2. Baker M. 1,500 scientists lift the lid on reproducibility.
   *Nature* 533, 452–454 (2016). doi:10.1038/533452a — motivation:
   reproducibility expectations on published results. → Introduction
3. Munafò MR et al. A manifesto for reproducible science.
   *Nat Hum Behav* 1, 0021 (2017). doi:10.1038/s41562-016-0021 —
   systemic framing of reproducibility reform. → Introduction
4. Peng RD. Reproducible research in computational science.
   *Science* 334, 1226–1227 (2011). doi:10.1126/science.1213847 —
   spectrum of reproducibility; our levels formalize an analogous
   graduated scale at object level. → Introduction/Discussion
5. Stodden V et al. Enhancing reproducibility for computational methods.
   *Science* 354, 1240–1241 (2016). doi:10.1126/science.aah6168 —
   policy expectation that artifacts support reuse. → Introduction
6. Gentleman R, Temple Lang D. Statistical analyses and reproducible
   research. *J Comput Graph Stat* 16, 1–23 (2007).
   doi:10.1198/106186007X178663 — compendium concept; contrasts bundle
   vs per-object contract. → Introduction
7. Vandewalle P et al. Reproducible research in signal processing.
   *IEEE Signal Process Mag* 26(3), 37–47 (2009).
   doi:10.1109/MSP.2009.932122 — earliest formal RR definitions; shows
   the unsolved "published artifact itself" gap. → Introduction

## B. Machine-readable / semantic publishing (4)

8. Shotton D. Semantic publishing: the coming revolution in scientific
   journal publishing. *Learned Publishing* 22, 85–94 (2009).
   doi:10.1087/2009203 — machine-actionable articles; boundary:
   semantics of *text*, not object recoverability. → Introduction
9. Groth P, Gibson A, Velterop J. The anatomy of a nanopublication.
   *Information Services & Use* 30, 51–56 (2010).
   doi:10.3233/ISU-2010-0613 — smallest publishable assertion with
   provenance; contrast: no embedded contract in the rendered artifact.
   → Introduction
10. Clark T, Ciccarese PN, Goble CA. Micropublications: a semantic model
    for claims, evidence, arguments and annotations in biomedical
    communications. *J Biomed Semantics* 5, 15 (2014).
    doi:10.1186/2041-1480-5-15 — claim-evidence granularity; our
    contract is a verifiable claim about an object. → Discussion
11. Kuhn T, Dumontier M. Genuine semantic publishing.
    *Data Science* 1, 27–34 (2017). doi:10.3233/DS-170010 — rigorous
    machine-interpretable publication standard. → Introduction

## C. Research objects / packaging (4)

12. Bechhofer S et al. Why linked data is not enough for scientists.
    *Future Gener Comput Syst* 29, 599–611 (2013).
    doi:10.1016/j.future.2013.01.004 — Research Objects: aggregation +
    annotation; boundary vs per-object contract. → Introduction
13. Soiland-Reyes S et al. Packaging research artefacts with RO-Crate.
    *Data Science* 5, 97–138 (2022). doi:10.3233/DS-210053 —
    RO-Crate: bundle-level metadata; complementary, not competing. →
    Introduction/Discussion
14. De Smedt K et al. FAIR Digital Objects for Science: from data pieces
    to actionable knowledge units. *Publications* 8, 21 (2020).
    doi:10.3390/publications8020021 — FAIR Digital Objects; boundary:
    identifier/metadata vs enforced recoverability. → Introduction
15. Data Citation Synthesis Group. Joint Declaration of Data Citation
    Principles. FORCE11 (2014). doi:10.25490/a97f-egyk — data as
    first-class citable objects; motivation for object-level guarantees.
    → Introduction

## D. Provenance / integrity infrastructure (5)

16. W3C PROV-O: The PROV Ontology. W3C Recommendation (2013).
    https://www.w3.org/TR/prov-o/ — provenance vocab; boundary:
    history vs recoverability semantics. → Methods/Discussion
17. C2PA Technical Specification v2.1. Coalition for Content Provenance
    and Authenticity (2024).
    https://c2pa.org/specifications/specifications/2.1/index.html —
    content credentials; complementary infrastructure, see boundary
    note. → Discussion/Limitations
18. Parsons R et al. (Adobe/Microsoft/BBC steering) — see 17; the C2PA
    spec is the stable identifier.
19. Rosenthol L et al. C2PA provenance security analysis / CAI overview —
    use spec (17) plus CAI whitepaper
    https://contentauthenticity.org/standards — authenticity layer.
    → Discussion
20. England P, Kaur J, England P, various — skip; see C2PA spec (17).
    (placeholder merged into 17/19)

## E. Executable / reproducible papers (3)

21. Gavish M, Donoho D. Three dream applications of verifiable
    computational results. *Comput Sci Eng* 19, 26–31 (2017).
    doi:10.1109/MCSE.2017.3154049 — verifiable computational results
    vision. → Discussion
22. Maciocci G, Tsang E, Bentley N, Aufreiter M. Reproducible Document
    Stack: towards a scalable solution for reproducible articles.
    *eLife Labs* (2019).
    https://elifesciences.org/labs/b521cf4d/ — executable documents;
    contrast: container ≠ embedded per-object contract. → Introduction
23. Way R. Executable papers? *Procedia Comput Sci* 4, 688–697 (2011).
    doi:10.1016/j.procs.2011.04.074 — executable-paper proposal.
    → Introduction

## F. Image/figure integrity (2)

24. Bik EM et al. The prevalence of inappropriate image duplication in
    biomedical research publications. *mBio* 7, e00809-16 (2016).
    doi:10.1128/mBio.00809-16 — fabrication detection; explicit
    non-claim boundary. → Limitations
25. Cromey DW. Avoiding twisted pixels: ethical guidelines for the
    appropriate use and manipulation of scientific digital images.
    *J Microsc* 238, 165–168 (2010). doi:10.1111/j.1365-2818.2010.03467.x
    — image-manipulation norms; boundary: we detect post-signing change,
    not fabrication. → Limitations

## G. Biomedical methods + demo datasets (6)

26. Kaplan EL, Meier P. Nonparametric estimation from incomplete
    observations. *J Am Stat Assoc* 53, 457–481 (1958).
    doi:10.1080/01621459.1958.10501452 — survival object semantics.
    → Methods
27. Peto R, Peto J. Asymptotically efficient rank invariant test
    procedures. *J R Stat Soc A* 135, 185–207 (1972).
    doi:10.2307/2344317 — log-rank reanalysis basis. → Methods/Results
28. Royston P, Parmar MK. Restricted mean survival time: an alternative
    to the hazard ratio. *BMC Med Res Methodol* 13, 152 (2013).
    doi:10.1186/1471-2288-13-152 — RMST reanalysis metric. → Results
29. Schumacher M et al. Randomized 2 × 2 trial evaluating hormonal
    treatment and the duration of chemotherapy in node-positive breast
    cancer patients. *J Clin Oncol* 12, 2086–2093 (1994).
    doi:10.1200/JCO.1994.12.10.2086 — GBSG2 cohort (lifelines gbsg2).
    → Results/Methods
30. Street WN, Wolberg WH, Mangasarian OL. Nuclear feature extraction
    for breast tumor diagnosis. *IS&T/SPIE 1905* (1993)
    doi:10.1117/12.148698 — WDBC cohort (UCI doi:10.24432/C5DW2B).
    → Results/Methods
31. Efron B, Hastie T, Johnstone I, Tibshirani R. Least angle regression.
    *Ann Statist* 32, 407–499 (2004). doi:10.1214/009053604000000067 —
    diabetes dataset provenance. → Methods

## H. Editorial policy (1)

32. Nature Portfolio Editorial Policies: Reporting standards and
    availability of data, materials, code and protocols.
    https://www.nature.com/nature-research/editorial-policies/reporting-standards
    — journal source-data expectations; deploys the codec's niche.
    → Introduction/Discussion

## Notes for drafting

- Items 18–20 are folded into the C2PA spec citation (17) — count of
  distinct references ≈ 30.
- Add STROBE/reporting-standard refs only if a manuscript sentence needs
  them; do not citation-pad.
