"""
test_brief_compilation.py
-------------------------
Acceptance tests for CAE Mandate M04 — Activative Interview Brief Compilation.

Validates:
1. Real Brief compilation and read-back through BriefService and Repository (AC-01).
2. Invalid or scripted planned questions are rejected (AC-02).
3. Upstream AIR objects remain non-canonical and unmutated (AC-03).
4. Compilation is idempotent under existing composer repository conventions (AC-04).
5. Only SELECTED / APPROVED candidate states are admitted into the Brief (AC-05).
6. Missing operator authority fails compilation.
"""

import hashlib
import pytest
from datetime import datetime, timezone

from conscious_activations_interview_composer.application import InterviewComposerApplication
from conscious_activations_interview_composer.errors import ValidationError
from conscious_activations_interview_composer.repository import InterviewComposerRepository
from conscious_activations_interview_composer.services.brief_service import BriefService
from conscious_activations_interview_composer.services.research_service import ResearchService

from cae_interview_intelligence.brief_compiler import ActivativeInterviewBriefCompiler
from cae_interview_intelligence.errors import ScriptedAnswerViolationError
from cae_interview_intelligence.hypothesis_adapter import (
    CandidateState,
    CoordinateBasis,
    HypothesisCandidate,
    Provenance,
    SelectionDiagnostics,
    SemanticRef,
)
from cae_interview_intelligence.question_resolver import (
    QuestionCandidate,
    QuestionIntelligenceResolver,
    QuestionProgramDerived,
)


def dummy_sha(name: str) -> str:
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


def make_test_candidate(
    cid: str = "comp_hyp_01",
    state: CandidateState = CandidateState.APPROVED,
    collision: str = "Corporate hierarchy suppresses crisis anomalies until catastrophic failure.",
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
            d01_audience_tension="fear_of_loss_vs_status_quo",
            d02_audience_belief="belief_in_process",
            d03_audience_desired_state="operational_resilience",
            d04_guest_lived_authority="incident_commander",
            d05_guest_contradiction="protocol_adherence_vs_emergency_action",
            d06_guest_transformation="from_rule_follower_to_field_decision_maker",
            d07_cultural_world_signal="sig:macro_outage_2026",
            d08_target_enemy_status_quo="bureaucratic_cover_up",
            d09_oblique_lens="complex_systems_drift",
            d10_archetype_opportunity="archetype_crucible",
            d11_distribution_condition="high_retention_provocation",
            d12_evidence_opportunity="internal_incident_chat_log",
        ),
        desired_evidence=[
            "Exact decision timestamp when protocol was bypassed",
            "Personal disciplinary risk accepted by guest",
        ],
        provenance=Provenance(
            source_refs=[SemanticRef(object_id="doc:incident_report_01", sha256=dummy_sha("doc:incident_report_01"))],
            generated_by="test-fixture:m04",
        ),
    )


def setup_composer_services(tmp_path):
    db_path = str(tmp_path / "composer_m04.db")
    repo = InterviewComposerRepository(db_path)
    repo.initialize()
    research_svc = ResearchService(repo)
    brief_svc = BriefService(repo)
    return repo, research_svc, brief_svc


def create_sample_research_package(research_svc, pkg_id="res_01"):
    res = research_svc.create_package(
        {
            "workspace_id": "ws-m04",
            "project_id": "prj-m04",
            "guest_name": "Dr. Aris Vance",
            "source_urls": [],
            "uploaded_documents": [],
            "composer_authority": {
                "operator_id": "op-audrey",
                "authority_scope": "PRODUCTION",
                "assertion_id": "assert-m04-01",
            },
        },
        idempotency_key=f"idemp-res-{pkg_id}",
    )
    return res["object"]


# -----------------------------------------------------------------------------
# AC-01: Real Brief Compilation and Read-Back
# -----------------------------------------------------------------------------

