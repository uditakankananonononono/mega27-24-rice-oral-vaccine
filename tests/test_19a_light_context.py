import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_replay():
    actual=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/audit_19a_light_context.py')],text=True))
    expected=json.loads((ROOT/'results/19a_light_context.json').read_text())
    assert actual==expected
    assert actual['checks']['same_light_range_printed_for_51A_comparator']
    assert actual['checks']['descriptive_floor_over_historical_mean_percent']==17.7
    assert not actual['checks']['high_light_sunlight_yield_data_shown']
