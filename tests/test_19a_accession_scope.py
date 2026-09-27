import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_primary_article_ena_run_scope_replay():
 actual=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/check_19a_accession_scope.py')],text=True))
 assert actual==json.loads((ROOT/'results/19a_accession_scope.json').read_text())
 assert actual['metadata']['library_strategy']=='WGS'
 assert actual['metadata']['run']=='DRR376734'
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
