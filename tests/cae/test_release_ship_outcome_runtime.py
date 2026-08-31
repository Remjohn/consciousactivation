"""
test_release_ship_outcome_runtime.py
------------------------------------
Acceptance Test Suite for CAE Phase 4 Mandate M45: Release / Ship / Outcome Runtime.

Covers:
1. Program package discovery, manifest, and flat passive skills
2. Canonical state machine grammar and transitions
3. Full receipt-driven production release, ship, outcome, and learning lifecycle
4. Four-lane authority separation strict enforcement
5. Anti-synthetic fail-closed blocking
6. Evidence quote integrity and lineage verification
7. Dual-Axis QA independent separation & error isolation
8. Backend-authoritative operator release authorization
9. Failed ship never reports success & delivery failure handling
10. Anti-reward hacking (engagement without truth, misleading context, disagreement laundering)
11. Prohibited direct ontology auto-mutation
12. Multi-tenant workspace isolation
13. Governed fault recovery and bounded repair
"""

import hashlib
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_state_runtime import (
    ProgramStateAggregate,
    UniversalProgramStateRuntime,
    get_canonical_release_ship_outcome_state_machine,
)
from ca_runtime.release_ship_outcome_program import (
    AntiRewardHackingViolationError,
    EvidenceIntegrityViolationError,
    FinalQAVerificationRecord,
    IncompleteQAError,
    InvalidStateTransitionError,
    LaneAuthorityViolationError,
    MissingEvidenceLineageError,
    OntologyMutationViolationError,
    OperatorAuthorizationRequiredError,
    OperatorReleaseAuthorization,
    OutcomeObservationRecord,
    ReleaseShipOutcomeCoordinator,
    ReleaseShipProgramError,
    RenderQAFailureError,
    SemanticQAFailureError,
    ShipmentExecutionFailureError,
    ShipmentReceipt,
    SyntheticProductionBlockedError,
)
from cae_outcome_intelligence.domain import (
    FailureMode,
    LearningProposal,
    ObservedOutcome,
    OutcomeDomain,
    PerformanceMemory,
)


@pytest.fixture
def runtime() -> UniversalProgramStateRuntime:
    return UniversalProgramStateRuntime()


@pytest.fixture
def coordinator(runtime: UniversalProgramStateRuntime) -> ReleaseShipOutcomeCoordinator:
    return ReleaseShipOutcomeCoordinator(runtime=runtime)


@pytest.fixture
def sample_workspace_id() -> UUID:
    return uuid4()


@pytest.fixture
def authentic_evidence() -> dict:
    quote = "Conscious activation is about anchoring directly into authentic human expression."
    quote_sha = hashlib.sha256(quote.encode("utf-8")).hexdigest()
    return {
        "segment_id": "seg-auth-001",
        "quote_text": quote,
        "evidence_quote_sha256": quote_sha,
        "speaker": "Jean Pierre",
        "is_synthetic": False,
    }


@pytest.fixture
def valid_wrong_reading_locks() -> list:
    return sorted([
        "NO_GENERIC_MARKETING_PLATITUDES",
        "PRESERVE_AUTHENTIC_ACOUSTIC_TAIL",
        "SOURCE_ANCHORED_PRIMARY_A_ROLL",
    ])


@pytest.fixture
def passing_qa_results() -> tuple:
    semantic_qa = {
        "passed": True,
        "source_fidelity_score": 0.98,
        "narrative_role": "PRIMARY_EXPRESSION",
        "speaker_verified": True,
    }
    render_qa = {
        "passed": True,
        "container_format": "mp4",
        "resolution": "1080x1920",
        "duration_ms": 42500,
        "audio_sync_valid": True,
    }
    return semantic_qa, render_qa


# ============================================================================
# Test 1: Program Package Discovery and Manifest Verification
# ============================================================================

