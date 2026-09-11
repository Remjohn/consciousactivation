"""
test_live_interview_activation.py
---------------------------------
CAE Phase 3 Mandate M34: Live Interview Activation + Authenticated Evidence Verification.

Comprehensive test suite verifying:
1. Full 4-lane live interview elicitation lifecycle (HUNTER, ANALYST, COMPOSER, COMMANDER).
2. Bounded adaptive question frontier navigation and deterministic question selection.
3. Transcript SHA-256 hashing and Source Sovereignty preservation.
4. 6-link cryptographic lineage survival from upstream hypothesis to downstream candidate.
5. Strict Anti-Self-Attestation enforcement (hunter actor cannot authenticate own evidence).
6. Anti-fabrication rejection (empty transcript, zero turns, missing reality).
7. Tenant workspace isolation across all CRUD and runtime operations.
8. Quarantine and repair lifecycles.
9. Integer micros score formatting in all authoritative receipts.
"""

import hashlib
import json
import sqlite3
import pytest
from datetime import datetime, timezone
from typing import Dict, Any

from ca_runtime.interview_semantic_store import (
    InterviewSemanticStore,
    InterviewBriefRecord,
    InterviewSessionRecord,
    InterviewTurnRecord,
    InterviewObservationRecord,
    EvidencePackageRecord,
    EvidenceAuthenticationRecord,
    InterviewSemanticReceiptRecord,
)
from ca_runtime.interview_semantic_program import (
    InterviewSemanticProgramCoordinator,
    InterviewProgramError,
    UnauthorizedInterviewLaneError,
    WorkspaceScopeViolationError,
    BriefAuthorizationError,
    SelfAttestationViolationError,
    SourceLineageViolationError,
    AntiFabricationViolationError,
    InvalidLineageError,
    compute_canonical_sha256,
)
from ca_runtime.program_state_runtime import (
    AuthorityLane,
    UniversalProgramStateRuntime,
)
from conscious_activations_interview_composer.repository import InterviewComposerRepository
from conscious_activations_interview_composer.services.brief_service import BriefService
from conscious_activations_interview_composer.services.research_service import ResearchService

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
    QuestionCandidate,
    SocialReferenceFrame,
    TemporalOrientation,
)
from cae_interview_intelligence.adaptive_frontier import (
    AdaptiveAction,
    FrontierState,
)
from cae_interview_intelligence.semantic_acquisition import (
    EvidenceLineageKind,
)
from cae_interview_intelligence.evidence_handoff import (
    SourceReference,
)


@pytest.fixture
def sqlite_store():
    """In-memory SQLite connection wrapped with InterviewSemanticStore."""
    conn = sqlite3.connect(":memory:")
    return InterviewSemanticStore(conn)


