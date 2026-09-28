from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[1]
def test_provenance_reference_replay():
 x=json.loads(subprocess.check_output(['python3',str(R/'scripts/dose_provenance.py')],text=True))
 assert x==json.loads((R/'results/dose_provenance_reference.json').read_text())
 assert (x['permitted_computations'],x['blocked_cross_context'],x['blocked_unknown_lot'])==(1,3,1)
 assert x['cases'][0]['computed_ctb_ug']==75
 assert all(v['individual_measured_ctb_ug'] is None and v['intestinal_surviving_ctb_ug'] is None for v in x['cases'])
 assert x['gate_credit']['audited_derivations']==0
