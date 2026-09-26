import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_audit_matches_archived_sources():
    actual=json.loads(subprocess.check_output([sys.executable,str(ROOT/'scripts/audit_metabolights_source.py')],text=True))
    expected=json.loads((ROOT/'results/metabolights_source_audit.json').read_text())
    assert actual==expected
    assert actual['sample_names_match_abundance_columns']
    assert actual['gate_credit']=={'external_services':0,'fetched_and_used_accession_datasets':0,'audited_derivations':0,'paper_pages':0}
