"""JIT Context-Budget Compiler — CA-M036 (INV-CTX-002).

Implements input-scoped context projection, authority-lane masking, and
committed state_hash parity assertion as required by CAE Mandate 036
(Canonical Question Q36, Spine Q03).

The sole responsibility of this module is to compile a pruned, lane-masked,
hash-bound context snapshot for an active program node.  It does NOT
implement host runner loops, provider routing, or output self-repair.

Governed by:
- docs/cae/CAE_PRD_mandates/CAE_MANDATE_BUNDLE_WAVE_05/06_CA_MANDATE_036.md
- FUNCTIONAL_REQUIREMENTS.md  FR-036 / INV-CTX-002
- Architecture.md  §"context projection"
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, FrozenSet, List, Optional, Set

from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_state_runtime import (
    ProgramStateAggregate,
    ProgramStateLocalContext,
    ProgramStateRuntimeError,
    UniversalProgramStateRuntime,
)


# ---------------------------------------------------------------------------
# Typed exceptions (fail-closed contract)
# ---------------------------------------------------------------------------

class ContextBudgetError(ProgramStateRuntimeError):
    """Base error for JIT context-budget compilation failures."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "CONTEXT_BUDGET_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, reason_code=reason_code, details=details)


class MissingNodeDeclarationError(ContextBudgetError):
    """Raised when a node has no declared inputs and no lane metadata is available.

    Per mandate: stop and report rather than projecting full state as a workaround.
    """

    def __init__(self, node_id: str) -> None:
        super().__init__(
            f"Node '{node_id}' has neither declared inputs nor lane metadata; "
            "cannot project context without risking full-state leakage.",
            reason_code="MISSING_NODE_DECLARATION",
            details={"node_id": node_id},
        )


class StateHashParityError(ContextBudgetError):
    """Raised when the aggregate's committed state_hash does not match the recomputed digest.

    This means the snapshot would be bound to stale or tampered state.
    """

    def __init__(
        self,
        aggregate_id: str,
        committed_hash: str,
        recomputed_hash: str,
    ) -> None:
        super().__init__(
            f"state_hash parity failure on aggregate '{aggregate_id}': "
            f"committed={committed_hash!r} recomputed={recomputed_hash!r}. "
            "Projection aborted fail-closed.",
            reason_code="STATE_HASH_PARITY_FAILURE",
            details={
                "aggregate_id": aggregate_id,
                "committed_hash": committed_hash,
                "recomputed_hash": recomputed_hash,
            },
        )


class LaneMaskViolationError(ContextBudgetError):
    """Raised when the requested field is masked by the active authority lane."""

    def __init__(self, field_key: str, lane: AuthorityLane) -> None:
        super().__init__(
            f"Field '{field_key}' is masked for authority lane '{lane.value}'.",
            reason_code="LANE_MASK_VIOLATION",
            details={"field_key": field_key, "lane": lane.value},
        )


# ---------------------------------------------------------------------------
# Authority-lane field masks
#
# Each lane sees only the keys listed here.  An empty set means the lane
# receives NO state_data fields (only the envelope metadata).
# Keys not in any lane's allow-list are masked from all lanes (system-only).
# ---------------------------------------------------------------------------

