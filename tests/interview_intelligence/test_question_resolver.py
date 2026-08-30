"""
test_question_resolver.py
--------------------------
Acceptance tests for CAE Mandate M03 — Question Intelligence Resolution.

Validates:
1. Distinct syntactic realizations for the same semantic target (AC-01).
2. Regeneration cannot silently change locked hypothesis/evidence dimensions (AC-02).
3. Unaudited/provisional mechanisms cannot be marked canonical (AC-03).
4. Question candidate retains full audit and upstream provenance (AC-04).
5. Downstream compatibility filtering and rejection (AC-05).
6. Synthesis catalog completeness (QI-C01 to QI-C15).
"""

import pytest
from datetime import datetime, timezone

from cae_interview_intelligence.hypothesis_adapter import (
    CoordinateBasis,
    HypothesisCandidate,
    Provenance,
    SelectionDiagnostics,
    SemanticRef,
)
from cae_interview_intelligence.question_resolver import (
    APPROVED_PROVISIONAL_MECHANISMS,
    AnswerResolution,
    EvidenceMode,
    MechanismDisposition,
    ProvisionalMechanism,
    QuestionCandidate,
    QuestionIntelligenceResolver,
    QuestionProgramDerived,
    SocialReferenceFrame,
    TemporalOrientation,
)


def make_sample_hypothesis_candidate(
    cid: str = "test_hyp_01",
    collision_text: str = "Radical transparency collapses under organizational panic.",
    tension: str = "tension_transparency_vs_security",
    island: str = "island_governance_illusion",
    territory: str = "territory_post_mortem_ceo",
    archetype: str = "archetype_crucible",
) -> HypothesisCandidate:
    """Helper to build a valid HypothesisCandidate instance."""
    return HypothesisCandidate(
        candidate_id=f"hc:{cid}",
        collision_statement=collision_text,
        upstream_hypothesis_refs=[
            SemanticRef(
                object_id=f"air:hyp:{cid}",
                version="1.0.0",
                sha256="1234567890abcdef1234567890abcdef",
                object_type="activation_hypothesis",
            )
        ],
        coordinates=CoordinateBasis(
            d01_audience_tension=tension,
            d02_audience_belief=island,
            d03_audience_desired_state="clarity_under_fire",
            d04_guest_lived_authority=territory,
            d05_guest_contradiction="openness_policy_vs_crisis_secrecy",
            d06_guest_transformation="from_naive_openness_to_contextual_candor",
            d07_cultural_world_signal="sig:startup_leaks_2026",
            d08_target_enemy_status_quo="platitudinous_transparency",
            d09_oblique_lens="thermodynamic_entropy_dissipation",
            d10_archetype_opportunity=archetype,
            d11_distribution_condition="high_retention_provocation",
            d12_evidence_opportunity="q2_all_hands_crisis_transcript",
        ),
        audience_cognitive_island_ref=SemanticRef(object_id=island),
        guest_territory_ref=SemanticRef(object_id=territory),
        edge_ref=SemanticRef(object_id=tension),
        archetype_refs=[SemanticRef(object_id=archetype)],
        desired_evidence=[
            "Exact internal crisis meeting when transparency was suspended",
            "Specific cost paid in employee trust during the restructuring",
        ],
        selection_diagnostics=SelectionDiagnostics(
            relevance=0.90,
            evidence_potential=0.85,
            guest_authority=0.88,
            collision_strength=0.92,
        ),
        provenance=Provenance(
            source_refs=[SemanticRef(object_id="doc:research_interview_01", sha256="abc123def456")],
            generated_by="test-fixture:m03",
        ),
    )


# -----------------------------------------------------------------------------
# AC-01: Distinct Syntactic Realizations for Same Semantic Target
# -----------------------------------------------------------------------------

def test_distinct_syntactic_realizations_same_semantic_target():
    """The same hypothesis produces distinct syntactic realizations without changing its semantic target."""
    resolver = QuestionIntelligenceResolver()
    candidate = make_sample_hypothesis_candidate()
    
    q_program = resolver.resolve_question_program(candidate)
    
    assert isinstance(q_program, QuestionProgramDerived)
    assert len(q_program.candidate_questions) >= 3
    
    # All candidates share identical objective and underlying hypothesis ref
    shared_objective = q_program.objective
    shared_hyp_id = q_program.hypothesis_ref.object_id
    
    for qc in q_program.candidate_questions:
        assert qc.objective == shared_objective
        assert qc.provenance.source_refs[0].object_id == shared_hyp_id
        
    # The syntactic realizations (prompt text) are all distinct
    texts = [qc.text for qc in q_program.candidate_questions]
    assert len(set(texts)) == len(texts)
    
    # Different syntactic strategies are represented
    resolutions = [qc.target_resolution for qc in q_program.candidate_questions]
    evidence_modes = [qc.evidence_mode for qc in q_program.candidate_questions]
    assert len(set(resolutions)) > 1
    assert len(set(evidence_modes)) > 1


# -----------------------------------------------------------------------------
# AC-02: Regeneration Preserves Locked Dimensions
# -----------------------------------------------------------------------------

