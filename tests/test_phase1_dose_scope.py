from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
def test_phase1_dose_scope():
 x=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_phase1_dose_scope.py')],text=True))
 assert x==json.loads((ROOT/'results/phase1_dose_scope.json').read_text())
 assert x['reported_design']['total_allocated']==60
 assert not x['classification']['ctb_content_per_trial_dose_in_abstract']