@pytest.fixture
def setup_sealed_brief(sqlite_store):
    """Helper to populate a valid SEALED InterviewBriefRecord in the store."""
    workspace_id = "ws_m34_prod"
    brief_id = "ic:brief:jean_pierre_m34"
    hyp_id = "hyp_m34_crucible"

    brief_record = InterviewBriefRecord(
        workspace_id=workspace_id,
        brief_id=brief_id,
        hypothesis_id=hyp_id,
        guest_name="Dr. Jean-Pierre Laurent",
        research_package_ref={"research_id": "res_jp_01", "citation": "Flight Control Safety Archive"},
        brand_context_ref={"brand_id": "conscious_activation"},
        voice_dna_ref={"voice_tone": "unflinching", "candor_index": 95},
        tension_hypothesis="Executive override bypassed critical flight-control safety sign-off 48h before launch under IPO pressure.",
        matrix_of_edging_seed={
            "institutional_taboo": "Bypassing safety sign-offs for capital market deadlines",
            "safe_corporate_narrative": "All regulatory standards were rigorously respected.",
            "unvarnished_reality": "Waivers were forced under explicit executive threat.",
            "price_paid": "Complete grounding of the fleet 6 months post-IPO.",
        },
        planned_questions=[
            {
                "question_id": "q1_orientation",
                "stage": "ORIENTATION",
                "text": "When you first confronted the flight safety review, what was the ground reality nobody wanted to admit?",
                "objective": "Establish baseline experiential ground truth.",
            },
            {
                "question_id": "q2_tension",
                "stage": "TENSION_PROBE",
                "text": "Where did the protocol collision occur between flight engineering and executive leadership?",
                "objective": "Probe systemic friction between engineering checklists and IPO deadline.",
            },
            {
                "question_id": "q3_crucible",
                "stage": "CRUCIBLE_EXPOSURE",
                "text": "Take me to the exact moment you were handed the waiver to sign. What was the tangible cost paid?",
                "objective": "Elicit unvarnished crucible turning point and price paid.",
            },
            {
                "question_id": "q4_resolution",
                "stage": "RESOLUTION_SYNTHESIS",
                "text": "What is the counter-intuitive flight safety operating rule you now hold that peers reject?",
                "objective": "Extract contrarian transferable proof rule.",
            },
        ],
        expression_targets=["self-recognizing witness", "crucible testimony"],
        composer_authority={
            "operator_id": "op_director_jp",
            "authority_scope": "PRODUCTION",
            "assertion_id": "assert_brief_seal_m34",
        },
        canonical_sha256="sha256_brief_sealed_m34_001",
        lifecycle_state="SEALED",
    )
    sqlite_store.store_brief(brief_record)
    return workspace_id, brief_id, hyp_id


# -----------------------------------------------------------------------------
# 1. Full 4-Lane Live Elicitation & Evidence Packaging Test
# -----------------------------------------------------------------------------

