"""Explicit projection states for OD-AM-005 / ST-10.12."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Any


def sha256_of(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()).hexdigest()


class ProjectionStateError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class ProjectionStateClass(str, Enum):
    LOADING = "LOADING"
    EMPTY = "EMPTY"
    READY = "READY"
    STALE = "STALE"
    DISCONNECTED = "DISCONNECTED"
    UNAVAILABLE = "UNAVAILABLE"


@dataclass(frozen=True)
class ProjectionState:
    subject_identity: str
    state_class: ProjectionStateClass
    source_identity: str
    last_successful_revision: str
    current_requested_revision: str
    detection_reason: str
    operator_safe_message: str
    retry_eligible: bool
    fallback_available: bool
    limitations: tuple[str, ...]
    evidence_ref: str = "NOT_APPLICABLE"
    last_known_payload_identity: str = "NONE"

    def __post_init__(self) -> None:
        if not self.source_identity or not self.detection_reason or not self.operator_safe_message:
            raise ProjectionStateError("PROJECTION_STATE_EVIDENCE_REQUIRED", "projection state requires source, reason and safe message")
        if self.state_class is ProjectionStateClass.EMPTY and self.detection_reason == "FAILURE":
            raise ProjectionStateError("EMPTY_STATE_MISREPRESENTED_AS_FAILURE", "empty is not failure")
        if self.state_class is ProjectionStateClass.STALE and self.last_successful_revision == self.current_requested_revision:
            raise ProjectionStateError("STALE_REQUIRES_REVISION_DRIFT", "stale requires revision drift")
        if self.state_class is ProjectionStateClass.DISCONNECTED and self.fallback_available and self.last_known_payload_identity == "NONE":
            raise ProjectionStateError("DISCONNECTED_FALLBACK_UNLABELED", "fallback data must be explicitly identified")
        if self.state_class is ProjectionStateClass.LOADING and self.last_known_payload_identity != "NONE":
            raise ProjectionStateError("LOADING_FABRICATED_PARTIAL_RESULT", "loading cannot fabricate partial results")
        if self.state_class is ProjectionStateClass.UNAVAILABLE and "cached_authority" in self.limitations:
            raise ProjectionStateError("UNAVAILABLE_FABRICATED_CACHED_AUTHORITY", "unavailable cannot fabricate cached authority")

    @property
    def state_identity(self) -> str:
        return sha256_of(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "subject_identity": self.subject_identity,
            "state_class": self.state_class.value,
            "source_identity": self.source_identity,
            "last_successful_revision": self.last_successful_revision,
            "current_requested_revision": self.current_requested_revision,
            "detection_reason": self.detection_reason,
            "operator_safe_message": self.operator_safe_message,
            "retry_eligible": self.retry_eligible,
            "fallback_available": self.fallback_available,
            "limitations": list(self.limitations),
            "evidence_ref": self.evidence_ref,
            "last_known_payload_identity": self.last_known_payload_identity,
            "production_ready": False,
            "certified": False,
        }


def summarize_projection_states(states: tuple[ProjectionState, ...]) -> dict[str, Any]:
    ordered = sorted(states, key=lambda item: (item.subject_identity, item.state_class.value))
    return {
        "states": [item.as_dict() for item in ordered],
        "summary_identity": sha256_of([item.state_identity for item in ordered]),
        "production_ready": False,
        "certified": False,
    }
