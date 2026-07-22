from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import ActivationHypothesis, ActivationHypothesisPortfolio


@dataclass(frozen=True, slots=True)
class CandidateScore:
    hypothesis_id: str
    source_support: float
    coach_fit: float
    audience_fit: float
    role_clarity: float
    edge_pressure: float
    freshness: float
    counteractivation_control: float
    cognitive_load: float
    format_fit: float

    def total(self) -> float:
        weights = {
            "source_support": 0.18,
            "coach_fit": 0.14,
            "audience_fit": 0.14,
            "role_clarity": 0.12,
            "edge_pressure": 0.12,
            "freshness": 0.08,
            "counteractivation_control": 0.08,
            "cognitive_load": 0.07,
            "format_fit": 0.07,
        }
        return sum(getattr(self, key) * weight for key, weight in weights.items())


def mechanically_eligible(hypothesis: ActivationHypothesis) -> bool:
    return bool(
        hypothesis.evidence_refs
        and hypothesis.roles
        and hypothesis.wrong_reading_locks
        and hypothesis.smallest_useful_commitment.strip()
    )


def select_candidate(
    portfolio: ActivationHypothesisPortfolio,
    scores: Iterable[CandidateScore],
    *,
    minimum_margin: float = 0.03,
) -> str | None:
    eligible_ids = {
        h.hypothesis_id for h in portfolio.candidates if mechanically_eligible(h)
    }
    ranked = sorted(
        (score for score in scores if score.hypothesis_id in eligible_ids),
        key=lambda score: score.total(),
        reverse=True,
    )
    if not ranked:
        return None
    if len(ranked) == 1:
        return ranked[0].hypothesis_id
    if ranked[0].total() - ranked[1].total() < minimum_margin:
        return None
    return ranked[0].hypothesis_id
