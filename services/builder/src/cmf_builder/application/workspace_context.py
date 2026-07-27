"""Persistent governed workspace context for OD-AM-005 / ST-10.11."""

from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import json
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_of(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


class WorkspaceContextError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


@dataclass(frozen=True)
class WorkspaceContext:
    workspace_identity: str
    operator_identity: str
    active_run: str = "NONE"
    active_harness: str = "NONE"
    active_workflow: str = "NONE"
    active_story: str = "NONE"
    selected_graph: str = "NONE"
    selected_decision: str = "NONE"
    selected_evidence_subject: str = "NONE"
    filters: tuple[str, ...] = ()
    sorting: tuple[str, ...] = ()
    pagination_cursor: str = "START"
    logical_views: tuple[str, ...] = ()
    redaction_context: tuple[str, ...] = ()
    projection_revision: str = "rev:0"
    persistence_revision: int = 0
    invalidation_status: str = "ACTIVE"
    limitations: tuple[str, ...] = ("workspace_context_is_not_authority_evidence",)

    def __post_init__(self) -> None:
        if not self.workspace_identity or not self.operator_identity:
            raise WorkspaceContextError("WORKSPACE_IDENTITY_REQUIRED", "workspace and operator identity are required")
        if self.invalidation_status not in {"ACTIVE", "STALE", "INVALIDATED", "CONTAINED"}:
            raise WorkspaceContextError("INVALID_WORKSPACE_STATUS", "unsupported workspace invalidation status")
        if "UNREDACTED_SECRET" in self.redaction_context:
            raise WorkspaceContextError("REDACTION_CONTEXT_UNSAFE", "redaction context cannot persist unredacted secrets")

    @property
    def context_identity(self) -> str:
        return sha256_of(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "workspace_identity": self.workspace_identity,
            "operator_identity": self.operator_identity,
            "active_run": self.active_run,
            "active_harness": self.active_harness,
            "active_workflow": self.active_workflow,
            "active_story": self.active_story,
            "selected_graph": self.selected_graph,
            "selected_decision": self.selected_decision,
            "selected_evidence_subject": self.selected_evidence_subject,
            "filters": list(self.filters),
            "sorting": list(self.sorting),
            "pagination_cursor": self.pagination_cursor,
            "logical_views": list(self.logical_views),
            "redaction_context": list(self.redaction_context),
            "projection_revision": self.projection_revision,
            "persistence_revision": self.persistence_revision,
            "invalidation_status": self.invalidation_status,
            "limitations": list(self.limitations),
        }


class InMemoryWorkspaceContextRepository:
    def __init__(self) -> None:
        self._contexts: dict[tuple[str, str], WorkspaceContext] = {}

    def save(self, context: WorkspaceContext) -> WorkspaceContext:
        if context.invalidation_status == "INVALIDATED":
            raise WorkspaceContextError("INVALIDATED_CONTEXT_CANNOT_SAVE_ACTIVE", "invalidated context cannot be saved as active")
        key = (context.operator_identity, context.workspace_identity)
        current = self._contexts.get(key)
        next_context = replace(context, persistence_revision=(current.persistence_revision + 1 if current else context.persistence_revision + 1))
        self._contexts[key] = next_context
        return next_context

    def load(self, *, operator_identity: str, workspace_identity: str, known_references: set[str]) -> WorkspaceContext:
        context = self._contexts[(operator_identity, workspace_identity)]
        refs = {
            context.active_run,
            context.active_harness,
            context.active_workflow,
            context.active_story,
            context.selected_graph,
            context.selected_decision,
            context.selected_evidence_subject,
        } - {"NONE"}
        if not refs <= known_references:
            return replace(context, invalidation_status="STALE")
        return context

    def raw_snapshot(self) -> dict[str, dict[str, Any]]:
        return {f"{operator}/{workspace}": context.as_dict() for (operator, workspace), context in sorted(self._contexts.items())}


def apply_workspace_update(context: WorkspaceContext, **changes: Any) -> WorkspaceContext:
    if "operator_identity" in changes and changes["operator_identity"] != context.operator_identity:
        raise WorkspaceContextError("OPERATOR_CONTEXT_ISOLATION_VIOLATION", "workspace updates cannot change operator ownership")
    return replace(context, **changes)
