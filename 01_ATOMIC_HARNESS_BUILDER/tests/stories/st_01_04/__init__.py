from __future__ import annotations

from datetime import timedelta

from cmf_builder.adapters.in_memory_run_repository import (
    DeterministicUuid7IdProvider,
    FixedClock,
    RecordingObservationSink,
)
from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.application.evidence_saturation_commands import (
    EvaluateSaturationCommand,
    InvalidateSaturationCommand,
    SaturationCommandService,
)
from cmf_builder.domain.evidence_saturation import SaturationContract
from tests.stories.st_01_01_synthetic_proof import NOW
from tests.stories.st_01_03 import build_context as build_index_context, index_command


def build_context(*, seed: str = "ST-01.04", observations=None):
    index_service, repository, _, run_id, source_receipt = build_index_context()
    index_receipt = index_service.index(index_command(run_id))
    actors = (
        Actor("code-1", ActorKind.CODE),
        Actor("architect-1", ActorKind.HUMAN),
        Actor("agent-1", ActorKind.AGENT),
        Actor("external-1", ActorKind.EXTERNAL),
        Actor("expired-code", ActorKind.CODE),
    )
    grants = tuple(
        AuthorityGrant(
            actor_id=actor.actor_id,
            actions=frozenset(Action),
            resource_id="*",
            expires_at=(
                NOW - timedelta(seconds=1)
                if actor.actor_id == "expired-code"
                else NOW + timedelta(days=1)
            ),
        )
        for actor in actors
    )
    sink = observations or RecordingObservationSink()
    service = SaturationCommandService(
        repository=repository,
        authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_200_000_000,
            seed=seed,
        ),
        clock=FixedClock(NOW),
        observations=sink,
    )
    lock = repository.get_source_lock(source_receipt.source_lock_ref)
    assert lock is not None
    contract = SaturationContract.create(
        contract_id="synthetic_category_neutral_saturation_v1",
        source_profile_ref=lock.source_profile_ref,
        required_roles=("governed_task_definition",),
    )
    return service, repository, sink, run_id, source_receipt, index_receipt, contract


def evaluation_command(
    run_id: str,
    contract: SaturationContract,
    *,
    command_id: str = "saturation-command-1",
    actor_id: str = "code-1",
    expected_version: int = 6,
    **changes: object,
) -> EvaluateSaturationCommand:
    values: dict[str, object] = {
        "command_id": command_id,
        "run_id": run_id,
        "actor_id": actor_id,
        "expected_version": expected_version,
        "correlation_id": "st-01-04-correlation-1",
        "causation_id": "ST-01.03:StoryCompletionReceipt",
        "contract": contract,
    }
    values.update(changes)
    return EvaluateSaturationCommand(**values)


def invalidation_command(
    run_id: str,
    evaluation_id: str,
    *,
    command_id: str = "saturation-invalidation-1",
    expected_version: int = 7,
) -> InvalidateSaturationCommand:
    return InvalidateSaturationCommand(
        command_id=command_id,
        run_id=run_id,
        actor_id="code-1",
        expected_version=expected_version,
        correlation_id="st-01-04-correlation-1",
        causation_id="upstream-evidence-index-change",
        evaluation_id=evaluation_id,
        reason="governed upstream evidence change requires a new evaluation",
    )
