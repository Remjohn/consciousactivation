"""
Test Suite for Mandate M10: Content Menu Readiness (FR-IP-010)

Verifies:
  1. Generic fluent material can be rejected.
  2. Strong evidence may yield multiple compatible formats.
  3. Unsupported archetype is flagged with missing requirements.
  4. Candidate lineage survives selection.
  5. No production candidate appears without evidence lineage.
  6. No quota forcing across heterogeneous hypotheses.
"""

import pytest
from datetime import datetime, timezone

from conscious_activations_interview_composer.errors import ValidationError, NotFoundError

from cae_interview_intelligence.hypothesis_adapter import (
    CoordinateBasis,
    HypothesisCandidate,
    Provenance,
    SemanticRef,
)
from cae_interview_intelligence.question_resolver import (
    AnswerResolution,
    EvidenceMode,
    QuestionCandidate,
    SocialReferenceFrame,
    TemporalOrientation,
)
from cae_interview_intelligence.semantic_acquisition import (
    AcquisitionEvidenceRecord,
    EvidenceLineageKind,
    SemanticAcquisitionObservation,
)
from cae_interview_intelligence.evidence_handoff import (
    AcceptedEvidenceRecord,
    AuthenticatedEvidenceHandoffEngine,
    AuthenticatedEvidencePackage,
    DownstreamContentCandidate,
    QuestionAttemptRef,
    SourceReference,
)
from cae_interview_intelligence.content_menu import (
    ContentCandidateMenu,
    ContentCandidateMenuStatus,
    ContentMenuCluster,
    ContentMenuReadinessEngine,
    MenuCandidateDiagnostics,
    MenuCandidateItem,
)


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def build_test_hypothesis(candidate_id: str = "hyp_01", summary: str = "Root tension") -> HypothesisCandidate:
    return HypothesisCandidate(
        candidate_id=candidate_id,
        air_hypothesis_id=f"air:{candidate_id}",
        candidate_version=1,
        hypothesis_summary=summary,
        tension_statement=f"Tension for {summary}",
        collision_statement=f"Collision for {summary}",
        significance_score=0.9,
        actionability_score=0.85,
        specificity_score=0.9,
        coordinate_basis=CoordinateBasis(
            temporal_orientation="past_reconstruction",
            social_reference_frame="self",
            evidence_mode="story",
            resolution="episodic",
        ),
        target_archetypes=["ARCH-CRUCIBLE", "ARCH-WITNESS"],
        target_formats=["FMT-01-STORY", "FMT-03-BREAKDOWN"],
        provenance=Provenance(source_system="air", source_refs=[SemanticRef(object_id="air_root", object_type="air_hypothesis")]),
    )


def build_test_evidence_record(
    evidence_id: str,
    hypothesis_id: str,
    statement: str,
    response_structure: list[str],
    workspace_id: str = "ws_primary",
    project_id: str = "proj_01",
) -> AcceptedEvidenceRecord:
    source_ref = SourceReference.create_verified_source(
        session_id="sess_test",
        turn_id=f"turn_{evidence_id}",
        raw_answer_text=f"Raw text: {statement}",
        workspace_id=workspace_id,
        project_id=project_id,
    )
    return AcceptedEvidenceRecord(
        evidence_id=evidence_id,
        question_attempt_ref=SemanticRef(object_id=f"qa:{evidence_id}", object_type="question_attempt"),
        observation_ref=SemanticRef(object_id=f"obs:{evidence_id}", object_type="observation"),
        source_ref=source_ref,
        hypothesis_ref=SemanticRef(object_id=hypothesis_id, object_type="hypothesis"),
        lineage_kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
        extracted_statement=statement,
        resolution=AnswerResolution.EPISODIC,
        evidence_modes=[EvidenceMode.STORY],
        response_structure_present=response_structure,
        workspace_id=workspace_id,
        project_id=project_id,
        is_authenticated=True,
    )


# -----------------------------------------------------------------------------
# Acceptance Test 1: Generic Fluent Material Can Be Rejected
# -----------------------------------------------------------------------------

