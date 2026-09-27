"""Compare overlapping printed accession ratios across two distinct rice studies."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
a=R/'data/sources/pmc7814724.xml';b=R/'data/sources/pmc10978600.xml'
x=BeautifulSoup(a.read_bytes(),'xml').find('table-wrap',{'id':'Tab2'})
y=BeautifulSoup(b.read_bytes(),'xml').find('table-wrap',{'id':'T1'})
assert x and y
older={}
for tr in x.find_all('tr')[1:]:
 c=[td.get_text(' ',strip=True) for td in tr.find_all('td')]
 older[re.sub(r'\s+','',c[1])]=float(c[-1])
newer={}
for tr in y.find_all('tr')[1:]:
 c=[td.get_text(' ',strip=True) for td in tr.find_all('td')]
 newer[re.sub(r'\s+','',c[0])]=float(c[-1])
overlap=sorted(older.keys()&newer.keys())
rows=[{'printed_protein_accession':acc,'seed_bank_nsb_over_msb_2021':older[acc],
       'line19a_over_wt_2024':newer[acc],
       'seed_bank_ratio_side_of_one':'above' if older[acc]>1 else 'below',
       'line_ratio_side_of_one':'above' if newer[acc]>1 else 'below'} for acc in overlap]
out={'source_2021':'https://pmc.ncbi.nlm.nih.gov/articles/PMC7814724/',
     'source_2024':'https://pmc.ncbi.nlm.nih.gov/articles/PMC10978600/',
     'source_2021_sha256':hashlib.sha256(a.read_bytes()).hexdigest(),
     'source_2024_sha256':hashlib.sha256(b.read_bytes()).hexdigest(),
     'overlap_count':len(rows),'rows':rows,
     'opposite_ratio_side_count':sum(r['seed_bank_ratio_side_of_one']!=r['line_ratio_side_of_one'] for r in rows),
     'interpretation':'Same printed accession labels can be compared for metadata alignment, but NSB/MSB in a 51A seed-bank generation comparison is a different estimand from 19A/WT in the later line comparison. Neither sign agreement nor disagreement is a biological replication test.',
     'limits':['Ratios are author-reported aggregates from different source contexts and different denominators, not a paired experiment',
               'Protein accession labels are copied from articles; individual protein records and raw PSM payloads were not fetched',
               'No antigen-dose, safety, allergenicity, efficacy, causal, benchmark or discovery inference'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
