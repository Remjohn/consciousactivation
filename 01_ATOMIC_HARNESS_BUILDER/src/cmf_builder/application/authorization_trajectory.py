"""Evaluation, repair, maturity, and authorization trajectory for OD-AM-004 / ST-10.07."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Any


def sha256_of(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


class AuthorizationTrajectoryError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class TrajectoryStage(str, Enum):
    IMPLEMENTATION_COMPLETION = "IMPLEMENTATION_COMPLETION"
    EVALUATION = "EVALUATION"
    DIMENSION_SCORE = "DIMENSION_SCORE"
    NON_COMPENSABLE_FAILURE = "NON_COMPENSABLE_FAILURE"
    DIAGNOSIS = "DIAGNOSIS"
    REPAIR = "REPAIR"
    SELECTIVE_RERUN = "SELECTIVE_RERUN"
    EVIDENCE_CLOSURE = "EVIDENCE_CLOSURE"
    MATURITY_PROMOTION = "MATURITY_PROMOTION"
    RUNTIME_AUTHORIZATION = "RUNTIME_AUTHORIZATION"
    DEPLOYMENT_AUTHORIZATION = "DEPLOYMENT_AUTHORIZATION"
    PRODUCTION_READINESS = "PRODUCTION_READINESS"
    CERTIFICATION = "CERTIFICATION"
    INVALIDATION = "INVALIDATION"


REQUIRED_ORDER = tuple(stage for stage in TrajectoryStage)


@dataclass(frozen=True)
class TrajectoryRecord:
    subject_identity: str
    stage: TrajectoryStage
    stage_status: str
    predecessor_stage: TrajectoryStage | None
    receipt_identity: str
    evidence_refs: tuple[str, ...]
    authority_owner: str
    applicable_scope: str
    limitations: tuple[str, ...]
    open_gates: tuple[str, ...]
    invalidation_conditions: tuple[str, ...]
    superseding_records: tuple[str, ...]
    timestamp: str
    projection_freshness: str
    invalidated: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "subject_identity": self.subject_identity,
            "stage": self.stage.value,
            "stage_status": self.stage_status,
            "predecessor_stage": self.predecessor_stage.value if self.predecessor_stage else None,
            "receipt_identity": self.receipt_identity,
            "evidence_refs": list(self.evidence_refs),
            "authority_owner": self.authority_owner,
            "applicable_scope": self.applicable_scope,
            "limitations": list(self.limitations),
            "open_gates": list(self.open_gates),
            "invalidation_conditions": list(self.invalidation_conditions),
            "superseding_records": list(self.superseding_records),
            "timestamp": self.timestamp,
            "projection_freshness": self.projection_freshness,
            "invalidated": self.invalidated,
        }

    @property
    def record_identity(self) -> str:
        return sha256_of(self.as_dict())


def validate_trajectory(records: tuple[TrajectoryRecord, ...]) -> None:
    seen = {record.stage for record in records}
    for record in records:
        if record.stage is TrajectoryStage.REPAIR and TrajectoryStage.DIAGNOSIS not in seen:
            raise AuthorizationTrajectoryError("REPAIR_WITHOUT_DIAGNOSIS", "repair requires diagnosis")
        if record.stage is TrajectoryStage.MATURITY_PROMOTION and not record.evidence_refs:
            raise AuthorizationTrajectoryError("MATURITY_PROMOTION_WITHOUT_EVIDENCE", "maturity promotion requires evidence")
        if record.stage in {TrajectoryStage.PRODUCTION_READINESS, TrajectoryStage.CERTIFICATION} and record.stage_status == "PASS":
            raise AuthorizationTrajectoryError("FALSE_PRODUCTION_OR_CERTIFICATION_INFERENCE", "offline implementation cannot pass production or certification")
        if record.stage is TrajectoryStage.NON_COMPENSABLE_FAILURE and record.stage_status == "HIDDEN_BY_AGGREGATE":
            raise AuthorizationTrajectoryError("NON_COMPENSABLE_FAILURE_HIDDEN", "aggregate score cannot hide non-compensable failure")
        if record.invalidated and record.stage_status == "ACTIVE":
            raise AuthorizationTrajectoryError("INVALIDATED_EVIDENCE_SHOWN_ACTIVE", "invalidated evidence cannot be active")
    ordered = [record.stage for record in records]
    for index, stage in enumerate(ordered):
        if index and records[index].predecessor_stage != ordered[index - 1]:
            raise AuthorizationTrajectoryError("SKIPPED_REQUIRED_STAGE", "stage predecessor chain is broken")


def current_trajectory(records: tuple[TrajectoryRecord, ...]) -> tuple[TrajectoryRecord, ...]:
    return tuple(record for record in records if not record.invalidated)


def blocked_stage_explanation(records: tuple[TrajectoryRecord, ...]) -> dict[str, Any]:
    blocked = [record for record in records if record.open_gates]
    return {record.stage.value: list(record.open_gates) for record in blocked}