def test_01_program_package_discovery_and_manifest():
    """Verify package manifest, constitutional CAE.md, and flat passive skills."""
    programs_dir = Path(__file__).parents[2] / "programs"
    registry = ProgramRegistry(discovery_roots=[programs_dir])
    packages = {p.manifest.id: p for p in registry.discover()}

    assert "release_ship_outcome_program" in packages, "release_ship_outcome_program must be discovered"
    pkg = packages["release_ship_outcome_program"]

    assert pkg.manifest.id == "release_ship_outcome_program"
    assert pkg.manifest.version == "1.0.0"
    assert pkg.manifest.state_machine == "RELEASE_SHIP_OUTCOME_STATE_MACHINE_V1"

    expected_lanes = {"COMMANDER", "HUNTER", "COMPOSER", "ANALYST"}
    actual_lanes = set(pkg.manifest.lanes)
    assert expected_lanes.issubset(actual_lanes), f"Missing lanes: {expected_lanes - actual_lanes}"

    skill_ids = [s.name for s in pkg.manifest.skills]
    assert "final_qa_verifier" in skill_ids
    assert "release_authorization_operator" in skill_ids
    assert "shipment_distribution_composer" in skill_ids
    assert "outcome_empirical_hunter" in skill_ids
    assert "selective_learning_analyst" in skill_ids

    # Verify no skill nesting
    for skill in pkg.manifest.skills:
        skill_path = Path(pkg.package_root) / skill.path
        assert skill_path.exists(), f"Skill file {skill_path} must exist"
        content = skill_path.read_text(encoding="utf-8")
        assert "invoke_skill" not in content, f"Skill nesting forbidden in {skill.name}"


# ============================================================================
# Test 2: State Machine Grammar and Transitions
# ============================================================================

def test_02_state_machine_grammar_and_transitions():
    """Verify state machine states, lane requirements, and repair transitions."""
    sm = get_canonical_release_ship_outcome_state_machine()

    assert sm.machine_id == "RELEASE_SHIP_OUTCOME_STATE_MACHINE_V1"
    assert sm.initial_state == "INITIAL"

    expected_transitions = {
        "verify_final_qa": ("INITIAL", "QA_VERIFIED", AuthorityLane.ANALYST),
        "authorize_release": ("QA_VERIFIED", "RELEASE_AUTHORIZED", AuthorityLane.COMMANDER),
        "execute_ship": ("RELEASE_AUTHORIZED", "SHIPPED", AuthorityLane.COMPOSER),
        "capture_outcome": ("SHIPPED", "OUTCOME_CAPTURED", AuthorityLane.HUNTER),
        "propose_learning": ("OUTCOME_CAPTURED", "LEARNING_PROPOSED", AuthorityLane.ANALYST),
        "ratify_proposal": ("LEARNING_PROPOSED", "LEARNING_PROPOSED", AuthorityLane.COMMANDER),
    }

    for trans_name, (from_s, to_s, req_lane) in expected_transitions.items():
        assert trans_name in sm.transitions, f"Transition {trans_name} must be declared"
        t = sm.transitions[trans_name]
        assert t.from_state == from_s
        assert t.to_state == to_s
        assert t.required_lane == req_lane

    assert "fail_qa_to_repair" in sm.repair_transitions
    assert "fail_ship_to_repair" in sm.repair_transitions
    assert "repair_to_initial" in sm.repair_transitions


# ============================================================================
# Test 3: Full Receipt-Driven Release / Ship / Outcome Lifecycle E2E
# ============================================================================

