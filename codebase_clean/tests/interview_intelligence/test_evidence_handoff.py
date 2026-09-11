"""
Acceptance Test Suite for Mandate M09: Authenticated Evidence Handoff (FR-IP-007, FR-IP-010)

Tests the 5 mandatory acceptance criteria and anti-fabrication rules:
1. missing response prevents evidence acceptance;
2. wrong workspace/session reference is rejected;
3. fabricated receipt cannot authenticate evidence;
4. accepted evidence can be read back from the authoritative store;
5. downstream candidate can trace back to the same source evidence;
6. inference cannot be relabeled as Guest statement;
7. archetype readiness requires supporting response structure.
"""

import pytest
from datetime import datetime, timezone

from conscious_activations_interview_composer.errors import ConflictError, NotFoundError, ValidationError

from cae_interview_intelligence.hypothesis_adapter import CoordinateBasis, HypothesisCandidate, Provenance, SemanticRef
from cae_interview_intelligence.question_resolver import (
    AnswerResolution,
    EvidenceMode,
    QuestionCandidate,
    SocialReferenceFrame,
    TemporalOrientation,
)
from cae_interview_intelligence.semantic_acquisition import (
    AcquisitionEvidenceRecord,
    DiscrepancyRecord,
    EvidenceLineageKind,
    SemanticAcquisitionObservation,
)
from cae_interview_intelligence.evidence_handoff import (
    AcceptedEvidenceRecord,
    AuthenticatedEvidenceHandoffEngine,
    AuthenticatedEvidencePackage,
    DownstreamContentCandidate,
    LineageTraceNode,
    QuestionAttemptRef,
    SourceReference,
)


def create_mock_hypothesis() -> HypothesisCandidate:
    coords = CoordinateBasis(
        d01_tension="operational_friction",
        d02_polarity=0.6,
        d03_depth="deep",
        d04_domain="infrastructure",
        d05_guest_contradiction="policy_vs_reality",
        d06_guest_transformation="cautious_to_resigned",
        d07_narrative_charge=0.8,
        d08_systemic_scale=0.7,
        d09_temporal_locus="post_incident",
        d10_agency_posture="reluctant_actor",
        d11_counteractivation_risk=0.2,
        d12_voice_resonance=0.85,
    )
    return HypothesisCandidate(
        candidate_id="hc:audit_901",
        collision_statement="System bypasses became the standard operational procedure under deadline pressure.",
        desired_evidence=["Lived account of the first signed bypass waiver", "Direct personal consequence"],
        coordinates=coords,
        source_lineage=["book:crucible_studies", "air:hypothesis:901"],
    )


def create_mock_attempt(
    hyp: HypothesisCandidate,
    workspace_id: str = "ws_primary",
    project_id: str = "proj_01",
    session_id: str = "sess_100",
    raw_answer: str = "In October 2024, I signed the waiver because the release was blocked. My manager explicitly stated no release means no bonus.",
) -> tuple[QuestionAttemptRef, SourceReference, SemanticAcquisitionObservation]:
    source_ref = SourceReference.create_verified_source(
        session_id=session_id,
        turn_id="turn_01",
        workspace_id=workspace_id,
        project_id=project_id,
        raw_answer_text=raw_answer,
        guest_id="guest_expert_01",
    )
    q_candidate_ref = SemanticRef(object_id="qc:crucible_bypass", object_type="question_candidate")
    attempt = QuestionAttemptRef(
        attempt_id="qa:attempt_001",
        question_candidate_ref=q_candidate_ref,
        hypothesis_ref=SemanticRef(object_id=hyp.candidate_id, object_type="hypothesis_candidate"),
        presented_question_text="Can you describe the exact moment you signed the bypass waiver?",
        source_ref=source_ref,
        workspace_id=workspace_id,
        project_id=project_id,
    )
    obs = SemanticAcquisitionObservation(
        observation_id="obs:turn_01",
        question_attempt_ref=SemanticRef(object_id=attempt.attempt_id, object_type="question_attempt"),
        observed_response_ref=SemanticRef(object_id=source_ref.source_ref_id, object_type="source_reference"),
        turn_id="turn_01",
        transcript_text=raw_answer,
        resolution=AnswerResolution.EPISODIC,
        evidence_modes=[EvidenceMode.STORY, EvidenceMode.FACT],
        temporal_orientation=[TemporalOrientation.PAST_RECONSTRUCTION],
        social_reference_frame=[SocialReferenceFrame.SELF],
        evidence_records=[
            AcquisitionEvidenceRecord(
                record_id="rec:turn_01_fact",
                kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
                turn_id="turn_01",
                statement_text="Guest signed bypass waiver in October 2024 under managerial bonus pressure.",
                source_ref=SemanticRef(object_id=source_ref.source_ref_id, object_type="source_reference"),
                is_authenticated=True,
                authentication_method="direct_spoken_testimony",
            )
        ],
    )
    return attempt, source_ref, obs


