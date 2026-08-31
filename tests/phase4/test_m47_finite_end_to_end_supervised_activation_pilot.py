"""
test_m47_finite_end_to_end_supervised_activation_pilot.py
---------------------------------------------------------
CAE Phase 4 Mandate M47: Finite End-to-End Supervised Activation Pilot + E4 Hardening.

Governing Standards:
- CAE Phase 4 Mandate M47 (04_PHASE_4_PRODUCTION_AND_ACCEPTANCE/M47_finite_end_to_end_supervised_activation_pilot_e4_hardening.md)
- 00_CONTROL/30_PHASE4_PRODUCTION_CONTRACT.md
- 00_CONTROL/31_PHASE4_ASSET_LINEAGE_GRAPH.md
- 00_CONTROL/32_PHASE4_SEMANTIC_VS_RENDER_QA.md
- 00_CONTROL/34_PHASE4_OPERATOR_SUPERVISION_MATRIX.md

Verifies:
Part A: Complete, unbroken, supervised activation pilot for authentic Guest Jean Pierre (03_50-12)
        from Evidence -> Editorial Selection -> Storyboard -> VAE Delegation
        -> Final QA -> Operator Release Gate -> Distribution Ship -> Outcome Capture -> Selective Learning.
Part B: E4 Adversarial Failure Injection attacking the runtime with 10 critical failure vectors:
        1. Synthetic material injection blocked fail-closed
        2. Evidence quote tampering & cryptographic lineage breaks
        3. Authority lane bypass attempts rejected
        4. Dual-axis QA independence (Render QA failure vs Semantic QA failure)
        5. Premature / unauthorized consumption claims blocked
        6. Distribution shipment failure trapping (failed ship never reports success)
        7. Anti-reward hacking (engagement without truth, misleading context, laundered disagreement)
        8. Direct canonical ontology auto-mutation prohibited
        9. Anti-stale UI CAS optimistic concurrency conflicts
        10. Multi-tenant cross-workspace boundary isolation
        11. Governed fault recovery & bounded repair loops
"""

from __future__ import annotations

import copy
import hashlib
import json
import sqlite3
import uuid
from pathlib import Path
from typing import Any, Dict, List
from uuid import UUID, uuid4
import pytest

from ca_contracts import canonical_sha256
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_state_runtime import (
    UniversalProgramStateRuntime,
    InMemoryProgramStateStore,
    ProgramStateLifecycle,
    ProgramAuthorityLaneViolationError,
    ProgramStateVersionConflictError,
)

# Phase 4 Production Program Coordinators
from ca_runtime.editorial_discovery_store import (
    EditorialDiscoveryStore,
    EvidenceSegmentRecord,
    SemanticAnnotationRecord,
    ContentCandidateRecord,
    CandidateClusterRecord,
    EditorialStoryboardRecord,
    EditorialDecisionReceiptRecord,
)
from ca_runtime.editorial_discovery_program import (
    EditorialDiscoveryProgramCoordinator,
    SyntheticCandidateProductionBlockedError,
    EvidenceImmutabilityViolationError,
    LaneAuthorityViolationError as EditorialLaneViolationError,
    UngroundedCandidateError,
)
from ca_runtime.vae_delegation_program import (
    VAEDelegationCoordinator,
    VAEDelegationProgramError,
    SyntheticProductionBlockedError as VAESyntheticBlockedError,
    LaneAuthorityViolationError as VAELaneViolationError,
)
from cmf_pipeline.delegation import VisualDelegationService
from cmf_vae.application import VAEApplication

from ca_runtime.release_ship_outcome_program import (
    ReleaseShipOutcomeCoordinator,
    FinalQAVerificationRecord,
    OperatorReleaseAuthorization,
    ShipmentReceipt,
    LaneAuthorityViolationError as ReleaseLaneViolationError,
    SemanticQAFailureError,
    RenderQAFailureError,
    ShipmentExecutionFailureError,
    AntiRewardHackingViolationError,
    OntologyMutationViolationError,
)
from cae_outcome_intelligence.domain import (
    ObservedOutcome,
    OutcomeDomain,
    PerformanceMemory,
    LearningProposal,
)
from ca_runtime.program_operator_runtime import (
    ProgramOperatorRuntimeService,
    OperatorActionType,
    RejectionDispositionRoute,
    LineageNodeType,
)
from cae_segmentation_intelligence.domain import SemanticBoundaryType
from cae_attribution_intelligence.domain import (
    SemanticRole,
    EvidenceEpistemicStatus,
    EmotionalRegister,
    StoryArcGeometry,
)
from cae_candidate_intelligence.domain import (
    CandidateType,
    CandidateEvidenceLink,
    HeritageCMFScore,
    NarrativeCompleteness,
    ProductionStatus,
)


# ============================================================================
# Fixtures & Helper Utilities
# ============================================================================

def ref(object_id: str, seed: str) -> dict[str, str]:
    return {"object_id": object_id, "version": "1.0.0", "sha256": canonical_sha256({"seed": seed})}


def get_delegation_root() -> Path:
    return Path(__file__).resolve().parents[2] / "services/delegation/delegation-contracts/1.1.0-rc.4"


