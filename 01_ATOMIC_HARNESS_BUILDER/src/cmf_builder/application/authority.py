from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ActorKind(str, Enum):
    HUMAN = "HUMAN"
    AGENT = "AGENT"
    CODE = "CODE"
    EXTERNAL = "EXTERNAL"
    EVALUATOR = "EVALUATOR"


class Action(str, Enum):
    CREATE_RUN = "CREATE_RUN"
    LOCK_EVIDENCE_WORKSPACE = "LOCK_EVIDENCE_WORKSPACE"
    INDEX_EVIDENCE = "INDEX_EVIDENCE"
    EVALUATE_SATURATION = "EVALUATE_SATURATION"
    OPEN_GENESIS_QUESTION = "OPEN_GENESIS_QUESTION"
    RATIFY_GENESIS_DECISION = "RATIFY_GENESIS_DECISION"
    REOPEN_GENESIS_DECISION = "REOPEN_GENESIS_DECISION"
    TRANSITION_RUN = "TRANSITION_RUN"
    GRANT_WAIVER = "GRANT_WAIVER"
    CREATE_CHECKPOINT = "CREATE_CHECKPOINT"
    RESUME_RUN = "RESUME_RUN"
    RATIFY_ATOMIC_BOUNDARY = "RATIFY_ATOMIC_BOUNDARY"
    REVISE_ATOMIC_BOUNDARY = "REVISE_ATOMIC_BOUNDARY"
    REJECT_ATOMIC_BOUNDARY = "REJECT_ATOMIC_BOUNDARY"
    REOPEN_ATOMIC_BOUNDARY = "REOPEN_ATOMIC_BOUNDARY"
    BIND_HARNESS_CATEGORY = "BIND_HARNESS_CATEGORY"
    COMPILE_CATEGORY_PROFILES = "COMPILE_CATEGORY_PROFILES"


HUMAN_ONLY_ACTIONS = frozenset(
    {
        Action.GRANT_WAIVER,
        Action.RATIFY_ATOMIC_BOUNDARY,
        Action.REVISE_ATOMIC_BOUNDARY,
        Action.REJECT_ATOMIC_BOUNDARY,
        Action.REOPEN_ATOMIC_BOUNDARY,
        Action.RATIFY_GENESIS_DECISION,
        Action.REOPEN_GENESIS_DECISION,
    }
)


class AuthorityDenied(Exception):
    code = "AuthorityDenied"

    def __init__(self, message: str, **context: object) -> None:
        super().__init__(message)
        self.context = dict(context)


@dataclass(frozen=True, slots=True)
class Actor:
    actor_id: str
    kind: ActorKind


@dataclass(frozen=True, slots=True)
class AuthorityGrant:
    actor_id: str
    actions: frozenset[Action]
    resource_id: str
    expires_at: datetime


class AuthorityService:
    def __init__(
        self,
        *,
        actors: tuple[Actor, ...],
        grants: tuple[AuthorityGrant, ...],
    ) -> None:
        self._actors = {actor.actor_id: actor for actor in actors}
        self._grants = grants

    def authorize(
        self,
        *,
        actor_id: str,
        action: Action,
        resource_id: str,
        now: datetime,
    ) -> Actor:
        actor = self._actors.get(actor_id)
        if actor is None:
            raise AuthorityDenied(
                "Actor identity is not registered.", actor_id=actor_id, action=action.value
            )
        if actor.kind in {ActorKind.AGENT, ActorKind.EXTERNAL, ActorKind.EVALUATOR}:
            raise AuthorityDenied(
                "This actor kind may not commit governed run state.",
                actor_id=actor_id,
                actor_kind=actor.kind.value,
                action=action.value,
            )
        if action in HUMAN_ONLY_ACTIONS and actor.kind is not ActorKind.HUMAN:
            raise AuthorityDenied(
                "Only a human authority may perform this governed decision.",
                actor_id=actor_id,
                actor_kind=actor.kind.value,
                action=action.value,
            )
        matching = tuple(
            grant
            for grant in self._grants
            if grant.actor_id == actor_id
            and action in grant.actions
            and grant.resource_id in {"*", resource_id}
            and grant.expires_at > now
        )
        if not matching:
            raise AuthorityDenied(
                "No active exact authority grant covers this action and resource.",
                actor_id=actor_id,
                action=action.value,
                resource_id=resource_id,
            )
        return actor
