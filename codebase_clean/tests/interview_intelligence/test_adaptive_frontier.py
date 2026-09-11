"""
test_adaptive_frontier.py
-------------------------
Acceptance tests for CAE Mandate M06 — Adaptive Question Frontier.

Validates:
1. Deterministic next-question selection stability (AC-01).
2. Generic/abstract answer triggers DEEPEN specificity escalation (AC-02).
3. Contradiction observation triggers RECONCILE (AC-03).
4. Incomplete requirements coverage triggers BROADEN (AC-04).
5. Sufficient/verified evidence triggers ADVANCE and final CLOSE (AC-05).
6. Scripted/invalid candidates pruned from candidate pool (AC-06).
7. Operator locks enforced at runtime without override (AC-07).
8. Candidate pool bounded between 3 and 5 options (AC-08).
"""

import hashlib
import pytest
from datetime import datetime, timezone

from cae_interview_intelligence.adaptive_frontier import (
    AdaptiveAction,
    AdaptiveQuestionFrontierEngine,
    AnswerObservation,
    CoverageSpineItem,
    EvidenceRequirement,
    FrontierState,
    QuestionAttempt,
    RequirementStatus,
)
from cae_interview_intelligence.domain import QuestionStage
from cae_interview_intelligence.hypothesis_adapter import (
    CandidateState,
    CoordinateBasis,
    HypothesisCandidate,
    Provenance,
    SemanticRef,
)
from cae_interview_intelligence.question_resolver import (
    AnswerResolution,
    InformationCompleteness,
    QuestionCandidate,
)


