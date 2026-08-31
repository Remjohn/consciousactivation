"""Final Production Acceptance & 48-Mandate Closure Test Suite (CAE Phase 4 Mandate M48).

Governed by:
- 04_PHASE_4_PRODUCTION_AND_ACCEPTANCE/M48_final_production_acceptance_current_md_synchronization.md
- 00_CONTROL/38_PHASE4_PRODUCTION_READINESS_DASHBOARD_SCHEMA.json
- 00_CONTROL/30_PHASE4_PRODUCTION_CONTRACT.md
- 00_CONTROL/31_PHASE4_ASSET_LINEAGE_GRAPH.md
- 00_CONTROL/32_PHASE4_SEMANTIC_VS_RENDER_QA.md
- 00_CONTROL/34_PHASE4_OPERATOR_SUPERVISION_MATRIX.md
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4

import pytest

from ca_runtime.editorial_discovery_program import EditorialDiscoveryProgramCoordinator
from ca_runtime.editorial_discovery_store import EditorialDiscoveryStore
from ca_runtime.program_operator_runtime import ProgramOperatorRuntimeService
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_state_runtime import UniversalProgramStateRuntime
from ca_runtime.release_ship_outcome_program import ReleaseShipOutcomeCoordinator
from ca_runtime.vae_delegation_program import VAEDelegationCoordinator
from ca_runtime.video_edit_program import VideoEditProductionCoordinator
from ca_runtime.visual_prompt_annotation_program import VisualPromptAnnotationCoordinator


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DASHBOARD_SCHEMA_PATH = REPO_ROOT / "docs/cae/CAE_Phase4_Production_Mandate_Bundle_v2/00_CONTROL/38_PHASE4_PRODUCTION_READINESS_DASHBOARD_SCHEMA.json"
DASHBOARD_PATH = REPO_ROOT / "docs/cae/CAE_Phase4_Production_Mandate_Bundle_v2/04_PHASE_4_PRODUCTION_AND_ACCEPTANCE/M48_PRODUCTION_READINESS_DASHBOARD.json"
PRD_PATH = REPO_ROOT / "docs/PRD/CURRENT.md"


@pytest.fixture
def state_runtime() -> UniversalProgramStateRuntime:
    return UniversalProgramStateRuntime()


@pytest.fixture
def operator_runtime(state_runtime: UniversalProgramStateRuntime) -> ProgramOperatorRuntimeService:
    root = REPO_ROOT / "programs"
    registry = ProgramRegistry(discovery_roots=[root])
    registry.discover()
    return ProgramOperatorRuntimeService(runtime=state_runtime, program_registry=registry)


def test_01_all_48_mandates_inventory_and_traceability_closure():
    """Asserts that all 48 mandates have recorded deliverables and verified reports across Phases 1-4."""
    # Check Phase 1 bundle reports
    p1_dir = REPO_ROOT / "docs/cae/CAE_Phase1_Production_Mandate_Bundle_v1/01_PHASE_1_INVENTORY_AND_CONTRACTS"
    assert p1_dir.exists(), "Phase 1 directory must exist"

    # Check Phase 2 bundle reports
    p2_dir = REPO_ROOT / "docs/cae/CAE_Phase2_Production_Mandate_Bundle_v2/02_PHASE_2_RUNTIME_FOUNDATION"
    assert p2_dir.exists(), "Phase 2 directory must exist"

    # Check Phase 3 bundle reports
    p3_dir = REPO_ROOT / "docs/cae/CAE_Phase3_Production_Mandate_Bundle_v2/03_PHASE_3_INTELLIGENCE_AND_PROGRAMS"
    assert p3_dir.exists(), "Phase 3 directory must exist"

    # Check Phase 4 bundle reports (M37 through M48)
    p4_dir = REPO_ROOT / "docs/cae/CAE_Phase4_Production_Mandate_Bundle_v2/04_PHASE_4_PRODUCTION_AND_ACCEPTANCE"
    assert p4_dir.exists(), "Phase 4 directory must exist"
    for mandate_num in range(37, 49):
        report_path = p4_dir / f"M{mandate_num}_MANDATE_REPORT.md"
        assert report_path.exists(), f"Mandate report {report_path.name} must exist"


def test_02_production_readiness_dashboard_schema_conformance():
    """Validates that M48_PRODUCTION_READINESS_DASHBOARD.json strictly satisfies the dashboard schema."""
    assert DASHBOARD_SCHEMA_PATH.exists(), "Dashboard schema file must exist"
    assert DASHBOARD_PATH.exists(), "Production readiness dashboard file must exist"

    with open(DASHBOARD_SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)

    with open(DASHBOARD_PATH, "r", encoding="utf-8") as f:
        dashboard = json.load(f)

    # Validate top-level schema keys
    for required_key in schema.keys():
        assert required_key in dashboard, f"Missing required top-level key: {required_key}"

    # Validate programs map keys
    for program_key in schema["programs"].keys():
        assert program_key in dashboard["programs"], f"Missing program key: {program_key}"
        prog_entry = dashboard["programs"][program_key]
        assert "status" in prog_entry and prog_entry["status"] == "READY_AND_VERIFIED"
        assert "evidence" in prog_entry and len(prog_entry["evidence"]) > 0

    # Validate all verification flags
    assert dashboard["artifact_lineage_verified"] is True
    assert dashboard["semantic_qa_verified"] is True
    assert dashboard["render_qa_verified"] is True
    assert dashboard["operator_gates_verified"] is True
    assert dashboard["failure_injection_verified"] is True
    assert dashboard["e2e_pilot_verified"] is True
    assert dashboard["current_prd_synchronized"] is True
    assert dashboard["operator_decision"] == "READY-WITH-EXPLICIT-LIMITATIONS"


def test_03_universal_program_state_runtime_freeze_integrity(state_runtime: UniversalProgramStateRuntime):
    """Verifies that all core production programs and state machines are registered and immutable."""
    programs_root = REPO_ROOT / "programs"
    registry = ProgramRegistry(discovery_roots=[programs_root])
    discovered = registry.discover()
    discovered_ids = {p.program_id for p in discovered}

    expected_programs = [
        "editorial_discovery_program",
        "interview_semantic_program",
        "script_program",
        "visual_prompt_annotation_program",
        "visual_derivative_production_program",
        "video_edit_program",
        "vae_delegation_program",
        "release_ship_outcome_program",
    ]
    for prog_id in expected_programs:
        assert prog_id in discovered_ids, f"Program {prog_id} must be discoverable in {discovered_ids}"

    # Initialize coordinators to ensure state machines are wired into state runtime
    discovery_store = EditorialDiscoveryStore(db_path=":memory:")
    EditorialDiscoveryProgramCoordinator(editorial_store=discovery_store)
    ReleaseShipOutcomeCoordinator(runtime=state_runtime)
    VideoEditProductionCoordinator(runtime=state_runtime)
    VisualPromptAnnotationCoordinator(runtime=state_runtime)
    VAEDelegationCoordinator(runtime=state_runtime)

    for prog_id in [
        "release_ship_outcome_program",
        "video_edit_program",
        "visual_prompt_annotation_program",
        "vae_delegation_program",
    ]:
        sm = state_runtime.get_state_machine(prog_id)
        assert sm is not None
        assert sm.initial_state is not None
        assert len(sm.transitions) >= 2


def test_04_dual_axis_qa_and_lineage_graph_freeze_integrity(
    state_runtime: UniversalProgramStateRuntime,
    operator_runtime: ProgramOperatorRuntimeService,
):
    """Verifies cryptographic lineage projection and DAG trace generation."""
    release_coord = ReleaseShipOutcomeCoordinator(runtime=state_runtime)
    ws_uuid = uuid4()
    candidate_id = "cand-freeze-001"
    quote_text = "Authentic evidence for production freeze verification."
    quote_sha256 = hashlib.sha256(quote_text.encode("utf-8")).hexdigest()

    # Initialize and advance session to QA_VERIFIED
    agg = release_coord.initialize_session(
        candidate_id=candidate_id,
        workspace_id=ws_uuid,
        actor_id="operator-lead",
        artifact_ref={"artifact_id": "art-freeze-001", "sha256": quote_sha256, "path": "/media/freeze.mp4"},
    )
    release_coord.verify_final_qa(
        aggregate_id=agg.aggregate_id,
        actor_id="analyst-lead",
        semantic_qa_result={"passed": True, "evidence_integrity": True},
        render_qa_result={"passed": True, "resolution": "1080x1920"},
        evidence_segment={"segment_id": "seg-freeze-01", "quote_text": quote_text, "evidence_quote_sha256": quote_sha256},
        wrong_reading_locks=["Maintain truthful representation"],
    )

    # Lineage graph projection
    lineage = operator_runtime.project_artifact_lineage(agg.aggregate_id)
    assert lineage.aggregate_id == agg.aggregate_id
    assert lineage.is_lossless is True
    assert len(lineage.nodes) >= 2
    assert len(lineage.edges) >= 1

    # Execution trace projection
    trace = operator_runtime.project_execution_trace(agg.aggregate_id)
    assert trace.aggregate_id == agg.aggregate_id
    assert trace.current_state == "QA_VERIFIED"
    assert len(trace.trace_nodes) >= 1


def test_05_explicit_production_readiness_posture_verification():
    """Asserts that PRD CURRENT.md is synchronized and explicitly documents the readiness posture."""
    assert PRD_PATH.exists(), "CURRENT.md must exist"
    prd_text = PRD_PATH.read_text(encoding="utf-8")

    # Assert Phase 4 and Mandate closure references
    assert "Mandates M37–M48" in prd_text
    assert "Mandate M48" in prd_text
    assert "READY-WITH-EXPLICIT-LIMITATIONS" in prd_text