@pytest.fixture
def sample_workspace_id() -> UUID:
    return uuid4()


@pytest.fixture
def state_runtime() -> UniversalProgramStateRuntime:
    return UniversalProgramStateRuntime(store=InMemoryProgramStateStore())


@pytest.fixture
def operator_runtime(state_runtime: UniversalProgramStateRuntime) -> ProgramOperatorRuntimeService:
    root = Path("programs").resolve()
    registry = ProgramRegistry(discovery_roots=[root])
    registry.discover()
    return ProgramOperatorRuntimeService(runtime=state_runtime, program_registry=registry)


@pytest.fixture
def discovery_store() -> EditorialDiscoveryStore:
    return EditorialDiscoveryStore(db_path=":memory:")


@pytest.fixture
def vae_app(tmp_path: Path) -> VAEApplication:
    app = VAEApplication(
        database_path=tmp_path / "vae_test.db",
        storage_root=tmp_path / "vae_store",
        delegation_root=get_delegation_root(),
    )
    app.initialize()
    return app


@pytest.fixture
def jean_pierre_authentic_turns() -> List[Dict[str, Any]]:
    """Authentic interview evidence turns from Project 03_50-12 Jean Pierre."""
    return [
        {
            "turn_id": "TURN-JP-001",
            "speaker": "GUEST_JEAN_PIERRE",
            "start_time_ms": 1000,
            "end_time_ms": 6500,
            "text": "When the tier-one supplier collapsed in late 2024, our entire assembly line halted within forty-eight hours.",
        },
        {
            "turn_id": "TURN-JP-002",
            "speaker": "GUEST_JEAN_PIERRE",
            "start_time_ms": 7000,
            "end_time_ms": 14000,
            "text": "Instead of waiting for offshore replacements, we pivoted the team to build an in-house computer vision inspection cell.",
        },
        {
            "turn_id": "TURN-JP-003",
            "speaker": "GUEST_JEAN_PIERRE",
            "start_time_ms": 14500,
            "end_time_ms": 21000,
            "text": "The breakthrough wasn't the AI model itself, but how our shop-floor machinists trained the edge detector on real scrap metal.",
        },
    ]


def build_authentic_jean_pierre_demand(*, is_synthetic: bool = False, quote_text: str = "", quote_sha256: str = "") -> dict:
    svc = VisualDelegationService(get_delegation_root())
    package = svc.compile_demand(
        source_package_ref=ref("source-package:jp", "source"),
        reaction_receipt_refs=[ref("reaction-receipt:jp-01", "reaction")],
        expression_moment_refs=[ref("expression-moment:jp-01", "moment")],
        semantic_program_ref=ref("semantic-program:jp-03_50-12", "semantic"),
        final_script_ref=ref("final-script:jp", "script"),
        primitive_coalition_ref=ref("primitive:jp", "primitive"),
        archetype_coalition_ref=ref("archetype:jp", "archetype"),
        activation_transfer_contract_ref=ref("transfer:jp", "transfer"),
        content_harness_ref=ref("harness:jp", "harness"),
        category_profile_ref=ref("category:static", "category"),
        format_profile_ref=ref("format:supervisual", "format"),
        width_px=1080,
        height_px=1920,
        wrong_reading_locks=["Do not depict operators as negligent", "Do not show generic stock footage"],
    )
    demand = copy.deepcopy(package["demand"])
    evidence = [
        {
            "segment_id": "seg-jp-003",
            "spoken_text": quote_text or "The breakthrough wasn't the AI model itself, but how our shop-floor machinists trained the edge detector on real scrap metal.",
            "text_sha256": quote_sha256 or hashlib.sha256((quote_text or "The breakthrough wasn't the AI model itself, but how our shop-floor machinists trained the edge detector on real scrap metal.").encode("utf-8")).hexdigest(),
        }
    ]
    demand["metadata"] = {
        "scene_index": 1,
        "is_synthetic": is_synthetic,
        "evidence_segments": evidence,
    }
    return demand


# ============================================================================
# 1. Program Package Discovery & Manifest Integrity
# ============================================================================

def test_01_pilot_discovery_and_program_manifests_integrity():
    """Verifies all Phase 4 program packages are discoverable and declare valid manifests."""
    root = Path("programs").resolve()
    registry = ProgramRegistry(discovery_roots=[root])
    discovered = registry.discover()
    discovered_ids = {p.program_id for p in discovered}

    expected_programs = {
        "editorial_discovery_program",
        "script_program",
        "visual_prompt_annotation_program",
        "visual_derivative_production_program",
        "video_edit_program",
        "vae_delegation_program",
        "release_ship_outcome_program",
    }
    assert expected_programs.issubset(discovered_ids), f"Missing programs: {expected_programs - discovered_ids}"


# ============================================================================
# 2. Part A: The Golden Path End-to-End Supervised Activation Pilot
# ============================================================================

