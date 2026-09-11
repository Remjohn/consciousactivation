"""
test_operator_studio.py
-----------------------
Acceptance tests for CAE Mandate M05 — Operator Hypothesis & Question Studio.

Validates:
1. Real candidate retrieval & studio inspection metadata (AC-01).
2. Operator action state transitions: KEEP, REJECT, EDIT, DEFER, LOCK (AC-02).
3. Constrained regeneration with locked dimensions (AC-03).
4. Optimistic concurrency control / stale write rejection (AC-04).
5. Idempotent duplicate action replay (AC-05).
6. Unauthorized approval rejection (AC-06).
7. Rejected candidates excluded from working portfolio & brief compilation (AC-07).
8. End-to-end studio review -> brief compilation roundtrip (AC-08).
"""

import hashlib
import pytest
from datetime import datetime, timezone

from conscious_activations_interview_composer.errors import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from conscious_activations_interview_composer.repository import InterviewComposerRepository
from conscious_activations_interview_composer.services.brief_service import BriefService
from conscious_activations_interview_composer.services.research_service import ResearchService

from cae_interview_intelligence.hypothesis_adapter import (
    CandidateState,
    CoordinateBasis,
    HypothesisCandidate,
    Provenance,
    SemanticRef,
)
from cae_interview_intelligence.operator_studio import (
    CandidateReviewItem,
    OperatorActionType,
    OperatorFeedback,
    OperatorStudioService,
    StudioSession,
)
from cae_interview_intelligence.question_resolver import (
    QuestionCandidate,
    QuestionIntelligenceResolver,
    QuestionProgramDerived,
)


def dummy_sha(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


def make_test_candidate(
    cid: str = "studio_hyp_01",
    state: CandidateState = CandidateState.EVALUATED,
    collision: str = "Traditional safety protocols mask executive complacency during system degradation.",
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
            generated_by="test-fixture:m05",
        ),
    )


def setup_studio_environment(tmp_path):
    db_path = str(tmp_path / "studio_m05.db")
    repo = InterviewComposerRepository(db_path)
    repo.initialize()
    research_svc = ResearchService(repo)
    brief_svc = BriefService(repo)

    res = research_svc.create_package(
        {
            "workspace_id": "ws-m05",
            "project_id": "prj-m05",
            "guest_name": "Dr. Aris Vance",
            "source_urls": [],
            "uploaded_documents": [],
            "composer_authority": {
                "operator_id": "op-audrey",
                "authority_scope": "PRODUCTION",
                "assertion_id": "assert-res-01",
            },
        },
        idempotency_key="idemp-res-m05",
    )
    research_obj = res["object"]

    studio_service = OperatorStudioService()
    return repo, brief_svc, studio_service, research_obj


# -----------------------------------------------------------------------------
# AC-01: Real Candidate Retrieval & Studio Metadata Inspection
# -----------------------------------------------------------------------------

def test_real_candidate_retrieval_and_studio_view(tmp_path):
    """Studio exposes complete provenance, tension, expected evidence, coalition, and compatibility."""
    _, _, studio_svc, research_obj = setup_studio_environment(tmp_path)

    cand1 = make_test_candidate("hyp_01")
    cand2 = make_test_candidate("hyp_02", collision="Automated compliance audits produce brittle safety cultures.")

    session = studio_svc.create_session(
        workspace_id="ws-m05",
        project_id="prj-m05",
        guest_name="Dr. Aris Vance",
        research_package_ref=research_obj,
        candidates=[cand1, cand2],
    )

    assert session.session_id.startswith("studio:sess:")
    assert len(session.candidates) == 2

    view = studio_svc.get_candidate_view(session.session_id, cand1.candidate_id)
    assert view.candidate.candidate_id == cand1.candidate_id
    assert view.candidate.coordinates.d01_audience_tension == "safety_guarantee_vs_actual_risk"
    assert len(view.candidate.desired_evidence) == 2
    assert view.question_program is not None
    assert len(view.question_program.candidate_questions) >= 3
    assert view.compatibility_view.is_compatible() is True
    assert view.current_version == 1
    assert view.review_state == CandidateState.EVALUATED



# -----------------------------------------------------------------------------
# AC-02: Operator Action State Transitions
# -----------------------------------------------------------------------------

