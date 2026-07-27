from __future__ import annotations
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'CMF_PROGRAM_CONTROL/03_PROGRAM_STATUS/PHASE_05_SEMANTIC_PRODUCTION_COMPILER'

def rows(name):
    with (REPORT/name).open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def test_phase5_traceability_counts_and_scope():
    specs=rows('PHASE_05_SPEC_IMPLEMENTATION_MATRIX.csv');acs=rows('PHASE_05_ACCEPTANCE_TEST_MATRIX.csv')
    assert [x['spec_id'] for x in specs]==['TS-AIR-003','TS-AIR-015','TS-AIR-016']
    assert len(acs)==66
    assert all(x['full_spec_completed']=='false' for x in specs)
    assert sum(int(x['direct_acceptance_test_count']) for x in specs)==25
    assert sum(int(x['implementation_no_direct_test_count']) for x in specs)==30
    assert sum(int(x['deferred_not_implemented_count']) for x in specs)==11

def test_phase5_spec_hashes_and_all_acceptance_ids_resolve():
    specs=rows('PHASE_05_SPEC_IMPLEMENTATION_MATRIX.csv');acs=rows('PHASE_05_ACCEPTANCE_TEST_MATRIX.csv')
    import hashlib
    for spec in specs:
        path=ROOT/spec['spec_path'];assert path.is_file();assert hashlib.sha256(path.read_bytes()).hexdigest()==spec['spec_sha256']
        ids=[x['acceptance_criterion_id'] for x in acs if x['spec_id']==spec['spec_id']]
        assert ids==[f'AC-{i:02d}' for i in range(1,23)]

def test_phase5_claim_ceiling_and_gap_ledger_are_conservative():
    data=json.loads((REPORT/'TRACEABILITY_DATA.json').read_text(encoding='utf-8'))
    assert data['phase']=='PHASE_05_SEMANTIC_PRODUCTION_COMPILER'
    assert all(x['claim_ceiling']=='PHASE_05_SEMANTIC_PRODUCTION_COMPILER_DEVELOPMENT_EVIDENCE' for x in data['acceptance_criteria'])
    assert any(x['status']=='OPEN' for x in data['gaps'])
    assert any(x['status']=='DEFERRED' for x in data['gaps'])
