from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from cmf_builder.application.authority import Action, Actor, ActorKind, AuthorityGrant, AuthorityService
from cmf_builder.application.target_registration_commands import (
    CompilationTargetService,
    InMemoryTargetObservationSink,
    InMemoryTargetRegistryRepository,
    RegisterTargetRegistryCommand,
    RollbackTargetRegistryCommand,
    SelectCompilationTargetCommand,
    TargetRegistrationCommandRejected,
    REGISTER_COMPILATION_TARGETS_CAPABILITY_SCOPE,
)
from cmf_builder.domain.compilation_targets import TARGET_IDS, TargetVersionConflict, migrate_target_registry
from test_three_target_registry import profile, ref, registry


NOW = datetime(2026, 7, 17, tzinfo=timezone.utc)


def service():
    authority = AuthorityService(
        actors=(Actor("target-code", ActorKind.CODE),),
        grants=(AuthorityGrant("target-code", frozenset({Action.REGISTER_COMPILATION_TARGETS}), "*", NOW + timedelta(days=1)),),
    )
    repo = InMemoryTargetRegistryRepository()
    return CompilationTargetService(authority, repo, InMemoryTargetObservationSink()), repo


def register_command(current, command_id, expected=None):
    return RegisterTargetRegistryCommand(
        command_id=command_id,
        registry=current,
        actor_id="target-code",
        expected_active_registry_hash=expected,
        now=NOW,
        correlation_id="corr",
        causation_id="cause",
    )


def test_migration_preserves_all_targets_and_requires_new_version() -> None:
    first = registry()
    changed_profiles = tuple(
        replace(profile(target_id), target_version="1.1.0")
        if target_id == "atomic_content_harness"
        else profile(target_id)
        for target_id in TARGET_IDS
    )
    second = migrate_target_registry(
        first,
        new_version="1.1.0",
        profiles=changed_profiles,
        authority_ref=ref("target_authority", "v1"),
    )
    assert second.registry_hash != first.registry_hash
    assert {item.target_id for item in second.profiles} == set(TARGET_IDS)
    with pytest.raises(TargetVersionConflict):
        migrate_target_registry(
            first,
            new_version=first.registry_version,
            profiles=changed_profiles,
            authority_ref=ref("target_authority", "v1"),
        )


def test_registration_replay_is_idempotent_and_conflict_fails() -> None:
    svc, repo = service()
    cmd = register_command(registry(), "register")
    first = svc.register(cmd)
    assert svc.register(cmd) == first
    assert len(repo.history("compilation-target-registry")) == 1
    with pytest.raises(TargetRegistrationCommandRejected, match="different payload"):
        svc.register(replace(cmd, correlation_id="changed"))


def test_registry_history_and_non_destructive_rollback() -> None:
    svc, repo = service()
    first = registry()
    svc.register(register_command(first, "first"))
    second = registry(version="1.1.0")
    svc.register(register_command(second, "second", first.registry_hash))
    assert len(repo.history(first.registry_id)) == 2
    receipt = svc.rollback(
        RollbackTargetRegistryCommand(
            command_id="rollback",
            registry_id=first.registry_id,
            target_registry_hash=first.registry_hash,
            actor_id="target-code",
            expected_active_registry_hash=second.registry_hash,
            now=NOW,
            correlation_id="corr-rollback",
            causation_id="second",
        )
    )
    assert receipt.outcome == "ROLLBACK_VERIFIED"
    assert repo.active(first.registry_id) == first
    assert len(repo.history(first.registry_id)) == 2


def test_new_command_for_same_active_registry_is_persisted_for_replay() -> None:
    svc, repo = service()
    current = registry()
    svc.register(register_command(current, "first"))
    second = register_command(current, "same-content-new-command")
    receipt = svc.register(second)
    assert repo.command_state(second.command_id) is not None
    assert svc.register(second) == receipt


def test_rollback_requires_governed_authority_and_is_payload_safe() -> None:
    svc, repo = service()
    first = registry()
    svc.register(register_command(first, "first"))
    second = registry(version="1.1.0")
    svc.register(register_command(second, "second", first.registry_hash))
    command = RollbackTargetRegistryCommand(
        command_id="rollback",
        registry_id=first.registry_id,
        target_registry_hash=first.registry_hash,
        actor_id="target-code",
        expected_active_registry_hash=second.registry_hash,
        now=NOW,
        correlation_id="corr",
        causation_id="second",
    )
    receipt = svc.rollback(command)
    assert svc.rollback(command) == receipt
    with pytest.raises(TargetRegistrationCommandRejected, match="different payload"):
        svc.rollback(replace(command, target_registry_hash=second.registry_hash))


def test_rollback_impersonation_is_rejected_by_authority_service() -> None:
    svc, _ = service()
    first = registry()
    svc.register(register_command(first, "first"))
    with pytest.raises(TargetRegistrationCommandRejected):
        svc.rollback(
            RollbackTargetRegistryCommand(
                command_id="bad-rollback",
                registry_id=first.registry_id,
                target_registry_hash=first.registry_hash,
                actor_id="impersonator",
                expected_active_registry_hash=first.registry_hash,
                now=NOW,
                correlation_id="corr",
                causation_id="first",
            )
        )


def test_selection_command_replay_is_payload_safe() -> None:
    svc, _ = service()
    current = registry()
    svc.register(register_command(current, "register"))
    command = SelectCompilationTargetCommand(
        command_id="select",
        run_id="run-1",
        requested_target_ids=("atomic_content_harness",),
        actor_id="target-code",
        expected_active_registry_hash=current.registry_hash,
        now=NOW,
        correlation_id="corr",
        causation_id="register",
    )
    assert svc.select(command) == svc.select(command)
    with pytest.raises(TargetRegistrationCommandRejected, match="different payload"):
        svc.select(replace(command, run_id="run-2"))


def test_selection_rejects_active_registry_version_drift() -> None:
    svc, _ = service()
    current = registry()
    svc.register(register_command(current, "register"))
    with pytest.raises(TargetRegistrationCommandRejected, match="selection expectation"):
        svc.select(
            SelectCompilationTargetCommand(
                command_id="stale-selection",
                run_id="run",
                requested_target_ids=("atomic_content_harness",),
                actor_id="target-code",
                expected_active_registry_hash="sha256:" + "0" * 64,
                now=NOW,
                correlation_id="corr",
                causation_id="register",
            )
        )


def test_combined_target_control_action_is_explicitly_least_privilege() -> None:
    assert REGISTER_COMPILATION_TARGETS_CAPABILITY_SCOPE == frozenset(
        {"register_registry", "select_target", "rollback_registry"}
    )
    assert "compile_target" not in REGISTER_COMPILATION_TARGETS_CAPABILITY_SCOPE
    assert "external_runtime" not in REGISTER_COMPILATION_TARGETS_CAPABILITY_SCOPE
