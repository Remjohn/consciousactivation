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
from cmf_builder.application.target_validation_commands import (
    AtomicContentHarnessValidationCommandService,
    ValidateAtomicContentHarnessCommand,
)
from cmf_builder.domain.atomic_harness_definition import PROFILE_ID, TARGET_KIND
from cmf_builder.domain.target_package_validation import (
    EXTERNAL_TARGET_COMPATIBILITY,
    INTERNAL_COMPATIBILITY,
    REQUIRED_VALIDATION_DIMENSIONS,
    VALIDATION_POLICY_PATH,
    VALIDATION_POLICY_SHA256,
)
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_07_02 import build_context as build_definition_context
from tests.stories.st_07_02 import compile_command


def build_context(*, seed: str = "ST-07.04", root=ROOT):
    (
        definition_service,
        atomicity,
        repository,
        observations,
        run_id,
        _,
        _,
        _,
    ) = build_definition_context(seed=f"{seed}-definition", root=root)
    definition_receipt = definition_service.compile(compile_command(run_id))
    definition = definition_service.get_active(run_id)
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
    service = AtomicContentHarnessValidationCommandService(
        root=root,
        repository=repository,
        authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_006_000_000,
            seed=seed,
        ),
        clock=FixedClock(NOW),
        observations=observations,
    )
    return (
        service,
        definition_service,
        atomicity,
        repository,
        observations,
        run_id,
        definition_receipt,
        definition,
    )


def validation_command(
    run_id: str,
    *,
    command_id: str = "synthetic-atomic-content-harness-validation-1",
    actor_id: str = "code-1",
    expected_version: int = 23,
    policy_path: str = VALIDATION_POLICY_PATH,
    policy_sha256: str = VALIDATION_POLICY_SHA256,
    requested_operation: str = "validate_atomic_content_harness",
    requested_target_kind: str = TARGET_KIND,
    requested_profile_id: str = PROFILE_ID,
    requested_dimensions: tuple[str, ...] = REQUIRED_VALIDATION_DIMENSIONS,
    requested_internal_compatibility: str = INTERNAL_COMPATIBILITY,
    requested_external_target_compatibility: str = EXTERNAL_TARGET_COMPATIBILITY,
    requested_production_eligible: bool = False,
    requested_certified: bool = False,
    requested_synthetic_not_certifiable: bool = True,
    field_overrides: tuple[tuple[str, str], ...] = (),
    lineage_overrides: tuple[tuple[str, str], ...] = (),
) -> ValidateAtomicContentHarnessCommand:
    return ValidateAtomicContentHarnessCommand(
        command_id=command_id,
        run_id=run_id,
        actor_id=actor_id,
        expected_version=expected_version,
        correlation_id="st-07-04-correlation-1",
        causation_id="ST-07.02:StoryCompletionReceipt",
        policy_path=policy_path,
        policy_sha256=policy_sha256,
        requested_operation=requested_operation,
        requested_target_kind=requested_target_kind,
        requested_profile_id=requested_profile_id,
        requested_dimensions=requested_dimensions,
        requested_internal_compatibility=requested_internal_compatibility,
        requested_external_target_compatibility=requested_external_target_compatibility,
        requested_production_eligible=requested_production_eligible,
        requested_certified=requested_certified,
        requested_synthetic_not_certifiable=requested_synthetic_not_certifiable,
        field_overrides=field_overrides,
        lineage_overrides=lineage_overrides,
    )
