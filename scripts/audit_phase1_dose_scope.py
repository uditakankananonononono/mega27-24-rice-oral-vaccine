"""Classify published human-trial dose evidence without extrapolating from seed lots."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/mucorice_phase1_pubmed_abstract.xml'
s=BeautifulSoup(p.read_bytes(),'xml')
assert s.find('PMID').get_text(strip=True)=='35544149'
a=s.find('Abstract')
parts={x.get('Label','').lower():x.get_text(' ',strip=True) for x in a.find_all('AbstractText')}
methods=parts['methods'];findings=parts['findings']
for marker in ['1 g, 3 g, or 6 g','once every 2 weeks for 8 weeks','total of 4 doses','Three dose cohorts']:
 assert marker in methods,marker
for marker in ['60 male volunteers','10 participants assigned to 1 g','10 participants assigned to 3 g','10 participants assigned to 6 g','Two participants given MucoRice-CTB 3 g','one participant given MucoRice-CTB 6 g']:
 assert marker in findings,marker
out={'source_url':'https://pubmed.ncbi.nlm.nih.gov/35544149/',
     'efetch_url':'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=35544149&rettype=abstract&retmode=xml',
     'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
     'reported_design':{'phase':1,'trial_center_count':1,'dose_cohorts_g_rice_powder':[1,3,6],
                        'allocated_vaccine_per_cohort':10,'allocated_placebo_per_cohort':10,'total_allocated':60,
                        'administered_doses_planned_per_person':4,'vaccine_follow_up_losses':{'3g':2,'6g':1}},
     'allocation_replay':{'vaccine_allocated':30,'placebo_allocated':30,'vaccine_with_followup_if_losses_only':27},
     'classification':{'dose_mass_basis':'grams of administered rice product','seed_lot_antigen_mass_per_trial_dose_in_abstract':False,
                       'individual_lot_antigen_concentrations_in_abstract':False,
                       'matched_digestion_fraction_in_abstract':False},
     'finding':'The trial abstract documents randomized rice-product gram doses and participant allocation, not individually measured seed-lot antigen mass or post-digestion delivery. Therefore multiplying earlier 2021/2024 mean CTB concentration by trial grams would produce an illustrative cross-study estimate, not a verified trial dose.',
     'limits':['PubMed abstract only; full trial methods, lot certificates and supplements not audited',
               'Vaccine arm follow-up count is simple subtraction, not an independently audited efficacy-analysis population',
               'Cannot infer clinical protection, cross-study lot equivalence, calibrated delivered antigen or a benchmark win'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
