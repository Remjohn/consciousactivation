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
from cmf_builder.application.development_capsule_commands import (
    DevelopmentCapsuleCommandService,
    GenerateDevelopmentCapsuleCommand,
)
from cmf_builder.domain.development_capsule import (
    CAPSULE_INPUT_PATH,
    CAPSULE_INPUT_SHA256,
    CAPSULE_MODE,
    CAPSULE_PROFILE_ID,
    DIRECT_DEPENDENCIES,
    OWNED_OBLIGATIONS,
    REQUIRED_CAPSULE_SECTIONS,
)
from cmf_builder.domain.target_package_validation import (
    EXTERNAL_TARGET_COMPATIBILITY,
)
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_07_04 import build_context as build_validation_context
from tests.stories.st_07_04 import validation_command


def build_context(*, seed: str = "ST-11.01", root=ROOT):
    (
        validation_service,
        _,
        atomicity,
        repository,
        observations,
        run_id,
        _,
        definition,
    ) = build_validation_context(seed=f"{seed}-validation", root=root)
    validation_receipt = validation_service.validate(validation_command(run_id))
    validation = validation_service.get_active(run_id)
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
    service = DevelopmentCapsuleCommandService(
        root=root,
        repository=repository,
        authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_008_000_000,
            seed=seed,
        ),
        clock=FixedClock(NOW),
        observations=observations,
    )
    return (
        service,
        validation_service,
        atomicity,
        repository,
        observations,
        run_id,
        validation_receipt,
        validation,
        definition,
    )


def capsule_command(
    run_id: str,
    *,
    command_id: str = "synthetic-development-capsule-1",
    actor_id: str = "code-1",
    expected_version: int = 24,
    capsule_input_path: str = CAPSULE_INPUT_PATH,
    capsule_input_sha256: str = CAPSULE_INPUT_SHA256,
    requested_operation: str = "generate_versioned_traceable_development_capsule",
    requested_mode: str = CAPSULE_MODE,
    requested_profile_id: str = CAPSULE_PROFILE_ID,
    requested_sections: tuple[str, ...] = REQUIRED_CAPSULE_SECTIONS,
    requested_obligations: tuple[str, ...] = OWNED_OBLIGATIONS,
    requested_dependencies: tuple[str, ...] = DIRECT_DEPENDENCIES,
    requested_external_target_compatibility: str = EXTERNAL_TARGET_COMPATIBILITY,
    requested_production_eligible: bool = False,
    requested_certified: bool = False,
    requested_generated_product_implementation: bool = False,
    requested_external_runtime_ids: tuple[str, ...] = (),
    requested_external_skill_ids: tuple[str, ...] = (),
    reference_overrides: tuple[tuple[str, str], ...] = (),
    scaffolding_overrides: tuple[tuple[str, str], ...] = (),
) -> GenerateDevelopmentCapsuleCommand:
    return GenerateDevelopmentCapsuleCommand(
        command_id=command_id,
        run_id=run_id,
        actor_id=actor_id,
        expected_version=expected_version,
        correlation_id="st-11-01-correlation-1",
        causation_id="ST-07.04:StoryCompletionReceipt",
        capsule_input_path=capsule_input_path,
        capsule_input_sha256=capsule_input_sha256,
        requested_operation=requested_operation,
        requested_mode=requested_mode,
        requested_profile_id=requested_profile_id,
        requested_sections=requested_sections,
        requested_obligations=requested_obligations,
        requested_dependencies=requested_dependencies,
        requested_external_target_compatibility=requested_external_target_compatibility,
        requested_production_eligible=requested_production_eligible,
        requested_certified=requested_certified,
        requested_generated_product_implementation=requested_generated_product_implementation,
        requested_external_runtime_ids=requested_external_runtime_ids,
        requested_external_skill_ids=requested_external_skill_ids,
        reference_overrides=reference_overrides,
        scaffolding_overrides=scaffolding_overrides,
    )
