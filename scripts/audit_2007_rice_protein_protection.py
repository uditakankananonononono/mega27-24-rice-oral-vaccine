"""Replay bounded published 2007 antigen-protection comparator; no sequence design."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'data/sources/pmc1904174.html'
s=BeautifulSoup(p.read_text(),'html.parser')
paras=[x.get_text(' ',strip=True) for x in s.find_all('p')]
def paragraph(needle):
    found=[x for x in paras if needle in x]
    assert len(found)==1,(needle,len(found))
    return found[0]
def caption(id):
    fig=s.find('figure',id=id)
    assert fig is not None,id
    return fig.get_text(' ',strip=True)
methods=paragraph('Seed powder (10 mg containing 15 μg of CTB)')
dose=paragraph('A low dose of rice-expressed CTB (e.g., 50 mg of rice powder containing 75 μg CTB)')
stability=paragraph('rice-based mucosal vaccine was preserved for 0.5, 1.0, or 1.5 years')
f2=caption('F2');f4=caption('F4')
assert '≈75% of rice-based CTB but not purified rCTB remained intact' in f2
assert 'not changed compared to that in freshly harvested rice (29 ± 4 μg per seed)' in f4
assert '0.5 mg/ml pepsin' in methods and 'pH 1.7' in methods and '1 h at 37°C' in methods
assert 'same contents of purified rCTB induced no or low levels' in dose
out={'source_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC1904174/',
     'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
     'pepsin_methods_quote':methods,'figure_2_caption_quote':f2,
     'oral_dose_comparator_quote':dose,'storage_paragraph_quote':stability,
     'figure_4_caption_quote':f4,
     'pepsin_initial_ctb_ug':15,'pepsin_seed_powder_mg':10,
     'oral_nominal_ctb_ug':75,'oral_seed_powder_mg':50,
     'implied_reported_ctb_ug_per_mg_powder_in_both_2007_contexts':15/10,
     'reported_in_vitro_rice_ctb_remaining_approx_percent':75,
     'reported_storage_temperature_c':25,'reported_storage_duration_years':1.5,
     'interpretation':'The authors report an equal nominal CTB oral-dose contrast against purified recombinant CTB with greater rice-group fecal IgA, an in vitro pepsin contrast (~75% rice CTB remaining versus no reported intact purified rCTB), and storage stability at 25 C for 1.5 years. This is a published positive comparator, not a new independent benchmark or discovery.',
     'limits':['Figure 2 ~75% is a graphical/author approximate endpoint, not raw replicate-level data or a human delivered-dose estimate.',
               'Figure 4 reports unchanged CTB content and comparable mouse fecal IgA, not a newly estimated equivalence margin or patient efficacy.',
               'This 2007 research line cannot be equated to later 19A or 51A production lines or pooled across them.',
               'No independently fetched accession dataset, genuine new discovery, same-task strongest-comparator win or paper-page gate credit.'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
