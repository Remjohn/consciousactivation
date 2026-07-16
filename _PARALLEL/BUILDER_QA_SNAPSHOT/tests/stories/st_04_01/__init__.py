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
from cmf_builder.application.capability_commands import (
    CapabilityCommandService,
    CompileCapabilityOwnershipCommand,
)
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_03_05 import build_context as build_constitutional_context
from tests.stories.st_03_05 import validate_command


def build_context(*, seed: str = "ST-04.01", root=ROOT):
    constitutional, atomicity, repository, observations, run_id, _ = (
        build_constitutional_context(seed=f"{seed}-constitutional", root=root)
    )
    constitutional_receipt = constitutional.validate(validate_command(run_id))
    actors = tuple(
        Actor(actor_id, kind)
        for actor_id, kind in (
            ("architect-1", ActorKind.HUMAN),
            ("code-1", ActorKind.CODE),
            ("agent-1", ActorKind.AGENT),
            ("external-1", ActorKind.EXTERNAL),
            ("evaluator-1", ActorKind.EVALUATOR),
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
    service = CapabilityCommandService(
        root=root,
        repository=repository,
        authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_000_500_000,
            seed=seed,
        ),
        clock=FixedClock(NOW),
        observations=observations,
    )
    return (
        service,
        atomicity,
        repository,
        observations,
        run_id,
        constitutional_receipt,
    )


def compile_command(
    run_id: str,
    *,
    command_id: str = "capability-ownership-1",
    actor_id: str = "code-1",
    expected_version: int = 13,
    ownership_input_path: str | None = None,
    ownership_input_sha256: str | None = None,
) -> CompileCapabilityOwnershipCommand:
    values: dict[str, object] = {
        "command_id": command_id,
        "run_id": run_id,
        "actor_id": actor_id,
        "expected_version": expected_version,
        "correlation_id": "st-04-01-correlation-1",
        "causation_id": "ST-03.05:StoryCompletionReceipt",
    }
    if ownership_input_path is not None:
        values["ownership_input_path"] = ownership_input_path
    if ownership_input_sha256 is not None:
        values["ownership_input_sha256"] = ownership_input_sha256
    return CompileCapabilityOwnershipCommand(**values)
