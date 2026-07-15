from __future__ import annotations

from datetime import timedelta

from cmf_builder.adapters.in_memory_run_repository import (
    DeterministicUuid7IdProvider,
    FixedClock,
)
from cmf_builder.application.artifact_commands import (
    ArtifactCommandService,
    CompileArtifactSetCommand,
)
from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.domain.generated_artifacts import ReproducibleBuildConfig
from tests.stories.st_01_01_synthetic_proof import NOW
from tests.stories.st_03_03 import build_context as build_ir_context
from tests.stories.st_03_03 import compile_command as compile_ir_command


BUILD_CONFIG = ReproducibleBuildConfig(
    compiler_id="cmf-builder/deterministic-artifact-compiler",
    compiler_version="1.0.0",
    config_version="1.0.0",
    generation_timestamp="2026-01-10T12:00:00Z",
)


def build_context(*, seed: str = "ST-03.04"):
    ir_service, atomicity, repository, observations, run_id, approval = build_ir_context(
        seed=f"{seed}-ir"
    )
    ir_receipt = ir_service.compile(compile_ir_command(run_id))
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
    service = ArtifactCommandService(
        repository=repository,
        authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_000_300_000,
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
        approval,
        ir_receipt,
    )


def compile_command(
    run_id: str,
    *,
    command_id: str = "artifact-set-compile-1",
    actor_id: str = "code-1",
    expected_version: int = 11,
    build_config: ReproducibleBuildConfig = BUILD_CONFIG,
) -> CompileArtifactSetCommand:
    return CompileArtifactSetCommand(
        command_id=command_id,
        run_id=run_id,
        actor_id=actor_id,
        expected_version=expected_version,
        correlation_id="st-03-04-correlation-1",
        causation_id="ST-03.03:StoryCompletionReceipt",
        build_config=build_config,
    )

