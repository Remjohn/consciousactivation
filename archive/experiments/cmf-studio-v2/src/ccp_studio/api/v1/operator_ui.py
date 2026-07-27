"""FastAPI adapter for TS-CMF-070 Operator UI architecture."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.operator_ui import (
    AgentFactoryState,
    ContentAssetCodeParts,
    ContentAssetFormatRegistryState,
    OperatorShellState,
    UiActionReceipt,
    UiBlockerSummary,
    UiCommandEnvelope,
    UiSurface,
    WorkspaceControlTowerState,
)
from ccp_studio.services.operator_ui_service import OperatorUiService


router = APIRouter(prefix="/api/v1/operator-ui", tags=["operator-ui"])
_operator_ui_service = OperatorUiService()


class BuildShellRequest(BaseModel):
    operator_user_id: UUID
    active_role_key: str
    organization_id: UUID
    organization_name: str
    brand_workspace_id: UUID
    brand_workspace_code: str
    brand_workspace_display_name: str
    guest_id: UUID | None = None
    guest_code: str | None = None
    guest_display_name: str | None = None
    blockers: list[UiBlockerSummary] = Field(default_factory=list)


class RenderAssetCodeRequest(BaseModel):
    brand_workspace_code: str
    guest_code: str
    session_code: str
    package_code: str
    format_code: str
    sequence_number: int
    version_number: int


class CreateCommandRequest(BaseModel):
    requested_by_user_id: UUID
    requested_role_key: str
    organization_id: UUID
    brand_workspace_id: UUID
    guest_id: UUID | None = None
    active_object_type: str
    active_object_id: UUID
    command_type: str
    command_payload: dict = Field(default_factory=dict)
    source_surface: UiSurface
    source_route: str
    expected_object_version: str | None = None


class SubmitCommandRequest(BaseModel):
    envelope: UiCommandEnvelope
    blockers: list[UiBlockerSummary] = Field(default_factory=list)
    content_asset_code: str | None = None
    object_version_current: bool = True
    pwa_deep_link: str | None = None


def set_operator_ui_service(service: OperatorUiService) -> None:
    global _operator_ui_service
    _operator_ui_service = service


def get_operator_ui_service() -> OperatorUiService:
    return _operator_ui_service


@router.post("/shell", response_model=OperatorShellState)
def build_shell(
    request: BuildShellRequest,
    service: OperatorUiService = Depends(get_operator_ui_service),
) -> OperatorShellState:
    return service.build_shell_state(
        operator_user_id=request.operator_user_id,
        active_role_key=request.active_role_key,
        organization_id=request.organization_id,
        organization_name=request.organization_name,
        brand_workspace_id=request.brand_workspace_id,
        brand_workspace_code=request.brand_workspace_code,
        brand_workspace_display_name=request.brand_workspace_display_name,
        guest_id=request.guest_id,
        guest_code=request.guest_code,
        guest_display_name=request.guest_display_name,
        blockers=request.blockers,
    )


@router.post("/control-tower", response_model=WorkspaceControlTowerState)
def build_control_tower(
    shell: OperatorShellState,
    service: OperatorUiService = Depends(get_operator_ui_service),
) -> WorkspaceControlTowerState:
    return service.build_control_tower_state(shell)


@router.get("/content-formats", response_model=ContentAssetFormatRegistryState)
def content_formats(
    service: OperatorUiService = Depends(get_operator_ui_service),
) -> ContentAssetFormatRegistryState:
    return service.content_format_registry()


@router.post("/asset-codes/render", response_model=ContentAssetCodeParts)
def render_asset_code(
    request: RenderAssetCodeRequest,
    service: OperatorUiService = Depends(get_operator_ui_service),
) -> ContentAssetCodeParts:
    return service.render_asset_code(**request.model_dump())


@router.post("/commands", response_model=UiCommandEnvelope)
def create_command(
    request: CreateCommandRequest,
    service: OperatorUiService = Depends(get_operator_ui_service),
) -> UiCommandEnvelope:
    return service.create_command_envelope(
        requested_by_user_id=request.requested_by_user_id,
        requested_role_key=request.requested_role_key,
        organization_id=request.organization_id,
        brand_workspace_id=request.brand_workspace_id,
        guest_id=request.guest_id,
        active_object_type=request.active_object_type,
        active_object_id=request.active_object_id,
        command_type=request.command_type,
        command_payload=request.command_payload,
        source_surface=request.source_surface,
        source_route=request.source_route,
        expected_object_version=request.expected_object_version,
    )


@router.post("/commands/submit", response_model=UiActionReceipt)
def submit_command(
    request: SubmitCommandRequest,
    service: OperatorUiService = Depends(get_operator_ui_service),
) -> UiActionReceipt:
    return service.submit_ui_command(
        request.envelope,
        blockers=request.blockers,
        content_asset_code=request.content_asset_code,
        object_version_current=request.object_version_current,
        pwa_deep_link=request.pwa_deep_link,
    )


@router.get("/agent-factory/{brand_workspace_id}", response_model=AgentFactoryState)
def agent_factory_state(
    brand_workspace_id: UUID,
    service: OperatorUiService = Depends(get_operator_ui_service),
) -> AgentFactoryState:
    return service.build_agent_factory_state(brand_workspace_id=brand_workspace_id)
