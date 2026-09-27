import json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_fulltext_cohort_content():
 x=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_phase1_fulltext_content.py')],text=True))
 assert x==json.loads((ROOT/'results/phase1_fulltext_content.json').read_text())
 assert [r['implied_ctb_mg_per_g_product'] for r in x['trial_printed_contents']]==[3,2,3]
