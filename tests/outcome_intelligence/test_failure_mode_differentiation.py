"""
test_failure_mode_differentiation.py
------------------------------------
Tests precise differentiation between semantic, perceptual, distribution, and grounding failures.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "outcome-intelligence" / "src"))

from cae_outcome_intelligence.collector import OutcomeCollector
from cae_outcome_intelligence.domain import FailureMode, OutcomeDomain


def test_failure_mode_classification():
    # 1. Distribution failure (good content, bad algorithmic delivery/timing)
    out_dist, rec_dist = OutcomeCollector.record_outcome_and_receipt(
        program_id="PRG-01",
        candidate_id="CND-01",
        workspace_id="ws-99",
        domain=OutcomeDomain.DISTRIBUTION,
        metrics={"views": 120.0, "retention_rate": 0.85},
        predicted_composite_score=0.82,
        observed_normalized_score=0.30,
        failure_mode=FailureMode.DISTRIBUTION_FAILURE,
        notes="Published at 3am Tuesday; audience offline but retention among viewers was exceptional.",
    )
    assert rec_dist.failure_mode == FailureMode.DISTRIBUTION_FAILURE
    assert rec_dist.score_delta == -0.52

    # 2. Perceptual failure (good thesis, poor pacing/kinetic styling)
    out_perc, rec_perc = OutcomeCollector.record_outcome_and_receipt(
        program_id="PRG-02",
        candidate_id="CND-02",
        workspace_id="ws-99",
        domain=OutcomeDomain.PERCEPTUAL,
        metrics={"views": 5000.0, "dropoff_at_3s": 0.75},
        predicted_composite_score=0.85,
        observed_normalized_score=0.35,
        failure_mode=FailureMode.PERCEPTUAL_FAILURE,
        notes="First visual cut was sluggish; 75% dropped off in first 3 seconds.",
    )
    assert rec_perc.failure_mode == FailureMode.PERCEPTUAL_FAILURE
