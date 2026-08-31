"""
test_interview_semantic_program.py
----------------------------------
Acceptance and Verification Test Suite for CAE Phase 3 M33:
Interview Semantic Program + Existing Composer Boundary.
"""

import sqlite3
import pytest
from datetime import datetime, timezone
from pathlib import Path

from ca_runtime.program_state_runtime import (
    AuthorityLane,
    InMemoryProgramStateStore,
    ProgramRegistry,
    UniversalProgramStateRuntime,
    get_canonical_interview_state_machine,
)
from ca_runtime.interview_semantic_store import (
    InterviewSemanticStore,
    InterviewBriefRecord,
    InterviewSessionRecord,
    InterviewSemanticReceiptRecord,
)
from ca_runtime.interview_semantic_program import (
    InterviewSemanticProgramCoordinator,
    InterviewProgramError,
    UnauthorizedInterviewLaneError,
    WorkspaceScopeViolationError,
    LeadingQuestionViolationError,
    MatrixOfEdgingValidationError,
    BriefCompilationError,
    BriefAuthorizationError,
)
from ca_runtime.collision_hypothesis_store import (
    CollisionHypothesisRecord,
)
from conscious_activations_interview_composer.services.brief_service import BriefService
from conscious_activations_interview_composer.services.research_service import ResearchService
from conscious_activations_interview_composer.repository import InterviewComposerRepository


@pytest.fixture
def programs_root() -> Path:
    return Path("programs").resolve()


@pytest.fixture
def test_setup(programs_root: Path, tmp_path: Path):
    """Sets up an isolated in-memory runtime and stores for interview testing."""
    conn = sqlite3.connect(":memory:")
    store = InterviewSemanticStore(conn)
    state_store = InMemoryProgramStateStore()
    registry = ProgramRegistry(discovery_roots=[programs_root])
    registry.discover()
    runtime = UniversalProgramStateRuntime(store=state_store, program_registry=registry)
    runtime.register_state_machine(get_canonical_interview_state_machine())

    # Isolated composer repository and service
    composer_db = str(tmp_path / "composer.db")
    composer_repo = InterviewComposerRepository(database_path=composer_db)
    composer_repo.initialize()
    research_service = ResearchService(composer_repo)
    brief_service = BriefService(composer_repo)

    return {
        "conn": conn,
        "store": store,
        "state_store": state_store,
        "runtime": runtime,
        "registry": registry,
        "composer_repo": composer_repo,
        "research_service": research_service,
        "brief_service": brief_service,
    }


def _create_approved_hypothesis(workspace_id: str, hyp_id: str = "HYP-AUDREY-01") -> CollisionHypothesisRecord:
    """Helper to create an authentic M32 approved CollisionHypothesisRecord."""
    return CollisionHypothesisRecord(
        workspace_id=workspace_id,
        hypothesis_id=hyp_id,
        title="Decentralized Autonomy Under Pressure",
        relation_type="PARADOX",
        audience_id="AUD-TECH-LEADERS-01",
        audience_tension_ref="Command-and-control instinct during acute crisis vs true team empowerment",
        guest_id="GUEST-AUDREY-01",
        guest_lived_proof_citation="Resolved existential infrastructure crisis in 2021 by delegating root authority to 14 distributed pods without central signoff.",
        research_signal_id="SIG-MACRO-BURNOUT-2024",
        bridge_statement="True leadership control is gained only when central leadership intentionally surrenders tactical veto power during acute crisis.",
        evidence_references=["INCIDENT-POSTMORTEM-2021-08", "TRANSCRIPT-POD-LEADERS-2021"],
        novelty_assessment={
            "novelty_score_micros": 920_000,
            "trope_overlap_micros": 80_000,
            "justification": "Direct paradox confronting conventional executive intuition.",
        },
        falsification_condition={
            "disconfirmed_if": "Delegating veto authority during crisis reliably produces organizational paralysis.",
            "test_boundary": "High-velocity technical outages with existential SLA impact.",
        },
        heritage_eval={
            "heritage_score_micros": 880_000,
            "guest_alignment_micros": 950_000,
        },
        status="APPROVED",
        approval_notes="Approved for full Activative Interview Brief compilation.",
    )


# =============================================================================
# 1. Full E2E Lifecycle: Hypothesis -> Candidate -> Evaluation -> Brief -> Seal
# =============================================================================

