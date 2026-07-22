"""FastAPI adapter for TS-CMF-039 assembly planning."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.assembly import AssemblyPlan
from ccp_studio.services.assembly_planner import AssemblyPlanner


router = APIRouter(prefix="/api/v1/assembly-plans", tags=["assembly-plans"])
_assembly_planner: AssemblyPlanner | None = None


class CompileAssemblyPlanRequest(BaseModel):
    scene_spec_id: UUID
    actor_id: UUID
    caption_cues: list[dict[str, Any]] | None = None
    audio_components: list[dict[str, Any]] | None = None


def set_assembly_planner(service: AssemblyPlanner) -> None:
    global _assembly_planner
    _assembly_planner = service


def get_assembly_planner() -> AssemblyPlanner:
    if _assembly_planner is None:
        raise RuntimeError("AssemblyPlanner must be configured by the application.")
    return _assembly_planner


@router.post("", response_model=AssemblyPlan)
def compile_assembly_plan(
    request: CompileAssemblyPlanRequest,
    service: AssemblyPlanner = Depends(get_assembly_planner),
) -> AssemblyPlan:
    return service.compile_assembly_plan(
        scene_spec_id=request.scene_spec_id,
        actor_id=request.actor_id,
        caption_cues=request.caption_cues,
        audio_components=request.audio_components,
    )


@router.get("/{assembly_plan_id}", response_model=AssemblyPlan)
def get_assembly_plan(
    assembly_plan_id: UUID,
    service: AssemblyPlanner = Depends(get_assembly_planner),
) -> AssemblyPlan:
    return service.validate_assembly_plan(assembly_plan_id)
