"""Fail-closed autonomous collision approval gate (CA-M055 / INV-AUTO-001).

The gate is deliberately policy-centric: a collision is approved autonomously only
when every required score meets its configured threshold and the aggregate score
also clears the autonomous threshold. Missing, malformed, non-finite, or borderline
inputs never become approvals; they route to manual review.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import math
from typing import Mapping


class GateDecision(str, Enum):
    APPROVE_AUTONOMOUS = "APPROVE_AUTONOMOUS"
    MANUAL_REVIEW = "MANUAL_REVIEW"
    REJECT = "REJECT"


class GateReason(str, Enum):
    ALL_THRESHOLDS_MET = "ALL_THRESHOLDS_MET"
    BORDERLINE_CONFIDENCE = "BORDERLINE_CONFIDENCE"
    BELOW_AUTONOMOUS_THRESHOLD = "BELOW_AUTONOMOUS_THRESHOLD"
    MISSING_SCORE = "MISSING_SCORE"
    INVALID_SCORE = "INVALID_SCORE"
    POLICY_VIOLATION = "POLICY_VIOLATION"


@dataclass(frozen=True)
class CollisionScores:
    """Normalized collision-policy scores in the inclusive range [0.0, 1.0]."""

    confidence: float
    grounding: float
    evidence_quality: float
    novelty: float
    safety: float

    def as_mapping(self) -> dict[str, float]:
        return {
            "confidence": self.confidence,
            "grounding": self.grounding,
            "evidence_quality": self.evidence_quality,
            "novelty": self.novelty,
            "safety": self.safety,
        }


@dataclass(frozen=True)
class AutonomousGatePolicy:
    """Strict thresholds that authorize an autonomous collision approval.

    ``minimum_score`` applies to every required dimension. ``autonomous_score``
    applies to the weighted aggregate. ``borderline_band`` defines the zone just
    below a passing threshold that must receive manual review rather than being
    hard-rejected.
    """

    minimum_score: float = 0.90
    autonomous_score: float = 0.95
    borderline_band: float = 0.05
    weights: Mapping[str, float] = field(
        default_factory=lambda: {
            "confidence": 0.30,
            "grounding": 0.25,
            "evidence_quality": 0.20,
            "novelty": 0.10,
            "safety": 0.15,
        }
    )

    def __post_init__(self) -> None:
        values = {
            "minimum_score": self.minimum_score,
            "autonomous_score": self.autonomous_score,
            "borderline_band": self.borderline_band,
        }
        for name, value in values.items():
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)):
                raise ValueError(f"{name} must be finite")
        if not 0.0 <= self.minimum_score <= 1.0:
            raise ValueError("minimum_score must be within [0, 1]")
        if not 0.0 <= self.autonomous_score <= 1.0:
            raise ValueError("autonomous_score must be within [0, 1]")
        if self.autonomous_score < self.minimum_score:
            raise ValueError("autonomous_score cannot be lower than minimum_score")
        if not 0.0 <= self.borderline_band <= 1.0:
            raise ValueError("borderline_band must be within [0, 1]")
        if set(self.weights) != set(CollisionScores.__dataclass_fields__):
            raise ValueError("weights must cover every collision score dimension exactly")
        if any(
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(float(value))
            or float(value) < 0.0
            for value in self.weights.values()
        ):
            raise ValueError("weights must be finite and non-negative")
        if math.isclose(sum(float(v) for v in self.weights.values()), 0.0):
            raise ValueError("weights must contain a positive total")

    @property
    def weight_total(self) -> float:
        return sum(float(value) for value in self.weights.values())


@dataclass(frozen=True)
class AutonomousGateResult:
    collision_id: str
    decision: GateDecision
    reason: GateReason
    aggregate_score: float | None
    failed_dimensions: tuple[str, ...]
    scores: dict[str, float]
    policy: AutonomousGatePolicy
    receipt_sha256: str

    @property
    def autonomous_approved(self) -> bool:
        return self.decision is GateDecision.APPROVE_AUTONOMOUS

    @property
    def requires_manual_review(self) -> bool:
        return self.decision is GateDecision.MANUAL_REVIEW


class AutonomousCollisionApprovalGate:
    """Evaluate collision scores without ever inferring authorization from context."""

    REQUIRED_DIMENSIONS = tuple(CollisionScores.__dataclass_fields__)

    def __init__(self, policy: AutonomousGatePolicy | None = None) -> None:
        self.policy = policy or AutonomousGatePolicy()

    def evaluate(self, collision_id: str, scores: CollisionScores | Mapping[str, float]) -> AutonomousGateResult:
        if not isinstance(collision_id, str) or not collision_id.strip():
            raise ValueError("collision_id is required")
        normalized = self._normalize_scores(scores)
        aggregate = self._aggregate(normalized)
        failed = tuple(
            name for name in self.REQUIRED_DIMENSIONS
            if normalized[name] < self.policy.minimum_score
        )

        if failed:
            near_borderline = tuple(
                name
                for name in failed
                if normalized[name] >= self.policy.minimum_score - self.policy.borderline_band
            )
            if near_borderline:
                decision = GateDecision.MANUAL_REVIEW
                reason = GateReason.BORDERLINE_CONFIDENCE
            else:
                decision = GateDecision.REJECT
                reason = GateReason.BELOW_AUTONOMOUS_THRESHOLD
        elif aggregate < self.policy.autonomous_score:
            decision = GateDecision.MANUAL_REVIEW
            reason = GateReason.BORDERLINE_CONFIDENCE
        else:
            decision = GateDecision.APPROVE_AUTONOMOUS
            reason = GateReason.ALL_THRESHOLDS_MET

        return AutonomousGateResult(
            collision_id=collision_id,
            decision=decision,
            reason=reason,
            aggregate_score=aggregate,
            failed_dimensions=failed,
            scores=dict(normalized),
            policy=self.policy,
            receipt_sha256=self._receipt_digest(
                collision_id=collision_id,
                decision=decision,
                reason=reason,
                aggregate_score=aggregate,
                failed_dimensions=failed,
                scores=normalized,
                policy=self.policy,
            ),
        )

    def require_autonomous_approval(
        self,
        collision_id: str,
        scores: CollisionScores | Mapping[str, float],
    ) -> AutonomousGateResult:
        result = self.evaluate(collision_id, scores)
        if result.decision is not GateDecision.APPROVE_AUTONOMOUS:
            raise AutonomousApprovalDeniedError(result)
        return result

    @staticmethod
    def _normalize_scores(scores: CollisionScores | Mapping[str, float]) -> dict[str, float]:
        if isinstance(scores, CollisionScores):
            raw = scores.as_mapping()
        elif isinstance(scores, Mapping):
            raw = dict(scores)
        else:
            raise TypeError("scores must be CollisionScores or a mapping")
        if set(raw) != set(AutonomousCollisionApprovalGate.REQUIRED_DIMENSIONS):
            missing = sorted(set(AutonomousCollisionApprovalGate.REQUIRED_DIMENSIONS) - set(raw))
            extra = sorted(set(raw) - set(AutonomousCollisionApprovalGate.REQUIRED_DIMENSIONS))
            detail = []
            if missing:
                detail.append(f"missing={missing}")
            if extra:
                detail.append(f"unknown={extra}")
            raise ValueError("score payload must contain exactly the required dimensions: " + ", ".join(detail))
        normalized: dict[str, float] = {}
        for name, value in raw.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be numeric")
            value = float(value)
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be finite and within [0, 1]")
            normalized[name] = value
        return normalized

    def _aggregate(self, scores: Mapping[str, float]) -> float:
        return sum(scores[name] * float(self.policy.weights[name]) for name in self.REQUIRED_DIMENSIONS) / self.policy.weight_total

    @staticmethod
    def _receipt_digest(
        *,
        collision_id: str,
        decision: GateDecision,
        reason: GateReason,
        aggregate_score: float | None,
        failed_dimensions: tuple[str, ...],
        scores: Mapping[str, float],
        policy: AutonomousGatePolicy,
    ) -> str:
        payload = {
            "mandate_id": "CA-M055",
            "invariant": "INV-AUTO-001",
            "collision_id": collision_id,
            "decision": decision.value,
            "reason": reason.value,
            "aggregate_score": aggregate_score,
            "failed_dimensions": list(failed_dimensions),
            "scores": {key: scores[key] for key in AutonomousCollisionApprovalGate.REQUIRED_DIMENSIONS},
            "policy": {
                "minimum_score": policy.minimum_score,
                "autonomous_score": policy.autonomous_score,
                "borderline_band": policy.borderline_band,
                "weights": {key: policy.weights[key] for key in AutonomousCollisionApprovalGate.REQUIRED_DIMENSIONS},
            },
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


class AutonomousApprovalDeniedError(RuntimeError):
    """Raised when the gate cannot prove autonomous approval."""

    def __init__(self, result: AutonomousGateResult) -> None:
        self.result = result
        super().__init__(
            f"autonomous approval denied for {result.collision_id}: "
            f"{result.decision.value} ({result.reason.value})"
        )
