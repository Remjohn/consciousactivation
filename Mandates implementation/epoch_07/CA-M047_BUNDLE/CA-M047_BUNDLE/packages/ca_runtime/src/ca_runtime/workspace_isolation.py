"""CA-M047 / INV-ISO-001 workspace and campaign isolation primitives.

The module provides the smallest reusable security boundary for workspace-scoped
execution state:

* authenticated workspace authority is fail-closed and cannot be substituted by
  a caller-supplied workspace identifier;
* SQLite state is keyed and queried by the complete
  ``(workspace_id, campaign_id, aggregate_id)`` scope;
* filesystem roots are partitioned by workspace and campaign and path traversal,
  symlink aliases, and workspace/campaign substitution are rejected;
* canonical receipt/state digests are domain-separated by workspace and campaign,
  so otherwise identical content cannot share an identity across scopes.

This module deliberately does not infer authorization from aggregate IDs,
campaign names, path prefixes, or UI/client filters.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

INVARIANT_ID = "INV-ISO-001"
HASH_DOMAIN = "cae.workspace-isolation.v1"
SCHEMA_VERSION = 1
_IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:@+-]{0,127}$")


class WorkspaceIsolationError(RuntimeError):
    """Base exception for INV-ISO-001 violations."""


class WorkspaceAuthorizationError(WorkspaceIsolationError):
    """Raised when authenticated workspace authority is missing or mismatched."""


class WorkspaceScopeError(WorkspaceIsolationError):
    """Raised when a workspace/campaign/aggregate identifier is unsafe."""


class WorkspaceDatabaseIsolationError(WorkspaceIsolationError):
    """Raised when a database operation is outside an exact tenant/campaign scope."""


class WorkspaceStateNotFoundError(WorkspaceDatabaseIsolationError):
    """Raised when scoped state does not exist.

    The error intentionally does not expose whether an aggregate exists in a
    different workspace.
    """


class WorkspaceVersionConflictError(WorkspaceDatabaseIsolationError):
    """Raised when a scoped state CAS update observes a different version."""


class WorkspacePathIsolationError(WorkspaceIsolationError):
    """Raised when a filesystem path escapes its scoped root or crosses aliases."""


class WorkspaceDigestMismatchError(WorkspaceIsolationError):
    """Raised when a workspace-bound digest fails verification."""


def _normalize_identifier(value: str, *, field: str) -> str:
    if not isinstance(value, str):
        raise WorkspaceScopeError(f"{field} must be a string")
    if not value or value in {".", ".."} or "\x00" in value:
        raise WorkspaceScopeError(f"Invalid {field}")
    if "/" in value or "\\" in value:
        raise WorkspaceScopeError(f"{field} must not contain path separators")
    if not _IDENTIFIER_RE.fullmatch(value):
        raise WorkspaceScopeError(f"Invalid {field} syntax")
    return value


def canonical_scope(
    workspace_id: str,
    campaign_id: str,
    aggregate_id: str,
) -> tuple[str, str, str]:
    """Validate and canonicalize the three identifiers forming the isolation key."""
    return (
        _normalize_identifier(workspace_id, field="workspace_id"),
        _normalize_identifier(campaign_id, field="campaign_id"),
        _normalize_identifier(aggregate_id, field="aggregate_id"),
    )


@dataclass(frozen=True, slots=True)
class WorkspaceAuthority:
    """Authenticated authority used to bind all subsequent operations to one workspace."""

    workspace_id: str
    actor_id: str
    campaign_id: str

    def __post_init__(self) -> None:
        workspace = _normalize_identifier(self.workspace_id, field="workspace_id")
        actor = _normalize_identifier(self.actor_id, field="actor_id")
        campaign = _normalize_identifier(self.campaign_id, field="campaign_id")
        object.__setattr__(self, "workspace_id", workspace)
        object.__setattr__(self, "actor_id", actor)
        object.__setattr__(self, "campaign_id", campaign)

    def require_workspace(self, requested_workspace_id: Optional[str]) -> str:
        """Fail closed when a request omits or substitutes the authenticated workspace."""
        if requested_workspace_id is None or requested_workspace_id == "":
            raise WorkspaceAuthorizationError(
                "Workspace identity is required; no default workspace is permitted"
            )
        requested = _normalize_identifier(
            requested_workspace_id, field="requested_workspace_id"
        )
        if requested != self.workspace_id:
            raise WorkspaceAuthorizationError(
                "Requested workspace does not match authenticated workspace authority"
            )
        return self.workspace_id

    def require_campaign(self, requested_campaign_id: Optional[str]) -> str:
        """Bind a campaign to the authenticated workspace authority."""
        if requested_campaign_id is None or requested_campaign_id == "":
            raise WorkspaceAuthorizationError(
                "Campaign identity is required for scoped execution state"
            )
        requested = _normalize_identifier(
            requested_campaign_id, field="requested_campaign_id"
        )
        if requested != self.campaign_id:
            raise WorkspaceAuthorizationError(
                "Requested campaign does not match the authenticated execution scope"
            )
        return self.campaign_id

    def scope(self, aggregate_id: str) -> tuple[str, str, str]:
        """Return the only database/filesystem scope this authority may access."""
        return canonical_scope(self.workspace_id, self.campaign_id, aggregate_id)


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def workspace_bound_payload(
    *,
    workspace_id: str,
    campaign_id: str,
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    """Create the canonical cryptographic envelope for scoped identity."""
    workspace, campaign, _ = canonical_scope(workspace_id, campaign_id, "aggregate")
    return {
        "hash_domain": HASH_DOMAIN,
        "workspace_id": workspace,
        "campaign_id": campaign,
        "payload": dict(payload),
    }


def workspace_bound_sha256(
    *,
    workspace_id: str,
    campaign_id: str,
    payload: Mapping[str, Any],
) -> str:
    """Hash canonical content while cryptographically binding workspace/campaign identity."""
    envelope = workspace_bound_payload(
        workspace_id=workspace_id,
        campaign_id=campaign_id,
        payload=payload,
    )
    return hashlib.sha256(_canonical_json(envelope).encode("utf-8")).hexdigest()


def verify_workspace_bound_sha256(
    *,
    workspace_id: str,
    campaign_id: str,
    payload: Mapping[str, Any],
    expected_sha256: str,
) -> None:
    actual = workspace_bound_sha256(
        workspace_id=workspace_id,
        campaign_id=campaign_id,
        payload=payload,
    )
    if actual != expected_sha256:
        raise WorkspaceDigestMismatchError("Workspace-bound digest verification failed")


@dataclass(frozen=True, slots=True)
class ScopedState:
    """Portable state record returned only within one exact scope."""

    workspace_id: str
    campaign_id: str
    aggregate_id: str
    version: int
    state: dict[str, Any]
    state_sha256: str


class WorkspaceIsolatedDatabase:
    """SQLite state repository whose authoritative key is workspace+campaign+aggregate."""

    TABLE_NAME = "cae_workspace_scoped_state"

    def __init__(self, db_path: str | os.PathLike[str]) -> None:
        self.db_path = str(db_path)
        self._initialize()

    def _connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _initialize(self) -> None:
        with self._connection() as conn:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                    workspace_id TEXT NOT NULL,
                    campaign_id TEXT NOT NULL,
                    aggregate_id TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    state_json TEXT NOT NULL,
                    state_sha256 TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, campaign_id, aggregate_id)
                )
                """
            )
            conn.execute(
                f"""
                CREATE INDEX IF NOT EXISTS idx_{self.TABLE_NAME}_workspace_campaign
                ON {self.TABLE_NAME}(workspace_id, campaign_id)
                """
            )
            conn.commit()

    def save(
        self,
        *,
        workspace_id: str,
        campaign_id: str,
        aggregate_id: str,
        state: Mapping[str, Any],
        version: int = 0,
    ) -> ScopedState:
        workspace, campaign, aggregate = canonical_scope(
            workspace_id, campaign_id, aggregate_id
        )
        if version < 0:
            raise WorkspaceDatabaseIsolationError("version must be non-negative")
        state_dict = dict(state)
        digest = workspace_bound_sha256(
            workspace_id=workspace,
            campaign_id=campaign,
            payload={
                "aggregate_id": aggregate,
                "version": version,
                "state": state_dict,
            },
        )
        with self._connection() as conn:
            conn.execute(
                f"""
                INSERT INTO {self.TABLE_NAME}
                    (workspace_id, campaign_id, aggregate_id, version, state_json, state_sha256)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(workspace_id, campaign_id, aggregate_id) DO UPDATE SET
                    version=excluded.version,
                    state_json=excluded.state_json,
                    state_sha256=excluded.state_sha256
                """,
                (
                    workspace,
                    campaign,
                    aggregate,
                    version,
                    _canonical_json(state_dict),
                    digest,
                ),
            )
            conn.commit()
        return ScopedState(workspace, campaign, aggregate, version, state_dict, digest)

    def get(
        self,
        *,
        workspace_id: str,
        campaign_id: str,
        aggregate_id: str,
    ) -> ScopedState:
        workspace, campaign, aggregate = canonical_scope(
            workspace_id, campaign_id, aggregate_id
        )
        with self._connection() as conn:
            row = conn.execute(
                f"""
                SELECT workspace_id, campaign_id, aggregate_id, version, state_json, state_sha256
                FROM {self.TABLE_NAME}
                WHERE workspace_id = ? AND campaign_id = ? AND aggregate_id = ?
                """,
                (workspace, campaign, aggregate),
            ).fetchone()
        if row is None:
            raise WorkspaceStateNotFoundError("Scoped state was not found")
        state = json.loads(row["state_json"])
        verify_workspace_bound_sha256(
            workspace_id=workspace,
            campaign_id=campaign,
            payload={
                "aggregate_id": aggregate,
                "version": int(row["version"]),
                "state": state,
            },
            expected_sha256=row["state_sha256"],
        )
        return ScopedState(
            workspace_id=row["workspace_id"],
            campaign_id=row["campaign_id"],
            aggregate_id=row["aggregate_id"],
            version=int(row["version"]),
            state=state,
            state_sha256=row["state_sha256"],
        )

    def compare_and_swap(
        self,
        *,
        workspace_id: str,
        campaign_id: str,
        aggregate_id: str,
        expected_version: int,
        state: Mapping[str, Any],
    ) -> ScopedState:
        workspace, campaign, aggregate = canonical_scope(
            workspace_id, campaign_id, aggregate_id
        )
        if expected_version < 0:
            raise WorkspaceDatabaseIsolationError("expected_version must be non-negative")
        next_version = expected_version + 1
        state_dict = dict(state)
        digest = workspace_bound_sha256(
            workspace_id=workspace,
            campaign_id=campaign,
            payload={
                "aggregate_id": aggregate,
                "version": next_version,
                "state": state_dict,
            },
        )
        with self._connection() as conn:
            cursor = conn.execute(
                f"""
                UPDATE {self.TABLE_NAME}
                SET version = ?, state_json = ?, state_sha256 = ?
                WHERE workspace_id = ? AND campaign_id = ? AND aggregate_id = ? AND version = ?
                """,
                (
                    next_version,
                    _canonical_json(state_dict),
                    digest,
                    workspace,
                    campaign,
                    aggregate,
                    expected_version,
                ),
            )
            if cursor.rowcount != 1:
                exists = conn.execute(
                    f"""
                    SELECT 1 FROM {self.TABLE_NAME}
                    WHERE workspace_id = ? AND campaign_id = ? AND aggregate_id = ?
                    """,
                    (workspace, campaign, aggregate),
                ).fetchone()
                if exists is None:
                    # Do not reveal whether the same aggregate exists elsewhere.
                    raise WorkspaceStateNotFoundError("Scoped state was not found")
                raise WorkspaceVersionConflictError("Scoped state version conflict")
            conn.commit()
        return self.get(
            workspace_id=workspace,
            campaign_id=campaign,
            aggregate_id=aggregate,
        )

    def delete(
        self,
        *,
        workspace_id: str,
        campaign_id: str,
        aggregate_id: str,
    ) -> None:
        workspace, campaign, aggregate = canonical_scope(
            workspace_id, campaign_id, aggregate_id
        )
        with self._connection() as conn:
            cursor = conn.execute(
                f"""
                DELETE FROM {self.TABLE_NAME}
                WHERE workspace_id = ? AND campaign_id = ? AND aggregate_id = ?
                """,
                (workspace, campaign, aggregate),
            )
            if cursor.rowcount != 1:
                raise WorkspaceStateNotFoundError("Scoped state was not found")
            conn.commit()

    def list_workspace(
        self,
        *,
        workspace_id: str,
        campaign_id: str,
    ) -> list[ScopedState]:
        workspace = _normalize_identifier(workspace_id, field="workspace_id")
        campaign = _normalize_identifier(campaign_id, field="campaign_id")
        with self._connection() as conn:
            rows = conn.execute(
                f"""
                SELECT workspace_id, campaign_id, aggregate_id, version, state_json, state_sha256
                FROM {self.TABLE_NAME}
                WHERE workspace_id = ? AND campaign_id = ?
                ORDER BY aggregate_id ASC
                """,
                (workspace, campaign),
            ).fetchall()
        return [
            self.get(
                workspace_id=workspace,
                campaign_id=campaign,
                aggregate_id=row["aggregate_id"],
            )
            for row in rows
        ]

    def schema_has_composite_scope_key(self) -> bool:
        """Return whether the authoritative table's primary key spans all three scope IDs."""
        with self._connection() as conn:
            columns = conn.execute(
                f"PRAGMA table_info({self.TABLE_NAME})"
            ).fetchall()
        pk = {
            int(row["pk"]): row["name"]
            for row in columns
            if int(row["pk"]) > 0
        }
        return [pk[i] for i in sorted(pk)] == [
            "workspace_id",
            "campaign_id",
            "aggregate_id",
        ]