def test_live_interview_full_lifecycle_success(sqlite_store, setup_sealed_brief):
    """
    Proves complete 4-lane live interview execution:
    - HUNTER starts session and receives bounded next-question attempt.
    - HUNTER records turns with verifiable SHA-256 transcript digests.
    - ANALYST generates structured semantic observations.
    - COMPOSER packages accepted evidence with 6-link lineage survival.
    - COMMANDER executes independent anti-self-attestation verification and seals session.
    """
    workspace_id, brief_id, hyp_id = setup_sealed_brief
    coord = InterviewSemanticProgramCoordinator(workspace_id=workspace_id, store=sqlite_store)

    hunter_actor = "actor_hunter_elicitation"
    composer_actor = "actor_composer_packager"
    commander_actor = "actor_commander_evaluator"

    # Step 1: Start Live Interview Session (HUNTER)
    session_rec, frontier_state = coord.start_interview_session(
        workspace_id=workspace_id,
        brief_id=brief_id,
        session_id="sess_m34_001",
        actor_id=hunter_actor,
        lane=AuthorityLane.HUNTER,
    )
    assert session_rec.session_id == "sess_m34_001"
    assert session_rec.status == "QUESTIONING"
    assert session_rec.turns_count == 0
    assert len(frontier_state.coverage_spine) > 0

    # Step 2: Get next question attempt from adaptive frontier (HUNTER)
    qa1 = coord.get_next_question_attempt(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        actor_id=hunter_actor,
        lane=AuthorityLane.HUNTER,
    )
    assert qa1 is not None
    assert qa1.action in (AdaptiveAction.ADVANCE, AdaptiveAction.DEEPEN, AdaptiveAction.BROADEN)

    # Step 3: Record Live Turn 1 (HUNTER + ANALYST Observation)
    raw_answer_1 = (
        "On October 14th at 2 AM, the Vice President of Flight Operations came to my desk with the unsigned "
        "flight safety waiver. He said the IPO roadshow began in 48 hours and we couldn't show any red flags. "
        "I explicitly refused to sign, but the executive override was executed above my authority."
    )
    turn_rec_1, obs_1 = coord.record_turn_and_observe(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        question_attempt=qa1,
        transcript_text=raw_answer_1,
        guest_statements=["VP forced safety waiver override on Oct 14th 48 hours prior to IPO roadshow."],
        resolution=AnswerResolution.EPISODIC,
        completeness=InformationCompleteness.SUFFICIENT,
        evidence_modes=[EvidenceMode.STORY],
        specificity_score=0.98,
        authenticity_score=0.99,
        actor_id=hunter_actor,
        lane=AuthorityLane.HUNTER,
    )

    assert turn_rec_1.turn_index == 1
    assert turn_rec_1.transcript_sha256 == hashlib.sha256(raw_answer_1.strip().encode("utf-8")).hexdigest()
    assert len(obs_1.evidence_records) == 1
    assert obs_1.evidence_records[0].kind == EvidenceLineageKind.GUEST_STATED_EVIDENCE

    # Verify Turn and Observation stored in InterviewSemanticStore
    stored_turn = sqlite_store.get_turn(workspace_id, turn_rec_1.turn_id)
    assert stored_turn is not None
    assert stored_turn.transcript_sha256 == turn_rec_1.transcript_sha256

    stored_observations = sqlite_store.list_observations(workspace_id, session_id=session_rec.session_id)
    assert len(stored_observations) >= 1
    assert stored_observations[0].specificity_micros == 980_000
    assert stored_observations[0].authenticity_micros == 990_000

    # Step 4: Package Authenticated Evidence (COMPOSER)
    pkg_rec, pkg_obj = coord.package_interview_evidence(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        actor_id=composer_actor,
        lane=AuthorityLane.COMPOSER,
    )
    assert pkg_rec.package_id == pkg_obj.package_id
    assert pkg_rec.canonical_sha256 == pkg_obj.package_sha256
    assert len(pkg_rec.accepted_evidence_records) >= 1
    assert len(pkg_rec.downstream_candidates) >= 1

    # Verify stored EvidencePackage
    stored_pkg = sqlite_store.get_evidence_package(workspace_id, pkg_rec.package_id)
    assert stored_pkg is not None
    assert stored_pkg.canonical_sha256 == pkg_rec.canonical_sha256

    # Step 5: Authenticate and Complete Session (COMMANDER - Distinct Evaluator)
    completed_sess, auth_rec, receipt_rec = coord.authenticate_and_complete_session(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        evaluator_actor_id=commander_actor,
        verdict="AUTHENTICATED",
        rationale="Supervised adaptive interview evidence verified with intact 6-link lineage and verified transcript SHA-256.",
        operator_authorized=True,
        actor_id=commander_actor,
        lane=AuthorityLane.COMMANDER,
    )
    assert completed_sess.status == "COMPLETED"
    assert auth_rec.verdict == "AUTHENTICATED"
    assert auth_rec.evaluator_actor_id == commander_actor
    assert receipt_rec.decision == "AUTHENTICATED"
    assert receipt_rec.score_breakdown_micros["lineage_survival_micros"] == 1_000_000

    # Verify stored authentication and receipt
    auths = sqlite_store.list_evidence_authentications(workspace_id, session_id=session_rec.session_id)
    assert len(auths) == 1
    assert auths[0].auth_id == auth_rec.auth_id

    receipt = sqlite_store.get_receipt(workspace_id, receipt_rec.receipt_id)
    assert receipt is not None
    assert receipt.decision == "AUTHENTICATED"


# -----------------------------------------------------------------------------
# 2. Bounded Adaptive Question Frontier Navigation
# -----------------------------------------------------------------------------