def test_regeneration_preserves_locked_dimensions():
    """A regeneration request cannot silently change locked hypothesis/evidence dimensions."""
    resolver = QuestionIntelligenceResolver()
    candidate = make_sample_hypothesis_candidate()
    q_program = resolver.resolve_question_program(candidate)
    original_q = q_program.candidate_questions[0]
    
    # Request syntactic regeneration
    regen_q = resolver.regenerate_question_candidate(
        existing_candidate=original_q,
        syntax_style="unvarnished_direct",
        variation_prompt_prefix="Let's focus on the turning point: ",
    )
    
    # Text changed
    assert regen_q.text != original_q.text
    assert "Let's focus on the turning point" in regen_q.text
    
    # Version incremented
    assert regen_q.version != original_q.version
    
    # Locked dimensions are strictly preserved
    assert regen_q.objective == original_q.objective
    assert regen_q.target_resolution == original_q.target_resolution
    assert regen_q.evidence_mode == original_q.evidence_mode
    assert regen_q.expected_evidence == original_q.expected_evidence
    
    # Parent lineage is maintained
    assert regen_q.parent_candidate_ref is not None
    assert regen_q.parent_candidate_ref.object_id == original_q.question_id
    assert regen_q.provenance.source_refs[0].object_id == original_q.question_id


# -----------------------------------------------------------------------------
# AC-03: Unaudited/Provisional Mechanisms Cannot Be Canonical
# -----------------------------------------------------------------------------

def test_unaudited_provisional_mechanism_cannot_be_canonical():
    """Unaudited mechanisms from synthesis cannot be marked canonical without promotion authority."""
    resolver = QuestionIntelligenceResolver()
    
    # Admitted mechanism QI-C01 is verified and non-canonical
    mech = resolver.verify_mechanism_admissibility("QI-C01")
    assert mech.is_canonical is False
    assert mech.disposition == MechanismDisposition.PROMOTION_CANDIDATE
    
    # Setting is_canonical=True is strictly blocked by schema validator
    with pytest.raises(ValueError, match="cannot be marked canonical"):
        ProvisionalMechanism(
            mechanism_id="QI-C01",
            name="Answer Resolution Escalation",
            family="Resolution Control",
            primary_transformation="abstract -> specific",
            runtime_trigger="low_resolution",
            disposition=MechanismDisposition.PROMOTION_CANDIDATE,
            is_canonical=True,  # Boundary Violation
        )

    # Non-admitted mechanism raises ValueError
    with pytest.raises(ValueError, match="not an admitted provisional mechanism"):
        resolver.verify_mechanism_admissibility("QI-UNKNOWN-999")


# -----------------------------------------------------------------------------
# AC-04: Question Candidate Retains Full Upstream Lineage
# -----------------------------------------------------------------------------

def test_question_candidate_retains_upstream_provenance():
    """Question candidate retains complete audit and upstream provenance."""
    resolver = QuestionIntelligenceResolver()
    candidate = make_sample_hypothesis_candidate("lineage_hyp_04")
    q_program = resolver.resolve_question_program(candidate)
    
    assert q_program.is_canonical is False
    assert q_program.hypothesis_ref.object_id == "air:hyp:lineage_hyp_04"
    assert q_program.provenance.source_refs[0].object_id == "air:hyp:lineage_hyp_04"
    
    for qc in q_program.candidate_questions:
        assert qc.is_canonical is False
        assert qc.parent_candidate_ref.object_id == candidate.candidate_id
        assert qc.provenance.source_refs[0].object_id == "air:hyp:lineage_hyp_04"
        assert len(qc.mechanism_refs) > 0


# -----------------------------------------------------------------------------
# AC-05: Downstream Compatibility Filtering
# -----------------------------------------------------------------------------

def test_downstream_compatibility_rejection():
    """A question candidate can be rejected/flagged for poor downstream compatibility even when structurally valid."""
    resolver = QuestionIntelligenceResolver()
    candidate = make_sample_hypothesis_candidate()
    
    # Resolve with incompatible archetype
    q_program = resolver.resolve_question_program(
        candidate,
        target_archetype="incompatible_archetype_broadcast_promo",
    )
    
    compat = q_program.composition_compatibility
    assert compat.is_compatible(min_threshold=0.50) is False
    assert compat.compatibility_score < 0.50
    assert len(compat.incompatible_reasons) > 0
    assert "incompatible with promotional soundbite" in compat.incompatible_reasons[0]


# -----------------------------------------------------------------------------
# Synthesis Catalog Completeness (QI-C01 through QI-C15)
# -----------------------------------------------------------------------------

def test_synthesis_mechanism_catalog_completeness():
    """Validates that all 15 candidate mechanism families from Synthesis §2 are registered."""
    catalog = APPROVED_PROVISIONAL_MECHANISMS
    assert len(catalog) == 15
    
    for idx in range(1, 16):
        mid = f"QI-C{idx:02d}"
        assert mid in catalog
        m = catalog[mid]
        assert m.is_canonical is False
        assert m.disposition in (
            MechanismDisposition.PROMOTION_CANDIDATE,
            MechanismDisposition.MERGE_CANDIDATE,
            MechanismDisposition.RESEARCH_MORE,
        )
        assert len(m.source_lineage) > 0
        assert len(m.forbidden_failure_patterns) > 0
