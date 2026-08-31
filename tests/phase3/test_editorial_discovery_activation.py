"""
test_editorial_discovery_activation.py
--------------------------------------
Comprehensive test suite for CAE Phase 3 Mandate M35:
Evidence → Editorial Discovery with Synthetic-Proof Block.

Verifies:
1. Complete 6-step causal chain from real InterviewResponse to EditorialStoryboard.
2. Strict fail-closed Synthetic-Proof Block preventing synthetic/mock candidate producers from passing production gates.
3. Ungrounded / tampered evidence rejection.
4. Four Authority Lanes isolation (HUNTER, ANALYST, COMPOSER, COMMANDER).
5. Operator selection, rejection, and framing modification with evidence immutability and audit receipts.
6. Multi-tenant workspace isolation.
"""

import pytest
import hashlib
import uuid
from typing import Any, Dict, List

from ca_contracts import canonical_sha256
from ca_runtime.program_state_runtime import AuthorityLane
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
    EditorialDiscoveryError,
    LaneAuthorityViolationError,
    UngroundedCandidateError,
    SyntheticCandidateProductionBlockedError,
    EvidenceImmutabilityViolationError,
    MissingOperatorRationaleError,
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
    NarrativeCompleteness,
    ProductionStatus,
)
from cae_scoring_intelligence.domain import (
    CandidateEvaluationProfile,
    DimensionScores,
    EvaluatorProvenance,
    GateStatus,
)


@pytest.fixture
def store() -> EditorialDiscoveryStore:
    return EditorialDiscoveryStore(db_path=":memory:")


@pytest.fixture
def coordinator(store: EditorialDiscoveryStore) -> EditorialDiscoveryProgramCoordinator:
    return EditorialDiscoveryProgramCoordinator(editorial_store=store)


@pytest.fixture
def real_interview_turns() -> List[Dict[str, Any]]:
    return [
        {
            "turn_id": "TURN-001",
            "speaker": "GUEST",
            "start_time_ms": 1000,
            "end_time_ms": 5000,
            "text": "When the pandemic hit, we lost eighty percent of our client base within two weeks.",
        },
        {
            "turn_id": "TURN-002",
            "speaker": "GUEST",
            "start_time_ms": 5500,
            "end_time_ms": 12000,
            "text": "Rather than laying off the team, we pivoted to an asynchronous coaching model that saved the company.",
        },
    ]


# ---------------------------------------------------------------------------
# Test 1: Complete 6-Step Lineage Flow (Real Interview → Storyboard)
# ---------------------------------------------------------------------------

