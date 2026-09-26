"""Replay the published paired salt-soluble protein PSM supplement, not raw proteomics."""
from pathlib import Path
import hashlib,json,math,re,subprocess,statistics
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/12864_2020_7355_MOESM3_ESM.pdf'
lines=subprocess.check_output(['pdftotext','-layout','-nopgbrk',str(p),'-'],text=True).splitlines()
pat=re.compile(r'^\s*(\d{1,3})\s+.*?\s+(\d+)\s+(\d+)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+)\s+(\d+)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s*$')
rows=[]
for line in lines:
 m=pat.match(line)
 if m:
  n,msb,aa,mw,pi,nsb,naa,nmw,npi,ratio=m.groups()
  rows.append({'row':int(n),'msb_psms':int(msb),'nsb_psms':int(nsb),'printed_ratio':float(ratio),'aa':int(aa),'mw':float(mw)})
assert len(rows)==477 and sorted(r['row'] for r in rows)==list(range(1,478))
source_order=[r['row'] for r in rows]
order_discontinuities=[(source_order[i-1],source_order[i]) for i in range(1,len(rows)) if source_order[i]!=source_order[i-1]+1]
assert order_discontinuities==[(367,392),(460,368),(391,461)]
assert all(r['msb_psms']>0 and r['nsb_psms']>0 and abs(r['nsb_psms']/r['msb_psms']-r['printed_ratio'])<.00051 for r in rows)
xs=[r['msb_psms'] for r in rows];ys=[r['nsb_psms'] for r in rows]
def r2(x,y):
 a=statistics.mean(x);b=statistics.mean(y);cov=sum((u-a)*(v-b) for u,v in zip(x,y));v1=sum((u-a)**2 for u in x);v2=sum((v-b)**2 for v in y)
 return (cov*cov)/(v1*v2)
result={'source_url':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7814724/supplementaryFiles', 'supplement':'12864_2020_7355_MOESM3_ESM.pdf','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'common_protein_rows':len(rows),'pdftotext_row_order_discontinuities':order_discontinuities, 'psm_sum_msb':sum(xs),'psm_sum_nsb':sum(ys),'psm_ratio_of_sums':sum(ys)/sum(xs),'individual_ratio_median':statistics.median(r['nsb_psms']/r['msb_psms'] for r in rows),'individual_ratio_minmax':[min(r['nsb_psms']/r['msb_psms'] for r in rows),max(r['nsb_psms']/r['msb_psms'] for r in rows)],'raw_psm_pearson_r_squared':r2(xs,ys), 'log1p_psm_pearson_r_squared':r2([math.log1p(x) for x in xs],[math.log1p(y) for y in ys]),'count_ratio_below_0_5':sum(r['nsb_psms']/r['msb_psms']<.5 for r in rows),'count_ratio_above_2':sum(r['nsb_psms']/r['msb_psms']>2 for r in rows),'limits':['Published supplementary protein-level aggregated PSM counts, not individual seed-level replicates, not 477 independently accessioned datasets','Shared-protein list excludes proteins unique to either bank; correlations and ratio distribution condition on detected-in-both proteins','PSM abundance cannot be equated to cholera antigen dose, immune efficacy or storage/digestion stability; exploratory audits do not establish a comparator win'],'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