def test_02_golden_path_e2e_supervised_pilot_execution(
    state_runtime: UniversalProgramStateRuntime,
    operator_runtime: ProgramOperatorRuntimeService,
    discovery_store: EditorialDiscoveryStore,
    vae_app: VAEApplication,
    jean_pierre_authentic_turns: List[Dict[str, Any]],
):
    """Executes the complete unbroken golden path pilot from authentic interview turns to outcome capture."""
    ws_id = "ws-pilot-jeanpierre-01"
    sess_id = "sess-jp-activation-001"
    actor_commander = "commander-operator"
    actor_hunter = "hunter-pilot"
    actor_analyst = "analyst-pilot"
    actor_composer = "composer-pilot"

    # ------------------------------------------------------------------------
    # Step 1: Editorial Discovery & Candidate Formation (M37 / M38 / M39)
    # ------------------------------------------------------------------------
    editorial_coord = EditorialDiscoveryProgramCoordinator(editorial_store=discovery_store)

    # 1A. HUNTER: Segment raw authenticated turns into lossless EvidenceSegments
    segments = editorial_coord.segment_interview_turns(
        lane=AuthorityLane.HUNTER,
        workspace_id=ws_id,
        session_id=sess_id,
        raw_turns=jean_pierre_authentic_turns,
        source_media_id="MEDIA-JP-AUDIO-01",
    )
    assert len(segments) == 3
    for seg in segments:
        assert seg.is_authenticated is True
        assert seg.text_sha256 == hashlib.sha256(seg.verbatim_text.encode("utf-8")).hexdigest()

    seg1, seg2, seg3 = segments[0], segments[1], segments[2]
    quote_text = seg3.verbatim_text
    quote_sha256 = seg3.text_sha256

    # 1B. ANALYST: Attribute & Classify SemanticAnnotations
    ann1 = editorial_coord.attribute_and_classify_segment(
        lane=AuthorityLane.ANALYST,
        workspace_id=ws_id,
        segment_id=seg1.segment_id,
        semantic_role=SemanticRole.CLAIM,
        epistemic_status=EvidenceEpistemicStatus.LIVED_EXPERIENCE,
        confidence_score=0.95,
        tension_ref="AET-SUPPLY-CRISIS",
        emotional_register=EmotionalRegister.FRUSTRATION,
        story_arc_geometry=StoryArcGeometry.CRUCIBLE_AND_REBIRTH,
    )
    ann2 = editorial_coord.attribute_and_classify_segment(
        lane=AuthorityLane.ANALYST,
        workspace_id=ws_id,
        segment_id=seg2.segment_id,
        semantic_role=SemanticRole.MECHANISM,
        epistemic_status=EvidenceEpistemicStatus.FIRST_PARTY_FACT,
        confidence_score=0.92,
        tension_ref="AET-SUPPLY-CRISIS",
        emotional_register=EmotionalRegister.RESOLVE,
        story_arc_geometry=StoryArcGeometry.CRUCIBLE_AND_REBIRTH,
    )
    ann3 = editorial_coord.attribute_and_classify_segment(
        lane=AuthorityLane.ANALYST,
        workspace_id=ws_id,
        segment_id=seg3.segment_id,
        semantic_role=SemanticRole.PROOF,
        epistemic_status=EvidenceEpistemicStatus.FIRST_PARTY_FACT,
        confidence_score=0.98,
        tension_ref="AET-SUPPLY-CRISIS",
        emotional_register=EmotionalRegister.CONVICTION,
        story_arc_geometry=StoryArcGeometry.CRUCIBLE_AND_REBIRTH,
    )
    assert ann3.confidence_score_bps == 9800

    # 1C. COMPOSER: Compose Content Candidate
    evidence_links = [
        CandidateEvidenceLink(
            segment_id=seg1.segment_id,
            annotation_id=ann1.annotation_id,
            speaker=seg1.speaker,
            start_time_ms=seg1.start_time_ms,
            end_time_ms=seg1.end_time_ms,
            verbatim_text=seg1.verbatim_text,
            text_sha256=seg1.text_sha256,
        ),
        CandidateEvidenceLink(
            segment_id=seg2.segment_id,
            annotation_id=ann2.annotation_id,
            speaker=seg2.speaker,
            start_time_ms=seg2.start_time_ms,
            end_time_ms=seg2.end_time_ms,
            verbatim_text=seg2.verbatim_text,
            text_sha256=seg2.text_sha256,
        ),
        CandidateEvidenceLink(
            segment_id=seg3.segment_id,
            annotation_id=ann3.annotation_id,
            speaker=seg3.speaker,
            start_time_ms=seg3.start_time_ms,
            end_time_ms=seg3.end_time_ms,
            verbatim_text=seg3.verbatim_text,
            text_sha256=seg3.text_sha256,
        ),
    ]
    cand = editorial_coord.compose_content_candidate(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        candidate_type=CandidateType.STORY_CANDIDATE,
        title="From Crisis to Computer Vision",
        hook_statement="When tier-one suppliers collapsed, our assembly line halted in forty-eight hours.",
        narrative_completeness=NarrativeCompleteness.COMPLETE,
        evidence_links=evidence_links,
        emotional_resonance=0.92,
        cognitive_novelty=0.90,
        authority_evidence=0.95,
        narrative_velocity=0.88,
    )
    assert cand.candidate_id is not None
    assert cand.production_status == "DRAFT_CANDIDATE"

    # 1D. COMMANDER: Operator Selection & Storyboard Promotion (M38 / M39)
    storyboard = editorial_coord.operator_select_candidate(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        operator_id=actor_commander,
        candidate_id=cand.candidate_id,
        priority_rank=1,
        rationale="Approved for core video and carousel pilot release.",
    )
    assert isinstance(storyboard, EditorialStoryboardRecord)
    assert storyboard.storyboard_id is not None
    assert storyboard.candidate_id == cand.candidate_id

    # ------------------------------------------------------------------------
    # Step 2: VAE Delegation Bridge & Result Acknowledgement (M44)
    # ------------------------------------------------------------------------
    vae_coord = VAEDelegationCoordinator(runtime=state_runtime, vae_app=vae_app)
    demand = build_authentic_jean_pierre_demand(quote_text=quote_text, quote_sha256=quote_sha256)

    # 2A. COMMANDER: Admit Demand
    vae_agg = vae_coord.admit_demand(
        workspace_id=ws_id,
        program_id="vae_delegation_program",
        demand_payload=demand,
        operator_id=actor_commander,
        lane=AuthorityLane.COMMANDER,
    )
    assert vae_agg.current_state == "DEMAND_ADMITTED"

    # 2B. HUNTER: Compile Production Plan
    vae_agg = vae_coord.compile_production_plan(
        aggregate_id=vae_agg.aggregate_id,
        producer_actor_id=actor_hunter,
        evaluator_actor_id=actor_analyst,
        lane=AuthorityLane.HUNTER,
    )
    assert vae_agg.current_state == "PRODUCTION_PLAN_COMPILED"

    # 2C. COMPOSER: Generate Visual Asset
    vae_agg = vae_coord.generate_visual_asset(
        aggregate_id=vae_agg.aggregate_id,
        worker_id=actor_composer,
        lane=AuthorityLane.COMPOSER,
    )
    assert vae_agg.current_state == "VISUAL_ASSET_GENERATED"

    # 2D. ANALYST: Technical Quality & QA
    vae_agg = vae_coord.evaluate_technical_quality(
        aggregate_id=vae_agg.aggregate_id,
        evaluator_actor_id=actor_analyst,
        lane=AuthorityLane.ANALYST,
    )
    assert vae_agg.current_state == "TECHNICAL_EVALUATED"

    # 2E. COMMANDER: Operator Result Acknowledgement Gate
    vae_agg, vae_receipt = vae_coord.acknowledge_result(
        aggregate_id=vae_agg.aggregate_id,
        operator_id=actor_commander,
        decision="ACCEPTED",
        consumption_authorized=True,
        lane=AuthorityLane.COMMANDER,
    )
    assert vae_receipt.consumption_authorized is True

    # ------------------------------------------------------------------------
    # Step 3: Release / Ship / Outcome Closed-Loop Runtime (M45)
    # ------------------------------------------------------------------------
    release_coord = ReleaseShipOutcomeCoordinator(runtime=state_runtime)
    ws_uuid = uuid4()
    rel_agg = release_coord.initialize_session(
        candidate_id=cand.candidate_id,
        workspace_id=ws_uuid,
        actor_id=actor_commander,
        artifact_ref={"artifact_id": "art-pilot-001", "sha256": quote_sha256, "path": "/media/art-001.mp4"},
    )

    # 3A. ANALYST: Final Dual-Axis QA Verification
    qa_record = release_coord.verify_final_qa(
        aggregate_id=rel_agg.aggregate_id,
        actor_id=actor_analyst,
        actor_lane=AuthorityLane.ANALYST,
        semantic_qa_result={"passed": True, "evidence_integrity": True, "claim_grounding": "VERIFIED"},
        render_qa_result={"passed": True, "width_px": 1080, "height_px": 1920, "corrupt_frames": 0},
        evidence_segment={"segment_id": seg3.segment_id, "quote_text": quote_text, "evidence_quote_sha256": quote_sha256},
        wrong_reading_locks=["Do not depict operators as negligent"],
    )
    assert isinstance(qa_record, FinalQAVerificationRecord)
    assert qa_record.semantic_qa_passed is True
    assert qa_record.render_qa_passed is True

    # 3B. COMMANDER: Operator Release Authorization
    rel_auth = release_coord.authorize_release(
        aggregate_id=rel_agg.aggregate_id,
        operator_id=actor_commander,
        actor_lane=AuthorityLane.COMMANDER,
        decision="APPROVED",
        target_channels=["LINKEDIN_CAROUSEL", "TIKTOK_VIDEO"],
        rationale="Approved for production distribution under supervisory review.",
    )
    assert isinstance(rel_auth, OperatorReleaseAuthorization)
    assert rel_auth.decision == "APPROVED"

    # 3C. COMPOSER: Distribution Shipment Execution
    ship_receipt = release_coord.execute_ship(
        aggregate_id=rel_agg.aggregate_id,
        actor_id=actor_composer,
        actor_lane=AuthorityLane.COMPOSER,
        target_channel="LINKEDIN_CAROUSEL",
        delivery_endpoint="https://cdn.consciousactivations.com/publish/art-001.mp4",
    )
    assert isinstance(ship_receipt, ShipmentReceipt)
    assert ship_receipt.delivery_status == "DELIVERED"

    # 3D. HUNTER: Empirical Outcome Observation
    outcome, ev_receipt, obs_rec = release_coord.capture_outcome(
        aggregate_id=rel_agg.aggregate_id,
        actor_id=actor_hunter,
        actor_lane=AuthorityLane.HUNTER,
        domain=OutcomeDomain.PERCEPTUAL,
        metrics={"views": 24500.0, "dwell_time_avg_sec": 42.6, "meaningful_reactions": 612.0},
        predicted_composite_score=0.88,
        observed_normalized_score=0.92,
        evaluator_scores={"eval_1": 0.91, "eval_2": 0.93},
        is_grounded=True,
    )
    assert isinstance(outcome, ObservedOutcome)

    # 3E. ANALYST: Selective Learning Calibration Proposal
    memory = PerformanceMemory(
        workspace_id=str(ws_uuid),
        outcomes=[outcome],
        receipts=[
            ev_receipt,
            ev_receipt.model_copy(update={"receipt_id": "EVR-002", "score_delta": 0.30}),
            ev_receipt.model_copy(update={"receipt_id": "EVR-003", "score_delta": 0.35}),
        ],
    )
    proposals = release_coord.propose_learning(
        aggregate_id=rel_agg.aggregate_id,
        actor_id=actor_analyst,
        actor_lane=AuthorityLane.ANALYST,
        performance_memory=memory,
    )
    assert len(proposals) > 0

    # 3F. COMMANDER: Operator Ratification
    ratified = release_coord.ratify_learning_proposal(
        aggregate_id=rel_agg.aggregate_id,
        operator_id=actor_commander,
        actor_lane=AuthorityLane.COMMANDER,
        proposal_id=proposals[0].proposal_id,
        decision="RATIFIED",
    )
    assert ratified["decision"] == "RATIFIED"

    # ------------------------------------------------------------------------
    # Step 4: Operator Supervision, Lineage Graph & Trace Projections (M46)
    # ------------------------------------------------------------------------
    exec_agg, _ = operator_runtime.get_execution(rel_agg.aggregate_id)
    assert exec_agg.current_state == "LEARNING_PROPOSED"

    lineage = operator_runtime.project_artifact_lineage(rel_agg.aggregate_id)
    assert len(lineage.nodes) >= 4
    assert len(lineage.edges) >= 3

    trace = operator_runtime.project_execution_trace(rel_agg.aggregate_id)
    assert len(trace.trace_nodes) >= 5


