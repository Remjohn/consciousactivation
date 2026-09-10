"""
asset_demand_resolution.py
---------------------------
Runtime-neutral lifecycle validation for the CAE-M061 asset demand boundary.

The runtime owns state-transition validity only. It does not infer semantic
meaning, select assets, or reinterpret Program obligations.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AssetDemandLifecycleState(str, Enum):
    PROGRAM_NEEDS_ASSET = "PROGRAM_NEEDS_ASSET"
    DEMAND_EMITTED = "DEMAND_EMITTED"
    RESOLUTION_PENDING = "RESOLUTION_PENDING"
    SATISFIED = "SATISFIED"
    BLOCKED = "BLOCKED"


_ALLOWED_TRANSITIONS: dict[AssetDemandLifecycleState, frozenset[AssetDemandLifecycleState]] = {
    AssetDemandLifecycleState.PROGRAM_NEEDS_ASSET: frozenset(
        {AssetDemandLifecycleState.DEMAND_EMITTED}
    ),
    AssetDemandLifecycleState.DEMAND_EMITTED: frozenset(
        {
            AssetDemandLifecycleState.RESOLUTION_PENDING,
            AssetDemandLifecycleState.SATISFIED,
            AssetDemandLifecycleState.BLOCKED,
        }
    ),
    AssetDemandLifecycleState.RESOLUTION_PENDING: frozenset(
        {AssetDemandLifecycleState.SATISFIED, AssetDemandLifecycleState.BLOCKED}
    ),
    AssetDemandLifecycleState.SATISFIED: frozenset(),
    AssetDemandLifecycleState.BLOCKED: frozenset(),
}


class AssetDemandStateError(ValueError):
    """Raised when a demand lifecycle transition is not governed."""


@dataclass(frozen=True)
class AssetDemandStateTransition:
    actor: str
    source: AssetDemandLifecycleState
    target: AssetDemandLifecycleState
    preconditions: tuple[str, ...]
    validator: str
    postconditions: tuple[str, ...]
    receipt_ref: str
    error_route: str
    recovery_route: str
    validation: str


def validate_asset_demand_transition(
    *,
    actor: str,
    source: AssetDemandLifecycleState | str,
    target: AssetDemandLifecycleState | str,
    receipt_ref: str,
) -> AssetDemandStateTransition:
    """Validate only the declared lifecycle transition.

    `actor` and `receipt_ref` are audit data; semantic interpretation remains
    upstream in the Program and demand contract.
    """
    if not actor.strip():
        raise AssetDemandStateError("actor is required")
    if not receipt_ref.strip():
        raise AssetDemandStateError("receipt_ref is required")
    source_state = AssetDemandLifecycleState(source)
    target_state = AssetDemandLifecycleState(target)
    if target_state not in _ALLOWED_TRANSITIONS[source_state]:
        raise AssetDemandStateError(
            f"Invalid asset demand transition: {source_state.value} -> {target_state.value}"
        )
    return AssetDemandStateTransition(
        actor=actor,
        source=source_state,
        target=target_state,
        preconditions=("source_state_matches_current_contract", "target_state_is_declared"),
        validator="validate_asset_demand_transition",
        postconditions=("target_state_is_recorded", "semantic_obligation_is_unchanged"),
        receipt_ref=receipt_ref,
        error_route="REJECT_TRANSITION_WITH_ASSET_DEMAND_STATE_ERROR",
        recovery_route="RETAIN_SOURCE_STATE_AND_REPAIR_OR_REEMIT_DECLARED_TRANSITION",
        validation="LIFECYCLE_ONLY; SEMANTIC_AUTHORITY_REMAINS_WITH_PROGRAM",
    )
