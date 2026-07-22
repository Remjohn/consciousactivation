"""FastAPI adapter for TS-CMF-041 scene intelligence."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.scene_intelligence import SceneIntelligenceAuditView, SceneIntelligenceReceipt
from ccp_studio.services.scene_intelligence_service import SceneIntelligenceService


router = APIRouter(prefix="/api/v1/scene-intelligence", tags=["scene-intelligence"])
_scene_intelligence_service: SceneIntelligenceService | None = None


class RunSceneIntelligenceRequest(BaseModel):
    scene_spec_id: UUID
    actor_id: UUID


def set_scene_intelligence_service(service: SceneIntelligenceService) -> None:
    global _scene_intelligence_service
    _scene_intelligence_service = service


def get_scene_intelligence_service() -> SceneIntelligenceService:
    if _scene_intelligence_service is None:
        raise RuntimeError("SceneIntelligenceService must be configured by the application.")
    return _scene_intelligence_service


@router.post("", response_model=SceneIntelligenceReceipt)
def run_scene_intelligence(
    request: RunSceneIntelligenceRequest,
    service: SceneIntelligenceService = Depends(get_scene_intelligence_service),
) -> SceneIntelligenceReceipt:
    return service.run_scene_intelligence(scene_spec_id=request.scene_spec_id, actor_id=request.actor_id)


@router.get("/{scene_spec_id}/audit", response_model=SceneIntelligenceAuditView)
def get_scene_intelligence_audit(
    scene_spec_id: UUID,
    service: SceneIntelligenceService = Depends(get_scene_intelligence_service),
) -> SceneIntelligenceAuditView:
    return service.reconstruct_scene_intelligence(scene_spec_id)