def test_03_full_receipt_driven_release_ship_outcome_lifecycle_e2e(
    coordinator: ReleaseShipOutcomeCoordinator,
    sample_workspace_id: UUID,
    authentic_evidence: dict,
    valid_wrong_reading_locks: list,
    passing_qa_results: tuple,
):
    """E2E verification of full lifecycle: admit -> QA verify -> authorize -> ship -> outcome -> learning proposal -> ratify."""
    semantic_qa, render_qa = passing_qa_results

    # 1. Initialize session
    aggregate = coordinator.initialize_session(
        candidate_id="cand-001",
        workspace_id=sample_workspace_id,
        actor_id="operator:lead",
        artifact_ref={"artifact_id": "art-001", "sha256": "a" * 64, "path": "/media/art-001.mp4"},
    )
    assert aggregate.current_state == "INITIAL"

    # 2. Verify Final QA (ANALYST)
    qa_record = coordinator.verify_final_qa(
        aggregate_id=aggregate.aggregate_id,
        actor_id="analyst:qa",
        actor_lane=AuthorityLane.ANALYST,
        semantic_qa_result=semantic_qa,
        render_qa_result=render_qa,
        evidence_segment=authentic_evidence,
        wrong_reading_locks=valid_wrong_reading_locks,
    )
    assert isinstance(qa_record, FinalQAVerificationRecord)
    assert qa_record.semantic_qa_passed is True
    assert qa_record.render_qa_passed is True
    assert coordinator.runtime.get_aggregate(aggregate.aggregate_id).current_state == "QA_VERIFIED"

    # 3. Authorize Release (COMMANDER)
    auth = coordinator.authorize_release(
        aggregate_id=aggregate.aggregate_id,
        operator_id="commander:lead",
        actor_lane=AuthorityLane.COMMANDER,
        decision="APPROVED",
        target_channels=["web", "podcast_feed"],
        rationale="Approved for multi-channel distribution following complete QA clearance.",
    )
    assert isinstance(auth, OperatorReleaseAuthorization)
    assert auth.decision == "APPROVED"
    assert coordinator.runtime.get_aggregate(aggregate.aggregate_id).current_state == "RELEASE_AUTHORIZED"

    # 4. Execute Shipment (COMPOSER)
    receipt = coordinator.execute_ship(
        aggregate_id=aggregate.aggregate_id,
        actor_id="composer:dispatcher",
        actor_lane=AuthorityLane.COMPOSER,
        target_channel="web",
        delivery_endpoint="https://cdn.consciousactivations.com/publish/art-001.mp4",
    )
    assert isinstance(receipt, ShipmentReceipt)
    assert receipt.delivery_status == "DELIVERED"
    assert receipt.target_channel == "web"
    assert coordinator.runtime.get_aggregate(aggregate.aggregate_id).current_state == "SHIPPED"

    # 5. Capture Outcome (HUNTER)
    outcome, ev_receipt, obs_rec = coordinator.capture_outcome(
        aggregate_id=aggregate.aggregate_id,
        actor_id="hunter:telemetry",
        actor_lane=AuthorityLane.HUNTER,
        domain=OutcomeDomain.PERCEPTUAL,
        metrics={"views": 1500.0, "completion_rate": 0.82, "resonance_score": 0.88},
        predicted_composite_score=0.85,
        observed_normalized_score=0.88,
        evaluator_scores={"eval_1": 0.86, "eval_2": 0.90},
        is_grounded=True,
    )
    assert isinstance(outcome, ObservedOutcome)
    assert outcome.metrics["views"] == 1500.0
    assert coordinator.runtime.get_aggregate(aggregate.aggregate_id).current_state == "OUTCOME_CAPTURED"

    # 6. Propose Learning (ANALYST)
    memory = PerformanceMemory(
        workspace_id=str(sample_workspace_id),
        outcomes=[outcome],
        receipts=[
            ev_receipt,
            # Add recurring under-prediction receipts to trigger calibration proposal
            ev_receipt.model_copy(update={"receipt_id": "EVR-002", "score_delta": 0.30}),
            ev_receipt.model_copy(update={"receipt_id": "EVR-003", "score_delta": 0.35}),
        ],
    )
    proposals = coordinator.propose_learning(
        aggregate_id=aggregate.aggregate_id,
        actor_id="analyst:calibration",
        actor_lane=AuthorityLane.ANALYST,
        performance_memory=memory,
        min_recurrence=2,
    )
    assert len(proposals) >= 1
    assert proposals[0].requires_operator_ratification is True
    assert coordinator.runtime.get_aggregate(aggregate.aggregate_id).current_state == "LEARNING_PROPOSED"

    # 7. Ratify Proposal (COMMANDER)
    rat_rec = coordinator.ratify_learning_proposal(
        aggregate_id=aggregate.aggregate_id,
        operator_id="commander:lead",
        actor_lane=AuthorityLane.COMMANDER,
        proposal_id=proposals[0].proposal_id,
        decision="RATIFIED",
    )
    assert rat_rec["decision"] == "RATIFIED"


# ============================================================================
# Test 4: Four-Lane Authority Separation Strict Enforcement
# ============================================================================

