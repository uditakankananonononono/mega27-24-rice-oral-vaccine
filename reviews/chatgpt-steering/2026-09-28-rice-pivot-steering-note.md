# ChatGPT steering consult for the rice pivot, 2026-09-28

Conversation URL: https://chatgpt.com/c/6aba1c3a-7d60-83e9-8169-46a8b05bc64b

Purpose: user-directed steering rule (when a direction stalls, consult ChatGPT and mine new literature; creativity/novelty leads; negatives stay minority by pivoting sooner, never by softening numbers). The exact prompt and the page-rendered reply are archived beside this note. ChatGPT output is treated as external opinion and leads only; every named accession, DOI and dataset-availability claim below is an unverified candidate until checked against the primary source.

## What was consulted

- Prompt: skeptical-strategist framing, our known source contexts (2007 rice mouse pepsin/IgA study, 2021 phase I nominal contents, 2021 51A seed-bank means, 2024 19A three-lot means, MTBLS437 2017 seed metabolome), the dose-provenance guard prototype with only constructed regression cases, and a request for 3 new directions each with estimand, source accession, sample unit, untouched validation source, fair comparator, preregistered pass/fail, novelty claim and 48-hour falsification test. No wet-lab construct/formulation advice requested or taken.

## What came back (ranked by the reviewer)

1. Cross-vaccine microbiome signature transfer (rank 1, feasibility high): derive a frozen microbiome response score from an independent 2025/2026 oral cholera vaccine metagenome study (Chac et al., candidate DOI 10.1038/s41467-025-67388-y - UNVERIFIED) and test it once, untouched, on the 20-person MucoRice phase-I baseline metagenome cohort (Yuki et al., DOI 10.1016/S2666-5247(20)30196-8, UMIN000018001). Preregistered pass: AUROC >= 0.75 with CI, beats baseline beta-diversity comparator by >= 0.10, no MucoRice-derived feature selection. 48-hour falsification: obtain participant-level data for both cohorts; if the frozen score is near chance, kill the direction. Reviewer caveat: raw-read accessions for BOTH cohorts are unverified; if the external cohort data cannot be obtained, pivot to a cross-vaccine transportability replication from published effect sizes rather than manufacturing a validation cohort from 51A/19A/MTBLS437.
2. Lot/line stability variance decomposition (rank 2, methods contribution): decompose published CTB-content variability into line / seed-bank generation / production-lot components using 51A MSB/NSB (Sasou 2021, DOI 10.1186/s12864-020-07355-7) and 19A (Yuki 2024, DOI 10.3389/fpls.2024.1342662) measurements. Explicit FAIL condition: no independent external validation dataset exists; do not treat paper-level means as replicate-level observations. 48-hour falsification: if the measurement table lacks nested replicate structure, stop.
3. Human dose-response heterogeneity reanalysis (rank 3, weakest novelty ceiling): individual-level dose-response slopes in the 60-person phase-I trial; "dose increases response" is already published and not a discovery.

## What was taken

- The steering answer confirms the pivot away from further dose/provenance discrepancy audits: the reviewer independently judges the MucoRice-only evidence too small for a new dose law, matching our own finding.
- Direction 1 is the lead candidate for the next prereg, contingent on a data-availability check first: locate raw/participant-level metagenome accessions for (a) the 2025/2026 Nature Communications OCV cohort and (b) the MucoRice phase-I 20-person subset before any analysis is designed. Both accessions are currently unverified candidates.
- Direction 2 retained as a fallback methods contribution with its brutal 48-hour gate (nested replicates exist or stop).
- Direction 3 deprioritized; novelty ceiling too low.
- Reviewer's fallback rule adopted: never manufacture a validation cohort from 51A/19A/MTBLS437; if external data access fails, reframe as cross-vaccine transportability from published effect sizes.

## Next step (light, slow-group compatible)

Literature/accession verification only: check whether the two metagenome datasets named in Direction 1 are actually downloadable; record findings in the source ledger. No heavy compute.
