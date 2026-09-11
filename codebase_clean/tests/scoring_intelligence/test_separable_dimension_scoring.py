"""
test_separable_dimension_scoring.py
-----------------------------------
Tests 8 separable evaluation dimension score calculations and non-compensable gates.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "scoring-intelligence" / "src"))

from cae_scoring_intelligence.domain import DimensionScores, GateStatus
from cae_scoring_intelligence.evaluator import MultiDimensionalCandidateEvaluator


def test_separable_dimension_weights():
    scores = DimensionScores.calculate_composite(
        semantic_strength=1.0,
        guest_authenticity=1.0,
        audience_relevance=1.0,
        novelty=1.0,
        narrative_utility=1.0,
        visual_opportunity=1.0,
        editorial_completeness=1.0,
        distribution_potential=1.0,
    )
    assert scores.weighted_composite_score == 1.0


def test_non_compensable_authenticity_gate():
    # Low authenticity candidate (<0.40) must fail gate and become ineligible for board
    profile = MultiDimensionalCandidateEvaluator.evaluate(
        candidate_id="CND-LOW-AUTH",
        workspace_id="ws-client-99",
        text_content="A generic marketing statement about team synergy.",
        semantic_strength=0.70,
        guest_authenticity=0.35,  # FAILS THRESHOLD (<0.40)
        audience_relevance=0.80,
        novelty=0.50,
        narrative_utility=0.60,
        visual_opportunity=0.50,
        editorial_completeness=0.80,
        distribution_potential=0.70,
    )

    assert profile.gate_status == GateStatus.FAILED_AUTHENTICITY
    assert profile.is_eligible_for_board is False