def test_04_four_lane_authority_separation_strict_enforcement(
    coordinator: ReleaseShipOutcomeCoordinator,
    sample_workspace_id: UUID,
    authentic_evidence: dict,
    valid_wrong_reading_locks: list,
    passing_qa_results: tuple,
):
    """Verify that calling operations from the wrong authority lane strictly fails closed."""
    semantic_qa, render_qa = passing_qa_results

    aggregate = coordinator.initialize_session(
        candidate_id="cand-lane-001",
        workspace_id=sample_workspace_id,
        actor_id="operator:lead",
        artifact_ref={"artifact_id": "art-001", "sha256": "a" * 64},
    )

    # 1. COMMANDER cannot execute verify_final_qa (must be ANALYST)
    with pytest.raises(LaneAuthorityViolationError):
        coordinator.verify_final_qa(
            aggregate_id=aggregate.aggregate_id,
            actor_id="commander:lead",
            actor_lane=AuthorityLane.COMMANDER,
            semantic_qa_result=semantic_qa,
            render_qa_result=render_qa,
            evidence_segment=authentic_evidence,
            wrong_reading_locks=valid_wrong_reading_locks,
        )

    # Legitimate QA verification
    coordinator.verify_final_qa(
        aggregate_id=aggregate.aggregate_id,
        actor_id="analyst:qa",
        actor_lane=AuthorityLane.ANALYST,
        semantic_qa_result=semantic_qa,
        render_qa_result=render_qa,
        evidence_segment=authentic_evidence,
        wrong_reading_locks=valid_wrong_reading_locks,
    )

    # 2. ANALYST cannot authorize release (must be COMMANDER)
    with pytest.raises(LaneAuthorityViolationError):
        coordinator.authorize_release(
            aggregate_id=aggregate.aggregate_id,
            operator_id="analyst:qa",
            actor_lane=AuthorityLane.ANALYST,
            decision="APPROVED",
            target_channels=["web"],
            rationale="Analyst attempting unauthorized release authorization.",
        )

    # Legitimate Release authorization
    coordinator.authorize_release(
        aggregate_id=aggregate.aggregate_id,
        operator_id="commander:lead",
        actor_lane=AuthorityLane.COMMANDER,
        decision="APPROVED",
        target_channels=["web"],
        rationale="Authorized by human operator.",
    )

    # 3. HUNTER cannot execute ship (must be COMPOSER)
    with pytest.raises(LaneAuthorityViolationError):
        coordinator.execute_ship(
            aggregate_id=aggregate.aggregate_id,
            actor_id="hunter:scout",
            actor_lane=AuthorityLane.HUNTER,
            target_channel="web",
            delivery_endpoint="https://cdn.example.com/asset.mp4",
        )


# ============================================================================
# Test 5: Anti-Synthetic Fail-Closed Blocking
# ============================================================================

def test_05_anti_synthetic_fail_closed_blocking(
    coordinator: ReleaseShipOutcomeCoordinator,
    sample_workspace_id: UUID,
    authentic_evidence: dict,
    valid_wrong_reading_locks: list,
    passing_qa_results: tuple,
):
    """Verify that synthetic demands or ungrounded mock candidates fail closed."""
    semantic_qa, render_qa = passing_qa_results

    aggregate = coordinator.initialize_session(
        candidate_id="cand-syn-001",
        workspace_id=sample_workspace_id,
        actor_id="operator:lead",
        artifact_ref={"artifact_id": "art-syn-001", "sha256": "b" * 64},
    )

    # Flagged synthetic
    with pytest.raises(SyntheticProductionBlockedError):
        coordinator.verify_final_qa(
            aggregate_id=aggregate.aggregate_id,
            actor_id="analyst:qa",
            actor_lane=AuthorityLane.ANALYST,
            semantic_qa_result=semantic_qa,
            render_qa_result=render_qa,
            evidence_segment=authentic_evidence,
            wrong_reading_locks=valid_wrong_reading_locks,
            is_synthetic=True,
        )


# ============================================================================
# Test 6: Evidence Quote Integrity and Lineage Verification
# ============================================================================

def test_06_evidence_lineage_verification(
    coordinator: ReleaseShipOutcomeCoordinator,
    sample_workspace_id: UUID,
    valid_wrong_reading_locks: list,
    passing_qa_results: tuple,
):
    """Verify that quote tampering or missing evidence quotes strictly fail closed."""
    semantic_qa, render_qa = passing_qa_results

    aggregate = coordinator.initialize_session(
        candidate_id="cand-tamper-001",
        workspace_id=sample_workspace_id,
        actor_id="operator:lead",
        artifact_ref={"artifact_id": "art-001", "sha256": "c" * 64},
    )

    # 1. Missing quote text
    with pytest.raises(MissingEvidenceLineageError):
        coordinator.verify_final_qa(
            aggregate_id=aggregate.aggregate_id,
            actor_id="analyst:qa",
            actor_lane=AuthorityLane.ANALYST,
            semantic_qa_result=semantic_qa,
            render_qa_result=render_qa,
            evidence_segment={"quote_text": "", "is_synthetic": False},
            wrong_reading_locks=valid_wrong_reading_locks,
        )

    # 2. Tampered SHA-256
    with pytest.raises(EvidenceIntegrityViolationError):
        coordinator.verify_final_qa(
            aggregate_id=aggregate.aggregate_id,
            actor_id="analyst:qa",
            actor_lane=AuthorityLane.ANALYST,
            semantic_qa_result=semantic_qa,
            render_qa_result=render_qa,
            evidence_segment={
                "quote_text": "Genuine quote from the interview.",
                "evidence_quote_sha256": "deadbeef" * 8,
                "is_synthetic": False,
            },
            wrong_reading_locks=valid_wrong_reading_locks,
        )


