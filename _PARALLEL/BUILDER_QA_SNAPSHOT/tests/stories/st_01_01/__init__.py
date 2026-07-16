from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from cmf_builder.adapters.file_target_profile_repository import (
    FileTargetProfileRepository,
)
from cmf_builder.adapters.in_memory_run_repository import (
    DeterministicUuid7IdProvider,
    FixedClock,
    InMemoryRunRepository,
    RecordingObservationSink,
)
from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.application.run_commands import CreateRunCommand, RunCommandService


ROOT = Path(__file__).resolve().parents[3]
NOW = datetime(2026, 7, 15, 12, 0, tzinfo=timezone.utc)
TARGET_ID = "atomic_content_harness"
CATEGORY_ID = "2d_character_animation"
PROFILE_ID = "format02_minimal_coach_theatre"


def build_service(*, agent_granted: bool = False):
    repository = InMemoryRunRepository()
    observations = RecordingObservationSink()
    clock = FixedClock(NOW)
    ids = DeterministicUuid7IdProvider(
        timestamp_ms=1_768_000_000_000,
        seed="ST-01.01",
    )
    actions = frozenset(Action)
    actors = (
        Actor("architect-1", ActorKind.HUMAN),
        Actor("agent-1", ActorKind.AGENT),
        Actor("code-1", ActorKind.CODE),
    )
    grants = [
        AuthorityGrant(
            actor_id="architect-1",
            actions=actions,
            resource_id="*",
            expires_at=NOW + timedelta(days=1),
        )
    ]
    if agent_granted:
        grants.append(
            AuthorityGrant(
                actor_id="agent-1",
                actions=actions,
                resource_id="*",
                expires_at=NOW + timedelta(days=1),
            )
        )
    authority = AuthorityService(actors=actors, grants=tuple(grants))
    profiles = FileTargetProfileRepository(ROOT)
    service = RunCommandService(
        repository=repository,
        profiles=profiles,
        authority=authority,
        ids=ids,
        clock=clock,
        observations=observations,
    )
    return service, repository, observations, clock, profiles


def create_command(
    *,
    command_id: str = "command-create-1",
    actor_id: str = "architect-1",
    target_ids: tuple[str, ...] = (TARGET_ID,),
    category_id: str = CATEGORY_ID,
    profile_id: str = PROFILE_ID,
) -> CreateRunCommand:
    return CreateRunCommand(
        command_id=command_id,
        target_ids=target_ids,
        category_id=category_id,
        profile_id=profile_id,
        compiler_version="builder-v1.2",
        actor_id=actor_id,
        correlation_id="correlation-1",
        causation_id="human-authorization-ST-01.01",
    )
