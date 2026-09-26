import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def test_harmonization_protocol_replay():
 p=subprocess.run([sys.executable,str(R/'scripts/harmonization_protocol.py')],capture_output=True,text=True,check=True)
 d=json.loads(p.stdout)
 assert d==json.loads((R/'results/harmonization_protocol.json').read_text())
 assert d['MTBLS437']['named_rows']==212 and d['MTBLS437']['distinct_analytes']==104
 assert d['MTBLS437']['sample_columns']==18
 assert d['identifier_overlap_with_MTBLS437_deduped']=={'MTBLS288':12,'MTBLS801_split':19,'MTBLS801_splitless':35}
 assert d['harmonization_verdict']['quantitative_pooling'].startswith('not defensible')
 assert d['gate_credit']['fetched_and_used_accession_datasets']==0
