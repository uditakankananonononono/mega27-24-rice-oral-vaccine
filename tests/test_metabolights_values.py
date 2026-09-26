import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_value_audit_reproduces_and_does_not_count_features_as_datasets():
    actual=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/audit_metabolights_values.py')],text=True))
    expected=json.loads((ROOT/'results/metabolights_value_audit.json').read_text())
    assert actual==expected
    assert actual['feature_rows']==351 and actual['sample_columns']==18
    assert sum(c['numeric'] for c in actual['values_by_sample'].values())==6318
    assert actual['unknown_name_rows']==139
    assert actual['gate_credit']['fetched_and_used_accession_datasets']==0