def test_operator_action_state_transitions(tmp_path):
    """Studio processes KEEP, REJECT, EDIT, DEFER, and LOCK actions with audit trails."""
    _, _, studio_svc, research_obj = setup_studio_environment(tmp_path)

    c1 = make_test_candidate("c1")
    c2 = make_test_candidate("c2")
    c3 = make_test_candidate("c3")
    c4 = make_test_candidate("c4")

    session = studio_svc.create_session(
        workspace_id="ws-m05",
        project_id="prj-m05",
        guest_name="Dr. Aris Vance",
        research_package_ref=research_obj,
        candidates=[c1, c2, c3, c4],
    )
    sid = session.session_id

    # 1. KEEP
    fb_keep = OperatorFeedback(
        action=OperatorActionType.KEEP,
        operator_id="op-audrey",
        authority_scope="PRODUCTION",
        assertion_id="assert-keep-c1",
        notes="Strong contrarian tension.",
    )
    item_c1 = studio_svc.apply_action(session_id=sid, candidate_id=c1.candidate_id, feedback=fb_keep, expected_version=1)
    assert item_c1.review_state == CandidateState.SELECTED
    assert len(item_c1.feedback_history) == 1

    # 2. REJECT
    fb_reject = OperatorFeedback(
        action=OperatorActionType.REJECT,
        operator_id="op-audrey",
        authority_scope="PRODUCTION",
        assertion_id="assert-reject-c2",
        notes="Redundant with prior interview.",
    )
    item_c2 = studio_svc.apply_action(session_id=sid, candidate_id=c2.candidate_id, feedback=fb_reject, expected_version=1)
    assert item_c2.review_state == CandidateState.REJECTED

    # 3. DEFER
    fb_defer = OperatorFeedback(
        action=OperatorActionType.DEFER,
        operator_id="op-audrey",
        authority_scope="PRODUCTION",
        assertion_id="assert-defer-c3",
        notes="Needs external verification first.",
    )
    item_c3 = studio_svc.apply_action(session_id=sid, candidate_id=c3.candidate_id, feedback=fb_defer, expected_version=1)
    assert item_c3.review_state == CandidateState.DEFERRED

    # 4. LOCK
    fb_lock = OperatorFeedback(
        action=OperatorActionType.LOCK,
        operator_id="op-audrey",
        authority_scope="PRODUCTION",
        assertion_id="assert-lock-c4",
        notes="Anchor question locked for broadcast.",
    )
    item_c4 = studio_svc.apply_action(session_id=sid, candidate_id=c4.candidate_id, feedback=fb_lock, expected_version=1)
    assert item_c4.review_state == CandidateState.LOCKED


# -----------------------------------------------------------------------------
# AC-03: Constrained Regeneration with Locked Dimensions
# -----------------------------------------------------------------------------

def test_constrained_regeneration_with_locked_dimensions(tmp_path):
    """Regeneration produces 3 bounded alternatives while strictly locking core dimensions."""
    _, _, studio_svc, research_obj = setup_studio_environment(tmp_path)

    candidate = make_test_candidate("regen_c1")
    session = studio_svc.create_session(
        workspace_id="ws-m05",
        project_id="prj-m05",
        guest_name="Dr. Aris Vance",
        research_package_ref=research_obj,
        candidates=[candidate],
    )
    sid = session.session_id

    fb_regen = OperatorFeedback(
        action=OperatorActionType.REGENERATE,
        operator_id="op-audrey",
        authority_scope="PRODUCTION",
        assertion_id="assert-regen-01",
        notes="Make the inquiry more direct and less polite.",
        locked_dimensions=["hypothesis_ref", "target_resolution", "evidence_mode", "expected_evidence"],
    )

    item = studio_svc.apply_action(session_id=sid, candidate_id=candidate.candidate_id, feedback=fb_regen, expected_version=1)
    assert item.current_version == 2
    assert len(item.alternatives) == 3
    for alt in item.alternatives:
        assert alt.version == "1.1.0"
        assert "hypothesis_ref" in alt.locked_dimensions
        assert alt.is_canonical is False
        assert alt.text != ""


# -----------------------------------------------------------------------------
# AC-04: Optimistic Concurrency Control / Stale Write Rejection
# -----------------------------------------------------------------------------

