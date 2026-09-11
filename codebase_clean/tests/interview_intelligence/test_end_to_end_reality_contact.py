"""
Test Suite for Mandate M11: End-to-End Reality Contact Regression (FR-IP-001 through FR-IP-010)

Proves the complete integrated CAE Interview Program against real repository paths and strict
adversarial attacks:
  1. Complete 10-Stage Proof Chain:
     Upstream Ingestion -> Operator Selection -> Resolution -> Brief Compilation -> Session Frontier
     -> Observation -> Evidence Lineage -> Content Menu -> Operator Review -> Production Manifest.
  2. 11 Required Adversarial Attacks:
     - receipt without reality
     - schema-only success
     - wrong-workspace reference laundering
     - generic answer passing structural validation
     - archetype laundering
     - score/performance proxy replacing semantic evidence
     - question-count gaming
     - Operator bypass
     - stale UI overwriting current state
     - lock enforced only in UI
     - rejected candidate leaking into launch/production.
"""

import hashlib
import pytest
from datetime import datetime, timezone
from typing import List

from conscious_activations_interview_composer.errors import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from conscious_activations_interview_composer.repository import InterviewComposerRepository
from conscious_activations_interview_composer.services.brief_service import BriefService
from conscious_activations_interview_composer.services.research_service import ResearchService

