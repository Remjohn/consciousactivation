"""
test_semantic_acquisition.py
----------------------------
Acceptance tests for CAE Mandate M07 — Semantic Acquisition Observation.

Validates:
1. Receipt existence alone does not authenticate evidence (AC-01, FR-IP-007).
2. System inference is never serialized or conflated with Guest facts (AC-02, FR-IP-007).
3. Completeness mutation preserves upstream hypothesis identity (AC-03, FR-IP-006).
4. Contradiction is recorded as discrepancy before reconciliation (AC-04).
5. Observation directly drives differential next-question actions (AC-05, FR-IP-005/006).
6. Guest-validated interpretation promotes inference while retaining lineage (AC-06).
7. Observation conforms to derived schema and non-canonical boundary (AC-07).
"""

import hashlib
import pytest
from datetime import datetime, timezone

from conscious_activations_interview_composer.errors import ValidationError

from cae_interview_intelligence.adaptive_frontier import (
    AdaptiveAction,
    AdaptiveQuestionFrontierEngine,
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
    EvidenceMode,
    InformationCompleteness,
    SocialReferenceFrame,
    TemporalOrientation,
)
from cae_interview_intelligence.semantic_acquisition import (
    AcquisitionEvidenceRecord,
    DiscrepancyRecord,
    EvidenceLineageKind,
    SemanticAcquisitionObservation,
    SemanticAcquisitionObserver,
)


