from __future__ import annotations
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/PHASE_06_COMPOSITION_MEDIA_RUNTIME'

def test_phase6_traceability_complete():
    with (REPORT/'PHASE_06_SPEC_IMPLEMENTATION_MATRIX.csv').open(encoding='utf-8', newline='') as handle:
        specs=list(csv.DictReader(handle))
    with (REPORT/'PHASE_06_ACCEPTANCE_TEST_MATRIX.csv').open(encoding='utf-8', newline='') as handle:
        acs=list(csv.DictReader(handle))
    assert len(specs)==13
    assert len(acs)==182
    assert all(row['per_spec_status']=='PARTIALLY_IMPLEMENTED' for row in specs)
    assert all(row['full_spec_completed'].lower()=='false' for row in specs)
    for row in specs:
        assert (ROOT/'05_ATOMIC_HARNESS_PIPELINE/docs/tech-specs'/f"{row['spec_id']}.md").is_file()

def test_phase6_gap_and_claim_boundary():
    data=json.loads((REPORT/'TRACEABILITY_DATA.json').read_text())
    assert data['full_specs_completed']==0
    assert data['direct_criterion_evidence_count']==111
    status=(REPORT/'COMPLETION_RECEIPT.yaml').read_text()
    assert 'PHASE_06_COMPOSITION_MEDIA_RUNTIME_DEVELOPMENT_EVIDENCE' in status
    assert '"production_authorized": false' in status
