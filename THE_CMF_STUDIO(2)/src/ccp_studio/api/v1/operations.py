"""FastAPI adapter for TS-CMF-059 Operations Board."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from ccp_studio.contracts.operations_board import BlockerSummary, OperationsActionDecision, OperationsBoardState, RecoveryRecommendation
from ccp_studio.services.operations_board_service import OperationsBoardService


router = APIRouter(prefix="/api/v1/operations", tags=["operations"])
_operations_board_service: OperationsBoardService | None = None


class BuildOperationsBoardRequest(BaseModel):
    organization_id: UUID
    brand_id: UUID | None = None
    include_resolved: bool = True
    idempotency_key: str | None = None


class LinkBlockerRequest(BaseModel):
    blocker_type: str
    blocker_code: str
    object_ref: str
    receipt_id: str
    required_action: str
    allowed_command_type: str


class RecommendRecoveryRequest(BaseModel):
    object_ref: str
    recommended_command_type: str
    reason: str
    receipt_refs: list[str] = Field(default_factory=list)


class OperationsActionRequest(BaseModel):
    requested_action: str
    allowed_command_type: str
    manual_database_edit_requested: bool = False


def set_operations_board_service(service: OperationsBoardService) -> None:
    global _operations_board_service
    _operations_board_service = service


def get_operations_board_service() -> OperationsBoardService:
    if _operations_board_service is None:
        raise RuntimeError("OperationsBoardService must be configured by the application.")
    return _operations_board_service


@router.post("/board", response_model=OperationsBoardState)
def build_operations_board(
    request: BuildOperationsBoardRequest,
    service: OperationsBoardService = Depends(get_operations_board_service),
) -> OperationsBoardState:
    return service.build_operations_board_state(**request.model_dump())


@router.post("/blockers", response_model=BlockerSummary)
def link_blocker(
    request: LinkBlockerRequest,
    service: OperationsBoardService = Depends(get_operations_board_service),
) -> BlockerSummary:
    return service.link_blocker_to_object(**request.model_dump())


@router.post("/recommendations", response_model=RecoveryRecommendation)
def recommend_recovery_action(
    request: RecommendRecoveryRequest,
    service: OperationsBoardService = Depends(get_operations_board_service),
) -> RecoveryRecommendation:
    return service.recommend_recovery_action(**request.model_dump())


@router.post("/action-boundary", response_model=OperationsActionDecision)
def operations_action_boundary(
    request: OperationsActionRequest,
    service: OperationsBoardService = Depends(get_operations_board_service),
) -> OperationsActionDecision:
    return service.operations_action_boundary(**request.model_dump())
