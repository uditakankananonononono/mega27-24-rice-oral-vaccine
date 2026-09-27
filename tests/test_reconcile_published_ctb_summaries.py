import json
import math
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def test_replay_from_archived_primary_sources():
    actual = json.loads(subprocess.check_output([sys.executable, str(ROOT / 'scripts/reconcile_published_ctb_summaries.py')], text=True))
    assert actual == json.loads((ROOT / 'results/reconciled_published_ctb_summaries.json').read_text())
    a = actual['descriptive_arithmetic']
    assert math.isclose(a['2021_NSB_over_MSB'], 5.83 / 6.45)
    assert math.isclose(a['between_publications_2024_51A_minus_2021_MSB_ug_per_mg'], 0.07)
    assert actual['gate_credit']['audited_derivations'] == 0
    assert len(actual['evidence']) == 2
