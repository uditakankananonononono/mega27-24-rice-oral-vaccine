import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_cross_context():
 x=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_shared_protein_cross_context.py')],text=True))
 assert x==json.loads((ROOT/'results/shared_protein_cross_context.json').read_text())
 assert x['overlap_count']==4 and x['opposite_ratio_side_count']==2
