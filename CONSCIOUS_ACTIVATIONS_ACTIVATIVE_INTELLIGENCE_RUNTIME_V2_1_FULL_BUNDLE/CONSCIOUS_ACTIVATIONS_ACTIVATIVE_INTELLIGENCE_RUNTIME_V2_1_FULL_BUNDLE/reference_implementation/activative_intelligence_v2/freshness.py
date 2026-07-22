from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class PatternExposure:
    pattern_id: str
    last_used_at: datetime
    uses_last_30_days: int
    audience_exposure: float
    qualitative_fatigue: float


def freshness_score(exposure: PatternExposure) -> float:
    recency_penalty = min(exposure.uses_last_30_days / 10.0, 1.0)
    return max(
        0.0,
        1.0
        - 0.35 * recency_penalty
        - 0.35 * exposure.audience_exposure
        - 0.30 * exposure.qualitative_fatigue,
    )
