"""
test_adaptive_follow_up_and_edging.py
-------------------------------------
Tests adaptive follow-up policies and Matrix of Edging pressure configurations.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "interview-intelligence" / "src"))

from cae_interview_intelligence.domain import (
    AdaptiveFollowUpPolicy,
    InterviewTurnResponse,
    MatrixOfEdgingConfig,
    QuestionStage,
)


def test_adaptive_policy_defaults_and_triggers():
    policy = AdaptiveFollowUpPolicy()

    assert "specific episodic scene" in policy.on_intellectualization
    assert "specific numbers" in policy.on_vagueness
    assert "mirror" in policy.on_defensiveness
    assert policy.max_adaptive_probes_per_stage == 2


def test_matrix_of_edging_safety_limits():
    edging = MatrixOfEdgingConfig(
        target_vulnerability_depth=0.85,
        pressure_gradient="PROGRESSIVE_EXPONENTIAL",
        forbidden_territories=["Divorce proceedings", "NDA proprietary code"],
        safety_ceiling_threshold=0.90,
    )

    assert edging.safety_ceiling_threshold == 0.90
    assert len(edging.forbidden_territories) == 2