def test_complete_editorial_discovery_lineage(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_interview_turns: List[Dict[str, Any]],
):
    ws_id = "WS-PROD-ALPHA"
    session_id = "SES-INTERVIEW-001"

    # Step 1: HUNTER Lane - Segmentation
    segments = coordinator.segment_interview_turns(
        lane=AuthorityLane.HUNTER,
        workspace_id=ws_id,
        session_id=session_id,
        raw_turns=real_interview_turns,
    )
    assert len(segments) == 2
    seg1, seg2 = segments[0], segments[1]
    assert seg1.speaker == "GUEST"
    assert seg1.text_sha256 == hashlib.sha256(seg1.verbatim_text.encode("utf-8")).hexdigest()
    assert seg1.is_authenticated is True

    # Step 2: ANALYST Lane - Semantic Attribution
    ann1 = coordinator.attribute_and_classify_segment(
        lane=AuthorityLane.ANALYST,
        workspace_id=ws_id,
        segment_id=seg1.segment_id,
        semantic_role=SemanticRole.CLAIM,
        epistemic_status=EvidenceEpistemicStatus.LIVED_EXPERIENCE,
        confidence_score=0.92,
        tension_ref="TEN-EXT-01",
    )
    assert ann1.confidence_score_bps == 9200
    assert ann1.is_publishable is False
    assert ann1.semantic_role == "CLAIM"

    ann2 = coordinator.attribute_and_classify_segment(
        lane=AuthorityLane.ANALYST,
        workspace_id=ws_id,
        segment_id=seg2.segment_id,
        semantic_role=SemanticRole.MECHANISM,
        epistemic_status=EvidenceEpistemicStatus.LIVED_EXPERIENCE,
        confidence_score=0.88,
        tension_ref="TEN-EXT-01",
    )
    assert ann2.semantic_role == "MECHANISM"

    # Step 3: COMPOSER Lane - Candidate Formation
    links = [
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
    ]

    candidate = coordinator.compose_content_candidate(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        candidate_type=CandidateType.STORY_CANDIDATE,
        title="Pivoting Under Extreme Crisis",
        hook_statement="How losing 80% of our clients saved our company culture.",
        narrative_completeness=NarrativeCompleteness.COMPLETE,
        evidence_links=links,
        emotional_resonance=0.85,
        cognitive_novelty=0.80,
        authority_evidence=0.90,
        narrative_velocity=0.75,
        story_arc="CRISIS_TO_TRANSFORMATION",
        tension_ref="TEN-EXT-01",
    )
    assert candidate.production_status == "DRAFT_CANDIDATE"
    assert candidate.is_synthetic is False
    assert len(candidate.evidence_links) == 2

    # Step 4: ANALYST Lane - Candidate Clustering
    scores = DimensionScores.calculate_composite(
        semantic_strength=0.90,
        guest_authenticity=0.95,
        audience_relevance=0.85,
        novelty=0.80,
        narrative_utility=0.75,
        visual_opportunity=0.70,
        editorial_completeness=0.85,
        distribution_potential=0.80,
    )
    eval_profile = CandidateEvaluationProfile(
        candidate_id=candidate.candidate_id,
        workspace_id=ws_id,
        scores=scores,
        gate_status=GateStatus.PASSED,
        is_eligible_for_board=True,
        provenance=EvaluatorProvenance(
            evaluator_id="EVAL-TEST-001",
            evaluator_version="1.0.0",
            rationale="High crisis stakes with authentic turnaround mechanism.",
        ),
    )
    clusters = coordinator.cluster_candidates(
        lane=AuthorityLane.ANALYST,
        workspace_id=ws_id,
        evaluations=[eval_profile],
        theme_map={"CRISIS_PIVOT": [candidate.candidate_id]},
    )
    assert len(clusters) == 1
    assert clusters[0].theme == "CRISIS_PIVOT"

    # Step 5: COMMANDER Lane - Candidate Portfolio Evaluation & Search
    portfolio_cand = {
        "candidate_id": candidate.candidate_id,
        "score_bps": 8350,
        "cost_units": 10,
        "evidence_links": candidate.evidence_links,
        "is_synthetic": False,
    }
    search_res = coordinator.evaluate_production_portfolio(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        candidates=[portfolio_cand],
        quality_threshold_bps=8000,
    )
    assert search_res["best_candidate_id"] == candidate.candidate_id
    assert len(search_res["candidates"]) == 1
    assert search_res["stop_reason"] == "QUALITY_THRESHOLD"

    # Step 6: COMMANDER Lane - Operator Selection Gate
    storyboard = coordinator.operator_select_candidate(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        operator_id="OPERATOR-JEAN-PIERRE",
        candidate_id=candidate.candidate_id,
        priority_rank=1,
        rationale="Compelling first-hand narrative with authentic stakes and transferable turnaround mechanism.",
        taste_delta="Framing approved for Format 01 Cinematic Story.",
    )
    assert storyboard.candidate_id == candidate.candidate_id
    assert storyboard.approved_by == "OPERATOR-JEAN-PIERRE"

    # Verify audit receipt
    receipts = store.list_decision_receipts(workspace_id=ws_id, candidate_id=candidate.candidate_id)
    assert len(receipts) == 1
    rec = receipts[0]
    assert rec.action_type == "SELECT"
    assert rec.is_synthetic_blocked is False
    assert len(rec.receipt_sha256) == 64


# ---------------------------------------------------------------------------
# Test 2: Synthetic-Proof Block (Fail-Closed & Rejection Receipts)
# ---------------------------------------------------------------------------

