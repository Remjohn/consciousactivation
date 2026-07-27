"""Workspace lifecycle policy for TS-CMF-004."""

from __future__ import annotations

from ccp_studio.contracts.workspace_lifecycle import WorkspaceStatus


OWNER_ADMIN_ROLES = {"owner", "admin"}
READ_ONLY_ROLES = {"owner", "admin", "operator", "auditor"}

ALLOWED_TRANSITIONS = {
    WorkspaceStatus.active: {WorkspaceStatus.suspended, WorkspaceStatus.archived},
    WorkspaceStatus.suspended: {WorkspaceStatus.active, WorkspaceStatus.archived},
    WorkspaceStatus.archived: {WorkspaceStatus.restoring},
    WorkspaceStatus.restoring: {WorkspaceStatus.active, WorkspaceStatus.archived},
}


class WorkspacePolicyError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class WorkspaceLifecyclePolicy:
    def require_owner_or_admin(self, role_ids: list[str]) -> None:
        if not set(role_ids).intersection(OWNER_ADMIN_ROLES):
            raise WorkspacePolicyError(
                "PERMISSION_DENIED",
                "Owner or Admin role is required for workspace lifecycle mutation.",
            )

    def require_read_access(self, role_ids: list[str]) -> None:
        if not set(role_ids).intersection(READ_ONLY_ROLES):
            raise WorkspacePolicyError(
                "NOT_FOUND",
                "Workspace is not visible to this actor.",
            )

    def validate_transition(self, current: WorkspaceStatus, target: WorkspaceStatus) -> None:
        if target not in ALLOWED_TRANSITIONS.get(current, set()):
            raise WorkspacePolicyError(
                "WORKSPACE_TRANSITION_FORBIDDEN",
                f"Cannot transition workspace from {current.value} to {target.value}.",
            )

    def require_mutation_allowed(self, status: WorkspaceStatus) -> None:
        if status == WorkspaceStatus.suspended:
            raise WorkspacePolicyError("WORKSPACE_SUSPENDED", "Suspended workspace blocks mutation.")
        if status == WorkspaceStatus.archived:
            raise WorkspacePolicyError("WORKSPACE_ARCHIVED", "Archived workspace blocks mutation.")
        if status == WorkspaceStatus.restoring:
            raise WorkspacePolicyError("WORKSPACE_RESTORING", "Restoring workspace blocks mutation.")
