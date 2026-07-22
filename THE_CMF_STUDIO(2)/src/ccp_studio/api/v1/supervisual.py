"""FastAPI adapter for SuperVisual project production."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from ccp_studio.contracts.supervisual_projects import (
    SuperVisualApprovalReceipt,
    SuperVisualExportArtifact,
    SuperVisualProject,
    SuperVisualTimelineReadModel,
    SuperVisualVariant,
)
from ccp_studio.services.supervisual_project_service import SuperVisualProjectService, SuperVisualProjectServiceError


router = APIRouter(prefix="/api/v1/supervisual", tags=["supervisual"])
_supervisual_project_service = SuperVisualProjectService()


class CreateSuperVisualProjectRequest(BaseModel):
    project_name: str
    workspace_id: UUID
    brand_context_version_ref: str
    source_evidence_refs: list[str]
    brand_id: UUID | None = None
    context_type: str = "manual_context"
    interview_brief_ref: str | None = None
    transcript_ref: str | None = None
    context_payload: dict = Field(default_factory=dict)
    frame_profile_code: str = "4:5_FEED_POSTER"
    style_route_code: str = "GMG_EXPERT_05_EDITORIAL_SCRIBE"


class BuildSuperVisualProjectRequest(BaseModel):
    frame_profile_code: str | None = None
    style_route_code: str | None = None
    primitive_score: float = 0.92
    doctrine_score: float = 0.91
    source_truth_score: float = 0.94
    frame_profile_score: float = 0.95
    style_route_score: float = 0.93


class ReviseSuperVisualProjectRequest(BuildSuperVisualProjectRequest):
    revision_instruction: str


class ApproveSuperVisualProjectRequest(BaseModel):
    operator_id: UUID
    variant_id: UUID | None = None


class RejectSuperVisualProjectRequest(BaseModel):
    operator_id: UUID
    reason: str
    variant_id: UUID | None = None


class ExportSuperVisualProjectRequest(BaseModel):
    variant_id: UUID | None = None


def set_supervisual_project_service(service: SuperVisualProjectService) -> None:
    global _supervisual_project_service
    _supervisual_project_service = service


def get_supervisual_project_service() -> SuperVisualProjectService:
    return _supervisual_project_service


@router.post("/projects", response_model=SuperVisualProject)
def create_project(
    request: CreateSuperVisualProjectRequest,
    service: SuperVisualProjectService = Depends(get_supervisual_project_service),
) -> SuperVisualProject:
    return _guard(lambda: service.create_project(**request.model_dump()))


@router.get("/projects/{project_id}", response_model=SuperVisualProject)
def get_project(
    project_id: UUID,
    service: SuperVisualProjectService = Depends(get_supervisual_project_service),
) -> SuperVisualProject:
    return _guard(lambda: service.get_project(project_id=project_id))


@router.post("/projects/{project_id}/build", response_model=SuperVisualVariant)
def build_project(
    project_id: UUID,
    request: BuildSuperVisualProjectRequest,
    service: SuperVisualProjectService = Depends(get_supervisual_project_service),
) -> SuperVisualVariant:
    return _guard(lambda: service.build_project(project_id=project_id, **request.model_dump()))


@router.post("/projects/{project_id}/revise", response_model=SuperVisualVariant)
def revise_project(
    project_id: UUID,
    request: ReviseSuperVisualProjectRequest,
    service: SuperVisualProjectService = Depends(get_supervisual_project_service),
) -> SuperVisualVariant:
    return _guard(lambda: service.revise_project(project_id=project_id, **request.model_dump()))


@router.post("/projects/{project_id}/approve", response_model=SuperVisualApprovalReceipt)
def approve_project(
    project_id: UUID,
    request: ApproveSuperVisualProjectRequest,
    service: SuperVisualProjectService = Depends(get_supervisual_project_service),
) -> SuperVisualApprovalReceipt:
    return _guard(lambda: service.approve_project(project_id=project_id, operator_id=request.operator_id, variant_id=request.variant_id))


@router.post("/projects/{project_id}/reject", response_model=SuperVisualApprovalReceipt)
def reject_project(
    project_id: UUID,
    request: RejectSuperVisualProjectRequest,
    service: SuperVisualProjectService = Depends(get_supervisual_project_service),
) -> SuperVisualApprovalReceipt:
    return _guard(lambda: service.reject_project(project_id=project_id, operator_id=request.operator_id, reason=request.reason, variant_id=request.variant_id))


@router.post("/projects/{project_id}/export", response_model=SuperVisualExportArtifact)
def export_project(
    project_id: UUID,
    request: ExportSuperVisualProjectRequest | None = None,
    service: SuperVisualProjectService = Depends(get_supervisual_project_service),
) -> SuperVisualExportArtifact:
    variant_id = request.variant_id if request else None
    return _guard(lambda: service.export_project(project_id=project_id, variant_id=variant_id))


@router.get("/projects/{project_id}/timeline", response_model=SuperVisualTimelineReadModel)
def get_timeline(
    project_id: UUID,
    service: SuperVisualProjectService = Depends(get_supervisual_project_service),
) -> SuperVisualTimelineReadModel:
    return _guard(lambda: service.get_timeline(project_id=project_id))


def _guard(operation):
    try:
        return operation()
    except SuperVisualProjectServiceError as exc:
        raise HTTPException(status_code=400, detail={"code": exc.code, "message": exc.message}) from exc
