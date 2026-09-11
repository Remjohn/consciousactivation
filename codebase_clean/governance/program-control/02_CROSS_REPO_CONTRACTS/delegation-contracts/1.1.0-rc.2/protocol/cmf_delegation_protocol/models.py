"""Reference protocol records and immutable processing outcomes."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ProcessingResult:
    accepted: bool
    code: str
    correlation_id: str
    message_id: str
    state: str
    audit_receipt: dict[str, Any]
    audit_hash: str
    outbox_sequence: int
    lifecycle_changed: bool
    idempotent: bool = False


@dataclass(frozen=True)
class StoredDecision:
    fingerprint: str
    result: ProcessingResult


@dataclass(frozen=True)
class IdempotencyRecord:
    message_id: str
    payload_hash: str
    fingerprint: str
    result: ProcessingResult


@dataclass(frozen=True)
class ReplayRecord:
    message_id: str
    fingerprint: str
    result: ProcessingResult


@dataclass(frozen=True)
class AuditRecord:
    receipt: dict[str, Any]
    record_hash: str
    decision: str
    code: str


@dataclass(frozen=True)
class OutboxEntry:
    sequence: int
    correlation_id: str
    message_id: str
    kind: str
    audit_hash: str
    delivered: bool = False


@dataclass
class CorrelationRecord:
    correlation_id: str
    state: str = "DRAFT"
    audit_sequence: int = 0
    audit: list[AuditRecord] = field(default_factory=list)
    demand_identity: dict[str, Any] | None = None
    current_result: dict[str, Any] | None = None
    pending_replacement: dict[str, Any] | None = None
    pending_amendment_id: str | None = None
    successor_demand: dict[str, Any] | None = None
    compatibility_profile: dict[str, Any] | None = None
    submission_id: str | None = None
    validation_receipt_id: str | None = None
    execution_id: str | None = None
    cancellation_request_id: str | None = None
    budget_escalation_request_id: str | None = None


@dataclass(frozen=True)
class DelegationSetRecord:
    set_id: str
    version: int
    member_demands: tuple[tuple[str, int, str], ...]
    completion_policy: str
    minimum_completed: int
