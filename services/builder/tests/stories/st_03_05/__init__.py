from __future__ import annotations

from datetime import timedelta

from cmf_builder.adapters.file_constitutional_policy_repository import (
    FileConstitutionalPolicyRepository,
)
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
from cmf_builder.application.constitutional_commands import (
    ConstitutionalCommandService,
    ValidateConstitutionalPrecedenceCommand,
)
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_03_04 import build_context as build_artifact_context
from tests.stories.st_03_04 import compile_command as compile_artifact_command


def build_context(*, seed: str = "ST-03.05", root=ROOT):
    artifact_service, atomicity, repository, observations, run_id, _, _ = (
        build_artifact_context(seed=f"{seed}-artifacts")
    )
    artifact_receipt = artifact_service.compile(compile_artifact_command(run_id))
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
    service = ConstitutionalCommandService(
        repository=repository,
        policies=FileConstitutionalPolicyRepository(root),
        authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_000_400_000,
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
        artifact_receipt,
    )


def validate_command(
    run_id: str,
    *,
    command_id: str = "constitutional-validation-1",
    actor_id: str = "code-1",
    expected_version: int = 12,
    policy_path: str | None = None,
    policy_sha256: str | None = None,
) -> ValidateConstitutionalPrecedenceCommand:
    values: dict[str, object] = {
        "command_id": command_id,
        "run_id": run_id,
        "actor_id": actor_id,
        "expected_version": expected_version,
        "correlation_id": "st-03-05-correlation-1",
        "causation_id": "ST-03.04:StoryCompletionReceipt",
    }
    if policy_path is not None:
        values["policy_path"] = policy_path
    if policy_sha256 is not None:
        values["policy_sha256"] = policy_sha256
    return ValidateConstitutionalPrecedenceCommand(**values)
