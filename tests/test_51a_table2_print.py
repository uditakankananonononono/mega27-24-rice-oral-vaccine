import json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def test_table2_printed_ratio_replay():
    result = json.loads(subprocess.check_output(['python3', str(ROOT/'scripts/audit_51a_table2_print.py')], text=True))
    assert result == json.loads((ROOT/'results/51a_table2_print.json').read_text())
    assert len(result['rows']) == 6 and result['all_six_ratios_round_to_printed']
    assert result['ratios_below_one'] == 4 and result['ratios_above_one'] == 2
