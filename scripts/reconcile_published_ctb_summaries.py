"""Reconcile published rice CTB summary units and provenance, not efficacy."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    '2021_seed_bank': ('pmc7814724.xml', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7814724/'),
    '2024_line_comparison': ('pmc10978600.xml', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10978600/'),
}
PATTERNS = {
    '2021_seed_bank': r'Average CTB content.*?6\.45\s*±\s*0\.89.*?MSB.*?5\.83\s*±\s*0\.58.*?NSB.*?P\s*=\s*0\.60',
    '2024_line_comparison': r'SDS-PAGE densitometric analysis\s*\(n=3 lot\).*?4\.94\s*±\s*0\.29\s*μg/mg.*?19A.*?6\.52\s*±\s*0\.22\s*μg/mg.*?51A',
}


def replay():
    evidence = {}
    for key, (filename, url) in SOURCES.items():
        raw = (ROOT / 'data/sources' / filename).read_bytes()
        soup = BeautifulSoup(raw, 'xml')
        paragraphs = [p.get_text(' ', strip=True).replace('\u00a0', ' ') for p in soup.find_all('p')]
        hits = [p for p in paragraphs if re.search(PATTERNS[key], p)]
        if not hits:
            raise ValueError('Published summary not found: ' + key)
        evidence[key] = {'url': url, 'archive_sha256': hashlib.sha256(raw).hexdigest(), 'quote': hits[0]}
    return {
        'evidence': evidence,
        'source_reported': {
            '2021_seed_bank': {'line': '51A', 'comparison': 'MSB versus NSB, distinct seed-bank generations', 'MSB_mean_ug_per_mg': 6.45, 'MSB_plus_minus_unspecified': 0.89, 'NSB_mean_ug_per_mg': 5.83, 'NSB_plus_minus_unspecified': 0.58, 'authors_p_value': 0.60},
            '2024_line_comparison': {'lines': '19A versus 51A', 'comparison': 'distinct lines in 2024 study, n=3 lots as reported', 'line19A_mean_ug_per_mg': 4.94, 'line19A_plus_minus_unspecified': 0.29, 'line51A_mean_ug_per_mg': 6.52, 'line51A_plus_minus_unspecified': 0.22},
        },
        'descriptive_arithmetic': {
            '2021_NSB_over_MSB': 5.83 / 6.45,
            '2021_NSB_minus_MSB_ug_per_mg': 5.83 - 6.45,
            '2024_19A_over_51A': 4.94 / 6.52,
            '2024_19A_minus_51A_ug_per_mg': 4.94 - 6.52,
            'between_publications_2024_51A_minus_2021_MSB_ug_per_mg': 6.52 - 6.45,
        },
        'interpretation_limits': [
            'The two publications describe different experimental settings and sample frames; 2024 line 51A must not be treated as a replication of 2021 MSB or NSB.',
            'A small difference between published 51A and MSB means is descriptive coincidence, not an equivalence or stability test.',
            'The displayed ± semantics and per-lot/per-seed values are not established in these passages; do not compute confidence intervals, pool variance, or compare P values.',
            'Authors’ 2021 P=0.60 is not evidence of equivalence; there is no independent dose/digestion or clinical outcome here.',
        ],
        'gate_credit': {'applied_external_services': 0, 'individually_fetched_used_accessions': 0, 'audited_derivations': 0, 'substantive_paper_pages': 0},
    }


if __name__ == '__main__':
    print(json.dumps(replay(), indent=2, sort_keys=True))
