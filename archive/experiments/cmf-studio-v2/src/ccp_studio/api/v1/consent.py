"""Consent API adapter for TS-CMF-008."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.consent import ConsentRecordVersion, ConsentScope
from ccp_studio.services.consent_service import ConsentService


class GrantConsentRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    guest_or_client_id: UUID
    actor_id: UUID
    scope: ConsentScope
    evidence_refs: list[str]


router = APIRouter(prefix="/api/v1/consent", tags=["consent"])
_consent_service = ConsentService()


def set_consent_service(service: ConsentService) -> None:
    global _consent_service
    _consent_service = service


def get_consent_service() -> ConsentService:
    return _consent_service


@router.post("/grant", response_model=ConsentRecordVersion)
async def grant_consent(
    request: GrantConsentRequest,
    service: ConsentService = Depends(get_consent_service),
) -> ConsentRecordVersion:
    return service.grant_consent(
        organization_id=request.organization_id,
        brand_id=request.brand_id,
        guest_or_client_id=request.guest_or_client_id,
        scope=request.scope,
        actor_id=request.actor_id,
        evidence_refs=request.evidence_refs,
    )
