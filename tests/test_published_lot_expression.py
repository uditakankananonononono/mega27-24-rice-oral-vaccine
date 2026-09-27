import json,subprocess,sys,math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_lot_summary_replays():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/audit_published_lot_expression.py')],text=True))
 assert actual==json.loads((R/'results/published_lot_expression.json').read_text())
 s=actual['lot_summary']
 assert s['n_lots_reported']==3
 assert math.isclose(s['ratio_19A_over_51A'],4.94/6.52)
 assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
