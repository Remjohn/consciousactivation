"""
test_cmf_heritage_scoring_integration.py
----------------------------------------
Tests 4-axis OLD CMF heritage diagnostic evaluation score calculations.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "candidate-intelligence" / "src"))

from cae_candidate_intelligence.domain import HeritageCMFScore


def test_cmf_score_calculation_weights():
    # Weights: 0.30 emotional + 0.30 cognitive + 0.25 authority + 0.15 velocity
    score = HeritageCMFScore.calculate(
        emotional_resonance=1.0,
        cognitive_novelty=1.0,
        authority_evidence=1.0,
        narrative_velocity=1.0,
    )
    assert score.composite_score == 1.0

    score_mixed = HeritageCMFScore.calculate(
        emotional_resonance=0.8,
        cognitive_novelty=0.6,
        authority_evidence=0.9,
        narrative_velocity=0.7,
    )
    # Expected: 0.3*0.8 (0.24) + 0.3*0.6 (0.18) + 0.25*0.9 (0.225) + 0.15*0.7 (0.105) = 0.75
    assert abs(score_mixed.composite_score - 0.75) < 1e-4
