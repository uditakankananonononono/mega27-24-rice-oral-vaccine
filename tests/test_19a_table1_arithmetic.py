import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_table1_source_arithmetic():
 d=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/audit_19a_table1_arithmetic.py')],text=True))
 assert d==json.loads((R/'results/19a_table1_arithmetic.json').read_text())
 assert [r['rounds_to_printed_integer_percent'] for r in d['rows']]==[True]*4+[False]
 assert d['gate_credit']['audited_derivations']==0
