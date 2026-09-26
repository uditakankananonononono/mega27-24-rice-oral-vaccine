"""Descriptive integrity screen of published MTBLS437 values, no antigen design or biological claim."""
import csv, json, math, hashlib
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'data/sources/MTBLS437_maf.tsv'
with source.open(newline='') as f:
    rows=list(csv.DictReader(f,delimiter='\t'))
columns=[x for x in rows[0] if x.startswith(('MR-CTB51A_replicate','NPB-HP_replicate','NPB-PF_replicate','MR-RNAi_replicate'))]
assert len(columns)==18 and len(rows)==351
summary={}
for col in columns:
    values=[r[col].strip() for r in rows]
    numeric=[]; tokens=Counter()
    for value in values:
        try:
            v=float(value)
            if math.isfinite(v): numeric.append(v)
            else: tokens[value]+=1
        except ValueError: tokens[value]+=1
    summary[col]={'numeric':len(numeric),'positive':sum(x>0 for x in numeric),'zero':sum(x==0 for x in numeric),'negative':sum(x<0 for x in numeric),'non_numeric_tokens':dict(tokens)}
ident=Counter(r['metabolite_identification'].strip() for r in rows)
chem=Counter(r['database_identifier'].strip() for r in rows)
result={'study':'MTBLS437','sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'feature_rows':len(rows),'sample_columns':len(columns),'values_by_sample':summary,
 'distinct_metabolite_names':len(ident),'unknown_name_rows':sum(n for k,n in ident.items() if k.lower() in ('unknown','')),
 'distinct_nonempty_database_identifiers':len({k for k in chem if k}),
 'cautions':['Mass-spec feature rows are not independent dataset accessions; many have unknown identification.', 'Numeric cells alone do not establish calibrated comparability across four groups; audit original assay normalization and censoring before testing outcomes.', 'Descriptive source integrity only: no benchmark, biological discovery or derivation gate credit.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
