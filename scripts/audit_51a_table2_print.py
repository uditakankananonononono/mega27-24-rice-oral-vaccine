"""Printed Table 2 ratio replay from archived PMC XML; no raw assay inference."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib, json
root = Path(__file__).resolve().parents[1]
source = root / 'data/sources/pmc7814724.xml'
soup = BeautifulSoup(source.read_bytes(), 'xml')
table = soup.find('table-wrap', {'id': 'Tab2'})
assert table and 'allerg' in table.get_text().lower()
rows = []
for tr in table.find_all('tr')[1:]:
    cells = [c.get_text(' ', strip=True) for c in tr.find_all('td')]
    assert len(cells) == 8, cells
    msb, nsb, printed = int(cells[5]), int(cells[6]), float(cells[7])
    exact = nsb / msb
    rows.append({'description': cells[0], 'accession_printed': cells[1],
                 'msb_psm_printed': msb, 'nsb_psm_printed': nsb,
                 'ratio_printed': printed, 'ratio_exact_from_counts': round(exact, 6),
                 'ratio_rounds_to_printed': abs(exact-printed) < 0.00050001})
assert len(rows) == 6
out = {'source_url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7814724/',
       'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
       'table': 'Table 2', 'rows': rows,
       'all_six_ratios_round_to_printed': all(x['ratio_rounds_to_printed'] for x in rows),
       'ratios_below_one': sum(x['ratio_exact_from_counts'] < 1 for x in rows),
       'ratios_above_one': sum(x['ratio_exact_from_counts'] > 1 for x in rows),
       'ratio_of_summed_psm': round(sum(x['nsb_psm_printed'] for x in rows) / sum(x['msb_psm_printed'] for x in rows), 6),
       'limits': ['Six published aggregated Table 2 rows only; not independently fetched protein accession records or individual seed-level replicates',
                  'PSM ratios do not measure allergenicity, safety, antigen dose or immune response',
                  'Allergen labels here reflect the article; no independent protein annotation audit'],
       'gate_credit': {'external_services': 0, 'fetched_and_used_accession_datasets': 0, 'audited_derivations': 0, 'paper_pages': 0}}
print(json.dumps(out, indent=2, sort_keys=True))
