import json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def test_table1_replay():
    actual = json.loads(subprocess.check_output(['python3', str(ROOT / 'scripts/audit_51a_table1_sequencing.py')], text=True))
    assert actual == json.loads((ROOT / 'results/51a_table1_sequencing.json').read_text())
    c = actual['checks']
    assert c['all_six_mapping_rates_round_correctly']
    assert c['ena_run_listing_bijective_with_printed_experiments'] and c['ena_run_count'] == 6
    assert not c['depth_reproducible_from_printed_inputs']