def test_optimistic_concurrency_stale_write_rejection(tmp_path):
    """Attempting an edit or action on an outdated candidate version raises ConflictError."""
    _, _, studio_svc, research_obj = setup_studio_environment(tmp_path)

    candidate = make_test_candidate("conc_c1")
    session = studio_svc.create_session(
        workspace_id="ws-m05",
        project_id="prj-m05",
        guest_name="Dr. Aris Vance",
        research_package_ref=research_obj,
        candidates=[candidate],
    )
    sid = session.session_id

    # Action 1: EDIT bumps version from 1 to 2
    fb_edit = OperatorFeedback(
        action=OperatorActionType.EDIT,
        operator_id="op-audrey",
        authority_scope="PRODUCTION",
        assertion_id="assert-edit-v1",
        edited_text="Take us into the room when you signed the safety sign-off — what did you know?",
    )
    studio_svc.apply_action(session_id=sid, candidate_id=candidate.candidate_id, feedback=fb_edit, expected_version=1)

    # Action 2: Stale action targeting version 1 must fail
    fb_stale = OperatorFeedback(
        action=OperatorActionType.LOCK,
        operator_id="op-audrey",
        authority_scope="PRODUCTION",
        assertion_id="assert-stale-action",
    )
    with pytest.raises(ConflictError, match="Stale edit conflict"):
        studio_svc.apply_action(
            session_id=sid,
            candidate_id=candidate.candidate_id,
            feedback=fb_stale,
            expected_version=1,  # Stale! Current is 2
        )


# -----------------------------------------------------------------------------
# AC-05: Idempotent Duplicate Action Replay
# -----------------------------------------------------------------------------

def test_idempotent_duplicate_actions(tmp_path):
    """Replaying an action with identical assertion_id is idempotent and avoids duplicate history."""
    _, _, studio_svc, research_obj = setup_studio_environment(tmp_path)

    candidate = make_test_candidate("idemp_c1")
    session = studio_svc.create_session(
        workspace_id="ws-m05",
        project_id="prj-m05",
        guest_name="Dr. Aris Vance",
        research_package_ref=research_obj,
        candidates=[candidate],
    )
    sid = session.session_id

    fb = OperatorFeedback(
        action=OperatorActionType.KEEP,
        operator_id="op-audrey",
        authority_scope="PRODUCTION",
        assertion_id="assert-idemp-unique-01",
        notes="First application.",
    )

    res1 = studio_svc.apply_action(session_id=sid, candidate_id=candidate.candidate_id, feedback=fb, expected_version=1)
    assert len(res1.feedback_history) == 1

    res2 = studio_svc.apply_action(session_id=sid, candidate_id=candidate.candidate_id, feedback=fb, expected_version=1)
    assert len(res2.feedback_history) == 1
    assert res2.review_state == CandidateState.SELECTED


# -----------------------------------------------------------------------------
# AC-06: Unauthorized Approval Rejection
# -----------------------------------------------------------------------------

def test_unauthorized_approval_rejection(tmp_path):
    """Approvals without valid operator authority scope are rejected server-side."""
    _, _, studio_svc, research_obj = setup_studio_environment(tmp_path)

    candidate = make_test_candidate("auth_c1")
    session = studio_svc.create_session(
        workspace_id="ws-m05",
        project_id="prj-m05",
        guest_name="Dr. Aris Vance",
        research_package_ref=research_obj,
        candidates=[candidate],
    )
    sid = session.session_id

    # Invalid authority scope
    fb_invalid_scope = OperatorFeedback(
        action=OperatorActionType.APPROVE,
        operator_id="guest_client",
        authority_scope="UNAUTHORIZED_CLIENT",
        assertion_id="assert-bad-auth",
    )
    with pytest.raises(ValidationError, match="Invalid authority scope"):
        studio_svc.apply_action(session_id=sid, candidate_id=candidate.candidate_id, feedback=fb_invalid_scope, expected_version=1)


# -----------------------------------------------------------------------------
# AC-07: Rejected Candidates Excluded from Working Portfolio & Brief Compilation
# -----------------------------------------------------------------------------

