"""Replay the published 19A shared-protein shotgun-MS supplement table, not raw proteomics."""
from pathlib import Path
import hashlib,json,math,re,statistics,subprocess
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/PMC10978600_DataSheet_1.pdf'
lines=subprocess.check_output(['pdftotext','-layout','-nopgbrk',str(p),'-'],text=True).splitlines()
start=next(i for i,l in enumerate(lines) if 'Table 5' in l)
caption=lines[start].strip()
region=[l for l in lines[start+1:] if l.strip()]
num=r'(\d+(?:\.\d+)?)'
strict=re.compile(r'^\s*(\S+(?:\s\d{6,}\.\d+)?)\s{2,}.*?\s+'+r'\s+'.join([num]*9)+r'\s*$')
rows=[];rejected=[]
for l in region:
 m=strict.match(l)
 if m:
  g=m.groups()
  rows.append({'accession':g[0].replace(' ','_'),'printed_with_space':' ' in g[0],'psms_a':int(g[1]),'aas_a':int(g[2]),'mw_a':float(g[3]),'pi_a':float(g[4]),'psms_b':int(g[5]),'aas_b':int(g[6]),'mw_b':float(g[7]),'pi_b':float(g[8]),'printed_ratio':float(g[9])})
 else:
  rejected.append(l)
assert len(rows)==43 and len({r['accession'] for r in rows})==43
assert all(r['aas_a']==r['aas_b'] and r['mw_a']==r['mw_b'] and r['pi_a']==r['pi_b'] for r in rows)
assert all(abs(r['psms_a']/r['psms_b']-r['printed_ratio'])<.0005 for r in rows)
orphan_re=re.compile(r'^\D*(\d+\.\d+)\s*$')
orphan_numbers=[orphan_re.match(l.strip()).group(1) for l in rejected if orphan_re.match(l.strip())]
loose=re.compile(r'^\s*(\S+)\s+.*?\s+'+r'\s+'.join([num]*8)+r'\s*$')
defects=[];header_layout=[]
for l in rejected:
 m=loose.match(l)
 if m:
  g=m.groups()
  defects.append({'accession':g[0],'eight_numeric_fields':[float(x) for x in g[1:]]})
 elif not orphan_re.match(l.strip()):
  header_layout.append(l.strip())
assert len(defects)==2 and len(orphan_numbers)==1
# BAA77337.1: printed ratio orphaned onto its own line; 6/2 matches the orphan 3.000
d0=defects[0]
assert d0['accession']=='BAA77337.1' and abs(d0['eight_numeric_fields'][0]/d0['eight_numeric_fields'][4]-float(orphan_numbers[0]))<.0005
# BAD68706.l: 19A PSM cell blank; printed ratio 3.000 with 3 WT PSMs implies 9, not printed
d1=defects[1]
assert d1['accession']=='BAD68706.l' and d1['eight_numeric_fields'][3]==3 and d1['eight_numeric_fields'][7]==3.0
last_data_line=max(i for i,l in enumerate(lines) if 'BAF17027.1' in l)
last_nonempty=max(i for i,l in enumerate(lines) if l.strip())
xs=[r['psms_a'] for r in rows];ys=[r['psms_b'] for r in rows]
def r2(x,y):
 a=statistics.mean(x);b=statistics.mean(y);cov=sum((u-a)*(v-b) for u,v in zip(x,y));v1=sum((u-a)**2 for u in x);v2=sum((v-b)**2 for v in y)
 return (cov*cov)/(v1*v2)
ratios=[r['printed_ratio'] for r in rows]
result={'source_url':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10978600/supplementaryFiles','supplement':'PMC10978600_DataSheet_1.pdf','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'caption_as_printed_in_text_layer':caption,'strict_rows':len(rows),'accessions_printed_with_internal_space':sum(r['printed_with_space'] for r in rows),'defective_printed_rows':[{'accession':'BAA77337.1','defect':'ratio value orphaned onto a separate line','orphan_value':orphan_numbers[0],'psms_a':6,'psms_b':2},{'accession':'BAD68706.l','defect':'19A PSM cell blank in the PDF','psms_b':3,'printed_ratio':3.0,'implied_19a_psms_unprinted':9}],'table_extends_to_document_end':last_data_line==last_nonempty,'all_strict_ratios_gte_2':min(ratios)>=2.0,'psm_sum_19a':sum(xs),'psm_sum_wt':sum(ys),'psm_ratio_of_sums':sum(xs)/sum(ys),'printed_ratio_median':statistics.median(ratios),'printed_ratio_minmax':[min(ratios),max(ratios)],'raw_psm_pearson_r_squared':r2(xs,ys),'log1p_psm_pearson_r_squared':r2([math.log1p(x) for x in xs],[math.log1p(y) for y in ys]),'count_ratio_above_2':sum(r>2 for r in ratios),'count_ratio_equal_2':sum(r==2 for r in ratios),'limits':['Published supplementary protein-level aggregated PSM counts, not individual seed-level replicates, not raw spectra, not independently accessioned datasets','Printed table covers only 19A/WT ratios >= 2.000 and ends at the document end; no filter is stated in the caption, so this is a subset of shared proteins, not the complete shared-protein list the 51A supplement provides','Two printed rows carry layout or blank-cell defects and are excluded from the strict replay; implied values are recorded, not filled in','PSM abundance cannot be equated to antigen dose, immune efficacy or storage/digestion stability; exploratory audits do not establish a comparator win'],'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(result,indent=2,sort_keys=True))