def test_synthetic_proof_block_rejects_synthetic_candidate(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
):
    ws_id = "WS-PROD-BETA"

    # Synthetic candidate marked is_synthetic=True
    synth_rec = ContentCandidateRecord(
        workspace_id=ws_id,
        candidate_id="CND-SYNTH-001",
        candidate_type="STORY_CANDIDATE",
        title="Synthetic AI Generated Concept",
        hook_statement="This was generated purely by a mock adapter.",
        narrative_completeness="COMPLETE",
        evidence_links=[{"segment_id": "MOCK-SEG", "text_sha256": "fake", "verbatim_text": "fake"}],
        cmf_score_bps={"composite_score_bps": 9000},
        production_status="DRAFT_CANDIDATE",
        is_synthetic=True,
    )
    store.insert_content_candidate(synth_rec)

    # Attempting to select this synthetic candidate for production MUST fail closed
    with pytest.raises(SyntheticCandidateProductionBlockedError) as exc_info:
        coordinator.operator_select_candidate(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            operator_id="OPERATOR-JEAN-PIERRE",
            candidate_id="CND-SYNTH-001",
            priority_rank=1,
            rationale="Trying to select synthetic concept.",
        )
    assert "Synthetic producer block" in str(exc_info.value)

    # Verify rejection receipt was recorded
    receipts = store.list_decision_receipts(workspace_id=ws_id, candidate_id="CND-SYNTH-001")
    assert len(receipts) == 1
    rec = receipts[0]
    assert rec.action_type == "SYNTHETIC_BLOCKED"
    assert rec.is_synthetic_blocked is True


def test_synthetic_proof_block_rejects_synthetic_payload_in_portfolio_search(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
):
    ws_id = "WS-PROD-GAMMA"

    synth_payload = {
        "candidate_id": "CND-SYNTH-002",
        "score_bps": 8500,
        "cost_units": 10,
        "production_authorized": False,  # Pipeline adapter flag
        "classification": "SYNTHETIC_DEVELOPMENT_EVIDENCE",
        "implementation_id": "cmf-pipeline.synthetic.compose",
        "evidence_links": [],
    }

    with pytest.raises(SyntheticCandidateProductionBlockedError):
        coordinator.evaluate_production_portfolio(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            candidates=[synth_payload],
        )


# ---------------------------------------------------------------------------
# Test 3: Ungrounded Candidate Rejection (Missing or Tampered Evidence)
# ---------------------------------------------------------------------------

def test_ungrounded_candidate_missing_links(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
):
    ws_id = "WS-PROD-DELTA"

    # Attempting to compose candidate without evidence links fails closed
    with pytest.raises(UngroundedCandidateError) as exc_info:
        coordinator.compose_content_candidate(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_id,
            candidate_type=CandidateType.STORY_CANDIDATE,
            title="Ungrounded Hallucination",
            hook_statement="No evidence backing this up.",
            narrative_completeness=NarrativeCompleteness.COMPLETE,
            evidence_links=[],
            emotional_resonance=0.9,
            cognitive_novelty=0.9,
            authority_evidence=0.9,
            narrative_velocity=0.9,
        )
    assert "must link to at least one authentic evidence segment" in str(exc_info.value)


def test_tampered_evidence_hash_rejection(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_interview_turns: List[Dict[str, Any]],
):
    ws_id = "WS-PROD-EPSILON"
    session_id = "SES-TAMPER-001"

    segments = coordinator.segment_interview_turns(
        lane=AuthorityLane.HUNTER,
        workspace_id=ws_id,
        session_id=session_id,
        raw_turns=real_interview_turns,
    )
    seg1 = segments[0]

    tampered_link = CandidateEvidenceLink(
        segment_id=seg1.segment_id,
        annotation_id="ANN-TAMPER-001",
        speaker=seg1.speaker,
        start_time_ms=seg1.start_time_ms,
        end_time_ms=seg1.end_time_ms,
        verbatim_text=seg1.verbatim_text,
        text_sha256="0000000000000000000000000000000000000000000000000000000000000000",  # tampered
    )

    with pytest.raises(UngroundedCandidateError) as exc_info:
        coordinator.compose_content_candidate(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_id,
            candidate_type=CandidateType.STORY_CANDIDATE,
            title="Tampered Evidence Candidate",
            hook_statement="Altered hash test",
            narrative_completeness=NarrativeCompleteness.COMPLETE,
            evidence_links=[tampered_link],
            emotional_resonance=0.8,
            cognitive_novelty=0.8,
            authority_evidence=0.8,
            narrative_velocity=0.8,
        )
    assert "SHA-256 mismatch" in str(exc_info.value)


