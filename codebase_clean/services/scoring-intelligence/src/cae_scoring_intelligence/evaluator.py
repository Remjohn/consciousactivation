"""
evaluator.py
------------
Multi-dimensional Candidate Evaluator with OLD CMF heritage adapter and non-compensable safety gates.
"""

from __future__ import annotations

import re
from typing import Optional

from .domain import (
    CandidateEvaluationProfile,
    DimensionScores,
    EvaluatorProvenance,
    GateStatus,
)
from .errors import (
    KeywordStuffingDetectedError,
    LengthGamingDetectedError,
    LowEvidenceViralityError,
    NonCompensableGateFailureError,
)


class MultiDimensionalCandidateEvaluator:
    """Evaluates candidates across 8 separable dimensions with non-compensable gates."""

    EVALUATOR_ID = "EVAL-CMF-HERITAGE-V2"
    EVALUATOR_VERSION = "2.1.0"

    STUFFING_KEYWORDS = ["secret", "shocking", "millionaire", "hacks", "exposed", "insane", "miracle"]

    @classmethod
    def evaluate(
        cls,
        *,
        candidate_id: str,
        workspace_id: str,
        text_content: str,
        semantic_strength: float,
        guest_authenticity: float,
        audience_relevance: float,
        novelty: float,
        narrative_utility: float,
        visual_opportunity: float,
        editorial_completeness: float,
        distribution_potential: float,
        rationale: str = "Automated multi-dimensional evaluation with CMF heritage adapter",
    ) -> CandidateEvaluationProfile:
        """Evaluates a candidate and applies non-compensable safety gates and anti-gaming checks."""
        lower_text = text_content.lower()

        # 1. Anti-Reward-Hacking: Keyword Stuffing
        stuffing_count = sum(1 for kw in cls.STUFFING_KEYWORDS if kw in lower_text)
        if stuffing_count >= 3:
            raise KeywordStuffingDetectedError(
                f"Candidate '{candidate_id}' exhibits keyword stuffing ({stuffing_count} clickbait markers detected)."
            )

        # 2. Anti-Reward-Hacking: Length Gaming (Repetitive filler)
        words = lower_text.split()
        if len(words) > 100:
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < 0.45:
                raise LengthGamingDetectedError(
                    f"Candidate '{candidate_id}' exhibits length gaming (excessive repetitive filler detected, unique word ratio={unique_ratio:.2f})."
                )

        # 3. Anti-Reward-Hacking: High Predicted Virality with Low Evidence
        if distribution_potential > 0.80 and guest_authenticity < 0.50:
            raise LowEvidenceViralityError(
                f"Candidate '{candidate_id}' violates grounding: distribution_potential={distribution_potential:.2f} "
                f"with inadequate guest_authenticity={guest_authenticity:.2f} (<0.50)."
            )

        # 4. Non-Compensable Safety Gates
        if guest_authenticity < 0.40:
            gate_status = GateStatus.FAILED_AUTHENTICITY
            is_eligible = False
        elif editorial_completeness < 0.40:
            gate_status = GateStatus.FAILED_COMPLETENESS
            is_eligible = False
        else:
            gate_status = GateStatus.PASSED
            is_eligible = True

        scores = DimensionScores.calculate_composite(
            semantic_strength=semantic_strength,
            guest_authenticity=guest_authenticity,
            audience_relevance=audience_relevance,
            novelty=novelty,
            narrative_utility=narrative_utility,
            visual_opportunity=visual_opportunity,
            editorial_completeness=editorial_completeness,
            distribution_potential=distribution_potential,
        )

        provenance = EvaluatorProvenance(
            evaluator_id=cls.EVALUATOR_ID,
            evaluator_version=cls.EVALUATOR_VERSION,
            rationale=rationale,
        )

        return CandidateEvaluationProfile(
            candidate_id=candidate_id,
            workspace_id=workspace_id,
            scores=scores,
            gate_status=gate_status,
            is_eligible_for_board=is_eligible,
            provenance=provenance,
        )
