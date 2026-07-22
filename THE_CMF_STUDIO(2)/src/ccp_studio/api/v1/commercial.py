"""Commercial policy API adapter for TS-CMF-006."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.commercial import CommercialEntitlement, PublicContentOffer
from ccp_studio.services.commercial_policy_service import CommercialPolicyService


class CreateCommercialEntitlementRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID
    public_offer: PublicContentOffer
    provider_budget_cents_per_period: int | None = None
    manual_override_above_cents: int | None = None
    max_provider_jobs_per_period: int | None = None


router = APIRouter(prefix="/api/v1/commercial", tags=["commercial"])
_commercial_policy = CommercialPolicyService()


def set_commercial_policy(service: CommercialPolicyService) -> None:
    global _commercial_policy
    _commercial_policy = service


def get_commercial_policy() -> CommercialPolicyService:
    return _commercial_policy


@router.post("/entitlements", response_model=CommercialEntitlement)
async def create_entitlement(
    request: CreateCommercialEntitlementRequest,
    service: CommercialPolicyService = Depends(get_commercial_policy),
) -> CommercialEntitlement:
    return service.create_entitlement(
        organization_id=request.organization_id,
        brand_id=request.brand_id,
        public_offer=request.public_offer,
        provider_budget_cents_per_period=request.provider_budget_cents_per_period,
        manual_override_above_cents=request.manual_override_above_cents,
        max_provider_jobs_per_period=request.max_provider_jobs_per_period,
    )
