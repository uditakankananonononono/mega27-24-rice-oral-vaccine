import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_all_partitions_replay():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/exhaustive_label_sensitivity.py')],text=True))
 assert actual==json.loads((R/'results/exhaustive_label_sensitivity.json').read_text())
 assert len(actual['counts_by_group'])==126
 assert actual['counts_by_group']['0,1,2,3']==actual['observed_stable_count']==95
 assert actual['assignments_with_count_at_least_observed']>=2
 assert actual['gate_credit']['audited_derivations']==0
