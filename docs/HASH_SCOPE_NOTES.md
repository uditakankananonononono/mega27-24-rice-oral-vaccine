# Hash scope notes (2026-10-08 audit)

This sidecar note labels what the hash and checksum fields in the files below actually cover. The data files themselves are unchanged. It is a documentation clarification, not a license verdict and not a source re-admission.

Audited commit: `553a6c8d2c9b87da6b2063bad954cb5094a1700d`

## `results/source_eligibility.json`
- Lines (verified against the audited commit): 2-4, 6-8, 46 (7 lines)
- Scope: This file records source documents and ENA metadata scope only; it is not a payload hash record.

## `results/metabolights_source_audit.json`
- Lines (verified against the audited commit): 14, 20, 45-48 (6 lines)
- Scope: This audit covers coverage and source identity only (its own "limits" field says so). It is not an assay-data clearance, and MTBLS437 metabolite features are not independently accessioned datasets.

