"""Scope an independent US trial abstract against Japanese phase 1 full text."""
from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parents[1]
u=R/'data/sources/mucorice_us_phase1_pubmed_35484039.medline.txt'
j=R/'data/sources/mucorice_phase1_lancet_fulltext.md'
text=u.read_text();japan=j.read_text()
assert text.lstrip().startswith('PMID- 35484039')
assert '10.1016/j.vaccine.2022.04.051 [doi]' in text
assert 'double-blind, randomized, placebo-controlled, phase I study conducted' in text
assert 'in the USA' in text and '6-g dose of MucoRice-CTB' in text
assert 'saliva of two of the nine treated subjects' in text
assert 'three of the five responders to the vaccine prevented CTB from' in text
assert 'healthy men and women' in text
assert 'healthy Japanese male volunteers aged 20–40 years' in japan
assert '10 participants assigned to 6 g × 4' in japan
out={'us_pubmed_url':'https://pubmed.ncbi.nlm.nih.gov/35484039/',
     'us_pubmed_efetch_url':'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=35484039&rettype=medline&retmode=text',
     'us_abstract_sha256':hashlib.sha256(u.read_bytes()).hexdigest(),
     'japan_fulltext_url':'https://www.thelancet.com/journals/lanmic/article/PIIS2666-5247%2820%2930196-8/fulltext',
     'japan_fulltext_sha256':hashlib.sha256(j.read_bytes()).hexdigest(),
     'us_trial':{'design':'double-blind randomized placebo-controlled phase I in USA',
                 'dose_g':6,'includes_men_and_women':True,
                 'saliva_iga_response':'2 of 9 treated subjects (as abstract states)',
                 'gm1_binding_inhibition':'3 of 5 responders (as abstract states)'},
     'japan_trial':{'design':'double-blind randomized placebo-controlled phase I in Japan',
                    'dose_g_in_6g_cohort':6,'six_g_treated_assigned':10,'healthy_men_only':True},
     'finding':'A separate published US randomized trial tested the 6-g rice-product dose in men and women; its abstract reports salivary CTB-specific IgA in 2/9 treated participants and GM1 inhibition in 3/5 responders. This adds external clinical context, not a head-to-head or data-level replication.',
     'limits':['Two separate trials and selected abstract endpoints cannot be pooled as matched participant-level data or used for a fair strongest-comparator win.',
               'The US abstract gives no CTB milligram content, 6-g cohort denominator matching rule, individual endpoint values or participant-level safety record.',
               'The 2/9 salivary result is not directly comparable with the Japanese trial faecal IgA measurement or its technical sampling limitations.',
               'The US article full text was not fetched and its abstract is not an accession payload; no gate credit.'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