def test_generic_fluent_material_can_be_rejected():
    """AC-01: Generic fluent material is flagged as deficient and rejected from selection."""
    engine = ContentMenuReadinessEngine()
    hyp = build_test_hypothesis("hyp_generic", "Generic corporate management challenges")

    # Generic ungrounded statement
    ev_generic = build_test_evidence_record(
        evidence_id="ev_gen_01",
        hypothesis_id=hyp.candidate_id,
        statement="generic corporate management challenges without specific facts.",
        response_structure=["generic_overview"],
    )

    cand_generic = DownstreamContentCandidate(
        candidate_id="cand_gen_01",
        title="Generic Management Story",
        core_narrative_claim="Managers often face hard choices in modern workplaces.",
        target_archetype_ref=SemanticRef(object_id="ARCH-CRUCIBLE", object_type="archetype"),
        target_format_ref=SemanticRef(object_id="FMT-01-STORY", object_type="format"),
        target_narrative_role_ref=SemanticRef(object_id="ROLE-PROTAGONIST-CRUCIBLE", object_type="narrative_role"),
        source_evidence_refs=[SemanticRef(object_id=ev_generic.evidence_id, object_type="accepted_evidence")],
        upstream_hypothesis_refs=[SemanticRef(object_id=hyp.candidate_id, object_type="hypothesis")],
        response_structure_present=["generic_overview"],
        workspace_id="ws_primary",
        project_id="proj_01",
        archetype_readiness=False,
    )

    pkg = AuthenticatedEvidencePackage(
        session_ref=SemanticRef(object_id="sess_test", object_type="interview_session"),
        brief_ref=SemanticRef(object_id="brief_test", object_type="interview_brief"),
        workspace_id="ws_primary",
        project_id="proj_01",
        accepted_evidence=[ev_generic],
        content_candidates=[cand_generic],
    )

    menu = engine.generate_menu(pkg)
    assert menu.total_candidates == 1
    assert menu.viable_candidates_count == 0

    item = menu.clusters[0].candidates[0]
    assert item.status == ContentCandidateMenuStatus.DEFICIENT_EVIDENCE
    assert item.diagnostics.is_generic_slop is True

    # Operator selection must fail for generic slop
    with pytest.raises(ValidationError, match="generic fluent material"):
        engine.operator_select_candidate(menu, item.menu_item_id, operator_id="op_jane")

    # Operator rejection succeeds
    menu = engine.operator_reject_candidate(
        menu, item.menu_item_id, operator_id="op_jane", reason="Lacks specific episodic grounding"
    )
    assert item.status == ContentCandidateMenuStatus.REJECTED
    assert menu.rejected_candidates_count == 1


# -----------------------------------------------------------------------------
# Acceptance Test 2: Strong Evidence Yields Multiple Compatible Formats
# -----------------------------------------------------------------------------

def test_strong_evidence_yields_multiple_compatible_formats():
    """AC-02: A single rich hypothesis with strong evidence generates multiple compatible formats."""
    engine = ContentMenuReadinessEngine()
    hyp = build_test_hypothesis("hyp_crucible", "The Executive Bypass Decision")

    # Strong episodic evidence with all crucible components
    ev_strong = build_test_evidence_record(
        evidence_id="ev_strong_01",
        hypothesis_id=hyp.candidate_id,
        statement="VP signed the safety override waiver under direct deadline pressure on Oct 14.",
        response_structure=["chronological_event", "internal_friction", "cost_paid"],
    )

    # Candidate 1: Narrative Story format
    cand_story = DownstreamContentCandidate(
        candidate_id="cand_story_01",
        title="The Waiver Crucible",
        core_narrative_claim="The override was coerced by executive bonus targets.",
        target_archetype_ref=SemanticRef(object_id="ARCH-CRUCIBLE", object_type="archetype"),
        target_format_ref=SemanticRef(object_id="FMT-01-STORY", object_type="format"),
        target_narrative_role_ref=SemanticRef(object_id="ROLE-PROTAGONIST-CRUCIBLE", object_type="narrative_role"),
        source_evidence_refs=[SemanticRef(object_id=ev_strong.evidence_id, object_type="accepted_evidence")],
        upstream_hypothesis_refs=[SemanticRef(object_id=hyp.candidate_id, object_type="hypothesis")],
        response_structure_present=["chronological_event", "internal_friction", "cost_paid"],
        workspace_id="ws_primary",
        project_id="proj_01",
        archetype_readiness=True,
    )

    # Candidate 2: Breakdown format
    cand_breakdown = DownstreamContentCandidate(
        candidate_id="cand_breakdown_02",
        title="Anatomy of the Override Failure",
        core_narrative_claim="Step-by-step institutional friction during the bypass waiver signature.",
        target_archetype_ref=SemanticRef(object_id="ARCH-CRUCIBLE", object_type="archetype"),
        target_format_ref=SemanticRef(object_id="FMT-03-BREAKDOWN", object_type="format"),
        target_narrative_role_ref=SemanticRef(object_id="ROLE-PROTAGONIST-CRUCIBLE", object_type="narrative_role"),
        source_evidence_refs=[SemanticRef(object_id=ev_strong.evidence_id, object_type="accepted_evidence")],
        upstream_hypothesis_refs=[SemanticRef(object_id=hyp.candidate_id, object_type="hypothesis")],
        response_structure_present=["chronological_event", "internal_friction", "cost_paid"],
        workspace_id="ws_primary",
        project_id="proj_01",
        archetype_readiness=True,
    )

    pkg = AuthenticatedEvidencePackage(
        session_ref=SemanticRef(object_id="sess_test", object_type="interview_session"),
        brief_ref=SemanticRef(object_id="brief_test", object_type="interview_brief"),
        workspace_id="ws_primary",
        project_id="proj_01",
        accepted_evidence=[ev_strong],
        content_candidates=[cand_story, cand_breakdown],
    )

    menu = engine.generate_menu(pkg)
    assert menu.total_candidates == 2
    assert menu.viable_candidates_count == 2
    assert len(menu.clusters) == 1
    assert len(menu.clusters[0].candidates) == 2

    # Select both candidates
    for item in menu.clusters[0].candidates:
        menu = engine.operator_select_candidate(
            menu, item.menu_item_id, operator_id="op_jane", notes="High evidentiary quality."
        )

    assert menu.selected_candidates_count == 2
    manifest = engine.export_production_manifest(menu)
    assert manifest["selected_count"] == 2
    assert len(manifest["selected_production_candidates"]) == 2