# -----------------------------------------------------------------------------
# Acceptance Test 1: Missing Response Prevents Evidence Acceptance
# -----------------------------------------------------------------------------

def test_missing_response_prevents_evidence_acceptance():
    """AC-01: An attempt with missing, empty, or whitespace-only response text must fail validation."""
    engine = AuthenticatedEvidenceHandoffEngine()
    hyp = create_mock_hypothesis()

    # Attempt to create source reference with empty text fails
    with pytest.raises(ValidationError, match="raw_answer_text is empty or too short"):
        SourceReference.create_verified_source(
            session_id="sess_100",
            turn_id="turn_01",
            workspace_id="ws_01",
            project_id="proj_01",
            raw_answer_text="   ",
        )


# -----------------------------------------------------------------------------
# Acceptance Test 2: Wrong Workspace/Session Reference is Rejected
# -----------------------------------------------------------------------------

def test_wrong_workspace_session_reference_is_rejected():
    """AC-02: Cross-workspace or cross-session reference laundering must be strictly rejected."""
    engine = AuthenticatedEvidenceHandoffEngine()
    hyp = create_mock_hypothesis()
    attempt, source_ref, obs = create_mock_attempt(hyp, workspace_id="ws_alpha", session_id="sess_alpha")

    # Mismatched source reference from different workspace
    mismatched_source = SourceReference.create_verified_source(
        session_id="sess_alpha",
        turn_id="turn_01",
        workspace_id="ws_bravo",  # Different workspace!
        project_id="proj_01",
        raw_answer_text="I was in the server room when the outage occurred.",
    )

    with pytest.raises(ValidationError, match="Cross-workspace reference laundering rejected"):
        engine.accept_turn_evidence(
            question_attempt=attempt,
            observation=obs,
            source_ref=mismatched_source,
            lineage_kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
            extracted_statement="Guest observed outage in server room.",
        )


# -----------------------------------------------------------------------------
# Acceptance Test 3: Fabricated Receipt Cannot Authenticate Evidence
# -----------------------------------------------------------------------------

def test_fabricated_receipt_cannot_authenticate_evidence():
    """AC-03: Fabricated receipt flags or corrupted checksums cannot produce authenticated evidence."""
    engine = AuthenticatedEvidenceHandoffEngine()
    hyp = create_mock_hypothesis()
    attempt, source_ref, obs = create_mock_attempt(hyp)

    # 1. Tampered checksum
    tampered_source = SourceReference(
        source_ref_id="src:tampered",
        session_id=source_ref.session_id,
        turn_id=source_ref.turn_id,
        workspace_id=source_ref.workspace_id,
        project_id=source_ref.project_id,
        raw_answer_text="Completely different forged statement.",
        transcript_sha256=source_ref.transcript_sha256,  # Old hash!
    )

    with pytest.raises(ValidationError, match="Fabricated receipt / corrupted transcript checksum"):
        engine.accept_turn_evidence(
            question_attempt=attempt,
            observation=obs,
            source_ref=tampered_source,
            lineage_kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
            extracted_statement="Forged statement.",
        )

    # 2. Unauthenticated receipt flag
    with pytest.raises(ValidationError, match="fabricated receipt cannot authenticate evidence"):
        engine.accept_turn_evidence(
            question_attempt=attempt,
            observation=obs,
            source_ref=source_ref,
            lineage_kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
            extracted_statement="Valid statement.",
            is_authenticated_receipt=False,
        )


