"""
test_interview_domain_contracts.py
----------------------------------
Validates InterviewBrief serialization, typing, and schema integrity.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "interview-intelligence" / "src"))

from cae_interview_intelligence.composer import InterviewBriefComposer
from cae_interview_intelligence.domain import (
    InterviewBrief,
    QuestionStage,
)
from cae_interview_intelligence.verifier import InterviewSessionVerifier


def test_interview_brief_serialization_and_verification():
    ws_id = "ws-client-99"

    brief = InterviewBriefComposer.compose_standard_brief(
        workspace_id=ws_id,
        hypothesis_id="HYP-12345",
        guest_id="GST-100",
        audience_id="AUD-200",
        target_activation="Transform acute exhaustion into systemic boundaries",
        context_premise="Over 70% of tech founders report severe burnout during late-stage scaling.",
        collision_thesis="Burnout is an institutional local optimum, not personal weakness.",
        orientation_prompt="When you look at your calendar during that peak crisis in 2022, what was happening?",
        tension_prompt="Where did the board's growth targets directly conflict with team health?",
        crucible_prompt="Take us to the exact room and moment you decided to shut down that division.",
        resolution_prompt="What non-negotiable governance rule did you write immediately after that event?",
    )

    assert brief.brief_id.startswith("BRF-")
    assert len(brief.question_progression) == 4
    assert brief.question_progression[0].stage == QuestionStage.ORIENTATION
    assert brief.question_progression[2].stage == QuestionStage.CRUCIBLE_EXPOSURE

    assert InterviewSessionVerifier.verify_brief(brief) is True
