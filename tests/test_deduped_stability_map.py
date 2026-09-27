import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_deduped_stability_replays_and_bounds():
 actual=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/deduped_stability_map.py')],text=True))
 assert actual==json.loads((R/'results/deduped_stability_map.json').read_text())
 assert actual['named_feature_rows']==212
 assert actual['distinct_analyte_keys']==104
 assert actual['analytes_with_all_nine_positive_values']==104
 assert 0<=actual['fully_stable_analytes']<=104
 assert len(actual['rotated_label_counts'])==8
 assert actual['gate_credit']['audited_derivations']==0
