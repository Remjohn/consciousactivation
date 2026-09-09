"""
CA-M006 — Activative to Elicitation Linking.

Provides the authoritative many-to-many relationship boundary between immutable
Activative trigger revisions and immutable interview Elicitation Step revisions.

The implementation intentionally keeps the relationship as governed edge records
instead of duplicating identifier arrays on either parent.  Each edge carries a
deterministic SHA-256 trace over the exact parent revisions and their canonical
digests.  Resolution re-verifies the edge and the authorization boundary before
returning planning data; an untraceable elicitation branch is rejected rather
than guessed.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json
import sqlite3
from typing import Any, Iterable, Optional


TRACE_SCHEMA_VERSION = "CA-M006.v1"
DEFAULT_LINK_ROLE = "PRIMARY"
LINK_ROLES = frozenset({"PRIMARY", "FOLLOW_UP", "FALLBACK", "SUPPORTING"})


class ActivativeElicitationLinkError(RuntimeError):
    """Base error for CA-M006 relationship violations."""


class InvalidLinkError(ActivativeElicitationLinkError):
    """Raised when a relationship does not satisfy the CA-M006 contract."""


class MissingParentError(ActivativeElicitationLinkError):
    """Raised when a referenced Activative or Elicitation parent is absent."""


class UnauthorizedOriginError(ActivativeElicitationLinkError):
    """Raised when an elicitation branch lacks an authorized Activative origin."""


class DuplicateLinkError(ActivativeElicitationLinkError):
    """Raised when the same immutable edge is inserted more than once."""


class CrossWorkspaceLinkError(ActivativeElicitationLinkError):
    """Raised when an edge attempts to cross workspace boundaries."""


class TraceIntegrityError(ActivativeElicitationLinkError):
    """Raised when stored lineage bytes no longer match the trace hash."""


class RevisionConflictError(ActivativeElicitationLinkError):
    """Raised when the same identity is reused with different immutable bytes."""


class LinkRole(StrEnum):
    PRIMARY = "PRIMARY"
    FOLLOW_UP = "FOLLOW_UP"
    FALLBACK = "FALLBACK"
    SUPPORTING = "SUPPORTING"


def _canonical_json(payload: Any) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _sha256(payload: Any) -> str:
    return hashlib.sha256(_canonical_json(payload)).hexdigest()


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidLinkError(f"{field_name} must be a non-empty string")
    return value


def _require_revision(revision: int, field_name: str) -> int:
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise InvalidLinkError(f"{field_name} must be a positive integer")
    return revision


@dataclass(frozen=True, slots=True)
class ActivativeTrigger:
    """Immutable, workspace-scoped source that is allowed to originate a branch."""

    workspace_id: str
    activative_id: str
    activative_revision: int
    trigger_id: str
    authority_ref: str
    authorized: bool
    trigger_kind: str
    canonical_sha256: str

    @classmethod
    def create(
        cls,
        *,
        workspace_id: str,
        activative_id: str,
        activative_revision: int,
        trigger_id: str,
        authority_ref: str,
        trigger_kind: str = "ACTIVATIVE_TRIGGER",
        authorized: bool = True,
    ) -> "ActivativeTrigger":
        workspace_id = _require_non_empty(workspace_id, "workspace_id")
        activative_id = _require_non_empty(activative_id, "activative_id")
        trigger_id = _require_non_empty(trigger_id, "trigger_id")
        authority_ref = _require_non_empty(authority_ref, "authority_ref")
        trigger_kind = _require_non_empty(trigger_kind, "trigger_kind")
        activative_revision = _require_revision(activative_revision, "activative_revision")
        if not isinstance(authorized, bool):
            raise InvalidLinkError("authorized must be a boolean")
        if not authorized:
            # Store the record for auditability, but never permit it to originate a link.
            pass

        digest = _sha256(
            {
                "schema": TRACE_SCHEMA_VERSION,
                "kind": "activative_trigger",
                "workspace_id": workspace_id,
                "activative_id": activative_id,
                "activative_revision": activative_revision,
                "trigger_id": trigger_id,
                "authority_ref": authority_ref,
                "authorized": authorized,
                "trigger_kind": trigger_kind,
            }
        )
        return cls(
            workspace_id=workspace_id,
            activative_id=activative_id,
            activative_revision=activative_revision,
            trigger_id=trigger_id,
            authority_ref=authority_ref,
            authorized=authorized,
            trigger_kind=trigger_kind,
            canonical_sha256=digest,
        )


@dataclass(frozen=True, slots=True)
class ElicitationStep:
    """Immutable interview step identified independently from its Activative origins."""

    workspace_id: str
    elicitation_id: str
    elicitation_revision: int
    step_id: str
    branch_id: str
    sequence: int
    objective: str
    canonical_sha256: str

    @classmethod
    def create(
        cls,
        *,
        workspace_id: str,
        elicitation_id: str,
        elicitation_revision: int,
        step_id: str,
        branch_id: str,
        sequence: int,
        objective: str,
    ) -> "ElicitationStep":
        workspace_id = _require_non_empty(workspace_id, "workspace_id")
        elicitation_id = _require_non_empty(elicitation_id, "elicitation_id")
        step_id = _require_non_empty(step_id, "step_id")
        branch_id = _require_non_empty(branch_id, "branch_id")
        objective = _require_non_empty(objective, "objective")
        elicitation_revision = _require_revision(elicitation_revision, "elicitation_revision")
        if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 0:
            raise InvalidLinkError("sequence must be a non-negative integer")

        digest = _sha256(
            {
                "schema": TRACE_SCHEMA_VERSION,
                "kind": "elicitation_step",
                "workspace_id": workspace_id,
                "elicitation_id": elicitation_id,
                "elicitation_revision": elicitation_revision,
                "step_id": step_id,
                "branch_id": branch_id,
                "sequence": sequence,
                "objective": objective,
            }
        )
        return cls(
            workspace_id=workspace_id,
            elicitation_id=elicitation_id,
            elicitation_revision=elicitation_revision,
            step_id=step_id,
            branch_id=branch_id,
            sequence=sequence,
            objective=objective,
            canonical_sha256=digest,
        )


@dataclass(frozen=True, slots=True)
class ActivativeElicitationLink:
    """Governed immutable edge between one Activative trigger and one Elicitation Step."""

    workspace_id: str
    activative_id: str
    activative_revision: int
    trigger_id: str
    elicitation_id: str
    elicitation_revision: int
    step_id: str
    branch_id: str
    role: str
    trace_hash: str

    @classmethod
    def create(
        cls,
        *,
        activative: ActivativeTrigger,
        step: ElicitationStep,
        role: str = DEFAULT_LINK_ROLE,
    ) -> "ActivativeElicitationLink":
        if activative.workspace_id != step.workspace_id:
            raise CrossWorkspaceLinkError(
                "Activative trigger and elicitation step must belong to the same workspace"
            )
        role = _require_non_empty(role, "role").upper()
        if role not in LINK_ROLES:
            raise InvalidLinkError(
                f"role must be one of {sorted(LINK_ROLES)}; got {role!r}"
            )

        trace_hash = _sha256(
            {
                "schema": TRACE_SCHEMA_VERSION,
                "kind": "activative_elicitation_link",
                "workspace_id": activative.workspace_id,
                "activative_id": activative.activative_id,
                "activative_revision": activative.activative_revision,
                "trigger_id": activative.trigger_id,
                "activative_canonical_sha256": activative.canonical_sha256,
                "elicitation_id": step.elicitation_id,
                "elicitation_revision": step.elicitation_revision,
                "step_id": step.step_id,
                "branch_id": step.branch_id,
                "elicitation_canonical_sha256": step.canonical_sha256,
                "role": role,
            }
        )
        return cls(
            workspace_id=activative.workspace_id,
            activative_id=activative.activative_id,
            activative_revision=activative.activative_revision,
            trigger_id=activative.trigger_id,
            elicitation_id=step.elicitation_id,
            elicitation_revision=step.elicitation_revision,
            step_id=step.step_id,
            branch_id=step.branch_id,
            role=role,
            trace_hash=trace_hash,
        )


@dataclass(frozen=True, slots=True)
class LinkedElicitationStep:
    link: ActivativeElicitationLink
    step: ElicitationStep
    origin: ActivativeTrigger


@dataclass(frozen=True, slots=True)
class LinkedActivativeTrigger:
    link: ActivativeElicitationLink
    origin: ActivativeTrigger
    step: ElicitationStep


class ActivativeElicitationLinkRegistry:
    """
    Authoritative many-to-many edge registry.

    SQLite is used as the persistence boundary because the existing CAE runtime
    already uses SQLite for local authoritative state. Foreign keys and immutable
    parent rows prevent dangling edges. Read methods re-verify every digest so
    tampered or stale lineage never becomes a valid planning input.
    """

    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def _init_schema(self) -> None:
        with self.conn:
            self.conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS ca_m006_activative_triggers (
                    workspace_id TEXT NOT NULL,
                    activative_id TEXT NOT NULL,
                    activative_revision INTEGER NOT NULL,
                    trigger_id TEXT NOT NULL,
                    authority_ref TEXT NOT NULL,
                    authorized INTEGER NOT NULL CHECK (authorized IN (0, 1)),
                    trigger_kind TEXT NOT NULL,
                    canonical_sha256 TEXT NOT NULL,
                    PRIMARY KEY (
                        workspace_id,
                        activative_id,
                        activative_revision,
                        trigger_id
                    )
                );

                CREATE TABLE IF NOT EXISTS ca_m006_elicitation_steps (
                    workspace_id TEXT NOT NULL,
                    elicitation_id TEXT NOT NULL,
                    elicitation_revision INTEGER NOT NULL,
                    step_id TEXT NOT NULL,
                    branch_id TEXT NOT NULL,
                    sequence INTEGER NOT NULL CHECK (sequence >= 0),
                    objective TEXT NOT NULL,
                    canonical_sha256 TEXT NOT NULL,
                    PRIMARY KEY (
                        workspace_id,
                        elicitation_id,
                        elicitation_revision,
                        step_id
                    )
                );

                CREATE TABLE IF NOT EXISTS ca_m006_links (
                    workspace_id TEXT NOT NULL,
                    activative_id TEXT NOT NULL,
                    activative_revision INTEGER NOT NULL,
                    trigger_id TEXT NOT NULL,
                    elicitation_id TEXT NOT NULL,
                    elicitation_revision INTEGER NOT NULL,
                    step_id TEXT NOT NULL,
                    branch_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    trace_hash TEXT NOT NULL,
                    PRIMARY KEY (
                        workspace_id,
                        activative_id,
                        activative_revision,
                        trigger_id,
                        elicitation_id,
                        elicitation_revision,
                        step_id
                    ),
                    FOREIGN KEY (
                        workspace_id,
                        activative_id,
                        activative_revision,
                        trigger_id
                    ) REFERENCES ca_m006_activative_triggers (
                        workspace_id,
                        activative_id,
                        activative_revision,
                        trigger_id
                    ),
                    FOREIGN KEY (
                        workspace_id,
                        elicitation_id,
                        elicitation_revision,
                        step_id
                    ) REFERENCES ca_m006_elicitation_steps (
                        workspace_id,
                        elicitation_id,
                        elicitation_revision,
                        step_id
                    )
                );

                CREATE INDEX IF NOT EXISTS ix_ca_m006_links_by_activative
                ON ca_m006_links (
                    workspace_id,
                    activative_id,
                    activative_revision,
                    trigger_id
                );

                CREATE INDEX IF NOT EXISTS ix_ca_m006_links_by_elicitation
                ON ca_m006_links (
                    workspace_id,
                    elicitation_id,
                    elicitation_revision,
                    step_id,
                    branch_id
                );
                """
            )

    def register_activative(self, trigger: ActivativeTrigger) -> ActivativeTrigger:
        existing = self.conn.execute(
            """
            SELECT authority_ref, authorized, trigger_kind, canonical_sha256
            FROM ca_m006_activative_triggers
            WHERE workspace_id = ?
              AND activative_id = ?
              AND activative_revision = ?
              AND trigger_id = ?
            """,
            (
                trigger.workspace_id,
                trigger.activative_id,
                trigger.activative_revision,
                trigger.trigger_id,
            ),
        ).fetchone()

        if existing:
            if tuple(existing) != (
                trigger.authority_ref,
                int(trigger.authorized),
                trigger.trigger_kind,
                trigger.canonical_sha256,
            ):
                raise RevisionConflictError(
                    "Activative trigger revision is immutable and cannot be reused with different bytes"
                )
            return trigger

        with self.conn:
            self.conn.execute(
                """
                INSERT INTO ca_m006_activative_triggers (
                    workspace_id,
                    activative_id,
                    activative_revision,
                    trigger_id,
                    authority_ref,
                    authorized,
                    trigger_kind,
                    canonical_sha256
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    trigger.workspace_id,
                    trigger.activative_id,
                    trigger.activative_revision,
                    trigger.trigger_id,
                    trigger.authority_ref,
                    int(trigger.authorized),
                    trigger.trigger_kind,
                    trigger.canonical_sha256,
                ),
            )
        return trigger

    def register_elicitation_step(self, step: ElicitationStep) -> ElicitationStep:
        existing = self.conn.execute(
            """
            SELECT branch_id, sequence, objective, canonical_sha256
            FROM ca_m006_elicitation_steps
            WHERE workspace_id = ?
              AND elicitation_id = ?
              AND elicitation_revision = ?
              AND step_id = ?
            """,
            (
                step.workspace_id,
                step.elicitation_id,
                step.elicitation_revision,
                step.step_id,
            ),
        ).fetchone()

        if existing:
            if tuple(existing) != (
                step.branch_id,
                step.sequence,
                step.objective,
                step.canonical_sha256,
            ):
                raise RevisionConflictError(
                    "Elicitation step revision is immutable and cannot be reused with different bytes"
                )
            return step

        with self.conn:
            self.conn.execute(
                """
                INSERT INTO ca_m006_elicitation_steps (
                    workspace_id,
                    elicitation_id,
                    elicitation_revision,
                    step_id,
                    branch_id,
                    sequence,
                    objective,
                    canonical_sha256
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    step.workspace_id,
                    step.elicitation_id,
                    step.elicitation_revision,
                    step.step_id,
                    step.branch_id,
                    step.sequence,
                    step.objective,
                    step.canonical_sha256,
                ),
            )
        return step

    def link(
        self,
        *,
        activative: ActivativeTrigger,
        step: ElicitationStep,
        role: str = DEFAULT_LINK_ROLE,
    ) -> ActivativeElicitationLink:
        if activative.workspace_id != step.workspace_id:
            raise CrossWorkspaceLinkError(
                "Cannot link Activative and Elicitation entities from different workspaces"
            )
        if not activative.authorized:
            raise UnauthorizedOriginError(
                f"Activative trigger {activative.trigger_id!r} is not authorized as an origin"
            )

        stored_activative = self._get_activative(activative)
        if stored_activative is None:
            raise MissingParentError(
                f"Activative trigger {activative.trigger_id!r} revision "
                f"{activative.activative_revision} is not registered"
            )
        stored_step = self._get_step(step)
        if stored_step is None:
            raise MissingParentError(
                f"Elicitation step {step.step_id!r} revision "
                f"{step.elicitation_revision} is not registered"
            )

        if stored_activative != activative:
            raise RevisionConflictError(
                "Supplied Activative trigger bytes do not match registered revision"
            )
        if stored_step != step:
            raise RevisionConflictError(
                "Supplied Elicitation step bytes do not match registered revision"
            )

        edge = ActivativeElicitationLink.create(
            activative=stored_activative,
            step=stored_step,
            role=role,
        )
        try:
            with self.conn:
                self.conn.execute(
                    """
                    INSERT INTO ca_m006_links (
                        workspace_id,
                        activative_id,
                        activative_revision,
                        trigger_id,
                        elicitation_id,
                        elicitation_revision,
                        step_id,
                        branch_id,
                        role,
                        trace_hash
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        edge.workspace_id,
                        edge.activative_id,
                        edge.activative_revision,
                        edge.trigger_id,
                        edge.elicitation_id,
                        edge.elicitation_revision,
                        edge.step_id,
                        edge.branch_id,
                        edge.role,
                        edge.trace_hash,
                    ),
                )
        except sqlite3.IntegrityError as exc:
            if "UNIQUE" in str(exc).upper():
                raise DuplicateLinkError(
                    "The exact Activative↔Elicitation edge already exists"
                ) from exc
            raise InvalidLinkError(f"Relationship insertion rejected: {exc}") from exc
        return edge

    def unlink(
        self,
        *,
        workspace_id: str,
        activative_id: str,
        activative_revision: int,
        trigger_id: str,
        elicitation_id: str,
        elicitation_revision: int,
        step_id: str,
    ) -> None:
        """
        Remove an edge from the active relationship set.

        Parent revisions remain immutable and auditable. A removed edge can only
        reappear through an explicit new link operation; there is no mutation of
        parent identity or revision bytes.
        """
        with self.conn:
            self.conn.execute(
                """
                DELETE FROM ca_m006_links
                WHERE workspace_id = ?
                  AND activative_id = ?
                  AND activative_revision = ?
                  AND trigger_id = ?
                  AND elicitation_id = ?
                  AND elicitation_revision = ?
                  AND step_id = ?
                """,
                (
                    workspace_id,
                    activative_id,
                    activative_revision,
                    trigger_id,
                    elicitation_id,
                    elicitation_revision,
                    step_id,
                ),
            )

    def resolve_elicitation_branch(
        self,
        *,
        workspace_id: str,
        elicitation_id: str,
        elicitation_revision: int,
        branch_id: str,
    ) -> tuple[LinkedActivativeTrigger, ...]:
        """
        Resolve all authorized Activative origins for a branch.

        Fail-closed invariant: a branch is usable only when every returned edge
        resolves to a registered authorized Activative and its exact immutable
        Elicitation Step revision, with an intact trace hash. A missing edge is
        an authorization failure, not an empty success.
        """
        _require_non_empty(workspace_id, "workspace_id")
        _require_non_empty(elicitation_id, "elicitation_id")
        _require_non_empty(branch_id, "branch_id")
        _require_revision(elicitation_revision, "elicitation_revision")

        step_rows = self.conn.execute(
            """
            SELECT workspace_id, elicitation_id, elicitation_revision,
                   step_id, branch_id, sequence, objective, canonical_sha256
            FROM ca_m006_elicitation_steps
            WHERE workspace_id = ?
              AND elicitation_id = ?
              AND elicitation_revision = ?
              AND branch_id = ?
            ORDER BY sequence ASC, step_id ASC
            """,
            (workspace_id, elicitation_id, elicitation_revision, branch_id),
        ).fetchall()
        if not step_rows:
            raise MissingParentError(
                f"Elicitation branch {branch_id!r} revision {elicitation_revision} "
                "is not registered"
            )

        results: list[LinkedActivativeTrigger] = []
        for step_row in step_rows:
            step = self._step_from_row(step_row)
            edge_rows = self.conn.execute(
                """
                SELECT workspace_id, activative_id, activative_revision,
                       trigger_id, elicitation_id, elicitation_revision,
                       step_id, branch_id, role, trace_hash
                FROM ca_m006_links
                WHERE workspace_id = ?
                  AND elicitation_id = ?
                  AND elicitation_revision = ?
                  AND step_id = ?
                ORDER BY activative_id ASC, activative_revision ASC, trigger_id ASC
                """,
                (
                    workspace_id,
                    elicitation_id,
                    elicitation_revision,
                    step.step_id,
                ),
            ).fetchall()
            if not edge_rows:
                raise UnauthorizedOriginError(
                    f"Elicitation branch {branch_id!r} cannot be traced to an authorized Activative origin"
                )

            for row in edge_rows:
                edge = self._link_from_row(row)
                origin = self._get_activative_by_edge(edge)
                if origin is None:
                    raise UnauthorizedOriginError(
                        "Elicitation branch contains an edge whose Activative origin is missing"
                    )
                if not origin.authorized:
                    raise UnauthorizedOriginError(
                        f"Activative trigger {origin.trigger_id!r} is not authorized"
                    )
                self._verify_edge(edge=edge, activative=origin, step=step)
                if edge.workspace_id != workspace_id or step.branch_id != branch_id:
                    raise CrossWorkspaceLinkError(
                        "Resolved lineage does not remain inside the requested workspace/branch"
                    )

                results.append(
                    LinkedActivativeTrigger(
                        link=edge,
                        origin=origin,
                        step=step,
                    )
                )

        if not results:
            raise UnauthorizedOriginError(
                f"Elicitation branch {branch_id!r} has no authorized Activative origin"
            )
        return tuple(results)

    def resolve_activative(
        self,
        *,
        workspace_id: str,
        activative_id: str,
        activative_revision: int,
    ) -> tuple[LinkedElicitationStep, ...]:
        _require_non_empty(workspace_id, "workspace_id")
        _require_non_empty(activative_id, "activative_id")
        _require_revision(activative_revision, "activative_revision")

        origin_rows = self.conn.execute(
            """
            SELECT workspace_id, activative_id, activative_revision,
                   trigger_id, authority_ref, authorized, trigger_kind, canonical_sha256
            FROM ca_m006_activative_triggers
            WHERE workspace_id = ?
              AND activative_id = ?
              AND activative_revision = ?
            ORDER BY trigger_id ASC
            """,
            (workspace_id, activative_id, activative_revision),
        ).fetchall()
        if not origin_rows:
            raise MissingParentError(
                f"Activative {activative_id!r} revision {activative_revision} is not registered"
            )

        results: list[LinkedElicitationStep] = []
        for origin_row in origin_rows:
            origin = self._activative_from_row(origin_row)
            edge_rows = self.conn.execute(
                """
                SELECT workspace_id, activative_id, activative_revision,
                       trigger_id, elicitation_id, elicitation_revision,
                       step_id, branch_id, role, trace_hash
                FROM ca_m006_links
                WHERE workspace_id = ?
                  AND activative_id = ?
                  AND activative_revision = ?
                  AND trigger_id = ?
                ORDER BY elicitation_id ASC, elicitation_revision ASC, step_id ASC
                """,
                (
                    workspace_id,
                    activative_id,
                    activative_revision,
                    origin.trigger_id,
                ),
            ).fetchall()
            for row in edge_rows:
                edge = self._link_from_row(row)
                step = self._get_step_by_edge(edge)
                if step is None:
                    raise TraceIntegrityError(
                        "Linked Elicitation Step revision is missing"
                    )
                self._verify_edge(edge=edge, activative=origin, step=step)
                results.append(
                    LinkedElicitationStep(
                        link=edge,
                        step=step,
                        origin=origin,
                    )
                )

        return tuple(results)

    def build_interview_planning_input(
        self,
        *,
        workspace_id: str,
        elicitation_id: str,
        elicitation_revision: int,
        branch_id: str,
    ) -> tuple[dict[str, Any], ...]:
        """
        Produce structured interview-planning records without parsing labels.

        Every record is backed by an already-verified CA-M006 edge, including its
        exact Activative and Elicitation revisions and deterministic trace hash.
        """
        linked = self.resolve_elicitation_branch(
            workspace_id=workspace_id,
            elicitation_id=elicitation_id,
            elicitation_revision=elicitation_revision,
            branch_id=branch_id,
        )
        return tuple(
            {
                "workspace_id": item.link.workspace_id,
                "activative": {
                    "id": item.origin.activative_id,
                    "revision": item.origin.activative_revision,
                    "trigger_id": item.origin.trigger_id,
                    "authority_ref": item.origin.authority_ref,
                    "canonical_sha256": item.origin.canonical_sha256,
                },
                "elicitation": {
                    "id": item.step.elicitation_id,
                    "revision": item.step.elicitation_revision,
                    "step_id": item.step.step_id,
                    "branch_id": item.step.branch_id,
                    "sequence": item.step.sequence,
                    "objective": item.step.objective,
                    "canonical_sha256": item.step.canonical_sha256,
                },
                "relationship": {
                    "role": item.link.role,
                    "trace_hash": item.link.trace_hash,
                },
            }
            for item in linked
        )

    def list_links(self, *, workspace_id: str) -> tuple[ActivativeElicitationLink, ...]:
        rows = self.conn.execute(
            """
            SELECT workspace_id, activative_id, activative_revision,
                   trigger_id, elicitation_id, elicitation_revision,
                   step_id, branch_id, role, trace_hash
            FROM ca_m006_links
            WHERE workspace_id = ?
            ORDER BY activative_id, activative_revision, trigger_id,
                     elicitation_id, elicitation_revision, step_id
            """,
            (workspace_id,),
        ).fetchall()
        return tuple(self._link_from_row(row) for row in rows)

    def _get_activative(self, trigger: ActivativeTrigger) -> Optional[ActivativeTrigger]:
        row = self.conn.execute(
            """
            SELECT workspace_id, activative_id, activative_revision,
                   trigger_id, authority_ref, authorized, trigger_kind, canonical_sha256
            FROM ca_m006_activative_triggers
            WHERE workspace_id = ?
              AND activative_id = ?
              AND activative_revision = ?
              AND trigger_id = ?
            """,
            (
                trigger.workspace_id,
                trigger.activative_id,
                trigger.activative_revision,
                trigger.trigger_id,
            ),
        ).fetchone()
        return self._activative_from_row(row) if row else None

    def _get_activative_by_edge(
        self, edge: ActivativeElicitationLink
    ) -> Optional[ActivativeTrigger]:
        row = self.conn.execute(
            """
            SELECT workspace_id, activative_id, activative_revision,
                   trigger_id, authority_ref, authorized, trigger_kind, canonical_sha256
            FROM ca_m006_activative_triggers
            WHERE workspace_id = ?
              AND activative_id = ?
              AND activative_revision = ?
              AND trigger_id = ?
            """,
            (
                edge.workspace_id,
                edge.activative_id,
                edge.activative_revision,
                edge.trigger_id,
            ),
        ).fetchone()
        return self._activative_from_row(row) if row else None

    def _get_step(self, step: ElicitationStep) -> Optional[ElicitationStep]:
        row = self.conn.execute(
            """
            SELECT workspace_id, elicitation_id, elicitation_revision,
                   step_id, branch_id, sequence, objective, canonical_sha256
            FROM ca_m006_elicitation_steps
            WHERE workspace_id = ?
              AND elicitation_id = ?
              AND elicitation_revision = ?
              AND step_id = ?
            """,
            (
                step.workspace_id,
                step.elicitation_id,
                step.elicitation_revision,
                step.step_id,
            ),
        ).fetchone()
        return self._step_from_row(row) if row else None

    def _get_step_by_edge(
        self, edge: ActivativeElicitationLink
    ) -> Optional[ElicitationStep]:
        row = self.conn.execute(
            """
            SELECT workspace_id, elicitation_id, elicitation_revision,
                   step_id, branch_id, sequence, objective, canonical_sha256
            FROM ca_m006_elicitation_steps
            WHERE workspace_id = ?
              AND elicitation_id = ?
              AND elicitation_revision = ?
              AND step_id = ?
            """,
            (
                edge.workspace_id,
                edge.elicitation_id,
                edge.elicitation_revision,
                edge.step_id,
            ),
        ).fetchone()
        return self._step_from_row(row) if row else None

    @staticmethod
    def _activative_from_row(row: Any) -> ActivativeTrigger:
        return ActivativeTrigger(
            workspace_id=row[0],
            activative_id=row[1],
            activative_revision=int(row[2]),
            trigger_id=row[3],
            authority_ref=row[4],
            authorized=bool(row[5]),
            trigger_kind=row[6],
            canonical_sha256=row[7],
        )

    @staticmethod
    def _step_from_row(row: Any) -> ElicitationStep:
        return ElicitationStep(
            workspace_id=row[0],
            elicitation_id=row[1],
            elicitation_revision=int(row[2]),
            step_id=row[3],
            branch_id=row[4],
            sequence=int(row[5]),
            objective=row[6],
            canonical_sha256=row[7],
        )

    @staticmethod
    def _link_from_row(row: Any) -> ActivativeElicitationLink:
        return ActivativeElicitationLink(
            workspace_id=row[0],
            activative_id=row[1],
            activative_revision=int(row[2]),
            trigger_id=row[3],
            elicitation_id=row[4],
            elicitation_revision=int(row[5]),
            step_id=row[6],
            branch_id=row[7],
            role=row[8],
            trace_hash=row[9],
        )

    @staticmethod
    def _verify_edge(
        *,
        edge: ActivativeElicitationLink,
        activative: ActivativeTrigger,
        step: ElicitationStep,
    ) -> None:
        if activative.workspace_id != edge.workspace_id or step.workspace_id != edge.workspace_id:
            raise CrossWorkspaceLinkError(
                "Edge, Activative origin, and Elicitation step must share a workspace"
            )
        expected_edge = ActivativeElicitationLink.create(
            activative=activative,
            step=step,
            role=edge.role,
        )
        if expected_edge.trace_hash != edge.trace_hash:
            raise TraceIntegrityError(
                f"Trace hash mismatch for edge {edge.activative_id!r}↔{edge.step_id!r}"
            )

        expected_activative_sha = ActivativeTrigger.create(
            workspace_id=activative.workspace_id,
            activative_id=activative.activative_id,
            activative_revision=activative.activative_revision,
            trigger_id=activative.trigger_id,
            authority_ref=activative.authority_ref,
            trigger_kind=activative.trigger_kind,
            authorized=activative.authorized,
        ).canonical_sha256
        if expected_activative_sha != activative.canonical_sha256:
            raise TraceIntegrityError("Activative trigger canonical digest is invalid")

        expected_step_sha = ElicitationStep.create(
            workspace_id=step.workspace_id,
            elicitation_id=step.elicitation_id,
            elicitation_revision=step.elicitation_revision,
            step_id=step.step_id,
            branch_id=step.branch_id,
            sequence=step.sequence,
            objective=step.objective,
        ).canonical_sha256
        if expected_step_sha != step.canonical_sha256:
            raise TraceIntegrityError("Elicitation step canonical digest is invalid")


__all__ = [
    "ActivativeElicitationLink",
    "ActivativeElicitationLinkError",
    "ActivativeElicitationLinkRegistry",
    "ActivativeTrigger",
    "CrossWorkspaceLinkError",
    "DEFAULT_LINK_ROLE",
    "DuplicateLinkError",
    "ElicitationStep",
    "InvalidLinkError",
    "LinkRole",
    "LinkedActivativeTrigger",
    "LinkedElicitationStep",
    "LINK_ROLES",
    "MissingParentError",
    "RevisionConflictError",
    "TRACE_SCHEMA_VERSION",
    "TraceIntegrityError",
    "UnauthorizedOriginError",
]
