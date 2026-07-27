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
from cmf_builder.application.syntax_commands import (
    CategorySyntaxCompilationService,
    CompileCategorySyntaxCommand,
    InMemoryCategorySyntaxObservationSink,
    InMemoryCategorySyntaxRepository,
    SyntaxCommandRejected,
)
from cmf_builder.domain.category_syntax import (
    CategorySyntaxError,
    compile_category_native_syntax,
)


NOW = datetime(2026, 7, 17, tzinfo=timezone.utc)


def _service():
    authority = AuthorityService(
        actors=(
            Actor("compiler-code", ActorKind.CODE),
            Actor("external", ActorKind.EXTERNAL),
        ),
        grants=(
            AuthorityGrant(
                "compiler-code",
                frozenset({Action.COMPILE_CATEGORY_SYNTAX}),
                "*",
                NOW + timedelta(days=1),
            ),
            AuthorityGrant(
                "external",
                frozenset({Action.COMPILE_CATEGORY_SYNTAX}),
                "*",
                NOW + timedelta(days=1),
            ),
        ),
    )
    repository = InMemoryCategorySyntaxRepository()
    observations = InMemoryCategorySyntaxObservationSink()
    return (
        CategorySyntaxCompilationService(authority, repository, observations),
        repository,
        observations,
    )


def _command(source, command_id: str = "syntax-1", actor_id: str = "compiler-code"):
    return CompileCategorySyntaxCommand(
        command_id=command_id,
        source=source,
        actor_id=actor_id,
        now=NOW,
        correlation_id="corr-st0603",
        causation_id="ST-06.02",
    )


def test_cross_category_profile_and_grammar_substitution_fail_closed(
    source_factory,
) -> None:
    source = source_factory("2d_character_animation")
    with pytest.raises(CategorySyntaxError, match="profile"):
        compile_category_native_syntax(replace(source, profile_id="format01_story_video"))
    with pytest.raises(CategorySyntaxError, match="substitution"):
        compile_category_native_syntax(
            replace(source, requested_grammar_family="SHORT_FORM_EDITED_VIDEO_TIMELINE")
        )


def test_missing_rich_role_and_wrong_reading_lock_fail_closed(source_factory) -> None:
    source = source_factory("short_form_edited_video")
    missing = tuple(
        ref for ref in source.rich_source_object_refs if ref.lineage_role != "identity_dna"
    )
    with pytest.raises(CategorySyntaxError) as lineage_error:
        compile_category_native_syntax(replace(source, rich_source_object_refs=missing))
    assert lineage_error.value.code == "HG-015"
    with pytest.raises(CategorySyntaxError, match="wrong_reading_locks"):
        compile_category_native_syntax(replace(source, wrong_reading_locks=()))


def test_stale_lineage_and_false_certification_fail_closed(
    source_factory, ref_factory
) -> None:
    source = source_factory("supervisuals")
    stale = ref_factory("syntax_evidence", status="INVALIDATED")
    with pytest.raises(CategorySyntaxError, match="invalidated"):
        compile_category_native_syntax(replace(source, evidence_refs=(stale,)))
    with pytest.raises(CategorySyntaxError, match="production or certification"):
        compile_category_native_syntax(replace(source, certified=True))


def test_command_commit_replay_and_observability(source_factory) -> None:
    service, repository, observations = _service()
    command = _command(source_factory("carousels"))
    first = service.compile(command)
    second = service.compile(command)
    assert first == second
    assert first.implementation_status == "IMPLEMENTED_DEVELOPMENT_PASS"
    assert first.evidence_status == "EVIDENCE_PENDING"
    assert repository.artifact_set_count == 1
    assert repository.receipt_count == 1
    assert [item.event_name for item in observations.items] == [
        "ST-06.03:CategoryNativeSyntaxCompiled",
        "ST-06.03:CategoryNativeCompilationReplayReturned",
    ]


def test_conflicting_command_and_external_actor_are_rejected(source_factory) -> None:
    service, repository, observations = _service()
    source = source_factory("short_form_edited_video")
    service.compile(_command(source))
    with pytest.raises(SyntaxCommandRejected, match="different payload"):
        service.compile(_command(replace(source, payoff="different")))
    with pytest.raises(SyntaxCommandRejected, match="actor"):
        service.compile(_command(source, "syntax-2", "external"))
    assert repository.artifact_set_count == 1
    assert observations.items[-1].outcome == "FAIL"


def test_injected_failure_has_zero_partial_state(source_factory) -> None:
    service, repository, observations = _service()
    repository.inject_failure_before_commit()
    with pytest.raises(SyntaxCommandRejected, match="Injected"):
        service.compile(_command(source_factory("supervisuals")))
    assert repository.artifact_set_count == 0
    assert repository.receipt_count == 0
    assert repository.command_count == 0
    assert observations.items[-1].event_name == "ST-06.03:CategoryNativeCompilationRejected"
