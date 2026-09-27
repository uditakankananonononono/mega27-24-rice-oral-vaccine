import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_19a_shared_protein_table_replay():
 p=subprocess.run([sys.executable,str(R/'scripts/audit_19a_shared_protein_table.py')],capture_output=True,text=True,check=True)
 d=json.loads(p.stdout)
 assert d==json.loads((R/'results/19a_shared_protein_table_check.json').read_text())
 assert d['strict_rows']==43 and d['gate_credit']['fetched_and_used_accession_datasets']==0
