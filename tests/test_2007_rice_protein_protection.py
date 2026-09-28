from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
def test_2007_replay():
    out=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_2007_rice_protein_protection.py')],text=True))
    assert out==json.loads((ROOT/'results/2007_rice_protein_protection.json').read_text())
    assert out['pepsin_initial_ctb_ug']==15
    assert out['implied_reported_ctb_ug_per_mg_powder_in_both_2007_contexts']==1.5
    assert out['gate_credit']['audited_derivations']==0
