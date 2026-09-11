"""
collector.py
------------
Outcome collector and evaluation receipt generator with anti-reward-hacking checks.
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple

from .domain import (
    EvaluationReceipt,
    FailureMode,
    ObservedOutcome,
    OutcomeDomain,
)
from .errors import (
    EngagementWithoutTruthError,
    MisleadingContextRewardHackError,
)


class OutcomeCollector:
    """Collects empirical outcome metrics and emits auditable EvaluationReceipts."""

    @classmethod
    def record_outcome_and_receipt(
        cls,
        *,
        program_id: str,
        candidate_id: str,
        workspace_id: str,
        domain: OutcomeDomain,
        metrics: Dict[str, float],
        predicted_composite_score: float,
        observed_normalized_score: float,
        evaluator_scores: Optional[Dict[str, float]] = None,
        is_grounded: bool = True,
        misleading_context: bool = False,
        failure_mode: FailureMode = FailureMode.NONE,
        notes: Optional[str] = None,
    ) -> Tuple[ObservedOutcome, EvaluationReceipt]:
        """Records an observed outcome and generates a cryptographically tracked EvaluationReceipt."""
        # 1. Anti-Reward-Hack: Engagement without truth
        views = metrics.get("views", 0.0)
        retention = metrics.get("retention_rate", 0.0)
        if (views > 10000 or retention > 0.70) and not is_grounded:
            raise EngagementWithoutTruthError(
                f"Engagement without truth detected! High metrics (views={views}) recorded for ungrounded content."
            )

        # 2. Anti-Reward-Hack: Misleading context
        if misleading_context:
            raise MisleadingContextRewardHackError(
                "Misleading context detected! Positive metrics derived from sensationalized distortion."
            )

        # 3. Disagreement spread calculation
        eval_scores = evaluator_scores or {}
        if eval_scores:
            min_s = min(eval_scores.values())
            max_s = max(eval_scores.values())
            spread = round(max_s - min_s, 3)
        else:
            spread = 0.0

        score_delta = round(observed_normalized_score - predicted_composite_score, 3)

        outcome = ObservedOutcome(
            program_id=program_id,
            candidate_id=candidate_id,
            workspace_id=workspace_id,
            domain=domain,
            metrics=metrics,
            failure_mode=failure_mode,
            is_grounded=is_grounded,
            misleading_context=misleading_context,
            notes=notes,
        )

        receipt = EvaluationReceipt(
            outcome_id=outcome.outcome_id,
            program_id=program_id,
            candidate_id=candidate_id,
            predicted_composite_score=predicted_composite_score,
            observed_normalized_score=observed_normalized_score,
            score_delta=score_delta,
            evaluator_scores=eval_scores,
            disagreement_spread=spread,
            failure_mode=failure_mode,
            is_grounded=is_grounded,
        )

        return outcome, receipt