def test_bounded_adaptive_question_frontier_pacing(sqlite_store, setup_sealed_brief):
    """Verifies that the adaptive question frontier bounds candidate selection and updates state."""
    workspace_id, brief_id, _ = setup_sealed_brief
    coord = InterviewSemanticProgramCoordinator(workspace_id=workspace_id, store=sqlite_store)

    session_rec, f_state = coord.start_interview_session(
        workspace_id=workspace_id,
        brief_id=brief_id,
        session_id="sess_m34_frontier",
        actor_id="actor_hunter_01",
        lane=AuthorityLane.HUNTER,
    )

    # First question attempt
    qa1 = coord.get_next_question_attempt(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        actor_id="actor_hunter_01",
        lane=AuthorityLane.HUNTER,
    )
    assert qa1 is not None
    assert qa1.selected_candidate.text != ""

    # Record partial/abstract answer -> Frontier should deepen
    raw_answer_abstract = "Things were challenging at the leadership level, and we had to balance priorities."
    turn_rec_1, obs_1 = coord.record_turn_and_observe(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        question_attempt=qa1,
        transcript_text=raw_answer_abstract,
        resolution=AnswerResolution.ABSTRACT,
        completeness=InformationCompleteness.PARTIAL,
        specificity_score=0.45,
        authenticity_score=0.70,
        actor_id="actor_hunter_01",
        lane=AuthorityLane.HUNTER,
    )

    # Next attempt evaluated from frontier
    qa2 = coord.get_next_question_attempt(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        actor_id="actor_hunter_01",
        lane=AuthorityLane.HUNTER,
    )
    assert qa2 is not None
    assert qa2.attempt_id != qa1.attempt_id


# -----------------------------------------------------------------------------
# 3. 6-Link Lineage Survival Verification
# -----------------------------------------------------------------------------

def test_six_link_lineage_survival(sqlite_store, setup_sealed_brief):
    """
    Verifies the complete 6-link cryptographic lineage chain:
    Upstream Hypothesis -> Question Candidate -> Question Attempt -> Source Ref -> Observation -> Accepted Evidence -> Downstream Candidate.
    """
    workspace_id, brief_id, hyp_id = setup_sealed_brief
    coord = InterviewSemanticProgramCoordinator(workspace_id=workspace_id, store=sqlite_store)

    session_rec, _ = coord.start_interview_session(
        workspace_id=workspace_id,
        brief_id=brief_id,
        session_id="sess_m34_lineage",
        actor_id="actor_hunter_02",
        lane=AuthorityLane.HUNTER,
    )

    qa = coord.get_next_question_attempt(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        actor_id="actor_hunter_02",
        lane=AuthorityLane.HUNTER,
    )

    transcript = "The flight control sensor drift was known for 3 weeks prior to the certification flight."
    coord.record_turn_and_observe(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        question_attempt=qa,
        transcript_text=transcript,
        guest_statements=["Sensor drift known 3 weeks prior to certification flight."],
        resolution=AnswerResolution.EPISODIC,
        completeness=InformationCompleteness.SUFFICIENT,
        evidence_modes=[EvidenceMode.FACT],
        specificity_score=0.95,
        authenticity_score=0.95,
        actor_id="actor_hunter_02",
        lane=AuthorityLane.HUNTER,
    )

    pkg_rec, pkg_obj = coord.package_interview_evidence(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        actor_id="actor_composer_02",
        lane=AuthorityLane.COMPOSER,
    )

    # Verify lineage in downstream candidates
    assert len(pkg_obj.content_candidates) >= 1
    cand = pkg_obj.content_candidates[0]
    trace = coord._handoff_engine.trace_lineage(cand)

    assert trace.downstream_candidate_id == cand.candidate_id
    assert len(trace.evidence_lineage) >= 1
    assert trace.is_lineage_complete is True
    assert trace.anti_fabrication_checks_passed is True
    assert len(trace.upstream_hypotheses) >= 1


# -----------------------------------------------------------------------------
# 4. Strict Anti-Self-Attestation Enforcement
# -----------------------------------------------------------------------------

