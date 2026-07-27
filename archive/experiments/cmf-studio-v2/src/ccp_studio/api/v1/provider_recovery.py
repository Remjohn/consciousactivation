"""FastAPI adapter for TS-CMF-048 provider recovery."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.provider_recovery import (
    OperationalIncident,
    ProviderJobCheckpoint,
    RecoveryActionType,
    RecoveryReceipt,
)
from ccp_studio.services.provider_recovery_service import ProviderRecoveryService


router = APIRouter(prefix="/api/v1/provider-recovery", tags=["provider-recovery"])
_provider_recovery_service: ProviderRecoveryService | None = None


class ProviderCheckpointRequest(BaseModel):
    provider_job_id: UUID
    work_id: str
    completed: bool
    actor_id: UUID
    output_artifact_uri: str | None = None
    output_artifact_hash: str | None = None
    cost_amount: float | None = None
    provider_receipt_id: UUID | None = None


class RecoveryActionRequest(BaseModel):
    provider_job_id: UUID
    actor_id: UUID
    idempotency_key: str
    reason: str
    requeued_work_ids: list[str] = Field(default_factory=list)
    missing_work_ids: list[str] = Field(default_factory=list)
    allow_duplicate_cost: bool = False
    side_effects: list[str] = Field(default_factory=list)


class IncidentRequest(BaseModel):
    provider_job_id: UUID
    incident_type: str
    severity: str = "medium"
    summary: str
    actor_id: UUID
    duplicate_webhook_count: int = 0
    recovery_action_id: UUID | None = None
    evidence_refs: list[str] = Field(default_factory=list)


def set_provider_recovery_service(service: ProviderRecoveryService) -> None:
    global _provider_recovery_service
    _provider_recovery_service = service


def get_provider_recovery_service() -> ProviderRecoveryService:
    if _provider_recovery_service is None:
        raise RuntimeError("ProviderRecoveryService must be configured by the application.")
    return _provider_recovery_service


@router.post("/checkpoints", response_model=ProviderJobCheckpoint)
def record_provider_job_checkpoint(
    request: ProviderCheckpointRequest,
    service: ProviderRecoveryService = Depends(get_provider_recovery_service),
) -> ProviderJobCheckpoint:
    return service.record_provider_job_checkpoint(**request.model_dump())


@router.post("/jobs/{provider_job_id}/pause", response_model=RecoveryReceipt)
def pause_provider_job(
    provider_job_id: UUID,
    request: RecoveryActionRequest,
    service: ProviderRecoveryService = Depends(get_provider_recovery_service),
) -> RecoveryReceipt:
    return service.pause_provider_job(
        provider_job_id=provider_job_id,
        actor_id=request.actor_id,
        idempotency_key=request.idempotency_key,
        reason=request.reason,
    )


@router.post("/jobs/{provider_job_id}/retry", response_model=RecoveryReceipt)
def retry_provider_job(
    provider_job_id: UUID,
    request: RecoveryActionRequest,
    service: ProviderRecoveryService = Depends(get_provider_recovery_service),
) -> RecoveryReceipt:
    return service.retry_provider_job(
        provider_job_id=provider_job_id,
        actor_id=request.actor_id,
        idempotency_key=request.idempotency_key,
        reason=request.reason,
        requeued_work_ids=request.requeued_work_ids,
        allow_duplicate_cost=request.allow_duplicate_cost,
        side_effects=request.side_effects,
    )


@router.post("/jobs/{provider_job_id}/resume", response_model=RecoveryReceipt)
def resume_provider_job(
    provider_job_id: UUID,
    request: RecoveryActionRequest,
    service: ProviderRecoveryService = Depends(get_provider_recovery_service),
) -> RecoveryReceipt:
    return service.resume_provider_job(
        provider_job_id=provider_job_id,
        actor_id=request.actor_id,
        idempotency_key=request.idempotency_key,
        reason=request.reason,
    )


@router.post("/jobs/{provider_job_id}/cancel", response_model=RecoveryReceipt)
def cancel_provider_job(
    provider_job_id: UUID,
    request: RecoveryActionRequest,
    service: ProviderRecoveryService = Depends(get_provider_recovery_service),
) -> RecoveryReceipt:
    return service.cancel_provider_job(
        provider_job_id=provider_job_id,
        actor_id=request.actor_id,
        idempotency_key=request.idempotency_key,
        reason=request.reason,
    )


@router.post("/jobs/{provider_job_id}/compensate", response_model=RecoveryReceipt)
def compensate_provider_job(
    provider_job_id: UUID,
    request: RecoveryActionRequest,
    service: ProviderRecoveryService = Depends(get_provider_recovery_service),
) -> RecoveryReceipt:
    return service.compensate_provider_job(
        provider_job_id=provider_job_id,
        actor_id=request.actor_id,
        idempotency_key=request.idempotency_key,
        reason=request.reason,
        missing_work_ids=request.missing_work_ids,
    )


@router.post("/jobs/{provider_job_id}/block-duplicate-cost", response_model=RecoveryReceipt)
def block_duplicate_cost_recovery(
    provider_job_id: UUID,
    request: RecoveryActionRequest,
    service: ProviderRecoveryService = Depends(get_provider_recovery_service),
) -> RecoveryReceipt:
    return service.block_duplicate_cost_recovery(
        provider_job_id=provider_job_id,
        actor_id=request.actor_id,
        idempotency_key=request.idempotency_key,
        reason=request.reason,
        action_type=RecoveryActionType.escalate,
        risk_reasons=request.side_effects,
    )


@router.post("/incidents", response_model=OperationalIncident)
def record_operational_incident(
    request: IncidentRequest,
    service: ProviderRecoveryService = Depends(get_provider_recovery_service),
) -> OperationalIncident:
    return service.record_operational_incident(**request.model_dump())
