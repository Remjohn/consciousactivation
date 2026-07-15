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
from cmf_builder.application.skill_commands import (
    RunSkillNecessityTestCommand,
    SyntheticSkillNecessityCommandService,
)
from cmf_builder.domain.skill_registry import (
    SKILL_NECESSITY_INPUT_PATH,
    SKILL_NECESSITY_INPUT_SHA256,
)
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_05_01 import (
    build_context as build_skill_registry_context,
    compile_command as compile_skill_registry,
)


def build_context(*, seed: str = "ST-05.02", root=ROOT):
    registry_service, atomicity, repository, observations, run_id, _, context_receipt = (
        build_skill_registry_context(seed=f"{seed}-registry", root=root)
    )
    registry_receipt = registry_service.compile(compile_skill_registry(run_id))
    snapshot = registry_service.get_active(run_id)
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
    service = SyntheticSkillNecessityCommandService(
        root=root,
        repository=repository,
        authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_002_000_000,
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
        context_receipt,
        registry_receipt,
        snapshot,
    )


def evaluate_command(
    run_id: str,
    snapshot_id: str,
    snapshot_hash: str,
    *,
    command_id: str = "synthetic-skill-necessity-1",
    actor_id: str = "code-1",
    expected_version: int = 21,
    necessity_input_path: str = SKILL_NECESSITY_INPUT_PATH,
    necessity_input_sha256: str = SKILL_NECESSITY_INPUT_SHA256,
    requested_operation: str = "evaluate_skill_necessity",
    capability_evidence_overrides: tuple[tuple[str, str, str], ...] = (),
    declared_skill_ids: tuple[str, ...] = (),
    requested_skill_artifacts: tuple[str, ...] = (),
    human_authority_receipt_id: str | None = None,
) -> RunSkillNecessityTestCommand:
    return RunSkillNecessityTestCommand(
        command_id=command_id,
        run_id=run_id,
        actor_id=actor_id,
        expected_version=expected_version,
        correlation_id="st-05-02-correlation-1",
        causation_id="ST-05.01:StoryCompletionReceipt",
        snapshot_id=snapshot_id,
        snapshot_hash=snapshot_hash,
        necessity_input_path=necessity_input_path,
        necessity_input_sha256=necessity_input_sha256,
        requested_operation=requested_operation,
        capability_evidence_overrides=capability_evidence_overrides,
        declared_skill_ids=declared_skill_ids,
        requested_skill_artifacts=requested_skill_artifacts,
        human_authority_receipt_id=human_authority_receipt_id,
    )
