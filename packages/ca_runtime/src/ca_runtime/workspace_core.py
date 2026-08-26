"""Typed PostgreSQL semantic operations for Workspace, Membership, and Operator Grant lifecycle.

Governed by TS-CAE-TEN-001, FR-CAE-TEN-001 through FR-CAE-TEN-005, and CA-TWC-01 Mandate.
Provides strongly-typed operations with Row-Level Security session enforcement,
append-only receipt ledger emission, and strict epistemic boundary tracking.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from typing import Any, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
import psycopg

from ca_contracts import canonical_json_text, canonical_sha256
from ca_runtime.tenancy import (
    CrossWorkspaceLeakError,
    StaleVersionConflictError,
    TenantContext,
    TenancyError,
    TenancyViolationError,
    UnauthorizedOperatorAccessError,
    apply_tenant_session,
    require_current_tenant_context,
)


# --- Typed Error Taxonomy (TS-CAE-TEN-001 §9) ---

class WorkspaceError(TenancyError):
    """Base error for workspace operations."""
    pass


class WorkspaceNotFoundError(WorkspaceError):
    """Raised when workspace is not found or inaccessible under RLS (TENANT_NOT_FOUND)."""
    pass


class WorkspaceConflictError(WorkspaceError):
    """Raised when workspace slug or identity conflicts (SLUG_EXISTS)."""
    pass


class MembershipError(WorkspaceError):
    """Base error for membership operations."""
    pass


class MembershipNotFoundError(MembershipError):
    """Raised when membership record does not exist (MEMBERSHIP_NOT_FOUND)."""
    pass


class MembershipExistsError(MembershipError):
    """Raised when membership already exists for actor in workspace (MEMBERSHIP_EXISTS)."""
    pass


class OperatorGrantError(WorkspaceError):
    """Base error for operator grant operations."""
    pass


class OperatorGrantNotFoundError(OperatorGrantError):
    """Raised when operator grant does not exist or is inaccessible (GRANT_NOT_FOUND)."""
    pass


class OperatorGrantExistsError(OperatorGrantError):
    """Raised when active operator grant already exists (GRANT_EXISTS)."""
    pass


class OperatorGrantExpiredError(OperatorGrantError):
    """Raised when attempting to issue or use an expired grant (GRANT_EXPIRED)."""
    pass


class OperatorOrgNotFoundError(OperatorGrantError):
    """Raised when referenced operator organization does not exist (OPERATOR_ORG_NOT_FOUND)."""
    pass


class UnauthorizedAccessError(WorkspaceError):
    """Raised when actor lacks required permissions (UNAUTHORIZED_CROSS_TENANT_ACCESS)."""
    pass


# --- Pydantic V2 Models ---

class CreateWorkspaceInput(BaseModel):
    slug: str = Field(..., min_length=2, max_length=64, pattern=r"^[a-z0-9-]+$")
    display_name: str = Field(..., min_length=1, max_length=255)


class UpdateWorkspaceInput(BaseModel):
    workspace_id: UUID
    display_name: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[str] = Field(None, pattern=r"^(ACTIVE|SUSPENDED|ARCHIVED)$")


class WorkspaceResult(BaseModel):
    workspace_id: UUID
    slug: str
    display_name: str
    status: str
    created_at: datetime
    updated_at: datetime
    receipt_id: UUID


class AddMembershipInput(BaseModel):
    workspace_id: UUID
    actor_id: str = Field(..., min_length=1, max_length=128)
    role: str = Field("MEMBER", pattern=r"^(ADMIN|MEMBER|VIEWER)$")


class RemoveMembershipInput(BaseModel):
    workspace_id: UUID
    actor_id: str = Field(..., min_length=1, max_length=128)


class MembershipResult(BaseModel):
    membership_id: UUID
    workspace_id: UUID
    actor_id: str
    role: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    receipt_id: UUID


class IssueOperatorGrantInput(BaseModel):
    operator_org_id: UUID
    workspace_id: UUID
    operator_actor_id: str = Field(..., min_length=1, max_length=128)
    justification: str = Field(..., min_length=1)
    expires_at: datetime


class RevokeOperatorGrantInput(BaseModel):
    grant_id: UUID
    workspace_id: UUID


class OperatorGrantResult(BaseModel):
    grant_id: UUID
    operator_org_id: UUID
    workspace_id: UUID
    operator_actor_id: str
    justification: str
    expires_at: datetime
    revoked_at: Optional[datetime] = None
    created_at: datetime
    receipt_id: UUID


class ReceiptRecord(BaseModel):
    receipt_id: UUID
    workspace_id: UUID
    action_type: str
    actor_id: str
    result_status: str
    payload_hash: str
    created_at: datetime
    reward_hack_result: str = "UNVERIFIED"
    taste_integrity_result: str = "NOT_APPLICABLE"


# --- Helper to emit immutable receipt ---

def _emit_receipt(
    cur: psycopg.Cursor[Any],
    *,
    workspace_id: UUID,
    action_type: str,
    actor_id: str,
    payload_dict: dict[str, Any],
) -> UUID:
    receipt_id = uuid4()
    payload_hash = canonical_sha256(payload_dict)
    cur.execute(
        """
        INSERT INTO cae.receipt (
            receipt_id, workspace_id, action_type, actor_id, result_status, payload_hash, created_at
        ) VALUES (%s, %s, %s, %s, 'SUCCESS', %s, clock_timestamp())
        RETURNING receipt_id;
        """,
        (receipt_id, workspace_id, action_type, actor_id, payload_hash),
    )
    return cur.fetchone()[0]


# --- Core Typed Operations ---

def create_workspace(
    input_data: CreateWorkspaceInput,
    session: TenantContext,
    conn: psycopg.Connection[Any],
) -> WorkspaceResult:
    """Create a new workspace, bind initial admin membership, and emit immutable receipt."""
    new_ws_id = uuid4()
    with conn.transaction():
        with conn.cursor() as cur:
            # Workspace creation requires operator or administrative authority
            if session.is_operator:
                cur.execute("SET LOCAL app.is_system_operator = 'true';")
            else:
                apply_tenant_session(cur, session)

            # Check if slug exists
            cur.execute("SELECT 1 FROM cae.workspace WHERE slug = %s;", (input_data.slug,))
            if cur.fetchone():
                raise WorkspaceConflictError(f"Workspace slug '{input_data.slug}' already exists")

            cur.execute(
                """
                INSERT INTO cae.workspace (workspace_id, slug, display_name, status, created_at, updated_at)
                VALUES (%s, %s, %s, 'ACTIVE', clock_timestamp(), clock_timestamp())
                RETURNING workspace_id, slug, display_name, status, created_at, updated_at;
                """,
                (new_ws_id, input_data.slug, input_data.display_name),
            )
            row = cur.fetchone()

            # Insert creator as initial ADMIN member
            cur.execute(
                """
                INSERT INTO cae.workspace_membership (
                    membership_id, workspace_id, actor_id, role, status, created_at
                ) VALUES (gen_random_uuid(), %s, %s, 'ADMIN', 'ACTIVE', clock_timestamp());
                """,
                (new_ws_id, session.actor_id),
            )

            # Emit receipt
            receipt_id = _emit_receipt(
                cur,
                workspace_id=new_ws_id,
                action_type="WORKSPACE_CREATED",
                actor_id=session.actor_id,
                payload_dict={
                    "workspace_id": str(new_ws_id),
                    "slug": input_data.slug,
                    "display_name": input_data.display_name,
                    "creator_actor_id": session.actor_id,
                },
            )

            return WorkspaceResult(
                workspace_id=row[0],
                slug=row[1],
                display_name=row[2],
                status=row[3],
                created_at=row[4],
                updated_at=row[5],
                receipt_id=receipt_id,
            )


def get_workspace(
    workspace_id: UUID,
    session: TenantContext,
    conn: psycopg.Connection[Any],
) -> WorkspaceResult:
    """Retrieve workspace details ensuring RLS session boundaries."""
    if session.workspace_id != workspace_id and not session.is_operator:
        raise WorkspaceNotFoundError(f"Workspace {workspace_id} not found or inaccessible")

    with conn.cursor() as cur:
        apply_tenant_session(cur, session)
        cur.execute(
            """
            SELECT workspace_id, slug, display_name, status, created_at, updated_at
            FROM cae.workspace
            WHERE workspace_id = %s;
            """,
            (workspace_id,),
        )
        row = cur.fetchone()
        if not row:
            raise WorkspaceNotFoundError(f"Workspace {workspace_id} not found or inaccessible")


        # Fetch latest receipt for workspace or generate stable receipt marker
        cur.execute(
            """
            SELECT receipt_id FROM cae.receipt
            WHERE workspace_id = %s
            ORDER BY created_at DESC LIMIT 1;
            """,
            (workspace_id,),
        )
        rcpt = cur.fetchone()
        receipt_id = rcpt[0] if rcpt else uuid4()

        return WorkspaceResult(
            workspace_id=row[0],
            slug=row[1],
            display_name=row[2],
            status=row[3],
            created_at=row[4],
            updated_at=row[5],
            receipt_id=receipt_id,
        )


def update_workspace(
    input_data: UpdateWorkspaceInput,
    session: TenantContext,
    conn: psycopg.Connection[Any],
) -> WorkspaceResult:
    """Update workspace attributes with admin role enforcement and receipt emission."""
    if session.workspace_id != input_data.workspace_id and not session.is_operator:
        raise CrossWorkspaceLeakError(f"Cross-workspace mutation denied: {session.workspace_id} != {input_data.workspace_id}")

    if session.role != "ADMIN" and not session.is_operator:
        raise UnauthorizedAccessError("Only workspace ADMIN or system operator can update workspace settings")

    with conn.transaction():
        with conn.cursor() as cur:
            apply_tenant_session(cur, session)

            cur.execute(
                """
                SELECT workspace_id, slug, display_name, status, created_at
                FROM cae.workspace
                WHERE workspace_id = %s FOR UPDATE;
                """,
                (input_data.workspace_id,),
            )
            current = cur.fetchone()
            if not current:
                raise WorkspaceNotFoundError(f"Workspace {input_data.workspace_id} not found")

            new_display = input_data.display_name if input_data.display_name is not None else current[2]
            new_status = input_data.status if input_data.status is not None else current[3]

            cur.execute(
                """
                UPDATE cae.workspace
                SET display_name = %s, status = %s, updated_at = clock_timestamp()
                WHERE workspace_id = %s
                RETURNING workspace_id, slug, display_name, status, created_at, updated_at;
                """,
                (new_display, new_status, input_data.workspace_id),
            )
            updated = cur.fetchone()

            receipt_id = _emit_receipt(
                cur,
                workspace_id=input_data.workspace_id,
                action_type="WORKSPACE_UPDATED",
                actor_id=session.actor_id,
                payload_dict={
                    "workspace_id": str(input_data.workspace_id),
                    "previous_display_name": current[2],
                    "new_display_name": new_display,
                    "previous_status": current[3],
                    "new_status": new_status,
                },
            )

            return WorkspaceResult(
                workspace_id=updated[0],
                slug=updated[1],
                display_name=updated[2],
                status=updated[3],
                created_at=updated[4],
                updated_at=updated[5],
                receipt_id=receipt_id,
            )


def add_workspace_membership(
    input_data: AddMembershipInput,
    session: TenantContext,
    conn: psycopg.Connection[Any],
) -> MembershipResult:
    """Add a user to a workspace under admin governance with immutable receipt."""
    if session.workspace_id != input_data.workspace_id and not session.is_operator:
        raise CrossWorkspaceLeakError("Cannot add membership to foreign workspace")

    if session.role != "ADMIN" and not session.is_operator:
        raise UnauthorizedAccessError("ADMIN role required to add workspace members")

    new_mem_id = uuid4()
    with conn.transaction():
        with conn.cursor() as cur:
            apply_tenant_session(cur, session)

            cur.execute(
                """
                SELECT membership_id, status FROM cae.workspace_membership
                WHERE workspace_id = %s AND actor_id = %s;
                """,
                (input_data.workspace_id, input_data.actor_id),
            )
            existing = cur.fetchone()
            if existing:
                if existing[1] == "ACTIVE":
                    raise MembershipExistsError(f"Actor '{input_data.actor_id}' is already an ACTIVE member")
                # Reactivate
                cur.execute(
                    """
                    UPDATE cae.workspace_membership
                    SET role = %s, status = 'ACTIVE'
                    WHERE membership_id = %s
                    RETURNING membership_id, workspace_id, actor_id, role, status, created_at;
                    """,
                    (input_data.role, existing[0]),
                )
                row = cur.fetchone()
            else:
                cur.execute(
                    """
                    INSERT INTO cae.workspace_membership (
                        membership_id, workspace_id, actor_id, role, status, created_at
                    ) VALUES (%s, %s, %s, %s, 'ACTIVE', clock_timestamp())
                    RETURNING membership_id, workspace_id, actor_id, role, status, created_at;
                    """,
                    (new_mem_id, input_data.workspace_id, input_data.actor_id, input_data.role),
                )
                row = cur.fetchone()

            receipt_id = _emit_receipt(
                cur,
                workspace_id=input_data.workspace_id,
                action_type="MEMBERSHIP_ADDED",
                actor_id=session.actor_id,
                payload_dict={
                    "membership_id": str(row[0]),
                    "workspace_id": str(input_data.workspace_id),
                    "target_actor_id": input_data.actor_id,
                    "role": input_data.role,
                },
            )

            return MembershipResult(
                membership_id=row[0],
                workspace_id=row[1],
                actor_id=row[2],
                role=row[3],
                status=row[4],
                created_at=row[5],
                receipt_id=receipt_id,
            )


def remove_workspace_membership(
    input_data: RemoveMembershipInput,
    session: TenantContext,
    conn: psycopg.Connection[Any],
) -> MembershipResult:
    """Revoke membership for an actor from workspace with immutable receipt."""
    if session.workspace_id != input_data.workspace_id and not session.is_operator:
        raise CrossWorkspaceLeakError("Cannot remove membership from foreign workspace")

    if session.role != "ADMIN" and not session.is_operator:
        raise UnauthorizedAccessError("ADMIN role required to remove workspace members")

    with conn.transaction():
        with conn.cursor() as cur:
            apply_tenant_session(cur, session)

            cur.execute(
                """
                UPDATE cae.workspace_membership
                SET status = 'REVOKED'
                WHERE workspace_id = %s AND actor_id = %s AND status = 'ACTIVE'
                RETURNING membership_id, workspace_id, actor_id, role, status, created_at;
                """,
                (input_data.workspace_id, input_data.actor_id),
            )
            row = cur.fetchone()
            if not row:
                raise MembershipNotFoundError(f"Active membership for '{input_data.actor_id}' not found in workspace")

            receipt_id = _emit_receipt(
                cur,
                workspace_id=input_data.workspace_id,
                action_type="MEMBERSHIP_REMOVED",
                actor_id=session.actor_id,
                payload_dict={
                    "membership_id": str(row[0]),
                    "workspace_id": str(input_data.workspace_id),
                    "target_actor_id": input_data.actor_id,
                    "status": "REVOKED",
                },
            )

            return MembershipResult(
                membership_id=row[0],
                workspace_id=row[1],
                actor_id=row[2],
                role=row[3],
                status=row[4],
                created_at=row[5],
                receipt_id=receipt_id,
            )


def issue_operator_grant(
    input_data: IssueOperatorGrantInput,
    session: TenantContext,
    conn: psycopg.Connection[Any],
) -> OperatorGrantResult:
    """Issue a bounded time-limited operator access grant to a designated operator organization."""
    if session.workspace_id != input_data.workspace_id and not session.is_operator:
        raise CrossWorkspaceLeakError("Cannot issue grant for foreign workspace")

    if session.role != "ADMIN" and not session.is_operator:
        raise UnauthorizedAccessError("ADMIN role required to issue operator grants")

    now = datetime.now(timezone.utc)
    if input_data.expires_at <= now:
        raise OperatorGrantExpiredError("Grant expiration time must be in the future")

    new_grant_id = uuid4()
    with conn.transaction():
        with conn.cursor() as cur:
            apply_tenant_session(cur, session)

            # Check if operator org exists
            cur.execute(
                "SELECT 1 FROM cae.operator_organization WHERE operator_org_id = %s;",
                (input_data.operator_org_id,),
            )
            if not cur.fetchone():
                raise OperatorOrgNotFoundError(f"Operator organization {input_data.operator_org_id} does not exist")

            # Check existing grant
            cur.execute(
                """
                SELECT grant_id, revoked_at, expires_at FROM cae.operator_access_grant
                WHERE operator_org_id = %s AND workspace_id = %s AND operator_actor_id = %s;
                """,
                (input_data.operator_org_id, input_data.workspace_id, input_data.operator_actor_id),
            )
            existing = cur.fetchone()
            if existing and existing[1] is None and existing[2] > now:
                raise OperatorGrantExistsError("Active operator grant already exists for this operator actor and workspace")

            cur.execute(
                """
                INSERT INTO cae.operator_access_grant (
                    grant_id, operator_org_id, operator_actor_id, workspace_id, justification, expires_at, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, clock_timestamp())
                RETURNING grant_id, operator_org_id, workspace_id, operator_actor_id, justification, expires_at, revoked_at, created_at;
                """,
                (new_grant_id, input_data.operator_org_id, input_data.operator_actor_id, input_data.workspace_id, input_data.justification, input_data.expires_at),
            )
            row = cur.fetchone()

            receipt_id = _emit_receipt(
                cur,
                workspace_id=input_data.workspace_id,
                action_type="OPERATOR_GRANT_ISSUED",
                actor_id=session.actor_id,
                payload_dict={
                    "grant_id": str(row[0]),
                    "operator_org_id": str(input_data.operator_org_id),
                    "workspace_id": str(input_data.workspace_id),
                    "operator_actor_id": input_data.operator_actor_id,
                    "justification": input_data.justification,
                    "expires_at": input_data.expires_at.isoformat(),
                },
            )

            return OperatorGrantResult(
                grant_id=row[0],
                operator_org_id=row[1],
                workspace_id=row[2],
                operator_actor_id=row[3],
                justification=row[4],
                expires_at=row[5],
                revoked_at=row[6],
                created_at=row[7],
                receipt_id=receipt_id,
            )


def revoke_operator_grant(
    input_data: RevokeOperatorGrantInput,
    session: TenantContext,
    conn: psycopg.Connection[Any],
) -> OperatorGrantResult:
    """Revoke an active operator access grant."""
    if session.workspace_id != input_data.workspace_id and not session.is_operator:
        raise CrossWorkspaceLeakError("Cannot revoke grant for foreign workspace")

    if session.role != "ADMIN" and not session.is_operator:
        raise UnauthorizedAccessError("ADMIN role required to revoke operator grants")

    with conn.transaction():
        with conn.cursor() as cur:
            apply_tenant_session(cur, session)

            cur.execute(
                """
                UPDATE cae.operator_access_grant
                SET revoked_at = clock_timestamp()
                WHERE grant_id = %s AND workspace_id = %s AND revoked_at IS NULL
                RETURNING grant_id, operator_org_id, workspace_id, operator_actor_id, justification, expires_at, revoked_at, created_at;
                """,
                (input_data.grant_id, input_data.workspace_id),
            )
            row = cur.fetchone()
            if not row:
                raise OperatorGrantNotFoundError(f"Active operator grant {input_data.grant_id} not found in workspace")

            receipt_id = _emit_receipt(
                cur,
                workspace_id=input_data.workspace_id,
                action_type="OPERATOR_GRANT_REVOKED",
                actor_id=session.actor_id,
                payload_dict={
                    "grant_id": str(row[0]),
                    "workspace_id": str(input_data.workspace_id),
                    "revoked_at": row[6].isoformat(),
                },
            )

            return OperatorGrantResult(
                grant_id=row[0],
                operator_org_id=row[1],
                workspace_id=row[2],
                operator_actor_id=row[3],
                justification=row[4],
                expires_at=row[5],
                revoked_at=row[6],
                created_at=row[7],
                receipt_id=receipt_id,
            )
