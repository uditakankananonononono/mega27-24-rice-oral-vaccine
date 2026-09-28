"""Keep article-reported mouse administrations separate from human trial dose."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/pmc10978600.xml'
s=BeautifulSoup(p.read_text(),'xml')
methods=[x.get_text(' ',strip=True) for x in s.find_all('p') if '150 mg containing 740' in x.get_text(' ',strip=True)]
assert len(methods)==1 and 'four times at 2-week intervals' in methods[0]
fig=[x for x in s.find_all('fig') if x.find('label') and x.find('label').get_text(' ',strip=True).replace('\u00a0',' ')=='Figure 6']
assert len(fig)==1
caption=fig[0].find('caption').get_text(' ',strip=True)
assert 'immunized 5 times at 2-week intervals' in caption
lot=next(x.get_text(' ',strip=True) for x in s.find_all('p') if 'SDS-PAGE densitometric analysis (n=3 lot)' in x.get_text(' ',strip=True))
assert '4.94 ± 0.29 μg/mg in line 19A' in lot
human=(R/'data/sources/mucorice_phase1_lancet_fulltext.md').read_text()
assert '10 participants assigned to 1 g × 4' in human
out={'article_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC10978600/',
     'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
     'mouse_methods_quote':methods[0], 'figure_6_caption_quote':caption,
     'reported_powder_mg':150,'reported_ctb_ug':740,
     'implied_ctb_ug_per_mg_powder':740/150,
     'lot_mean_19a_ctb_ug_per_mg':4.94,
     'implied_minus_lot_mean_ug_per_mg':740/150-4.94,
     'mouse_administration_counts':{'methods':4,'figure_6_caption':5},
     'human_trial_url':'https://www.thelancet.com/journals/lanmic/article/PIIS2666-5247%2820%2930196-8/fulltext',
     'finding':'The printed mouse dose 150 mg powder/740 ug CTB implies 4.933 ug/mg, approximately the 19A three-lot mean 4.94 ug/mg; the mouse methods say four oral administrations whereas Figure 6 caption says five. The source alone does not settle which count was performed.',
     'limits':['Arithmetic consistency of the printed mass pair does not independently assay the lot or verify individual mouse exposure.',
               'Four versus five administrations is a source-text disagreement; do not resolve by guessing or convert it to a biological result.',
               'The human phase I trial has separate participants, line/product context and dose schedule; do not transfer the mouse count or lot mean to human exposure.',
               'No participant-level, comparator, biological discovery or project gate credit.'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
