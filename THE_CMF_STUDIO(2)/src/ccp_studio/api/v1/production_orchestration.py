"""FastAPI adapter for Batch 3 production orchestration."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.production_orchestration import (
    CapabilityRouteRequest,
    HumanApprovalReceipt,
    ProductionManifestActivationReceipt,
    ProductionPipelineManifestDraft,
    ProviderMenuSnapshot,
    ProviderRouteDecisionReceipt,
    RenderRuntimeLock,
    RenderRuntimeSelectionRequest,
    StageDirectorSkillSpec,
)
from ccp_studio.services.production_orchestration_service import ProductionOrchestrationService


router = APIRouter(prefix="/api/v1/production-orchestration", tags=["production-orchestration"])
_production_orchestration_service = ProductionOrchestrationService()


class ManifestRequest(BaseModel):
    manifest_code: str = "CMF-PRODUCTION-MANIFEST-V1"
    project_type: str = "interview_first_asset_pack"


class StageSkillInvokeRequest(BaseModel):
    skill_id: UUID
    manifest_snapshot_id: UUID
    source_context_refs: list[str]
    requested_output_artifact_type: str = "stage_artifact"


class RuntimeLockRequest(BaseModel):
    selection_request: RenderRuntimeSelectionRequest
    candidates: list[dict]


class ArtifactApprovalRequest(BaseModel):
    review_request_id: UUID
    reviewer_id: UUID
    approve: bool = True


def set_production_orchestration_service(service: ProductionOrchestrationService) -> None:
    global _production_orchestration_service
    _production_orchestration_service = service


def get_production_orchestration_service() -> ProductionOrchestrationService:
    return _production_orchestration_service


@router.post("/manifests", response_model=ProductionPipelineManifestDraft)
def create_manifest(
    request: ManifestRequest,
    service: ProductionOrchestrationService = Depends(get_production_orchestration_service),
) -> ProductionPipelineManifestDraft:
    return service.create_manifest_draft(manifest_code=request.manifest_code, project_type=request.project_type)


@router.post("/manifests/{manifest_id}/activate", response_model=ProductionManifestActivationReceipt)
def activate_manifest(
    manifest_id: UUID,
    service: ProductionOrchestrationService = Depends(get_production_orchestration_service),
) -> ProductionManifestActivationReceipt:
    snapshot = service.validate_manifest(service.repository.manifest_drafts[manifest_id])
    return service.activate_manifest(snapshot)


@router.post("/stage-skills", response_model=StageDirectorSkillSpec)
def register_stage_skill(
    service: ProductionOrchestrationService = Depends(get_production_orchestration_service),
) -> StageDirectorSkillSpec:
    return service.register_stage_skill()


@router.post("/provider-menu", response_model=ProviderMenuSnapshot)
def build_provider_menu(
    service: ProductionOrchestrationService = Depends(get_production_orchestration_service),
) -> ProviderMenuSnapshot:
    return service.build_provider_menu()


@router.post("/provider-route", response_model=ProviderRouteDecisionReceipt)
def route_provider(
    request: CapabilityRouteRequest,
    service: ProductionOrchestrationService = Depends(get_production_orchestration_service),
) -> ProviderRouteDecisionReceipt:
    return service.route_provider(request, service.build_provider_menu())


@router.post("/runtime/lock", response_model=RenderRuntimeLock)
def lock_runtime(
    request: RuntimeLockRequest,
    service: ProductionOrchestrationService = Depends(get_production_orchestration_service),
) -> RenderRuntimeLock:
    from ccp_studio.contracts.production_orchestration import RenderRuntimeCandidate

    candidates = [RenderRuntimeCandidate(**item) for item in request.candidates]
    return service.select_and_lock_runtime(request.selection_request, candidates)


@router.post("/artifacts/approve", response_model=HumanApprovalReceipt)
def approve_artifact(
    request: ArtifactApprovalRequest,
    service: ProductionOrchestrationService = Depends(get_production_orchestration_service),
) -> HumanApprovalReceipt:
    return service.decide_human_approval(
        review_request_id=request.review_request_id,
        reviewer_id=request.reviewer_id,
        approve=request.approve,
    )
