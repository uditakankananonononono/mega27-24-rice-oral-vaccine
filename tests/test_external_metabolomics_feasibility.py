import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_external_feasibility_reproduces():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/check_external_metabolomics_feasibility.py')],text=True))
 assert actual==json.loads((R/'results/external_metabolomics_feasibility.json').read_text())
 assert actual['MTBLS288']['feature_rows']==31 and actual['MTBLS801']['feature_rows']==911
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