def dummy_sha(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


def make_test_candidate(
    cid: str = "af_hyp_01",
    collision: str = "Traditional safety protocols mask executive complacency during system degradation.",
    locked: bool = False,
) -> HypothesisCandidate:
    return HypothesisCandidate(
        candidate_id=f"hc:{cid}",
        collision_statement=collision,
        state=CandidateState.LOCKED if locked else CandidateState.APPROVED,
        upstream_hypothesis_refs=[
            SemanticRef(
                object_id=f"air:hyp:{cid}",
                version="1.0.0",
                sha256=dummy_sha(f"air:hyp:{cid}"),
                object_type="activation_hypothesis",
            )
        ],
        coordinates=CoordinateBasis(
            d01_audience_tension="safety_guarantee_vs_actual_risk",
            d02_audience_belief="belief_in_checklists",
            d03_audience_desired_state="true_systemic_resilience",
            d04_guest_lived_authority="lead_safety_auditor",
            d05_guest_contradiction="compliance_signoff_vs_known_vulnerability",
            d06_guest_transformation="from_passive_auditor_to_whistleblower",
            d07_cultural_world_signal="sig:airline_near_miss_2026",
            d08_target_enemy_status_quo="checklist_theater",
            d09_oblique_lens="drift_into_failure",
            d10_archetype_opportunity="crucible_testimony",
            d11_distribution_condition="high_retention_provocation",
            d12_evidence_opportunity="internal_audit_paper_trail",
        ),
        desired_evidence=[
            "Exact audit timestamp when the exception was overridden",
            "Signed waiver demonstrating executive awareness",
        ],
        provenance=Provenance(
            source_refs=[SemanticRef(object_id="doc:faa_audit_log_01", sha256=dummy_sha("doc:faa_audit_log_01"))],
            generated_by="test-fixture:m06",
        ),
    )


# -----------------------------------------------------------------------------
# AC-01: Deterministic Next-Question Selection Stability
# -----------------------------------------------------------------------------

def test_deterministic_selection_stability():
    """Identical frontier state and observations produce identical rankings and selections."""
    engine = AdaptiveQuestionFrontierEngine()
    c1 = make_test_candidate("c1")
    c2 = make_test_candidate("c2", collision="Automated compliance audits produce brittle safety cultures.")

    f1 = engine.initialize_frontier(session_id="sess-det-1", candidates=[c1, c2])
    f2 = engine.initialize_frontier(session_id="sess-det-2", candidates=[c1, c2])

    attempt1 = engine.select_next_question(f1)
    attempt2 = engine.select_next_question(f2)

    assert attempt1.action == attempt2.action
    assert attempt1.selected_candidate.text == attempt2.selected_candidate.text
    assert attempt1.selected_candidate.question_id == attempt2.selected_candidate.question_id
    assert attempt1.scoring_breakdown == attempt2.scoring_breakdown


# -----------------------------------------------------------------------------
# AC-02: Generic / Abstract Answer Triggers DEEPEN Action
# -----------------------------------------------------------------------------

def test_generic_answer_triggers_deepen_action():
    """When a response is vague or generic slop, frontier triggers DEEPEN specificity escalation."""
    engine = AdaptiveQuestionFrontierEngine()
    cand = make_test_candidate("c_generic")
    frontier = engine.initialize_frontier(session_id="sess-deepen", candidates=[cand])

    # Turn 1: Initial question
    qa1 = engine.select_next_question(frontier)
    assert qa1.action == AdaptiveAction.ADVANCE

    # Answer 1: Abstract corporate slop
    engine.observe_answer(
        frontier,
        question_attempt_id=qa1.attempt_id,
        turn_id="t1",
        transcript_text="As a leader, we always prioritize safety and holistic stakeholder alignment across divisions.",
        resolution=AnswerResolution.ABSTRACT,
        completeness=InformationCompleteness.PARTIAL,
        specificity_score=0.25,
        authenticity_score=0.40,
    )

    # Next move must be DEEPEN
    action, rationale = engine.evaluate_next_action(frontier)
    assert action == AdaptiveAction.DEEPEN
    assert "escalating specificity" in rationale

    qa2 = engine.select_next_question(frontier)
    assert qa2.action == AdaptiveAction.DEEPEN
    assert qa2.selected_candidate.target_resolution == AnswerResolution.EPISODIC


# -----------------------------------------------------------------------------
# AC-03: Contradiction Observation Triggers RECONCILE
# -----------------------------------------------------------------------------

def test_contradiction_triggers_reconcile_action():
    """When an observed answer contradicts known facts, frontier triggers RECONCILE."""
    engine = AdaptiveQuestionFrontierEngine()
    cand = make_test_candidate("c_contra")
    frontier = engine.initialize_frontier(session_id="sess-reconcile", candidates=[cand])

    qa1 = engine.select_next_question(frontier)

    # Answer with contradiction
    engine.observe_answer(
        frontier,
        question_attempt_id=qa1.attempt_id,
        turn_id="t1",
        transcript_text="We had zero safety warnings prior to the incident, everything was 100% green.",
        resolution=AnswerResolution.SPECIFIC,
        completeness=InformationCompleteness.PARTIAL,
        has_contradiction=True,
        discrepancy_refs=[SemanticRef(object_id="doc:faa_audit_warning_01", sha256=dummy_sha("doc:faa_audit_01"))],
    )

    action, rationale = engine.evaluate_next_action(frontier)
    assert action == AdaptiveAction.RECONCILE
    assert "reconciling" in rationale

    qa2 = engine.select_next_question(frontier)
    assert qa2.action == AdaptiveAction.RECONCILE


# -----------------------------------------------------------------------------
# AC-04: Incomplete Requirements Coverage Triggers BROADEN
# -----------------------------------------------------------------------------

def test_incomplete_coverage_triggers_broaden_action():
    """When answer is partial and current milestone has unresolved requirements, frontier triggers BROADEN."""
    engine = AdaptiveQuestionFrontierEngine()
    cand = make_test_candidate("c_broaden")
    frontier = engine.initialize_frontier(session_id="sess-broaden", candidates=[cand])

    qa1 = engine.select_next_question(frontier)

    # Partial answer covering only 1 of 2 requirements
    engine.observe_answer(
        frontier,
        question_attempt_id=qa1.attempt_id,
        turn_id="t1",
        transcript_text="I remember the warning email came in on a Tuesday morning around 9:15 AM from our lead analyst.",
        resolution=AnswerResolution.SPECIFIC,
        completeness=InformationCompleteness.PARTIAL,
        has_contradiction=False,
        specificity_score=0.75,
    )

    action, rationale = engine.evaluate_next_action(frontier)
    assert action == AdaptiveAction.BROADEN
    assert "expanding breadth" in rationale

    qa2 = engine.select_next_question(frontier)
    assert qa2.action == AdaptiveAction.BROADEN


# -----------------------------------------------------------------------------
# AC-05: Sufficient / Verified Evidence Triggers ADVANCE and CLOSE
# -----------------------------------------------------------------------------

def test_sufficient_evidence_triggers_advance_and_close():
    """Sufficient evidence satisfies requirements, advances the spine, and closes at termination."""
    engine = AdaptiveQuestionFrontierEngine()
    c1 = make_test_candidate("c_sat1")
    c2 = make_test_candidate("c_sat2")
    frontier = engine.initialize_frontier(session_id="sess-advance", candidates=[c1, c2])

    # Step 1: Milestone 1
    qa1 = engine.select_next_question(frontier)
    assert frontier.spine_index == 0

    # Answer 1: Verified and sufficient
    engine.observe_answer(
        frontier,
        question_attempt_id=qa1.attempt_id,
        turn_id="t1",
        transcript_text="Here is the exact signed waiver from the COO approving the exception on Oct 14 at 16:32.",
        resolution=AnswerResolution.EVIDENTIAL,
        completeness=InformationCompleteness.VERIFIED,
        specificity_score=0.95,
        authenticity_score=0.95,
    )

    # Step 2: Advances to Milestone 2
    qa2 = engine.select_next_question(frontier)
    assert qa2.action == AdaptiveAction.ADVANCE
    assert frontier.spine_index == 1

    # Answer 2: Verified and sufficient
    engine.observe_answer(
        frontier,
        question_attempt_id=qa2.attempt_id,
        turn_id="t2",
        transcript_text="The post-mortem revealed that 3 other teams had silently bypassed the same audit check.",
        resolution=AnswerResolution.EVIDENTIAL,
        completeness=InformationCompleteness.VERIFIED,
        specificity_score=0.90,
    )

    # Step 3: All spine items satisfied -> CLOSE
    action, _ = engine.evaluate_next_action(frontier)
    assert action == AdaptiveAction.CLOSE

    qa3 = engine.select_next_question(frontier)
    assert qa3.action == AdaptiveAction.CLOSE
    assert frontier.is_terminal is True


# -----------------------------------------------------------------------------
# AC-06: Scripted / Invalid Candidates Pruned from Candidate Pool
# -----------------------------------------------------------------------------

def test_invalid_and_scripted_candidate_pruned():
    """Scripted or leading candidate prompts are pruned from the candidate pool."""
    engine = AdaptiveQuestionFrontierEngine()
    cand = make_test_candidate("c_prune")
    frontier = engine.initialize_frontier(session_id="sess-prune", candidates=[cand])

    # Inject an invalid scripted candidate manually into spine
    frontier.coverage_spine[0].primary_question.text = (
        "Don't you agree that management was completely negligent in ignoring the audit?"
    )

    # Pool assembly must discard the scripted question and provide valid non-scripted alternatives
    pool = engine.assemble_candidate_pool(frontier, AdaptiveAction.ADVANCE)
    for qc in pool:
        assert not qc.text.startswith("Don't you agree")
        assert len(qc.text) >= 15


# -----------------------------------------------------------------------------
# AC-07: Operator Locks Enforced at Runtime
# -----------------------------------------------------------------------------

def test_operator_locks_enforced_at_runtime():
    """Locked candidate questions are prioritized and cannot be overridden by adaptive routing."""
    engine = AdaptiveQuestionFrontierEngine()
    c_normal = make_test_candidate("c_norm")
    c_locked = make_test_candidate("c_locked", locked=True)

    frontier = engine.initialize_frontier(
        session_id="sess-lock",
        candidates=[c_normal, c_locked],
        locked_candidate_ids={"hc:c_locked"},
    )

    assert frontier.coverage_spine[1].is_locked is True

    # Advance to milestone 2
    frontier.spine_index = 1
    pool = engine.assemble_candidate_pool(frontier, AdaptiveAction.ADVANCE)
    assert pool[0].text == frontier.coverage_spine[1].primary_question.text


# -----------------------------------------------------------------------------
# AC-08: Candidate Pool Size Bounded Between 3 and 5 Options
# -----------------------------------------------------------------------------

def test_bounded_candidate_pool_size_limits():
    """Evaluated candidate pool size is strictly bounded: 3 <= len(pool) <= 5."""
    engine = AdaptiveQuestionFrontierEngine()
    cand = make_test_candidate("c_bound")
    frontier = engine.initialize_frontier(session_id="sess-bound", candidates=[cand])

    actions = [
        AdaptiveAction.DEEPEN,
        AdaptiveAction.BROADEN,
        AdaptiveAction.RECONCILE,
        AdaptiveAction.VERIFY,
        AdaptiveAction.ADVANCE,
        AdaptiveAction.CLOSE,
    ]

    for act in actions:
        pool = engine.assemble_candidate_pool(frontier, act)
        assert 3 <= len(pool) <= 5, f"Pool size {len(pool)} out of bounds for action {act}"