# -----------------------------------------------------------------------------
# Acceptance Test 3: Unsupported Archetype Is Flagged With Missing Requirements
# -----------------------------------------------------------------------------

def test_unsupported_archetype_is_flagged_with_missing_requirements():
    """AC-03: Candidate missing archetype structural moves is flagged with explicit missing requirements."""
    engine = ContentMenuReadinessEngine()
    hyp = build_test_hypothesis("hyp_witness", "Third-party observation of system failure")

    # Evidence has only observer claim, lacking 'observed_event' and 'corroborating_detail'
    ev_partial = build_test_evidence_record(
        evidence_id="ev_part_01",
        hypothesis_id=hyp.candidate_id,
        statement="Engineer observed the failure light blinking from across the control room.",
        response_structure=["observed_event"],  # missing corroborating_detail, impact_on_others
    )

    cand_witness = DownstreamContentCandidate(
        candidate_id="cand_witness_01",
        title="Control Room Witness",
        core_narrative_claim="The warning was visible to all engineers on shift.",
        target_archetype_ref=SemanticRef(object_id="ARCH-WITNESS", object_type="archetype"),
        target_format_ref=SemanticRef(object_id="FMT-01-STORY", object_type="format"),
        target_narrative_role_ref=SemanticRef(object_id="ROLE-OBSERVER-WITNESS", object_type="narrative_role"),
        source_evidence_refs=[SemanticRef(object_id=ev_partial.evidence_id, object_type="accepted_evidence")],
        upstream_hypothesis_refs=[SemanticRef(object_id=hyp.candidate_id, object_type="hypothesis")],
        response_structure_present=["observed_event"],
        workspace_id="ws_primary",
        project_id="proj_01",
        archetype_readiness=False,
    )

    pkg = AuthenticatedEvidencePackage(
        session_ref=SemanticRef(object_id="sess_test", object_type="interview_session"),
        brief_ref=SemanticRef(object_id="brief_test", object_type="interview_brief"),
        workspace_id="ws_primary",
        project_id="proj_01",
        accepted_evidence=[ev_partial],
        content_candidates=[cand_witness],
    )

    menu = engine.generate_menu(pkg)
    item = menu.clusters[0].candidates[0]
    assert item.status == ContentCandidateMenuStatus.DEFICIENT_EVIDENCE
    assert item.diagnostics.archetype_compatible is False
    assert "sensory_detail" in item.diagnostics.missing_evidence_required
    assert "verifiable_action" in item.diagnostics.missing_evidence_required

    # Attempting to select fails
    with pytest.raises(ValidationError, match="unsupported archetype"):
        engine.operator_select_candidate(menu, item.menu_item_id, operator_id="op_jane")


