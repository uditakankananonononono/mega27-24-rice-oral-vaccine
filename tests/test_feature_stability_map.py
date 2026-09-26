import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_feature_stability_map_replays():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/feature_stability_map.py')],text=True))
 assert actual==json.loads((R/'results/feature_stability_map.json').read_text())
 assert len(actual['rows'])==212 and len(actual['rotated_label_fully_stable_counts'])==8
 assert all(0<=x['direction_stability']<=1 for x in actual['rows'])
 assert actual['gate_credit']['audited_derivations']==0
