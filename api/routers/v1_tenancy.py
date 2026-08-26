"""Versioned FastAPI Router for CAE Workspace, Membership, and Operator Grant Management.

Governed by TS-CAE-TEN-001, FR-CAE-TEN-001 through FR-CAE-TEN-005, and CA-TWC-01 Mandate §3 T3.
Enforces typed Pydantic V2 payloads, tenant isolation, and atomic immutable receipt ledger emission.
"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Generator, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
import psycopg
from pydantic import BaseModel, Field

from ca_runtime.database import get_staging_postgres_connection
from ca_runtime.tenancy import TenantContext, TenancyViolationError, CrossWorkspaceLeakError
from ca_runtime.workspace_core import (
    AddMembershipInput,
    CreateWorkspaceInput,
    IssueOperatorGrantInput,
    MembershipError,
    MembershipExistsError,
    MembershipNotFoundError,
    MembershipResult,
    OperatorGrantError,
    OperatorGrantExistsError,
    OperatorGrantExpiredError,
    OperatorGrantNotFoundError,
    OperatorGrantResult,
    OperatorOrgNotFoundError,
    RemoveMembershipInput,
    RevokeOperatorGrantInput,
    UnauthorizedAccessError,
    UpdateWorkspaceInput,
    WorkspaceConflictError,
    WorkspaceError,
    WorkspaceNotFoundError,
    WorkspaceResult,
    add_workspace_membership,
    create_workspace,
    get_workspace,
    issue_operator_grant,
    remove_workspace_membership,
    revoke_operator_grant,
    update_workspace,
)

router = APIRouter(prefix="/v1/workspaces", tags=["cae-tenancy-v1"])


# --- Database Connection Dependency ---

def get_db_connection() -> Generator[psycopg.Connection[Any], None, None]:
    """Provide a connection to the PostgreSQL staging database."""
    conn = get_staging_postgres_connection()
    try:
        yield conn
    finally:
        conn.close()


# --- Tenant Context Dependency ---

def get_tenant_context(
    x_actor_id: Optional[str] = Header(None, alias="X-Actor-Id"),
    x_workspace_id: Optional[str] = Header(None, alias="X-Workspace-Id"),
    x_role: Optional[str] = Header("MEMBER", alias="X-Role"),
    x_is_operator: Optional[str] = Header("false", alias="X-Is-Operator"),
    x_operator_grant_id: Optional[str] = Header(None, alias="X-Operator-Grant-Id"),
) -> TenantContext:
    """Extract and validate TenantContext from request headers."""
    actor_id = x_actor_id or "system-anonymous"
    is_operator = (x_is_operator or "").lower() in ("true", "1", "yes")

    ws_id: UUID
    if x_workspace_id:
        try:
            ws_id = UUID(x_workspace_id)
        except ValueError as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid X-Workspace-Id header format: {x_workspace_id}",
            ) from err
    else:
        # Default placeholder workspace for global operator actions if omitted
        ws_id = UUID("00000000-0000-0000-0000-000000000000")

    op_grant_id: Optional[UUID] = None
    if x_operator_grant_id:
        try:
            op_grant_id = UUID(x_operator_grant_id)
        except ValueError as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid X-Operator-Grant-Id header format: {x_operator_grant_id}",
            ) from err

    try:
        return TenantContext(
            workspace_id=ws_id,
            actor_id=actor_id,
            role=x_role or "MEMBER",
            is_operator=is_operator,
            operator_grant_id=op_grant_id,
        )
    except UnauthorizedOperatorAccessError as err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operator context requires a valid X-Operator-Grant-Id header",
        ) from err
    except TenancyViolationError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        ) from err



# --- HTTP Request Bodies ---

class CreateWorkspaceRequestBody(BaseModel):
    slug: str = Field(..., min_length=2, max_length=64, pattern=r"^[a-z0-9-]+$")
    display_name: str = Field(..., min_length=1, max_length=255)


class UpdateWorkspaceRequestBody(BaseModel):
    display_name: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[str] = Field(None, pattern=r"^(ACTIVE|SUSPENDED|ARCHIVED)$")


class AddMembershipRequestBody(BaseModel):
    actor_id: str = Field(..., min_length=1, max_length=128)
    role: str = Field("MEMBER", pattern=r"^(ADMIN|MEMBER|VIEWER)$")


class IssueOperatorGrantRequestBody(BaseModel):
    operator_org_id: UUID
    operator_actor_id: str = Field(..., min_length=1, max_length=128)
    justification: str = Field(..., min_length=1)
    expires_at: datetime


# --- Endpoints ---

@router.post("", response_model=WorkspaceResult, status_code=status.HTTP_201_CREATED)
def provision_workspace_endpoint(
    body: CreateWorkspaceRequestBody,
    session: TenantContext = Depends(get_tenant_context),
    conn: psycopg.Connection[Any] = Depends(get_db_connection),
) -> WorkspaceResult:
    """Create a new isolated workspace and register creator as initial ADMIN."""
    try:
        return create_workspace(
            CreateWorkspaceInput(slug=body.slug, display_name=body.display_name),
            session=session,
            conn=conn,
        )
    except WorkspaceConflictError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err


@router.get("/{workspace_id}", response_model=WorkspaceResult)
def get_workspace_endpoint(
    workspace_id: UUID,
    session: TenantContext = Depends(get_tenant_context),
    conn: psycopg.Connection[Any] = Depends(get_db_connection),
) -> WorkspaceResult:
    """Retrieve workspace details ensuring RLS session boundaries."""
    try:
        return get_workspace(workspace_id=workspace_id, session=session, conn=conn)
    except WorkspaceNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err)) from err
    except CrossWorkspaceLeakError as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err


@router.patch("/{workspace_id}", response_model=WorkspaceResult)
def update_workspace_endpoint(
    workspace_id: UUID,
    body: UpdateWorkspaceRequestBody,
    session: TenantContext = Depends(get_tenant_context),
    conn: psycopg.Connection[Any] = Depends(get_db_connection),
) -> WorkspaceResult:
    """Update workspace display name or status under ADMIN governance."""
    try:
        return update_workspace(
            UpdateWorkspaceInput(workspace_id=workspace_id, display_name=body.display_name, status=body.status),
            session=session,
            conn=conn,
        )
    except WorkspaceNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err)) from err
    except UnauthorizedAccessError as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err)) from err
    except CrossWorkspaceLeakError as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err


@router.post("/{workspace_id}/memberships", response_model=MembershipResult, status_code=status.HTTP_201_CREATED)
def add_membership_endpoint(
    workspace_id: UUID,
    body: AddMembershipRequestBody,
    session: TenantContext = Depends(get_tenant_context),
    conn: psycopg.Connection[Any] = Depends(get_db_connection),
) -> MembershipResult:
    """Add a member to a workspace under ADMIN role governance."""
    try:
        return add_workspace_membership(
            AddMembershipInput(workspace_id=workspace_id, actor_id=body.actor_id, role=body.role),
            session=session,
            conn=conn,
        )
    except MembershipExistsError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err)) from err
    except UnauthorizedAccessError as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err)) from err
    except CrossWorkspaceLeakError as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err


@router.delete("/{workspace_id}/memberships/{actor_id}", response_model=MembershipResult)
def remove_membership_endpoint(
    workspace_id: UUID,
    actor_id: str,
    session: TenantContext = Depends(get_tenant_context),
    conn: psycopg.Connection[Any] = Depends(get_db_connection),
) -> MembershipResult:
    """Revoke membership for an actor from a workspace."""
    try:
        return remove_workspace_membership(
            RemoveMembershipInput(workspace_id=workspace_id, actor_id=actor_id),
            session=session,
            conn=conn,
        )
    except MembershipNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err)) from err
    except UnauthorizedAccessError as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err)) from err
    except CrossWorkspaceLeakError as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err


@router.post("/{workspace_id}/operator-grants", response_model=OperatorGrantResult, status_code=status.HTTP_201_CREATED)
def issue_operator_grant_endpoint(
    workspace_id: UUID,
    body: IssueOperatorGrantRequestBody,
    session: TenantContext = Depends(get_tenant_context),
    conn: psycopg.Connection[Any] = Depends(get_db_connection),
) -> OperatorGrantResult:
    """Issue a bounded time-limited operator access grant."""
    try:
        return issue_operator_grant(
            IssueOperatorGrantInput(
                operator_org_id=body.operator_org_id,
                workspace_id=workspace_id,
                operator_actor_id=body.operator_actor_id,
                justification=body.justification,
                expires_at=body.expires_at,
            ),
            session=session,
            conn=conn,
        )
    except OperatorOrgNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err)) from err
    except OperatorGrantExistsError as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err)) from err
    except OperatorGrantExpiredError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err
    except UnauthorizedAccessError as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err)) from err
    except CrossWorkspaceLeakError as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err


@router.delete("/{workspace_id}/operator-grants/{grant_id}", response_model=OperatorGrantResult)
def revoke_operator_grant_endpoint(
    workspace_id: UUID,
    grant_id: UUID,
    session: TenantContext = Depends(get_tenant_context),
    conn: psycopg.Connection[Any] = Depends(get_db_connection),
) -> OperatorGrantResult:
    """Revoke an active operator access grant."""
    try:
        return revoke_operator_grant(
            RevokeOperatorGrantInput(grant_id=grant_id, workspace_id=workspace_id),
            session=session,
            conn=conn,
        )
    except OperatorGrantNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err)) from err
    except UnauthorizedAccessError as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err)) from err
    except CrossWorkspaceLeakError as err:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(err)) from err
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err