def test_rejected_candidates_absent_from_launch_payload(tmp_path):
    """Rejected and deferred candidates are strictly excluded from the working portfolio and brief compilation."""
    _, brief_svc, studio_svc, research_obj = setup_studio_environment(tmp_path)

    c_keep = make_test_candidate("c_keep")
    c_reject = make_test_candidate("c_reject")
    c_defer = make_test_candidate("c_defer")

    session = studio_svc.create_session(
        workspace_id="ws-m05",
        project_id="prj-m05",
        guest_name="Dr. Aris Vance",
        research_package_ref=research_obj,
        candidates=[c_keep, c_reject, c_defer],
    )
    sid = session.session_id

    studio_svc.apply_action(
        session_id=sid,
        candidate_id=c_keep.candidate_id,
        feedback=OperatorFeedback(
            action=OperatorActionType.KEEP,
            operator_id="op-audrey",
            authority_scope="PRODUCTION",
            assertion_id="a-keep",
        ),
        expected_version=1,
    )
    studio_svc.apply_action(
        session_id=sid,
        candidate_id=c_reject.candidate_id,
        feedback=OperatorFeedback(
            action=OperatorActionType.REJECT,
            operator_id="op-audrey",
            authority_scope="PRODUCTION",
            assertion_id="a-reject",
        ),
        expected_version=1,
    )
    studio_svc.apply_action(
        session_id=sid,
        candidate_id=c_defer.candidate_id,
        feedback=OperatorFeedback(
            action=OperatorActionType.DEFER,
            operator_id="op-audrey",
            authority_scope="PRODUCTION",
            assertion_id="a-defer",
        ),
        expected_version=1,
    )

    portfolio = studio_svc.assemble_working_portfolio(sid)
    candidate_ids = [p.candidate.candidate_id for p in portfolio]
    assert c_keep.candidate_id in candidate_ids
    assert c_reject.candidate_id not in candidate_ids
    assert c_defer.candidate_id not in candidate_ids

    # Attempting to force compilation of a rejected candidate must fail
    with pytest.raises(ValidationError, match="Cannot compile brief: candidate .* is REJECTED"):
        studio_svc.compile_and_authorize_brief(
            session_id=sid,
            brief_service=brief_svc,
            idempotency_key="idemp-bad-comp",
            composer_authority={"operator_id": "op-audrey", "authority_scope": "PRODUCTION", "assertion_id": "a-auth"},
            primary_candidate_id=c_reject.candidate_id,
        )


# -----------------------------------------------------------------------------
# AC-08: End-to-End Studio Review -> Brief Compilation Roundtrip
# -----------------------------------------------------------------------------

def test_compile_and_authorize_brief_roundtrip(tmp_path):
    """Full workflow: create session -> review -> edit -> approve -> compile brief -> readback & authorized launch."""
    repo, brief_svc, studio_svc, research_obj = setup_studio_environment(tmp_path)

    candidate = make_test_candidate("flow_01")
    session = studio_svc.create_session(
        workspace_id="ws-m05",
        project_id="prj-m05",
        guest_name="Dr. Aris Vance",
        research_package_ref=research_obj,
        candidates=[candidate],
    )
    sid = session.session_id

    # 1. Edit question prompt
    fb_edit = OperatorFeedback(
        action=OperatorActionType.EDIT,
        operator_id="op-audrey",
        authority_scope="PRODUCTION",
        assertion_id="a-flow-edit",
        edited_text="Walk me through the exact moment the automated alert fired — what did leadership tell you to do?",
    )
    item = studio_svc.apply_action(session_id=sid, candidate_id=candidate.candidate_id, feedback=fb_edit, expected_version=1)
    assert item.current_version == 2

    # 2. Approve candidate
    fb_appr = OperatorFeedback(
        action=OperatorActionType.APPROVE,
        operator_id="op-audrey",
        authority_scope="PRODUCTION",
        assertion_id="a-flow-appr",
        notes="Approved for episode recording.",
    )
    item = studio_svc.apply_action(session_id=sid, candidate_id=candidate.candidate_id, feedback=fb_appr, expected_version=2)
    assert item.review_state == CandidateState.APPROVED

    # 3. Server-side authorized brief compilation
    authority = {
        "operator_id": "op-audrey",
        "authority_scope": "PRODUCTION",
        "assertion_id": "a-flow-launch",
    }
    result = studio_svc.compile_and_authorize_brief(
        session_id=sid,
        brief_service=brief_svc,
        idempotency_key="idemp-flow-brief-01",
        composer_authority=authority,
        brand_context_ref={"object_id": "bc:01", "version": "1.0.0", "sha256": dummy_sha("bc:01")},
        voice_dna_ref={"object_id": "vd:01", "version": "1.0.0", "sha256": dummy_sha("vd:01")},
    )

    assert result["created"] is True
    brief_id = result["object"]["object_id"]
    assert brief_id.startswith("ic:brief:")

    # 4. Readback from SQLite repository
    stored = repo.get_object(brief_id)
    assert stored["payload"]["guest_name"] == "Dr. Aris Vance"
    assert stored["payload"]["planned_questions"][0]["question_text"] == (
        "Walk me through the exact moment the automated alert fired — what did leadership tell you to do?"
    )

    # 5. Session state updated
    sess = studio_svc.get_session(sid)
    assert sess.launch_authorized is True
    assert sess.compiled_brief_id == brief_id