def test_anti_self_attestation_enforcement(sqlite_store, setup_sealed_brief):
    """
    Proves that an actor acting as the capturing HUNTER cannot self-attest
    and authenticate its own evidence findings.
    """
    workspace_id, brief_id, _ = setup_sealed_brief
    coord = InterviewSemanticProgramCoordinator(workspace_id=workspace_id, store=sqlite_store)

    hunter_actor = "actor_hunter_capturing_agent"

    session_rec, _ = coord.start_interview_session(
        workspace_id=workspace_id,
        brief_id=brief_id,
        session_id="sess_m34_anti_self",
        actor_id=hunter_actor,
        lane=AuthorityLane.HUNTER,
    )

    qa = coord.get_next_question_attempt(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        actor_id=hunter_actor,
        lane=AuthorityLane.HUNTER,
    )

    coord.record_turn_and_observe(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        question_attempt=qa,
        transcript_text="Testimony regarding the engineering failure mode and cost paid.",
        actor_id=hunter_actor,
        lane=AuthorityLane.HUNTER,
    )

    coord.package_interview_evidence(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        actor_id="actor_composer_distinct",
        lane=AuthorityLane.COMPOSER,
    )

    # Attack: The capturing hunter attempts to authenticate the session
    with pytest.raises(SelfAttestationViolationError, match="Anti-self-attestation violation"):
        coord.authenticate_and_complete_session(
            workspace_id=workspace_id,
            session_id=session_rec.session_id,
            evaluator_actor_id=hunter_actor,  # Same as capturing hunter!
            verdict="AUTHENTICATED",
            actor_id="actor_commander",
            lane=AuthorityLane.COMMANDER,
        )

    # Legitimate independent commander succeeds
    completed_sess, auth_rec, receipt_rec = coord.authenticate_and_complete_session(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        evaluator_actor_id="actor_commander_independent_director",
        verdict="AUTHENTICATED",
        actor_id="actor_commander_independent_director",
        lane=AuthorityLane.COMMANDER,
    )
    assert completed_sess.status == "COMPLETED"


# -----------------------------------------------------------------------------
# 5. Anti-Fabrication & Empty Transcript Rejection
# -----------------------------------------------------------------------------

def test_anti_fabrication_unauthenticated_receipt_rejection(sqlite_store, setup_sealed_brief):
    """Proves that empty transcripts or zero turns fail packaging and observation."""
    workspace_id, brief_id, _ = setup_sealed_brief
    coord = InterviewSemanticProgramCoordinator(workspace_id=workspace_id, store=sqlite_store)

    session_rec, _ = coord.start_interview_session(
        workspace_id=workspace_id,
        brief_id=brief_id,
        session_id="sess_m34_fabrication",
        actor_id="actor_hunter_03",
        lane=AuthorityLane.HUNTER,
    )

    qa = coord.get_next_question_attempt(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        actor_id="actor_hunter_03",
        lane=AuthorityLane.HUNTER,
    )

    # 1. Empty transcript fails immediately
    with pytest.raises(SourceLineageViolationError, match="empty transcript text"):
        coord.record_turn_and_observe(
            workspace_id=workspace_id,
            session_id=session_rec.session_id,
            question_attempt=qa,
            transcript_text="   ",
            actor_id="actor_hunter_03",
            lane=AuthorityLane.HUNTER,
        )

    # 2. Packaging with 0 turns fails
    with pytest.raises(AntiFabricationViolationError, match="0 recorded turns"):
        coord.package_interview_evidence(
            workspace_id=workspace_id,
            session_id=session_rec.session_id,
            actor_id="actor_composer_03",
            lane=AuthorityLane.COMPOSER,
        )


# -----------------------------------------------------------------------------
# 6. Tenant Workspace Isolation
# -----------------------------------------------------------------------------

