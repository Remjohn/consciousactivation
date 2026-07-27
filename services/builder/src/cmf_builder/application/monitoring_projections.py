"""Deterministic local monitoring projections for OD-AM-004 / ST-10.08."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Any


def sha256_of(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


class MonitoringProjectionError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class MonitorFamily(str, Enum):
    WORKFLOW_MONITOR = "WORKFLOW_MONITOR"
    QUEUE_MONITOR = "QUEUE_MONITOR"
    INCIDENT_MONITOR = "INCIDENT_MONITOR"
    RESOURCE_AND_COST_MONITOR = "RESOURCE_AND_COST_MONITOR"
    CONTEXT_MONITOR = "CONTEXT_MONITOR"


@dataclass(frozen=True)
class MonitorRecord:
    monitor_identity: str
    family: MonitorFamily
    subject_identity: str
    status: str
    evidence_refs: tuple[str, ...]
    owner: str
    checkpoint_ref: str
    stale: bool = False
    partial: bool = False
    disconnected: bool = False
    redacted: bool = False
    invalidated: bool = False
    simulated: bool = False
    root_cause_ref: str = "NOT_DIAGNOSED"
    cost: str = "NOT_APPLICABLE"
    budget: str = "NOT_APPLICABLE"
    selected_context: tuple[str, ...] = ()
    required_context: tuple[str, ...] = ()
    excluded_context: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.evidence_refs:
            raise MonitoringProjectionError("MONITOR_EVIDENCE_REQUIRED", "monitor projection requires evidence")
        if self.family is MonitorFamily.INCIDENT_MONITOR and self.root_cause_ref == "INFERRED":
            raise MonitoringProjectionError("ROOT_CAUSE_NOT_DIAGNOSED", "do not infer root cause")
        if self.family is MonitorFamily.RESOURCE_AND_COST_MONITOR and not self.simulated and self.cost.startswith("$"):
            raise MonitoringProjectionError("REAL_CLOUD_COST_REQUIRES_REAL_EVIDENCE", "real cloud cost requires real evidence")
        if self.family is MonitorFamily.CONTEXT_MONITOR and set(self.excluded_context) & set(self.selected_context):
            raise MonitoringProjectionError("EXCLUDED_CONTEXT_SELECTED", "excluded context cannot be selected")

    def as_dict(self) -> dict[str, Any]:
        return {
            "monitor_identity": self.monitor_identity,
            "family": self.family.value,
            "subject_identity": self.subject_identity,
            "status": self.status,
            "evidence_refs": list(self.evidence_refs),
            "owner": self.owner,
            "checkpoint_ref": self.checkpoint_ref,
            "stale": self.stale,
            "partial": self.partial,
            "disconnected": self.disconnected,
            "redacted": self.redacted,
            "invalidated": self.invalidated,
            "simulated": self.simulated,
            "root_cause_ref": self.root_cause_ref,
            "cost": self.cost,
            "budget": self.budget,
            "selected_context": list(self.selected_context),
            "required_context": list(self.required_context),
            "excluded_context": list(self.excluded_context),
        }

    @property
    def record_identity(self) -> str:
        return sha256_of(self.as_dict())


def filter_monitors(records: tuple[MonitorRecord, ...], *, family: MonitorFamily | None = None, stale: bool | None = None) -> tuple[MonitorRecord, ...]:
    result = []
    for record in records:
        if family is not None and record.family is not family:
            continue
        if stale is not None and record.stale is not stale:
            continue
        result.append(record)
    return tuple(sorted(result, key=lambda item: item.monitor_identity))
