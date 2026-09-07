"""
preparation_graph_store.py
--------------------------
CA-M009 — Interactive Parameter-Sensitive Preparation Graph.

Authoritative storage adapter for the PreparationGraph lifecycle:

    DRAFT_GRAPH
        → SAVE_REVISION   (Operator edits params and saves)
        → CANDIDATE_GRAPH_REVISION
        → SEAL / EXECUTION_BINDING
        → ACTIVE_EXECUTION_GRAPH

Governing doctrine:
  - UI.md §9 — Preparation Graph invariants
  - Architecture.md §13 — Pre-Production Snapshot (sealed, cryptographically bound)
  - CA-M009 mandate §5 — exact scope (draft, revision, run binding, historical inspection)
  - CA-M009 mandate §7 — prohibitions (no collapse of draft/candidate/sealed/active into one
    mutable row; no silent overwrite from stale editor)

Invariants enforced here:
  INV-M009-01 — A revision row is immutable once written.
  INV-M009-02 — stale_write_rejected: a SAVE_REVISION whose base_revision_id does not match
                the current latest revision for the graph is rejected.
  INV-M009-03 — active_binding_immutable: an active run's bound revision_id cannot be
                overwritten by a subsequent SAVE_REVISION.
  INV-M009-04 — historical revisions remain inspectable forever.
  INV-M009-05 — run binding stores revision_id + canonical_sha256 of the parameter payload.

False-proof case (anti-centroid):
  The UI may display a new revision (R2) while the backend row for an active run still
  references R1.  A GET of the active run must return R1's revision_id and digest.  If
  the backend row was mutated in-place (collapsing R1 and R2 into the same row) the
  invariant is violated.  All writes go through save_graph_revision(); in-place update of
  a committed revision raises RevisionImmutabilityError.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from ca_contracts import canonical_sha256, utc_now_rfc3339


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class PreparationGraphError(Exception):
    """Base for all preparation-graph store errors."""
    def __init__(self, message: str, reason_code: str = "PREPARATION_GRAPH_ERROR") -> None:
        super().__init__(message)
        self.reason_code = reason_code


class RevisionImmutabilityError(PreparationGraphError):
    """
    INV-M009-01: Raised when caller attempts to mutate an already-committed revision row.

    This is the anti-centroid guard: if the backend row is mutated in-place, the active run
    unknowingly uses a different parameter set.  That is invalid per mandate §9.
    """
    def __init__(self, revision_id: str) -> None:
        super().__init__(
            f"Revision '{revision_id}' is immutable; create a new revision instead.",
            reason_code="REVISION_IMMUTABILITY_VIOLATION",
        )
        self.revision_id = revision_id


class StaleBaseRevisionError(PreparationGraphError):
    """
    INV-M009-02: Raised when save_graph_revision is called with a base_revision_id that does
    not match the current latest revision for the graph, indicating a stale editor.
    """
    def __init__(self, graph_id: str, expected_base: Optional[str], actual_latest: Optional[str]) -> None:
        super().__init__(
            f"Stale write rejected for graph '{graph_id}': "
            f"caller base_revision_id='{expected_base}' but current latest='{actual_latest}'.",
            reason_code="STALE_BASE_REVISION",
        )
        self.graph_id = graph_id
        self.expected_base = expected_base
        self.actual_latest = actual_latest


class ActiveBindingMutationError(PreparationGraphError):
    """
    INV-M009-03: Raised when a caller attempts to change the revision binding on an active run.
    """
    def __init__(self, run_id: str, bound_revision_id: str) -> None:
        super().__init__(
            f"Run '{run_id}' is already bound to revision '{bound_revision_id}'. "
            "Active run bindings are immutable.",
            reason_code="ACTIVE_BINDING_MUTATION",
        )
        self.run_id = run_id
        self.bound_revision_id = bound_revision_id


class GraphNotFoundError(PreparationGraphError):
    """Raised when the requested graph does not exist."""
    def __init__(self, graph_id: str) -> None:
        super().__init__(
            f"PreparationGraph '{graph_id}' not found.",
            reason_code="GRAPH_NOT_FOUND",
        )


class RevisionNotFoundError(PreparationGraphError):
    """Raised when the requested revision does not exist."""
    def __init__(self, revision_id: str) -> None:
        super().__init__(
            f"GraphRevision '{revision_id}' not found.",
            reason_code="REVISION_NOT_FOUND",
        )


class RunBindingNotFoundError(PreparationGraphError):
    """Raised when the requested run binding does not exist."""
    def __init__(self, run_id: str) -> None:
        super().__init__(
            f"GraphRunBinding for run '{run_id}' not found.",
            reason_code="RUN_BINDING_NOT_FOUND",
        )


class DigestMismatchError(PreparationGraphError):
    """
    INV-M009-05 diagnostic: raised when a digest read from the store does not match the
    expected canonical digest of the revision's parameter payload.
    """
    def __init__(self, revision_id: str, stored: str, computed: str) -> None:
        super().__init__(
            f"Digest mismatch for revision '{revision_id}': stored='{stored}', computed='{computed}'.",
            reason_code="DIGEST_MISMATCH",
        )
        self.revision_id = revision_id
        self.stored = stored
        self.computed = computed


# ---------------------------------------------------------------------------
# Domain models (Pydantic — validate-on-construction)
# ---------------------------------------------------------------------------

class GraphLifecycleState(str):
    """Allowed lifecycle states for a PreparationGraph row."""
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    SEALED = "SEALED"
    ARCHIVED = "ARCHIVED"


class RevisionLifecycleState(str):
    """Allowed lifecycle states for a GraphRevision row."""
    CANDIDATE = "CANDIDATE"
    EXECUTION_BOUND = "EXECUTION_BOUND"
    HISTORICAL = "HISTORICAL"


class PreparationGraphRecord(BaseModel):
    """
    Authoritative record for a named preparation graph.

    A graph is a first-class planning artifact scoped to a workspace and campaign.
    Multiple revisions are children of a single graph.
    The graph row tracks the latest_revision_id for stale-write detection.
    """
    workspace_id: str
    graph_id: str
    campaign_id: str
    name: str
    lifecycle_state: str = GraphLifecycleState.DRAFT
    latest_revision_id: Optional[str] = None
    created_at: str = Field(default_factory=utc_now_rfc3339)
    updated_at: str = Field(default_factory=utc_now_rfc3339)


class GraphRevisionRecord(BaseModel):
    """
    Immutable revision snapshot of a preparation graph's parameters.

    Once a row is written it MUST NOT be updated (INV-M009-01).
    The canonical_sha256 field is the integrity digest of parameter_payload_json.

    lifecycle_state transitions:
        CANDIDATE  →  EXECUTION_BOUND  (when a run binds this revision)
        CANDIDATE  →  HISTORICAL       (when a newer revision supersedes it)
        EXECUTION_BOUND stays EXECUTION_BOUND; cannot be HISTORICAL while a run references it.
    """
    workspace_id: str
    graph_id: str
    revision_id: str
    revision_seq: int                   # monotonically increasing within a graph
    base_revision_id: Optional[str]     # the revision this was created from (lineage)
    parameter_payload_json: str         # canonical JSON of the graph's parameters
    canonical_sha256: str               # SHA-256 of parameter_payload_json bytes
    author_id: str
    lifecycle_state: str = RevisionLifecycleState.CANDIDATE
    created_at: str = Field(default_factory=utc_now_rfc3339)


class GraphRunBindingRecord(BaseModel):
    """
    Binds a CAE run to the exact graph revision it was started with.

    The binding is immutable (INV-M009-03): once created it is never changed.
    The revision_digest stores the SHA-256 at binding time for later verification.
    """
    workspace_id: str
    run_id: str
    graph_id: str
    revision_id: str
    revision_digest: str    # copied from GraphRevisionRecord.canonical_sha256 at bind time
    bound_at: str = Field(default_factory=utc_now_rfc3339)
    bound_by_id: str = ""


# ---------------------------------------------------------------------------
# Store implementation
# ---------------------------------------------------------------------------

class PreparationGraphStore:
    """
    Relational storage adapter for the CA-M009 Preparation Graph lifecycle.

    Uses SQLite for local / test environments and is forward-compatible with
    PostgreSQL (the project's canonical persistence layer) via the same SQL dialect
    subset the other stores use.

    Thread-safety: each call that mutates state uses an explicit `with self.conn:`
    context to issue a transaction boundary, matching the pattern of
    CollisionHypothesisStore and InterviewSemanticStore.

    Public API
    ----------
    create_graph(...)                 → PreparationGraphRecord
    get_graph(workspace_id, graph_id) → PreparationGraphRecord
    save_graph_revision(...)          → GraphRevisionRecord     ← creates new revision, rejects stale base
    get_revision(workspace_id, rev_id)→ GraphRevisionRecord
    list_revisions(workspace_id, graph_id) → List[GraphRevisionRecord]  ← historical inspection
    bind_run_to_revision(...)         → GraphRunBindingRecord   ← atomic, immutable
    get_run_binding(workspace_id, run_id) → GraphRunBindingRecord
    verify_run_binding_digest(...)    → bool                    ← post-bind integrity check
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.conn = connection
        self._init_schema()

    # ------------------------------------------------------------------
    # Schema bootstrap
    # ------------------------------------------------------------------

    def _init_schema(self) -> None:
        """
        Create the three tables required by M009.
        These are the SQLite-compatible equivalents of the PostgreSQL migration
        in 0011_cae_preparation_graph.sql.
        """
        with self.conn:
            # 1. preparation_graph — one row per named graph (draft tracking)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS preparation_graph (
                    workspace_id TEXT NOT NULL,
                    graph_id TEXT NOT NULL,
                    campaign_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    lifecycle_state TEXT NOT NULL DEFAULT 'DRAFT',
                    latest_revision_id TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, graph_id)
                );
            """)

            # 2. graph_revision — immutable snapshot rows (one per operator SAVE_REVISION)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS graph_revision (
                    workspace_id TEXT NOT NULL,
                    graph_id TEXT NOT NULL,
                    revision_id TEXT NOT NULL,
                    revision_seq INTEGER NOT NULL,
                    base_revision_id TEXT,
                    parameter_payload_json TEXT NOT NULL,
                    canonical_sha256 TEXT NOT NULL,
                    author_id TEXT NOT NULL,
                    lifecycle_state TEXT NOT NULL DEFAULT 'CANDIDATE',
                    created_at TEXT NOT NULL,
                    PRIMARY KEY (workspace_id, revision_id),
                    FOREIGN KEY (workspace_id, graph_id)
                        REFERENCES preparation_graph(workspace_id, graph_id)
                );
            """)

            # 3. graph_run_binding — immutable run→revision binding records
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS graph_run_binding (
                    workspace_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    graph_id TEXT NOT NULL,
                    revision_id TEXT NOT NULL,
                    revision_digest TEXT NOT NULL,
                    bound_at TEXT NOT NULL,
                    bound_by_id TEXT NOT NULL DEFAULT '',
                    PRIMARY KEY (workspace_id, run_id),
                    FOREIGN KEY (workspace_id, revision_id)
                        REFERENCES graph_revision(workspace_id, revision_id)
                );
            """)

            # Indexes for common access patterns
            self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_graph_revision_graph
                    ON graph_revision (workspace_id, graph_id, revision_seq);
            """)
            self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_graph_revision_state
                    ON graph_revision (workspace_id, lifecycle_state);
            """)
            self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_graph_run_binding_revision
                    ON graph_run_binding (workspace_id, revision_id);
            """)

    # ------------------------------------------------------------------
    # Graph CRUD
    # ------------------------------------------------------------------

    def create_graph(
        self,
        *,
        workspace_id: str,
        graph_id: Optional[str] = None,
        campaign_id: str,
        name: str,
    ) -> PreparationGraphRecord:
        """
        Create a new preparation graph in DRAFT state.
        No revision exists yet; latest_revision_id is NULL.
        """
        gid = graph_id or f"graph_{uuid4().hex[:20]}"
        now = utc_now_rfc3339()
        record = PreparationGraphRecord(
            workspace_id=workspace_id,
            graph_id=gid,
            campaign_id=campaign_id,
            name=name,
            lifecycle_state=GraphLifecycleState.DRAFT,
            latest_revision_id=None,
            created_at=now,
            updated_at=now,
        )
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO preparation_graph
                    (workspace_id, graph_id, campaign_id, name,
                     lifecycle_state, latest_revision_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.workspace_id,
                    record.graph_id,
                    record.campaign_id,
                    record.name,
                    record.lifecycle_state,
                    record.latest_revision_id,
                    record.created_at,
                    record.updated_at,
                ),
            )
        return record

    def get_graph(self, workspace_id: str, graph_id: str) -> PreparationGraphRecord:
        """Return the current graph header; raises GraphNotFoundError if absent."""
        row = self.conn.execute(
            """
            SELECT workspace_id, graph_id, campaign_id, name,
                   lifecycle_state, latest_revision_id, created_at, updated_at
            FROM preparation_graph
            WHERE workspace_id = ? AND graph_id = ?
            """,
            (workspace_id, graph_id),
        ).fetchone()
        if row is None:
            raise GraphNotFoundError(graph_id)
        return PreparationGraphRecord(
            workspace_id=row[0],
            graph_id=row[1],
            campaign_id=row[2],
            name=row[3],
            lifecycle_state=row[4],
            latest_revision_id=row[5],
            created_at=row[6],
            updated_at=row[7],
        )

    # ------------------------------------------------------------------
    # Revision creation (SAVE_REVISION — the core M009 operation)
    # ------------------------------------------------------------------

    def save_graph_revision(
        self,
        *,
        workspace_id: str,
        graph_id: str,
        base_revision_id: Optional[str],
        parameters: Dict[str, Any],
        author_id: str,
    ) -> GraphRevisionRecord:
        """
        Create a new immutable revision of the preparation graph.

        Lifecycle:
            DRAFT_GRAPH
                → SAVE_REVISION
                → CANDIDATE_GRAPH_REVISION   (new revision row created)
            Previous latest revision is transitioned CANDIDATE → HISTORICAL
            graph.latest_revision_id is updated to the new revision_id.

        Stale-write rejection (INV-M009-02):
            If the caller supplies a base_revision_id that does not match the graph's
            current latest_revision_id, the write is rejected with StaleBaseRevisionError.
            This prevents an editor that loaded an older revision from overwriting a newer one.

        Parameters
        ----------
        workspace_id : str
        graph_id : str
        base_revision_id : str | None
            The revision_id the caller's editor was showing when the user clicked Save.
            Must match graph.latest_revision_id.  Pass None only for the very first revision.
        parameters : dict
            The preparation graph parameter payload (audience, hypotheses, elicitation config…).
        author_id : str
            Operator identity issuing this SAVE_REVISION.

        Returns
        -------
        GraphRevisionRecord — the newly created, immutable revision.
        """
        graph = self.get_graph(workspace_id, graph_id)

        # INV-M009-02 — stale write detection
        if graph.latest_revision_id != base_revision_id:
            raise StaleBaseRevisionError(
                graph_id=graph_id,
                expected_base=base_revision_id,
                actual_latest=graph.latest_revision_id,
            )

        # Derive next sequence number
        row = self.conn.execute(
            """
            SELECT COALESCE(MAX(revision_seq), 0)
            FROM graph_revision
            WHERE workspace_id = ? AND graph_id = ?
            """,
            (workspace_id, graph_id),
        ).fetchone()
        next_seq = (row[0] if row else 0) + 1

        # Build the canonical payload and digest
        payload_json = json.dumps(parameters, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        digest = canonical_sha256(parameters)
        revision_id = f"rev_{graph_id}_{uuid4().hex[:16]}"
        now = utc_now_rfc3339()

        revision = GraphRevisionRecord(
            workspace_id=workspace_id,
            graph_id=graph_id,
            revision_id=revision_id,
            revision_seq=next_seq,
            base_revision_id=base_revision_id,
            parameter_payload_json=payload_json,
            canonical_sha256=digest,
            author_id=author_id,
            lifecycle_state=RevisionLifecycleState.CANDIDATE,
            created_at=now,
        )

        with self.conn:
            # Mark previous latest revision HISTORICAL (if any)
            if graph.latest_revision_id is not None:
                # Guard: only mark CANDIDATE → HISTORICAL; never change EXECUTION_BOUND revisions
                self.conn.execute(
                    """
                    UPDATE graph_revision
                    SET lifecycle_state = 'HISTORICAL'
                    WHERE workspace_id = ?
                      AND revision_id = ?
                      AND lifecycle_state = 'CANDIDATE'
                    """,
                    (workspace_id, graph.latest_revision_id),
                )

            # Insert new revision row (immutable from this point forward)
            self.conn.execute(
                """
                INSERT INTO graph_revision
                    (workspace_id, graph_id, revision_id, revision_seq,
                     base_revision_id, parameter_payload_json, canonical_sha256,
                     author_id, lifecycle_state, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    revision.workspace_id,
                    revision.graph_id,
                    revision.revision_id,
                    revision.revision_seq,
                    revision.base_revision_id,
                    revision.parameter_payload_json,
                    revision.canonical_sha256,
                    revision.author_id,
                    revision.lifecycle_state,
                    revision.created_at,
                ),
            )

            # Update graph header's latest_revision_id and updated_at
            self.conn.execute(
                """
                UPDATE preparation_graph
                SET latest_revision_id = ?, updated_at = ?
                WHERE workspace_id = ? AND graph_id = ?
                """,
                (revision_id, now, workspace_id, graph_id),
            )

        return revision

    # ------------------------------------------------------------------
    # Revision reads (historical inspection — INV-M009-04)
    # ------------------------------------------------------------------

    def get_revision(self, workspace_id: str, revision_id: str) -> GraphRevisionRecord:
        """
        Return a specific revision by ID.  All historical revisions remain accessible.
        """
        row = self.conn.execute(
            """
            SELECT workspace_id, graph_id, revision_id, revision_seq,
                   base_revision_id, parameter_payload_json, canonical_sha256,
                   author_id, lifecycle_state, created_at
            FROM graph_revision
            WHERE workspace_id = ? AND revision_id = ?
            """,
            (workspace_id, revision_id),
        ).fetchone()
        if row is None:
            raise RevisionNotFoundError(revision_id)
        return GraphRevisionRecord(
            workspace_id=row[0],
            graph_id=row[1],
            revision_id=row[2],
            revision_seq=row[3],
            base_revision_id=row[4],
            parameter_payload_json=row[5],
            canonical_sha256=row[6],
            author_id=row[7],
            lifecycle_state=row[8],
            created_at=row[9],
        )

    def list_revisions(
        self, workspace_id: str, graph_id: str
    ) -> List[GraphRevisionRecord]:
        """
        Return all revisions for a graph, ordered by revision_seq ascending.
        Historical revisions are included (INV-M009-04).
        """
        rows = self.conn.execute(
            """
            SELECT workspace_id, graph_id, revision_id, revision_seq,
                   base_revision_id, parameter_payload_json, canonical_sha256,
                   author_id, lifecycle_state, created_at
            FROM graph_revision
            WHERE workspace_id = ? AND graph_id = ?
            ORDER BY revision_seq ASC
            """,
            (workspace_id, graph_id),
        ).fetchall()
        return [
            GraphRevisionRecord(
                workspace_id=r[0],
                graph_id=r[1],
                revision_id=r[2],
                revision_seq=r[3],
                base_revision_id=r[4],
                parameter_payload_json=r[5],
                canonical_sha256=r[6],
                author_id=r[7],
                lifecycle_state=r[8],
                created_at=r[9],
            )
            for r in rows
        ]

    # ------------------------------------------------------------------
    # Run binding (SEAL / EXECUTION_BINDING — INV-M009-03, INV-M009-05)
    # ------------------------------------------------------------------

    def bind_run_to_revision(
        self,
        *,
        workspace_id: str,
        run_id: str,
        graph_id: str,
        revision_id: str,
        bound_by_id: str = "",
    ) -> GraphRunBindingRecord:
        """
        Atomically bind a run to a specific graph revision.

        Lifecycle:
            CANDIDATE_GRAPH_REVISION
                → SEAL / EXECUTION_BINDING
                → ACTIVE_EXECUTION_GRAPH

        This is the M009 §2 contract:
          "Once a run begins, the active execution must remain bound to the exact graph
           revision captured for that run."

        The revision's lifecycle_state is transitioned from CANDIDATE → EXECUTION_BOUND.
        The binding record is written atomically with that state change.
        Once created, the binding row is never updated (INV-M009-03).

        Raises ActiveBindingMutationError if a binding already exists for this run_id.
        Raises RevisionNotFoundError if revision_id does not exist.
        """
        # Verify revision exists and retrieve its digest
        revision = self.get_revision(workspace_id, revision_id)

        # Idempotency guard: if already bound, return existing binding unchanged
        try:
            existing = self.get_run_binding(workspace_id, run_id)
            if existing.revision_id == revision_id:
                # Idempotent re-bind to the same revision is OK
                return existing
            # Different revision → immutability violation
            raise ActiveBindingMutationError(
                run_id=run_id,
                bound_revision_id=existing.revision_id,
            )
        except RunBindingNotFoundError:
            pass  # expected; proceed to create

        now = utc_now_rfc3339()
        binding = GraphRunBindingRecord(
            workspace_id=workspace_id,
            run_id=run_id,
            graph_id=graph_id,
            revision_id=revision_id,
            revision_digest=revision.canonical_sha256,  # INV-M009-05
            bound_at=now,
            bound_by_id=bound_by_id,
        )

        with self.conn:
            # Transition revision: CANDIDATE → EXECUTION_BOUND
            self.conn.execute(
                """
                UPDATE graph_revision
                SET lifecycle_state = 'EXECUTION_BOUND'
                WHERE workspace_id = ? AND revision_id = ?
                  AND lifecycle_state = 'CANDIDATE'
                """,
                (workspace_id, revision_id),
            )

            # Create the immutable binding row
            self.conn.execute(
                """
                INSERT INTO graph_run_binding
                    (workspace_id, run_id, graph_id, revision_id,
                     revision_digest, bound_at, bound_by_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    binding.workspace_id,
                    binding.run_id,
                    binding.graph_id,
                    binding.revision_id,
                    binding.revision_digest,
                    binding.bound_at,
                    binding.bound_by_id,
                ),
            )

        return binding

    def get_run_binding(self, workspace_id: str, run_id: str) -> GraphRunBindingRecord:
        """
        Return the immutable run binding.

        This is the authoritative read for "what revision is this run using?"
        It MUST return the revision from when the run started, regardless of how many
        subsequent revisions exist on the graph (UI-001 — runtime authority).
        """
        row = self.conn.execute(
            """
            SELECT workspace_id, run_id, graph_id, revision_id,
                   revision_digest, bound_at, bound_by_id
            FROM graph_run_binding
            WHERE workspace_id = ? AND run_id = ?
            """,
            (workspace_id, run_id),
        ).fetchone()
        if row is None:
            raise RunBindingNotFoundError(run_id)
        return GraphRunBindingRecord(
            workspace_id=row[0],
            run_id=row[1],
            graph_id=row[2],
            revision_id=row[3],
            revision_digest=row[4],
            bound_at=row[5],
            bound_by_id=row[6],
        )

    def verify_run_binding_digest(
        self, workspace_id: str, run_id: str
    ) -> bool:
        """
        Post-bind integrity check (INV-M009-05).

        Re-reads the revision's parameter_payload_json, recomputes its canonical SHA-256,
        and compares against the digest stored in the run binding.

        Returns True if digests match; raises DigestMismatchError otherwise.

        This detects any in-place mutation of the revision row after binding (the
        false-proof case: backend mutating the row while the run is active).
        """
        binding = self.get_run_binding(workspace_id, run_id)
        revision = self.get_revision(workspace_id, binding.revision_id)

        # Recompute from stored JSON (the canonical representation)
        parameters = json.loads(revision.parameter_payload_json)
        computed = canonical_sha256(parameters)

        if computed != binding.revision_digest:
            raise DigestMismatchError(
                revision_id=revision.revision_id,
                stored=binding.revision_digest,
                computed=computed,
            )
        if computed != revision.canonical_sha256:
            raise DigestMismatchError(
                revision_id=revision.revision_id,
                stored=revision.canonical_sha256,
                computed=computed,
            )
        return True

    # ------------------------------------------------------------------
    # Operator projection helper
    # ------------------------------------------------------------------

    def get_operator_projection(
        self, workspace_id: str, graph_id: str
    ) -> Dict[str, Any]:
        """
        Return a structured projection for the operator surface (UI §9).

        Exposes:
        - graph header (draft graph / lifecycle)
        - latest revision identity and lifecycle_state (candidate / execution-bound)
        - ordered list of all revision summaries (revision_id, seq, lifecycle_state, created_at)
        - list of run bindings referencing any revision of this graph

        This is a READ ONLY operation — no state is mutated.
        """
        graph = self.get_graph(workspace_id, graph_id)
        revisions = self.list_revisions(workspace_id, graph_id)

        # Fetch run bindings for this graph
        binding_rows = self.conn.execute(
            """
            SELECT run_id, revision_id, revision_digest, bound_at, bound_by_id
            FROM graph_run_binding
            WHERE workspace_id = ? AND graph_id = ?
            ORDER BY bound_at ASC
            """,
            (workspace_id, graph_id),
        ).fetchall()

        return {
            "graph": {
                "graph_id": graph.graph_id,
                "campaign_id": graph.campaign_id,
                "name": graph.name,
                "lifecycle_state": graph.lifecycle_state,
                "latest_revision_id": graph.latest_revision_id,
                "created_at": graph.created_at,
                "updated_at": graph.updated_at,
            },
            "revisions": [
                {
                    "revision_id": r.revision_id,
                    "revision_seq": r.revision_seq,
                    "base_revision_id": r.base_revision_id,
                    "lifecycle_state": r.lifecycle_state,
                    "canonical_sha256": r.canonical_sha256,
                    "author_id": r.author_id,
                    "created_at": r.created_at,
                }
                for r in revisions
            ],
            "run_bindings": [
                {
                    "run_id": row[0],
                    "revision_id": row[1],
                    "revision_digest": row[2],
                    "bound_at": row[3],
                    "bound_by_id": row[4],
                }
                for row in binding_rows
            ],
        }
