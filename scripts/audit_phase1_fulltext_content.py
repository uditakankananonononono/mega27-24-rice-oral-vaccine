"""Reconcile human trial's printed content with its administered rice mass."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
p=R/'data/sources/mucorice_phase1_lancet_fulltext.md'
s=p.read_text()
assert 'Oral MucoRice-CTB vaccine for safety and microbiota-dependent immunogenicity in humans' in s
expected=[(1,3),(3,6),(6,18)]
for rice_g,ctb_mg in expected:
    assert f'{rice_g} g of MucoRice-CTB containing {ctb_mg} mg of CTB' in s
rows=[{'rice_product_g':rice_g,'ctb_mg_per_admin_printed':ctb_mg,
       'implied_ctb_mg_per_g_product':round(ctb_mg/rice_g,3)} for rice_g,ctb_mg in expected]
out={'fulltext_url':'https://www.thelancet.com/journals/lanmic/article/PIIS2666-5247%2820%2930196-8/fulltext',
     'fulltext_readable_markdown_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
     'fulltext_publication_doi':'10.1016/S2666-5247(20)30196-8',
     'trial_printed_contents':rows,
     'content_per_g_identical_across_cohorts':len(set(r['implied_ctb_mg_per_g_product'] for r in rows))==1,
     'interpretation':'The full-text methods print a 3, 6 and 18 mg CTB content for 1, 3 and 6 g administered rice product respectively. The implied concentrations are 3, 2 and 3 mg/g, so the printed content does not scale uniformly across the three stated rice masses. This is a source-reported cohort/formulation distinction, not proof of a manufacturing defect or patient exposure.',
     'limits':['The source does not identify lot-level concentration records in this passage; printed cohort contents are not independent per-participant assays',
               'The readable Markdown is the fetched web-page representation, not publisher PDF; source text may differ from PDF typesetting and should be checked before any clinical inference',
               'Do not equate administered content with intestinal surviving dose or clinical efficacy',
               'No underlying trial dataset, comparator, biological discovery or gate credit'],
     'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