def test_interview_semantic_program_full_lifecycle_e2e(test_setup):
    """
    Test 1: Full end-to-end lifecycle across all 4 authority lanes:
    HUNTER (ingest) -> ANALYST (evaluate) -> COMPOSER (compile) -> COMMANDER (seal)
    """
    store: InterviewSemanticStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    brief_service: BriefService = test_setup["brief_service"]
    composer_repo: InterviewComposerRepository = test_setup["composer_repo"]
    ws_id = "ws-interview-prod-01"

    # Seed research package in composer repo via ResearchService
    research_svc: ResearchService = test_setup["research_service"]
    research_pkg_cmd = {
        "workspace_id": ws_id,
        "project_id": "prj-interview-01",
        "guest_name": "Audrey Tang",
        "source_urls": ["https://example.com/audrey-tang-2021"],
        "uploaded_documents": [],
        "composer_authority": {
            "operator_id": "op_commander_01",
            "authority_scope": "production_brief_compiler",
            "assertion_id": "assert_auth_2026_m33",
        },
    }
    pkg_res = research_svc.create_package(
        research_pkg_cmd, idempotency_key="idemp_pkg_audrey_01"
    )
    pkg_obj_id = pkg_res["object"]["object_id"]
    pkg_sha = pkg_res["object"]["sha256"]
    pkg_ver = pkg_res["object"]["version"]

    coord = InterviewSemanticProgramCoordinator(
        workspace_id=ws_id,
        store=store,
        state_runtime=runtime,
    )

    hypothesis = _create_approved_hypothesis(workspace_id=ws_id)
    research_package_ref = {
        "object_id": pkg_obj_id,
        "version": pkg_ver,
        "sha256": pkg_sha,
    }

    # --- 1. HUNTER Lane: Ingest Hypothesis & Derive 4-Stage Questions ---
    candidate, question_program = coord.ingest_approved_hypothesis(
        workspace_id=ws_id,
        hypothesis_record=hypothesis,
        guest_research_package=research_package_ref,
        actor_id="actor_hunter_01",
        lane=AuthorityLane.HUNTER,
    )

    assert candidate.candidate_id == f"hc:{hypothesis.hypothesis_id}"
    assert candidate.collision_statement == hypothesis.bridge_statement
    assert len(question_program.candidate_questions) == 4

    # Verify 4 progression resolutions
    resolutions = [q.target_resolution.value for q in question_program.candidate_questions]
    assert resolutions == ["episodic", "mechanistic", "evidential", "mechanistic"]

    # --- 2. ANALYST Lane: Adversarially Evaluate Matrix & Non-Scripting ---
    eval_res = coord.evaluate_elicitation_matrix(
        workspace_id=ws_id,
        candidate=candidate,
        question_program=question_program,
        target_archetype="F01_CINEMATIC_STORY",
        actor_id="actor_analyst_01",
        lane=AuthorityLane.ANALYST,
    )

    assert eval_res.matrix_valid is True
    assert eval_res.non_scripted_valid is True
    assert eval_res.archetype_compatibility_score_micros == 1_000_000
    assert eval_res.evaluated_questions_count == 4

    # --- 3. COMPOSER Lane: Compile Canonical ActivativeInterviewBrief ---
    composer_auth = {
        "operator_id": "op_commander_01",
        "authority_scope": "production_brief_compiler",
        "assertion_id": "assert_auth_2026_m33",
    }
    compiled_brief, canonical_sha = coord.compile_interview_brief(
        workspace_id=ws_id,
        candidate=candidate,
        question_program=question_program,
        guest_name="Audrey Tang",
        research_package_ref=research_package_ref,
        composer_authority=composer_auth,
        actor_id="actor_composer_01",
        lane=AuthorityLane.COMPOSER,
    )

    assert "payload_json" in compiled_brief or "planned_questions" in compiled_brief
    assert len(canonical_sha) == 64

    # --- 4. COMMANDER Lane: Authorize & Seal Brief ---
    brief_record, receipt = coord.seal_interview_brief(
        workspace_id=ws_id,
        compiled_brief=compiled_brief,
        idempotency_key="idemp_seal_brief_audrey_01",
        brief_service=brief_service,
        actor_id="actor_commander_01",
        lane=AuthorityLane.COMMANDER,
    )

    assert brief_record.workspace_id == ws_id
    assert brief_record.lifecycle_state == "SEALED"
    assert brief_record.canonical_sha256 == canonical_sha
    assert len(brief_record.planned_questions) == 4
    assert receipt.decision == "SEALED"
    assert receipt.signature is not None

    # Verify persistence in InterviewSemanticStore
    stored_brief = store.get_brief(workspace_id=ws_id, brief_id=brief_record.brief_id)
    assert stored_brief is not None
    assert stored_brief.guest_name == "Audrey Tang"
    assert stored_brief.hypothesis_id == hypothesis.hypothesis_id

    stored_receipt = store.get_receipt(workspace_id=ws_id, receipt_id=receipt.receipt_id)
    assert stored_receipt is not None
    assert stored_receipt.brief_id == brief_record.brief_id

    # Verify State Machine Aggregation
    agg = runtime.get_aggregate(coord._aggregate_id)
    assert agg.current_state == "BRIEF_SEALED"
    assert agg.version == 5  # Initialized (v1) + 4 transitions (v2, v3, v4, v5)
    assert agg.state_data["brief_sealed"] is True


