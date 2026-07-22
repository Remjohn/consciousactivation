"""FastAPI adapter for TS-CMF-042 provider jobs."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.provider_jobs import (
    ProviderCapabilityRecord,
    ProviderJob,
    ProviderJobStatus,
    ProviderReceipt,
    ProviderWebhookEnvelope,
)
from ccp_studio.services.provider_operations_service import ProviderOperationsService


router = APIRouter(prefix="/api/v1/provider-jobs", tags=["provider-jobs"])
_provider_operations_service: ProviderOperationsService | None = None


class SubmitProviderJobRequest(BaseModel):
    provider_capability_id: str
    organization_id: UUID
    brand_id: UUID
    requested_by_actor_id: UUID
    complete_editing_session_id: UUID | None = None
    scene_spec_id: UUID | None = None
    input_artifact_hashes: list[str]
    input_types: list[str]
    prompt_hash: str | None = None
    parameters: dict[str, Any] = {}
    idempotency_key: str


class NormalizeProviderResponseRequest(BaseModel):
    status: ProviderJobStatus
    output_artifact_hashes: list[str] = []
    cost_amount: float | None = None
    failure_code: str | None = None
    response_metadata: dict[str, Any] = {}
    provider_correlation_id: str


def set_provider_operations_service(service: ProviderOperationsService) -> None:
    global _provider_operations_service
    _provider_operations_service = service


def get_provider_operations_service() -> ProviderOperationsService:
    if _provider_operations_service is None:
        raise RuntimeError("ProviderOperationsService must be configured by the application.")
    return _provider_operations_service


@router.post("/capabilities", response_model=ProviderCapabilityRecord)
def activate_provider_capability(
    capability: ProviderCapabilityRecord,
    service: ProviderOperationsService = Depends(get_provider_operations_service),
) -> ProviderCapabilityRecord:
    return service.activate_provider_capability(capability)


@router.get("/capabilities/current", response_model=list[ProviderCapabilityRecord])
def seed_current_provider_capabilities(
    service: ProviderOperationsService = Depends(get_provider_operations_service),
) -> list[ProviderCapabilityRecord]:
    return service.seed_current_cmf_capabilities()


@router.post("", response_model=ProviderJob)
def submit_provider_job(
    request: SubmitProviderJobRequest,
    service: ProviderOperationsService = Depends(get_provider_operations_service),
) -> ProviderJob:
    return service.submit_provider_job(**request.model_dump())


@router.post("/{provider_job_id}/responses", response_model=ProviderReceipt)
def normalize_provider_response(
    provider_job_id: UUID,
    request: NormalizeProviderResponseRequest,
    service: ProviderOperationsService = Depends(get_provider_operations_service),
) -> ProviderReceipt:
    return service.normalize_provider_response(provider_job_id=provider_job_id, **request.model_dump())


@router.post("/webhooks/providers", response_model=ProviderReceipt)
def process_provider_webhook(
    envelope: ProviderWebhookEnvelope,
    service: ProviderOperationsService = Depends(get_provider_operations_service),
) -> ProviderReceipt:
    return service.process_provider_webhook(envelope)