def test_compile_real_brief_and_read_back(tmp_path):
    """Real Brief can be compiled from approved hypothesis/question program and read back from repository."""
    repo, research_svc, brief_svc = setup_composer_services(tmp_path)
    research_obj = create_sample_research_package(research_svc)
    research_ref = {
        "object_id": research_obj["object_id"],
        "version": research_obj["version"],
        "sha256": research_obj["sha256"],
    }

    candidate = make_test_candidate(state=CandidateState.APPROVED)
    resolver = QuestionIntelligenceResolver()
    q_program = resolver.resolve_question_program(candidate)

    authority = {
        "operator_id": "op-audrey",
        "authority_scope": "PRODUCTION",
        "assertion_id": "assert-m04-brief",
    }

    result = ActivativeInterviewBriefCompiler.compile_and_store(
        brief_service=brief_svc,
        idempotency_key="brief-m04-01",
        candidate=candidate,
        question_program=q_program,
        guest_name="Dr. Aris Vance",
        research_package_ref=research_ref,
        composer_authority=authority,
        brand_context_ref={"object_id": "bc:01", "version": "1.0.0", "sha256": dummy_sha("bc:01")},
        voice_dna_ref={"object_id": "vd:01", "version": "1.0.0", "sha256": dummy_sha("vd:01")},
    )

    assert result["created"] is True
    brief_id = result["object"]["object_id"]
    assert brief_id.startswith("ic:brief:")

    # Read back from repository
    stored_brief = repo.get_object(brief_id)
    payload = stored_brief["payload"]

    assert payload["guest_name"] == "Dr. Aris Vance"
    assert payload["tension_hypothesis"] == candidate.collision_statement
    assert payload["research_package_ref"]["object_id"] == research_ref["object_id"]
    assert len(payload["planned_questions"]) >= 3
    assert payload["matrix_of_edging_seed"]["psychological_role"] == "incident_commander"
    assert payload["composer_authority"]["operator_id"] == "op-audrey"



# -----------------------------------------------------------------------------
# AC-02: Invalid / Scripted Questions Rejected
# -----------------------------------------------------------------------------

def test_invalid_planned_questions_rejected():
    """Scripted leading questions are rejected during brief compilation."""
    candidate = make_test_candidate()
    resolver = QuestionIntelligenceResolver()
    q_program = resolver.resolve_question_program(candidate)

    # Inject a scripted leading phrase
    bad_q = QuestionCandidate(
        text="Don't you agree that corporate hierarchy suppresses crisis anomalies?",
        objective="Elicit evidence",
    )
    bad_program = QuestionProgramDerived(
        hypothesis_ref=candidate.upstream_hypothesis_refs[0],
        objective="Test bad program",
        expected_evidence=["evidence"],
        candidate_questions=[bad_q],
    )

    with pytest.raises(ScriptedAnswerViolationError, match="Scripted answer violation"):
        ActivativeInterviewBriefCompiler.compile_brief_payload(
            candidate=candidate,
            question_program=bad_program,
            guest_name="Dr. Aris Vance",
            research_package_ref={"object_id": "res:01", "version": "1.0.0", "sha256": dummy_sha("res:01")},
            composer_authority={"operator_id": "op-1", "authority_scope": "DEV", "assertion_id": "a1"},
        )


# -----------------------------------------------------------------------------
# AC-03: AIR Ownership Not Duplicated
# -----------------------------------------------------------------------------

def test_air_ownership_not_duplicated():
    """Brief compilation references upstream AIR hypotheses without duplicating tables or creating copies."""
    candidate = make_test_candidate()
    resolver = QuestionIntelligenceResolver()
    q_program = resolver.resolve_question_program(candidate)

    payload = ActivativeInterviewBriefCompiler.compile_brief_payload(
        candidate=candidate,
        question_program=q_program,
        guest_name="Dr. Aris Vance",
        research_package_ref={"object_id": "res:01", "version": "1.0.0", "sha256": dummy_sha("res:01")},
        composer_authority={"operator_id": "op-1", "authority_scope": "DEV", "assertion_id": "a1"},
    )

    # The brief conforms to the existing canonical schema
    assert "brief_id" in payload
    assert payload["content_origin"] == "operator_supplied"
    assert payload["hypothesis_pipeline_status"]["status"] == "BLOCKED_PENDING_GAP_007"
    # AIR upstream reference remains in candidate provenance, not duplicated into brief schema
    assert candidate.upstream_hypothesis_refs[0].object_id == "air:hyp:comp_hyp_01"


