"""Role and permission contracts for TS-CMF-005."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class RoleKey(str, Enum):
    owner = "owner"
    admin = "admin"
    operator = "operator"
    reviewer = "reviewer"
    migration_steward = "migration_steward"
    production_steward = "production_steward"
    publishing_approver = "publishing_approver"
    commercial_administrator = "commercial_administrator"
    service_actor = "service_actor"


class RoleAssignmentStatus(str, Enum):
    active = "active"
    revoked = "revoked"
    expired = "expired"


class RoleAssignment(BaseModel):
    schema_version: Literal["cmf.role_assignment.v1"]
    role_assignment_id: UUID
    actor_id: UUID
    organization_id: UUID
    brand_id: UUID | None = None
    role_key: RoleKey
    status: RoleAssignmentStatus
    assigned_by_actor_id: UUID
    assigned_at: datetime
    revoked_at: datetime | None = None


class CommandPermission(BaseModel):
    schema_version: Literal["cmf.command_permission.v1"]
    permission_key: str = Field(min_length=1)
    command_type: str = Field(min_length=1)
    allowed_roles: list[RoleKey] = Field(min_length=1)
    requires_brand_scope: bool = True
    allowed_surfaces: list[str] = Field(default_factory=list)


class PermissionDecision(BaseModel):
    schema_version: Literal["cmf.permission_decision.v1"]
    actor_id: UUID
    command_type: str
    organization_id: UUID
    brand_id: UUID | None
    allowed: bool
    decision_code: str = Field(min_length=1)
    matched_role_assignment_ids: list[UUID] = Field(default_factory=list)
    decided_at: datetime


class RoleAssignmentReceipt(BaseModel):
    schema_version: Literal["cmf.role_assignment_receipt.v1"]
    role_assignment_receipt_id: UUID
    role_assignment_id: UUID
    organization_id: UUID
    brand_id: UUID | None
    actor_id: UUID
    action: str = Field(min_length=1)
    decision: str = Field(min_length=1)
    written_at: datetime


class MigrationApprovalReceipt(BaseModel):
    schema_version: Literal["cmf.migration_approval_receipt.v1"]
    migration_approval_receipt_id: UUID
    reviewer_actor_id: UUID
    organization_id: UUID
    brand_id: UUID
    source_hash: str = Field(min_length=1)
    target_contract: str = Field(min_length=1)
    fixture_target: str = Field(min_length=1)
    eval_target: str = Field(min_length=1)
    role_assignment_id: UUID
    written_at: datetime


def new_role_assignment(
    *,
    actor_id: UUID,
    organization_id: UUID,
    brand_id: UUID | None,
    role_key: RoleKey,
    assigned_by_actor_id: UUID,
) -> RoleAssignment:
    return RoleAssignment(
        schema_version="cmf.role_assignment.v1",
        role_assignment_id=uuid4(),
        actor_id=actor_id,
        organization_id=organization_id,
        brand_id=brand_id,
        role_key=role_key,
        status=RoleAssignmentStatus.active,
        assigned_by_actor_id=assigned_by_actor_id,
        assigned_at=utc_now(),
    )


def new_permission_decision(
    *,
    actor_id: UUID,
    command_type: str,
    organization_id: UUID,
    brand_id: UUID | None,
    allowed: bool,
    decision_code: str,
    matched_role_assignment_ids: list[UUID] | None = None,
) -> PermissionDecision:
    return PermissionDecision(
        schema_version="cmf.permission_decision.v1",
        actor_id=actor_id,
        command_type=command_type,
        organization_id=organization_id,
        brand_id=brand_id,
        allowed=allowed,
        decision_code=decision_code,
        matched_role_assignment_ids=matched_role_assignment_ids or [],
        decided_at=utc_now(),
    )
