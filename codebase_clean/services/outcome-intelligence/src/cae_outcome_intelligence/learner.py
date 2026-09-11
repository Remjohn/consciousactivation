"""
learner.py
----------
Selective learning engine that aggregates recurring outcome evidence and generates advisory proposals.
"""

from __future__ import annotations

from typing import List, Optional

from .domain import (
    EvaluationReceipt,
    FailureMode,
    LearningProposal,
    PerformanceMemory,
)
from .errors import OntologyMutationViolationError


class SelectiveLearningEngine:
    """Processes outcome receipts to generate governed learning proposals without auto-mutating ontology."""

    @classmethod
    def analyze_memory_and_propose_calibrations(
        cls,
        memory: PerformanceMemory,
        min_recurrence: int = 3,
    ) -> List[LearningProposal]:
        """Scans receipts for recurring patterns and emits advisory proposals."""
        proposals: List[LearningProposal] = []

        # 1. Check for recurring perceptual failures
        perceptual_failures = [
            r for r in memory.receipts if r.failure_mode == FailureMode.PERCEPTUAL_FAILURE
        ]
        if len(perceptual_failures) >= min_recurrence:
            proposal = LearningProposal(
                workspace_id=memory.workspace_id,
                pattern_summary=f"Detected recurring perceptual failures across {len(perceptual_failures)} programs.",
                proposal_type="EVALUATOR_CALIBRATION",
                suggested_modifications={
                    "pacing_evaluator_weight_adjustment": +0.10,
                    "target_rule": "Enforce minimum 3.5s visual scene duration preference",
                },
                recurrence_count=len(perceptual_failures),
                evidence_receipt_ids=[r.receipt_id for r in perceptual_failures],
                requires_operator_ratification=True,
            )
            proposals.append(proposal)

        # 2. Check for systematic under-prediction
        under_predictions = [r for r in memory.receipts if r.score_delta > 0.25]
        if len(under_predictions) >= min_recurrence:
            proposal = LearningProposal(
                workspace_id=memory.workspace_id,
                pattern_summary=f"Detected systematic under-prediction across {len(under_predictions)} programs.",
                proposal_type="BENCHMARK_UPDATE",
                suggested_modifications={
                    "novelty_threshold_adjustment": -0.05,
                    "target_rule": "Expand audience curiosity benchmark for emerging topics",
                },
                recurrence_count=len(under_predictions),
                evidence_receipt_ids=[r.receipt_id for r in under_predictions],
                requires_operator_ratification=True,
            )
            proposals.append(proposal)

        return proposals

    @classmethod
    def apply_proposal_direct_to_ontology(cls, proposal: LearningProposal) -> None:
        """Attempts to apply proposal directly without Operator approval - strictly forbidden!"""
        if proposal.requires_operator_ratification:
            raise OntologyMutationViolationError(
                f"Cannot auto-mutate ontology from proposal {proposal.proposal_id}! Requires explicit Operator ratification."
            )
