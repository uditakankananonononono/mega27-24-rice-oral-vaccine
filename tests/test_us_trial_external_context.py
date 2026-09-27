from pathlib import Path
import json, subprocess
R=Path(__file__).resolve().parents[1]
def test_us_trial_external_context():
    result=json.loads(subprocess.check_output(['python3',str(R/'scripts/audit_us_trial_external_context.py')],text=True))
    assert result==json.loads((R/'results/us_trial_external_context.json').read_text())
    assert result['us_trial']['dose_g']==result['japan_trial']['dose_g_in_6g_cohort']==6
    assert result['gate_credit']['fetched_and_used_accession_datasets']==0