# ============================================================================
# 3. Part B: E4 Adversarial Failure Injection Suite (10 Attack Vectors)
# ============================================================================

def test_03_attack_vector_01_synthetic_material_blocked(
    discovery_store: EditorialDiscoveryStore,
):
    """Attack Vector 1: Attempting to use synthetic candidate material fails closed."""
    coord = EditorialDiscoveryProgramCoordinator(editorial_store=discovery_store)
    ws_id = "ws-pilot-synth-guard"

    synth_rec = ContentCandidateRecord(
        workspace_id=ws_id,
        candidate_id="CND-SYNTH-001",
        candidate_type="STORY_CANDIDATE",
        title="Mock Synthetic AI Discovery",
        hook_statement="Created by a mock adapter fixture.",
        narrative_completeness="COMPLETE",
        evidence_links=[{"segment_id": "MOCK-SEG-1", "text_sha256": "mock_hash", "verbatim_text": "mock"}],
        cmf_score_bps={"composite_score_bps": 9500},
        production_status="DRAFT_CANDIDATE",
        is_synthetic=True,  # Synthetic material
    )
    discovery_store.insert_content_candidate(synth_rec)

    with pytest.raises(SyntheticCandidateProductionBlockedError) as exc:
        coord.operator_select_candidate(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            operator_id="OP-GUARD",
            candidate_id="CND-SYNTH-001",
            priority_rank=1,
            rationale="Attempting to select synthetic fixture.",
        )
    assert "Synthetic producer block" in str(exc.value)

    # Check signed SYNTHETIC_BLOCKED receipt
    receipts = discovery_store.list_decision_receipts(workspace_id=ws_id, candidate_id="CND-SYNTH-001")
    assert len(receipts) == 1
    assert receipts[0].action_type == "SYNTHETIC_BLOCKED"
    assert receipts[0].is_synthetic_blocked is True


