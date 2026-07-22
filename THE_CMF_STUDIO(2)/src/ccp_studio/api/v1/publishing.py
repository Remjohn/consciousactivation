"""FastAPI adapter for TS-CMF-054 Publishing Intent and Publer."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.publishing import PublerJob, PublerWebhookEnvelope, PublishingIntent, PublishingOutcome
from ccp_studio.services.publishing_service import PublishingService


router = APIRouter(prefix="/api/v1/publishing-intents", tags=["publishing-intents"])
_publishing_service: PublishingService | None = None


class DraftPublishingIntentRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    approved_asset_id: UUID
    approval_event_id: UUID | None = None
    consent_record_version_id: UUID | None = None
    approver_user_id: UUID
    platform_variants: list[dict[str, Any]]
    schedule: dict[str, Any]
    idempotency_key: str
    compliance_notes: list[str] = Field(default_factory=list)


class ConfirmPublishingIntentRequest(BaseModel):
    confirmed_by_user_id: UUID
    human_confirmation: bool


class SubmitPublerRequest(BaseModel):
    idempotency_key: str


def set_publishing_service(service: PublishingService) -> None:
    global _publishing_service
    _publishing_service = service


def get_publishing_service() -> PublishingService:
    if _publishing_service is None:
        raise RuntimeError("PublishingService must be configured by the application.")
    return _publishing_service


@router.post("", response_model=PublishingIntent)
def draft_publishing_intent(
    request: DraftPublishingIntentRequest,
    service: PublishingService = Depends(get_publishing_service),
) -> PublishingIntent:
    return service.draft_publishing_intent(**request.model_dump())


@router.post("/{publishing_intent_id}/validate", response_model=PublishingIntent)
def validate_publishing_intent(
    publishing_intent_id: UUID,
    service: PublishingService = Depends(get_publishing_service),
) -> PublishingIntent:
    return service.validate_publishing_intent(publishing_intent_id)


@router.post("/{publishing_intent_id}/confirm", response_model=PublishingIntent)
def confirm_publishing_intent(
    publishing_intent_id: UUID,
    request: ConfirmPublishingIntentRequest,
    service: PublishingService = Depends(get_publishing_service),
) -> PublishingIntent:
    return service.confirm_publishing_intent(publishing_intent_id, **request.model_dump())


@router.post("/{publishing_intent_id}/submit-publer", response_model=PublerJob)
def submit_publishing_intent_to_publer(
    publishing_intent_id: UUID,
    request: SubmitPublerRequest,
    service: PublishingService = Depends(get_publishing_service),
) -> PublerJob:
    return service.submit_publishing_intent_to_publer(
        publishing_intent_id,
        idempotency_key=request.idempotency_key,
    )


@router.post("/publer-webhooks", response_model=PublishingOutcome)
def reconcile_publer_webhook(
    request: PublerWebhookEnvelope,
    service: PublishingService = Depends(get_publishing_service),
) -> PublishingOutcome:
    return service.reconcile_publer_status(request)