#: Allow-lists for each authority lane.
#: Keys that exist in state_data but are NOT in the lane's allow-list are masked.
#: Extend this mapping as new state_data schemas are defined.
LANE_FIELD_ALLOW_LISTS: Dict[AuthorityLane, FrozenSet[str]] = {
    # HUNTER discovers and ingests raw evidence; sees source-origin fields.
    AuthorityLane.HUNTER: frozenset(
        {
            "hypothesis",
            "corpus_refs",
            "source_refs",
            "guest_profile",
            "evidence_segments",
            "interview_brief",
            "node_id",
            "declared_inputs",
            "repairs",
        }
    ),
    # ANALYST evaluates signals; sees scored/evaluated fields.
    AuthorityLane.ANALYST: frozenset(
        {
            "hypothesis",
            "matrix_scores",
            "collision_candidates",
            "signals",
            "qa_scores",
            "semantic_qa",
            "transcript_refs",
            "audience_tensions",
            "node_id",
            "declared_inputs",
            "repairs",
        }
    ),
    # COMPOSER compiles and packages; sees compilation/composition fields.
    AuthorityLane.COMPOSER: frozenset(
        {
            "brief_content",
            "narrative_draft",
            "script_draft",
            "visual_demands",
            "edl_content",
            "production_plan",
            "compiled_output",
            "node_id",
            "declared_inputs",
            "repairs",
        }
    ),
    # COMMANDER governs approvals, repair, and operator decisions; sees all
    # governance-relevant fields but NOT raw lane-specific payloads.
    AuthorityLane.COMMANDER: frozenset(
        {
            "approved_by",
            "approval_timestamp",
            "rejection_reason",
            "operator_decision",
            "repair_action",
            "repairs",
            "node_id",
            "declared_inputs",
            "lifecycle_override",
            # Commanders may also inspect summary fields needed for gate decisions
            "hypothesis",
            "signals",
            "qa_scores",
        }
    ),
}


# ---------------------------------------------------------------------------
# Output type
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class PrunedContextSnapshot:
    """A pruned, lane-masked, hash-bound context snapshot for a single node.

    This is the only context object that should be delivered to a node.
    It carries exactly the declared inputs for the active node, masked by
    authority lane, and is cryptographically bound to the committed state_hash
    of the source aggregate.

    Invariant (INV-CTX-002):
        pruned_state_data ⊆ declared_inputs  ∩  lane_allow_list
        committed_state_hash == aggregate.state_hash (verified at compile time)
    """

    aggregate_id: str
    program_id: str
    node_id: str
    active_lane: AuthorityLane
    committed_state_hash: str
    snapshot_hash: str          # SHA-256 of the snapshot envelope (self-binding)
    pruned_state_data: Dict[str, Any]
    masked_keys: List[str]      # Keys that were masked (audit trail, no values)
    declared_inputs: List[str]  # Inputs declared by the node (normative source)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "aggregate_id": self.aggregate_id,
            "program_id": self.program_id,
            "node_id": self.node_id,
            "active_lane": self.active_lane.value,
            "committed_state_hash": self.committed_state_hash,
            "snapshot_hash": self.snapshot_hash,
            "pruned_state_data": self.pruned_state_data,
            "masked_keys": self.masked_keys,
            "declared_inputs": self.declared_inputs,
        }


# ---------------------------------------------------------------------------
# Core compiler
# ---------------------------------------------------------------------------

def _recompute_aggregate_state_hash(aggregate: ProgramStateAggregate) -> str:
    """Recompute the state_hash from the aggregate's fields (mirrors _compute_state_hash)."""
    from ca_contracts import canonical_sha256

    payload = {
        "aggregate_id": aggregate.aggregate_id,
        "program_id": aggregate.program_id,
        "program_version": aggregate.program_version,
        "current_state": aggregate.current_state,
        "version": aggregate.version,
        "state_data": aggregate.state_data,
    }
    return canonical_sha256(payload)


def _compute_snapshot_hash(
    aggregate_id: str,
    node_id: str,
    lane: str,
    committed_state_hash: str,
    pruned_state_data: Dict[str, Any],
) -> str:
    """Compute a deterministic snapshot hash binding the pruned context to the committed state."""
    from ca_contracts import canonical_sha256

    payload = {
        "aggregate_id": aggregate_id,
        "node_id": node_id,
        "lane": lane,
        "committed_state_hash": committed_state_hash,
        "pruned_state_data": pruned_state_data,
    }
    return canonical_sha256(payload)


