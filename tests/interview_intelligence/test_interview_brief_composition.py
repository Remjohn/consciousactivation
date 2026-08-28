"""
test_interview_brief_composition.py
-----------------------------------
Tests the composition of InterviewBriefs across multiple guest domains and safety configs.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "interview-intelligence" / "src"))

from cae_interview_intelligence.composer import InterviewBriefComposer
from cae_interview_intelligence.domain import DesiredEvidenceClass, QuestionStage


def test_brief_composition_evidence_mapping():
    brief = InterviewBriefComposer.compose_standard_brief(
        workspace_id="ws-medical-health",
        hypothesis_id="HYP-ICU-001",
        guest_id="GST-SURGEON",
        audience_id="AUD-RESIDENTS",
        target_activation="Shift from emotional suppression to psychological safety",
        context_premise="Surgical training culture historically penalizes vulnerability.",
        collision_thesis="Vulnerability is the foundation of surgical error prevention.",
        orientation_prompt="Walk us through your typical handoff routine at 6:00 AM.",
        tension_prompt="When was the first time you noticed a senior surgeon make an error?",
        crucible_prompt="Describe the exact case where speaking up cost you professional standing.",
        resolution_prompt="What protocol did your department implement to permanently protect junior staff?",
        forbidden_territories=["Active malpractice litigation cases"],
    )

    assert brief.edging_config.forbidden_territories == ["Active malpractice litigation cases"]
    assert brief.question_progression[1].expected_evidence_class == DesiredEvidenceClass.FAILURE_ANALYSIS
    assert brief.question_progression[2].expected_evidence_class == DesiredEvidenceClass.CRUCIBLE_MOMENT
