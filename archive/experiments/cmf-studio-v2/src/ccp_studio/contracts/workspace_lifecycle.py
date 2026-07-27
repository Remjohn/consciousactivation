"""Organization and brand workspace lifecycle contracts for TS-CMF-004."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class WorkspaceStatus(str, Enum):
    active = "active"
    suspended = "suspended"
    archived = "archived"
    restoring = "restoring"


class Organization(BaseModel):
    schema_version: Literal["cmf.organization.v1"]
    organization_id: UUID
    name: str = Field(min_length=1)
    status: WorkspaceStatus
    created_at: datetime
    updated_at: datetime


class BrandWorkspace(BaseModel):
    schema_version: Literal["cmf.brand_workspace.v1"]
    brand_id: UUID
    organization_id: UUID
    display_name: str = Field(min_length=1)
    status: WorkspaceStatus
    default_retention_policy_id: UUID
    created_at: datetime
    updated_at: datetime


class ActiveBrandContext(BaseModel):
    schema_version: Literal["cmf.active_brand_context.v1"]
    actor_id: UUID
    organization_id: UUID
    brand_id: UUID
    selected_at: datetime
    source_surface: str = Field(min_length=1)


class RoleAssignment(BaseModel):
    schema_version: Literal["cmf.role_assignment.v1"]
    role_assignment_id: UUID
    actor_id: UUID
    organization_id: UUID
    brand_id: UUID
    role: str = Field(min_length=1)
    active: bool = True
    created_at: datetime


class RetentionPolicy(BaseModel):
    schema_version: Literal["cmf.retention_policy.v1"]
    retention_policy_id: UUID
    organization_id: UUID
    brand_id: UUID
    policy_name: str = Field(default="default")
    retention_days: int = Field(default=365, ge=1)
    created_at: datetime


class WorkspaceLifecycleEvent(BaseModel):
    schema_version: Literal["cmf.workspace_lifecycle_event.v1"]
    lifecycle_event_id: UUID
    organization_id: UUID
    brand_id: UUID
    event_type: str = Field(min_length=1)
    actor_id: UUID
    command_id: UUID | None = None
    created_at: datetime


class WorkspaceReceipt(BaseModel):
    schema_version: Literal["cmf.workspace_receipt.v1"]
    workspace_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    actor_id: UUID
    action: str = Field(min_length=1)
    status: WorkspaceStatus
    decision: str = Field(min_length=1)
    lifecycle_event_id: UUID | None = None
    command_id: UUID | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime


class WorkspaceInspectionSnapshot(BaseModel):
    schema_version: Literal["cmf.workspace_inspection_snapshot.v1"]
    organization_id: UUID
    brand_id: UUID
    status: WorkspaceStatus
    active_role_count: int = Field(ge=0)
    entitlement_state: str = Field(min_length=1)
    recent_command_ids: list[UUID] = Field(default_factory=list)
    open_blockers: list[str] = Field(default_factory=list)
    production_health: str = Field(min_length=1)
    last_receipt_id: UUID | None = None


class BrandScopedObject(BaseModel):
    object_id: UUID
    organization_id: UUID
    brand_id: UUID
    title: str
    preview_uri: str | None = None


def new_organization(*, organization_id: UUID, name: str) -> Organization:
    now = utc_now()
    return Organization(
        schema_version="cmf.organization.v1",
        organization_id=organization_id,
        name=name,
        status=WorkspaceStatus.active,
        created_at=now,
        updated_at=now,
    )


def new_brand_workspace(
    *,
    organization_id: UUID,
    brand_id: UUID,
    display_name: str,
    default_retention_policy_id: UUID,
) -> BrandWorkspace:
    now = utc_now()
    return BrandWorkspace(
        schema_version="cmf.brand_workspace.v1",
        brand_id=brand_id,
        organization_id=organization_id,
        display_name=display_name,
        status=WorkspaceStatus.active,
        default_retention_policy_id=default_retention_policy_id,
        created_at=now,
        updated_at=now,
    )


def new_workspace_lifecycle_event(
    *,
    organization_id: UUID,
    brand_id: UUID,
    event_type: str,
    actor_id: UUID,
    command_id: UUID | None = None,
) -> WorkspaceLifecycleEvent:
    return WorkspaceLifecycleEvent(
        schema_version="cmf.workspace_lifecycle_event.v1",
        lifecycle_event_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        event_type=event_type,
        actor_id=actor_id,
        command_id=command_id,
        created_at=utc_now(),
    )
