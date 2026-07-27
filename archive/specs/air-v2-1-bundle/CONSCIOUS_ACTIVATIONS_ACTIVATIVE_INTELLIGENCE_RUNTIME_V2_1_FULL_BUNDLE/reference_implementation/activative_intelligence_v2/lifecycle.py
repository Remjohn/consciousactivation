from __future__ import annotations

from dataclasses import dataclass

from .models import LifecycleState


_ALLOWED: dict[LifecycleState, frozenset[LifecycleState]] = {
    LifecycleState.CONTEXT_LOCKED: frozenset({LifecycleState.HYPOTHESES_COMPILED, LifecycleState.CANCELLED}),
    LifecycleState.HYPOTHESES_COMPILED: frozenset({LifecycleState.PLANNED, LifecycleState.CANCELLED}),
    LifecycleState.PLANNED: frozenset({LifecycleState.ARMED, LifecycleState.CANCELLED}),
    LifecycleState.ARMED: frozenset({LifecycleState.LIVE, LifecycleState.CANCELLED}),
    LifecycleState.LIVE: frozenset({LifecycleState.OBSERVED, LifecycleState.CANCELLED}),
    LifecycleState.OBSERVED: frozenset({LifecycleState.RESOLVED}),
    LifecycleState.RESOLVED: frozenset({LifecycleState.SOURCE_PACKAGED, LifecycleState.CANCELLED}),
    LifecycleState.SOURCE_PACKAGED: frozenset({LifecycleState.TRANSFERRED}),
    LifecycleState.TRANSFERRED: frozenset({LifecycleState.PRODUCED}),
    LifecycleState.PRODUCED: frozenset({LifecycleState.PUBLISHED, LifecycleState.EVALUATED}),
    LifecycleState.PUBLISHED: frozenset({LifecycleState.EVALUATED}),
    LifecycleState.EVALUATED: frozenset({LifecycleState.LEARNED, LifecycleState.SUPERSEDED}),
    LifecycleState.LEARNED: frozenset({LifecycleState.SUPERSEDED}),
    LifecycleState.SUPERSEDED: frozenset(),
    LifecycleState.CANCELLED: frozenset(),
}


class InvalidLifecycleTransition(ValueError):
    pass


def may_transition(current: LifecycleState, target: LifecycleState) -> bool:
    return target in _ALLOWED[current]


def require_transition(current: LifecycleState, target: LifecycleState) -> None:
    if not may_transition(current, target):
        raise InvalidLifecycleTransition(f"invalid transition: {current.value} -> {target.value}")


@dataclass(frozen=True, slots=True)
class TransitionReceipt:
    object_id: str
    from_state: LifecycleState
    to_state: LifecycleState
    reason: str

    def validate(self) -> "TransitionReceipt":
        require_transition(self.from_state, self.to_state)
        if not self.reason.strip():
            raise ValueError("transition reason is required")
        return self
