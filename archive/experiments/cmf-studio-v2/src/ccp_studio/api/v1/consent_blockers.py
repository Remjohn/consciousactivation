"""Consent blocker API adapter for TS-CMF-010."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.consent_blockers import ConsentGuardDecision
from ccp_studio.services.consent_guard import ConsentGuardService
from ccp_studio.services.consent_service import ConsentService


class EvaluateConsentBoundaryRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    guest_or_client_id: UUID
    command_type: str
    object_type: str
    object_id: UUID
    require_mapping: bool = False


router = APIRouter(prefix="/api/v1/consent-blockers", tags=["consent-blockers"])
_consent_guard = ConsentGuardService(ConsentService())


def set_consent_guard(service: ConsentGuardService) -> None:
    global _consent_guard
    _consent_guard = service


def get_consent_guard() -> ConsentGuardService:
    return _consent_guard


@router.post("/evaluate", response_model=ConsentGuardDecision)
async def evaluate_consent_boundary(
    request: EvaluateConsentBoundaryRequest,
    service: ConsentGuardService = Depends(get_consent_guard),
) -> ConsentGuardDecision:
    return service.evaluate_workflow_boundary(
        organization_id=request.organization_id,
        brand_id=request.brand_id,
        guest_or_client_id=request.guest_or_client_id,
        command_type=request.command_type,
        object_type=request.object_type,
        object_id=request.object_id,
        require_mapping=request.require_mapping,
    )
