import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_supp_string_lengths():
 d=json.loads(subprocess.check_output([sys.executable,str(R/'scripts/audit_19a_supp_string_lengths.py')],text=True))
 assert d==json.loads((R/'results/19a_supp_string_lengths.json').read_text())
 c=d['checks']
 assert c['table4_all_lengths_match_printed'] is True and c['table4_mismatches']==[]
 assert c['table4_designed_lengths_row']==[90,90,89,80,80,80,67]
 assert c['table4_designed_row_matches_labels'] is True
 assert len(c['table4_rows'])==7
 assert c['table2_primer_count']==19
 lo,hi=c['table2_primer_length_range']
 assert 15<=lo and hi<=30
 names=[p['name'] for p in c['table2_primers']]
 assert 'CTB-F' in names and '10TLend5' in names and 'Glu B-R' in names
 assert all(v==0 for v in d['gate_credit'].values())
