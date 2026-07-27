from __future__ import annotations

import pytest

from cmf_builder.application.capsule_lifecycle_commands import (
    CapsuleLifecycleCommand,
    CapsuleLifecycleCommandService,
)
from cmf_builder.skills.capsule_lifecycle import CapsuleLifecycleError, CapsuleState, InMemoryCapsuleLifecycle
from tests.stories.st_05_04.test_jit_capsule import command
from cmf_builder.application.jit_capsule_commands import JITCapsuleCommandService


def capsule():
    return JITCapsuleCommandService(authorized_actor_ids=("analyst-1",)).assemble(command())


def call_args(value):
    return {
        "capsule_id": value.capsule_id,
        "capsule_hash": value.capsule_hash,
        "package_hash": value.skill_package_hash,
        "actor_id": "operator-1",
    }


def test_pin_verify_activate_dispose_and_historical_reproduction() -> None:
    value = capsule()
    service = InMemoryCapsuleLifecycle(authorized_actor_ids=("operator-1",))
    pinned = service.pin(command_id="pin", capsule=value, actor_id="operator-1")
    verified = service.verify(command_id="verify", **call_args(value))
    activated = service.activate(command_id="activate", **call_args(value))
    disposed = service.dispose(command_id="dispose", **call_args(value))
    historical = service.reproduce_historical(command_id="history", **call_args(value))
    assert [pinned.resulting_state, verified.resulting_state, activated.resulting_state, disposed.resulting_state] == [
        "PINNED", "VERIFIED", "ACTIVE", "DISPOSED"
    ]
    assert service.state_of(value.capsule_id) is CapsuleState.DISPOSED
    assert service.historical_capsule(value.capsule_id) == value
    assert historical.historical_reproducible is True
    with pytest.raises(CapsuleLifecycleError, match="cannot be loaded"):
        service.load(command_id="load-after-dispose", **call_args(value))


def test_exact_hash_pins_no_silent_upgrade_and_authority() -> None:
    value = capsule()
    service = InMemoryCapsuleLifecycle(authorized_actor_ids=("operator-1",))
    service.pin(command_id="pin", capsule=value, actor_id="operator-1")
    with pytest.raises(CapsuleLifecycleError, match="hash mismatch"):
        service.verify(command_id="bad-hash", **{**call_args(value), "capsule_hash": "0" * 64})
    with pytest.raises(CapsuleLifecycleError, match="authority"):
        service.verify(command_id="bad-actor", **{**call_args(value), "actor_id": "intruder"})
    with pytest.raises(CapsuleLifecycleError, match="Unpinned"):
        service.verify(command_id="unpinned", **{**call_args(value), "package_hash": ""})


def test_duplicate_commands_are_payload_safe_and_conflicts_fail_closed() -> None:
    value = capsule()
    service = InMemoryCapsuleLifecycle(authorized_actor_ids=("operator-1",))
    first = service.pin(command_id="same", capsule=value, actor_id="operator-1")
    assert service.pin(command_id="same", capsule=value, actor_id="operator-1") == first
    with pytest.raises(CapsuleLifecycleError, match="Conflicting"):
        service.reproduce_historical(command_id="same", **call_args(value))


def test_atomic_failure_preserves_prior_state_and_records_no_command() -> None:
    value = capsule()
    service = InMemoryCapsuleLifecycle(authorized_actor_ids=("operator-1",))
    with pytest.raises(CapsuleLifecycleError, match="Injected"):
        service.pin(command_id="pin", capsule=value, actor_id="operator-1", inject_failure=True)
    assert service.state_of(value.capsule_id) is None
    service.pin(command_id="pin", capsule=value, actor_id="operator-1")
    with pytest.raises(CapsuleLifecycleError, match="Injected"):
        service.verify(command_id="verify", **call_args(value), inject_failure=True)
    assert service.state_of(value.capsule_id) is CapsuleState.PINNED


def test_invalidation_prevents_reuse_but_preserves_history() -> None:
    value = capsule()
    service = InMemoryCapsuleLifecycle(authorized_actor_ids=("operator-1",))
    service.pin(command_id="pin", capsule=value, actor_id="operator-1")
    invalidated = service.invalidate(command_id="invalidate", **call_args(value))
    assert invalidated.resulting_state == "INVALIDATED"
    assert service.historical_capsule(value.capsule_id).capsule_hash == value.capsule_hash
    with pytest.raises(CapsuleLifecycleError, match="Only an exact pinned"):
        service.verify(command_id="reuse", **call_args(value))
    history = service.reproduce_historical(command_id="history", **call_args(value))
    assert history.resulting_state == "INVALIDATED"


def test_application_seam_emits_success_and_typed_rejection_evidence() -> None:
    value = capsule()
    service = CapsuleLifecycleCommandService(authorized_actor_ids=("operator-1",))
    receipt = service.execute(
        CapsuleLifecycleCommand(
            command_id="pin",
            operation="pin",
            actor_id="operator-1",
            capsule=value,
        )
    )
    assert receipt.resulting_state == "PINNED"
    assert service.observations[-1].outcome == "PASS"
    with pytest.raises(CapsuleLifecycleError, match="authority"):
        service.execute(
            CapsuleLifecycleCommand(
                command_id="unauthorized",
                operation="verify",
                actor_id="intruder",
                capsule_id=value.capsule_id,
                capsule_hash=value.capsule_hash,
                package_hash=value.skill_package_hash,
            )
        )
    failure = service.observations[-1]
    assert failure.outcome == "FAIL"
    assert failure.failure_context["code"] == "CapsuleLifecycleError"
