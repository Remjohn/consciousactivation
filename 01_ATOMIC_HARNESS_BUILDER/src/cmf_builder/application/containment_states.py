"""Partial, redacted, failed and invalidated containment for OD-AM-005 / ST-10.13."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Any


def sha256_of(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


class ContainmentError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class ContainmentState(str, Enum):
    PARTIAL = "PARTIAL"
    REDACTED = "REDACTED"
    FAILED = "FAILED"
    INVALIDATED = "INVALIDATED"


@dataclass(frozen=True)
class ContainmentRecord:
    subject_identity: str
    containment_state: ContainmentState
    visible_fields: tuple[str, ...]
    unavailable_fields: tuple[str, ...]
    redaction_reasons: tuple[str, ...]
    failure_class: str
    invalidation_cause: str
    affected_descendants: tuple[str, ...]
    safe_operator_actions: tuple[str, ...]
    recovery_eligible: bool
    evidence_refs: tuple[str, ...]
    limitations: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.evidence_refs:
            raise ContainmentError("CONTAINMENT_EVIDENCE_REQUIRED", "containment requires evidence references")
        if self.containment_state is ContainmentState.PARTIAL and not self.unavailable_fields:
            raise ContainmentError("PARTIAL_REQUIRES_UNAVAILABLE_FIELDS", "partial data must identify missing fields")
        if self.containment_state is ContainmentState.REDACTED:
            if not self.redaction_reasons:
                raise ContainmentError("REDACTION_REASON_REQUIRED", "redaction requires a reason")
            if self.failure_class == "MISSING_AUTHORITY":
                raise ContainmentError("MISSING_AUTHORITY_NOT_REDACTION", "missing authority is not ordinary redaction")
        if self.containment_state is ContainmentState.FAILED and self.recovery_eligible and not self.safe_operator_actions:
            raise ContainmentError("FAILED_RECOVERY_ACTION_REQUIRED", "failed records need safe recovery actions")
        if self.containment_state is ContainmentState.INVALIDATED and not self.invalidation_cause:
            raise ContainmentError("INVALIDATION_CAUSE_REQUIRED", "invalidated records require a cause")
        if "RECONSTRUCT_HUMAN_TRUTH" in self.safe_operator_actions:
            raise ContainmentError("HUMAN_TRUTH_RECONSTRUCTION_PROHIBITED", "human truth cannot be reconstructed from redaction")

    @property
    def containment_identity(self) -> str:
        return sha256_of(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "subject_identity": self.subject_identity,
            "containment_state": self.containment_state.value,
            "visible_fields": list(self.visible_fields),
            "unavailable_fields": list(self.unavailable_fields),
            "redaction_reasons": list(self.redaction_reasons),
            "failure_class": self.failure_class,
            "invalidation_cause": self.invalidation_cause,
            "affected_descendants": list(self.affected_descendants),
            "safe_operator_actions": list(self.safe_operator_actions),
            "recovery_eligible": self.recovery_eligible,
            "evidence_refs": list(self.evidence_refs),
            "limitations": list(self.limitations),
            "production_ready": False,
            "certified": False,
        }


def export_containment(records: tuple[ContainmentRecord, ...]) -> dict[str, Any]:
    ordered = sorted(records, key=lambda item: item.subject_identity)
    payload = {
        "containment_records": [record.as_dict() for record in ordered],
        "export_limitations": ["containment_state_preserved", "not_production", "not_certification"],
    }
    payload["export_identity"] = sha256_of(payload)
    return payload
