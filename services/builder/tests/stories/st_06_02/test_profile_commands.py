from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from cmf_builder.application.authority import Action, Actor, ActorKind, AuthorityGrant, AuthorityService
from cmf_builder.application.profile_commands import (
    CompileCategoryProfilesCommand,
    InMemoryProfileObservationSink,
    InMemoryProfileRegistryRepository,
    ProfileCommandRejected,
    ProfileCompilationService,
)


ROOT = Path(__file__).resolve().parents[3]
NOW = datetime(2026, 7, 16, tzinfo=timezone.utc)


def _service():
    authority = AuthorityService(
        actors=(Actor("compiler-code", ActorKind.CODE), Actor("external", ActorKind.EXTERNAL)),
        grants=(
            AuthorityGrant("compiler-code", frozenset({Action.COMPILE_CATEGORY_PROFILES}), "*", NOW + timedelta(days=1)),
            AuthorityGrant("external", frozenset({Action.COMPILE_CATEGORY_PROFILES}), "*", NOW + timedelta(days=1)),
        ),
    )
    repository = InMemoryProfileRegistryRepository()
    observations = InMemoryProfileObservationSink()
    return ProfileCompilationService(authority, repository, observations), repository, observations


def _command(command_id: str = "profiles-1", actor_id: str = "compiler-code"):
    return CompileCategoryProfilesCommand(
        command_id=command_id,
        registry_id="category-local-format-profiles",
        registry_version="1.0.0",
        category_registry_bytes=(ROOT / "governance/CANONICAL_CATEGORY_REGISTRY.yaml").read_bytes(),
        compatibility_bytes=(ROOT / "contracts/integration/CATEGORY_PROFILE_COMPATIBILITY.yaml").read_bytes(),
        conversational_registry_bytes=(ROOT / "governance/CONVERSATIONAL_PROFILE_REGISTRY.yaml").read_bytes(),
        actor_id=actor_id,
        now=NOW,
        correlation_id="corr-profiles",
        causation_id="ST-06.01",
    )


def test_command_commit_and_replay_are_idempotent() -> None:
    service, repository, observations = _service()
    first = service.compile(_command())
    second = service.compile(_command())
    assert first == second
    assert repository.registry_count == 1
    assert repository.receipt_count == 1
    assert [item.event_name for item in observations.items] == [
        "ST-06.02:ProfileRegistryCompiled",
        "ST-06.02:ProfileRegistryReplayReturned",
    ]


def test_conflicting_command_and_external_actor_reject() -> None:
    service, repository, observations = _service()
    service.compile(_command())
    conflict = _command()
    object.__setattr__(conflict, "registry_version", "2.0.0")
    with pytest.raises(ProfileCommandRejected, match="different payload"):
        service.compile(conflict)
    with pytest.raises(ProfileCommandRejected, match="actor"):
        service.compile(_command("profiles-2", "external"))
    assert repository.registry_count == 1
    assert observations.items[-1].outcome == "FAIL"


def test_injected_failure_leaves_zero_partial_state() -> None:
    service, repository, observations = _service()
    repository.inject_failure_before_commit()
    with pytest.raises(ProfileCommandRejected, match="Injected"):
        service.compile(_command())
    assert repository.registry_count == 0
    assert repository.receipt_count == 0
    assert observations.items[-1].outcome == "FAIL"
