from __future__ import annotations

from datetime import timedelta

from cmf_builder.adapters.in_memory_run_repository import FixedClock
from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.application.implementation_plan_commands import (
    CompileImplementationPlanCommand,
    ImplementationPlanCommandService,
)
from cmf_builder.domain.implementation_plan import (
    DIRECT_DEPENDENCIES,
    EXTERNAL_TARGET_COMPATIBILITY,
    OWNED_OBLIGATIONS,
    PLAN_INPUT_PATH,
    PLAN_INPUT_SHA256,
    PLAN_MODE,
    PLAN_PROFILE_ID,
)
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_11_01 import build_context as build_capsule_context
from tests.stories.st_11_01 import capsule_command


def build_context(*, seed: str = "ST-11.02", root=ROOT):
    (
        capsule_service,
        _,
        atomicity,
        repository,
        observations,
        run_id,
        _,
        _,
        _,
    ) = build_capsule_context(seed=f"{seed}-capsule", root=root)
    capsule_receipt = capsule_service.generate(capsule_command(run_id))
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
    service = ImplementationPlanCommandService(
        root=root,
        repository=repository,
        authority=AuthorityService(actors=actors, grants=grants),
        clock=FixedClock(NOW),
        observations=observations,
    )
    return (
        service,
        capsule_service,
        atomicity,
        repository,
        observations,
        run_id,
        capsule_receipt,
        capsule_service.get_active(run_id),
    )


def plan_command(
    run_id: str,
    *,
    command_id: str = "synthetic-vertical-plan-1",
    actor_id: str = "code-1",
    expected_version: int = 25,
    plan_input_path: str = PLAN_INPUT_PATH,
    plan_input_sha256: str = PLAN_INPUT_SHA256,
    requested_operation: str = "compile_dependency_ordered_vertical_plan",
    requested_mode: str = PLAN_MODE,
    requested_profile_id: str = PLAN_PROFILE_ID,
    requested_obligations: tuple[str, ...] = OWNED_OBLIGATIONS,
    requested_dependencies: tuple[str, ...] = DIRECT_DEPENDENCIES,
    requested_external_target_compatibility: str = EXTERNAL_TARGET_COMPATIBILITY,
    requested_implementation_authorized: bool = False,
    requested_production_eligible: bool = False,
    requested_certified: bool = False,
    requested_external_runtime_ids: tuple[str, ...] = (),
    requested_external_skill_ids: tuple[str, ...] = (),
    requested_increment_overrides: tuple[tuple[str, str], ...] = (),
) -> CompileImplementationPlanCommand:
    return CompileImplementationPlanCommand(
        command_id=command_id,
        run_id=run_id,
        actor_id=actor_id,
        expected_version=expected_version,
        correlation_id="st-11-02-correlation-1",
        causation_id="ST-11.01:StoryCompletionReceipt",
        plan_input_path=plan_input_path,
        plan_input_sha256=plan_input_sha256,
        requested_operation=requested_operation,
        requested_mode=requested_mode,
        requested_profile_id=requested_profile_id,
        requested_obligations=requested_obligations,
        requested_dependencies=requested_dependencies,
        requested_external_target_compatibility=requested_external_target_compatibility,
        requested_implementation_authorized=requested_implementation_authorized,
        requested_production_eligible=requested_production_eligible,
        requested_certified=requested_certified,
        requested_external_runtime_ids=requested_external_runtime_ids,
        requested_external_skill_ids=requested_external_skill_ids,
        requested_increment_overrides=requested_increment_overrides,
    )

