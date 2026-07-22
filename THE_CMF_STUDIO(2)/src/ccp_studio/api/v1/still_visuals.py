"""FastAPI adapter for still visual parent programs."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.still_visuals import (
    StillVisualApprovalReceipt,
    StillVisualCompositionProgram,
    StillVisualExportManifest,
    StillVisualReviewReadModel,
    StillVisualRevisionCommand,
    TelegramStillVisualReviewCard,
)
from ccp_studio.services.still_visual_program_service import StillVisualProgramService


router = APIRouter(prefix="/api/v1/still-visuals", tags=["still-visuals"])
_still_visual_program_service = StillVisualProgramService()


class CreateStillVisualProgramRequest(BaseModel):
    workspace_id: UUID
    brand_context_version_ref: str
    source_evidence_refs: list[str]
    target_format_family: str
    package_slot: str
    platform: str = "instagram"


class RouteProgramRequest(BaseModel):
    archetype_ref: str = "archetype.challenger_frame_breaker.v1"
    target_subtype_hint: str | None = "SPV-CON"


class ApproveProgramRequest(BaseModel):
    operator_id: UUID


class RejectProgramRequest(BaseModel):
    operator_id: UUID
    reason: str


class ReviseProgramRequest(BaseModel):
    revision_scope: str
    reason: str


def set_still_visual_program_service(service: StillVisualProgramService) -> None:
    global _still_visual_program_service
    _still_visual_program_service = service


def get_still_visual_program_service() -> StillVisualProgramService:
    return _still_visual_program_service


@router.post("/programs", response_model=StillVisualCompositionProgram)
def create_program(
    request: CreateStillVisualProgramRequest,
    service: StillVisualProgramService = Depends(get_still_visual_program_service),
) -> StillVisualCompositionProgram:
    return service.create_program(**request.model_dump())


@router.get("/programs/{program_id}", response_model=StillVisualCompositionProgram)
def get_program(
    program_id: UUID,
    service: StillVisualProgramService = Depends(get_still_visual_program_service),
) -> StillVisualCompositionProgram:
    return service.repository.programs[program_id]


@router.post("/programs/{program_id}/route", response_model=StillVisualCompositionProgram)
def route_program(
    program_id: UUID,
    request: RouteProgramRequest,
    service: StillVisualProgramService = Depends(get_still_visual_program_service),
) -> StillVisualCompositionProgram:
    return service.route_program(program_id=program_id, archetype_ref=request.archetype_ref, target_subtype_hint=request.target_subtype_hint)  # type: ignore[arg-type]


@router.post("/programs/{program_id}/materialize", response_model=StillVisualCompositionProgram)
def materialize_program(
    program_id: UUID,
    service: StillVisualProgramService = Depends(get_still_visual_program_service),
) -> StillVisualCompositionProgram:
    return service.materialize_program(program_id=program_id)


@router.post("/programs/{program_id}/render", response_model=StillVisualCompositionProgram)
def render_program(
    program_id: UUID,
    service: StillVisualProgramService = Depends(get_still_visual_program_service),
) -> StillVisualCompositionProgram:
    return service.render_program(program_id=program_id)


@router.post("/programs/{program_id}/evaluate", response_model=StillVisualCompositionProgram)
def evaluate_program(
    program_id: UUID,
    service: StillVisualProgramService = Depends(get_still_visual_program_service),
) -> StillVisualCompositionProgram:
    return service.evaluate_program(program_id=program_id)


@router.get("/programs/{program_id}/review", response_model=StillVisualReviewReadModel)
def review_program(
    program_id: UUID,
    service: StillVisualProgramService = Depends(get_still_visual_program_service),
) -> StillVisualReviewReadModel:
    return service.build_review_read_model(program_id=program_id)


@router.get("/programs/{program_id}/telegram-review", response_model=TelegramStillVisualReviewCard)
def telegram_review_program(
    program_id: UUID,
    service: StillVisualProgramService = Depends(get_still_visual_program_service),
) -> TelegramStillVisualReviewCard:
    return service.build_telegram_card(program_id=program_id)


@router.post("/programs/{program_id}/approve", response_model=StillVisualApprovalReceipt)
def approve_program(
    program_id: UUID,
    request: ApproveProgramRequest,
    service: StillVisualProgramService = Depends(get_still_visual_program_service),
) -> StillVisualApprovalReceipt:
    return service.approve_program(program_id=program_id, operator_id=request.operator_id)


@router.post("/programs/{program_id}/reject", response_model=StillVisualApprovalReceipt)
def reject_program(
    program_id: UUID,
    request: RejectProgramRequest,
    service: StillVisualProgramService = Depends(get_still_visual_program_service),
) -> StillVisualApprovalReceipt:
    return service.reject_program(program_id=program_id, operator_id=request.operator_id, reason=request.reason)


@router.post("/programs/{program_id}/revise", response_model=StillVisualRevisionCommand)
def revise_program(
    program_id: UUID,
    request: ReviseProgramRequest,
    service: StillVisualProgramService = Depends(get_still_visual_program_service),
) -> StillVisualRevisionCommand:
    return service.revise_program(program_id=program_id, revision_scope=request.revision_scope, reason=request.reason)


@router.post("/programs/{program_id}/export", response_model=StillVisualExportManifest)
def export_program(
    program_id: UUID,
    service: StillVisualProgramService = Depends(get_still_visual_program_service),
) -> StillVisualExportManifest:
    return service.export_program(program_id=program_id)
