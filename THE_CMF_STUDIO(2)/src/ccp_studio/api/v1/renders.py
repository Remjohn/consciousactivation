"""FastAPI adapter for TS-CMF-043 deterministic rendering."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.deterministic_rendering import DeterministicRenderer, RendererPropsBundle, RenderOutput
from ccp_studio.services.deterministic_rendering_service import DeterministicRenderService


router = APIRouter(prefix="/api/v1/renders", tags=["renders"])
_deterministic_render_service: DeterministicRenderService | None = None


class BuildRendererPropsRequest(BaseModel):
    render_contract_id: UUID
    assembly_plan_id: UUID
    actor_id: UUID
    preferred_renderer: DeterministicRenderer | None = None


class StartDeterministicRenderRequest(BaseModel):
    actor_id: UUID
    idempotency_key: str
    retry_count: int = 0


def set_deterministic_render_service(service: DeterministicRenderService) -> None:
    global _deterministic_render_service
    _deterministic_render_service = service


def get_deterministic_render_service() -> DeterministicRenderService:
    if _deterministic_render_service is None:
        raise RuntimeError("DeterministicRenderService must be configured by the application.")
    return _deterministic_render_service


@router.post("/props", response_model=RendererPropsBundle)
def build_renderer_props_bundle(
    request: BuildRendererPropsRequest,
    service: DeterministicRenderService = Depends(get_deterministic_render_service),
) -> RendererPropsBundle:
    return service.build_renderer_props_bundle(**request.model_dump())


@router.post("/props/{renderer_props_bundle_id}/start", response_model=RenderOutput)
def start_deterministic_render(
    renderer_props_bundle_id: UUID,
    request: StartDeterministicRenderRequest,
    service: DeterministicRenderService = Depends(get_deterministic_render_service),
) -> RenderOutput:
    return service.start_deterministic_render(
        renderer_props_bundle_id=renderer_props_bundle_id,
        actor_id=request.actor_id,
        idempotency_key=request.idempotency_key,
        retry_count=request.retry_count,
    )
