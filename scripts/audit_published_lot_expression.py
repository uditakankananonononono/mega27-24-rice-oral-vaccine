"""Reconcile distinct published rice oral-antigen lot summaries without inferring efficacy."""
from pathlib import Path
import hashlib,json,re
from bs4 import BeautifulSoup
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/pmc10978600.xml';s=BeautifulSoup(p.read_text(),'xml')
paras=[x.get_text(' ',strip=True).replace('\u00a0',' ') for x in s.find_all('p')]
claims={
 'lot_expression':r'SDS-PAGE densitometric analysis \(n=3 lot\) showed that the CTB protein level was 4\.94 ± 0\.29 μg/mg in line 19A and 6\.52 ± 0\.22 μg/mg in line 51A\.',
 'cultivation':'three consecutive cultivation experiments',
 'yield_sample':'six randomly selected plants',
}
matched={}
for key,pattern in claims.items():
 hits=[x for x in paras if re.search(pattern,x)]
 assert hits,(key,pattern)
 matched[key]=hits[0]
mean19,sd19,mean51,sd51=4.94,.29,6.52,.22
out={'source':'https://pmc.ncbi.nlm.nih.gov/articles/PMC10978600/',
 'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
 'source_claims':matched,
 'lot_summary':{'19A_mean_ug_per_mg':mean19,'19A_reported_plus_minus_ug_per_mg':sd19,'51A_mean_ug_per_mg':mean51,'51A_reported_plus_minus_ug_per_mg':sd51,'n_lots_reported':3,
   'difference_51A_minus_19A_ug_per_mg':mean51-mean19,
   'ratio_19A_over_51A':mean19/mean51,
   'reported_plus_minus_semantics':'not inferred from displayed paragraph; inspect original figure/statistical methods before treating as SD or SEM'},
 'limits':['This is an author-reported three-lot result and not individual lot measurements or an independent re-analysis.','The 19A/51A context includes distinct line and cultivation conditions; arithmetic difference is descriptive, not causal or a same-task model benchmark.','Cultivation yield sampled six plants per round, while antigen content is reported for n=3 lots; do not equate plant-level yield samples with antigen biological replicates.','Published protein amount is not intestinal delivered dose, vaccine efficacy or storage/digestion robustness.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
