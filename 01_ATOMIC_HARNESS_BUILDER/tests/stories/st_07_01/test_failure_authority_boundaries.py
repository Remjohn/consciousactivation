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
)
from cmf_builder.domain.compilation_targets import (
    TARGET_IDS,
    TargetAuthorityRejected,
    TargetRegistryRejected,
    compile_target_registry,
)
from test_three_target_registry import profile, ref, registry


NOW = datetime(2026, 7, 17, tzinfo=timezone.utc)


def service(actor_id: str = "target-code"):
    authority = AuthorityService(
        actors=(Actor(actor_id, ActorKind.CODE), Actor("unauthorized", ActorKind.CODE)),
        grants=(AuthorityGrant(actor_id, frozenset({Action.REGISTER_COMPILATION_TARGETS}), "*", NOW + timedelta(days=1)),),
    )
    repo = InMemoryTargetRegistryRepository()
    observations = InMemoryTargetObservationSink()
    return CompilationTargetService(authority, repo, observations), repo, observations


def command(current, *, actor_id="target-code", command_id="register-targets"):
    return RegisterTargetRegistryCommand(
        command_id=command_id,
        registry=current,
        actor_id=actor_id,
        expected_active_registry_hash=None,
        now=NOW,
        correlation_id="corr-st0701",
        causation_id="ST-06.05",
    )


def test_missing_fourth_duplicate_and_universal_targets_fail_closed() -> None:
    authority = ref("target_authority", "v1")
    values = tuple(profile(target_id) for target_id in TARGET_IDS)
    for invalid in (values[:2], values + (values[0],)):
        with pytest.raises(TargetRegistryRejected):
            compile_target_registry(
                registry_id="compilation-target-registry",
                registry_version="1.0.0",
                profiles=invalid,
                authority_ref=authority,
            )
    with pytest.raises(TargetRegistryRejected):
        replace(values[0], target_id="universal_target")


def test_forged_registry_hash_bytes_and_profiles_fail_at_construction() -> None:
    current = registry()
    with pytest.raises(TargetRegistryRejected, match="canonical bytes"):
        replace(current, registry_hash="sha256:" + "0" * 64)
    with pytest.raises(TargetRegistryRejected, match="canonical bytes"):
        replace(current, canonical_bytes=b"{}\n")
    with pytest.raises(TargetRegistryRejected):
        replace(current, profiles=current.profiles[:2])


def test_flattened_owner_missing_snapshot_false_certification_and_bad_delegation_pin_fail() -> None:
    with pytest.raises(TargetRegistryRejected, match="flattened"):
        replace(profile("visual_asset_editor"), product_owner="Atomic Harness Builder")
    with pytest.raises(TargetRegistryRejected, match="snapshot"):
        replace(profile("visual_asset_editor"), interface_snapshot_ref=None)
    with pytest.raises(TargetRegistryRejected, match="readiness or certification"):
        replace(profile("atomic_content_harness"), certified=True)
    with pytest.raises(TargetRegistryRejected, match="uncertified"):
        replace(profile("visual_asset_editor"), certification_scope="PRODUCTION_CERTIFIED")
    with pytest.raises(TargetRegistryRejected, match="exact governed target policy"):
        replace(
            profile("visual_asset_editor"),
            required_extensions=profile("visual_asset_editor").required_extensions + ("enable_runtime",),
        )
    with pytest.raises(TargetAuthorityRejected, match="external owning authority"):
        replace(
            profile("visual_asset_editor"),
            interface_snapshot_ref=ref("vae_interface_snapshot", "self-attested"),
        )
    with pytest.raises(TargetRegistryRejected, match="RC4"):
        replace(
            profile("content_asset_delegation_contract"),
            interface_snapshot_ref=ref(
                "delegation_interface_snapshot",
                "rc5",
                version="1.1.0-rc.5",
                authority="Delegation Protocol product authority",
            ),
        )


def test_unauthorized_or_mismatched_actor_rejected_with_observation() -> None:
    svc, _, observations = service()
    with pytest.raises(TargetRegistrationCommandRejected):
        svc.register(command(registry(), actor_id="unauthorized"))
    assert observations.items[-1].event_name == "ST-07.01:TargetRegistryRejected"
    mismatched = compile_target_registry(
        registry_id="compilation-target-registry",
        registry_version="1.0.0",
        profiles=tuple(
            replace(profile(target_id), authority_ref=ref("target_authority", "other", authority="other-code"))
            for target_id in TARGET_IDS
        ),
        authority_ref=ref("target_authority", "other", authority="other-code"),
    )
    with pytest.raises(TargetRegistrationCommandRejected, match="acting actor"):
        svc.register(command(mismatched, command_id="mismatch"))


def test_injected_failure_leaves_no_partial_registry_receipt_or_command() -> None:
    svc, repo, observations = service()
    repo.inject_failure_before_commit()
    with pytest.raises(TargetRegistrationCommandRejected, match="Injected"):
        svc.register(command(registry()))
    assert repo.history("compilation-target-registry") == ()
    assert observations.items[-1].outcome == "FAIL"


def test_observation_failure_is_atomic_for_registration_and_selection() -> None:
    svc, repo, observations = service()
    current = registry()
    observations.inject_failure_before_emit()
    with pytest.raises(TargetRegistrationCommandRejected, match="observation"):
        svc.register(command(current))
    assert repo.history(current.registry_id) == ()
    svc.register(command(current, command_id="register-after-failure"))
    observations.inject_failure_before_emit()
    with pytest.raises(TargetRegistrationCommandRejected, match="observation"):
        svc.select(
            SelectCompilationTargetCommand(
                command_id="select-fails-atomically",
                run_id="run",
                requested_target_ids=("atomic_content_harness",),
                actor_id="target-code",
                expected_active_registry_hash=current.registry_hash,
                now=NOW,
                correlation_id="corr",
                causation_id="register-after-failure",
            )
        )
    assert repo.command_state("select-fails-atomically") is None


def test_observation_failure_is_atomic_for_rollback() -> None:
    svc, repo, observations = service()
    first = registry()
    svc.register(command(first, command_id="first"))
    second = registry(version="1.1.0")
    second_command = replace(
        command(second, command_id="second"),
        expected_active_registry_hash=first.registry_hash,
    )
    svc.register(second_command)
    observations.inject_failure_before_emit()
    with pytest.raises(TargetRegistrationCommandRejected, match="observation"):
        svc.rollback(
            RollbackTargetRegistryCommand(
                command_id="rollback-fails-atomically",
                registry_id=first.registry_id,
                target_registry_hash=first.registry_hash,
                actor_id="target-code",
                expected_active_registry_hash=second.registry_hash,
                now=NOW,
                correlation_id="corr",
                causation_id="second",
            )
        )
    assert repo.active(first.registry_id) == second
    assert repo.command_state("rollback-fails-atomically") is None


def test_replay_observation_failure_returns_committed_register_and_selection_results() -> None:
    svc, _, observations = service()
    current = registry()
    register = command(current, command_id="register-for-replay")
    register_receipt = svc.register(register)
    observations.inject_failure_before_emit()
    assert svc.register(register) == register_receipt

    select = SelectCompilationTargetCommand(
        command_id="select-for-replay",
        run_id="run-replay",
        requested_target_ids=("atomic_content_harness",),
        actor_id="target-code",
        expected_active_registry_hash=current.registry_hash,
        now=NOW,
        correlation_id="corr",
        causation_id="register-for-replay",
    )
    selection = svc.select(select)
    observations.inject_failure_before_emit()
    assert svc.select(select) == selection
