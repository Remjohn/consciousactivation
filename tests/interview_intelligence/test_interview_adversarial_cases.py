"""
test_interview_adversarial_cases.py
-----------------------------------
Adversarial tests for scripted leading questions, unauthenticated runs, and technical-success false proofs.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "interview-intelligence" / "src"))

import pytest

from cae_interview_intelligence.composer import InterviewBriefComposer
from cae_interview_intelligence.domain import (
    InterviewSessionResult,
    InterviewTurnResponse,
    QuestionStage,
)
from cae_interview_intelligence.errors import (
    GenericResponseFailureError,
    ScriptedAnswerViolationError,
    UnauthenticatedSessionError,
)
from cae_interview_intelligence.verifier import InterviewSessionVerifier


def test_scripted_leading_question_rejection():
    # Attempting to compose an interview brief with a presumptive, leading question
    with pytest.raises(ScriptedAnswerViolationError, match="Scripted answer violation"):
        InterviewBriefComposer.compose_standard_brief(
            workspace_id="ws-client-99",
            hypothesis_id="HYP-1",
            guest_id="GST-1",
            audience_id="AUD-1",
            target_activation="Target Shift",
            context_premise="Context premise with more than twenty characters.",
            collision_thesis="Collision thesis with more than fifteen characters.",
            orientation_prompt="Don't you agree that modern leadership is fundamentally broken?",  # Presumptive!
            tension_prompt="Valid tension prompt over fifteen characters.",
            crucible_prompt="Valid crucible prompt over fifteen characters.",
            resolution_prompt="Valid resolution prompt over fifteen characters.",
        )


def test_technical_success_false_proof_rejection():
    # All 4 questions executed, but every answer was generic platitudes / PR slop
    turns = [
        InterviewTurnResponse(
            question_id="QST-1",
            stage=QuestionStage.ORIENTATION,
            transcript_text="I think leadership is all about synergy, passion, and thinking outside the box.",
            specificity_score=0.20,
            authenticity_score=0.30,
            contains_lived_evidence=False,
            is_generic_slop=True,
        ),
        InterviewTurnResponse(
            question_id="QST-2",
            stage=QuestionStage.TENSION_PROBE,
            transcript_text="We always strive to align stakeholder values and maximize win-win outcomes.",
            specificity_score=0.15,
            authenticity_score=0.25,
            contains_lived_evidence=False,
            is_generic_slop=True,
        ),
        InterviewTurnResponse(
            question_id="QST-3",
            stage=QuestionStage.CRUCIBLE_EXPOSURE,
            transcript_text="Challenges are just opportunities in disguise for growth mindsets.",
            specificity_score=0.10,
            authenticity_score=0.20,
            contains_lived_evidence=False,
            is_generic_slop=True,
        ),
        InterviewTurnResponse(
            question_id="QST-4",
            stage=QuestionStage.RESOLUTION_SYNTHESIS,
            transcript_text="Never give up and always believe in your dream.",
            specificity_score=0.10,
            authenticity_score=0.15,
            contains_lived_evidence=False,
            is_generic_slop=True,
        ),
    ]

    session = InterviewSessionResult(
        brief_id="BRF-TEST",
        workspace_id="ws-client-99",
        guest_id="GST-1",
        turns=turns,
        is_authenticated=True,
    )

    with pytest.raises(GenericResponseFailureError, match="Technical Success False-Proof"):
        InterviewSessionVerifier.verify_session_result(session)

    assert session.execution_status == "INCOMPLETE"


def test_unauthenticated_session_rejection():
    # Session executed without human presence / voice authentication
    session = InterviewSessionResult(
        brief_id="BRF-TEST",
        workspace_id="ws-client-99",
        guest_id="GST-1",
        turns=[],
        is_authenticated=False,  # Unauthenticated!
    )

    with pytest.raises(UnauthenticatedSessionError, match="failed human presence/voice authentication"):
        InterviewSessionVerifier.verify_session_result(session)

    assert session.execution_status == "UNAUTHENTICATED"
