from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..domain.enums import StopReason
from ..domain.errors import PipelineBudgetError, PipelineValidationError
from ..domain.validation import require_int, require_ref, require_string, semantic_identity


class CandidateSearchService:
    """Deterministic candidate comparison using integer scores and bounded budgets."""

    def evaluate(
        self,
        candidates: list[Mapping[str, Any]],
        *,
        max_candidates: int,
        budget_units: int,
        quality_threshold_bps: int,
        plateau_window: int,
        plateau_delta_bps: int,
    ) -> dict[str, Any]:
        max_candidates = require_int(max_candidates, "max_candidates", minimum=1)
        budget_units = require_int(budget_units, "budget_units", minimum=0)
        quality_threshold_bps = require_int(quality_threshold_bps, "quality_threshold_bps", minimum=0)
        plateau_window = require_int(plateau_window, "plateau_window", minimum=1)
        plateau_delta_bps = require_int(plateau_delta_bps, "plateau_delta_bps", minimum=0)
        normalized = [self._candidate(item, index) for index, item in enumerate(candidates)]
        normalized.sort(key=lambda item: (item["sequence"], item["candidate_id"]))
        observed: list[dict[str, Any]] = []
        spent = 0
        best: dict[str, Any] | None = None
        reason: StopReason | None = None
        for candidate in normalized:
            if len(observed) >= max_candidates:
                reason = StopReason.MAX_CANDIDATES
                break
            if spent + candidate["cost_units"] > budget_units:
                reason = StopReason.BUDGET_EXHAUSTED
                break
            spent += candidate["cost_units"]
            observed.append(candidate)
            if best is None or self._rank_key(candidate) < self._rank_key(best):
                best = candidate
            if best and best["quality_score_bps"] >= quality_threshold_bps:
                reason = StopReason.QUALITY_THRESHOLD
                break
            if len(observed) >= plateau_window:
                window = observed[-plateau_window:]
                scores = [item["quality_score_bps"] for item in window]
                if max(scores) - min(scores) <= plateau_delta_bps:
                    reason = StopReason.PLATEAU
                    break
        if not observed:
            reason = StopReason.NO_ELIGIBLE_CANDIDATES
        elif reason is None:
            reason = StopReason.MAX_CANDIDATES if len(observed) >= max_candidates else StopReason.MANUAL_STOP
        core = {
            "candidate_ids_evaluated": [item["candidate_id"] for item in observed],
            "best_candidate_id": best["candidate_id"] if best else "NOT_APPLICABLE",
            "spent_units": spent,
            "budget_units": budget_units,
            "stop_reason": reason.value,
            "quality_threshold_bps": quality_threshold_bps,
            "max_candidates": max_candidates,
            "plateau_window": plateau_window,
            "plateau_delta_bps": plateau_delta_bps,
            "tie_breaker": "quality_desc_cost_asc_candidate_id_asc",
        }
        return {"portfolio_id": semantic_identity("candidate-portfolio", core), **core, "candidates": observed}

    @staticmethod
    def _rank_key(candidate: Mapping[str, Any]) -> tuple[int, int, str]:
        return (-int(candidate["quality_score_bps"]), int(candidate["cost_units"]), str(candidate["candidate_id"]))

    @staticmethod
    def _candidate(payload: Mapping[str, Any], index: int) -> dict[str, Any]:
        required = {"candidate_id", "artifact_ref", "quality_score_bps", "cost_units", "sequence", "eligible", "failure_codes"}
        if set(payload) != required:
            raise PipelineValidationError(f"candidate {index} has unknown or missing fields")
        if payload["eligible"] is not True:
            raise PipelineValidationError(f"candidate {index} is not eligible")
        score = require_int(payload["quality_score_bps"], f"candidate[{index}].quality_score_bps")
        if score > 10_000:
            raise PipelineValidationError("quality_score_bps must be <= 10000")
        failures = payload["failure_codes"]
        if not isinstance(failures, list) or failures != sorted(set(failures)):
            raise PipelineValidationError("failure_codes must be sorted and unique")
        if failures:
            raise PipelineValidationError("eligible candidate cannot carry failure codes")
        return {
            "candidate_id": require_string(payload["candidate_id"], f"candidate[{index}].candidate_id"),
            "artifact_ref": require_ref(payload["artifact_ref"], f"candidate[{index}].artifact_ref"),
            "quality_score_bps": score,
            "cost_units": require_int(payload["cost_units"], f"candidate[{index}].cost_units"),
            "sequence": require_int(payload["sequence"], f"candidate[{index}].sequence"),
            "eligible": True,
            "failure_codes": [],
        }
