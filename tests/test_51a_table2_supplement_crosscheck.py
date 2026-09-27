from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
def test_supplement_table2_crosscheck():
    result=json.loads(subprocess.check_output(['python3',str(ROOT/'scripts/crosscheck_51a_table2_supplement.py')],text=True))
    assert result==json.loads((ROOT/'results/51a_table2_supplement_crosscheck.json').read_text())
    assert result['all_six_table2_rows_match_supplement']
    assert [r['supplement_row'] for r in result['table2_rows']]==[1,3,5,21,59,16]
