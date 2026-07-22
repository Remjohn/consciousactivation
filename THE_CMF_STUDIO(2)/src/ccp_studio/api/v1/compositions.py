"""FastAPI adapter for TS-CMF-038 composition lineage."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.composition import CompositionJob, CompositionLineageAudit, CompositionPlate
from ccp_studio.services.composition_service import CompositionService


router = APIRouter(prefix="/api/v1/compositions", tags=["compositions"])
_composition_service: CompositionService | None = None


class CompileCompositionJobRequest(BaseModel):
    scene_spec_id: UUID
    actor_id: UUID
    constraints: dict[str, Any] | None = None
    output_requirements: dict[str, Any] | None = None
    final_text_plan: dict[str, Any] | None = None


class SubmitCompositionJobRequest(BaseModel):
    actor_id: UUID


def set_composition_service(service: CompositionService) -> None:
    global _composition_service
    _composition_service = service


def get_composition_service() -> CompositionService:
    if _composition_service is None:
        raise RuntimeError("CompositionService must be configured by the application.")
    return _composition_service


@router.post("/jobs", response_model=CompositionJob)
def compile_composition_job(
    request: CompileCompositionJobRequest,
    service: CompositionService = Depends(get_composition_service),
) -> CompositionJob:
    return service.compile_composition_job(
        scene_spec_id=request.scene_spec_id,
        actor_id=request.actor_id,
        constraints=request.constraints,
        output_requirements=request.output_requirements,
        final_text_plan=request.final_text_plan,
    )


@router.post("/jobs/{composition_job_id}/submit", response_model=CompositionPlate)
def submit_composition_job(
    composition_job_id: UUID,
    request: SubmitCompositionJobRequest,
    service: CompositionService = Depends(get_composition_service),
) -> CompositionPlate:
    return service.submit_ideogram_composition_job(
        composition_job_id=composition_job_id,
        actor_id=request.actor_id,
    )


@router.get("/jobs/{composition_job_id}/lineage", response_model=CompositionLineageAudit)
def get_composition_lineage(
    composition_job_id: UUID,
    service: CompositionService = Depends(get_composition_service),
) -> CompositionLineageAudit:
    return service.audit_composition_lineage(composition_job_id)