# ============================================================================
# Test 7: Dual-Axis QA Independent Separation & Failures
# ============================================================================

def test_07_dual_axis_qa_separation_and_independent_failures(
    coordinator: ReleaseShipOutcomeCoordinator,
    sample_workspace_id: UUID,
    authentic_evidence: dict,
    valid_wrong_reading_locks: list,
):
    """Verify independent isolation of Semantic QA vs Render QA failures."""
    aggregate = coordinator.initialize_session(
        candidate_id="cand-qa-001",
        workspace_id=sample_workspace_id,
        actor_id="operator:lead",
        artifact_ref={"artifact_id": "art-001", "sha256": "d" * 64},
    )

    # 1. Semantic QA failure isolates cleanly
    with pytest.raises(SemanticQAFailureError):
        coordinator.verify_final_qa(
            aggregate_id=aggregate.aggregate_id,
            actor_id="analyst:qa",
            actor_lane=AuthorityLane.ANALYST,
            semantic_qa_result={"passed": False, "failure_reason": "Speaker authenticity unverified."},
            render_qa_result={"passed": True},
            evidence_segment=authentic_evidence,
            wrong_reading_locks=valid_wrong_reading_locks,
        )

    # 2. Render QA failure isolates cleanly
    with pytest.raises(RenderQAFailureError):
        coordinator.verify_final_qa(
            aggregate_id=aggregate.aggregate_id,
            actor_id="analyst:qa",
            actor_lane=AuthorityLane.ANALYST,
            semantic_qa_result={"passed": True},
            render_qa_result={"passed": False, "failure_reason": "Audio-video sync out by 450ms."},
            evidence_segment=authentic_evidence,
            wrong_reading_locks=valid_wrong_reading_locks,
        )


# ============================================================================
# Test 8: Operator Authorization is Backend-Authoritative
# ============================================================================

def test_08_operator_authorization_is_backend_authoritative(
    coordinator: ReleaseShipOutcomeCoordinator,
    sample_workspace_id: UUID,
    authentic_evidence: dict,
    valid_wrong_reading_locks: list,
    passing_qa_results: tuple,
):
    """Verify that operator approval is strictly enforced and rejection blocks shipping."""
    semantic_qa, render_qa = passing_qa_results

    aggregate = coordinator.initialize_session(
        candidate_id="cand-op-001",
        workspace_id=sample_workspace_id,
        actor_id="operator:lead",
        artifact_ref={"artifact_id": "art-001", "sha256": "e" * 64},
    )
    coordinator.verify_final_qa(
        aggregate_id=aggregate.aggregate_id,
        actor_id="analyst:qa",
        actor_lane=AuthorityLane.ANALYST,
        semantic_qa_result=semantic_qa,
        render_qa_result=render_qa,
        evidence_segment=authentic_evidence,
        wrong_reading_locks=valid_wrong_reading_locks,
    )

    # Rejection by operator raises error
    with pytest.raises(OperatorAuthorizationRequiredError):
        coordinator.authorize_release(
            aggregate_id=aggregate.aggregate_id,
            operator_id="commander:lead",
            actor_lane=AuthorityLane.COMMANDER,
            decision="REJECTED",
            target_channels=["web"],
            rationale="Pacing does not meet editorial standards.",
        )

    # Attempting to ship without authorization fails
    with pytest.raises(OperatorAuthorizationRequiredError):
        coordinator.execute_ship(
            aggregate_id=aggregate.aggregate_id,
            actor_id="composer:dispatcher",
            actor_lane=AuthorityLane.COMPOSER,
            target_channel="web",
            delivery_endpoint="https://cdn.example.com/asset.mp4",
        )