class WorkspaceFilesystem:
    """Filesystem root resolver enforcing workspace/campaign partitioning."""

    def __init__(self, storage_root: str | os.PathLike[str]) -> None:
        self.storage_root = Path(storage_root).expanduser().resolve()
        self.storage_root.mkdir(parents=True, exist_ok=True)
        # The root itself may not be a symlink after resolution, and all child
        # workspace/campaign identifiers are validated before path construction.

    def workspace_root(self, workspace_id: str) -> Path:
        workspace = _normalize_identifier(workspace_id, field="workspace_id")
        root = self.storage_root / "workspaces" / workspace
        root.mkdir(parents=True, exist_ok=True)
        self._assert_within(root, self.storage_root)
        return root

    def campaign_root(self, workspace_id: str, campaign_id: str) -> Path:
        campaign = _normalize_identifier(campaign_id, field="campaign_id")
        root = self.workspace_root(workspace_id) / "campaigns" / campaign
        root.mkdir(parents=True, exist_ok=True)
        self._assert_within(root, self.workspace_root(workspace_id))
        return root

    def artifact_path(
        self,
        *,
        workspace_id: str,
        campaign_id: str,
        relative_path: str,
    ) -> Path:
        if not isinstance(relative_path, str) or not relative_path or "\x00" in relative_path:
            raise WorkspacePathIsolationError("Artifact path must be a non-empty string")
        if os.path.isabs(relative_path):
            raise WorkspacePathIsolationError("Absolute artifact paths are forbidden")
        raw_parts = re.split(r"[\\/]", relative_path)
        if not raw_parts or any(part in {"", ".", ".."} for part in raw_parts):
            raise WorkspacePathIsolationError("Artifact path contains an unsafe component")
        parts = Path(relative_path).parts
        if not parts:
            raise WorkspacePathIsolationError("Artifact path contains an unsafe component")
        root = self.campaign_root(workspace_id, campaign_id)
        candidate = root.joinpath(*parts)
        self._assert_no_symlink_path(candidate, root)
        self._assert_within(candidate, root)
        return candidate

    @staticmethod
    def _assert_within(candidate: Path, root: Path) -> None:
        try:
            candidate.resolve(strict=False).relative_to(root.resolve(strict=False))
        except ValueError as exc:
            raise WorkspacePathIsolationError(
                "Resolved artifact path escapes its scoped root"
            ) from exc

    @staticmethod
    def _assert_no_symlink_path(candidate: Path, root: Path) -> None:
        current = root
        try:
            relative = candidate.relative_to(root)
        except ValueError as exc:
            raise WorkspacePathIsolationError(
                "Artifact path is outside its scoped root"
            ) from exc
        for component in relative.parts:
            current = current / component
            try:
                if current.is_symlink():
                    raise WorkspacePathIsolationError(
                        "Symlink aliases are forbidden inside workspace storage"
                    )
            except OSError as exc:
                raise WorkspacePathIsolationError(
                    "Unable to validate filesystem isolation"
                ) from exc

    def write_bytes(
        self,
        *,
        workspace_id: str,
        campaign_id: str,
        relative_path: str,
        content: bytes,
    ) -> Path:
        path = self.artifact_path(
            workspace_id=workspace_id,
            campaign_id=campaign_id,
            relative_path=relative_path,
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        self._assert_no_symlink_path(path, self.campaign_root(workspace_id, campaign_id))
        with path.open("xb") as handle:
            handle.write(content)
        return path

    def read_bytes(
        self,
        *,
        workspace_id: str,
        campaign_id: str,
        relative_path: str,
    ) -> bytes:
        path = self.artifact_path(
            workspace_id=workspace_id,
            campaign_id=campaign_id,
            relative_path=relative_path,
        )
        try:
            with path.open("rb") as handle:
                return handle.read()
        except FileNotFoundError as exc:
            raise WorkspacePathIsolationError("Scoped artifact was not found") from exc


__all__ = [
    "HASH_DOMAIN",
    "INVARIANT_ID",
    "SCHEMA_VERSION",
    "ScopedState",
    "WorkspaceAuthority",
    "WorkspaceDatabaseIsolationError",
    "WorkspaceDigestMismatchError",
    "WorkspaceFilesystem",
    "WorkspaceAuthorizationError",
    "WorkspaceIsolatedDatabase",
    "WorkspaceIsolationError",
    "WorkspacePathIsolationError",
    "WorkspaceScopeError",
    "WorkspaceStateNotFoundError",
    "WorkspaceVersionConflictError",
    "canonical_scope",
    "verify_workspace_bound_sha256",
    "workspace_bound_payload",
    "workspace_bound_sha256",
]
