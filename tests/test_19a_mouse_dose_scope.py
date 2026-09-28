from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1]
def test_mouse_dose_scope():
    x=json.loads(subprocess.check_output(['python3',str(R/'scripts/audit_19a_mouse_dose_scope.py')],text=True))
    assert x==json.loads((R/'results/19a_mouse_dose_scope.json').read_text())
    assert x['mouse_administration_counts']=={'methods':4,'figure_6_caption':5}
    assert abs(x['implied_ctb_ug_per_mg_powder']-4.94)<0.01
    assert x['gate_credit']['fetched_and_used_accession_datasets']==0