# =============================================================================
# 2. Strict Authority Lane Governance (Fail-Closed)
# =============================================================================

def test_interview_semantic_program_four_lane_governance(test_setup):
    """Test 2: Verifies fail-closed enforcement when incorrect authority lane executes operations."""
    store: InterviewSemanticStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    ws_id = "ws-interview-governance"

    coord = InterviewSemanticProgramCoordinator(
        workspace_id=ws_id,
        store=store,
        state_runtime=runtime,
    )
    hypothesis = _create_approved_hypothesis(workspace_id=ws_id)
    research_ref = {"object_id": "pkg_1", "version": "1.0.0", "sha256": "a" * 64}

    # 1. Ingest with ANALYST lane -> must fail
    with pytest.raises(UnauthorizedInterviewLaneError) as exc_info:
        coord.ingest_approved_hypothesis(
            workspace_id=ws_id,
            hypothesis_record=hypothesis,
            guest_research_package=research_ref,
            lane=AuthorityLane.ANALYST,
        )
    assert "requires HUNTER lane" in str(exc_info.value)

    # Ingest legitimately with HUNTER
    candidate, q_prog = coord.ingest_approved_hypothesis(
        workspace_id=ws_id,
        hypothesis_record=hypothesis,
        guest_research_package=research_ref,
        lane=AuthorityLane.HUNTER,
    )

    # 2. Evaluate with COMPOSER lane -> must fail
    with pytest.raises(UnauthorizedInterviewLaneError) as exc_info:
        coord.evaluate_elicitation_matrix(
            workspace_id=ws_id,
            candidate=candidate,
            question_program=q_prog,
            lane=AuthorityLane.COMPOSER,
        )
    assert "requires ANALYST lane" in str(exc_info.value)

    # Evaluate legitimately with ANALYST
    coord.evaluate_elicitation_matrix(
        workspace_id=ws_id,
        candidate=candidate,
        question_program=q_prog,
        lane=AuthorityLane.ANALYST,
    )

    # 3. Compile with HUNTER lane -> must fail
    composer_auth = {"operator_id": "op_1", "authority_scope": "brief", "assertion_id": "ass_1"}
    with pytest.raises(UnauthorizedInterviewLaneError) as exc_info:
        coord.compile_interview_brief(
            workspace_id=ws_id,
            candidate=candidate,
            question_program=q_prog,
            guest_name="Guest",
            research_package_ref=research_ref,
            composer_authority=composer_auth,
            lane=AuthorityLane.HUNTER,
        )
    assert "requires COMPOSER lane" in str(exc_info.value)

    # Compile legitimately with COMPOSER
    compiled_brief, _ = coord.compile_interview_brief(
        workspace_id=ws_id,
        candidate=candidate,
        question_program=q_prog,
        guest_name="Guest",
        research_package_ref=research_ref,
        composer_authority=composer_auth,
        lane=AuthorityLane.COMPOSER,
    )

    # 4. Seal with ANALYST lane -> must fail
    with pytest.raises(UnauthorizedInterviewLaneError) as exc_info:
        coord.seal_interview_brief(
            workspace_id=ws_id,
            compiled_brief=compiled_brief,
            idempotency_key="idemp_gov_01",
            lane=AuthorityLane.ANALYST,
        )
    assert "requires COMMANDER lane" in str(exc_info.value)


