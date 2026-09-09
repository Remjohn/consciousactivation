"""
preparation_graph_program.py
----------------------------
CA-M009 — Interactive Parameter-Sensitive Preparation Graph.

Program coordinator: binds the PreparationGraph domain to the canonical
CAE runtime (UniversalProgramStateRuntime + StateLifecycleCoordinator).

This module owns the *program-level* operations that advance the preparation
graph through its lifecycle:

  DRAFT_GRAPH
      → SAVE_REVISION                 ← operator edits parameters
      → CANDIDATE_GRAPH_REVISION
      → EXECUTION_BINDING             ← run begins
      → ACTIVE_EXECUTION_GRAPH        ← run is live; graph is immutable

The coordinator does NOT own broader UI redesign, campaign lifecycle
semantics, or snapshot-sealing (those belong to CA-M011).

Authority lanes used:
  OPERATOR (COMMANDER)  — create_graph, bind_run
  OPERATOR (ANALYST)    — save_graph_revision (planning edit)
  HUNTER                — not used at this stage
  COMPOSER              — not used at this stage

Governing doctrine:
  - CA-M009 §5, §6, §7, §8
  - UI.md §9
  - Architecture.md §13
  - program_state_runtime.py (UniversalProgramStateRuntime, CAS)

False-proof case (anti-centroid) — enforced by PreparationGraphStore:
  The coordinator calls save_graph_revision, which writes a NEW immutable row.
  It never performs an UPDATE on an existing revision row.
  After run binding, verify_run_binding_digest is available to confirm
  the bound row has not been mutated.
"""

from __future__ import annotations

import sqlite3
from typing import Any, Dict, Optional
from uuid import uuid4

from ca_contracts import canonical_sha256, utc_now_rfc3339
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.preparation_graph_store import (
    ActiveBindingMutationError,
    DigestMismatchError,
    GraphNotFoundError,
    GraphRevisionRecord,
    GraphRunBindingRecord,
    PreparationGraphRecord,
    PreparationGraphStore,
    RevisionImmutabilityError,
    RevisionNotFoundError,
    RunBindingNotFoundError,
    StaleBaseRevisionError,
)


# ---------------------------------------------------------------------------
# Program-level exceptions
# ---------------------------------------------------------------------------

class PreparationGraphProgramError(Exception):
    """Base for program-level preparation graph errors."""
    def __init__(self, message: str, reason_code: str = "PREPARATION_GRAPH_PROGRAM_ERROR") -> None:
        super().__init__(message)
        self.reason_code = reason_code


class UnauthorizedGraphLaneError(PreparationGraphProgramError):
    """Raised when a caller uses a lane not permitted for the requested operation."""
    def __init__(self, operation: str, actual_lane: AuthorityLane, permitted: str) -> None:
        super().__init__(
            f"Operation '{operation}' requires {permitted}; called from lane '{actual_lane.value}'.",
            reason_code="UNAUTHORIZED_GRAPH_LANE",
        )


class GraphWorkspaceScopeError(PreparationGraphProgramError):
    """Raised when the workspace_id in a call does not match the graph's scope."""
    def __init__(self, graph_id: str, caller_ws: str, graph_ws: str) -> None:
        super().__init__(
            f"Graph '{graph_id}' belongs to workspace '{graph_ws}', not '{caller_ws}'.",
            reason_code="WORKSPACE_SCOPE_VIOLATION",
        )


class RunAlreadyBoundError(PreparationGraphProgramError):
    """Raised when an attempt is made to rebind an already-running execution."""
    def __init__(self, run_id: str, existing_revision_id: str) -> None:
        super().__init__(
            f"Run '{run_id}' is already bound to revision '{existing_revision_id}'.",
            reason_code="RUN_ALREADY_BOUND",
        )


# ---------------------------------------------------------------------------
# Preparation parameter helper
# ---------------------------------------------------------------------------

