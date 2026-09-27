"""Printed-number replay of the 2021 seed-bank paper Table 1 sequencing summary.

Replays the six printed sample rows (printed totals, mapped counts, rates,
coverage, depth), checks the printed mapping-rate arithmetic, checks the
printed depth against the paper's own stated definition, and cross-checks the
printed DDBJ experiment accessions against the archived ENA run listing for
the study. Pure print-layer and archive-metadata QC.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import csv, hashlib, io, json, re
ROOT = Path(__file__).resolve().parents[1]
xml = ROOT / 'data/sources/pmc7814724.xml'
tsv = ROOT / 'data/sources/DRA011151_ena_runs.tsv'
raw = xml.read_bytes()
soup = BeautifulSoup(raw, 'xml')
table = next(t for t in soup.find_all('table-wrap') if 'DRX246636' in t.get_text())
rows = []
for tr in table.find_all('tr'):
    cells = [c.get_text(' ', strip=True) for c in tr.find_all(['td', 'th'])]
    if len(cells) >= 8 and re.search(r'DRX\d+', cells[-1]):
        nums = [c.replace(',', '') for c in cells[2:7]]
        rows.append({'run_code': cells[0], 'sample_code': cells[1],
                     'total_reads': int(nums[0]), 'mapped_reads': int(nums[1]),
                     'printed_mapping_rate_pct': float(nums[2]),
                     'printed_coverage_rate_pct': float(nums[3]),
                     'printed_depth': float(nums[4]),
                     'printed_experiment_accession': cells[-1].strip()})
assert len(rows) == 6
REF_BP = 373_245_519  # reference size printed in the methods paragraph
for r in rows:
    r['calculated_mapping_rate_pct'] = round(100 * r['mapped_reads'] / r['total_reads'], 2)
    r['mapping_rate_rounds_to_printed'] = abs(r['calculated_mapping_rate_pct'] - r['printed_mapping_rate_pct']) < 0.005 + 1e-9
    covered_bp = r['printed_coverage_rate_pct'] / 100 * REF_BP
    r['depth_if_stated_definition'] = round(r['mapped_reads'] * 100 / covered_bp, 2)
    r['depth_printed_over_stated_definition'] = round(r['printed_depth'] / r['depth_if_stated_definition'], 3)
    r['depth_matches_stated_definition'] = abs(r['printed_depth'] - r['depth_if_stated_definition']) < 0.5
ena = list(csv.DictReader(io.StringIO(tsv.read_text()), delimiter='\t'))
exp_from_ena = sorted(x['experiment_accession'] for x in ena)
exp_printed = sorted(r['printed_experiment_accession'] for r in rows)
bijective = exp_from_ena == exp_printed and len(ena) == 6
out = {
 'source_url': 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7814724/',
 'ena_report_url': 'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=DRA011151&result=read_run&fields=run_accession%2Cexperiment_accession%2Csample_accession&format=tsv',
 'source_file': xml.name, 'article_sha256': hashlib.sha256(raw).hexdigest(),
 'ena_report_sha256': hashlib.sha256(tsv.read_bytes()).hexdigest(),
 'reference_bp_printed_in_methods': REF_BP,
 'checks': {
   'rows': rows,
   'all_six_mapping_rates_round_correctly': all(r['mapping_rate_rounds_to_printed'] for r in rows),
   'depth_reproducible_from_printed_inputs': any(r['depth_matches_stated_definition'] for r in rows),
   'printed_over_stated_depth_ratio_range': [min(r['depth_printed_over_stated_definition'] for r in rows),
                                             max(r['depth_printed_over_stated_definition'] for r in rows)],
   'ena_run_listing_bijective_with_printed_experiments': bijective,
   'ena_run_count': len(ena)},
 'finding': 'All six printed mapping rates replay exactly from the printed read counts, and the six printed DDBJ experiment accessions map one-to-one onto the six ENA run records archived for the study. The printed depth values are not reproducible from the printed inputs under the definition stated in the methods text (printed values range from 0.90x to 1.21x of the stated-definition value with no single systematic factor); the intermediate filtered-read counts the authors used are not printed.',
 'limits': ['Mapping-rate replay and archive-metadata correspondence only; no read payload downloaded or aligned',
            'The depth mismatch is an unresolved reproducibility gap, not proof of an error: the methods text states the formula but the filtered per-read inputs are not printed',
            'Sequencing-summary QC says nothing about seed composition, product quality, or any biological outcome'],
 'gate_credit': {'external_services': 0, 'fetched_and_used_accession_datasets': 0, 'audited_derivations': 0, 'paper_pages': 0}}
print(json.dumps(out, indent=2, sort_keys=True))