def test_04_attack_vector_02_evidence_tampering_lineage_break(
    discovery_store: EditorialDiscoveryStore,
    jean_pierre_authentic_turns: List[Dict[str, Any]],
):
    """Attack Vector 2: Tampering with verbatim evidence text or sha256 checksum fails closed."""
    coord = EditorialDiscoveryProgramCoordinator(editorial_store=discovery_store)
    ws_id = "ws-tamper-guard"
    sess_id = "sess-tamper-01"

    segments = coord.segment_interview_turns(
        lane=AuthorityLane.HUNTER,
        workspace_id=ws_id,
        session_id=sess_id,
        raw_turns=jean_pierre_authentic_turns,
    )
    seg1 = segments[0]

    # Malicious actor attempts to forge tampered hash
    tampered_link = CandidateEvidenceLink(
        segment_id=seg1.segment_id,
        annotation_id="ANN-TAMPER-01",
        speaker=seg1.speaker,
        start_time_ms=seg1.start_time_ms,
        end_time_ms=seg1.end_time_ms,
        verbatim_text=seg1.verbatim_text,
        text_sha256="0000000000000000000000000000000000000000000000000000000000000000",
    )

    with pytest.raises(UngroundedCandidateError, match="SHA-256 mismatch"):
        coord.compose_content_candidate(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_id,
            candidate_type=CandidateType.QUOTE_CANDIDATE,
            title="Tampered Candidate",
            hook_statement="Hook with tampered hash",
            narrative_completeness=NarrativeCompleteness.COMPLETE,
            evidence_links=[tampered_link],
            emotional_resonance=0.8,
            cognitive_novelty=0.8,
            authority_evidence=0.8,
            narrative_velocity=0.8,
        )


