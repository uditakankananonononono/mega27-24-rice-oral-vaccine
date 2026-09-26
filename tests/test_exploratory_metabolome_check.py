import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_exploratory_matrix_result_replays():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/exploratory_metabolome_check.py')],text=True))
 assert actual==json.loads((R/'results/exploratory_metabolome_check.json').read_text())
 assert actual['enumerated_label_partitions']==126
 assert actual['named_feature_rows']==212
 assert actual['gate_credit']['audited_derivations']==0
 assert any('NOT a confirmatory' in x for x in actual['limitations'])
