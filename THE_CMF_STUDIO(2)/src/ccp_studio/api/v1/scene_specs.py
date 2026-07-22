"""FastAPI adapter for TS-CMF-037 SceneSpec compilation."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.brand_context_gate import SelectedBrandAssetRef
from ccp_studio.contracts.scene_spec import RenderContract, SceneSpec
from ccp_studio.services.scene_spec_compiler import SceneSpecCompiler


router = APIRouter(prefix="/api/v1/scene-specs", tags=["scene-specs"])
_scene_spec_compiler: SceneSpecCompiler | None = None


class CompileSceneSpecRequest(BaseModel):
    actor_id: UUID
    complete_editing_session_id: UUID
    selected_asset_refs: list[SelectedBrandAssetRef]
    platform_variants: list[dict[str, Any]]
    revision_policy: dict[str, Any]
    subject: dict[str, Any] | None = None
    format: str = "short_video"
    aspect_ratio: str = "9:16"
    duration_seconds: float = 45.0
    content_type: str = "interview_first_short_video"
    visual_style: str = "cmf_paper_cut_expression_engine"
    platform_targets: list[str] | None = None
    message_role: str = "source_backed_expression"
    emotional_intent: str = "recognition_without_overstatement"
    composition_requirements: dict[str, Any] | None = None
    negative_constraints: dict[str, Any] | None = None
    evaluation_requirements: list[dict[str, Any]] | None = None
    renderer_route: str = "deterministic_scene_renderer"


def set_scene_spec_compiler(service: SceneSpecCompiler) -> None:
    global _scene_spec_compiler
    _scene_spec_compiler = service


def get_scene_spec_compiler() -> SceneSpecCompiler:
    if _scene_spec_compiler is None:
        raise RuntimeError("SceneSpecCompiler must be configured by the application.")
    return _scene_spec_compiler


@router.post("", response_model=SceneSpec)
def compile_scene_spec(
    request: CompileSceneSpecRequest,
    service: SceneSpecCompiler = Depends(get_scene_spec_compiler),
) -> SceneSpec:
    return service.compile_scene_spec(
        complete_editing_session_id=request.complete_editing_session_id,
        actor_id=request.actor_id,
        selected_asset_refs=request.selected_asset_refs,
        platform_variants=request.platform_variants,
        revision_policy=request.revision_policy,
        subject=request.subject,
        format=request.format,
        aspect_ratio=request.aspect_ratio,
        duration_seconds=request.duration_seconds,
        content_type=request.content_type,
        visual_style=request.visual_style,
        platform_targets=request.platform_targets,
        message_role=request.message_role,
        emotional_intent=request.emotional_intent,
        composition_requirements=request.composition_requirements,
        negative_constraints=request.negative_constraints,
        evaluation_requirements=request.evaluation_requirements,
        renderer_route=request.renderer_route,
    )


@router.get("/{scene_spec_id}/render-contract", response_model=RenderContract)
def get_render_contract(
    scene_spec_id: UUID,
    service: SceneSpecCompiler = Depends(get_scene_spec_compiler),
) -> RenderContract:
    return service.render_contract_for_scene(scene_spec_id)
