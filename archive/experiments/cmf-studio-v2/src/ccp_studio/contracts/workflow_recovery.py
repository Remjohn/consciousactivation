"""Workflow recovery contracts for TS-CMF-060."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class WorkflowRecoveryActionType(str, Enum):
    retry = "retry"
    resume = "resume"
    cancel = "cancel"
    compensate = "compensate"
    quarantine = "quarantine"


class QuarantineScope(str, Enum):
    workflow = "workflow"
    provider_job = "provider_job"
    asset = "asset"
    memory = "memory"
    publishing_intent = "publishing_intent"


class WorkflowRecoveryStatus(str, Enum):
    validated = "validated"
    applied = "applied"
    blocked = "blocked"
    replayed = "replayed"


class RecoveryValidationReport(BaseModel):
    schema_version: Literal["cmf.workflow_recovery_validation_report.v1"]
    report_id: UUID
    workflow_id: str = Field(min_length=1)
    failed_object_ref: str = Field(min_length=1)
    safe_actions: list[WorkflowRecoveryActionType] = Field(default_factory=list)
    blocked_actions: list[str] = Field(default_factory=list)
    completed_artifact_refs: list[str] = Field(default_factory=list)
    receipt_refs: list[str] = Field(default_factory=list)
    duplicate_side_effect_risks: list[str] = Field(default_factory=list)
    consent_compatible: bool
    provider_cost_risk: bool = False
    publishing_side_effect_risk: bool = False
    memory_side_effect_risk: bool = False
    checked_at: datetime


class WorkflowOperationalIncident(BaseModel):
    schema_version: Literal["cmf.workflow_operational_incident.v1"]
    incident_id: UUID
    workflow_id: str = Field(min_length=1)
    failed_object_ref: str = Field(min_length=1)
    severity: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    resolved: bool = False
    validation_report_id: UUID | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    recorded_at: datetime


class WorkflowRecoveryAction(BaseModel):
    schema_version: Literal["cmf.workflow_recovery_action.v1"]
    recovery_action_id: UUID
    incident_id: UUID
    action_type: WorkflowRecoveryActionType
    idempotency_key: str = Field(min_length=1)
    validation_report_id: UUID
    requested_by_user_id: UUID
    reason: str = Field(min_length=1)
    created_at: datetime


class WorkflowRecoveryReceipt(BaseModel):
    schema_version: Literal["cmf.workflow_recovery_receipt.v1"]
    receipt_id: UUID
    recovery_action_id: UUID | None = None
    validation_report_id: UUID
    incident_id: UUID
    action_type: WorkflowRecoveryActionType
    status: WorkflowRecoveryStatus
    idempotency_key: str = Field(min_length=1)
    preserved_artifact_refs: list[str] = Field(default_factory=list)
    requeued_work_refs: list[str] = Field(default_factory=list)
    quarantined_refs: list[str] = Field(default_factory=list)
    blocked_actions: list[str] = Field(default_factory=list)
    duplicate_side_effect_risks: list[str] = Field(default_factory=list)
    terminal_state: str | None = None
    decision_code: str = Field(min_length=1)
    actor_id: UUID
    receipt_hash: str = Field(min_length=1)
    written_at: datetime


class WorkflowRecoveryDomainEvent(BaseModel):
    schema_version: Literal["cmf.workflow_recovery_domain_event.v1"]
    workflow_recovery_event_id: UUID
    event_type: str = Field(min_length=1)
    incident_id: UUID | None = None
    recovery_action_id: UUID | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


def workflow_recovery_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_workflow_recovery_receipt(
    *,
    report: RecoveryValidationReport,
    incident_id: UUID,
    action_type: WorkflowRecoveryActionType,
    status: WorkflowRecoveryStatus,
    idempotency_key: str,
    actor_id: UUID,
    decision_code: str,
    recovery_action_id: UUID | None = None,
    preserved_artifact_refs: list[str] | None = None,
    requeued_work_refs: list[str] | None = None,
    quarantined_refs: list[str] | None = None,
    blocked_actions: list[str] | None = None,
    terminal_state: str | None = None,
) -> WorkflowRecoveryReceipt:
    payload = {
        "report_id": report.report_id,
        "incident_id": incident_id,
        "action_type": action_type.value,
        "status": status.value,
        "idempotency_key": idempotency_key,
        "preserved_artifact_refs": preserved_artifact_refs or [],
        "requeued_work_refs": requeued_work_refs or [],
        "quarantined_refs": quarantined_refs or [],
        "blocked_actions": blocked_actions or [],
        "duplicate_side_effect_risks": report.duplicate_side_effect_risks,
        "terminal_state": terminal_state,
        "decision_code": decision_code,
    }
    return WorkflowRecoveryReceipt(
        schema_version="cmf.workflow_recovery_receipt.v1",
        receipt_id=uuid4(),
        recovery_action_id=recovery_action_id,
        validation_report_id=report.report_id,
        incident_id=incident_id,
        action_type=action_type,
        status=status,
        idempotency_key=idempotency_key,
        preserved_artifact_refs=preserved_artifact_refs or [],
        requeued_work_refs=requeued_work_refs or [],
        quarantined_refs=quarantined_refs or [],
        blocked_actions=blocked_actions or [],
        duplicate_side_effect_risks=report.duplicate_side_effect_risks,
        terminal_state=terminal_state,
        decision_code=decision_code,
        actor_id=actor_id,
        receipt_hash=workflow_recovery_hash(payload),
        written_at=utc_now(),
    )
