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
from cmf_builder.application.module_commands import (
    CompileResponsibilityModulesCommand,
    ResponsibilityModuleCommandService,
)
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_04_01 import build_context as build_capability_context
from tests.stories.st_04_01 import compile_command as compile_capability_command


def build_context(*, seed: str = "ST-04.02", root=ROOT):
    capability, atomicity, repository, observations, run_id, _ = (
        build_capability_context(seed=f"{seed}-capability", root=root)
    )
    capability_receipt = capability.compile(compile_capability_command(run_id))
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
    service = ResponsibilityModuleCommandService(
        root=root,
        repository=repository,
        authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_000_600_000,
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
        capability_receipt,
    )


def compile_command(
    run_id: str,
    *,
    command_id: str = "responsibility-modules-1",
    actor_id: str = "code-1",
    expected_version: int = 14,
    module_input_path: str | None = None,
    module_input_sha256: str | None = None,
) -> CompileResponsibilityModulesCommand:
    values: dict[str, object] = {
        "command_id": command_id,
        "run_id": run_id,
        "actor_id": actor_id,
        "expected_version": expected_version,
        "correlation_id": "st-04-02-correlation-1",
        "causation_id": "ST-04.01:StoryCompletionReceipt",
    }
    if module_input_path is not None:
        values["module_input_path"] = module_input_path
    if module_input_sha256 is not None:
        values["module_input_sha256"] = module_input_sha256
    return CompileResponsibilityModulesCommand(**values)
