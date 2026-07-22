"""Role policy API adapter for TS-CMF-005."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ccp_studio.contracts.roles import PermissionDecision, RoleAssignment, RoleKey
from ccp_studio.services.role_policy import RolePolicyService


class AssignRoleRequest(BaseModel):
    assigner_actor_id: UUID
    target_actor_id: UUID
    organization_id: UUID
    brand_id: UUID
    role_key: RoleKey


class EvaluatePermissionRequest(BaseModel):
    actor_id: UUID
    command_type: str
    organization_id: UUID
    brand_id: UUID
    source_surface: str


router = APIRouter(prefix="/api/v1/roles", tags=["roles"])
_role_policy = RolePolicyService()


def set_role_policy(service: RolePolicyService) -> None:
    global _role_policy
    _role_policy = service


def get_role_policy() -> RolePolicyService:
    return _role_policy


@router.post("/assign", response_model=RoleAssignment)
async def assign_role(
    request: AssignRoleRequest,
    service: RolePolicyService = Depends(get_role_policy),
) -> RoleAssignment:
    return service.assign_role(
        assigner_actor_id=request.assigner_actor_id,
        target_actor_id=request.target_actor_id,
        organization_id=request.organization_id,
        brand_id=request.brand_id,
        role_key=request.role_key,
    )


@router.post("/evaluate", response_model=PermissionDecision)
async def evaluate_permission(
    request: EvaluatePermissionRequest,
    service: RolePolicyService = Depends(get_role_policy),
) -> PermissionDecision:
    return service.evaluate(
        actor_id=request.actor_id,
        command_type=request.command_type,
        organization_id=request.organization_id,
        brand_id=request.brand_id,
        source_surface=request.source_surface,
    )