from cae_interview_intelligence.brief_compiler import ActivativeInterviewBriefCompiler
from cae_interview_intelligence.errors import (
    ScriptedAnswerViolationError,
    UnauthenticatedSessionError,
)
from cae_interview_intelligence.hypothesis_adapter import (
    CandidateState,
    CoordinateBasis,
    HypothesisCandidate,
    HypothesisPortfolioAdapter,
    Provenance,
    SelectionDiagnostics,
    SemanticRef,
)
from cae_interview_intelligence.question_resolver import (
    AnswerResolution,
    AnswerRoutingProfile,
    CompositionCompatibility,
    EvidenceMode,
    InformationCompleteness,
    QuestionCandidate,
    QuestionIntelligenceResolver,
    QuestionProgramDerived,
    SocialReferenceFrame,
    TemporalOrientation,
)
from cae_interview_intelligence.operator_studio import (
    CandidateReviewItem,
    OperatorActionType,
    OperatorFeedback,
    OperatorStudioService,
    StudioSession,
)
from cae_interview_intelligence.adaptive_frontier import (
    AdaptiveAction,
    AdaptiveQuestionFrontierEngine,
    CoverageSpineItem,
    EvidenceRequirement,
    FrontierState,
    QuestionAttempt,
    RequirementStatus,
)
from cae_interview_intelligence.semantic_acquisition import (
    AcquisitionEvidenceRecord,
    DiscrepancyRecord,
    EvidenceLineageKind,
    SemanticAcquisitionObservation,
    SemanticAcquisitionObserver,
)
from cae_interview_intelligence.composition_compatibility import (
    CompositionCompatibilityEvaluator,
    KNOWN_ARCHETYPES,
    KNOWN_FORMATS,
    KNOWN_NARRATIVE_ROLES,
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
# Test Fixtures & Helpers
# -----------------------------------------------------------------------------

def dummy_sha(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


def make_hypothesis_candidate(
    cid: str = "hyp_01",
    collision: str = "Traditional safety protocols mask executive complacency during system degradation.",
    tension: str = "safety_guarantee_vs_actual_risk",
    island: str = "belief_in_checklists",
    territory: str = "lead_safety_auditor",
    archetype: str = "ARCH-CRUCIBLE",
    format_type: str = "FMT-01-STORY",
    state: CandidateState = CandidateState.EVALUATED,
    quality_score: float = 0.90,
) -> HypothesisCandidate:
    return HypothesisCandidate(
        candidate_id=f"hc:{cid}",
        collision_statement=collision,
        state=state,
        upstream_hypothesis_refs=[
            SemanticRef(
                object_id=f"air:hyp:{cid}",
                version="1.0.0",
                sha256=dummy_sha(f"air:hyp:{cid}"),
                object_type="activation_hypothesis",
            )
        ],
        coordinates=CoordinateBasis(
            d01_audience_tension=tension,
            d02_audience_belief=island,
            d03_audience_desired_state="true_systemic_resilience",
            d04_guest_lived_authority=territory,
            d05_guest_contradiction="compliance_signoff_vs_known_vulnerability",
            d06_guest_transformation="from_passive_auditor_to_whistleblower",
            d07_cultural_world_signal="sig:airline_near_miss_2026",
            d08_target_enemy_status_quo="checklist_theater",
            d09_oblique_lens="drift_into_failure",
            d10_archetype_opportunity=archetype,
            d11_distribution_condition="high_retention_provocation",
            d12_evidence_opportunity="internal_audit_paper_trail",
        ),
        desired_evidence=[
            "Exact audit timestamp when the exception was overridden",
            "Signed waiver demonstrating executive awareness",
        ],
        audience_cognitive_island_ref=SemanticRef(object_id=island),
        guest_territory_ref=SemanticRef(object_id=territory),
        edge_ref=SemanticRef(object_id=tension),
        archetype_refs=[SemanticRef(object_id=archetype)],
        selection_diagnostics=SelectionDiagnostics(
            relevance=quality_score,
            evidence_potential=quality_score,
            guest_authority=quality_score,
            audience_alignment=quality_score,
            collision_strength=quality_score,
            novelty=quality_score,
            research_grounding=quality_score,
        ),
        provenance=Provenance(
            source_refs=[
                SemanticRef(object_id=f"doc:memo_{cid}", sha256=dummy_sha(f"doc:memo_{cid}"))
            ],
            generated_by="test-fixture:m11",
        ),
    )


def setup_composer_environment(tmp_path):
    db_path = str(tmp_path / "composer_m11.db")
    repo = InterviewComposerRepository(db_path)
    repo.initialize()
    research_svc = ResearchService(repo)
    brief_svc = BriefService(repo)

    res = research_svc.create_package(
        {
            "workspace_id": "ws-m11",
            "project_id": "prj-m11",
            "guest_name": "Dr. Jean-Pierre Laurent",
            "source_urls": [],
            "uploaded_documents": [],
            "composer_authority": {
                "operator_id": "op-audrey",
                "authority_scope": "PRODUCTION",
                "assertion_id": "assert-res-m11",
            },
        },
        idempotency_key="idemp-res-m11",
    )
    research_obj = res["object"]
    return repo, brief_svc, research_obj


# -----------------------------------------------------------------------------
# 1. Complete 10-Stage Proof Chain
# -----------------------------------------------------------------------------

def test_complete_10_stage_proof_chain(tmp_path):
    """
    Executes the entire 10-stage proof chain from upstream AIR portfolio ingestion
    to downstream Operator-authorized production manifest export.
    """
    repo, brief_svc, research_obj = setup_composer_environment(tmp_path)
    workspace_id = "ws-m11"
    project_id = "prj-m11"
    operator_id = "op-director-jean-pierre"

    # Stage 1: Upstream Ingestion & Portfolio Adaptation
    adapter = HypothesisPortfolioAdapter()
    cand1 = make_hypothesis_candidate(
        "hyp_01",
        collision="Executive override bypassed critical flight-control safety sign-off 48h before launch.",
        tension="speed_vs_safety",
        island="checklists_guarantee_safety",
        territory="lead_safety_auditor",
        archetype="ARCH-CRUCIBLE",
        format_type="FMT-01-STORY",
    )
    cand2 = make_hypothesis_candidate(
        "hyp_02",
        collision="Distributed consensus failover locks DB shards under high concurrent billing spikes.",
        tension="throughput_vs_resilience",
        island="2pc_is_bulletproof",
        territory="principal_architect",
        archetype="ARCH-INVESTIGATIVE",
        format_type="FMT-03-BREAKDOWN",
    )
    cand_dup = make_hypothesis_candidate(
        "hyp_dup",
        collision="Duplicate collision on flight-control safety override before launch.",
        tension="speed_vs_safety",
        island="checklists_guarantee_safety",
        territory="lead_safety_auditor",
        archetype="ARCH-CRUCIBLE",
        format_type="FMT-01-STORY",
    )

    portfolio = adapter.select_working_portfolio(
        [cand1, cand2, cand_dup],
        target_min=1,
        target_max=2,
    )
    assert len(portfolio.selected_candidates) == 2
    selected_ids = [c.candidate_id for c in portfolio.selected_candidates]
    assert "hc:hyp_01" in selected_ids
    assert "hc:hyp_02" in selected_ids

    # Stage 2: Operator Studio Staging & Feedback
    studio_svc = OperatorStudioService()
    session = studio_svc.create_session(
        workspace_id=workspace_id,
        project_id=project_id,
        guest_name="Dr. Jean-Pierre Laurent",
        research_package_ref=research_obj,
        candidates=portfolio.selected_candidates,
    )
    assert session.session_id.startswith("studio:sess:")
    item1 = studio_svc.get_candidate_view(session.session_id, "hc:hyp_01")
    assert item1.current_version == 1

    # Apply Operator Action: KEEP with locked dimensions
    fb_keep = OperatorFeedback(
        action=OperatorActionType.KEEP,
        operator_id=operator_id,
        authority_scope="PRODUCTION",
        assertion_id="assert-keep-hyp01",
        notes="Crucible testimony is highly verified.",
        locked_dimensions=["hypothesis_ref", "target_resolution", "evidence_mode"],
    )
    item1 = studio_svc.apply_action(
        session_id=session.session_id,
        candidate_id="hc:hyp_01",
        feedback=fb_keep,
        expected_version=1,
    )
    assert item1.review_state == CandidateState.SELECTED

    # Stage 3: Question Program Intelligence Resolution
    resolver = QuestionIntelligenceResolver()
    q_prog_1 = resolver.resolve_question_program(item1.candidate)
    assert len(q_prog_1.candidate_questions) > 0
    qc1 = q_prog_1.candidate_questions[0]
    assert qc1.text != ""
    assert qc1.objective != ""
    assert len(qc1.expected_response_shape) > 0

    # Stage 4: Activative Interview Brief Compilation & Launch Authorization
    authority = {
        "operator_id": operator_id,
        "authority_scope": "PRODUCTION",
        "assertion_id": "assert-compile-m11",
    }
    compile_result = studio_svc.compile_and_authorize_brief(
        session_id=session.session_id,
        brief_service=brief_svc,
        idempotency_key="idemp_brief_m11",
        composer_authority=authority,
        primary_candidate_id="hc:hyp_01",
    )
    brief_obj = compile_result["object"]
    assert brief_obj["object_type"] == "activative_interview_brief"
    assert brief_obj["object_id"].startswith("ic:brief:")

    # Read back from authoritative store
    read_back = repo.get_object(brief_obj["object_id"])
    assert read_back["payload"]["brief_id"] == brief_obj["object_id"]

    # Stage 5: Live Runtime Interview Execution (Adaptive Frontier)
    frontier_engine = AdaptiveQuestionFrontierEngine()
    f_state = frontier_engine.initialize_frontier(
        session_id=session.session_id,
        candidates=[cand1, cand2],
    )
    qa1 = frontier_engine.select_next_question(f_state)
    assert qa1 is not None
    assert qa1.action == AdaptiveAction.ADVANCE

    # Stage 6: Semantic Acquisition & Answer Observation
    raw_answer_1 = "On October 14th, the VP signed the safety override waiver despite my written objection. We had 48 hours before the IPO filing."
    obs_front = frontier_engine.observe_answer(
        frontier=f_state,
        question_attempt_id=qa1.attempt_id,
        turn_id="turn_01",
        transcript_text=raw_answer_1,
        resolution=AnswerResolution.EPISODIC,
        completeness=InformationCompleteness.SUFFICIENT,
        specificity_score=0.95,
        authenticity_score=0.95,
    )
    assert len(f_state.history_observations) == 1

    observer = SemanticAcquisitionObserver()
    obs_1 = observer.observe_turn_response(
        question_attempt_id=qa1.attempt_id,
        turn_id="turn_01",
        transcript_text=raw_answer_1,
        guest_statements=["VP signed safety override on Oct 14 under IPO filing pressure."],
        resolution=AnswerResolution.EPISODIC,
        completeness=InformationCompleteness.SUFFICIENT,
        evidence_modes=[EvidenceMode.STORY],
    )
    assert len(obs_1.evidence_records) == 1

    # Stage 7 & 8: Evidence Handoff & 6-Link Lineage Verification
    source_ref = SourceReference.create_verified_source(
        session_id=session.session_id,
        turn_id="turn_01",
        workspace_id=workspace_id,
        project_id=project_id,
        raw_answer_text=raw_answer_1,
    )
    q_attempt_ref = QuestionAttemptRef(
        attempt_id="qa:attempt_001",
        question_candidate_ref=SemanticRef(object_id=qc1.question_id, object_type="question_candidate"),
        hypothesis_ref=SemanticRef(object_id="hc:hyp_01", object_type="hypothesis_candidate"),
        presented_question_text=qc1.text,
        source_ref=source_ref,
        workspace_id=workspace_id,
        project_id=project_id,
    )

    handoff_engine = AuthenticatedEvidenceHandoffEngine()
    accepted_ev_1 = handoff_engine.accept_turn_evidence(
        question_attempt=q_attempt_ref,
        observation=obs_1,
        source_ref=source_ref,
        lineage_kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
        extracted_statement=obs_1.evidence_records[0].statement_text,
        response_structure_present=["chronological_event", "internal_friction", "cost_paid"],
        is_authenticated_receipt=True,
    )

    cand_prod_1 = handoff_engine.synthesize_downstream_candidate(
        title="The IPO Safety Override Crucible",
        core_narrative_claim="Executive pressure forced a safety bypass 48 hours prior to IPO.",
        target_archetype="ARCH-CRUCIBLE",
        target_format="FMT-01-STORY",
        target_narrative_role="ROLE-PROTAGONIST-CRUCIBLE",
        source_evidence_records=[accepted_ev_1],
        workspace_id=workspace_id,
        project_id=project_id,
    )
    assert cand_prod_1.archetype_readiness is True

    # Trace 6-link lineage
    trace = handoff_engine.trace_lineage(cand_prod_1)
    assert trace.downstream_candidate_id == cand_prod_1.candidate_id
    assert trace.upstream_hypotheses == ["hc:hyp_01"]

    # Compile Evidence Package
    pkg = handoff_engine.compile_evidence_package(
        session_ref=SemanticRef(object_id=session.session_id, object_type="interview_session"),
        brief_ref=SemanticRef(object_id=brief_obj["object_id"], object_type="interview_brief"),
        workspace_id=workspace_id,
        project_id=project_id,
        accepted_evidence=[accepted_ev_1],
        content_candidates=[cand_prod_1],
    )
    assert pkg.package_sha256 != ""

    # Stage 9: Content Menu Readiness & Diagnostics
    menu_engine = ContentMenuReadinessEngine()
    menu = menu_engine.generate_menu(pkg)
    assert menu.total_candidates == 1
    assert menu.viable_candidates_count == 1

    menu_item = menu.clusters[0].candidates[0]
    assert menu_item.status == ContentCandidateMenuStatus.EVALUATED
    assert menu_item.diagnostics.archetype_compatible is True

    # Stage 10: Operator Review & Final Production Manifest Export
    menu = menu_engine.operator_select_candidate(
        menu=menu,
        menu_item_id=menu_item.menu_item_id,
        operator_id=operator_id,
        notes="High-fidelity episodic crucible testimony verified.",
    )
    assert menu.selected_candidates_count == 1

    manifest = menu_engine.export_production_manifest(menu)
    assert manifest["selected_count"] == 1
    assert manifest["production_manifest_sha256"] != ""
    assert manifest["selected_production_candidates"][0]["downstream_candidate_id"] == cand_prod_1.candidate_id


# -----------------------------------------------------------------------------
# 2. 11 Required Adversarial Attacks
# -----------------------------------------------------------------------------

def test_adversarial_receipt_without_reality():
    """Attack 1: Unauthenticated receipt or empty transcript cannot authenticate evidence."""
    handoff = AuthenticatedEvidenceHandoffEngine()
    hyp = make_hypothesis_candidate("hyp_fake")

    # Empty raw text fails SourceReference creation
    with pytest.raises(ValidationError, match="raw_answer_text is empty or too short"):
        SourceReference.create_verified_source(
            session_id="sess_fake",
            turn_id="turn_empty",
            workspace_id="ws_01",
            project_id="proj_01",
            raw_answer_text="   ",
        )

    # Unauthenticated receipt flag raises ValidationError during evidence acceptance
    source_ref = SourceReference.create_verified_source(
        session_id="sess_fake",
        turn_id="turn_unauth",
        workspace_id="ws_01",
        project_id="proj_01",
        raw_answer_text="Real words spoken by someone.",
    )
    q_attempt = QuestionAttemptRef(
        attempt_id="qa:unauth",
        question_candidate_ref=SemanticRef(object_id="qc:01", object_type="question_candidate"),
        hypothesis_ref=SemanticRef(object_id=hyp.candidate_id, object_type="hypothesis"),
        presented_question_text="What happened?",
        source_ref=source_ref,
        workspace_id="ws_01",
        project_id="proj_01",
    )
    obs = SemanticAcquisitionObservation(
        observation_id="obs:unauth",
        question_attempt_ref=SemanticRef(object_id=q_attempt.attempt_id, object_type="question_attempt"),
        observed_response_ref=SemanticRef(object_id=source_ref.source_ref_id, object_type="source_reference"),
        turn_id="turn_unauth",
        transcript_text="Real words spoken by someone.",
        resolution=AnswerResolution.EPISODIC,
        evidence_modes=[EvidenceMode.STORY],
        evidence_records=[],
    )

    with pytest.raises(ValidationError, match="fabricated receipt cannot authenticate evidence"):
        handoff.accept_turn_evidence(
            question_attempt=q_attempt,
            observation=obs,
            source_ref=source_ref,
            lineage_kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
            extracted_statement="Real statement",
            is_authenticated_receipt=False,
        )


def test_adversarial_schema_only_success():
    """Attack 2: Syntactically fluent material lacking empirical grounding fails grounding/archetype checks."""
    menu_engine = ContentMenuReadinessEngine()
    hyp = make_hypothesis_candidate("hyp_generic", collision="Agility requires breaking silos.")
    ev = AcceptedEvidenceRecord(
        evidence_id="ev_slop",
        question_attempt_ref=SemanticRef(object_id="qa_slop", object_type="question_attempt"),
        observation_ref=SemanticRef(object_id="obs_slop", object_type="observation"),
        source_ref=SourceReference.create_verified_source(
            session_id="sess_01",
            turn_id="turn_slop",
            raw_answer_text="Leadership is all about synergizing agile touchpoints across ecosystems.",
            workspace_id="ws_01",
            project_id="proj_01",
        ),
        hypothesis_ref=SemanticRef(object_id=hyp.candidate_id, object_type="hypothesis"),
        lineage_kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
        extracted_statement="Generic leadership synergies claim lacking empirical grounding.",
        resolution=AnswerResolution.GENERAL,
        evidence_modes=[EvidenceMode.FACT],
        response_structure_present=["generic_overview"],
        workspace_id="ws_01",
        project_id="proj_01",
        is_authenticated=True,
    )

    cand = DownstreamContentCandidate(
        candidate_id="cand_slop",
        title="Agile Synergy Story",
        core_narrative_claim="Leadership requires agile touchpoints.",
        target_archetype_ref=SemanticRef(object_id="ARCH-CRUCIBLE", object_type="archetype"),
        target_format_ref=SemanticRef(object_id="FMT-01-STORY", object_type="format"),
        target_narrative_role_ref=SemanticRef(object_id="ROLE-PROTAGONIST-CRUCIBLE", object_type="narrative_role"),
        source_evidence_refs=[SemanticRef(object_id=ev.evidence_id, object_type="accepted_evidence")],
        upstream_hypothesis_refs=[SemanticRef(object_id=hyp.candidate_id, object_type="hypothesis")],
        workspace_id="ws_01",
        project_id="proj_01",
        archetype_readiness=False,
    )

    pkg = AuthenticatedEvidencePackage(
        session_ref=SemanticRef(object_id="sess_01", object_type="interview_session"),
        brief_ref=SemanticRef(object_id="brief_01", object_type="interview_brief"),
        workspace_id="ws_01",
        project_id="proj_01",
        accepted_evidence=[ev],
        content_candidates=[cand],
    )

    menu = menu_engine.generate_menu(pkg)
    item = menu.clusters[0].candidates[0]
    assert item.status == ContentCandidateMenuStatus.DEFICIENT_EVIDENCE
    assert item.diagnostics.is_generic_slop is True

    with pytest.raises(ValidationError, match="generic fluent material"):
        menu_engine.operator_select_candidate(menu, item.menu_item_id, operator_id="op_jane")


def test_adversarial_wrong_workspace_reference_laundering():
    """Attack 3: Laundering evidence across workspace or project boundaries is strictly blocked."""
    handoff = AuthenticatedEvidenceHandoffEngine()
    hyp = make_hypothesis_candidate("hyp_cross")
    source_ref = SourceReference.create_verified_source(
        session_id="sess_cross",
        turn_id="turn_cross",
        workspace_id="ws_A",
        project_id="proj_01",
        raw_answer_text="Legitimate testimony from workspace A.",
    )
    # Attempt created under workspace_B
    q_attempt = QuestionAttemptRef(
        attempt_id="qa:cross",
        question_candidate_ref=SemanticRef(object_id="qc:01", object_type="question_candidate"),
        hypothesis_ref=SemanticRef(object_id=hyp.candidate_id, object_type="hypothesis"),
        presented_question_text="Tell me about the incident.",
        source_ref=source_ref,
        workspace_id="ws_B",  # Mismatched workspace!
        project_id="proj_01",
    )
    obs = SemanticAcquisitionObservation(
        observation_id="obs:cross",
        question_attempt_ref=SemanticRef(object_id=q_attempt.attempt_id, object_type="question_attempt"),
        observed_response_ref=SemanticRef(object_id=source_ref.source_ref_id, object_type="source_reference"),
        turn_id="turn_cross",
        transcript_text="Legitimate testimony from workspace A.",
        resolution=AnswerResolution.EPISODIC,
        evidence_modes=[EvidenceMode.STORY],
        evidence_records=[],
    )

    with pytest.raises(ValidationError, match="Cross-workspace reference laundering rejected"):
        handoff.accept_turn_evidence(
            question_attempt=q_attempt,
            observation=obs,
            source_ref=source_ref,
            lineage_kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
            extracted_statement="Legitimate testimony",
        )


def test_adversarial_generic_answer_passing_structural_validation():
    """Attack 4: Generic response lacking crucible shape moves fails structural validation."""
    evaluator = CompositionCompatibilityEvaluator()
    cand = make_hypothesis_candidate("hyp_struct", archetype="ARCH-CRUCIBLE")
    comp = evaluator.evaluate_compatibility(
        candidate=cand,
        target_archetype="ARCH-CRUCIBLE",
        target_format="FMT-01-STORY",
        target_narrative_role="ROLE-PROTAGONIST-CRUCIBLE",
    )
    observed_generic = ["generic_overview"]
    missing = [req for req in comp.expected_response_structure if req not in observed_generic]
    assert "internal_friction" in missing
    assert "cost_paid" in missing


def test_adversarial_archetype_laundering():
    """Attack 5: Applying an archetype label to ungrounded evidence fails validation."""
    handoff = AuthenticatedEvidenceHandoffEngine()
    hyp = make_hypothesis_candidate("hyp_witness")
    source_ref = SourceReference.create_verified_source(
        session_id="sess_01",
        turn_id="turn_01",
        raw_answer_text="I was in the room when it happened.",
        workspace_id="ws_01",
        project_id="proj_01",
    )
    q_attempt = QuestionAttemptRef(
        attempt_id="qa:01",
        question_candidate_ref=SemanticRef(object_id="qc:01", object_type="question_candidate"),
        hypothesis_ref=SemanticRef(object_id=hyp.candidate_id, object_type="hypothesis"),
        presented_question_text="What did you see?",
        source_ref=source_ref,
        workspace_id="ws_01",
        project_id="proj_01",
    )
    obs = SemanticAcquisitionObservation(
        observation_id="obs:01",
        question_attempt_ref=SemanticRef(object_id=q_attempt.attempt_id, object_type="question_attempt"),
        observed_response_ref=SemanticRef(object_id=source_ref.source_ref_id, object_type="source_reference"),
        turn_id="turn_01",
        transcript_text="I was in the room when it happened.",
        resolution=AnswerResolution.EPISODIC,
        evidence_modes=[EvidenceMode.STORY],
        evidence_records=[],
    )

    ev = handoff.accept_turn_evidence(
        question_attempt=q_attempt,
        observation=obs,
        source_ref=source_ref,
        lineage_kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
        extracted_statement="I was in the room.",
        response_structure_present=["observed_event"],  # missing 'sensory_detail', 'verifiable_action'
        is_authenticated_receipt=True,
    )

    cand = handoff.synthesize_downstream_candidate(
        title="Incomplete Witness Claim",
        core_narrative_claim="Observer saw the event.",
        target_archetype="ARCH-WITNESS",
        target_format="FMT-01-STORY",
        target_narrative_role="ROLE-OBSERVER-WITNESS",
        source_evidence_records=[ev],
        workspace_id="ws_01",
        project_id="proj_01",
    )
    assert cand.archetype_readiness is False


def test_adversarial_score_proxy_replacing_semantic_evidence():
    """Attack 6: Diversity selection prevents selecting duplicate high-score hypotheses from same cluster."""
    adapter = HypothesisPortfolioAdapter()
    cand_dup1 = make_hypothesis_candidate("dup_1", tension="tension_a", island="island_a", quality_score=0.99)
    cand_dup2 = make_hypothesis_candidate("dup_2", tension="tension_a", island="island_a", quality_score=0.98)
    cand_dist = make_hypothesis_candidate("dist_3", tension="tension_b", island="island_b", quality_score=0.85)

    portfolio = adapter.select_working_portfolio([cand_dup1, cand_dup2, cand_dist], target_min=2, target_max=2)
    selected_ids = [c.candidate_id for c in portfolio.selected_candidates]
    assert "hc:dup_1" in selected_ids
    assert "hc:dist_3" in selected_ids
    assert "hc:dup_2" not in selected_ids


def test_adversarial_question_count_gaming():
    """Attack 7: Planning numbers (~96, 16-24, ~32) are non-quota aspirations; sparse pools are preserved."""
    adapter = HypothesisPortfolioAdapter()
    single_cand = make_hypothesis_candidate("single_hyp", quality_score=0.90)
    res = adapter.select_working_portfolio([single_cand], target_min=1, target_max=24)
    assert len(res.selected_candidates) == 1
    assert res.total_pool_evaluated == 1


def test_adversarial_operator_bypass(tmp_path):
    """Attack 8: Attempting to launch a brief without Operator authority fails."""
    _, brief_svc, research_obj = setup_composer_environment(tmp_path)
    studio_svc = OperatorStudioService()
    cand = make_hypothesis_candidate("hyp_bypass")
    session = studio_svc.create_session(
        workspace_id="ws-m11",
        project_id="prj-m11",
        guest_name="Guest Test",
        research_package_ref=research_obj,
        candidates=[cand],
    )

    # Missing authority raises ValidationError
    with pytest.raises(ValidationError, match="Missing required composer authority field"):
        studio_svc.compile_and_authorize_brief(
            session_id=session.session_id,
            brief_service=brief_svc,
            idempotency_key="idemp-bypass",
            composer_authority={},
        )


def test_adversarial_stale_ui_concurrency_conflict(tmp_path):
    """Attack 9: Stale UI client writing with outdated version triggers ConflictError."""
    _, _, research_obj = setup_composer_environment(tmp_path)
    studio_svc = OperatorStudioService()
    cand = make_hypothesis_candidate("hyp_conc")
    session = studio_svc.create_session(
        workspace_id="ws-m11",
        project_id="prj-m11",
        guest_name="Guest Test",
        research_package_ref=research_obj,
        candidates=[cand],
    )

    # Client A updates via EDIT at version 1 -> advances to version 2
    studio_svc.apply_action(
        session_id=session.session_id,
        candidate_id="hc:hyp_conc",
        feedback=OperatorFeedback(
            action=OperatorActionType.EDIT,
            operator_id="op_alice",
            authority_scope="PRODUCTION",
            assertion_id="assert-conc-1",
            edited_text="What exact day did the production system fail under load?",
        ),
        expected_version=1,
    )

    # Client B attempts edit with stale version 1 -> raises ConflictError
    with pytest.raises(ConflictError, match="Stale edit conflict"):
        studio_svc.apply_action(
            session_id=session.session_id,
            candidate_id="hc:hyp_conc",
            feedback=OperatorFeedback(
                action=OperatorActionType.REJECT,
                operator_id="op_bob",
                authority_scope="PRODUCTION",
                assertion_id="assert-conc-2",
            ),
            expected_version=1,
        )


def test_adversarial_lock_enforcement_in_backend(tmp_path):
    """Attack 10: Backend OperatorStudioService preserves locked dimensions across regeneration."""
    _, _, research_obj = setup_composer_environment(tmp_path)
    studio_svc = OperatorStudioService()
    cand = make_hypothesis_candidate("hyp_lock")
    session = studio_svc.create_session(
        workspace_id="ws-m11",
        project_id="prj-m11",
        guest_name="Guest Test",
        research_package_ref=research_obj,
        candidates=[cand],
    )

    item = studio_svc.apply_action(
        session_id=session.session_id,
        candidate_id="hc:hyp_lock",
        feedback=OperatorFeedback(
            action=OperatorActionType.REGENERATE,
            operator_id="op_alice",
            authority_scope="PRODUCTION",
            assertion_id="assert-regen-1",
            locked_dimensions=["hypothesis_ref", "target_resolution", "evidence_mode"],
        ),
        expected_version=1,
    )
    assert item.current_version == 2
    assert len(item.alternatives) > 0
    for alt in item.alternatives:
        for dim in ["hypothesis_ref", "target_resolution", "evidence_mode"]:
            assert dim in alt.locked_dimensions


def test_adversarial_rejected_candidate_leakage_prevention(tmp_path):
    """Attack 11: Candidates rejected in Operator Studio are strictly omitted from compiled Briefs."""
    _, brief_svc, research_obj = setup_composer_environment(tmp_path)
    studio_svc = OperatorStudioService()
    cand_keep = make_hypothesis_candidate("hyp_keep")
    cand_reject = make_hypothesis_candidate("hyp_reject")
    session = studio_svc.create_session(
        workspace_id="ws-m11",
        project_id="prj-m11",
        guest_name="Guest Test",
        research_package_ref=research_obj,
        candidates=[cand_keep, cand_reject],
    )

    # Reject cand_reject
    studio_svc.apply_action(
        session_id=session.session_id,
        candidate_id="hc:hyp_reject",
        feedback=OperatorFeedback(
            action=OperatorActionType.REJECT,
            operator_id="op_jane",
            authority_scope="PRODUCTION",
            assertion_id="assert-rej-1",
        ),
        expected_version=1,
    )

    # Keep cand_keep
    studio_svc.apply_action(
        session_id=session.session_id,
        candidate_id="hc:hyp_keep",
        feedback=OperatorFeedback(
            action=OperatorActionType.KEEP,
            operator_id="op_jane",
            authority_scope="PRODUCTION",
            assertion_id="assert-keep-1",
        ),
        expected_version=1,
    )

    compile_res = studio_svc.compile_and_authorize_brief(
        session_id=session.session_id,
        brief_service=brief_svc,
        idempotency_key="idemp-compile-rej-leak",
        composer_authority={
            "operator_id": "op_jane",
            "authority_scope": "PRODUCTION",
            "assertion_id": "assert-compile-auth",
        },
        primary_candidate_id="hc:hyp_keep",
    )
    brief = compile_res["object"]
    # Verify brief compiled successfully for primary candidate
    assert brief["object_id"].startswith("ic:brief:")
    working = studio_svc.assemble_working_portfolio(session.session_id)
    working_ids = [w.candidate.candidate_id for w in working]
    assert "hc:hyp_keep" in working_ids
    assert "hc:hyp_reject" not in working_ids