def dummy_sha(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


def make_test_candidate(cid: str = "sa_hyp_01") -> HypothesisCandidate:
    return HypothesisCandidate(
        candidate_id=f"hc:{cid}",
        collision_statement="Routine maintenance waivers create hidden operational debt in flight operations.",
        state=CandidateState.APPROVED,
        upstream_hypothesis_refs=[
            SemanticRef(
                object_id=f"air:hyp:{cid}",
                version="1.0.0",
                sha256=dummy_sha(f"air:hyp:{cid}"),
                object_type="activation_hypothesis",
            )
        ],
        coordinates=CoordinateBasis(
            d01_audience_tension="safety_reputation_vs_hidden_waivers",
            d02_audience_belief="airline_checklists_catch_everything",
            d03_audience_desired_state="zero_tolerance_maintenance_integrity",
            d04_guest_lived_authority="chief_avionics_inspector",
            d05_guest_contradiction="maintenance_signoff_vs_known_avionics_glitch",
            d06_guest_transformation="from_corporate_compliance_officer_to_advocate",
            d07_cultural_world_signal="sig:faa_oversight_crackdown_2026",
            d08_target_enemy_status_quo="waiver_inflation",
            d09_oblique_lens="accumulated_operational_debt",
            d10_archetype_opportunity="crucible_testimony",
            d11_distribution_condition="high_impact_investigative",
            d12_evidence_opportunity="avionics_maintenance_waiver_log",
        ),
        desired_evidence=[
            "Exact avionics waiver approval timestamp",
            "Signed signoff log by flight ops director",
        ],
        provenance=Provenance(
            source_refs=[SemanticRef(object_id="doc:maint_log_001", sha256=dummy_sha("doc:maint_log_001"))],
            generated_by="test-fixture:m07",
        ),
    )


# -----------------------------------------------------------------------------
# AC-01: Receipt Existence Alone Does Not Authenticate Evidence
# -----------------------------------------------------------------------------

def test_receipt_existence_alone_does_not_authenticate_evidence():
    """Presence of an API receipt or 200 OK cannot mark evidence as authenticated."""
    source_ref = SemanticRef(object_id="turn_resp:turn_101", object_type="interview_turn_response")

    # Attempting to authenticate via unauthenticated_receipt must raise validation error
    with pytest.raises(ValueError, match="Receipt existence alone cannot authenticate evidence"):
        AcquisitionEvidenceRecord(
            kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
            turn_id="turn_101",
            statement_text="I saw the warning signal on the console.",
            source_ref=source_ref,
            is_authenticated=True,
            authentication_method="unauthenticated_receipt",
        )

    # Valid authenticated record using direct spoken testimony
    valid_record = AcquisitionEvidenceRecord(
        kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
        turn_id="turn_101",
        statement_text="I saw the warning signal on the console.",
        source_ref=source_ref,
        is_authenticated=True,
        authentication_method="direct_spoken_testimony",
    )
    assert valid_record.is_authenticated is True


# -----------------------------------------------------------------------------
# AC-02: System Inference Is Not Serialized as Guest Fact
# -----------------------------------------------------------------------------

def test_system_inference_not_serialized_as_guest_fact():
    """System inferences must remain separate and cannot be marked as authenticated guest facts."""
    observer = SemanticAcquisitionObserver()

    # Attempting to construct an observation where system inference is marked as authenticated must fail
    source_ref = SemanticRef(object_id="turn_resp:turn_102", object_type="interview_turn_response")
    with pytest.raises(ValueError, match="System inference cannot be marked as authenticated guest evidence"):
        AcquisitionEvidenceRecord(
            kind=EvidenceLineageKind.SYSTEM_INFERENCE,
            turn_id="turn_102",
            statement_text="Guest likely experienced executive intimidation during waiver signing.",
            source_ref=source_ref,
            is_authenticated=True,
            authentication_method=None,
        )

    # Observer creates clear separation between guest statements and system inferences
    obs = observer.observe_turn_response(
        question_attempt_id="qa:attempt_01",
        turn_id="turn_102",
        transcript_text="The ops director walked in and demanded the signed waiver before 5 PM.",
        guest_statements=["The ops director demanded the signed waiver before 5 PM."],
        inferred_statements=["High degree of hierarchical pressure exhibited during signing."],
    )

    assert len(obs.guest_stated_evidence_refs) == 1
    assert len(obs.system_inference_refs) == 1

    guest_rec = obs.evidence_records[0]
    inf_rec = obs.evidence_records[1]

    assert guest_rec.kind == EvidenceLineageKind.GUEST_STATED_EVIDENCE
    assert guest_rec.is_authenticated is True

    assert inf_rec.kind == EvidenceLineageKind.SYSTEM_INFERENCE
    assert inf_rec.is_authenticated is False


# -----------------------------------------------------------------------------
# AC-03: Completeness Mutation Preserves Upstream Hypothesis Identity
# -----------------------------------------------------------------------------

def test_completeness_mutation_preserves_hypothesis_identity():
    """An answer can change completeness without altering or mutating upstream hypothesis identity."""
    cand = make_test_candidate("c_immut")
    orig_hyp_ref = cand.upstream_hypothesis_refs[0]
    orig_id = orig_hyp_ref.object_id
    orig_version = orig_hyp_ref.version
    orig_sha = orig_hyp_ref.sha256

    observer = SemanticAcquisitionObserver()

    # Observation 1: Partial resolution
    obs1 = observer.observe_turn_response(
        question_attempt_id="qa:att_1",
        turn_id="t1",
        transcript_text="We had several waiver discussions in Q3.",
        resolution=AnswerResolution.SPECIFIC,
        completeness=InformationCompleteness.PARTIAL,
        hypothesis_refs=[orig_hyp_ref],
    )

    # Observation 2: Verified resolution
    obs2 = observer.observe_turn_response(
        question_attempt_id="qa:att_2",
        turn_id="t2",
        transcript_text="Here is waiver #8849 signed on August 12 by Director Vance.",
        resolution=AnswerResolution.EVIDENTIAL,
        completeness=InformationCompleteness.VERIFIED,
        hypothesis_refs=[orig_hyp_ref],
    )

    assert obs1.completeness == InformationCompleteness.PARTIAL
    assert obs2.completeness == InformationCompleteness.VERIFIED

    # Invariant: Upstream hypothesis reference must remain identical and unmodified
    for obs in (obs1, obs2):
        assert obs.provenance.source_refs[0].object_id == orig_id
        assert obs.provenance.source_refs[0].version == orig_version
        assert obs.provenance.source_refs[0].sha256 == orig_sha


# -----------------------------------------------------------------------------
# AC-04: Contradiction Recorded as Discrepancy Before Reconciliation
# -----------------------------------------------------------------------------

def test_contradiction_recorded_as_discrepancy_before_reconciliation():
    """Contradiction must be recorded as DiscrepancyRecord before triggering reconciliation action."""
    observer = SemanticAcquisitionObserver()

    prior_ref = SemanticRef(object_id="doc:annual_safety_report_2025", sha256=dummy_sha("doc:safety_rep"))
    observed_ref = SemanticRef(object_id="turn_resp:t3", object_type="interview_turn_response")

    disc = DiscrepancyRecord(
        prior_claim_or_doc_ref=prior_ref,
        observed_claim_ref=observed_ref,
        nature_of_contradiction="Annual report claimed zero maintenance waivers; Guest testified to 14 signed waivers.",
        turn_id="t3",
    )

    obs = observer.observe_turn_response(
        question_attempt_id="qa:att_3",
        turn_id="t3",
        transcript_text="Actually, we signed 14 waivers that quarter despite the report saying zero.",
        resolution=AnswerResolution.SPECIFIC,
        completeness=InformationCompleteness.PARTIAL,
        discrepancies=[disc],
    )

    assert obs.has_contradiction is True
    assert len(obs.discrepancies) == 1
    assert obs.discrepancies[0].is_reconciled is False
    assert len(obs.discrepancy_refs) == 1
    assert obs.discrepancy_refs[0].object_id == disc.discrepancy_id


# -----------------------------------------------------------------------------
# AC-05: Observation Drives Differential Next-Question Routing
# -----------------------------------------------------------------------------

def test_observation_drives_differential_next_question_routing():
    """Different observation states (slop, contradiction, partial, verified) trigger distinct adaptive actions."""
    engine = AdaptiveQuestionFrontierEngine()
    cand1 = make_test_candidate("c_routing_1")
    cand2 = make_test_candidate("c_routing_2")
    frontier = engine.initialize_frontier(session_id="sess-routing", candidates=[cand1, cand2])

    qa = engine.select_next_question(frontier)

    # 1. Generic slop triggers DEEPEN
    obs_slop = engine.observe_answer(
        frontier,
        question_attempt_id=qa.attempt_id,
        turn_id="t1",
        transcript_text="Safety is really important in everything we do.",
        resolution=AnswerResolution.ABSTRACT,
        completeness=InformationCompleteness.PARTIAL,
        specificity_score=0.20,
    )
    act1, _ = engine.evaluate_next_action(frontier)
    assert act1 == AdaptiveAction.DEEPEN

    # 2. Contradiction triggers RECONCILE
    frontier.history_observations.clear()
    obs_contra = engine.observe_answer(
        frontier,
        question_attempt_id=qa.attempt_id,
        turn_id="t2",
        transcript_text="I never saw any waivers.",
        resolution=AnswerResolution.SPECIFIC,
        completeness=InformationCompleteness.PARTIAL,
        has_contradiction=True,
    )
    act2, _ = engine.evaluate_next_action(frontier)
    assert act2 == AdaptiveAction.RECONCILE

    # 3. Partial coverage triggers BROADEN
    frontier.history_observations.clear()
    obs_partial = engine.observe_answer(
        frontier,
        question_attempt_id=qa.attempt_id,
        turn_id="t3",
        transcript_text="I remember waiver #8849 specifically.",
        resolution=AnswerResolution.SPECIFIC,
        completeness=InformationCompleteness.PARTIAL,
        has_contradiction=False,
        specificity_score=0.85,
    )
    act3, _ = engine.evaluate_next_action(frontier)
    assert act3 == AdaptiveAction.BROADEN

    # 4. Verified evidence triggers ADVANCE
    frontier.history_observations.clear()
    obs_verified = engine.observe_answer(
        frontier,
        question_attempt_id=qa.attempt_id,
        turn_id="t4",
        transcript_text="Here are all signed waiver docs with Director Vance's signature.",
        resolution=AnswerResolution.EVIDENTIAL,
        completeness=InformationCompleteness.VERIFIED,
        has_contradiction=False,
        specificity_score=0.95,
    )
    act4, _ = engine.evaluate_next_action(frontier)
    assert act4 == AdaptiveAction.ADVANCE


# -----------------------------------------------------------------------------
# AC-06: Guest-Validated Interpretation Promotes Inference with Lineage
# -----------------------------------------------------------------------------

def test_guest_validated_interpretation_promotes_inference_with_lineage():
    """When a guest validates a prior inference, it becomes GUEST_VALIDATED_INTERPRETATION with lineage."""
    observer = SemanticAcquisitionObserver()

    prior_inf_id = "evr:inference_pressure_99"
    obs = observer.observe_turn_response(
        question_attempt_id="qa:att_val",
        turn_id="t_val",
        transcript_text="Yes, that's exactly right — I felt if I refused to sign, my team would be defunded.",
        validated_interpretations=[
            {
                "prior_inference_id": prior_inf_id,
                "statement_text": "Guest confirmed signing waiver under direct threat of defunding.",
            }
        ],
    )

    assert len(obs.guest_validated_interpretation_refs) == 1
    val_rec = obs.evidence_records[0]

    assert val_rec.kind == EvidenceLineageKind.GUEST_VALIDATED_INTERPRETATION
    assert val_rec.is_authenticated is True
    assert val_rec.authentication_method == "guest_explicit_confirmation"
    assert val_rec.validated_from_inference_ref is not None
    assert val_rec.validated_from_inference_ref.object_id == prior_inf_id


# -----------------------------------------------------------------------------
# AC-07: Observation Schema Conformance and Non-Canonical Status
# -----------------------------------------------------------------------------

def test_observation_schema_conformance_and_non_canonical_status():
    """Observation object confirms to 03_DERIVED_SCHEMAS.yaml and remains non-canonical."""
    observer = SemanticAcquisitionObserver()

    obs = observer.observe_turn_response(
        question_attempt_id="qa:attempt_conf",
        turn_id="t_conf",
        transcript_text="Standard operational check completed at 14:00.",
        resolution=AnswerResolution.SPECIFIC,
        completeness=InformationCompleteness.PARTIAL,
        evidence_modes=[EvidenceMode.FACT, EvidenceMode.STORY],
        temporal_orientation=[TemporalOrientation.PAST_RECONSTRUCTION],
        social_reference_frame=[SocialReferenceFrame.SELF],
    )

    # Invariants from 03_DERIVED_SCHEMAS.yaml
    assert obs.is_canonical is False
    assert obs.question_attempt_ref.object_id == "qa:attempt_conf"
    assert obs.observed_response_ref.object_id == "turn_resp:t_conf"
    assert EvidenceMode.FACT in obs.evidence_modes
    assert EvidenceMode.STORY in obs.evidence_modes
    assert TemporalOrientation.PAST_RECONSTRUCTION in obs.temporal_orientation
    assert SocialReferenceFrame.SELF in obs.social_reference_frame
