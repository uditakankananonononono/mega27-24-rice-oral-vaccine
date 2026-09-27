# 19A supplementary Tables 2 and 4: printed-string length audit

A print-layer replay of the [2024 study's supplementary PDF](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10978600/supplementaryFiles), pages 15-18 (SHA-256 pinned in `results/19a_supp_string_lengths.json`), checking the character counts of its printed strings against their printed labels. Strings themselves are not reproduced in the JSON - only 16-character hash prefixes.

**Supplementary Table 4.** All seven labeled border strings parse cleanly from the text layer, and every counted character count exactly equals its printed bp label: LB-1 90, LB-2 90, LB-3 89, RB-1 80, RB-2 80, RB-3 80, RB-4 67. The table's separate "T-DNA vector designed" lengths row (90/90/89/80/80/80/67 bp) also agrees with the seven per-row labels - internally consistent.

**Supplementary Table 2.** Nineteen primer rows parse; counted string lengths span 18-22 characters, a normal primer range. The table prints no lengths, so these counts are descriptive, not pass/fail.

Unlike the earlier defects found in this same supplement (the "Sapplementary" caption typo, the orphaned fullwidth-comma ratio row, the blank PSM cell, and the Supplementary Table 1 total-percentage mismatch), this audit found the printed strings internally consistent. It is recorded as a verified-consistency result: character-count agreement in the text layer does not verify the strings against any genomic record, and no accession payload was fetched or aligned. A text-layer glyph defect would surface as a count mismatch, so absence of a mismatch supports (but does not prove) a clean print layer for these two tables. No gate credit of any kind.