# ---------------------------------------------------------------------------
# Test 4: Authority Lane Enforcement
# ---------------------------------------------------------------------------

def test_four_lane_authority_isolation(
    coordinator: EditorialDiscoveryProgramCoordinator,
    real_interview_turns: List[Dict[str, Any]],
):
    ws_id = "WS-PROD-ZETA"

    # Segmentation attempted by COMPOSER
    with pytest.raises(LaneAuthorityViolationError) as exc_info:
        coordinator.segment_interview_turns(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_id,
            session_id="SES-001",
            raw_turns=real_interview_turns,
        )
    assert "strictly requires 'HUNTER'" in str(exc_info.value)

    # Attribution attempted by HUNTER
    with pytest.raises(LaneAuthorityViolationError) as exc_info:
        coordinator.attribute_and_classify_segment(
            lane=AuthorityLane.HUNTER,
            workspace_id=ws_id,
            segment_id="SEG-001",
            semantic_role=SemanticRole.CLAIM,
            epistemic_status=EvidenceEpistemicStatus.LIVED_EXPERIENCE,
        )
    assert "strictly requires 'ANALYST'" in str(exc_info.value)

    # Composition attempted by ANALYST
    with pytest.raises(LaneAuthorityViolationError) as exc_info:
        coordinator.compose_content_candidate(
            lane=AuthorityLane.ANALYST,
            workspace_id=ws_id,
            candidate_type=CandidateType.STORY_CANDIDATE,
            title="Test",
            hook_statement="Test",
            narrative_completeness=NarrativeCompleteness.COMPLETE,
            evidence_links=[],
            emotional_resonance=0.5,
            cognitive_novelty=0.5,
            authority_evidence=0.5,
            narrative_velocity=0.5,
        )
    assert "strictly requires 'COMPOSER'" in str(exc_info.value)

    # Operator selection attempted by COMPOSER
    with pytest.raises(LaneAuthorityViolationError) as exc_info:
        coordinator.operator_select_candidate(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_id,
            operator_id="OP-1",
            candidate_id="CND-1",
            priority_rank=1,
            rationale="Valid rationale",
        )
    assert "strictly requires 'COMMANDER'" in str(exc_info.value)


# ---------------------------------------------------------------------------
# Test 5: Operator Actions (Reject, Modify Framing, Rationale Check)
# ---------------------------------------------------------------------------

def test_operator_rejection_and_rationale_enforcement(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_interview_turns: List[Dict[str, Any]],
):
    ws_id = "WS-PROD-ETA"
    session_id = "SES-REJECT-001"

    segments = coordinator.segment_interview_turns(
        lane=AuthorityLane.HUNTER,
        workspace_id=ws_id,
        session_id=session_id,
        raw_turns=real_interview_turns,
    )
    links = [
        CandidateEvidenceLink(
            segment_id=segments[0].segment_id,
            annotation_id="ANN-REJECT-001",
            speaker=segments[0].speaker,
            start_time_ms=segments[0].start_time_ms,
            end_time_ms=segments[0].end_time_ms,
            verbatim_text=segments[0].verbatim_text,
            text_sha256=segments[0].text_sha256,
        )
    ]
    cand = coordinator.compose_content_candidate(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        candidate_type=CandidateType.QUOTE_CANDIDATE,
        title="Candidate to Reject",
        hook_statement="Hook to reject",
        narrative_completeness=NarrativeCompleteness.COMPLETE,
        evidence_links=links,
        emotional_resonance=0.7,
        cognitive_novelty=0.7,
        authority_evidence=0.7,
        narrative_velocity=0.7,
    )

    # Rationale < 5 chars should fail
    with pytest.raises(Exception):
        coordinator.operator_reject_candidate(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            operator_id="OP-AUDREY",
            candidate_id=cand.candidate_id,
            rationale="No",
        )

    # Valid rejection
    receipt = coordinator.operator_reject_candidate(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        operator_id="OP-AUDREY",
        candidate_id=cand.candidate_id,
        rationale="Over-indexing on pandemic hardship; does not fit active audience context.",
        taste_delta="Prefer actionable operational pivots.",
    )
    assert receipt.action_type == "REJECT"
    assert receipt.taste_delta == "Prefer actionable operational pivots."


