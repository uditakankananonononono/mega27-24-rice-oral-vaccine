"""Identity and coverage audit only; no vaccine design or efficacy inference."""
from pathlib import Path
import csv, hashlib, json
ROOT = Path(__file__).resolve().parents[1]
base = ROOT/'data/sources'
maf = base/'MTBLS437_maf.tsv'
samples = base/'MTBLS437_samples.tsv'
run = base/'DRP010027_ena_runs.tsv'
with maf.open(newline='') as f:
    m = list(csv.DictReader(f, delimiter='\t'))
with samples.open(newline='') as f:
    s = list(csv.DictReader(f, delimiter='\t'))
with run.open(newline='') as f:
    r = list(csv.DictReader(f, delimiter='\t'))
replicate_cols = [key for key in m[0] if key.startswith(('MR-CTB51A_replicate', 'NPB-HP_replicate', 'NPB-PF_replicate', 'MR-RNAi_replicate'))]
sample_names = [row['Sample Name'] for row in s]
assert len(replicate_cols)==18 and len(sample_names)==18 and set(replicate_cols)==set(sample_names)
assert len(r)==1 and r[0]['run_accession']=='DRR376734'
valid = lambda v: v.strip() not in ('', 'NA', 'N/A', 'null', 'not reported')
counts={col:sum(valid(row[col]) for row in m) for col in replicate_cols}
identifications = sum(valid(row['metabolite_identification']) and row['metabolite_identification'].lower()!='unknown' for row in m)
result={
 'accessions': ['MTBLS437','DRP010027'],
 'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (maf,samples,run)},
 'metabolights_metabolite_rows':len(m),
 'sample_rows':len(s),
 'abundance_column_count':len(replicate_cols),
 'sample_names_match_abundance_columns':set(replicate_cols)==set(sample_names),
 'nonblank_abundance_cells_by_sample':counts,
 'non_unknown_metabolite_name_rows':identifications,
 'ena_run_metadata':r,
 'limits':'Coverage and source identity only. MTBLS437 metabolite features are not independently accessioned datasets. DRP010027 is metadata only, no raw genomic reads fetched; its line 19A is not the 51A seed-bank comparison. No efficacy, novelty, or causal inference.',
 'gate_credit':{'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}
}
print(json.dumps(result,indent=2,sort_keys=True))
