"""Printed-context audit of light and yield statements across 2024 main and supplement."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib, json, re, subprocess
root=Path(__file__).resolve().parents[1]
pdf=root/'data/sources/PMC10978600_DataSheet_1.pdf'
xml=root/'data/sources/pmc10978600.xml'
text=subprocess.check_output(['pdftotext','-f','17','-l','17','-layout',str(pdf),'-'],text=True)
assert 'Supplementary Table 3. Environmental parameters' in text
m=re.search(r'Light / Dark period\s+(\d+)h / (\d+)h\s+(\d+)h / (\d+)h',text)
n=re.search(r'Light intensity\s+(\d+)\s*[–-]\s*(\d+)µmol/m2/s\s+(\d+)\s*[–-]\s*(\d+)µmol/m2/s',text)
assert m and n
hours=list(map(int,m.groups())); levels=list(map(int,n.groups()))
assert hours==[16,8,12,12] and levels==[400,500,600,700]
soup=BeautifulSoup(xml.read_bytes(),'xml')
paragraphs=[p.get_text(' ',strip=True).replace('\xa0',' ') for p in soup.find_all('p')]
yield_p=next(p for p in paragraphs if 'equal to or greater than 588.5' in p)
compare_p=next(p for p in paragraphs if 'average 500 g/m' in p and '600–700' in p)
assert 'three consecutive cultivation' in yield_p and 'six randomly selected plants' in yield_p
assert '51A line' in compare_p and 'metal halide lamp' in compare_p and 'data not shown' in compare_p
out={
 'sources':{'main_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC10978600/',
            'supplement_url':'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10978600/supplementaryFiles',
            'main_sha256':hashlib.sha256(xml.read_bytes()).hexdigest(),
            'supplement_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
            'supplement_pdf_page':17},
 'checks':{'seedling_stage':{'light_hours':hours[0], 'dark_hours':hours[1], 'intensity_umol_m2_s':levels[:2]},
           'cultivation_stage':{'light_hours':hours[2], 'dark_hours':hours[3], 'intensity_umol_m2_s':levels[2:]},
           'same_light_range_printed_for_51A_comparator':levels[2:]==[600,700],
           'minimum_reported_19A_yield_g_m2':588.5,
           'reported_51A_historical_mean_g_m2':500,
           'descriptive_floor_over_historical_mean_percent':round((588.5/500-1)*100,1),
           'high_light_sunlight_yield_data_shown':False,
           'authors_high_light_claim_context':'>1000 g/m2 at 1400 umol/m2/s; data not shown'},
 'finding':'The printed same-light comparison concerns the 19A cultivation stage, not the 400-500 seedling stage. The 19A three-round reported floor exceeds the cited 51A historical mean by 17.7% arithmetically; this is not a matched experiment or a statistical win. The >1000 high-light statement is explicitly data not shown.',
 'limits':['51A and 19A numbers come from distinct reported settings, with metal-halide versus LED lighting; do not treat the ratio as a controlled comparator.',
           'The underlying six-plant values per round and high-light data are not provided in these passages; variability and significance cannot be recalculated.',
           'Source-context QC only, not an independent trial, new discovery, production protocol, or clinical finding.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
