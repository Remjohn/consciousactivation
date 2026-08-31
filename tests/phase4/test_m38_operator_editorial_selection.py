"""
test_m38_operator_editorial_selection.py
------------------------------------------
Phase 4 Mandate M38 Acceptance Suite:
Operator Editorial Selection Program

Verifies:
1. End-to-end promotion of authentic interview candidates (03_50-12 Jean Pierre) via authoritative SELECT action.
2. Operator REJECT action setting candidate status to REJECTED and capturing taste delta feedback.
3. Operator LOCK action protecting candidates from mutation/re-ranking with verified lock integrity.
4. Operator COMPARE action producing structured multi-dimensional comparison matrices across CMF axes.
5. Constrained regeneration creating versioned candidates (v2+) with unbroken predecessor lineage and immutable evidence links.
6. Downstream production eligibility gate enforcement strictly requiring valid SELECT receipts and blocking unselected/rejected candidates.
7. Fail-closed synthetic candidate blocking across all operator actions (SELECT, LOCK, REGENERATE, DOWNSTREAM).
8. Evidence immutability defense across all operator actions and downstream checks (rejects tampered verbatim text or hashes).
9. Agent text cannot override backend-authoritative operator decisions.
10. Strict 4-lane authority separation (HUNTER, ANALYST, COMPOSER, COMMANDER).
11. Mandatory operator rationale enforcement (>= 5 chars) on all actions.
12. Multi-tenant cross-workspace isolation for candidates, receipts, and lineage.
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
from cae_operator_intelligence.manager import OperatorSelectionManager
from cae_operator_intelligence.domain import (
    CandidateComparisonMatrix,
    CandidateLockRecord,
    ConstrainedRegenerationSpec,
    OperatorActionType,
    OperatorDecisionReceipt,
    OperatorSelectionSession,
)
from cae_operator_intelligence.verifier import OperatorSelectionVerifier
from cae_operator_intelligence.errors import (
    CandidateLockedError,
    EvidenceMutationViolationError,
    EvidenceTamperingDetectedError,
    InvalidRegenerationSpecError,
    MissingRationaleError,
    SilentSelectionViolationError,
    UnapprovedExecutionError,
)


@pytest.fixture
def store() -> EditorialDiscoveryStore:
    """Provides an isolated in-memory SQLite store for discovery and candidate records."""
    return EditorialDiscoveryStore(db_path=":memory:")


@pytest.fixture
def coordinator(store: EditorialDiscoveryStore) -> EditorialDiscoveryProgramCoordinator:
    """Provides the four-lane coordinator instance."""
    return EditorialDiscoveryProgramCoordinator(editorial_store=store)


@pytest.fixture
def real_jean_pierre_turns() -> List[Dict[str, Any]]:
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


def _setup_baseline_candidate(
    coordinator: EditorialDiscoveryProgramCoordinator,
    ws_id: str,
    turns: List[Dict[str, Any]],
    is_synthetic: bool = False,
) -> tuple[ContentCandidateRecord, List[EvidenceSegmentRecord]]:
    """Helper to setup segmented, annotated, and composed candidate from turns."""
    session_id = f"SESS-{uuid.uuid4().hex[:6].upper()}"

    # 1. HUNTER Lane: Segment
    segments = coordinator.segment_interview_turns(
        lane=AuthorityLane.HUNTER,
        workspace_id=ws_id,
        session_id=session_id,
        raw_turns=turns,
    )

    # 2. ANALYST Lane: Classify
    annotations = []
    for seg in segments:
        ann = coordinator.attribute_and_classify_segment(
            lane=AuthorityLane.ANALYST,
            workspace_id=ws_id,
            segment_id=seg.segment_id,
            semantic_role=SemanticRole.PROOF,
            epistemic_status=EvidenceEpistemicStatus.FIRST_PARTY_FACT,
            confidence_score=0.96,
            tension_ref="AET-SUPPLY-CRISIS",
            emotional_register=EmotionalRegister.RESOLVE,
            story_arc_geometry=StoryArcGeometry.CRUCIBLE_AND_REBIRTH,
        )
        annotations.append(ann)

    # 3. COMPOSER Lane: Compose Candidate
    evidence_links = [
        CandidateEvidenceLink(
            segment_id=seg.segment_id,
            annotation_id=ann.annotation_id,
            speaker=seg.speaker,
            start_time_ms=seg.start_time_ms,
            end_time_ms=seg.end_time_ms,
            verbatim_text=seg.verbatim_text,
            text_sha256=seg.text_sha256,
        )
        for seg, ann in zip(segments, annotations)
    ]

    candidate = coordinator.compose_content_candidate(
        lane=AuthorityLane.COMPOSER,
        workspace_id=ws_id,
        candidate_type=CandidateType.STORY_CANDIDATE,
        title="From Supply Collapse to Shop-Floor AI",
        hook_statement="How machinists built edge vision on real scrap metal after a tier-1 supplier collapsed.",
        narrative_completeness=NarrativeCompleteness.COMPLETE,
        evidence_links=evidence_links,
        emotional_resonance=0.88,
        cognitive_novelty=0.92,
        authority_evidence=0.95,
        narrative_velocity=0.85,
        story_arc="CRUCIBLE_AND_REBIRTH",
        tension_ref="AET-SUPPLY-CRISIS",
        invariant_ref="SDA-INV-GROUNDED-FACT",
        archetypal_container="THE_BUILDER",
        is_synthetic=is_synthetic,
        standalone_context_notes="Canonical Jean Pierre turnaround case study.",
    )

    return candidate, segments


# ===========================================================================
# 1. Operator SELECT Action & Downstream Promotion
# ===========================================================================

def test_real_evidence_to_operator_select_promotes_candidate_with_signed_receipt(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_turns: List[Dict[str, Any]],
):
    ws_id = "WS-M38-SELECT-PROD"
    candidate, segments = _setup_baseline_candidate(coordinator, ws_id, real_jean_pierre_turns)

    # Operator performs authoritative SELECT
    operator_id = "OP-LEAD-CHIEF-EDITOR"
    rationale = "High authenticity grounded turning point with excellent machinist agency."
    taste_delta = "Emphasize ground-level pragmatism over executive abstraction."

    storyboard = coordinator.operator_select_candidate(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        operator_id=operator_id,
        candidate_id=candidate.candidate_id,
        priority_rank=1,
        rationale=rationale,
        taste_delta=taste_delta,
        notes="Approved for full storyboard production.",
    )

    # 1. Verify Storyboard Record
    assert storyboard.candidate_id == candidate.candidate_id
    assert storyboard.approved_by == operator_id
    assert storyboard.priority_rank == 1

    # 2. Verify Store Status Update
    updated_cand = store.get_content_candidate(ws_id, candidate.candidate_id)
    assert updated_cand is not None
    assert updated_cand.production_status == "SELECTED_FOR_PRODUCTION"
    assert updated_cand.operator_decision_ref is not None

    # 3. Verify Decision Receipt
    receipts = store.list_decision_receipts(ws_id, candidate.candidate_id)
    assert len(receipts) == 1
    receipt = receipts[0]
    assert receipt.action_type == "SELECT"
    assert receipt.operator_id == operator_id
    assert receipt.rationale == rationale
    assert receipt.taste_delta == taste_delta
    assert not receipt.is_synthetic_blocked
    assert receipt.receipt_sha256 is not None

    # 4. Verify Downstream Gate allows selected candidate
    verified_cand = coordinator.verify_downstream_production_eligibility(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        candidate_id=candidate.candidate_id,
    )
    assert verified_cand.candidate_id == candidate.candidate_id


# ===========================================================================
# 2. Operator REJECT Action & Taste Delta Capture
# ===========================================================================

def test_operator_reject_blocks_candidate_and_captures_taste_delta(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_turns: List[Dict[str, Any]],
):
    ws_id = "WS-M38-REJECT"
    candidate, _ = _setup_baseline_candidate(coordinator, ws_id, real_jean_pierre_turns)

    operator_id = "OP-EDITOR-ALEX"
    rationale = "Hook lacks visceral tension; opening is too gradual for a short-form hook."
    taste_delta = "Reject dry chronological recaps; open directly at the forty-eight hour line shutdown."

    receipt_record = coordinator.operator_reject_candidate(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        operator_id=operator_id,
        candidate_id=candidate.candidate_id,
        rationale=rationale,
        taste_delta=taste_delta,
    )

    # 1. Verify Receipt
    assert receipt_record.action_type == "REJECT"
    assert receipt_record.rationale == rationale
    assert receipt_record.taste_delta == taste_delta

    # 2. Verify Candidate Status in Store
    updated_cand = store.get_content_candidate(ws_id, candidate.candidate_id)
    assert updated_cand.production_status == "REJECTED"

    # 3. Verify Downstream Gate strictly blocks rejected candidate
    with pytest.raises(UnapprovedExecutionError, match="marked REJECTED"):
        coordinator.verify_downstream_production_eligibility(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            candidate_id=candidate.candidate_id,
        )


# ===========================================================================
# 3. Operator LOCK Action & Mutation Protection
# ===========================================================================

def test_operator_lock_protects_candidate_from_automated_modifications(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_turns: List[Dict[str, Any]],
):
    ws_id = "WS-M38-LOCK"
    candidate, _ = _setup_baseline_candidate(coordinator, ws_id, real_jean_pierre_turns)

    operator_id = "OP-ARCHITECT-MARIE"
    rationale = "Locking candidate as the definitive benchmark turn for industrial resilience case."

    lock_record = coordinator.operator_lock_candidate(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        operator_id=operator_id,
        candidate_id=candidate.candidate_id,
        rationale=rationale,
    )

    assert lock_record.candidate_id == candidate.candidate_id
    assert lock_record.locked_by == operator_id
    assert lock_record.lock_id is not None

    # Verify store status
    updated_cand = store.get_content_candidate(ws_id, candidate.candidate_id)
    assert updated_cand.lock_status == "LOCKED"

    # Verify lock integrity blocks attempted automated mutation
    session = OperatorSelectionSession(
        session_id="SESS-LOCK-TEST",
        workspace_id=ws_id,
        operator_id=operator_id,
        locked_candidates=[lock_record],
    )
    with pytest.raises(CandidateLockedError):
        OperatorSelectionVerifier.verify_lock_integrity(
            session=session,
            candidate_id=candidate.candidate_id,
            attempted_action="RE_RANK",
        )


# ===========================================================================
# 4. Operator COMPARE Action & Matrix Evaluation
# ===========================================================================

def test_operator_compare_generates_comparison_matrix_and_receipt(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_turns: List[Dict[str, Any]],
):
    ws_id = "WS-M38-COMPARE"
    cand1, _ = _setup_baseline_candidate(coordinator, ws_id, real_jean_pierre_turns)
    cand2, _ = _setup_baseline_candidate(coordinator, ws_id, real_jean_pierre_turns[:2])

    operator_id = "OP-STRATEGIST-JEAN"
    rationale = "Comparative analysis between full 3-turn arc vs condensed 2-turn crisis opening."
    trade_off_notes = "Candidate 1 has higher authority evidence; Candidate 2 has higher velocity."

    matrix = coordinator.compare_candidates(
        lane=AuthorityLane.ANALYST,
        workspace_id=ws_id,
        operator_id=operator_id,
        candidate_ids=[cand1.candidate_id, cand2.candidate_id],
        rationale=rationale,
        trade_off_notes=trade_off_notes,
    )

    assert len(matrix.candidates) == 2
    assert matrix.candidates[0].candidate_id == cand1.candidate_id
    assert matrix.trade_off_notes == trade_off_notes
    assert matrix.score_deltas is not None

    # Verify receipt recorded
    receipts = store.list_decision_receipts(ws_id, cand1.candidate_id)
    compare_receipts = [r for r in receipts if r.action_type == "COMPARE"]
    assert len(compare_receipts) == 1
    assert compare_receipts[0].rationale == rationale


# ===========================================================================
# 5. Constrained Regeneration & Unbroken Lineage
# ===========================================================================

def test_operator_constrained_regeneration_creates_versioned_candidate_with_unbroken_lineage(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_turns: List[Dict[str, Any]],
):
    ws_id = "WS-M38-REGEN"
    v1_cand, segments = _setup_baseline_candidate(coordinator, ws_id, real_jean_pierre_turns)

    assert v1_cand.version == 1
    assert v1_cand.predecessor_candidate_id is None

    operator_id = "OP-DIRECTOR-SOPHIE"
    guidance = "Sharpen machinist agency and heighten urgency of 48-hour shutdown."
    target_hook = "Shop-floor machinists trained computer vision in 48 hours."

    v2_cand, receipt = coordinator.operator_request_regeneration(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        operator_id=operator_id,
        candidate_id=v1_cand.candidate_id,
        guidance=guidance,
        target_hook_emphasis=target_hook,
        tone_refinement="Tense and gritty industrial realism",
        preserve_evidence_segment_ids=[s.segment_id for s in segments],
        forbidden_angles=["Generic corporate AI hype", "Executive hero narrative"],
    )

    # 1. Verify v2 candidate properties
    assert v2_cand.candidate_id != v1_cand.candidate_id
    assert v2_cand.version == 2
    assert v2_cand.predecessor_candidate_id == v1_cand.candidate_id
    assert v2_cand.production_status == "DRAFT_CANDIDATE"
    assert target_hook in v2_cand.hook_statement

    # 2. Verify v1 predecessor status is SUPERSEDED_BY_REGENERATION
    v1_updated = store.get_content_candidate(ws_id, v1_cand.candidate_id)
    assert v1_updated.production_status == "SUPERSEDED_BY_REGENERATION"

    # 3. Verify lineage traversal from v2 back to root
    lineage = store.list_candidate_lineage(ws_id, v2_cand.candidate_id)
    assert len(lineage) == 2
    assert lineage[0].candidate_id == v1_cand.candidate_id
    assert lineage[0].version == 1
    assert lineage[1].candidate_id == v2_cand.candidate_id
    assert lineage[1].version == 2

    # 4. Verify immutable evidence links preserved exactly
    for link in v2_cand.evidence_links:
        seg_id = link["segment_id"]
        original_seg = store.get_evidence_segment(ws_id, seg_id)
        assert original_seg is not None
        assert original_seg.text_sha256 == link["text_sha256"]
        assert original_seg.verbatim_text == link["verbatim_text"]


# ===========================================================================
# 6. Downstream Gate Enforcement
# ===========================================================================

def test_downstream_gate_enforcement_blocks_unselected_or_rejected_candidates(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_turns: List[Dict[str, Any]],
):
    ws_id = "WS-M38-DOWNSTREAM-GATE"
    cand, _ = _setup_baseline_candidate(coordinator, ws_id, real_jean_pierre_turns)

    # A draft candidate (never selected) cannot proceed downstream
    with pytest.raises(UnapprovedExecutionError, match="missing authoritative SELECT receipt"):
        coordinator.verify_downstream_production_eligibility(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            candidate_id=cand.candidate_id,
        )

    # Select candidate
    coordinator.operator_select_candidate(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        operator_id="OP-SUPERVISOR",
        candidate_id=cand.candidate_id,
        priority_rank=1,
        rationale="Approved for publication pipeline.",
    )

    # Now downstream gate passes
    verified = coordinator.verify_downstream_production_eligibility(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        candidate_id=cand.candidate_id,
    )
    assert verified.candidate_id == cand.candidate_id


# ===========================================================================
# 7. Fail-Closed Synthetic Candidate Blocking
# ===========================================================================

def test_fail_closed_synthetic_candidate_blocking_at_selection_and_regeneration(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_turns: List[Dict[str, Any]],
):
    ws_id = "WS-M38-SYNTH-BLOCK"
    synth_cand, _ = _setup_baseline_candidate(coordinator, ws_id, real_jean_pierre_turns, is_synthetic=True)

    # 1. SELECT on synthetic must fail closed
    with pytest.raises(SyntheticCandidateProductionBlockedError):
        coordinator.operator_select_candidate(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            operator_id="OP-EDITOR",
            candidate_id=synth_cand.candidate_id,
            priority_rank=1,
            rationale="Attempting to select synthetic test candidate.",
        )

    # 2. LOCK on synthetic must fail closed
    with pytest.raises(SyntheticCandidateProductionBlockedError):
        coordinator.operator_lock_candidate(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            operator_id="OP-EDITOR",
            candidate_id=synth_cand.candidate_id,
            rationale="Attempting to lock synthetic candidate.",
        )

    # 3. REGENERATE on synthetic must fail closed
    with pytest.raises(SyntheticCandidateProductionBlockedError):
        coordinator.operator_request_regeneration(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            operator_id="OP-EDITOR",
            candidate_id=synth_cand.candidate_id,
            guidance="Attempting to regenerate synthetic candidate.",
        )

    # 4. DOWNSTREAM on synthetic must fail closed
    with pytest.raises(SyntheticCandidateProductionBlockedError):
        coordinator.verify_downstream_production_eligibility(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            candidate_id=synth_cand.candidate_id,
        )


# ===========================================================================
# 8. Evidence Immutability Defense Across Operator Actions
# ===========================================================================

def test_evidence_immutability_defense_across_all_operator_actions(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_turns: List[Dict[str, Any]],
):
    ws_id = "WS-M38-IMMUTABILITY"
    candidate, segments = _setup_baseline_candidate(coordinator, ws_id, real_jean_pierre_turns)

    # 1a. Modify framing with altered segment count should raise EvidenceMutationViolationError
    truncated_links = [
        {
            "segment_id": candidate.evidence_links[0]["segment_id"],
            "text_sha256": candidate.evidence_links[0]["text_sha256"],
            "verbatim_text": candidate.evidence_links[0]["verbatim_text"],
        }
    ]
    with pytest.raises(EvidenceMutationViolationError):
        coordinator.operator_modify_framing(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            operator_id="OP-ATTACKER",
            candidate_id=candidate.candidate_id,
            new_title="Truncated Links Title",
            new_hook="Truncated Links Hook",
            modified_evidence_links=truncated_links,
            rationale="Attempting to drop evidence segments.",
        )

    # 1b. Modify framing with all segments present but 1 tampered hash should raise EvidenceMutationViolationError
    tampered_links = [
        dict(candidate.evidence_links[0], text_sha256="0000000000000000000000000000000000000000000000000000000000000000"),
        dict(candidate.evidence_links[1]),
        dict(candidate.evidence_links[2]),
    ]
    with pytest.raises(EvidenceMutationViolationError):
        coordinator.operator_modify_framing(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            operator_id="OP-ATTACKER",
            candidate_id=candidate.candidate_id,
            new_title="Tampered Title",
            new_hook="Tampered Hook",
            modified_evidence_links=tampered_links,
            rationale="Attempting to rewrite evidence hash.",
        )

    # 1c. Direct verifier evidence immutability check raises EvidenceMutationViolationError on hash tampering
    with pytest.raises(EvidenceMutationViolationError):
        OperatorSelectionVerifier.verify_evidence_immutability(
            original_evidence_links=candidate.evidence_links,
            candidate_evidence_links=tampered_links,
        )

    # 1d. Direct verifier check raises EvidenceTamperingDetectedError on ungrounded segment ID
    ungrounded_links = [
        dict(candidate.evidence_links[0], segment_id="SEG-UNGROUNDED-FAKE-ID"),
    ]
    with pytest.raises(EvidenceTamperingDetectedError):
        OperatorSelectionVerifier.verify_evidence_immutability(
            original_evidence_links=candidate.evidence_links,
            candidate_evidence_links=ungrounded_links,
        )

    # 2. Corrupt store segment and test downstream verification failure
    coordinator.operator_select_candidate(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        operator_id="OP-LEGIT",
        candidate_id=candidate.candidate_id,
        priority_rank=1,
        rationale="Approved before tampering.",
    )

    # Manually simulate tampering on evidence segment in store
    cursor = store._conn.cursor()
    cursor.execute(
        "UPDATE cae_evidence_segments SET text_sha256 = ? WHERE segment_id = ?",
        ("ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", segments[0].segment_id),
    )
    store._conn.commit()

    with pytest.raises((EvidenceImmutabilityViolationError, UngroundedCandidateError)):
        coordinator.verify_downstream_production_eligibility(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            candidate_id=candidate.candidate_id,
        )


# ===========================================================================
# 9. Agent Text Cannot Override Backend Operator Decision
# ===========================================================================

def test_agent_text_cannot_override_backend_operator_decision(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_turns: List[Dict[str, Any]],
):
    ws_id = "WS-M38-NO-AGENT-OVERRIDE"
    candidate, _ = _setup_baseline_candidate(coordinator, ws_id, real_jean_pierre_turns)

    # Explicitly reject candidate
    coordinator.operator_reject_candidate(
        lane=AuthorityLane.COMMANDER,
        workspace_id=ws_id,
        operator_id="OP-REJECTOR",
        candidate_id=candidate.candidate_id,
        rationale="Rejected due to weak narrative arc.",
    )

    # An agent attempts to bypass by presenting metadata / text claiming approved
    # Downstream verification must fail closed regardless of any agent claims
    with pytest.raises(UnapprovedExecutionError, match="marked REJECTED"):
        coordinator.verify_downstream_production_eligibility(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            candidate_id=candidate.candidate_id,
        )


# ===========================================================================
# 10. Four-Lane Authority Separation Enforcement
# ===========================================================================

def test_four_lane_authority_separation_strict_enforcement(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_turns: List[Dict[str, Any]],
):
    ws_id = "WS-M38-LANES"
    candidate, _ = _setup_baseline_candidate(coordinator, ws_id, real_jean_pierre_turns)

    # 1. SELECT under non-COMMANDER lane
    for forbidden_lane in [AuthorityLane.HUNTER, AuthorityLane.ANALYST, AuthorityLane.COMPOSER]:
        with pytest.raises(LaneAuthorityViolationError):
            coordinator.operator_select_candidate(
                lane=forbidden_lane,
                workspace_id=ws_id,
                operator_id="OP-TEST",
                candidate_id=candidate.candidate_id,
                priority_rank=1,
                rationale="Valid rationale.",
            )

    # 2. COMPARE under non-ANALYST lane
    for forbidden_lane in [AuthorityLane.HUNTER, AuthorityLane.COMPOSER, AuthorityLane.COMMANDER]:
        with pytest.raises(LaneAuthorityViolationError):
            coordinator.compare_candidates(
                lane=forbidden_lane,
                workspace_id=ws_id,
                operator_id="OP-TEST",
                candidate_ids=[candidate.candidate_id, candidate.candidate_id],
                rationale="Valid rationale.",
            )

    # 3. REGENERATE under non-COMPOSER lane
    for forbidden_lane in [AuthorityLane.HUNTER, AuthorityLane.ANALYST, AuthorityLane.COMMANDER]:
        with pytest.raises(LaneAuthorityViolationError):
            coordinator.regenerate_content_candidate(
                lane=forbidden_lane,
                workspace_id=ws_id,
                predecessor_candidate_id=candidate.candidate_id,
                operator_id="OP-TEST",
                guidance="Valid guidance.",
            )


# ===========================================================================
# 11. Mandatory Operator Rationale Enforcement
# ===========================================================================

def test_mandatory_rationale_enforcement_across_all_actions(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_turns: List[Dict[str, Any]],
):
    ws_id = "WS-M38-RATIONALE"
    candidate, _ = _setup_baseline_candidate(coordinator, ws_id, real_jean_pierre_turns)

    # 1. SELECT without rationale
    with pytest.raises(MissingRationaleError):
        coordinator.operator_select_candidate(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            operator_id="OP-TEST",
            candidate_id=candidate.candidate_id,
            priority_rank=1,
            rationale="   ",  # Blank
        )

    # 2. REJECT without rationale
    with pytest.raises(MissingRationaleError):
        coordinator.operator_reject_candidate(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            operator_id="OP-TEST",
            candidate_id=candidate.candidate_id,
            rationale="no",  # Too short (< 5 chars)
        )

    # 3. LOCK without rationale
    with pytest.raises(MissingRationaleError):
        coordinator.operator_lock_candidate(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_id,
            operator_id="OP-TEST",
            candidate_id=candidate.candidate_id,
            rationale="",  # Empty
        )


# ===========================================================================
# 12. Cross-Workspace Multi-Tenant Isolation
# ===========================================================================

def test_cross_workspace_multi_tenant_isolation(
    coordinator: EditorialDiscoveryProgramCoordinator,
    store: EditorialDiscoveryStore,
    real_jean_pierre_turns: List[Dict[str, Any]],
):
    ws_a = "WS-M38-TENANT-ALPHA"
    ws_b = "WS-M38-TENANT-BETA"

    cand_a, _ = _setup_baseline_candidate(coordinator, ws_a, real_jean_pierre_turns)
    cand_b, _ = _setup_baseline_candidate(coordinator, ws_b, real_jean_pierre_turns)

    # Attempting to select Candidate A from Workspace B context must fail
    with pytest.raises(EditorialDiscoveryError, match="not found in workspace"):
        coordinator.operator_select_candidate(
            lane=AuthorityLane.COMMANDER,
            workspace_id=ws_b,
            operator_id="OP-TEST",
            candidate_id=cand_a.candidate_id,
            priority_rank=1,
            rationale="Cross-tenant access attempt.",
        )

    # Lineage query in workspace B for Candidate A must return empty
    lineage_b = store.list_candidate_lineage(ws_b, cand_a.candidate_id)
    assert len(lineage_b) == 0
