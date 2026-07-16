from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from shutil import copy2

from cmf_builder.adapters import (
    SYNTHETIC_CATEGORY_ID,
    SYNTHETIC_PROFILE_ID,
    SyntheticProofTargetProfileRepository,
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
NOW = datetime(2026, 7, 15, 14, 0, tzinfo=timezone.utc)
TARGET_ID = "atomic_content_harness"
PROFILE_ID = SYNTHETIC_PROFILE_ID
CATEGORY_ID = SYNTHETIC_CATEGORY_ID
PROFILE_FIXTURE_SHA256 = (
    "82f86a94e1183ee3d475277734b03eb5f2ab3d2bb7afe0520b8828105917337b"
)
EMPTY_REGISTRY_SHA256 = (
    "a4a9e5afaf91f60b22529ec01f1bc8e22a0d895444ad9a9e9a96e7a3e7b28114"
)


def build_service(*, root: Path = ROOT, agent_granted: bool = False):
    repository = InMemoryRunRepository()
    observations = RecordingObservationSink()
    clock = FixedClock(NOW)
    ids = DeterministicUuid7IdProvider(
        timestamp_ms=1_768_000_000_000,
        seed="ST-01.01-SYNTHETIC-PROOF",
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
    profiles = SyntheticProofTargetProfileRepository(root)
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
    command_id: str = "synthetic-create-1",
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
        compiler_version="builder-v1.2-synthetic-proof",
        actor_id=actor_id,
        correlation_id="synthetic-proof-correlation-1",
        causation_id="human-authorization-ST-01.01-SYNTHETIC-PROOF",
    )


def copy_governed_inputs(destination_root: Path) -> None:
    relative_paths = (
        Path(
            "development-capsules/ST-01.01-SYNTHETIC-PROOF/"
            "SYNTHETIC_TARGET_PROFILE_FIXTURE.yaml"
        ),
        Path("governance/EMPTY_SKILL_REGISTRY_POLICY.yaml"),
        Path("governance/fixtures/synthetic-core/empty-skill-registry.yaml"),
        Path("governance/schemas/empty-skill-registry.schema.json"),
    )
    for relative in relative_paths:
        target = destination_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(ROOT / relative, target)
