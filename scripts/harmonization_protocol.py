"""Preregistered-style dedupe/normalization protocol and cross-study harmonization feasibility audit.

Protocol (fixed before any cross-study outcome analysis):
 1. Keep only MAF rows with a nonempty, non-'unknown' metabolite identification.
 2. Key each analyte by database_identifier; fall back to the normalized name string only when
    the identifier is empty. Never merge two different identifiers on name similarity alone.
 3. Within one study, collapse duplicate rows of the same key to the per-sample median.
 4. A numeric sample column must parse as a finite positive float for every kept value.
 5. Cross-study quantitative pooling requires a shared internal standard, comparable units and a
    batch bridge; when any is absent, report 'not harmonizable' rather than forcing a join.
"""
import csv,hashlib,json,math,statistics
from pathlib import Path
R=Path(__file__).resolve().parents[1]
STUDIES={
 'MTBLS437':[R/'data/sources/MTBLS437_maf.tsv'],
 'MTBLS288':[R/'data/sources/m_MTBLS288_dynamic_metabolomics_of_rice_grain_metabolite_profiling_mass_spectrometry_v2_maf.tsv'],
 'MTBLS801_split':[R/'data/sources/m_MTBLS801_Split_GC_mass_spectrometry_v2_maf.tsv'],
 'MTBLS801_splitless':[R/'data/sources/m_MTBLS801_Splitless_GC_mass_spectrometry_v2_maf.tsv'],
}
META={'database_identifier','chemical_formula','smiles','inchi','metabolite_identification','mass_to_charge','fragmentation','modifications','charge','retention_time','taxid','species','database','database_version','reliability','uri','search_engine','search_engine_score','smallmolecule_abundance_sub','smallmolecule_abundance_stdev_sub','smallmolecule_abundance_std_error_sub','assigned_chebi_identifier','assigned_refmet_identifier','chebi_identifier','chebi_identifier_search_status','chebi_identifier_search_time','refmet_identifier_search_status','refmet_identifier_search_time'}
def load(paths):
 rows=[]
 for p in paths:
  with p.open(newline='') as f: rows.extend(list(csv.DictReader(f,delimiter='\t')))
 return rows
def audit(study,paths):
 rows=load(paths)
 named=[r for r in rows if r['metabolite_identification'].strip().lower() not in ('','unknown')]
 sample_cols=[c for c in rows[0] if c not in META and c]
 keyed={}; name_fallback=0
 for r in named:
  key=r['database_identifier'].strip().upper()
  if not key:
   key='NAME:'+r['metabolite_identification'].strip().lower(); name_fallback+=1
  vals={}
  for c in sample_cols:
   try: v=float(r[c])
   except (ValueError,KeyError): continue
   if math.isfinite(v) and v>0: vals[c]=v
  if key in keyed:
   for c,v in vals.items(): keyed[key].setdefault(c,[]).append(v)
  else: keyed[key]={c:[v] for c,v in vals.items()}
 analytes={k:{c:statistics.median(v) for c,v in cols.items() if v} for k,cols in keyed.items()}
 dup_rows=len(named)-len(analytes)
 return {'files':[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths],
  'feature_rows':len(rows),'named_rows':len(named),'distinct_analytes':len(analytes),
  'duplicate_rows_collapsed_by_median':dup_rows,'named_rows_without_identifier':name_fallback,
  'sample_columns':len(sample_cols),'analytes':set(analytes)}
res={}
sets={}
for s,p in STUDIES.items():
 a=audit(s,p); sets[s]=a.pop('analytes'); res[s]=a
assert res['MTBLS437']['named_rows']==212
res['identifier_overlap_with_MTBLS437_deduped']={s:len(sets[s]&sets['MTBLS437']) for s in sets if s!='MTBLS437'}
res['name_only_keys_excluded_from_overlap']=True
res['harmonization_verdict']={
 'shared_internal_standard_between_studies':False,
 'comparable_units_between_studies':False,
 'batch_bridge_or_reference_samples':False,
 'quantitative_pooling':'not defensible: MTBLS437 peak-intensity ratios to internal standards (testosterone/ribitol) vs platform-specific processed GC-MS values in MTBLS288/801; no shared reference sample or batch bridge',
 'allowed_use':'analyte-presence overlap and within-study contrasts only'}
res['limits']=['Dedupe collapses feature rows to distinct identifiers; it does not create independent measurements or new accession datasets','MTBLS288/801 study different biological questions (development, field stress) and are not held-out MucoRice cohorts','Harmonization verdict is a protocol-level result about data comparability, not a biological finding or comparator win']
res['gate_credit']={'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}
print(json.dumps(res,indent=2,sort_keys=True))