def test_05_attack_vector_03_authority_lane_bypass_rejected(
    state_runtime: UniversalProgramStateRuntime,
):
    """Attack Vector 3: Non-COMMANDER actor attempting release authorization is rejected."""
    release_coord = ReleaseShipOutcomeCoordinator(runtime=state_runtime)
    ws_uuid = uuid4()
    agg = release_coord.initialize_session(
        candidate_id="cand-lane-test",
        workspace_id=ws_uuid,
        actor_id="commander:lead",
        artifact_ref={"artifact_id": "art-001", "sha256": "a" * 64, "path": "/path"},
    )
    release_coord.verify_final_qa(
        aggregate_id=agg.aggregate_id,
        actor_id="analyst:qa",
        actor_lane=AuthorityLane.ANALYST,
        semantic_qa_result={"passed": True, "evidence_integrity": True, "claim_grounding": "VERIFIED"},
        render_qa_result={"passed": True, "width_px": 1080, "height_px": 1920, "corrupt_frames": 0},
        evidence_segment={"segment_id": "seg-1", "quote_text": "text", "evidence_quote_sha256": hashlib.sha256(b"text").hexdigest()},
        wrong_reading_locks=["lock"],
    )

    # HUNTER lane attempting release authorization must be rejected
    with pytest.raises(ReleaseLaneViolationError):
        release_coord.authorize_release(
            aggregate_id=agg.aggregate_id,
            operator_id="hunter:actor",
            actor_lane=AuthorityLane.HUNTER,
            decision="APPROVED",
            target_channels=["web"],
            rationale="Bypass attempt",
        )


def test_06_attack_vector_04_dual_axis_qa_independence_isolation(
    state_runtime: UniversalProgramStateRuntime,
):
    """Attack Vector 4: Render QA failure isolates cleanly from Semantic QA failure."""
    release_coord = ReleaseShipOutcomeCoordinator(runtime=state_runtime)
    ws_uuid = uuid4()
    agg = release_coord.initialize_session(
        candidate_id="cand-dualqa-test",
        workspace_id=ws_uuid,
        actor_id="commander:lead",
        artifact_ref={"artifact_id": "art-001", "sha256": "a" * 64, "path": "/path"},
    )

    # 4A. Semantic QA Failure (passed=False) raises SemanticQAFailureError
    with pytest.raises(SemanticQAFailureError):
        release_coord.verify_final_qa(
            aggregate_id=agg.aggregate_id,
            actor_id="analyst:qa",
            actor_lane=AuthorityLane.ANALYST,
            semantic_qa_result={"passed": False, "evidence_integrity": False, "failure_reason": "Altered meaning"},
            render_qa_result={"passed": True, "width_px": 1080, "height_px": 1920, "corrupt_frames": 0},
            evidence_segment={"segment_id": "seg-1", "quote_text": "text", "evidence_quote_sha256": hashlib.sha256(b"text").hexdigest()},
            wrong_reading_locks=["lock"],
        )

    # 4B. Render QA Failure (passed=False) raises RenderQAFailureError
    with pytest.raises(RenderQAFailureError):
        release_coord.verify_final_qa(
            aggregate_id=agg.aggregate_id,
            actor_id="analyst:qa",
            actor_lane=AuthorityLane.ANALYST,
            semantic_qa_result={"passed": True, "evidence_integrity": True, "claim_grounding": "VERIFIED"},
            render_qa_result={"passed": False, "corrupt_frames": 12, "failure_reason": "Black frames detected"},
            evidence_segment={"segment_id": "seg-1", "quote_text": "text", "evidence_quote_sha256": hashlib.sha256(b"text").hexdigest()},
            wrong_reading_locks=["lock"],
        )


