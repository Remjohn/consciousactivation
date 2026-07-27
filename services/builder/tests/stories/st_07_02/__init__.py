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
from cmf_builder.application.definition_commands import (
    CompileAtomicHarnessDefinitionCommand,
    SyntheticAtomicHarnessDefinitionCommandService,
)
from cmf_builder.domain.atomic_harness_definition import (
    CATEGORY_ADAPTER_REF,
    DEFINITION_INPUT_PATH,
    DEFINITION_INPUT_SHA256,
    PROFILE_ID,
    REQUIRED_SECTIONS,
    TARGET_KIND,
)
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_05_02 import (
    build_context as build_skill_necessity_context,
    evaluate_command,
)


def build_context(*, seed: str = "ST-07.02", root=ROOT):
    (
        necessity_service,
        atomicity,
        repository,
        observations,
        run_id,
        _,
        _,
        snapshot,
    ) = build_skill_necessity_context(seed=f"{seed}-necessity", root=root)
    necessity_receipt = necessity_service.evaluate(
        evaluate_command(run_id, snapshot.snapshot_id, snapshot.snapshot_hash)
    )
    necessity = necessity_service.get_active(run_id)
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
    service = SyntheticAtomicHarnessDefinitionCommandService(
        root=root,
        repository=repository,
        authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_004_000_000,
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
        necessity_receipt,
        necessity,
        snapshot,
    )


def compile_command(
    run_id: str,
    *,
    command_id: str = "synthetic-atomic-harness-definition-1",
    actor_id: str = "code-1",
    expected_version: int = 22,
    definition_input_path: str = DEFINITION_INPUT_PATH,
    definition_input_sha256: str = DEFINITION_INPUT_SHA256,
    requested_operation: str = "compile_atomic_harness_definition",
    requested_target_kind: str = TARGET_KIND,
    requested_profile_id: str = PROFILE_ID,
    requested_category_adapter_ref: str = CATEGORY_ADAPTER_REF,
    requested_required_sections: tuple[str, ...] = REQUIRED_SECTIONS,
    requested_external_runtime_ids: tuple[str, ...] = (),
    requested_external_skill_ids: tuple[str, ...] = (),
    requested_production_eligible: bool = False,
    requested_certified: bool = False,
    requested_synthetic_not_certifiable: bool = True,
    lineage_overrides: tuple[tuple[str, str], ...] = (),
) -> CompileAtomicHarnessDefinitionCommand:
    return CompileAtomicHarnessDefinitionCommand(
        command_id=command_id,
        run_id=run_id,
        actor_id=actor_id,
        expected_version=expected_version,
        correlation_id="st-07-02-correlation-1",
        causation_id="ST-05.02:StoryCompletionReceipt",
        definition_input_path=definition_input_path,
        definition_input_sha256=definition_input_sha256,
        requested_operation=requested_operation,
        requested_target_kind=requested_target_kind,
        requested_profile_id=requested_profile_id,
        requested_category_adapter_ref=requested_category_adapter_ref,
        requested_required_sections=requested_required_sections,
        requested_external_runtime_ids=requested_external_runtime_ids,
        requested_external_skill_ids=requested_external_skill_ids,
        requested_production_eligible=requested_production_eligible,
        requested_certified=requested_certified,
        requested_synthetic_not_certifiable=requested_synthetic_not_certifiable,
        lineage_overrides=lineage_overrides,
    )
