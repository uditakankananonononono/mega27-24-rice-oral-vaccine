"""Post-outcome exploratory descriptive matrix audit. Not confirmatory or vaccine efficacy."""
import csv,hashlib,itertools,json,math,statistics
from pathlib import Path
R=Path(__file__).resolve().parents[1]; source=R/'data/sources/MTBLS437_maf.tsv'
rows=list(csv.DictReader(source.open(newline=''),delimiter='\t'))
cols=[f'MR-CTB51A_replicate{i}' for i in range(1,5)]+[f'NPB-HP_replicate{i}' for i in range(1,6)]
# This small contrast was chosen after source values had already been inspected, so p-values are exploratory only.
features=[r for r in rows if r['metabolite_identification'].strip().lower() not in ('','unknown')]
assert len(features)==212
matrix=[]
for r in features:
 v=[math.log(float(r[c])) for c in cols]
 mean=statistics.mean(v); sd=statistics.stdev(v)
 if sd: matrix.append([(x-mean)/sd for x in v])
assert len(matrix)==212

def separation(indices):
 a=set(indices); b=[j for j in range(9) if j not in a]
 return sum((sum(v[j] for j in a)/4-sum(v[j] for j in b)/5)**2 for v in matrix)/len(matrix)
original=(0,1,2,3); observed=separation(original)
all_scores=[separation(g) for g in itertools.combinations(range(9),4)]
rank=sum(x>=observed-1e-12 for x in all_scores)
# Leave-one-replicate-out descriptive stability of the observed group mean difference.
rowdiff=[statistics.mean(v[:4])-statistics.mean(v[4:]) for v in matrix]
result={'source':'https://www.ebi.ac.uk/metabolights/ws/studies/MTBLS437/download?file=m_MTBLS437_seed_metabolome_metabolite_profiling_mass_spectrometry_v2_maf.tsv',
 'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
 'contrast':'MR-CTB51A versus NPB-HP, 4 versus 5 published processed peak-ratio profiles',
 'named_feature_rows':len(features),'matrix_rows':len(matrix),'sample_names':cols,
 'statistic':'mean squared group-centroid separation over rowwise standardized log intensity ratios',
 'observed':observed,'enumerated_label_partitions':len(all_scores),'partitions_at_least_as_large':rank,
 'exploratory_label_fraction':rank/len(all_scores),
 'top_named_rows_by_absolute_log_difference':[{'name':r['metabolite_identification'],'database_id':r['database_identifier'],'mean_log_difference':d} for d,r in sorted(zip([statistics.mean([math.log(float(r[c])) for c in cols[:4]])-statistics.mean([math.log(float(r[c])) for c in cols[4:]]) for r in features],features),key=lambda z:abs(z[0]),reverse=True)[:5]],
 'limitations':['Contrast and statistic chosen after table values inspected: label fraction is descriptive, NOT a confirmatory p-value or novelty proof','Shared growth/processing/batch conditions and nonrandom samples may invalidate label exchangeability','Peak-ratio differences do not measure antigen amount, oral dose, digestion survival or protection','Rows include repeated metabolite names and correlated peaks; no independent external validation','No strongest-comparator tool benchmark was run'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