# =============================================================================
# 3. Non-Scripted / Anti-Leading Question Rejection
# =============================================================================

def test_interview_semantic_program_anti_scripting_rejection(test_setup):
    """Test 3: Injects leading and scripted questions and verifies strict ANALYST rejection."""
    store: InterviewSemanticStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    ws_id = "ws-interview-scripting"

    coord = InterviewSemanticProgramCoordinator(
        workspace_id=ws_id,
        store=store,
        state_runtime=runtime,
    )
    hypothesis = _create_approved_hypothesis(workspace_id=ws_id)
    research_ref = {"object_id": "pkg_1", "version": "1.0.0", "sha256": "a" * 64}

    candidate, q_prog = coord.ingest_approved_hypothesis(
        workspace_id=ws_id,
        hypothesis_record=hypothesis,
        guest_research_package=research_ref,
        lane=AuthorityLane.HUNTER,
    )

    # Inject a forbidden leading question
    q_prog.candidate_questions[0].text = "Don't you agree that centralized management always fails during crises?"

    with pytest.raises(LeadingQuestionViolationError) as exc_info:
        coord.evaluate_elicitation_matrix(
            workspace_id=ws_id,
            candidate=candidate,
            question_program=q_prog,
            lane=AuthorityLane.ANALYST,
        )
    assert "failed non-scripted invariant" in str(exc_info.value)


# =============================================================================
# 4. Matrix of Edging Parameter & Pressure Path Validation
# =============================================================================

def test_interview_semantic_program_matrix_of_edging_validation(test_setup):
    """Test 4: Verifies rejection of incomplete or malformed Matrix of Edging seeds."""
    store: InterviewSemanticStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    ws_id = "ws-interview-matrix"

    coord = InterviewSemanticProgramCoordinator(
        workspace_id=ws_id,
        store=store,
        state_runtime=runtime,
    )
    hypothesis = _create_approved_hypothesis(workspace_id=ws_id)
    research_ref = {"object_id": "pkg_1", "version": "1.0.0", "sha256": "a" * 64}

    candidate, q_prog = coord.ingest_approved_hypothesis(
        workspace_id=ws_id,
        hypothesis_record=hypothesis,
        guest_research_package=research_ref,
        lane=AuthorityLane.HUNTER,
    )

    # Pass an override that blanks a mandatory field
    invalid_matrix_seed = {"pressure_path": ""}

    with pytest.raises(MatrixOfEdgingValidationError) as exc_info:
        coord.evaluate_elicitation_matrix(
            workspace_id=ws_id,
            candidate=candidate,
            question_program=q_prog,
            matrix_seed_overrides=invalid_matrix_seed,
            lane=AuthorityLane.ANALYST,
        )
    assert "missing mandatory fields" in str(exc_info.value)


# =============================================================================
# 5. Multi-Tenant Workspace Isolation
# =============================================================================

def test_interview_semantic_program_workspace_isolation(test_setup):
    """Test 5: Cross-workspace hypothesis ingestion and operation execution must fail."""
    store: InterviewSemanticStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    ws_id = "ws-tenant-alpha"
    foreign_ws_id = "ws-tenant-beta"

    coord = InterviewSemanticProgramCoordinator(
        workspace_id=ws_id,
        store=store,
        state_runtime=runtime,
    )

    # Hypothesis belongs to foreign workspace
    foreign_hypothesis = _create_approved_hypothesis(workspace_id=foreign_ws_id)
    research_ref = {"object_id": "pkg_1", "version": "1.0.0", "sha256": "a" * 64}

    with pytest.raises(WorkspaceScopeViolationError) as exc_info:
        coord.ingest_approved_hypothesis(
            workspace_id=ws_id,
            hypothesis_record=foreign_hypothesis,
            guest_research_package=research_ref,
            lane=AuthorityLane.HUNTER,
        )
    assert "belongs to workspace" in str(exc_info.value)


# =============================================================================
# 6. Missing Operator Authority Sealing Rejection
# =============================================================================

