"""Typed source-provenance guard for published CTB dose arithmetic."""
from pathlib import Path
import json,math
R=Path(__file__).resolve().parents[1]
SOURCES={
 '2007_rice_mouse':{'study':'2007_pnas','line':'early_rice','material':'seed_powder','cohort':'2007_mouse','stage':'administered','mass_mg':50,'printed_ctb_ug':75,'url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC1904174/'},
 '2024_19a_mouse':{'study':'2024_19a','line':'19A','material':'seed_powder','cohort':'mouse_unlinked_lot','stage':'administered','mass_mg':150,'printed_ctb_ug':740,'url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC10978600/'},
 '2021_trial_1g':{'study':'2021_human_trial','line':'51A','material':'rice_product','cohort':'1g','stage':'administered','mass_mg':1000,'printed_ctb_ug':3000,'url':'https://www.thelancet.com/journals/lanmic/article/PIIS2666-5247%2820%2930196-8/fulltext'},
 '2021_trial_3g':{'study':'2021_human_trial','line':'51A','material':'rice_product','cohort':'3g','stage':'administered','mass_mg':3000,'printed_ctb_ug':6000,'url':'https://www.thelancet.com/journals/lanmic/article/PIIS2666-5247%2820%2930196-8/fulltext'},
 '2021_trial_6g':{'study':'2021_human_trial','line':'51A','material':'rice_product','cohort':'6g','stage':'administered','mass_mg':6000,'printed_ctb_ug':18000,'url':'https://www.thelancet.com/journals/lanmic/article/PIIS2666-5247%2820%2930196-8/fulltext'},
 '2007_rice':{'study':'2007_pnas','line':'early_rice','material':'seed_powder','cohort':'2007_mouse','stage':'administered','ug_per_mg':1.5,'kind':'same_source_printed_ratio'},
 '2024_19a_mean':{'study':'2024_19a','line':'19A','material':'seed_powder','cohort':'three_lot_mean_unlinked_to_mouse','stage':'bulk_lot_assay','ug_per_mg':4.94,'kind':'published_three_lot_mean'},
 '2021_51a_msb':{'study':'2021_seed_bank','line':'51A','material':'seed_weight','cohort':'MSB','stage':'seedbank_assay','ug_per_mg':6.45,'kind':'published_msb_mean'}}
def assess(case):
 d=SOURCES[case['dose']];c=SOURCES[case['concentration']] if case['concentration'] else None
 ret={'case_id':case['id'],'reported_nominal_ctb_ug':d['printed_ctb_ug'],'dose_source':d['url'],
      'intestinal_surviving_ctb_ug':None,'individual_measured_ctb_ug':None}
 if c is None:ret['status']='source_printed_only';ret['computed_ctb_ug']=None
 elif any(c[key]!=d[key] for key in ['study','line','material']):
  ret['status']='blocked_cross_context';ret['computed_ctb_ug']=None
 elif c['cohort']!=d['cohort'] or c['stage']!=d['stage']:
  ret['status']='blocked_unknown_lot';ret['computed_ctb_ug']=None
 else:
  ret['status']='permitted';ret['computed_ctb_ug']=d['mass_mg']*c['ug_per_mg']
 return ret
def main():
 refs=json.loads((R/'data/dose_reference_cases.json').read_text())
 out=[]
 for x in refs:
  r=assess(x);assert r['status']==x['expected'];out.append(r)
 naive=[SOURCES[x['dose']]['mass_mg']*SOURCES[x['concentration']]['ug_per_mg'] if x['concentration'] else None for x in refs]
 assert all(v is None or math.isfinite(v) for v in naive)
 print(json.dumps({'source_basis':['results/2007_rice_protein_protection.json','results/19a_mouse_dose_scope.json','results/phase1_fulltext_content.json','results/reconciled_published_ctb_summaries.json'],
  'cases':out,'naive_multiply_any_concentration_ug':naive,
  'permitted_computations':sum(y['status']=='permitted' for y in out),
  'blocked_cross_context':sum(y['status']=='blocked_cross_context' for y in out),
  'blocked_unknown_lot':sum(y['status']=='blocked_unknown_lot' for y in out),
  'limits':['Reference cases and source rules are constructed after source inspection; this regression test is not an untouched benchmark or validated new algorithm.',
            'The three-lot mean may be numerically close to the 2024 mouse printed ratio, but unknown lot identity blocks a claim of measured individual exposure.',
            'No published in-vitro survival fraction is transported to a human intestinal-delivered dose.',
            'Source printed nominal CTB content remains visible even when cross-source calculations are blocked.'],
  'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}},indent=2,sort_keys=True))
if __name__=='__main__':main()
