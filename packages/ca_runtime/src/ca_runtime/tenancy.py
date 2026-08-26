"""Tenant context management, JWT/session claim resolution, and PostgreSQL RLS session configuration.

Governed by TS-CAE-TEN-001, FR-CAE-TEN-001, FR-CAE-TEN-003, and HN-TS-001.
"""

from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any, Iterator, Optional
from uuid import UUID

import psycopg


class TenancyError(RuntimeError):
    """Base exception for tenancy violations."""
    pass


class TenancyViolationError(TenancyError):
    """Raised when tenant boundary is breached, scope is forged, or context is missing."""
    pass


class UnauthorizedOperatorAccessError(TenancyError):
    """Raised when operator access is attempted without a valid grant."""
    pass


class CrossWorkspaceLeakError(TenancyError):
    """Raised when an operation attempts to link or access entities across different workspaces."""
    pass


class UnverifiedMediaDigestError(TenancyError):
    """Raised when media bytes do not match the claimed cryptographic SHA-256 digest."""
    pass


class ReceiptSelfAttestationViolationError(TenancyError):
    """Raised when an execution receipt attempts to self-attest qualitative/taste/truth claims."""
    pass


class StaleVersionConflictError(TenancyError):
    """Raised when optimistic concurrency version locking detects a concurrent mutation."""
    pass


class IdempotencyPayloadMismatchError(TenancyError):
    """Raised when an idempotency key is reused with a different canonical payload."""
    pass


@dataclass(frozen=True, slots=True)
class TenantContext:
    workspace_id: UUID
    actor_id: str
    role: str = "MEMBER"
    is_operator: bool = False
    operator_grant_id: Optional[UUID] = None

    def __post_init__(self) -> None:
        if not isinstance(self.workspace_id, UUID):
            raise TenancyViolationError(f"workspace_id must be a UUID instance, got {type(self.workspace_id)}")
        if not self.actor_id or not self.actor_id.strip():
            raise TenancyViolationError("actor_id cannot be empty")
        if self.is_operator and self.operator_grant_id is None:
            raise UnauthorizedOperatorAccessError("operator context requires an operator_grant_id")


_CURRENT_TENANT_CONTEXT: ContextVar[Optional[TenantContext]] = ContextVar(
    "current_tenant_context", default=None
)


def get_current_tenant_context() -> Optional[TenantContext]:
    """Retrieve active tenant context in current execution thread/task."""
    return _CURRENT_TENANT_CONTEXT.get()


def require_current_tenant_context() -> TenantContext:
    """Retrieve active tenant context or raise TenancyViolationError if unauthenticated."""
    context = _CURRENT_TENANT_CONTEXT.get()
    if context is None:
        raise TenancyViolationError("No tenant context is bound to the current execution frame")
    return context


class tenant_scope:
    """Context manager for binding a TenantContext to the current execution frame."""

    def __init__(self, context: TenantContext) -> None:
        self.context = context
        self._token: Optional[Any] = None

    def __enter__(self) -> TenantContext:
        self._token = _CURRENT_TENANT_CONTEXT.set(self.context)
        return self.context

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._token is not None:
            _CURRENT_TENANT_CONTEXT.reset(self._token)


def extract_tenant_context_from_claims(
    claims: dict[str, Any],
    *,
    requested_workspace_id: Optional[str | UUID] = None,
) -> TenantContext:
    """Extract and validate tenant context from trusted cryptographic JWT/session claims.

    Enforces server-side scope derivation:
    - If the caller supplies a requested_workspace_id in query/body params, it is verified
      against the token-derived workspace_id. Any discrepancy raises TenancyViolationError.
    - An unauthenticated caller supplying only requested_workspace_id is strictly rejected.
    """
    if not claims:
        raise TenancyViolationError("Authentication claims missing or unverified")

    actor_id = str(claims.get("sub") or claims.get("actor_id") or "")
    if not actor_id:
        raise TenancyViolationError("Claim missing valid actor subject (sub/actor_id)")

    is_operator = bool(claims.get("is_operator", False))
    grant_id_raw = claims.get("operator_grant_id")
    operator_grant_id = UUID(str(grant_id_raw)) if grant_id_raw else None

    # Resolve workspace_id from claims
    ws_raw = claims.get("workspace_id") or claims.get("app_metadata", {}).get("workspace_id")
    if not ws_raw:
        if is_operator and requested_workspace_id:
            # Ephemeral operator granted access to specific target workspace
            ws_raw = str(requested_workspace_id)
        else:
            raise TenancyViolationError("Claim missing authorized workspace_id")

    try:
        token_workspace_id = UUID(str(ws_raw))
    except ValueError as err:
        raise TenancyViolationError(f"Invalid workspace_id in claims: {ws_raw}") from err

    # Adversarial Defense: HN-TS-001 (Scope Forgery)
    if requested_workspace_id is not None:
        try:
            req_ws = UUID(str(requested_workspace_id))
        except ValueError as err:
            raise TenancyViolationError(f"Invalid requested_workspace_id syntax: {requested_workspace_id}") from err

        if req_ws != token_workspace_id and not is_operator:
            raise TenancyViolationError(
                f"TENANCY_VIOLATION: Requested workspace {req_ws} does not match token scope {token_workspace_id}"
            )

    role = str(claims.get("role", "MEMBER"))

    return TenantContext(
        workspace_id=token_workspace_id,
        actor_id=actor_id,
        role=role,
        is_operator=is_operator,
        operator_grant_id=operator_grant_id,
    )


def apply_tenant_session(
    cursor: psycopg.Cursor[object],
    context: TenantContext,
    is_local: bool = False,
) -> None:
    """Configure PostgreSQL session configuration variables for Row-Level Security (RLS)."""
    is_system_op = context.is_operator and context.role in ("SYSTEM_ADMIN", "SYSTEM_OPERATOR")
    if is_system_op:
        cursor.execute("RESET ROLE;")
    else:
        cursor.execute("SET ROLE authenticated;")

    cursor.execute("SELECT set_config('app.current_workspace_id', %s, %s)", (str(context.workspace_id), is_local))
    cursor.execute("SELECT set_config('app.current_actor_id', %s, %s)", (context.actor_id, is_local))
    cursor.execute("SELECT set_config('app.is_operator', %s, %s)", ("true" if context.is_operator else "false", is_local))
    cursor.execute("SELECT set_config('app.is_system_operator', %s, %s)", ("true" if is_system_op else "false", is_local))
    if context.operator_grant_id is not None:
        cursor.execute(
            "SELECT set_config('app.current_operator_grant_id', %s, %s)",
            (str(context.operator_grant_id), is_local),
        )
    else:
        cursor.execute("SELECT set_config('app.current_operator_grant_id', '', %s)", (is_local,))





