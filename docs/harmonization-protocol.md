# Dedupe/normalization protocol and harmonization feasibility, 2026-09-27

The prior exploratory note promised a fixed metabolite-level de-duplication and normalization protocol before any untouched-cohort analysis. `scripts/harmonization_protocol.py` now fixes it: named rows only; key by database identifier with name fallback only when the identifier is empty (no name-similarity merges); per-sample median collapse of duplicate rows; finite-positive numeric check on every kept value.

Applied to the archived tables:

- [MTBLS437](https://www.ebi.ac.uk/metabolights/MTBLS437): 351 feature rows -> 212 named -> **104 distinct analytes** (108 duplicate rows collapsed), 18 sample columns.
- [MTBLS288](https://www.ebi.ac.uk/metabolights/MTBLS288): 31 named rows, all distinct, 80 sample columns.
- [MTBLS801](https://www.ebi.ac.uk/metabolights/MTBLS801): split assay 205 named -> 62 distinct; splitless 706 named -> 199 distinct; one abundance column per assay.

Identifier-level overlap with MTBLS437's deduped set: MTBLS288 **12**, MTBLS801 split **19**, MTBLS801 splitless **35** (name-only keys excluded from overlap).

**Concrete result (negative/feasibility):** quantitative cross-study pooling is **not defensible** with these sources. MTBLS437 values are internal-standard peak-intensity ratios (testosterone/ribitol normalization per the 2017 methods); MTBLS288/801 are platform-specific processed GC-MS values from different biological questions (grain development; field heat/drought). There is no shared internal standard, no comparable units, and no batch bridge or reference samples. Allowed use is analyte-presence overlap and within-study contrasts only. This rules out a forced cross-study model and narrows any future held-out benchmark to a new study with harmonizable measurements - an honest protocol-level finding, not a biological discovery, comparator win, or gate credit.
