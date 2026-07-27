"""Pipeline orchestration contracts for CMF STUDIO.

These models implement TS-CMF-002. They make Pi and specialist-agent work
stage-bound, receipt-bound, and traceable without giving agents direct mutation
authority.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class StageRunStatus(str, Enum):
    opened = "opened"
    planned = "planned"
    executing = "executing"
    succeeded = "succeeded"
    failed = "failed"
    blocked = "blocked"
    waiting_for_human = "waiting_for_human"
    quarantined = "quarantined"
    compensated = "compensated"


class ActiveObjectRef(BaseModel):
    object_type: str = Field(min_length=1)
    object_id: UUID
    version_id: UUID | None = None


class OrchestrationRun(BaseModel):
    schema_version: Literal["cmf.orchestration_run.v1"]
    orchestration_run_id: UUID
    organization_id: UUID
    brand_id: UUID
    actor_id: UUID
    active_object: ActiveObjectRef
    requested_outcome: str = Field(min_length=1)
    status: StageRunStatus
    correlation_id: UUID
    opened_at: datetime
    updated_at: datetime

    @field_validator("opened_at", "updated_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("orchestration timestamps must be timezone-aware")
        return value


class StageExecutionPlan(BaseModel):
    schema_version: Literal["cmf.stage_execution_plan.v1"]
    stage_execution_plan_id: UUID
    orchestration_run_id: UUID
    pipeline_stage: str = Field(min_length=1)
    entry_object: ActiveObjectRef
    expected_exit_object_type: str = Field(min_length=1)
    allowed_actor_or_service: str = Field(min_length=1)
    required_inputs: list[str] = Field(default_factory=list)
    allowed_actions: list[str] = Field(min_length=1)
    blocked_actions: list[str] = Field(default_factory=list)
    downstream_proof_obligation: str = Field(min_length=1)
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("created_at must be timezone-aware")
        return value


class ValidationContract(BaseModel):
    schema_version: Literal["cmf.validation_contract.v1"]
    validation_contract_id: UUID
    stage_execution_plan_id: UUID
    success_criteria: list[str] = Field(min_length=1)
    failure_criteria: list[str] = Field(min_length=1)
    thresholds: dict[str, float] = Field(default_factory=dict)
    forbidden_skips: list[str] = Field(default_factory=list)
    required_evidence_refs: list[str] = Field(default_factory=list)
    required_receipt_types: list[str] = Field(min_length=1)
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("created_at must be timezone-aware")
        return value


class AgentHandoffPacket(BaseModel):
    schema_version: Literal["cmf.agent_handoff_packet.v1"]
    handoff_packet_id: UUID
    orchestration_run_id: UUID
    stage_execution_plan_id: UUID
    recipient_type: str = Field(min_length=1)
    recipient_name: str = Field(min_length=1)
    active_object: ActiveObjectRef
    source_evidence_refs: list[str] = Field(default_factory=list)
    upstream_receipt_ids: list[UUID] = Field(default_factory=list)
    allowed_actions: list[str] = Field(min_length=1)
    blocked_actions: list[str] = Field(default_factory=list)
    required_downstream_receipt: str = Field(min_length=1)
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("created_at must be timezone-aware")
        return value


class StageExecutionReceipt(BaseModel):
    schema_version: Literal["cmf.stage_execution_receipt.v1"]
    receipt_id: UUID
    orchestration_run_id: UUID
    stage_execution_plan_id: UUID
    receipt_type: str = Field(min_length=1)
    status: StageRunStatus
    decision: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    output_object: ActiveObjectRef | None = None
    created_event_id: UUID | None = None
    correlation_id: UUID
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
            raise ValueError("created_at must be timezone-aware")
        return value


class FailureReceipt(BaseModel):
    schema_version: Literal["cmf.failure_receipt.v1"]
    receipt_id: UUID
    orchestration_run_id: UUID
    stage_execution_plan_id: UUID
    failed_gate: str = Field(min_length=1)
    root_cause: str = Field(min_length=1)
    retry_policy: str = Field(min_length=1)
    quarantine_status: str = Field(default="not_quarantined")
    next_action: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime


class FrictionReceipt(BaseModel):
    schema_version: Literal["cmf.friction_receipt.v1"]
    receipt_id: UUID
    orchestration_run_id: UUID
    stage_execution_plan_id: UUID
    friction_type: str = Field(min_length=1)
    description: str = Field(min_length=1)
    severity: str = Field(default="medium")
    evidence_refs: list[str] = Field(default_factory=list)
    created_at: datetime


class HumanHandoffRequest(BaseModel):
    schema_version: Literal["cmf.human_handoff_request.v1"]
    handoff_request_id: UUID
    orchestration_run_id: UUID
    stage_execution_plan_id: UUID
    reason: str = Field(min_length=1)
    required_decision: str = Field(min_length=1)
    allowed_responses: list[str] = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    requested_at: datetime


class QuarantineReceipt(BaseModel):
    schema_version: Literal["cmf.quarantine_receipt.v1"]
    receipt_id: UUID
    orchestration_run_id: UUID
    stage_execution_plan_id: UUID
    quarantine_reason: str = Field(min_length=1)
    blocked_output_refs: list[str] = Field(default_factory=list)
    recovery_action: str = Field(min_length=1)
    created_at: datetime


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def new_orchestration_run(
    *,
    organization_id: UUID,
    brand_id: UUID,
    actor_id: UUID,
    active_object: ActiveObjectRef,
    requested_outcome: str,
    correlation_id: UUID | None = None,
) -> OrchestrationRun:
    now = utc_now()
    return OrchestrationRun(
        schema_version="cmf.orchestration_run.v1",
        orchestration_run_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        actor_id=actor_id,
        active_object=active_object,
        requested_outcome=requested_outcome,
        status=StageRunStatus.opened,
        correlation_id=correlation_id or uuid4(),
        opened_at=now,
        updated_at=now,
    )


def new_stage_execution_plan(
    *,
    orchestration_run_id: UUID,
    pipeline_stage: str,
    entry_object: ActiveObjectRef,
    expected_exit_object_type: str,
    allowed_actor_or_service: str,
    required_inputs: list[str],
    allowed_actions: list[str],
    blocked_actions: list[str],
    downstream_proof_obligation: str,
) -> StageExecutionPlan:
    return StageExecutionPlan(
        schema_version="cmf.stage_execution_plan.v1",
        stage_execution_plan_id=uuid4(),
        orchestration_run_id=orchestration_run_id,
        pipeline_stage=pipeline_stage,
        entry_object=entry_object,
        expected_exit_object_type=expected_exit_object_type,
        allowed_actor_or_service=allowed_actor_or_service,
        required_inputs=required_inputs,
        allowed_actions=allowed_actions,
        blocked_actions=blocked_actions,
        downstream_proof_obligation=downstream_proof_obligation,
        created_at=utc_now(),
    )


def new_validation_contract(
    *,
    stage_execution_plan_id: UUID,
    success_criteria: list[str],
    failure_criteria: list[str],
    required_receipt_types: list[str],
    thresholds: dict[str, float] | None = None,
    forbidden_skips: list[str] | None = None,
    required_evidence_refs: list[str] | None = None,
) -> ValidationContract:
    return ValidationContract(
        schema_version="cmf.validation_contract.v1",
        validation_contract_id=uuid4(),
        stage_execution_plan_id=stage_execution_plan_id,
        success_criteria=success_criteria,
        failure_criteria=failure_criteria,
        thresholds=thresholds or {},
        forbidden_skips=forbidden_skips or [],
        required_evidence_refs=required_evidence_refs or [],
        required_receipt_types=required_receipt_types,
        created_at=utc_now(),
    )


def new_agent_handoff_packet(
    *,
    orchestration_run_id: UUID,
    stage_execution_plan_id: UUID,
    recipient_type: str,
    recipient_name: str,
    active_object: ActiveObjectRef,
    source_evidence_refs: list[str],
    upstream_receipt_ids: list[UUID],
    allowed_actions: list[str],
    blocked_actions: list[str],
    required_downstream_receipt: str,
) -> AgentHandoffPacket:
    return AgentHandoffPacket(
        schema_version="cmf.agent_handoff_packet.v1",
        handoff_packet_id=uuid4(),
        orchestration_run_id=orchestration_run_id,
        stage_execution_plan_id=stage_execution_plan_id,
        recipient_type=recipient_type,
        recipient_name=recipient_name,
        active_object=active_object,
        source_evidence_refs=source_evidence_refs,
        upstream_receipt_ids=upstream_receipt_ids,
        allowed_actions=allowed_actions,
        blocked_actions=blocked_actions,
        required_downstream_receipt=required_downstream_receipt,
        created_at=utc_now(),
    )


def new_stage_execution_receipt(
    *,
    orchestration_run_id: UUID,
    stage_execution_plan_id: UUID,
    receipt_type: str,
    status: StageRunStatus,
    decision: str,
    evidence_refs: list[str],
    correlation_id: UUID,
    output_object: ActiveObjectRef | None = None,
    created_event_id: UUID | None = None,
) -> StageExecutionReceipt:
    return StageExecutionReceipt(
        schema_version="cmf.stage_execution_receipt.v1",
        receipt_id=uuid4(),
        orchestration_run_id=orchestration_run_id,
        stage_execution_plan_id=stage_execution_plan_id,
        receipt_type=receipt_type,
        status=status,
        decision=decision,
        evidence_refs=evidence_refs,
        output_object=output_object,
        created_event_id=created_event_id,
        correlation_id=correlation_id,
        created_at=utc_now(),
    )


def receipt_payload(receipt: BaseModel) -> dict[str, Any]:
    return receipt.model_dump(mode="json")
