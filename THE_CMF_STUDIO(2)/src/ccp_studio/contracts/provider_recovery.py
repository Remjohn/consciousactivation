"""Provider recovery contracts for TS-CMF-048."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


class RecoveryActionType(str, Enum):
    pause = "pause"
    retry = "retry"
    resume = "resume"
    cancel = "cancel"
    compensate = "compensate"
    escalate = "escalate"


class RecoveryActionStatus(str, Enum):
    requested = "requested"
    applied = "applied"
    blocked = "blocked"
    escalated = "escalated"
    replayed = "replayed"


class OperationalIncidentType(str, Enum):
    provider_timeout = "provider_timeout"
    duplicate_webhook = "duplicate_webhook"
    duplicate_cost_risk = "duplicate_cost_risk"
    cancellation_mismatch = "cancellation_mismatch"
    compensation_required = "compensation_required"
    terminal_failure = "terminal_failure"


class ProviderJobCheckpoint(BaseModel):
    schema_version: Literal["cmf.provider_job_checkpoint.v1"]
    provider_job_checkpoint_id: UUID
    provider_job_id: UUID
    work_id: str = Field(min_length=1)
    output_artifact_uri: str | None = None
    output_artifact_hash: str | None = None
    completed: bool
    cost_amount: float | None = Field(default=None, ge=0)
    provider_receipt_id: UUID | None = None
    recorded_at: datetime

    @model_validator(mode="after")
    def completed_checkpoints_need_hash(self):
        if self.completed and not self.output_artifact_hash:
            raise ValueError("completed checkpoints require an output artifact hash")
        return self


class DuplicateCostRisk(BaseModel):
    schema_version: Literal["cmf.duplicate_cost_risk.v1"]
    duplicate_cost_risk_id: UUID
    provider_job_id: UUID
    action_type: RecoveryActionType
    risk_detected: bool
    risk_reasons: list[str] = Field(default_factory=list)
    manual_review_required: bool
    blocked: bool
    created_at: datetime


class ProviderRecoveryAction(BaseModel):
    schema_version: Literal["cmf.provider_recovery_action.v1"]
    provider_recovery_action_id: UUID
    provider_job_id: UUID
    action_type: RecoveryActionType
    status: RecoveryActionStatus
    idempotency_key: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    duplicate_cost_risk: bool
    manual_review_required: bool = False
    preserved_output_hashes: list[str] = Field(default_factory=list)
    requeued_work_ids: list[str] = Field(default_factory=list)
    terminal_state: str | None = None
    created_at: datetime


class OperationalIncident(BaseModel):
    schema_version: Literal["cmf.operational_incident.v1"]
    operational_incident_id: UUID
    provider_job_id: UUID
    incident_type: OperationalIncidentType
    severity: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    duplicate_webhook_count: int = Field(default=0, ge=0)
    recovery_action_id: UUID | None = None
    resolved: bool = False
    evidence_refs: list[str] = Field(default_factory=list)
    recorded_at: datetime


class RecoveryReceipt(BaseModel):
    schema_version: Literal["cmf.recovery_receipt.v1"]
    recovery_receipt_id: UUID
    provider_job_id: UUID
    action_id: UUID
    action_type: RecoveryActionType
    idempotency_key: str = Field(min_length=1)
    preserved_output_hashes: list[str] = Field(default_factory=list)
    requeued_work_ids: list[str] = Field(default_factory=list)
    duplicate_cost_risk: bool
    manual_review_required: bool
    terminal_state: str | None = None
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    actor_id: UUID
    command_id: UUID | None = None
    receipt_hash: str = Field(min_length=1)
    written_at: datetime


def recovery_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_recovery_receipt(
    *,
    provider_job_id: UUID,
    action: ProviderRecoveryAction,
    decision_code: str,
    actor_id: UUID,
    evidence_refs: list[str],
    command_id: UUID | None = None,
) -> RecoveryReceipt:
    payload = {
        "provider_job_id": provider_job_id,
        "action_id": action.provider_recovery_action_id,
        "action_type": action.action_type.value,
        "idempotency_key": action.idempotency_key,
        "preserved_output_hashes": action.preserved_output_hashes,
        "requeued_work_ids": action.requeued_work_ids,
        "duplicate_cost_risk": action.duplicate_cost_risk,
        "manual_review_required": action.manual_review_required,
        "terminal_state": action.terminal_state,
        "decision_code": decision_code,
        "evidence_refs": evidence_refs,
    }
    return RecoveryReceipt(
        schema_version="cmf.recovery_receipt.v1",
        recovery_receipt_id=uuid4(),
        provider_job_id=provider_job_id,
        action_id=action.provider_recovery_action_id,
        action_type=action.action_type,
        idempotency_key=action.idempotency_key,
        preserved_output_hashes=action.preserved_output_hashes,
        requeued_work_ids=action.requeued_work_ids,
        duplicate_cost_risk=action.duplicate_cost_risk,
        manual_review_required=action.manual_review_required,
        terminal_state=action.terminal_state,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        actor_id=actor_id,
        command_id=command_id,
        receipt_hash=recovery_hash(payload),
        written_at=utc_now(),
    )
