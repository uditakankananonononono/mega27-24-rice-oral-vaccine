"""Prevent a similarly titled prior MucoRice trial record from being conflated."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib,json
R=Path(__file__).resolve().parents[1]
sources={'older':R/'data/sources/umin000009688_other_mucorice_trial.html',
         'published_phase1':R/'data/sources/umin000018001_phase1_registry.html'}
def parse(path):
 s=BeautifulSoup(path.read_text(),'html.parser')
 d={}
 for node in s.find_all(['h2','h3']):
  val=node.find_next_sibling()
  if val:d[node.get_text(' ',strip=True)]=val.get_text(' ',strip=True)
 return s.get_text(' ',strip=True),d
old,orow=parse(sources['older']);trial,trow=parse(sources['published_phase1'])
assert 'UMIN000009688 Receipt number R000011211' in old
assert 'UMIN000018001 Receipt number R000020832' in trial
assert '750mg containing 1mg of CTB' in orow['Interventions/Control_1']
assert orow['Target sample size']=='20'
assert 'Cohort 1 1 g' in trow['Interventions/Control_1'] and 'Cohort 3 6 g' in trow['Interventions/Control_1']
assert trow['Target sample size']=='60'
assert 'UMIN000018001' in (R/'data/sources/mucorice_phase1_lancet_fulltext.md').read_text()
out={'registries':[
 {'url':'https://upload.umin.ac.jp/cgi-open-bin/ctr_e/ctr_view.cgi?recptno=R000011211',
  'archive_sha256':hashlib.sha256(sources['older'].read_bytes()).hexdigest(),
  'umin_id':'UMIN000009688','receipt':'R000011211', 'target_n':20,
  'intervention_summary':'single-blind translation record, 750 mg rice containing 1 mg CTB versus wild-type rice'},
 {'url':'https://center6.umin.ac.jp/cgi-open-bin/ctr_e/ctr_view.cgi?recptno=R000020832',
  'archive_sha256':hashlib.sha256(sources['published_phase1'].read_bytes()).hexdigest(),
  'umin_id':'UMIN000018001','receipt':'R000020832','target_n':60,
  'intervention_summary':'sequential randomized three cohorts, 1/3/6 g rice product, each cohort 10 treated and 10 placebo'}],
 'published_trial_url':'https://www.thelancet.com/journals/lanmic/article/PIIS2666-5247%2820%2930196-8/fulltext',
 'finding':'The 20-participant 750-mg/1-mg UMIN000009688 registry is a similarly titled but distinct earlier MucoRice protocol; the published 60-participant 1/3/6-g phase I trial names UMIN000018001, which maps to receipt R000020832. Do not use one registry to fill source gaps in the other.',
 'limits':['Both registry pages list results publication as Unpublished; that field is stale or unmaintained for UMIN000018001 given its observed Lancet publication, and cannot override the article.',
           'Registry interventions state rice product grams but do not state CTB mass for the published trial cohorts; use the published full text for its reported mass pairing.',
           'No individual trial data, clinical efficacy conclusion, accession payload or project gate credit.'],
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}}
print(json.dumps(out,indent=2,sort_keys=True))
