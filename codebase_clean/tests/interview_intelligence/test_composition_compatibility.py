"""
test_composition_compatibility.py
---------------------------------
Acceptance tests for CAE Mandate M08 — Archetype / Format Compatibility.

Validates:
1. Story-oriented hypothesis/archetype prefers episodic story evidence (AC-01).
2. Mechanism-oriented hypothesis/archetype prefers causal/mechanistic evidence (AC-02).
3. A semantically strong question can be rejected when composition-incompatible (AC-03).
4. Archetype labels cannot turn generic responses into story evidence (AC-04, anti-reward invariant).
5. Compatibility view exposes derived reasons and expected response structure (AC-05).
6. Format harness constraints and multi-roll pacing structure are preserved (AC-06).
"""

import hashlib
import pytest

from conscious_activations_interview_composer.errors import ValidationError

from cae_interview_intelligence.composition_compatibility import (
    KNOWN_ARCHETYPES,
    KNOWN_FORMATS,
    KNOWN_NARRATIVE_ROLES,
    CompositionCompatibility,
    CompositionCompatibilityEvaluator,
)
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
    QuestionIntelligenceResolver,
    SocialReferenceFrame,
)
from cae_interview_intelligence.semantic_acquisition import (
    AcquisitionEvidenceRecord,
    EvidenceLineageKind,
    SemanticAcquisitionObservation,
    SemanticAcquisitionObserver,
)


def dummy_sha(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


def make_test_candidate(cid: str = "comp_hyp_01") -> HypothesisCandidate:
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
            generated_by="test-fixture:m08",
        ),
    )


# -----------------------------------------------------------------------------
# AC-01: Story-Oriented Intent Prefers Episodic Story Evidence
# -----------------------------------------------------------------------------

def test_story_oriented_hypothesis_prefers_episodic_evidence():
    """Crucible / Witness story archetypes evaluate high compatibility for episodic story resolution."""
    evaluator = CompositionCompatibilityEvaluator()
    candidate = make_test_candidate("c_story")

    compat = evaluator.evaluate_compatibility(
        candidate=candidate,
        target_archetype="ARCH-CRUCIBLE",
        target_format="FMT-01-STORY",
        target_narrative_role="ROLE-PROTAGONIST-CRUCIBLE",
        target_resolution=AnswerResolution.EPISODIC,
        evidence_mode=EvidenceMode.STORY,
    )

    assert compat.is_compatible() is True
    assert compat.compatibility_score >= 0.85
    assert len(compat.incompatible_reasons) == 0
    assert any("matches archetype 'Crucible Testimony'" in r for r in compat.compatible_reasons)
    assert "chronological_event" in compat.expected_response_structure
    assert "internal_friction" in compat.expected_response_structure
    assert "cost_paid" in compat.expected_response_structure


# -----------------------------------------------------------------------------
# AC-02: Mechanism-Oriented Intent Prefers Mechanistic / Causal Evidence
# -----------------------------------------------------------------------------

def test_mechanism_oriented_hypothesis_prefers_mechanistic_evidence():
    """Investigative / Debunk archetypes evaluate high compatibility for mechanistic causal traces."""
    evaluator = CompositionCompatibilityEvaluator()
    candidate = make_test_candidate("c_mech")

    compat = evaluator.evaluate_compatibility(
        candidate=candidate,
        target_archetype="ARCH-INVESTIGATIVE",
        target_format="FMT-03-BREAKDOWN",
        target_narrative_role="ROLE-TECHNICAL-ANALYST",
        target_resolution=AnswerResolution.MECHANISTIC,
        evidence_mode=EvidenceMode.FACT,
    )

    assert compat.is_compatible() is True
    assert compat.compatibility_score >= 0.85
    assert len(compat.incompatible_reasons) == 0
    assert any("matches archetype 'Investigative Breakdown'" in r for r in compat.compatible_reasons)
    assert "causal_mechanism" in compat.expected_response_structure
    assert "structural_anomaly" in compat.expected_response_structure
    assert "empirical_metric" in compat.expected_response_structure


# -----------------------------------------------------------------------------
# AC-03: Semantically Strong Question Rejected When Composition-Incompatible
# -----------------------------------------------------------------------------

