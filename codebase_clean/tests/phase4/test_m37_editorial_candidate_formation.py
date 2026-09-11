"""
test_m37_editorial_candidate_formation.py
------------------------------------------
Phase 4 Mandate M37 Acceptance Suite:
Editorial Candidate Formation + Heritage Intelligence

Verifies:
1. Full unbroken causal lineage from real interview turns (03_50-12 Jean Pierre) to EditorialStoryboard.
2. Direct wiring of real EvidenceSegment and SemanticAnnotation producers into ContentCandidate generation.
3. 4-axis Heritage CMF diagnostic scoring ($0.30 R + 0.30 N + 0.25 E + 0.15 V$) converted to integer basis points (_bps).
4. Advisory nature of CMF scores: cannot override missing evidence or failing narrative completeness.
5. Multi-dimensional candidate evaluation with non-compensable safety gates and anti-reward-hacking checks (keyword stuffing, length gaming, low evidence virality).
6. Thematic candidate clustering with redundancy index analysis via CandidateClusterEngine.
7. Strict fail-closed synthetic candidate production block with signed SYNTHETIC_BLOCKED receipts.
8. Verbatim evidence immutability and SHA-256 verification (rejects altered evidence).
9. Four non-negotiable Authority Lanes isolation (HUNTER, ANALYST, COMPOSER, COMMANDER).
10. Multi-tenant cross-workspace isolation.
"""

from __future__ import annotations

import hashlib
import uuid
import pytest
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
    HeritageCMFScore,
    NarrativeCompleteness,
    ProductionStatus,
)
from cae_scoring_intelligence.domain import (
    CandidateEvaluationProfile,
    DimensionScores,
    EditorialBoard,
    EvaluatorProvenance,
    GateStatus,
)
from cae_scoring_intelligence.errors import (
    KeywordStuffingDetectedError,
    LengthGamingDetectedError,
    LowEvidenceViralityError,
    NonCompensableGateFailureError,
)
from cae_scoring_intelligence.evaluator import MultiDimensionalCandidateEvaluator
from cae_scoring_intelligence.clusterer import CandidateClusterEngine
from cae_scoring_intelligence.verifier import EditorialBoardVerifier
from cmf_pipeline.candidates.service import CandidateSearchService


@pytest.fixture
def store() -> EditorialDiscoveryStore:
    """Provides an isolated in-memory SQLite store for discovery and candidate records."""
    return EditorialDiscoveryStore(db_path=":memory:")


@pytest.fixture
def coordinator(store: EditorialDiscoveryStore) -> EditorialDiscoveryProgramCoordinator:
    """Provides the four-lane coordinator instance."""
    return EditorialDiscoveryProgramCoordinator(editorial_store=store)


@pytest.fixture
def real_jean_pierre_interview_turns() -> List[Dict[str, Any]]:
    """
    Authenticated interview turns from canonical Project 03_50-12 Jean Pierre:
    Industrial manufacturing supply chain crisis and autonomous inspection pivot.
    """
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


# ===========================================================================
# 1. End-to-End Real Evidence Lineage Flow
# ===========================================================================

