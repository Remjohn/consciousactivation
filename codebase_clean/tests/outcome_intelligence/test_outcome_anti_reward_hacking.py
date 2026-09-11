"""
test_outcome_anti_reward_hacking.py
-----------------------------------
Adversarial tests for engagement without truth, misleading context reward-hacks, disagreement laundering, and auto-mutation.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2] / "services" / "outcome-intelligence" / "src"))

import pytest

from cae_outcome_intelligence.collector import OutcomeCollector
from cae_outcome_intelligence.domain import (
    EvaluationReceipt,
    LearningProposal,
    OutcomeDomain,
)
from cae_outcome_intelligence.errors import (
    AveragedDisagreementLaunderingError,
    EngagementWithoutTruthError,
    MisleadingContextRewardHackError,
    OntologyMutationViolationError,
)
from cae_outcome_intelligence.learner import SelectiveLearningEngine
from cae_outcome_intelligence.verifier import OutcomeIntelligenceVerifier


def test_engagement_without_truth_rejected():
    with pytest.raises(EngagementWithoutTruthError, match="Engagement without truth detected"):
        OutcomeCollector.record_outcome_and_receipt(
            program_id="PRG-01",
            candidate_id="CND-01",
            workspace_id="ws-99",
            domain=OutcomeDomain.DISTRIBUTION,
            metrics={"views": 50000.0, "retention_rate": 0.85},
            predicted_composite_score=0.90,
            observed_normalized_score=0.95,
            is_grounded=False,  # VIOLATION: Viral engagement without factual truth
        )


def test_misleading_context_reward_hack_rejected():
    with pytest.raises(MisleadingContextRewardHackError, match="Misleading context detected"):
        OutcomeCollector.record_outcome_and_receipt(
            program_id="PRG-01",
            candidate_id="CND-01",
            workspace_id="ws-99",
            domain=OutcomeDomain.DISTRIBUTION,
            metrics={"views": 500.0},
            predicted_composite_score=0.70,
            observed_normalized_score=0.75,
            misleading_context=True,  # VIOLATION: Clickbait sensationalism
        )


def test_averaged_disagreement_laundering_rejected():
    receipt = EvaluationReceipt(
        outcome_id="OUT-01",
        program_id="PRG-01",
        candidate_id="CND-01",
        predicted_composite_score=0.70,
        observed_normalized_score=0.75,
        score_delta=0.05,
        evaluator_scores={},  # VIOLATION: Concealed breakdown despite wide spread
        disagreement_spread=0.55,
    )

    with pytest.raises(AveragedDisagreementLaunderingError, match="conceals individual evaluator scores"):
        OutcomeIntelligenceVerifier.verify_evaluator_disagreement_exposure(receipt)


def test_direct_ontology_mutation_forbidden():
    proposal = LearningProposal(
        workspace_id="ws-client-99",
        pattern_summary="Proposal to adjust evaluator weights.",
        proposal_type="EVALUATOR_CALIBRATION",
        recurrence_count=3,
        evidence_receipt_ids=["EVR-01", "EVR-02", "EVR-03"],
        requires_operator_ratification=True,
    )

    with pytest.raises(OntologyMutationViolationError, match="Requires explicit Operator ratification"):
        SelectiveLearningEngine.apply_proposal_direct_to_ontology(proposal)