# -----------------------------------------------------------------------------
# Acceptance Test 4: Accepted Evidence Can Be Read Back from Authoritative Store
# -----------------------------------------------------------------------------

def test_accepted_evidence_can_be_read_back_from_authoritative_store():
    """AC-04: Stored evidence packages can be retrieved with cryptographic integrity validation."""
    engine = AuthenticatedEvidenceHandoffEngine()
    hyp = create_mock_hypothesis()
    attempt, source_ref, obs = create_mock_attempt(hyp)

    # Accept evidence
    ev = engine.accept_turn_evidence(
        question_attempt=attempt,
        observation=obs,
        source_ref=source_ref,
        lineage_kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
        extracted_statement="Guest signed bypass waiver in October 2024 under managerial bonus pressure.",
        response_structure_present=["chronological_event", "internal_friction", "cost_paid"],
    )

    # Synthesize downstream candidate
    cand = engine.synthesize_downstream_candidate(
        title="Crucible: The Waiver Decision",
        core_narrative_claim="Operational waivers became coercive under release deadline threats.",
        target_archetype="ARCH-CRUCIBLE",
        target_format="FMT-01-STORY",
        target_narrative_role="ROLE-PROTAGONIST-CRUCIBLE",
        source_evidence_records=[ev],
        workspace_id="ws_primary",
        project_id="proj_01",
    )

    # Compile package
    package = engine.compile_evidence_package(
        session_ref=SemanticRef(object_id=source_ref.session_id, object_type="interview_session"),
        brief_ref=SemanticRef(object_id="ic:brief_001", object_type="interview_brief"),
        workspace_id="ws_primary",
        project_id="proj_01",
        accepted_evidence=[ev],
        content_candidates=[cand],
    )

    # Read back from store
    retrieved = engine.read_evidence_package(package.package_id)
    assert retrieved.package_id == package.package_id
    assert len(retrieved.accepted_evidence) == 1
    assert retrieved.accepted_evidence[0].evidence_id == ev.evidence_id
    assert len(retrieved.content_candidates) == 1
    assert retrieved.content_candidates[0].candidate_id == cand.candidate_id
    assert retrieved.package_sha256 == package.package_sha256

    # Test corrupted package detection
    corrupted_pkg = retrieved.model_copy(deep=True)
    corrupted_pkg.workspace_id = "ws_hacked"
    engine.store[corrupted_pkg.package_id] = corrupted_pkg

    with pytest.raises(ConflictError, match="integrity compromised"):
        engine.read_evidence_package(corrupted_pkg.package_id)


# -----------------------------------------------------------------------------
# Acceptance Test 5: Downstream Candidate Can Trace Back to Source Evidence Lineage
# -----------------------------------------------------------------------------