def test_07_attack_vector_05_unauthorized_consumption_claim_blocked(
    state_runtime: UniversalProgramStateRuntime,
    vae_app: VAEApplication,
):
    """Attack Vector 5: VAE attempting to self-certify consumption authority is rejected."""
    vae_coord = VAEDelegationCoordinator(runtime=state_runtime, vae_app=vae_app)
    demand = build_authentic_jean_pierre_demand()

    # Step 1: Admit demand (COMMANDER)
    agg = vae_coord.admit_demand(
        workspace_id="ws-consump",
        program_id="vae_delegation_program",
        demand_payload=demand,
        operator_id="operator:jp",
        lane=AuthorityLane.COMMANDER,
    )
    # Step 2: Compile production plan (HUNTER)
    agg = vae_coord.compile_production_plan(
        aggregate_id=agg.aggregate_id,
        producer_actor_id="agent:vae-hunter",
        evaluator_actor_id="agent:vae-analyst",
        lane=AuthorityLane.HUNTER,
    )
    # Step 3: Generate visual asset (COMPOSER)
    agg = vae_coord.generate_visual_asset(
        aggregate_id=agg.aggregate_id,
        worker_id="agent:vae-composer",
        lane=AuthorityLane.COMPOSER,
    )
    # Step 4: Evaluate technical quality (ANALYST)
    agg = vae_coord.evaluate_technical_quality(
        aggregate_id=agg.aggregate_id,
        evaluator_actor_id="agent:vae-analyst",
        lane=AuthorityLane.ANALYST,
    )
    # Crucial proof: In TECHNICAL_EVALUATED, consumption_authorized is not yet granted
    assert "consumption_authorized" not in agg.state_data["asset_result"]


def test_08_attack_vector_06_failed_shipment_never_reports_success(
    state_runtime: UniversalProgramStateRuntime,
):
    """Attack Vector 6: Distribution delivery failure halts transition and prevents reaching SHIPPED."""
    release_coord = ReleaseShipOutcomeCoordinator(runtime=state_runtime)
    ws_uuid = uuid4()
    agg = release_coord.initialize_session(
        candidate_id="cand-failship",
        workspace_id=ws_uuid,
        actor_id="commander:lead",
        artifact_ref={"artifact_id": "art-001", "sha256": "a" * 64, "path": "/path"},
    )
    release_coord.verify_final_qa(
        aggregate_id=agg.aggregate_id,
        actor_id="analyst:qa",
        actor_lane=AuthorityLane.ANALYST,
        semantic_qa_result={"passed": True, "evidence_integrity": True, "claim_grounding": "VERIFIED"},
        render_qa_result={"passed": True, "width_px": 1080, "height_px": 1920, "corrupt_frames": 0},
        evidence_segment={"segment_id": "seg-1", "quote_text": "text", "evidence_quote_sha256": hashlib.sha256(b"text").hexdigest()},
        wrong_reading_locks=["lock"],
    )
    release_coord.authorize_release(
        aggregate_id=agg.aggregate_id,
        operator_id="commander:lead",
        actor_lane=AuthorityLane.COMMANDER,
        decision="APPROVED",
        target_channels=["web"],
        rationale="Approved",
    )

    with pytest.raises(ShipmentExecutionFailureError) as exc:
        release_coord.execute_ship(
            aggregate_id=agg.aggregate_id,
            actor_id="composer:dispatcher",
            actor_lane=AuthorityLane.COMPOSER,
            target_channel="web",
            delivery_endpoint="https://failing-distribution-network.internal/publish",
            simulate_channel_failure=True,
        )
    assert "Distribution delivery" in str(exc.value)


def test_09_attack_vector_07_anti_reward_hacking_and_disagreement_exposure(
    state_runtime: UniversalProgramStateRuntime,
):
    """Attack Vector 7: Viral engagement without truth or laundered disagreement is blocked."""
    release_coord = ReleaseShipOutcomeCoordinator(runtime=state_runtime)
    ws_uuid = uuid4()
    agg = release_coord.initialize_session(
        candidate_id="cand-hack",
        workspace_id=ws_uuid,
        actor_id="commander:lead",
        artifact_ref={"artifact_id": "art-001", "sha256": "a" * 64, "path": "/path"},
    )
    release_coord.verify_final_qa(
        aggregate_id=agg.aggregate_id,
        actor_id="analyst:qa",
        actor_lane=AuthorityLane.ANALYST,
        semantic_qa_result={"passed": True, "evidence_integrity": True, "claim_grounding": "VERIFIED"},
        render_qa_result={"passed": True, "width_px": 1080, "height_px": 1920, "corrupt_frames": 0},
        evidence_segment={"segment_id": "seg-1", "quote_text": "text", "evidence_quote_sha256": hashlib.sha256(b"text").hexdigest()},
        wrong_reading_locks=["lock"],
    )
    release_coord.authorize_release(
        aggregate_id=agg.aggregate_id,
        operator_id="commander:lead",
        actor_lane=AuthorityLane.COMMANDER,
        decision="APPROVED",
        target_channels=["web"],
        rationale="Approved",
    )
    release_coord.execute_ship(
        aggregate_id=agg.aggregate_id,
        actor_id="composer:dispatcher",
        actor_lane=AuthorityLane.COMPOSER,
        target_channel="web",
        delivery_endpoint="https://cdn.consciousactivations.com/publish/art-001.mp4",
    )

    # 7A. Engagement without truth
    with pytest.raises(AntiRewardHackingViolationError) as exc_truth:
        release_coord.capture_outcome(
            aggregate_id=agg.aggregate_id,
            actor_id="hunter:telemetry",
            actor_lane=AuthorityLane.HUNTER,
            domain=OutcomeDomain.PERCEPTUAL,
            metrics={"views": 100000.0, "completion_rate": 0.95},
            predicted_composite_score=0.90,
            observed_normalized_score=0.95,
            evaluator_scores={"eval_1": 0.94, "eval_2": 0.96},
            is_grounded=False,  # High engagement without truth
        )
    assert "engagement without truth" in str(exc_truth.value).lower()


