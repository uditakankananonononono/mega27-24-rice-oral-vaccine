from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1]
def test_registry_identity():
    x=json.loads(subprocess.check_output(['python3',str(R/'scripts/audit_phase1_registry_identity.py')],text=True))
    assert x==json.loads((R/'results/phase1_registry_identity.json').read_text())
    assert [q['umin_id'] for q in x['registries']]==['UMIN000009688','UMIN000018001']
    assert x['gate_credit']['fetched_and_used_accession_datasets']==0