def compile_jit_context_snapshot(
    *,
    aggregate: ProgramStateAggregate,
    node_id: str,
    declared_inputs: Optional[List[str]],
    active_lane: AuthorityLane,
) -> PrunedContextSnapshot:
    """Compile a pruned, lane-masked, hash-bound context snapshot.

    This is the authoritative implementation of INV-CTX-002.

    Parameters
    ----------
    aggregate:
        The source ``ProgramStateAggregate``.  Must not be modified by this function.
    node_id:
        Identity of the active node requesting context.
    declared_inputs:
        The list of state_data keys this node declared it needs.  If ``None``
        or empty and there is no lane allow-list match, the function raises
        ``MissingNodeDeclarationError`` (fail-closed).
    active_lane:
        The ``AuthorityLane`` of the requesting actor.

    Returns
    -------
    PrunedContextSnapshot
        Strictly pruned, lane-masked, hash-bound.  Only the intersection of
        declared inputs and the lane's allow-list is present.

    Raises
    ------
    MissingNodeDeclarationError
        When neither declared inputs nor lane metadata exist.
    StateHashParityError
        When the aggregate's committed state_hash does not match the recomputed
        digest, indicating stale or tampered state.
    """
    # ------------------------------------------------------------------
    # 1. Validate state_hash parity (fail-closed)
    # ------------------------------------------------------------------
    recomputed = _recompute_aggregate_state_hash(aggregate)
    if recomputed != aggregate.state_hash:
        raise StateHashParityError(
            aggregate_id=aggregate.aggregate_id,
            committed_hash=aggregate.state_hash,
            recomputed_hash=recomputed,
        )

    # ------------------------------------------------------------------
    # 2. Fail-closed if no node declaration present
    # ------------------------------------------------------------------
    effective_declared: List[str] = list(declared_inputs or [])
    if not effective_declared:
        raise MissingNodeDeclarationError(node_id=node_id)

    # ------------------------------------------------------------------
    # 3. Prune state_data to declared inputs only
    # ------------------------------------------------------------------
    declared_set: Set[str] = set(effective_declared)
    # Keys in state_data that were requested by this node
    candidate_keys: Set[str] = declared_set & set(aggregate.state_data.keys())

    # ------------------------------------------------------------------
    # 4. Apply authority-lane mask
    # ------------------------------------------------------------------
    lane_allow: FrozenSet[str] = LANE_FIELD_ALLOW_LISTS.get(active_lane, frozenset())
    allowed_keys: Set[str] = candidate_keys & lane_allow

    # Build audit trail of masked keys (no values exposed)
    masked_keys: List[str] = sorted(candidate_keys - allowed_keys)

    pruned_state_data: Dict[str, Any] = {
        k: aggregate.state_data[k] for k in sorted(allowed_keys)
    }

    # ------------------------------------------------------------------
    # 5. Compute snapshot hash (binds output to committed state_hash)
    # ------------------------------------------------------------------
    snapshot_hash = _compute_snapshot_hash(
        aggregate_id=aggregate.aggregate_id,
        node_id=node_id,
        lane=active_lane.value,
        committed_state_hash=aggregate.state_hash,
        pruned_state_data=pruned_state_data,
    )

    return PrunedContextSnapshot(
        aggregate_id=aggregate.aggregate_id,
        program_id=aggregate.program_id,
        node_id=node_id,
        active_lane=active_lane,
        committed_state_hash=aggregate.state_hash,
        snapshot_hash=snapshot_hash,
        pruned_state_data=pruned_state_data,
        masked_keys=masked_keys,
        declared_inputs=effective_declared,
    )


# ---------------------------------------------------------------------------
# Runtime-integrated helper
# ---------------------------------------------------------------------------

def get_jit_context_snapshot(
    runtime: UniversalProgramStateRuntime,
    *,
    aggregate_id: str,
    node_id: str,
    declared_inputs: Optional[List[str]],
    active_lane: AuthorityLane,
) -> PrunedContextSnapshot:
    """Resolve an aggregate and compile a JIT pruned context snapshot.

    This is the primary API callers should use.  It fetches the aggregate from
    the ``UniversalProgramStateRuntime`` and delegates to
    ``compile_jit_context_snapshot``.

    Raises the same errors as ``compile_jit_context_snapshot`` plus
    ``ProgramStateAggregateNotFoundError`` if the aggregate does not exist.
    """
    aggregate = runtime.get_aggregate(aggregate_id)
    return compile_jit_context_snapshot(
        aggregate=aggregate,
        node_id=node_id,
        declared_inputs=declared_inputs,
        active_lane=active_lane,
    )
