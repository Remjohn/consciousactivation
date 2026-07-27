"""FastAPI adapter for TS-CMF-044 generative provider adapters."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.generative_adapters import GenerativeProviderOutput
from ccp_studio.services.generative_provider_service import GenerativeProviderService


router = APIRouter(prefix="/api/v1/provider-jobs/generative", tags=["generative-provider-adapters"])
_generative_provider_service: GenerativeProviderService | None = None


class SubmitGenerativeProviderJobRequest(BaseModel):
    provider_capability_id: str
    organization_id: UUID
    brand_id: UUID
    actor_id: UUID
    purpose: str
    input_artifact_hashes: list[str]
    input_types: list[str]
    prompt_hash: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)
    consent_record_version_ids: list[UUID] = Field(default_factory=list)
    requires_consent_compatibility: bool = False
    evaluation_target_id: UUID | None = None
    idempotency_key: str


class EvaluateGeneratedAssetRequest(BaseModel):
    actor_id: UUID
    passed: bool
    notes: list[str] = Field(default_factory=list)


def set_generative_provider_service(service: GenerativeProviderService) -> None:
    global _generative_provider_service
    _generative_provider_service = service


def get_generative_provider_service() -> GenerativeProviderService:
    if _generative_provider_service is None:
        raise RuntimeError("GenerativeProviderService must be configured by the application.")
    return _generative_provider_service


@router.post("", response_model=GenerativeProviderOutput)
def submit_generative_provider_job(
    request: SubmitGenerativeProviderJobRequest,
    service: GenerativeProviderService = Depends(get_generative_provider_service),
) -> GenerativeProviderOutput:
    return service.submit_generative_provider_job(**request.model_dump())


@router.post("/outputs/{provider_output_id}/evaluate", response_model=GenerativeProviderOutput)
def evaluate_generated_asset(
    provider_output_id: UUID,
    request: EvaluateGeneratedAssetRequest,
    service: GenerativeProviderService = Depends(get_generative_provider_service),
) -> GenerativeProviderOutput:
    return service.evaluate_generated_asset(
        provider_output_id=provider_output_id,
        actor_id=request.actor_id,
        passed=request.passed,
        notes=request.notes,
    )
