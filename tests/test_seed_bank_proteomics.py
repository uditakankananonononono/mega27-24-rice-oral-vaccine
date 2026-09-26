import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_seed_bank_replay():
 p=subprocess.run([sys.executable,str(R/'scripts/audit_seed_bank_proteomics.py')],capture_output=True,text=True,check=True)
 d=json.loads(p.stdout)
 assert d==json.loads((R/'results/seed_bank_proteomics_check.json').read_text())
 assert d['common_protein_rows']==477 and d['gate_credit']['fetched_and_used_accession_datasets']==0
