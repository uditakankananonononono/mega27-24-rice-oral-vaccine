"""Exploratory, identifier-deduped robustness check on nine published seed samples.

Post-outcome contrast, not independent validation or an oral-dose measure.
"""
import csv,hashlib,json,math,statistics
from collections import defaultdict
from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=R/'data/sources/MTBLS437_maf.tsv'
cols=[f'MR-CTB51A_replicate{i}' for i in range(1,5)]+[f'NPB-HP_replicate{i}' for i in range(1,6)]
labels=[True]*4+[False]*5

def load_analytes(path):
 rows=list(csv.DictReader(path.open(newline=''),delimiter='\t'))
 groups=defaultdict(list)
 for r in rows:
  name=r['metabolite_identification'].strip()
  if name.lower() in ('','unknown'): continue
  key=r['database_identifier'].strip().upper() or 'NAME:'+name.lower()
  groups[key].append(r)
 result={}
 for key,group in groups.items():
  values=[]
  for c in cols:
   valid=[]
   for r in group:
    try: v=float(r[c])
    except (ValueError,TypeError,KeyError): continue
    if math.isfinite(v) and v>0: valid.append(v)
   values.append(statistics.median(valid) if valid else None)
  result[key]=values
 return rows,result

def effect(values,labels):
 a=[v for v,l in zip(values,labels) if l];b=[v for v,l in zip(values,labels) if not l]
 return statistics.mean(a)-statistics.mean(b)

def stable(values,labels):
 if any(v is None for v in values): return None
 raw=effect(values,labels);log=[math.log(v) for v in values]
 lg=effect(log,labels)
 loo=[]
 for i in range(len(values)):
  mask=[j for j in range(len(values)) if j!=i]
  x=[values[j] for j in mask];z=[log[j] for j in mask];y=[labels[j] for j in mask]
  loo.extend([effect(x,y),effect(z,y)])
 return raw!=0 and lg!=0 and raw*lg>0 and all(v*lg>0 for v in loo)

rows,analytes=load_analytes(source)
valid={key:v for key,v in analytes.items() if all(x is not None for x in v)}
observed={key:stable(v,labels) for key,v in valid.items()}
rotations=[]
for shift in range(1,9):
 rotated=labels[shift:]+labels[:shift]
 rotations.append({'shift':shift,'fully_stable_analytes':sum(stable(v,rotated) for v in valid.values())})
output={'source':'https://www.ebi.ac.uk/metabolights/MTBLS437',
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'named_feature_rows':sum(r['metabolite_identification'].strip().lower() not in ('','unknown') for r in rows),
 'distinct_analyte_keys':len(analytes),'analytes_with_all_nine_positive_values':len(valid),
 'fully_stable_analytes':sum(observed.values()),'rotated_label_counts':rotations,
 'sample_columns':cols,'protocol':'database identifier, falling back to name only when no identifier; median collapse of duplicate rows in each sample; finite positive values; same nine-sample contrast and eight label rotations as feature_stability_map.py',
 'limits':['Exploratory post-outcome contrast; not a preregistered test','Rotated labels are negative controls, not an exchangeable randomization null or p-value','The nine samples are shared with the feature-row analysis; deduplication does not create an independent cohort','No oral antigen dose, vaccine efficacy, or strongest-comparator result follows'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(output,indent=2,sort_keys=True))