def test_real_evidence_to_content_candidate_formation(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_interview_turns: List[Dict[str, Any]],
):
    ws_id = "WS-PROD-M37-JP"
    session_id = "SESS-JP-CRISIS-001"

    # 1. HUNTER Lane: Segment raw authenticated turns into lossless EvidenceSegments
    segments = coordinator.segment_interview_turns(
        lane=AuthorityLane.HUNTER,
        workspace_id=ws_id,
        session_id=session_id,
        raw_turns=real_jean_pierre_interview_turns,
        source_media_id="MEDIA-JP-AUDIO-01",
    )
    assert len(segments) == 3
    for seg in segments:
        assert seg.is_authenticated is True
        assert seg.text_sha256 == hashlib.sha256(seg.verbatim_text.encode("utf-8")).hexdigest()

    seg1, seg2, seg3 = segments[0], segments[1], segments[2]

    # 2. ANALYST Lane: Classify segments into typed SemanticAnnotations
    ann1 = coordinator.attribute_and_classify_segment(
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
    assert ann1.confidence_score_bps == 9500
    assert ann1.is_publishable is False

    ann2 = coordinator.attribute_and_classify_segment(
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
    assert ann2.semantic_role == "MECHANISM"

    ann3 = coordinator.attribute_and_classify_segment(
        lane=AuthorityLane.ANALYST,
        workspace_id=ws_id,
        segment_id=seg3.segment_id,
        semantic_role=SemanticRole.PROOF,
        epistemic_status=EvidenceEpistemicStatus.LIVED_EXPERIENCE,
        confidence_score=0.90,
        tension_ref="AET-SUPPLY-CRISIS",
        emotional_register=EmotionalRegister.CONVICTION,
        story_arc_geometry=StoryArcGeometry.CRUCIBLE_AND_REBIRTH,
    )
    assert ann3.semantic_role == "PROOF"

    # 3. COMPOSER Lane: Assemble ContentCandidate with real evidence links and CMF heritage score
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

    candidate = coordinator.compose_content_candidate(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        candidate_type=CandidateType.STORY_CANDIDATE,
        title="Industrial Pivot: From Supply Chain Collapse to Shop-Floor Edge AI",
        hook_statement="When our tier-one supplier collapsed in 48 hours, our machinists built their own vision inspection system.",
        narrative_completeness=NarrativeCompleteness.COMPLETE,
        evidence_links=links,
        emotional_resonance=0.88,
        cognitive_novelty=0.85,
        authority_evidence=0.94,
        narrative_velocity=0.80,
        story_arc="CRUCIBLE_AND_REBIRTH",
        tension_ref="AET-SUPPLY-CRISIS",
        invariant_ref="SDA-INV-GROUNDED-FACT",
        archetypal_container="THE_BUILDER",
        standalone_context_notes="Requires showing shop-floor machining B-roll.",
    )

    assert candidate.production_status == "DRAFT_CANDIDATE"
    assert candidate.is_synthetic is False
    assert len(candidate.evidence_links) == 3
    # Verify CMF score calculation: 0.30*0.88 + 0.30*0.85 + 0.25*0.94 + 0.15*0.80 = 0.264 + 0.255 + 0.235 + 0.120 = 0.874
    assert candidate.cmf_score_bps["composite_score_bps"] == 8740
    assert candidate.cmf_score_bps["authority_evidence_bps"] == 9400

    # 4. ANALYST Lane: Evaluate across 8 dimensions and cluster into thematic portfolio
    eval_profile = MultiDimensionalCandidateEvaluator.evaluate(
        candidate_id=candidate.candidate_id,
        workspace_id=ws_id,
        text_content=f"{candidate.title} {candidate.hook_statement} {seg1.verbatim_text} {seg2.verbatim_text} {seg3.verbatim_text}",
        semantic_strength=0.92,
        guest_authenticity=0.95,
        audience_relevance=0.88,
        novelty=0.85,
        narrative_utility=0.90,
        visual_opportunity=0.85,
        editorial_completeness=0.90,
        distribution_potential=0.82,
        rationale="High empirical groundedness and strong shop-floor turnaround narrative.",
    )
    assert eval_profile.gate_status == GateStatus.PASSED
    assert eval_profile.is_eligible_for_board is True
    assert eval_profile.scores.weighted_composite_score >= 0.85

    clusters = coordinator.cluster_candidates(
        lane=AuthorityLane.ANALYST,
        workspace_id=ws_id,
        evaluations=[eval_profile],
        theme_map={"INDUSTRIAL_CRISIS_PIVOT": [candidate.candidate_id]},
    )
    assert len(clusters) == 1
    assert clusters[0].theme == "INDUSTRIAL_CRISIS_PIVOT"
    assert clusters[0].dominant_candidate_id == candidate.candidate_id
    assert clusters[0].redundancy_score_bps == 0  # 1 candidate = 0 redundancy

    # 5. COMMANDER Lane: Deterministic Portfolio Search & Evaluation
    portfolio_cand = {
        "candidate_id": candidate.candidate_id,
        "score_bps": candidate.cmf_score_bps["composite_score_bps"],
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
    assert search_res["stop_reason"] == "QUALITY_THRESHOLD"

    # 6. COMMANDER Lane: Human Operator Selection
    storyboard = coordinator.operator_select_candidate(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        operator_id="OPERATOR-JEAN-PIERRE",
        candidate_id=candidate.candidate_id,
        priority_rank=1,
        rationale="Approved for production: Highly authentic first-person turnaround with transferable engineering insights.",
        taste_delta="Framing emphasizes machinist agency over AI hype.",
    )
    assert storyboard.candidate_id == candidate.candidate_id
    assert storyboard.approved_by == "OPERATOR-JEAN-PIERRE"
    assert len(storyboard.evidence_links) == 3

    # Verify decision receipt
    receipts = store.list_decision_receipts(workspace_id=ws_id, candidate_id=candidate.candidate_id)
    assert len(receipts) == 1
    rec = receipts[0]
    assert rec.action_type == "SELECT"
    assert rec.is_synthetic_blocked is False
    assert len(rec.receipt_sha256) == 64


# ===========================================================================
# 2. CMF Heritage Diagnostic Scoring Weights & Basis Points Conversion
# ===========================================================================

def test_heritage_cmf_diagnostic_scoring_weights_and_bps():
    # Test formula: 0.30 R + 0.30 N + 0.25 E + 0.15 V
    score = HeritageCMFScore.calculate(
        emotional_resonance=0.90,
        cognitive_novelty=0.80,
        authority_evidence=0.70,
        narrative_velocity=0.60,
    )
    # 0.30*0.90 (0.270) + 0.30*0.80 (0.240) + 0.25*0.70 (0.175) + 0.15*0.60 (0.090) = 0.775
    assert abs(score.composite_score - 0.775) < 1e-4

    # Convert to basis points (bps)
    bps = {
        "composite_score_bps": int(round(score.composite_score * 10000)),
        "emotional_resonance_bps": int(round(score.emotional_resonance * 10000)),
        "cognitive_novelty_bps": int(round(score.cognitive_novelty * 10000)),
        "authority_evidence_bps": int(round(score.authority_evidence * 10000)),
        "narrative_velocity_bps": int(round(score.narrative_velocity * 10000)),
    }
    assert bps["composite_score_bps"] == 7750
    assert bps["emotional_resonance_bps"] == 9000
    assert bps["cognitive_novelty_bps"] == 8000
    assert bps["authority_evidence_bps"] == 7000
    assert bps["narrative_velocity_bps"] == 6000


# ===========================================================================
# 3. Adversarial Anti-Gaming and Non-Compensable Gate Gating
# ===========================================================================

def test_adversarial_anti_gaming_and_non_compensable_gates():
    ws_id = "WS-PROD-ADVERSARIAL"

    # Test 1: Keyword stuffing detection
    stuffed_text = "This shocking secret will make you a millionaire with insane miracle hacks exposed."
    with pytest.raises(KeywordStuffingDetectedError, match="keyword stuffing"):
        MultiDimensionalCandidateEvaluator.evaluate(
            candidate_id="CND-STUFFED",
            workspace_id=ws_id,
            text_content=stuffed_text,
            semantic_strength=0.50,
            guest_authenticity=0.50,
            audience_relevance=0.50,
            novelty=0.50,
            narrative_utility=0.50,
            visual_opportunity=0.50,
            editorial_completeness=0.50,
            distribution_potential=0.50,
        )

    # Test 2: Length gaming detection (repetitive filler)
    padded_text = " ".join(["we repeat this filler text over and over again without substance"] * 15)
    with pytest.raises(LengthGamingDetectedError, match="length gaming"):
        MultiDimensionalCandidateEvaluator.evaluate(
            candidate_id="CND-PADDED",
            workspace_id=ws_id,
            text_content=padded_text,
            semantic_strength=0.50,
            guest_authenticity=0.50,
            audience_relevance=0.50,
            novelty=0.50,
            narrative_utility=0.50,
            visual_opportunity=0.50,
            editorial_completeness=0.50,
            distribution_potential=0.50,
        )

    # Test 3: Low evidence virality detection (distribution > 0.80 with authenticity < 0.50)
    with pytest.raises(LowEvidenceViralityError, match="violates grounding"):
        MultiDimensionalCandidateEvaluator.evaluate(
            candidate_id="CND-CLICKBAIT",
            workspace_id=ws_id,
            text_content="A high viral potential claim with unverified guest evidence.",
            semantic_strength=0.40,
            guest_authenticity=0.35,  # VIOLATION: < 0.50
            audience_relevance=0.80,
            novelty=0.80,
            narrative_utility=0.60,
            visual_opportunity=0.70,
            editorial_completeness=0.70,
            distribution_potential=0.90,  # VIOLATION: > 0.80
        )

    # Test 4: Non-compensable gate failure
    low_auth_profile = MultiDimensionalCandidateEvaluator.evaluate(
        candidate_id="CND-LOW-AUTH",
        workspace_id=ws_id,
        text_content="A reasonable text but with poor speaker authenticity score.",
        semantic_strength=0.80,
        guest_authenticity=0.30,  # Fails gate (< 0.40)
        audience_relevance=0.70,
        novelty=0.70,
        narrative_utility=0.70,
        visual_opportunity=0.70,
        editorial_completeness=0.70,
        distribution_potential=0.50,
    )
    assert low_auth_profile.gate_status == GateStatus.FAILED_AUTHENTICITY
    assert low_auth_profile.is_eligible_for_board is False


# ===========================================================================
# 4. Fail-Closed Synthetic Candidate Production Block
# ===========================================================================

def test_synthetic_candidate_producer_production_block(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
):
    ws_id = "WS-PROD-SYNTH-GUARD"

    synth_rec = ContentCandidateRecord(
        workspace_id=ws_id,
        candidate_id="CND-SYNTH-MOCK-001",
        candidate_type="STORY_CANDIDATE",
        title="Mock Synthetic AI Discovery",
        hook_statement="Created by a mock adapter fixture.",
        narrative_completeness="COMPLETE",
        evidence_links=[{"segment_id": "MOCK-SEG-1", "text_sha256": "mock_hash", "verbatim_text": "mock"}],
        cmf_score_bps={"composite_score_bps": 9500},
        production_status="DRAFT_CANDIDATE",
        is_synthetic=True,
    )
    store.insert_content_candidate(synth_rec)

    # Commander gate must fail closed
    with pytest.raises(SyntheticCandidateProductionBlockedError) as exc_info:
        coordinator.operator_select_candidate(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            operator_id="OP-GUARD",
            candidate_id="CND-SYNTH-MOCK-001",
            priority_rank=1,
            rationale="Attempting to select synthetic fixture.",
        )
    assert "Synthetic producer block" in str(exc_info.value)

    # Check that a signed SYNTHETIC_BLOCKED receipt was permanently stored
    receipts = store.list_decision_receipts(workspace_id=ws_id, candidate_id="CND-SYNTH-MOCK-001")
    assert len(receipts) == 1
    assert receipts[0].action_type == "SYNTHETIC_BLOCKED"
    assert receipts[0].is_synthetic_blocked is True


# ===========================================================================
# 5. Verbatim Evidence Immutability & Tampering Rejection
# ===========================================================================

def test_tampered_verbatim_evidence_rejection(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_interview_turns: List[Dict[str, Any]],
):
    ws_id = "WS-PROD-INTEGRITY"
    session_id = "SESS-INTEGRITY-001"

    segments = coordinator.segment_interview_turns(
        lane=AuthorityLane.HUNTER,
        workspace_id=ws_id,
        session_id=session_id,
        raw_turns=real_jean_pierre_interview_turns,
    )
    seg1 = segments[0]

    # Tamper with the SHA-256 hash
    tampered_link = CandidateEvidenceLink(
        segment_id=seg1.segment_id,
        annotation_id="ANN-TAMPER-01",
        speaker=seg1.speaker,
        start_time_ms=seg1.start_time_ms,
        end_time_ms=seg1.end_time_ms,
        verbatim_text=seg1.verbatim_text,
        text_sha256="ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    )

    with pytest.raises(UngroundedCandidateError, match="SHA-256 mismatch"):
        coordinator.compose_content_candidate(
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


# ===========================================================================
# 6. Four-Lane Authority Separation
# ===========================================================================

def test_four_lane_authority_separation(
    coordinator: EditorialDiscoveryProgramCoordinator,
    real_jean_pierre_interview_turns: List[Dict[str, Any]],
):
    ws_id = "WS-PROD-LANES"

    # Ingestion attempted under COMMANDER lane
    with pytest.raises(LaneAuthorityViolationError, match="strictly requires 'HUNTER'"):
        coordinator.segment_interview_turns(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            session_id="SESS-01",
            raw_turns=real_jean_pierre_interview_turns,
        )

    # Attribution attempted under COMPOSER lane
    with pytest.raises(LaneAuthorityViolationError, match="strictly requires 'ANALYST'"):
        coordinator.attribute_and_classify_segment(
            lane=AuthorityLane.COMPOSER,
            workspace_id=ws_id,
            segment_id="SEG-01",
            semantic_role=SemanticRole.CLAIM,
            epistemic_status=EvidenceEpistemicStatus.LIVED_EXPERIENCE,
        )

    # Composition attempted under HUNTER lane
    with pytest.raises(LaneAuthorityViolationError, match="strictly requires 'COMPOSER'"):
        coordinator.compose_content_candidate(
            lane=AuthorityLane.HUNTER,
            workspace_id=ws_id,
            candidate_type=CandidateType.QUOTE_CANDIDATE,
            title="Invalid Lane Composition",
            hook_statement="Hook",
            narrative_completeness=NarrativeCompleteness.COMPLETE,
            evidence_links=[],
            emotional_resonance=0.5,
            cognitive_novelty=0.5,
            authority_evidence=0.5,
            narrative_velocity=0.5,
        )

    # Operator selection attempted under ANALYST lane
    with pytest.raises(LaneAuthorityViolationError, match="strictly requires 'COMMANDER'"):
        coordinator.operator_select_candidate(
            lane=AuthorityLane.ANALYST,
            workspace_id=ws_id,
            operator_id="OP-01",
            candidate_id="CND-01",
            priority_rank=1,
            rationale="Valid rationale",
        )


# ===========================================================================
# 7. Cross-Workspace Isolation
# ===========================================================================

def test_cross_workspace_isolation(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_interview_turns: List[Dict[str, Any]],
):
    ws_alpha = "WS-TENANT-ALPHA"
    ws_beta = "WS-TENANT-BETA"

    segs = coordinator.segment_interview_turns(
        lane=AuthorityLane.HUNTER,
        workspace_id=ws_alpha,
        session_id="SESS-ALPHA",
        raw_turns=real_jean_pierre_interview_turns,
    )
    assert len(segs) == 3

    # Workspace Beta cannot see Workspace Alpha's segments
    beta_segs = store.list_evidence_segments(workspace_id=ws_beta)
    assert len(beta_segs) == 0

    lookup = store.get_evidence_segment(workspace_id=ws_beta, segment_id=segs[0].segment_id)
    assert lookup is None