def test_operator_modify_framing_preserves_evidence_immutability(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_interview_turns: List[Dict[str, Any]],
):
    ws_id = "WS-PROD-THETA"
    session_id = "SES-MODIFY-001"

    segments = coordinator.segment_interview_turns(
        lane=AuthorityLane.HUNTER,
        workspace_id=ws_id,
        session_id=session_id,
        raw_turns=real_interview_turns,
    )
    links = [
        CandidateEvidenceLink(
            segment_id=segments[0].segment_id,
            annotation_id="ANN-MOD-001",
            speaker=segments[0].speaker,
            start_time_ms=segments[0].start_time_ms,
            end_time_ms=segments[0].end_time_ms,
            verbatim_text=segments[0].verbatim_text,
            text_sha256=segments[0].text_sha256,
        )
    ]
    cand = coordinator.compose_content_candidate(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        candidate_type=CandidateType.QUOTE_CANDIDATE,
        title="Initial Title",
        hook_statement="Initial Hook",
        narrative_completeness=NarrativeCompleteness.COMPLETE,
        evidence_links=links,
        emotional_resonance=0.8,
        cognitive_novelty=0.8,
        authority_evidence=0.8,
        narrative_velocity=0.8,
    )

    # Valid modification of title and hook while keeping evidence links unmodified
    mod_receipt = coordinator.operator_modify_framing(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        operator_id="OP-AUDREY",
        candidate_id=cand.candidate_id,
        new_title="Sharpened Crisis Pivot Title",
        new_hook="Sharpened Turnaround Hook Statement",
        modified_evidence_links=[l.model_dump() for l in links],
        rationale="Reframing hook for maximum emotional resonance.",
    )
    assert mod_receipt.action_type == "MODIFY"

    # Attempting to tamper with evidence text inside modified_evidence_links MUST fail
    tampered_links = [l.model_dump() for l in links]
    tampered_links[0]["verbatim_text"] = "Completely rewritten quote that guest never said."
    with pytest.raises(Exception) as exc_info:
        coordinator.operator_modify_framing(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            operator_id="OP-AUDREY",
            candidate_id=cand.candidate_id,
            new_title="Tampered Title",
            new_hook="Tampered Hook",
            modified_evidence_links=tampered_links,
            rationale="Attempting to rewrite evidence text.",
        )
    assert "evidence mutation detected" in str(exc_info.value).lower()


# ---------------------------------------------------------------------------
# Test 6: Multi-Tenant Workspace Isolation
# ---------------------------------------------------------------------------

def test_workspace_isolation(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_interview_turns: List[Dict[str, Any]],
):
    ws_a = "WS-TENANT-A"
    ws_b = "WS-TENANT-B"

    # Ingest in Workspace A
    segs_a = coordinator.segment_interview_turns(
        lane=AuthorityLane.HUNTER,
        workspace_id=ws_a,
        session_id="SES-A",
        raw_turns=real_interview_turns,
    )
    assert len(segs_a) == 2

    # Verify Workspace B cannot access Workspace A's segments
    segs_b = store.list_evidence_segments(workspace_id=ws_b)
    assert len(segs_b) == 0

    seg_lookup = store.get_evidence_segment(workspace_id=ws_b, segment_id=segs_a[0].segment_id)
    assert seg_lookup is None