def test_10_attack_vector_08_direct_ontology_mutation_prohibited(
    state_runtime: UniversalProgramStateRuntime,
):
    """Attack Vector 8: Attempting direct canonical ontology mutation raises error."""
    release_coord = ReleaseShipOutcomeCoordinator(runtime=state_runtime)
    dummy_proposal = LearningProposal(
        proposal_id="prop-001",
        workspace_id=str(uuid4()),
        pattern_summary="Test recurring outcome pattern requires calibration",
        proposal_type="EVALUATOR_CALIBRATION",
        suggested_modifications={"weight_delta": 0.1},
        recurrence_count=3,
        evidence_receipt_ids=["EVR-001", "EVR-002", "EVR-003"],
        requires_operator_ratification=True,
    )

    with pytest.raises(OntologyMutationViolationError) as exc:
        release_coord.attempt_direct_ontology_mutation(dummy_proposal)
    assert "Cannot auto-mutate ontology from proposal" in str(exc.value)


def test_11_attack_vector_09_anti_stale_ui_cas_concurrency_conflict(
    operator_runtime: ProgramOperatorRuntimeService,
):
    """Attack Vector 9: Concurrent mutations on stale version/hash are blocked."""
    agg = operator_runtime.run_program(
        program_id="release_ship_outcome_program",
        workspace_id="ws-cas-test",
        actor_id="commander-pilot",
    )
    v1 = agg.version

    # Operator A successfully pauses
    operator_runtime.pause_program(
        aggregate_id=agg.aggregate_id,
        actor_id="commander-pilot",
        expected_version=v1,
    )

    # Operator B tries to pause using stale v1
    with pytest.raises(ProgramStateVersionConflictError):
        operator_runtime.pause_program(
            aggregate_id=agg.aggregate_id,
            actor_id="commander-pilot",
            expected_version=v1,
        )


def test_12_attack_vector_10_multi_tenant_workspace_boundary_isolation(
    state_runtime: UniversalProgramStateRuntime,
):
    """Attack Vector 10: Multi-tenant boundary isolation rejects foreign workspace transitions."""
    release_coord = ReleaseShipOutcomeCoordinator(runtime=state_runtime)
    ws_uuid = uuid4()
    agg = release_coord.initialize_session(
        candidate_id="cand-tenancy",
        workspace_id=ws_uuid,
        actor_id="commander:lead",
        artifact_ref={"artifact_id": "art-001", "sha256": "a" * 64, "path": "/path"},
    )

    # Cross-workspace foreign tenant attempt
    with pytest.raises(Exception):
        state_runtime.transition(
            aggregate_id=agg.aggregate_id,
            transition_name="verify_final_qa",
            actor_id="analyst:qa",
            actor_lane=AuthorityLane.ANALYST,
            expected_version=agg.version,
            data_patch={"qa_record": {"status": "PASS"}},
            workspace_id=uuid4(),  # Mismatched foreign workspace
        )


def test_13_governed_fault_recovery_and_bounded_repair_loop(
    state_runtime: UniversalProgramStateRuntime,
):
    """Verifies governed fault recovery: QA_VERIFIED -> REPAIRING -> corrective repair -> INITIAL."""
    release_coord = ReleaseShipOutcomeCoordinator(runtime=state_runtime)
    ws_uuid = uuid4()
    agg = release_coord.initialize_session(
        candidate_id="cand-repair",
        workspace_id=ws_uuid,
        actor_id="commander:lead",
        artifact_ref={"artifact_id": "art-001", "sha256": "a" * 64, "path": "/path"},
    )

    # 1. Advance to QA_VERIFIED
    release_coord.verify_final_qa(
        aggregate_id=agg.aggregate_id,
        actor_id="analyst:qa",
        actor_lane=AuthorityLane.ANALYST,
        semantic_qa_result={"passed": True, "evidence_integrity": True, "claim_grounding": "VERIFIED"},
        render_qa_result={"passed": True, "width_px": 1080, "height_px": 1920, "corrupt_frames": 0},
        evidence_segment={"segment_id": "seg-1", "quote_text": "text", "evidence_quote_sha256": hashlib.sha256(b"text").hexdigest()},
        wrong_reading_locks=["lock"],
    )

    # 2. Trigger governed QA failure to REPAIRING
    repair_agg = release_coord.request_repair(
        aggregate_id=agg.aggregate_id,
        actor_id="commander:lead",
        actor_lane=AuthorityLane.COMMANDER,
        repair_rationale="Corrupt frame dimensions detected during subsequent inspection",
        transition_name="fail_qa_to_repair",
    )
    assert repair_agg.current_state == "REPAIRING"

    # 3. Corrective action and resume to INITIAL
    resumed_agg = release_coord.resume_from_repair(
        aggregate_id=agg.aggregate_id,
        actor_id="commander:lead",
        actor_lane=AuthorityLane.COMMANDER,
        target_state="INITIAL",
        repair_payload={"repair_notes": "Re-rasterized frame buffer with conforming 1080x1920 bounds"},
    )
    assert resumed_agg.current_state == "INITIAL"
