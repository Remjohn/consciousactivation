"""Operations Board contracts for TS-CMF-059."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class QueueSnapshot(BaseModel):
    schema_version: Literal["cmf.queue_snapshot.v1"] = "cmf.queue_snapshot.v1"
    queue_name: str = Field(min_length=1)
    depth: int = Field(ge=0)
    active_count: int = Field(ge=0)
    failed_count: int = Field(ge=0)
    oldest_job_age_seconds: int | None = Field(default=None, ge=0)


class WorkerStatusSnapshot(BaseModel):
    schema_version: Literal["cmf.worker_status_snapshot.v1"] = "cmf.worker_status_snapshot.v1"
    worker_id: str = Field(min_length=1)
    worker_type: str = Field(min_length=1)
    status: Literal["idle", "running", "draining", "failed", "offline"]
    gpu_tier: str | None = None
    active_job_ids: list[str] = Field(default_factory=list)
    current_cost_estimate_usd: float | None = Field(default=None, ge=0)
    shutdown_status: str | None = None


class ProviderStatusSnapshot(BaseModel):
    schema_version: Literal["cmf.provider_status_snapshot.v1"] = "cmf.provider_status_snapshot.v1"
    provider_name: str = Field(min_length=1)
    status: Literal["healthy", "degraded", "outage"]
    affected_job_ids: list[str] = Field(default_factory=list)
    completed_artifact_hashes: list[str] = Field(default_factory=list)
    safe_retry_available: bool
    cost_estimate_usd: float = Field(ge=0)
    blocker_codes: list[str] = Field(default_factory=list)
    recommended_action: str | None = None


class CostSnapshot(BaseModel):
    schema_version: Literal["cmf.cost_snapshot.v1"] = "cmf.cost_snapshot.v1"
    total_cost_usd: float = Field(ge=0)
    provider_cost_usd: float = Field(ge=0)
    gpu_cost_usd: float = Field(ge=0)
    recovery_risk_usd: float = Field(ge=0)


class BlockerSummary(BaseModel):
    schema_version: Literal["cmf.blocker_summary.v1"] = "cmf.blocker_summary.v1"
    blocker_type: Literal["consent", "approval", "publishing", "memory", "projection"]
    blocker_code: str = Field(min_length=1)
    object_ref: str = Field(min_length=1)
    receipt_id: str = Field(min_length=1)
    required_action: str = Field(min_length=1)
    allowed_command_type: str = Field(min_length=1)


class IncidentSummary(BaseModel):
    schema_version: Literal["cmf.incident_summary.v1"] = "cmf.incident_summary.v1"
    incident_id: str = Field(min_length=1)
    provider_job_id: str = Field(min_length=1)
    severity: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    resolved: bool
    recovery_action_ids: list[str] = Field(default_factory=list)
    receipt_ids: list[str] = Field(default_factory=list)


class RecoveryRecommendation(BaseModel):
    schema_version: Literal["cmf.recovery_recommendation.v1"] = "cmf.recovery_recommendation.v1"
    recommendation_id: UUID
    object_ref: str = Field(min_length=1)
    recommended_command_type: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    receipt_refs: list[str] = Field(default_factory=list)
    manual_database_edit_allowed: bool = False


class OperationsBoardState(BaseModel):
    schema_version: Literal["cmf.operations_board_state.v1"]
    board_state_id: UUID
    organization_id: UUID
    brand_id: UUID | None = None
    queues: list[QueueSnapshot] = Field(default_factory=list)
    workers: list[WorkerStatusSnapshot] = Field(default_factory=list)
    blockers: list[BlockerSummary] = Field(default_factory=list)
    provider_statuses: list[ProviderStatusSnapshot] = Field(default_factory=list)
    incident_ids: list[str] = Field(default_factory=list)
    incidents: list[IncidentSummary] = Field(default_factory=list)
    workflow_checkpoint_refs: list[str] = Field(default_factory=list)
    cost_snapshot: CostSnapshot
    projection_health: str
    recovery_recommendations: list[RecoveryRecommendation] = Field(default_factory=list)
    generated_at: datetime


class OperationsActionDecision(BaseModel):
    schema_version: Literal["cmf.operations_action_decision.v1"]
    requested_action: str = Field(min_length=1)
    allowed_command_type: str = Field(min_length=1)
    manual_database_edit_allowed: bool
    reason: str = Field(min_length=1)


class OperationsReceipt(BaseModel):
    schema_version: Literal["cmf.operations_receipt.v1"]
    operations_receipt_id: UUID
    board_state_id: UUID
    organization_id: UUID
    brand_id: UUID | None = None
    source_query_snapshot: dict[str, Any] = Field(default_factory=dict)
    blocker_count: int = Field(ge=0)
    incident_count: int = Field(ge=0)
    cost_summary: CostSnapshot
    projection_health: str = Field(min_length=1)
    recommended_recovery_actions: list[str] = Field(default_factory=list)
    receipt_hash: str = Field(min_length=1)
    written_at: datetime


class OperationsDomainEvent(BaseModel):
    schema_version: Literal["cmf.operations_domain_event.v1"]
    operations_event_id: UUID
    event_type: str = Field(min_length=1)
    board_state_id: UUID | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


def operations_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_operations_receipt(
    *,
    state: OperationsBoardState,
    source_query_snapshot: dict[str, Any],
) -> OperationsReceipt:
    recommended = [item.recommended_command_type for item in state.recovery_recommendations]
    payload = {
        "board_state_id": state.board_state_id,
        "organization_id": state.organization_id,
        "brand_id": state.brand_id,
        "source_query_snapshot": source_query_snapshot,
        "blocker_count": len(state.blockers),
        "incident_count": len(state.incidents),
        "cost_summary": state.cost_snapshot.model_dump(mode="json"),
        "projection_health": state.projection_health,
        "recommended_recovery_actions": recommended,
    }
    return OperationsReceipt(
        schema_version="cmf.operations_receipt.v1",
        operations_receipt_id=uuid4(),
        board_state_id=state.board_state_id,
        organization_id=state.organization_id,
        brand_id=state.brand_id,
        source_query_snapshot=source_query_snapshot,
        blocker_count=len(state.blockers),
        incident_count=len(state.incidents),
        cost_summary=state.cost_snapshot,
        projection_health=state.projection_health,
        recommended_recovery_actions=recommended,
        receipt_hash=operations_hash(payload),
        written_at=utc_now(),
    )
