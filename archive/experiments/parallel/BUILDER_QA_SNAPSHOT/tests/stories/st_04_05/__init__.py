from __future__ import annotations

from datetime import timedelta

from cmf_builder.adapters.in_memory_run_repository import (
    DeterministicUuid7IdProvider,
    FixedClock,
)
from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.application.context_commands import (
    CompileMinimumContextCommand,
    MinimumContextCommandService,
)
from cmf_builder.domain.context_manifest import (
    MINIMUM_CONTEXT_INPUT_PATH,
    MINIMUM_CONTEXT_INPUT_SHA256,
)
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_04_04 import (
    build_context as build_handoff_context,
    compile_command as compile_handoff_command,
    decision_command,
    governed_artifacts,
    issue_command,
)


def build_context(*, seed: str = "ST-04.05", root=ROOT):
    handoffs, atomicity, repository, observations, run_id, _ = build_handoff_context(
        seed=f"{seed}-handoffs", root=root
    )
    handoffs.compile(compile_handoff_command(run_id))
    issued = handoffs.issue(issue_command(run_id, governed_artifacts(handoffs, repository, run_id)))
    accepted = handoffs.decide(decision_command(run_id, issued.handoff_id))
    actors = tuple(
        Actor(actor_id, kind)
        for actor_id, kind in (
            ("architect-1", ActorKind.HUMAN),
            ("code-1", ActorKind.CODE),
            ("agent-1", ActorKind.AGENT),
            ("external-1", ActorKind.EXTERNAL),
        )
    )
    grants = tuple(
        AuthorityGrant(
            actor_id=actor.actor_id,
            actions=frozenset(Action),
            resource_id="*",
            expires_at=NOW + timedelta(days=1),
        )
        for actor in actors
    )
    service = MinimumContextCommandService(
        root=root,
        repository=repository,
        authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_000_900_000,
            seed=seed,
        ),
        clock=FixedClock(NOW),
        observations=observations,
    )
    return service, handoffs, atomicity, repository, observations, run_id, accepted


def compile_command(
    run_id: str,
    *,
    command_id: str = "minimum-context-1",
    actor_id: str = "code-1",
    expected_version: int = 19,
    context_input_path: str = MINIMUM_CONTEXT_INPUT_PATH,
    context_input_sha256: str = MINIMUM_CONTEXT_INPUT_SHA256,
) -> CompileMinimumContextCommand:
    return CompileMinimumContextCommand(
        command_id=command_id,
        run_id=run_id,
        actor_id=actor_id,
        expected_version=expected_version,
        correlation_id="st-04-05-correlation-1",
        causation_id="ST-04.04:AcceptedInternalHandoff",
        context_input_path=context_input_path,
        context_input_sha256=context_input_sha256,
    )
