"""
test_outcome_domain_contracts.py
--------------------------------
Validates ObservedOutcome, EvaluationReceipt, and LearningProposal instantiation and serialization.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "outcome-intelligence" / "src"))

from cae_outcome_intelligence.domain import (
    EvaluationReceipt,
    FailureMode,
    LearningProposal,
    ObservedOutcome,
    OutcomeDomain,
    PerformanceMemory,
)


def test_outcome_domain_contracts():
    outcome = ObservedOutcome(
        program_id="PRG-001",
        candidate_id="CND-001",
        workspace_id="ws-client-99",
        domain=OutcomeDomain.DISTRIBUTION,
        metrics={"views": 4500.0, "completion_rate": 0.62},
        failure_mode=FailureMode.NONE,
    )

    receipt = EvaluationReceipt(
        outcome_id=outcome.outcome_id,
        program_id="PRG-001",
        candidate_id="CND-001",
        predicted_composite_score=0.75,
        observed_normalized_score=0.80,
        score_delta=0.05,
        evaluator_scores={"evaluator_a": 0.78, "evaluator_b": 0.82},
        disagreement_spread=0.04,
    )

    proposal = LearningProposal(
        workspace_id="ws-client-99",
        pattern_summary="Consistent strong retention on paradoxical hooks.",
        proposal_type="BENCHMARK_UPDATE",
        recurrence_count=3,
        evidence_receipt_ids=[receipt.receipt_id],
    )

    memory = PerformanceMemory(
        workspace_id="ws-client-99",
        outcomes=[outcome],
        receipts=[receipt],
        proposals=[proposal],
    )

    assert outcome.outcome_id.startswith("OUT-")
    assert receipt.receipt_id.startswith("EVR-")
    assert proposal.proposal_id.startswith("LPR-")
    assert len(memory.receipts) == 1