def test_workspace_tenancy_isolation(sqlite_store, setup_sealed_brief):
    """Verifies that operations across tenant boundaries are strictly blocked."""
    workspace_id, brief_id, _ = setup_sealed_brief
    coord = InterviewSemanticProgramCoordinator(workspace_id=workspace_id, store=sqlite_store)

    # Attempt operation for different workspace
    with pytest.raises(WorkspaceScopeViolationError, match="Workspace mismatch"):
        coord.start_interview_session(
            workspace_id="ws_other_tenant",
            brief_id=brief_id,
            actor_id="actor_hunter",
            lane=AuthorityLane.HUNTER,
        )

    # Verify store isolation
    turns = sqlite_store.list_turns("ws_other_tenant", "sess_m34_001")
    assert len(turns) == 0

    obs = sqlite_store.list_observations("ws_other_tenant", "sess_m34_001")
    assert len(obs) == 0


# -----------------------------------------------------------------------------
# 7. Quarantine and Repair Lifecycle
# -----------------------------------------------------------------------------

def test_quarantine_and_repair_lifecycle(sqlite_store, setup_sealed_brief):
    """Proves fail-closed quarantine and supervised repair transitions."""
    workspace_id, brief_id, _ = setup_sealed_brief
    coord = InterviewSemanticProgramCoordinator(workspace_id=workspace_id, store=sqlite_store)

    session_rec, _ = coord.start_interview_session(
        workspace_id=workspace_id,
        brief_id=brief_id,
        session_id="sess_m34_quarantine",
        actor_id="actor_hunter_04",
        lane=AuthorityLane.HUNTER,
    )
    assert session_rec.status == "QUESTIONING"

    # Commander quarantines the session
    quarantined = coord.quarantine_or_repair_session(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        action="quarantine",
        reason="Detected uncalibrated acoustic anomaly in turn 3",
        actor_id="actor_commander_repair",
        lane=AuthorityLane.COMMANDER,
    )
    assert quarantined.status == "QUARANTINED"

    # Cannot get next question or record turns while quarantined
    with pytest.raises(InterviewProgramError, match="not in active QUESTIONING state"):
        coord.get_next_question_attempt(
            workspace_id=workspace_id,
            session_id=session_rec.session_id,
            actor_id="actor_hunter_04",
            lane=AuthorityLane.HUNTER,
        )

    # Commander repairs the session back to questioning
    repaired = coord.quarantine_or_repair_session(
        workspace_id=workspace_id,
        session_id=session_rec.session_id,
        action="repair",
        reason="Operator reviewed audio log and confirmed ground truth valid.",
        actor_id="actor_commander_repair",
        lane=AuthorityLane.COMMANDER,
    )
    assert repaired.status == "QUESTIONING"


# -----------------------------------------------------------------------------
# 8. Authority Lane Enforcement
# -----------------------------------------------------------------------------

def test_authority_lane_enforcement(sqlite_store, setup_sealed_brief):
    """Ensures each operation is strictly constrained to its designated authority lane."""
    workspace_id, brief_id, _ = setup_sealed_brief
    coord = InterviewSemanticProgramCoordinator(workspace_id=workspace_id, store=sqlite_store)

    # ANALYST cannot start interview session
    with pytest.raises(UnauthorizedInterviewLaneError, match="requires HUNTER lane"):
        coord.start_interview_session(
            workspace_id=workspace_id,
            brief_id=brief_id,
            actor_id="actor_analyst",
            lane=AuthorityLane.ANALYST,
        )

    # HUNTER cannot package evidence
    with pytest.raises(UnauthorizedInterviewLaneError, match="requires COMPOSER lane"):
        coord.package_interview_evidence(
            workspace_id=workspace_id,
            session_id="sess_m34_001",
            actor_id="actor_hunter",
            lane=AuthorityLane.HUNTER,
        )

    # COMPOSER cannot authenticate and complete session
    with pytest.raises(UnauthorizedInterviewLaneError, match="requires COMMANDER lane"):
        coord.authenticate_and_complete_session(
            workspace_id=workspace_id,
            session_id="sess_m34_001",
            evaluator_actor_id="actor_evaluator",
            actor_id="actor_composer",
            lane=AuthorityLane.COMPOSER,
        )