# -----------------------------------------------------------------------------
# Acceptance Test 4: Candidate Lineage Survives Selection
# -----------------------------------------------------------------------------

def test_candidate_lineage_survives_operator_selection():
    """AC-04: Full evidence lineage survives through operator selection into the production manifest."""
    engine = ContentMenuReadinessEngine()
    hyp = build_test_hypothesis("hyp_lineage", "Crucible Lineage Verification")

    ev = build_test_evidence_record(
        evidence_id="ev_lineage_01",
        hypothesis_id=hyp.candidate_id,
        statement="Full crucible proof with internal friction and heavy cost paid on record.",
        response_structure=["chronological_event", "internal_friction", "cost_paid"],
    )

    cand = DownstreamContentCandidate(
        candidate_id="cand_lineage_01",
        title="Lineage Preserved Candidate",
        core_narrative_claim="The decision led to immense friction and personal cost.",
        target_archetype_ref=SemanticRef(object_id="ARCH-CRUCIBLE", object_type="archetype"),
        target_format_ref=SemanticRef(object_id="FMT-01-STORY", object_type="format"),
        target_narrative_role_ref=SemanticRef(object_id="ROLE-PROTAGONIST-CRUCIBLE", object_type="narrative_role"),
        source_evidence_refs=[SemanticRef(object_id=ev.evidence_id, object_type="accepted_evidence")],
        upstream_hypothesis_refs=[SemanticRef(object_id=hyp.candidate_id, object_type="hypothesis")],
        response_structure_present=["chronological_event", "internal_friction", "cost_paid"],
        workspace_id="ws_primary",
        project_id="proj_01",
        archetype_readiness=True,
    )

    pkg = AuthenticatedEvidencePackage(
        session_ref=SemanticRef(object_id="sess_test", object_type="interview_session"),
        brief_ref=SemanticRef(object_id="brief_test", object_type="interview_brief"),
        workspace_id="ws_primary",
        project_id="proj_01",
        accepted_evidence=[ev],
        content_candidates=[cand],
    )

    menu = engine.generate_menu(pkg)
    item = menu.clusters[0].candidates[0]
    menu = engine.operator_select_candidate(
        menu, item.menu_item_id, operator_id="op_lead", notes="Verified full lineage."
    )

    manifest = engine.export_production_manifest(menu)
    prod_cand = manifest["selected_production_candidates"][0]

    assert prod_cand["source_hypothesis"]["object_id"] == "hyp_lineage"
    assert prod_cand["supporting_evidence_refs"][0]["object_id"] == "ev_lineage_01"
    assert prod_cand["target_archetype"] == "ARCH-CRUCIBLE"
    assert prod_cand["target_format"] == "FMT-01-STORY"
    assert "op:op_lead" in [r["object_id"] for r in prod_cand["provenance"]["source_refs"]]
    assert manifest["production_manifest_sha256"] != ""


# -----------------------------------------------------------------------------
# Acceptance Test 5: No Production Candidate Without Evidence Lineage
# -----------------------------------------------------------------------------

def test_no_production_candidate_without_evidence_lineage():
    """AC-05: Menu generation fails if a candidate has missing or orphaned evidence references."""
    engine = ContentMenuReadinessEngine()
    hyp = build_test_hypothesis("hyp_orphan", "Orphaned candidate test")

    # Candidate cites non-existent evidence ID
    cand_orphan = DownstreamContentCandidate(
        candidate_id="cand_orphan_01",
        title="Orphan Candidate",
        core_narrative_claim="Fabricated claim without backing evidence.",
        target_archetype_ref=SemanticRef(object_id="ARCH-CRUCIBLE", object_type="archetype"),
        target_format_ref=SemanticRef(object_id="FMT-01-STORY", object_type="format"),
        target_narrative_role_ref=SemanticRef(object_id="ROLE-PROTAGONIST-CRUCIBLE", object_type="narrative_role"),
        source_evidence_refs=[SemanticRef(object_id="ev_non_existent", object_type="accepted_evidence")],
        upstream_hypothesis_refs=[SemanticRef(object_id=hyp.candidate_id, object_type="hypothesis")],
        response_structure_present=["chronological_event"],
        workspace_id="ws_primary",
        project_id="proj_01",
        archetype_readiness=False,
    )

    pkg = AuthenticatedEvidencePackage(
        session_ref=SemanticRef(object_id="sess_test", object_type="interview_session"),
        brief_ref=SemanticRef(object_id="brief_test", object_type="interview_brief"),
        workspace_id="ws_primary",
        project_id="proj_01",
        accepted_evidence=[],  # No evidence
        content_candidates=[cand_orphan],
    )

    with pytest.raises(ValidationError, match="no production candidate appears without evidence lineage"):
        engine.generate_menu(pkg)


