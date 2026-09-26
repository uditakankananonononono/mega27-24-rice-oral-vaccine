"""Check exact analyte identity overlap only; no cross-study outcome analysis."""
from pathlib import Path
import csv,glob,hashlib,json
R=Path(__file__).resolve().parents[1]
files={
 'MTBLS437':[R/'data/sources/MTBLS437_maf.tsv'],
 'MTBLS288':list((R/'data/sources').glob('m_MTBLS288*maf.tsv')),
 'MTBLS801':list((R/'data/sources').glob('m_MTBLS801*maf.tsv')),
}
assert all(files.values())
summary={}; names={}; identifiers={}
for id,paths in files.items():
 rs=[]
 for p in paths:
  with p.open(newline='') as f:rs.extend(csv.DictReader(f,delimiter='\t'))
 names[id]={r['metabolite_identification'].strip().lower() for r in rs if r['metabolite_identification'].strip().lower() not in ('','unknown')}
 identifiers[id]={r['database_identifier'].strip().upper() for r in rs if r['database_identifier'].strip()}
 summary[id]={'feature_rows':len(rs),'unique_named_analytes':len(names[id]),'nonempty_identifiers':len(identifiers[id]),
  'files':[{ 'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]}
for id in ['MTBLS288','MTBLS801']:
 summary[id]['shared_name_strings_with_MTBLS437']=len(names[id]&names['MTBLS437'])
 summary[id]['shared_database_identifiers_with_MTBLS437']=len(identifiers[id]&identifiers['MTBLS437'])
summary['limits']=['MTBLS288 rice grain developmental-stage GC-MS and MTBLS801 heat/drought field cultivar study are not equivalent to MucoRice-CTB 51A; cross-study labels and biological conditions differ.','The MAF tables are processed features, not raw spectra or independently accessioned samples.','No harmonized quantification, normalization or phenotypic validation has been attempted; overlapping names do not imply matched chemical identity or units.','These two sources cannot serve as held-out CTB51A-vs-parent classification cohorts without changing the task.']
summary['gate_credit']={'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}
print(json.dumps(summary,indent=2,sort_keys=True))