def test_semantically_strong_question_rejected_when_composition_incompatible():
    """A question that targets abstract discourse is rejected for an episodic Crucible archetype."""
    evaluator = CompositionCompatibilityEvaluator()
    candidate = make_test_candidate("c_incomp")

    # Abstract question targeting Crucible story archetype
    compat_abstract = evaluator.evaluate_compatibility(
        candidate=candidate,
        target_archetype="ARCH-CRUCIBLE",
        target_format="FMT-01-STORY",
        target_resolution=AnswerResolution.ABSTRACT,
        evidence_mode=EvidenceMode.INTERPRETATION,
    )

    assert compat_abstract.is_compatible() is False
    assert compat_abstract.compatibility_score < 0.60
    assert len(compat_abstract.incompatible_reasons) > 0
    assert any("requires EPISODIC lived testimony" in r for r in compat_abstract.incompatible_reasons)

    # Incompatible broadcast promo soundbite syntax
    compat_promo = evaluator.evaluate_compatibility(
        candidate=candidate,
        target_archetype="incompatible_archetype_broadcast_promo",
    )
    assert compat_promo.is_compatible() is False
    assert compat_promo.compatibility_score == 0.20
    assert "promotional soundbite broadcast syntax" in compat_promo.incompatible_reasons[0]


# -----------------------------------------------------------------------------
# AC-04: Archetype Labels Cannot Turn Generic Responses into Story Evidence
# -----------------------------------------------------------------------------

def test_archetype_labels_cannot_turn_generic_responses_into_story_evidence():
    """Anti-Reward invariant: Adding an archetype label cannot manufacture authenticated story evidence from slop."""
    evaluator = CompositionCompatibilityEvaluator()
    observer = SemanticAcquisitionObserver()

    # Create a generic slop response
    obs_slop = observer.observe_turn_response(
        question_attempt_id="qa:attempt_slop",
        turn_id="turn_slop",
        transcript_text="Compliance is a top priority for all airlines in the sector.",
        resolution=AnswerResolution.ABSTRACT,
        specificity_score=0.20,
    )

    # Creating a synthetic authenticated record out of generic response
    source_ref = SemanticRef(object_id="turn_resp:turn_slop", object_type="interview_turn_response")
    fake_authenticated_record = AcquisitionEvidenceRecord(
        kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
        turn_id="turn_slop",
        statement_text="Compliance is a top priority for all airlines in the sector.",
        source_ref=source_ref,
        is_authenticated=True,
        authentication_method="direct_spoken_testimony",
    )
    obs_slop.evidence_records.append(fake_authenticated_record)

    # Evaluator must detect and reject attempted evidence manufacturing
    with pytest.raises(ValidationError, match="cannot manufacture authenticated evidence from generic response"):
        evaluator.assert_archetype_does_not_manufacture_evidence(
            observation=obs_slop,
            target_archetype="ARCH-CRUCIBLE",
        )


# -----------------------------------------------------------------------------
# AC-05: Compatibility View Exposes Derived Reasons and Expected Structure
# -----------------------------------------------------------------------------

def test_compatibility_view_exposes_derived_reasons_and_expected_response_structure():
    """QuestionIntelligenceResolver outputs QuestionProgram with complete derived compatibility view."""
    resolver = QuestionIntelligenceResolver()
    candidate = make_test_candidate("c_view")

    qp = resolver.resolve_question_program(
        candidate=candidate,
        target_archetype="ARCH-WITNESS",
        target_format="FMT-01-STORY",
        target_narrative_role="ROLE-OBSERVER-WITNESS",
    )

    compat = qp.composition_compatibility
    assert compat.archetype_refs[0].object_id == "ARCH-WITNESS"
    assert compat.format_refs[0].object_id == "FMT-01-STORY"
    assert compat.narrative_role_refs[0].object_id == "ROLE-OBSERVER-WITNESS"
    assert "observed_scene" in compat.expected_response_structure
    assert len(compat.compatible_reasons) >= 2
    assert compat.is_compatible() is True


# -----------------------------------------------------------------------------
# AC-06: Format Harness Constrains Multi-Roll Narrative Roles
# -----------------------------------------------------------------------------

def test_format_harness_constrains_multi_roll_narrative_roles():
    """Known formats expose explicit multi-roll structure and supported archetype rosters."""
    story_fmt = KNOWN_FORMATS["FMT-01-STORY"]
    assert "A_ROLL_NARRATIVE" in story_fmt.pacing_and_roll_structure
    assert "B_ROLL_CONTEXT" in story_fmt.pacing_and_roll_structure
    assert "C_ROLL_EVIDENCE" in story_fmt.pacing_and_roll_structure
    assert "E_ROLL_SONIC" in story_fmt.pacing_and_roll_structure
    assert "ARCH-CRUCIBLE" in story_fmt.supported_archetype_ids
    assert "ARCH-WITNESS" in story_fmt.supported_archetype_ids

    breakdown_fmt = KNOWN_FORMATS["FMT-03-BREAKDOWN"]
    assert "ARCH-INVESTIGATIVE" in breakdown_fmt.supported_archetype_ids
    assert "CAUSAL_TRACE" in breakdown_fmt.pacing_and_roll_structure
