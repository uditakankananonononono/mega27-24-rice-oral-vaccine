from pathlib import Path
import csv, json, hashlib
from xml.etree import ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
xml = ROOT/'data/sources/pmc7814724.xml'
tsv = ROOT/'data/sources/DRA011151_ena_runs.tsv'
root=ET.parse(xml).getroot()
body=' '.join(root.itertext())
with tsv.open(newline='') as f: rows=list(csv.DictReader(f,delimiter='\t'))
assert 'DRA011151' in body
assert len(rows)==6 and len({r['run_accession'] for r in rows})==6
assert len({r['experiment_accession'] for r in rows})==6
assert len({r['sample_accession'] for r in rows})==6
assert all(r['run_accession'].startswith('DRR') and r['experiment_accession'].startswith('DRX') for r in rows)
result={
 'sources':{'article':'https://pmc.ncbi.nlm.nih.gov/articles/PMC7814724/','ena_report':'https://www.ebi.ac.uk/ena/portal/api/filereport?accession=DRA011151&result=read_run&fields=run_accession,experiment_accession,sample_accession&format=tsv'},
 'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (xml,tsv)},
 'study':'DRA011151','run_count':len(rows),'runs':rows,
 'paper_availability_accession':'DRX011151',
 'accession_discrepancy':'Paper availability paragraph names DRX011151; ENA run report names DRX246636-DRX246641. Unresolved, not corrected.',
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}
}
print(json.dumps(result,indent=2))