def test_interview_semantic_program_missing_operator_authority(test_setup):
    """Test 6: Verifies that sealing without valid operator authority assertions fails closed."""
    store: InterviewSemanticStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    ws_id = "ws-interview-auth"

    coord = InterviewSemanticProgramCoordinator(
        workspace_id=ws_id,
        store=store,
        state_runtime=runtime,
    )
    hypothesis = _create_approved_hypothesis(workspace_id=ws_id)
    research_ref = {"object_id": "pkg_1", "version": "1.0.0", "sha256": "a" * 64}

    candidate, q_prog = coord.ingest_approved_hypothesis(
        workspace_id=ws_id,
        hypothesis_record=hypothesis,
        guest_research_package=research_ref,
        lane=AuthorityLane.HUNTER,
    )
    coord.evaluate_elicitation_matrix(
        workspace_id=ws_id,
        candidate=candidate,
        question_program=q_prog,
        lane=AuthorityLane.ANALYST,
    )

    # Incomplete authority
    invalid_auth = {"operator_id": "op_1"}  # Missing authority_scope and assertion_id

    with pytest.raises(BriefCompilationError) as exc_info:
        coord.compile_interview_brief(
            workspace_id=ws_id,
            candidate=candidate,
            question_program=q_prog,
            guest_name="Guest",
            research_package_ref=research_ref,
            composer_authority=invalid_auth,
            lane=AuthorityLane.COMPOSER,
        )
    assert "Missing required composer authority" in str(exc_info.value)


# =============================================================================
# 7. Downstream Content Archetype Compatibility Gate
# =============================================================================

def test_interview_semantic_program_archetype_compatibility(test_setup):
    """Test 7: Verifies archetype compatibility evaluation across Formats 01, 02, and 03."""
    store: InterviewSemanticStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]

    for fmt in ["F01_CINEMATIC_STORY", "F02_MINIMAL_COACH", "F03_PROOF_COMMENTARY"]:
        ws_id = f"ws-interview-archetype-{fmt.lower()}"
        coord = InterviewSemanticProgramCoordinator(
            workspace_id=ws_id,
            store=store,
            state_runtime=runtime,
        )
        hypothesis = _create_approved_hypothesis(workspace_id=ws_id)
        research_ref = {"object_id": "pkg_1", "version": "1.0.0", "sha256": "a" * 64}

        candidate, q_prog = coord.ingest_approved_hypothesis(
            workspace_id=ws_id,
            hypothesis_record=hypothesis,
            guest_research_package=research_ref,
            lane=AuthorityLane.HUNTER,
        )

        res = coord.evaluate_elicitation_matrix(
            workspace_id=ws_id,
            candidate=candidate,
            question_program=q_prog,
            target_archetype=fmt,
            lane=AuthorityLane.ANALYST,
        )
        assert res.archetype_compatibility_score_micros == 1_000_000


# =============================================================================
# 8. Commander Repair and Quarantine Handling
# =============================================================================

def test_interview_semantic_program_repair_lifecycle(test_setup):
    """Test 8: Verifies Commander fail-closed repair transitions."""
    store: InterviewSemanticStore = test_setup["store"]
    runtime: UniversalProgramStateRuntime = test_setup["runtime"]
    ws_id = "ws-interview-repair"

    coord = InterviewSemanticProgramCoordinator(
        workspace_id=ws_id,
        store=store,
        state_runtime=runtime,
    )
    hypothesis = _create_approved_hypothesis(workspace_id=ws_id)
    research_ref = {"object_id": "pkg_1", "version": "1.0.0", "sha256": "a" * 64}

    coord.ingest_approved_hypothesis(
        workspace_id=ws_id,
        hypothesis_record=hypothesis,
        guest_research_package=research_ref,
        lane=AuthorityLane.HUNTER,
    )

    agg_id = coord._aggregate_id
    agg = runtime.get_aggregate(agg_id)
    assert agg.current_state == "HYPOTHESIS_LOADED"

    # Commander attempts repair to initial state
    coord.execute_repair_or_quarantine(
        workspace_id=ws_id,
        reason="Upstream research signal flagged as obsolete",
        target_state="INITIAL",
        lane=AuthorityLane.COMMANDER,
    )

    # In repair flow, aggregate returns to INITIAL state
    agg_repaired = runtime.get_aggregate(agg_id)
    assert agg_repaired.current_state == "INITIAL"
    assert "Upstream research signal" in agg_repaired.state_data["repaired_reason"]
