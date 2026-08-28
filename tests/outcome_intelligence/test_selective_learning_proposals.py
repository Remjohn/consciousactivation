"""
test_selective_learning_proposals.py
------------------------------------
Tests that recurring empirical patterns produce structured LearningProposals requiring Operator approval.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "outcome-intelligence" / "src"))

from cae_outcome_intelligence.collector import OutcomeCollector
from cae_outcome_intelligence.domain import FailureMode, OutcomeDomain, PerformanceMemory
from cae_outcome_intelligence.learner import SelectiveLearningEngine


def test_recurring_pattern_generates_learning_proposal():
    memory = PerformanceMemory(workspace_id="ws-client-99")

    # Simulate 3 consecutive perceptual failures
    for i in range(3):
        out, rec = OutcomeCollector.record_outcome_and_receipt(
            program_id=f"PRG-0{i}",
            candidate_id=f"CND-0{i}",
            workspace_id="ws-client-99",
            domain=OutcomeDomain.PERCEPTUAL,
            metrics={"views": 2000.0, "dropoff_at_3s": 0.80},
            predicted_composite_score=0.80,
            observed_normalized_score=0.30,
            failure_mode=FailureMode.PERCEPTUAL_FAILURE,
        )
        memory.outcomes.append(out)
        memory.receipts.append(rec)

    proposals = SelectiveLearningEngine.analyze_memory_and_propose_calibrations(memory, min_recurrence=3)

    assert len(proposals) == 1
    p = proposals[0]
    assert p.proposal_type == "EVALUATOR_CALIBRATION"
    assert p.recurrence_count == 3
    assert p.requires_operator_ratification is True
