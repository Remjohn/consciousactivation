from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from cmf_builder.application.authority import (
    Action,
    Actor,
    ActorKind,
    AuthorityGrant,
    AuthorityService,
)
from cmf_builder.application.category_policy_commands import (
    CategoryPolicyCommandRejected,
    CategoryPolicyCompilationService,
    CompileCategoryPolicyCommand,
    InMemoryCategoryPolicyObservationSink,
    InMemoryCategoryPolicyRepository,
)
from cmf_builder.domain.category_runtime_rules import (
    CategoryPolicyError,
    compile_category_operating_rules,
)


NOW = datetime(2026, 7, 17, tzinfo=timezone.utc)


def _service():
    authority = AuthorityService(
        actors=(
            Actor("policy-code", ActorKind.CODE),
            Actor("external", ActorKind.EXTERNAL),
        ),
        grants=(
            AuthorityGrant(
                "policy-code",
                frozenset({Action.COMPILE_CATEGORY_POLICY}),
                "*",
                NOW + timedelta(days=1),
            ),
            AuthorityGrant(
                "external",
                frozenset({Action.COMPILE_CATEGORY_POLICY}),
                "*",
                NOW + timedelta(days=1),
            ),
        ),
    )
    repository = InMemoryCategoryPolicyRepository()
    observations = InMemoryCategoryPolicyObservationSink()
    return (
        CategoryPolicyCompilationService(authority, repository, observations),
        repository,
        observations,
    )


def _command(source, command_id="policy-1", actor_id="policy-code"):
    return CompileCategoryPolicyCommand(
        command_id=command_id,
        source=source,
        actor_id=actor_id,
        now=NOW,
        correlation_id="corr-st0604",
        causation_id="ST-06.03",
    )


def test_altered_source_hash_and_linkage_fail_closed(policy_source_factory) -> None:
    source = policy_source_factory("short_form_edited_video")
    bad_syntax = replace(source.syntax, syntax_hash="sha256:" + "0" * 64)
    with pytest.raises(CategoryPolicyError, match="syntax hash"):
        compile_category_operating_rules(replace(source, syntax=bad_syntax))
    bad_sequence = replace(source.sequence, category_syntax_ref="sha256:" + "1" * 64)
    with pytest.raises(CategoryPolicyError, match="exact category syntax"):
        compile_category_operating_rules(replace(source, sequence=bad_sequence))


def test_missing_owner_and_owner_role_conflict_fail_closed(
    policy_source_factory, ref_factory
) -> None:
    source = policy_source_factory("carousels")
    with pytest.raises(CategoryPolicyError, match="evaluation_owner is required"):
        compile_category_operating_rules(replace(source, evaluator_owner_ref=None))
    wrong_role = ref_factory("repair_owner", suffix="conflict")
    with pytest.raises(CategoryPolicyError, match="conflicting owner role"):
        compile_category_operating_rules(
            replace(source, evaluator_owner_ref=wrong_role)
        )


def test_external_execution_and_certification_claims_fail_closed(
    policy_source_factory,
) -> None:
    source = policy_source_factory("conversational_activation_expression")
    with pytest.raises(CategoryPolicyError, match="External runtime"):
        compile_category_operating_rules(
            replace(source, requested_external_execution=True)
        )
    with pytest.raises(CategoryPolicyError, match="certification"):
        compile_category_operating_rules(replace(source, requested_certification=True))


def test_command_commit_replay_and_observability(policy_source_factory) -> None:
    service, repository, observations = _service()
    command = _command(policy_source_factory("supervisuals"))
    first = service.compile(command)
    second = service.compile(command)
    assert first == second
    assert repository.ruleset_count == 1
    assert repository.receipt_count == 1
    assert first.implementation_status == "IMPLEMENTED_DEVELOPMENT_PASS"
    assert [item.event_name for item in observations.items] == [
        "ST-06.04:CategoryPolicyCompiled",
        "ST-06.04:CategoryPolicyReplayReturned",
    ]


def test_command_conflict_external_actor_and_atomic_failure(policy_source_factory) -> None:
    source = policy_source_factory("short_form_edited_video")
    service, repository, observations = _service()
    service.compile(_command(source))
    with pytest.raises(CategoryPolicyCommandRejected, match="different payload"):
        service.compile(_command(replace(source, ruleset_version="2.0.0")))
    with pytest.raises(CategoryPolicyCommandRejected, match="actor"):
        service.compile(_command(source, "policy-2", "external"))
    assert repository.ruleset_count == 1
    assert observations.items[-1].outcome == "FAIL"

    fresh, fresh_repository, fresh_observations = _service()
    fresh_repository.inject_failure_before_commit()
    with pytest.raises(CategoryPolicyCommandRejected, match="Injected"):
        fresh.compile(_command(source))
    assert fresh_repository.ruleset_count == 0
    assert fresh_repository.receipt_count == 0
    assert fresh_repository.command_count == 0
    assert fresh_observations.items[-1].outcome == "FAIL"