def _build_default_parameters() -> Dict[str, Any]:
    """Return the minimal valid parameter scaffold for a new draft graph."""
    return {
        "audience_context": {},
        "research_signals": [],
        "collision_hypotheses": [],
        "narrative_architecture": {},
        "elicitation_config": {},
        "portfolio_refs": [],
        "format_requirements": {},
        "policy_refs": [],
    }


# ---------------------------------------------------------------------------
# Program coordinator
# ---------------------------------------------------------------------------

class PreparationGraphProgramCoordinator:
    """
    Operator-facing coordinator for the CA-M009 Preparation Graph program.

    All state-changing operations route through PreparationGraphStore, which
    enforces the CAS / revision-immutability invariants.  The coordinator adds
    lane-authority checks and workspace-scope enforcement before delegating.

    This coordinator intentionally does NOT embed a UniversalProgramStateRuntime
    dependency at this iteration.  The preparation graph's own state transitions
    (DRAFT → CANDIDATE → EXECUTION_BOUND) are local to the store; the broader
    campaign-level state machine integration is a concern for CA-M011.

    Operations
    ----------
    create_graph(...)               — COMMANDER lane
    save_graph_revision(...)        — ANALYST or COMMANDER lane
    bind_run_to_revision(...)       — COMMANDER lane (run start gate)
    get_graph_operator_view(...)    — any lane (read-only)
    verify_active_run_integrity(...)— any lane (read-only, integrity proof)
    """

    def __init__(
        self,
        workspace_id: str,
        store: PreparationGraphStore,
    ) -> None:
        self.workspace_id = workspace_id
        self.store = store

    # ------------------------------------------------------------------
    # create_graph
    # ------------------------------------------------------------------

    def create_graph(
        self,
        *,
        campaign_id: str,
        name: str,
        initial_parameters: Optional[Dict[str, Any]] = None,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
        actor_id: str = "operator",
    ) -> PreparationGraphRecord:
        """
        Create a new preparation graph in DRAFT state.

        Authority:  COMMANDER
        State arc:  (new) → DRAFT_GRAPH

        If initial_parameters are provided, an initial revision R0 is created
        immediately so the graph has a valid base_revision_id of None (the
        "genesis" save).

        Returns the PreparationGraphRecord.
        """
        if lane not in (AuthorityLane.COMMANDER,):
            raise UnauthorizedGraphLaneError(
                operation="create_graph",
                actual_lane=lane,
                permitted="COMMANDER",
            )

        graph = self.store.create_graph(
            workspace_id=self.workspace_id,
            campaign_id=campaign_id,
            name=name,
        )

        # If the caller supplies initial parameters, persist them as revision seq 1
        if initial_parameters is not None:
            self.store.save_graph_revision(
                workspace_id=self.workspace_id,
                graph_id=graph.graph_id,
                base_revision_id=None,   # genesis revision has no base
                parameters=initial_parameters,
                author_id=actor_id,
            )
            # Refresh the graph record to return the updated latest_revision_id
            graph = self.store.get_graph(self.workspace_id, graph.graph_id)

        return graph

    # ------------------------------------------------------------------
    # save_graph_revision
    # ------------------------------------------------------------------

    def save_graph_revision(
        self,
        *,
        graph_id: str,
        base_revision_id: Optional[str],
        parameters: Dict[str, Any],
        lane: AuthorityLane = AuthorityLane.ANALYST,
        actor_id: str = "operator",
    ) -> GraphRevisionRecord:
        """
        Operator edits the preparation graph and saves a new revision.

        Authority:  ANALYST or COMMANDER
        State arc:  DRAFT_GRAPH / CANDIDATE → SAVE_REVISION → CANDIDATE_GRAPH_REVISION

        Contract:
        - A new immutable row is always created; existing rows are never updated.
        - base_revision_id must equal graph.latest_revision_id or the write is rejected
          (StaleBaseRevisionError — INV-M009-02).
        - The previous latest revision is transitioned CANDIDATE → HISTORICAL.

        Raises
        ------
        UnauthorizedGraphLaneError      — wrong lane
        StaleBaseRevisionError          — stale editor (INV-M009-02)
        GraphNotFoundError              — unknown graph
        """
        if lane not in (AuthorityLane.ANALYST, AuthorityLane.COMMANDER):
            raise UnauthorizedGraphLaneError(
                operation="save_graph_revision",
                actual_lane=lane,
                permitted="ANALYST or COMMANDER",
            )

        # Workspace scope guard
        graph = self.store.get_graph(self.workspace_id, graph_id)
        if graph.workspace_id != self.workspace_id:
            raise GraphWorkspaceScopeError(graph_id, self.workspace_id, graph.workspace_id)

        return self.store.save_graph_revision(
            workspace_id=self.workspace_id,
            graph_id=graph_id,
            base_revision_id=base_revision_id,
            parameters=parameters,
            author_id=actor_id,
        )

    # ------------------------------------------------------------------
    # bind_run_to_revision
    # ------------------------------------------------------------------

    def bind_run_to_revision(
        self,
        *,
        run_id: Optional[str] = None,
        graph_id: str,
        revision_id: str,
        lane: AuthorityLane = AuthorityLane.COMMANDER,
        bound_by_id: str = "operator",
    ) -> GraphRunBindingRecord:
        """
        Atomically bind a run to a specific graph revision (EXECUTION_BINDING gate).

        Authority:  COMMANDER
        State arc:  CANDIDATE_GRAPH_REVISION → SEAL → ACTIVE_EXECUTION_GRAPH

        Once bound, the run's revision cannot be changed.  Any subsequent
        operator edit to the graph creates a new revision (R2, R3, …) which does
        NOT affect runs already bound to R1.

        Raises
        ------
        UnauthorizedGraphLaneError      — wrong lane
        ActiveBindingMutationError      — run already bound to a different revision (INV-M009-03)
        RevisionNotFoundError           — revision_id does not exist
        """
        if lane not in (AuthorityLane.COMMANDER,):
            raise UnauthorizedGraphLaneError(
                operation="bind_run_to_revision",
                actual_lane=lane,
                permitted="COMMANDER",
            )

        rid = run_id or f"run_{uuid4().hex[:20]}"

        return self.store.bind_run_to_revision(
            workspace_id=self.workspace_id,
            run_id=rid,
            graph_id=graph_id,
            revision_id=revision_id,
            bound_by_id=bound_by_id,
        )

    # ------------------------------------------------------------------
    # Read-only / inspection operations
    # ------------------------------------------------------------------

    def get_graph_operator_view(self, graph_id: str) -> Dict[str, Any]:
        """
        Return the full operator projection for the preparation graph (UI §9).

        Exposes: graph header, all revisions (with lifecycle states), and run bindings.
        This is a read-only operation; it never mutates state.
        """
        return self.store.get_operator_projection(self.workspace_id, graph_id)

    def get_active_run_revision(self, run_id: str) -> GraphRevisionRecord:
        """
        Return the exact revision a run was bound to at execution start.

        This is the authoritative answer to "what parameters is this run using?"
        It MUST return the bound revision even if the graph has since been updated
        to R2, R3, etc.  (UI-001 — runtime authority.)
        """
        binding = self.store.get_run_binding(self.workspace_id, run_id)
        return self.store.get_revision(self.workspace_id, binding.revision_id)

    def verify_active_run_integrity(self, run_id: str) -> bool:
        """
        Integrity check: recompute the revision digest and compare to the stored binding.

        Returns True if the stored revision row has not been mutated since binding.
        Raises DigestMismatchError if tampering is detected.

        This is the runtime proof for INV-M009-05 and the anti-centroid guard:
        if the backend row was mutated in-place (collapsing R1 and R2 into one row),
        this check will fail.
        """
        return self.store.verify_run_binding_digest(self.workspace_id, run_id)

    def list_graph_revisions(self, graph_id: str):
        """Return all revisions for the graph, ordered by revision_seq ascending."""
        return self.store.list_revisions(self.workspace_id, graph_id)