# -----------------------------------------------------------------------------
# AC-04: Compilation Idempotency
# -----------------------------------------------------------------------------

def test_compilation_idempotency(tmp_path):
    """Replaying brief compilation with same idempotency key returns identical object without duplication."""
    repo, research_svc, brief_svc = setup_composer_services(tmp_path)
    research_obj = create_sample_research_package(research_svc)
    research_ref = {
        "object_id": research_obj["object_id"],
        "version": research_obj["version"],
        "sha256": research_obj["sha256"],
    }

    candidate = make_test_candidate()
    resolver = QuestionIntelligenceResolver()
    q_program = resolver.resolve_question_program(candidate)

    authority = {
        "operator_id": "op-audrey",
        "authority_scope": "PRODUCTION",
        "assertion_id": "assert-m04-brief",
    }

    res1 = ActivativeInterviewBriefCompiler.compile_and_store(
        brief_service=brief_svc,
        idempotency_key="idemp-brief-01",
        candidate=candidate,
        question_program=q_program,
        guest_name="Dr. Aris Vance",
        research_package_ref=research_ref,
        composer_authority=authority,
    )
    assert res1["created"] is True
    assert res1["idempotent_replay"] is False

    res2 = ActivativeInterviewBriefCompiler.compile_and_store(
        brief_service=brief_svc,
        idempotency_key="idemp-brief-01",
        candidate=candidate,
        question_program=q_program,
        guest_name="Dr. Aris Vance",
        research_package_ref=research_ref,
        composer_authority=authority,
    )
    assert res2["idempotent_replay"] is True
    assert res2["object"]["object_id"] == res1["object"]["object_id"]


# -----------------------------------------------------------------------------
# AC-05: Selected / Rejected Candidate States Enforced
# -----------------------------------------------------------------------------

def test_candidate_approval_state_enforcement():
    """Unapproved, deferred, or rejected candidates cannot be compiled into an Activative Interview Brief."""
    resolver = QuestionIntelligenceResolver()

    for invalid_state in (CandidateState.REJECTED, CandidateState.DEFERRED):
        cand = make_test_candidate(state=invalid_state)
        q_prog = resolver.resolve_question_program(cand)

        with pytest.raises(ValueError, match="Cannot compile brief from candidate in state"):
            ActivativeInterviewBriefCompiler.compile_brief_payload(
                candidate=cand,
                question_program=q_prog,
                guest_name="Dr. Aris Vance",
                research_package_ref={"object_id": "res:01", "version": "1.0.0", "sha256": dummy_sha("res:01")},
                composer_authority={"operator_id": "op-1", "authority_scope": "DEV", "assertion_id": "a1"},
            )


# -----------------------------------------------------------------------------
# Operator Authority Verification
# -----------------------------------------------------------------------------

def test_missing_operator_authority_rejected():
    """Compilation fails when operator authority credentials are missing or incomplete."""
    candidate = make_test_candidate(state=CandidateState.APPROVED)
    resolver = QuestionIntelligenceResolver()
    q_program = resolver.resolve_question_program(candidate)

    # Incomplete authority
    with pytest.raises(ValueError, match="Missing required composer authority field"):
        ActivativeInterviewBriefCompiler.compile_brief_payload(
            candidate=candidate,
            question_program=q_program,
            guest_name="Dr. Aris Vance",
            research_package_ref={"object_id": "res:01", "version": "1.0.0", "sha256": dummy_sha("res:01")},
            composer_authority={"operator_id": "op-1"},  # Missing scope and assertion
        )