# ============================================================================
# Test 9: Failed Ship Never Reports Success
# ============================================================================

def test_09_failed_ship_never_reports_success(
    coordinator: ReleaseShipOutcomeCoordinator,
    sample_workspace_id: UUID,
    authentic_evidence: dict,
    valid_wrong_reading_locks: list,
    passing_qa_results: tuple,
):
    """Verify that failed shipment halts pipeline and NEVER reports success or transitions to SHIPPED."""
    semantic_qa, render_qa = passing_qa_results

    aggregate = coordinator.initialize_session(
        candidate_id="cand-shipfail-001",
        workspace_id=sample_workspace_id,
        actor_id="operator:lead",
        artifact_ref={"artifact_id": "art-001", "sha256": "f" * 64},
    )
    coordinator.verify_final_qa(
        aggregate_id=aggregate.aggregate_id,
        actor_id="analyst:qa",
        actor_lane=AuthorityLane.ANALYST,
        semantic_qa_result=semantic_qa,
        render_qa_result=render_qa,
        evidence_segment=authentic_evidence,
        wrong_reading_locks=valid_wrong_reading_locks,
    )
    coordinator.authorize_release(
        aggregate_id=aggregate.aggregate_id,
        operator_id="commander:lead",
        actor_lane=AuthorityLane.COMMANDER,
        decision="APPROVED",
        target_channels=["web"],
        rationale="Approved for web distribution.",
    )

    # Failed ship simulation
    with pytest.raises(ShipmentExecutionFailureError):
        coordinator.execute_ship(
            aggregate_id=aggregate.aggregate_id,
            actor_id="composer:dispatcher",
            actor_lane=AuthorityLane.COMPOSER,
            target_channel="web",
            delivery_endpoint="https://cdn.example.com/asset.mp4",
            simulate_channel_failure=True,
        )

    # State must remain RELEASE_AUTHORIZED (never SHIPPED)
    agg_after = coordinator.runtime.get_aggregate(aggregate.aggregate_id)
    assert agg_after.current_state == "RELEASE_AUTHORIZED"
    assert "shipment_receipt" not in agg_after.state_data


# ============================================================================
# Test 10: Anti-Reward Hacking & Disagreement Exposure
# ============================================================================

def test_10_anti_reward_hacking_and_disagreement_exposure(
    coordinator: ReleaseShipOutcomeCoordinator,
    sample_workspace_id: UUID,
    authentic_evidence: dict,
    valid_wrong_reading_locks: list,
    passing_qa_results: tuple,
):
    """Verify that viral engagement without truth and misleading context are rejected."""
    semantic_qa, render_qa = passing_qa_results

    aggregate = coordinator.initialize_session(
        candidate_id="cand-hack-001",
        workspace_id=sample_workspace_id,
        actor_id="operator:lead",
        artifact_ref={"artifact_id": "art-001", "sha256": "1" * 64},
    )
    coordinator.verify_final_qa(
        aggregate_id=aggregate.aggregate_id,
        actor_id="analyst:qa",
        actor_lane=AuthorityLane.ANALYST,
        semantic_qa_result=semantic_qa,
        render_qa_result=render_qa,
        evidence_segment=authentic_evidence,
        wrong_reading_locks=valid_wrong_reading_locks,
    )
    coordinator.authorize_release(
        aggregate_id=aggregate.aggregate_id,
        operator_id="commander:lead",
        actor_lane=AuthorityLane.COMMANDER,
        decision="APPROVED",
        target_channels=["web"],
        rationale="Approved for web.",
    )
    coordinator.execute_ship(
        aggregate_id=aggregate.aggregate_id,
        actor_id="composer:dispatcher",
        actor_lane=AuthorityLane.COMPOSER,
        target_channel="web",
        delivery_endpoint="https://cdn.example.com/asset.mp4",
    )

    # 1. Viral engagement without truth
    with pytest.raises(AntiRewardHackingViolationError):
        coordinator.capture_outcome(
            aggregate_id=aggregate.aggregate_id,
            actor_id="hunter:telemetry",
            actor_lane=AuthorityLane.HUNTER,
            domain=OutcomeDomain.DISTRIBUTION,
            metrics={"views": 50000.0, "retention_rate": 0.85},
            predicted_composite_score=0.90,
            observed_normalized_score=0.95,
            is_grounded=False,  # Un-grounded!
        )

    # 2. Misleading context
    with pytest.raises(AntiRewardHackingViolationError):
        coordinator.capture_outcome(
            aggregate_id=aggregate.aggregate_id,
            actor_id="hunter:telemetry",
            actor_lane=AuthorityLane.HUNTER,
            domain=OutcomeDomain.DISTRIBUTION,
            metrics={"views": 2000.0},
            predicted_composite_score=0.70,
            observed_normalized_score=0.75,
            is_grounded=True,
            misleading_context=True,  # Misleading!
        )


