"""FastAPI adapter for TS-CMF-046 ComfyUI template migration."""

from __future__ import annotations

from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.comfy_template_migration import MigratedComfyWorkflowAsset
from ccp_studio.services.comfy_template_migration_service import ComfyTemplateMigrationService


router = APIRouter(prefix="/api/v1/comfy-template-migration", tags=["comfy-template-migration"])
_comfy_template_migration_service: ComfyTemplateMigrationService | None = None


class MigrateComfyTemplateRequest(BaseModel):
    legacy_source_path: str
    template_json: dict[str, Any]
    required_inputs: list[dict[str, Any]]
    output_contract: dict[str, Any]
    compatibility_notes: list[dict[str, Any]] = Field(default_factory=list)
    known_defects: list[str] = Field(default_factory=list)
    eval_target: str
    eval_passed: bool = True
    reviewer_id: UUID
    actor_id: UUID


def set_comfy_template_migration_service(service: ComfyTemplateMigrationService) -> None:
    global _comfy_template_migration_service
    _comfy_template_migration_service = service


def get_comfy_template_migration_service() -> ComfyTemplateMigrationService:
    if _comfy_template_migration_service is None:
        raise RuntimeError("ComfyTemplateMigrationService must be configured by the application.")
    return _comfy_template_migration_service


@router.post("", response_model=MigratedComfyWorkflowAsset)
def migrate_comfy_template(
    request: MigrateComfyTemplateRequest,
    service: ComfyTemplateMigrationService = Depends(get_comfy_template_migration_service),
) -> MigratedComfyWorkflowAsset:
    return service.migrate_template_to_worker_asset(**request.model_dump())


@router.post("/{comfy_workflow_asset_id}/activate", response_model=MigratedComfyWorkflowAsset)
def activate_comfy_workflow_asset(
    comfy_workflow_asset_id: UUID,
    actor_id: UUID,
    service: ComfyTemplateMigrationService = Depends(get_comfy_template_migration_service),
) -> MigratedComfyWorkflowAsset:
    return service.activate_comfy_workflow_asset(comfy_workflow_asset_id, actor_id=actor_id)
