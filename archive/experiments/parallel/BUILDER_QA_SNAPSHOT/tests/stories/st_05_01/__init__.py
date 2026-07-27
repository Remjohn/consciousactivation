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
    CompileSyntheticSkillRegistryCommand,
    SyntheticSkillRegistryCommandService,
)
from cmf_builder.domain.skill_registry import (
    REGISTRY_FIXTURE_PATH,
    REGISTRY_FIXTURE_SHA256,
    REGISTRY_POLICY_PATH,
    REGISTRY_POLICY_SHA256,
    REGISTRY_REF,
    REGISTRY_SCHEMA_PATH,
    REGISTRY_SCHEMA_SHA256,
    REGISTRY_VALIDATION_RECEIPT_PATH,
    REGISTRY_VALIDATION_RECEIPT_SHA256,
    SKILL_REGISTRY_INPUT_PATH,
    SKILL_REGISTRY_INPUT_SHA256,
)
from tests.stories.st_01_01_synthetic_proof import NOW, ROOT
from tests.stories.st_04_05 import (
    build_context as build_minimum_context,
    compile_command as compile_minimum_context,
)


def build_context(*, seed: str = "ST-05.01", root=ROOT):
    context_service, _, atomicity, repository, observations, run_id, accepted = (
        build_minimum_context(seed=f"{seed}-minimum-context", root=root)
    )
    context_receipt = context_service.compile(compile_minimum_context(run_id))
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
    service = SyntheticSkillRegistryCommandService(
        root=root,
        repository=repository,
        authority=AuthorityService(actors=actors, grants=grants),
        ids=DeterministicUuid7IdProvider(
            timestamp_ms=1_768_001_000_000,
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
        accepted,
        context_receipt,
    )


def compile_command(
    run_id: str,
    *,
    command_id: str = "synthetic-skill-registry-1",
    actor_id: str = "code-1",
    expected_version: int = 20,
    registry_input_path: str = SKILL_REGISTRY_INPUT_PATH,
    registry_input_sha256: str = SKILL_REGISTRY_INPUT_SHA256,
    registry_fixture_path: str = REGISTRY_FIXTURE_PATH,
    registry_fixture_sha256: str = REGISTRY_FIXTURE_SHA256,
    policy_path: str = REGISTRY_POLICY_PATH,
    policy_sha256: str = REGISTRY_POLICY_SHA256,
    schema_path: str = REGISTRY_SCHEMA_PATH,
    schema_sha256: str = REGISTRY_SCHEMA_SHA256,
    validation_receipt_path: str = REGISTRY_VALIDATION_RECEIPT_PATH,
    validation_receipt_sha256: str = REGISTRY_VALIDATION_RECEIPT_SHA256,
    registry_ref: str = REGISTRY_REF,
    requested_operation: str = "consume_exact_registry",
    declared_external_skill_ids: tuple[str, ...] = (),
    capability_overrides: tuple[tuple[str, str], ...] = (),
    relation_edges: tuple[tuple[str, str], ...] = (),
    evaluator_receipt_ids: tuple[str, ...] = (),
    active_maturity_claims: tuple[tuple[str, str], ...] = (),
) -> CompileSyntheticSkillRegistryCommand:
    return CompileSyntheticSkillRegistryCommand(
        command_id=command_id,
        run_id=run_id,
        actor_id=actor_id,
        expected_version=expected_version,
        correlation_id="st-05-01-correlation-1",
        causation_id="ST-04.05:MinimumCompleteContextCompiled",
        registry_input_path=registry_input_path,
        registry_input_sha256=registry_input_sha256,
        registry_fixture_path=registry_fixture_path,
        registry_fixture_sha256=registry_fixture_sha256,
        policy_path=policy_path,
        policy_sha256=policy_sha256,
        schema_path=schema_path,
        schema_sha256=schema_sha256,
        validation_receipt_path=validation_receipt_path,
        validation_receipt_sha256=validation_receipt_sha256,
        registry_ref=registry_ref,
        requested_operation=requested_operation,
        declared_external_skill_ids=declared_external_skill_ids,
        capability_overrides=capability_overrides,
        relation_edges=relation_edges,
        evaluator_receipt_ids=evaluator_receipt_ids,
        active_maturity_claims=active_maturity_claims,
    )