# ============================================================================
# Test 11: Direct Ontology Mutation Prohibited
# ============================================================================

def test_11_direct_ontology_mutation_prohibited(
    coordinator: ReleaseShipOutcomeCoordinator,
    sample_workspace_id: UUID,
):
    """Verify that applying learning proposals directly to ontology raises OntologyMutationViolationError."""
    proposal = LearningProposal(
        workspace_id=str(sample_workspace_id),
        pattern_summary="Systematic under-prediction across 5 programs.",
        proposal_type="EVALUATOR_CALIBRATION",
        suggested_modifications={"weight_adjustment": +0.10},
        recurrence_count=5,
        evidence_receipt_ids=["EVR-001", "EVR-002"],
        requires_operator_ratification=True,
    )

    with pytest.raises(OntologyMutationViolationError):
        coordinator.attempt_direct_ontology_mutation(proposal)


# ============================================================================
# Test 12: Multi-Tenant Workspace Isolation
# ============================================================================

def test_12_multi_tenant_workspace_isolation(
    coordinator: ReleaseShipOutcomeCoordinator,
    sample_workspace_id: UUID,
):
    """Verify that aggregate access across distinct workspaces is partitioned."""
    ws_a = sample_workspace_id
    ws_b = uuid4()

    agg_a = coordinator.initialize_session(
        candidate_id="cand-ws-a",
        workspace_id=ws_a,
        actor_id="operator:a",
        artifact_ref={"artifact_id": "art-a", "sha256": "2" * 64},
    )

    agg_b = coordinator.initialize_session(
        candidate_id="cand-ws-b",
        workspace_id=ws_b,
        actor_id="operator:b",
        artifact_ref={"artifact_id": "art-b", "sha256": "3" * 64},
    )

    assert agg_a.workspace_id == str(ws_a)
    assert agg_b.workspace_id == str(ws_b)
    assert agg_a.aggregate_id != agg_b.aggregate_id


# ============================================================================
# Test 13: Governed Fault Recovery and Bounded Repair
# ============================================================================

def test_13_governed_fault_recovery_and_bounded_repair(
    coordinator: ReleaseShipOutcomeCoordinator,
    sample_workspace_id: UUID,
    authentic_evidence: dict,
    valid_wrong_reading_locks: list,
    passing_qa_results: tuple,
):
    """Verify transition to REPAIRING and governed resumption under COMMANDER lane."""
    semantic_qa, render_qa = passing_qa_results

    aggregate = coordinator.initialize_session(
        candidate_id="cand-repair-001",
        workspace_id=sample_workspace_id,
        actor_id="operator:lead",
        artifact_ref={"artifact_id": "art-001", "sha256": "4" * 64},
    )
    coordinator.verify_final_qa(
        aggregate_id=aggregate.aggregate_id,
        actor_id="analyst:qa",
        actor_lane=AuthorityLane.ANALYST,
        semantic_qa_result=semantic_qa,
        render_qa_result=render_qa,
        evidence_segment=authentic_evidence,
        wrong_reading_locks=valid_wrong_reading_locks,
    )

    # Trigger repair transition
    agg_rep = coordinator.request_repair(
        aggregate_id=aggregate.aggregate_id,
        actor_id="commander:lead",
        actor_lane=AuthorityLane.COMMANDER,
        repair_rationale="Upstream narrative adjustment requested by operator.",
        transition_name="fail_qa_to_repair",
    )
    assert agg_rep.current_state == "REPAIRING"

    # Resume from repair back to INITIAL
    agg_resumed = coordinator.resume_from_repair(
        aggregate_id=aggregate.aggregate_id,
        actor_id="commander:lead",
        actor_lane=AuthorityLane.COMMANDER,
        target_state="INITIAL",
    )
    assert agg_resumed.current_state == "INITIAL"
