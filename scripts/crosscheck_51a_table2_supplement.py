"""Cross-check published Table 2 against published shared-protein supplement."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib, json, re, subprocess
R=Path(__file__).resolve().parents[1]
xml=R/'data/sources/pmc7814724.xml'
pdf=R/'data/sources/12864_2020_7355_MOESM3_ESM.pdf'
article=BeautifulSoup(xml.read_bytes(),'xml')
table=article.find('table-wrap',{'id':'Tab2'})
assert table is not None
pairs=[]
for tr in table.find_all('tr')[1:]:
 c=[cell.get_text(' ',strip=True) for cell in tr.find_all('td')]
 assert len(c)==8
 pairs.append({'accession':re.sub(r'\s+','',c[1]),'msb_psm':int(c[5]),'nsb_psm':int(c[6]),'ratio':float(c[7])})
assert len(pairs)==6
text=subprocess.check_output(['pdftotext','-layout','-nopgbrk',str(pdf),'-'],text=True)
rows=[]
lines=text.splitlines()
for target in pairs:
    acc=target['accession']
    matching=[i for i,line in enumerate(lines) if acc in line]
    assert len(matching)==1,(acc,matching)
    i=matching[0]
    candidates=[]
    for nearby in lines[i:i+3]:
        n=re.search(r'^\s*(\d{1,3})\s+.*?\s+(\d+)\s+(\d+)\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+(\d+)\s+\d+\s+\d+(?:\.\d+)?\s+\d+(?:\.\d+)?\s+(\d+\.\d+)\s*$',nearby)
        if n and int(n[2])==target['msb_psm'] and int(n[4])==target['nsb_psm']:candidates.append({'row':int(n[1]),'accession':acc,'msb_psm':int(n[2]),'nsb_psm':int(n[4]),'ratio':float(n[5])})
    assert len(candidates)==1,(acc,candidates)
    rows.extend(candidates)
by_acc={r['accession']:r for r in rows}
checks=[]
for p in pairs:
 q=by_acc.get(p['accession'])
 checks.append({'accession':p['accession'],'found_in_shared_supplement':q is not None,
                'supplement_row':q['row'] if q else None,
                'printed_psm_and_ratio_match':bool(q and all(p[k]==q[k] for k in ('msb_psm','nsb_psm','ratio')))})
out={'paper_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC7814724/',
     'supplement_url':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7814724/supplementaryFiles',
     'article_sha256':hashlib.sha256(xml.read_bytes()).hexdigest(),
     'supplement_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
     'table2_rows':checks,'supplement_matched_target_rows':len(rows),
     'all_six_table2_rows_match_supplement':all(c['printed_psm_and_ratio_match'] for c in checks),
     'limits':['Source-to-source consistency of two parts of the same publication, not independent validation or individual accession fetches',
               'This does not assess allergenicity, antigen dose, vaccine efficacy or seed-level variance'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
