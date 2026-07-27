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
from cmf_builder.application.evidence_index_commands import (
    EvidenceIndexCommandService,
    IndexEvidenceCommand,
    InvalidateEvidenceIndexCommand,
)
from tests.stories.st_01_01_synthetic_proof import NOW
from tests.stories.st_01_02 import build_context as build_source_context, lock_command


def build_context(*, seed: str = "ST-01.03", observations=None):
    source_service, repository, _, _, run_id = build_source_context()
    source_receipt = source_service.lock(lock_command(run_id))
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
    service = EvidenceIndexCommandService(
        repository=repository,
        authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_100_000_000,
            seed=seed,
        ),
        clock=FixedClock(NOW),
        observations=sink,
    )
    return service, repository, sink, run_id, source_receipt


def index_command(
    run_id: str,
    *,
    command_id: str = "evidence-index-command-1",
    actor_id: str = "code-1",
    expected_version: int = 5,
    **changes: object,
) -> IndexEvidenceCommand:
    values: dict[str, object] = {
        "command_id": command_id,
        "run_id": run_id,
        "actor_id": actor_id,
        "expected_version": expected_version,
        "correlation_id": "st-01-03-correlation-1",
        "causation_id": "ST-01.02:StoryCompletionReceipt",
    }
    values.update(changes)
    return IndexEvidenceCommand(**values)


def invalidation_command(
    run_id: str,
    index_id: str,
    *,
    command_id: str = "evidence-index-invalidation-1",
    expected_version: int = 6,
) -> InvalidateEvidenceIndexCommand:
    return InvalidateEvidenceIndexCommand(
        command_id=command_id,
        run_id=run_id,
        actor_id="code-1",
        expected_version=expected_version,
        correlation_id="st-01-03-correlation-1",
        causation_id="upstream-source-lock-change",
        index_id=index_id,
        reason="governed upstream Source Lock replacement requires a new index",
    )
