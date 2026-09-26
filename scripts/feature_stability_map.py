"""Exploratory feature robustness under leave-one-out and transform perturbations.

Post-outcome design. Not a confirmatory prediction, antigen claim or source of vaccine design.
"""
from pathlib import Path
import csv, hashlib, json, math, statistics
R=Path(__file__).resolve().parents[1]
source=R/'data/sources/MTBLS437_maf.tsv'
rows=list(csv.DictReader(source.open(newline=''),delimiter='\t'))
cols=[f'MR-CTB51A_replicate{i}' for i in range(1,5)]+[f'NPB-HP_replicate{i}' for i in range(1,6)]
features=[r for r in rows if r['metabolite_identification'].strip().lower() not in ('','unknown')]
assert len(features)==212

def effects(values, labels):
 a=[x for x,l in zip(values,labels) if l]; b=[x for x,l in zip(values,labels) if not l]
 assert len(a)>=3 and len(b)>=4
 full=statistics.mean(a)-statistics.mean(b)
 loo=[]
 for i in range(len(values)):
  aa=[x for j,x in enumerate(values) if labels[j] and j!=i]
  bb=[x for j,x in enumerate(values) if not labels[j] and j!=i]
  loo.append(statistics.mean(aa)-statistics.mean(bb))
 return full,loo
labels=[True]*4+[False]*5
result_rows=[]
for idx,r in enumerate(features):
 x=[float(r[c]) for c in cols]
 log_full,log_loo=effects([math.log(v) for v in x],labels)
 raw_full,raw_loo=effects(x,labels)
 # Direction consistency across all 9 deletions and raw/log transforms;
 # a small descriptive stability object, not an independent-data score.
 def sign(x):return 0 if x==0 else (1 if x>0 else -1)
 dirs=[sign(y) for y in log_loo+raw_loo]
 stable=sum(y==sign(log_full) for y in dirs)/len(dirs)
 result_rows.append({'row_index':idx,'name':r['metabolite_identification'],
  'database_id':r['database_identifier'],'log_effect':log_full,'raw_effect':raw_full,
  'direction_stability':stable,'log_loo_effect_range':[min(log_loo),max(log_loo)]})
# Negative control: rotate the nine labels (without altering matrix) to test how readily
# the same simplistic stability rule also fires on biologically meaningless assignments.
control_counts=[]
for shift in range(1,9):
 rotated=labels[shift:]+labels[:shift]
 n=0
 for r in features:
  x=[float(r[c]) for c in cols]
  d,log_loo=effects([math.log(v) for v in x],rotated)
  _,raw_loo=effects(x,rotated)
  if d!=0 and all(v*d>0 for v in log_loo+raw_loo):n+=1
 control_counts.append(n)
result={'source':'https://www.ebi.ac.uk/metabolights/ws/studies/MTBLS437/download?file=m_MTBLS437_seed_metabolome_metabolite_profiling_mass_spectrometry_v2_maf.tsv',
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'feature_rows':len(result_rows),'sample_columns':cols,
 'fully_stable_direction_rows':sum(r['direction_stability']==1 for r in result_rows),
 'rotated_label_fully_stable_counts':control_counts,
 'rows':result_rows,
 'limitations':['Designed after seeing outcome values; feature-stability results exploratory and potentially overfit','Leave-one-out shares almost all samples and is not independent validation','Raw-versus-log direction is often invariant to monotonic transforms but mean effects need not be; two transforms are not broad preprocessing validation','Rotations are not a null with proven exchangeability under batch/condition confounding','Rows are correlated and repeated metabolite names remain; no independently held-out cohort or fair strongest comparator','Metabolite peak ratios do not measure antigen dose or vaccine efficacy'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
