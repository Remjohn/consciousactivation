from __future__ import annotations

from dataclasses import replace
from datetime import timedelta
from pathlib import Path

from cmf_builder.adapters.file_declared_boundary_repository import (
    FileDeclaredBoundaryRepository,
)
from cmf_builder.adapters.in_memory_run_repository import (
    DeterministicUuid7IdProvider,
    FixedClock,
)
from cmf_builder.application.atomicity_commands import (
    AtomicityCommandService,
    DecideAtomicBoundaryCommand,
    ReopenAtomicBoundaryCommand,
)
from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.domain.atomicity import AtomicityDecision, AtomicityDecisionAction
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_01_02 import build_context as build_evidence_context
from tests.stories.st_01_02 import lock_command


def build_context(*, root: Path = ROOT, input_repository=None, seed: str = "ST-02.05"):
    evidence_service, repository, observations, _, run_id = build_evidence_context(
        root=root
    )
    source_receipt = evidence_service.lock(lock_command(run_id))
    actors = (
        Actor("architect-1", ActorKind.HUMAN),
        Actor("other-human", ActorKind.HUMAN),
        Actor("expired-1", ActorKind.HUMAN),
        Actor("code-1", ActorKind.CODE),
        Actor("agent-1", ActorKind.AGENT),
        Actor("external-1", ActorKind.EXTERNAL),
        Actor("evaluator-1", ActorKind.EVALUATOR),
    )
    grants = (
        AuthorityGrant(
            actor_id="architect-1",
            actions=frozenset(Action),
            resource_id="*",
            expires_at=NOW + timedelta(days=1),
        ),
        AuthorityGrant(
            actor_id="other-human",
            actions=frozenset(Action),
            resource_id="another-run",
            expires_at=NOW + timedelta(days=1),
        ),
        AuthorityGrant(
            actor_id="expired-1",
            actions=frozenset(Action),
            resource_id="*",
            expires_at=NOW - timedelta(seconds=1),
        ),
        *(
            AuthorityGrant(
                actor_id=actor_id,
                actions=frozenset(Action),
                resource_id="*",
                expires_at=NOW + timedelta(days=1),
            )
            for actor_id in ("code-1", "agent-1", "external-1", "evaluator-1")
        ),
    )
    service = AtomicityCommandService(
        repository=repository,
        declared_inputs=input_repository or FileDeclaredBoundaryRepository(root),
        authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_000_100_000,
            seed=seed,
        ),
        clock=FixedClock(NOW),
        observations=observations,
    )
    return service, repository, observations, run_id, source_receipt


def decision(
    action: AtomicityDecisionAction = AtomicityDecisionAction.APPROVE,
    *,
    human_id: str = "architect-1",
    **changes: object,
) -> AtomicityDecision:
    values: dict[str, object] = {
        "action": action,
        "selected_candidate": (
            "synthetic_text_normalization_atomic_definition"
            if action is AtomicityDecisionAction.APPROVE
            else None
        ),
        "rejected_alternatives": (
            "general_text_transformation_engine",
            "execute_text_normalization",
        ),
        "evidence_refs": (
            "ST-01.02:StoryCompletionReceipt",
            "source-lock:governed-synthetic-definition",
        ),
        "rationale": "The declared definition is one bounded non-executing task.",
        "accepted_risks": ("synthetic_non_production_only",),
        "human_id": human_id,
        "decided_at": NOW,
        "revision_request": (
            "Narrow the declared output invariant before approval."
            if action is AtomicityDecisionAction.REVISE
            else None
        ),
    }
    values.update(changes)
    return AtomicityDecision(**values)


def decide_command(
    run_id: str,
    *,
    command_id: str = "atomicity-decision-1",
    actor_id: str = "architect-1",
    expected_version: int = 5,
    atomicity_decision: AtomicityDecision | None = None,
    **changes: object,
) -> DecideAtomicBoundaryCommand:
    values: dict[str, object] = {
        "command_id": command_id,
        "run_id": run_id,
        "actor_id": actor_id,
        "expected_version": expected_version,
        "correlation_id": "st-02-05-correlation-1",
        "causation_id": "authorized-ST-02.05",
        "decision": atomicity_decision or decision(human_id=actor_id),
    }
    values.update(changes)
    return DecideAtomicBoundaryCommand(**values)


def reopen_command(
    run_id: str,
    *,
    command_id: str = "atomicity-reopen-1",
    actor_id: str = "architect-1",
    expected_version: int = 9,
    reason: str = "A new immutable definition version is required.",
) -> ReopenAtomicBoundaryCommand:
    return ReopenAtomicBoundaryCommand(
        command_id=command_id,
        run_id=run_id,
        actor_id=actor_id,
        expected_version=expected_version,
        correlation_id="st-02-05-reopen-correlation-1",
        causation_id="atomicity-decision-1",
        reason=reason,
    )


def changed_decision(value: AtomicityDecision, **changes: object) -> AtomicityDecision:
    return replace(value, **changes)