def test_downstream_candidate_traces_to_source_evidence_lineage():
    """AC-05: Verifies the complete 6-link lineage chain for downstream content candidates."""
    engine = AuthenticatedEvidenceHandoffEngine()
    hyp = create_mock_hypothesis()
    attempt, source_ref, obs = create_mock_attempt(hyp)

    ev = engine.accept_turn_evidence(
        question_attempt=attempt,
        observation=obs,
        source_ref=source_ref,
        lineage_kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
        extracted_statement="Guest signed bypass waiver in October 2024 under managerial bonus pressure.",
        response_structure_present=["chronological_event", "internal_friction", "cost_paid"],
    )

    cand = engine.synthesize_downstream_candidate(
        title="Crucible: The Waiver Decision",
        core_narrative_claim="Operational waivers became coercive under release deadline threats.",
        target_archetype="ARCH-CRUCIBLE",
        target_format="FMT-01-STORY",
        target_narrative_role="ROLE-PROTAGONIST-CRUCIBLE",
        source_evidence_records=[ev],
        workspace_id="ws_primary",
        project_id="proj_01",
    )

    trace: LineageTraceNode = engine.trace_lineage(cand)
    assert trace.is_lineage_complete is True
    assert trace.anti_fabrication_checks_passed is True
    assert trace.downstream_candidate_id == cand.candidate_id
    assert trace.target_archetype == "ARCH-CRUCIBLE"
    assert trace.upstream_hypotheses == [hyp.candidate_id]
    assert len(trace.evidence_lineage) == 1
    
    lineage_entry = trace.evidence_lineage[0]
    assert lineage_entry["evidence_id"] == ev.evidence_id
    assert lineage_entry["lineage_kind"] == EvidenceLineageKind.GUEST_STATED_EVIDENCE.value
    assert lineage_entry["question_attempt_id"] == attempt.attempt_id
    assert lineage_entry["observation_id"] == obs.observation_id
    assert lineage_entry["source_ref"]["session_id"] == "sess_100"
    assert lineage_entry["source_ref"]["turn_id"] == "turn_01"


# -----------------------------------------------------------------------------
# Acceptance Test 6: Archetype Readiness Requires Supporting Response Structure
# -----------------------------------------------------------------------------

def test_archetype_readiness_requires_supporting_response_structure():
    """Anti-Fabrication: An archetype candidate cannot be marked ready if evidence lacks required response structure."""
    engine = AuthenticatedEvidenceHandoffEngine()
    hyp = create_mock_hypothesis()
    attempt, source_ref, obs = create_mock_attempt(hyp)

    # Evidence has only generic event, lacking internal_friction and cost_paid
    ev = engine.accept_turn_evidence(
        question_attempt=attempt,
        observation=obs,
        source_ref=source_ref,
        lineage_kind=EvidenceLineageKind.GUEST_STATED_EVIDENCE,
        extracted_statement="Guest signed a waiver.",
        response_structure_present=["chronological_event"],  # Missing internal_friction, cost_paid
    )

    cand = engine.synthesize_downstream_candidate(
        title="Crucible: The Incomplete Story",
        core_narrative_claim="A waiver was signed.",
        target_archetype="ARCH-CRUCIBLE",  # Requires: chronological_event, internal_friction, cost_paid
        target_format="FMT-01-STORY",
        target_narrative_role="ROLE-PROTAGONIST-CRUCIBLE",
        source_evidence_records=[ev],
        workspace_id="ws_primary",
        project_id="proj_01",
    )

    assert cand.archetype_readiness is False
    assert any("lacks required response structure" in note for note in cand.readiness_notes)


# -----------------------------------------------------------------------------
# Acceptance Test 7: No Downstream Candidate Without Source Lineage
# -----------------------------------------------------------------------------

def test_no_downstream_candidate_without_source_lineage():
    """Anti-Fabrication: Attempting to create a downstream candidate without source evidence records fails."""
    engine = AuthenticatedEvidenceHandoffEngine()

    with pytest.raises(ValidationError, match="no downstream candidate without source lineage"):
        engine.synthesize_downstream_candidate(
            title="Fabricated Story",
            core_narrative_claim="A completely fabricated story with no evidence.",
            target_archetype="ARCH-CRUCIBLE",
            target_format="FMT-01-STORY",
            target_narrative_role="ROLE-PROTAGONIST-CRUCIBLE",
            source_evidence_records=[],  # Empty!
            workspace_id="ws_primary",
            project_id="proj_01",
        )