# -----------------------------------------------------------------------------
# Acceptance Test 6: No Quota Forcing Across Heterogeneous Hypotheses
# -----------------------------------------------------------------------------

def test_no_quota_forcing_across_heterogeneous_hypotheses():
    """Quantity Rule: Heterogeneous hypotheses yield natural candidate counts without forcing fixed quotas."""
    engine = ContentMenuReadinessEngine()

    hyp_rich = build_test_hypothesis("hyp_rich", "Rich tension yielding 3 pieces")
    hyp_barren = build_test_hypothesis("hyp_barren", "Barren tension yielding 0 viable pieces")

    ev_rich = build_test_evidence_record(
        evidence_id="ev_rich_01",
        hypothesis_id=hyp_rich.candidate_id,
        statement="Rich multi-faceted testimony with full chronological friction and cost.",
        response_structure=["chronological_event", "internal_friction", "cost_paid"],
    )
    ev_barren = build_test_evidence_record(
        evidence_id="ev_barren_01",
        hypothesis_id=hyp_barren.candidate_id,
        statement="generic claim with no specific facts.",
        response_structure=["generic_overview"],
    )

    # 3 viable candidates for hyp_rich
    cands_rich = [
        DownstreamContentCandidate(
            candidate_id=f"cand_rich_{i}",
            title=f"Rich Story Part {i}",
            core_narrative_claim=f"Claim {i} from rich testimony.",
            target_archetype_ref=SemanticRef(object_id="ARCH-CRUCIBLE", object_type="archetype"),
            target_format_ref=SemanticRef(object_id="FMT-01-STORY", object_type="format"),
            target_narrative_role_ref=SemanticRef(object_id="ROLE-PROTAGONIST-CRUCIBLE", object_type="narrative_role"),
            source_evidence_refs=[SemanticRef(object_id=ev_rich.evidence_id, object_type="accepted_evidence")],
            upstream_hypothesis_refs=[SemanticRef(object_id=hyp_rich.candidate_id, object_type="hypothesis")],
            response_structure_present=["chronological_event", "internal_friction", "cost_paid"],
            workspace_id="ws_primary",
            project_id="proj_01",
            archetype_readiness=True,
        )
        for i in range(1, 4)
    ]

    # 1 candidate for hyp_barren that is deficient
    cand_barren = DownstreamContentCandidate(
        candidate_id="cand_barren_01",
        title="Barren Generic Piece",
        core_narrative_claim="Generic claims about management.",
        target_archetype_ref=SemanticRef(object_id="ARCH-CRUCIBLE", object_type="archetype"),
        target_format_ref=SemanticRef(object_id="FMT-01-STORY", object_type="format"),
        target_narrative_role_ref=SemanticRef(object_id="ROLE-PROTAGONIST-CRUCIBLE", object_type="narrative_role"),
        source_evidence_refs=[SemanticRef(object_id=ev_barren.evidence_id, object_type="accepted_evidence")],
        upstream_hypothesis_refs=[SemanticRef(object_id=hyp_barren.candidate_id, object_type="hypothesis")],
        response_structure_present=["generic_overview"],
        workspace_id="ws_primary",
        project_id="proj_01",
        archetype_readiness=False,
    )

    pkg = AuthenticatedEvidencePackage(
        session_ref=SemanticRef(object_id="sess_test", object_type="interview_session"),
        brief_ref=SemanticRef(object_id="brief_test", object_type="interview_brief"),
        workspace_id="ws_primary",
        project_id="proj_01",
        accepted_evidence=[ev_rich, ev_barren],
        content_candidates=cands_rich + [cand_barren],
    )

    menu = engine.generate_menu(pkg)
    assert menu.total_candidates == 4
    assert menu.viable_candidates_count == 3  # hyp_rich yielded 3, hyp_barren yielded 0

    cluster_map = {cl.hypothesis_ref.object_id: cl for cl in menu.clusters}
    assert cluster_map["hyp_rich"].viable_count == 3
    assert cluster_map["hyp_barren"].viable_count == 0
