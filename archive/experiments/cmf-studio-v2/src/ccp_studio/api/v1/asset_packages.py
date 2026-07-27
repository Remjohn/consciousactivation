"""FastAPI adapter for TS-CMF-034 asset package specs."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.asset_package import AssetPackageSpec, CompleteEditingSessionRequestCandidate
from ccp_studio.services.asset_package_service import AssetPackageService


router = APIRouter(prefix="/api/v1/asset-packages", tags=["asset-packages"])
_asset_package_service: AssetPackageService | None = None


class GenerateTrialGuestAssetPackSpecRequest(BaseModel):
    actor_id: UUID
    expression_session_id: UUID
    asset_route_receipt_ids: list[UUID]


class PrepareEditingSessionRequestsRequest(BaseModel):
    actor_id: UUID


def set_asset_package_service(service: AssetPackageService) -> None:
    global _asset_package_service
    _asset_package_service = service


def get_asset_package_service() -> AssetPackageService:
    if _asset_package_service is None:
        raise RuntimeError("AssetPackageService must be configured by the application.")
    return _asset_package_service


@router.post("/brands/{brand_id}/trial", response_model=AssetPackageSpec)
def generate_trial_guest_asset_pack_spec(
    brand_id: UUID,
    organization_id: UUID,
    request: GenerateTrialGuestAssetPackSpecRequest,
    service: AssetPackageService = Depends(get_asset_package_service),
) -> AssetPackageSpec:
    return service.generate_trial_guest_asset_pack_spec(
        organization_id=organization_id,
        brand_id=brand_id,
        expression_session_id=request.expression_session_id,
        asset_route_receipt_ids=request.asset_route_receipt_ids,
        actor_id=request.actor_id,
    )


@router.post("/{asset_package_spec_id}/editing-session-requests", response_model=list[CompleteEditingSessionRequestCandidate])
def prepare_editing_session_requests(
    asset_package_spec_id: UUID,
    request: PrepareEditingSessionRequestsRequest,
    service: AssetPackageService = Depends(get_asset_package_service),
) -> list[CompleteEditingSessionRequestCandidate]:
    return service.prepare_editing_session_requests(
        asset_package_spec_id=asset_package_spec_id,
        actor_id=request.actor_id,
    )
