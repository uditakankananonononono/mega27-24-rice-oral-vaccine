import json
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_source_screen_reproduces_committed_result():
    got=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/check_source_eligibility.py')],text=True))
    expected=json.loads((ROOT/'results/source_eligibility.json').read_text())
    assert got==expected
    assert got['run_count']==6
    assert got['gate_credit']=={'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}
    assert 'DRX011151' not in {row['experiment_accession'] for row in got['runs']}
