import pytest

from cmf_builder.workflow.observability_recovery import (
    AuthorityStatus,
    ObservabilityRecoveryError,
    RecoveryAction,
    RecoveryAuthority,
    RecoveryCommand,
    compute_transition_payload_sha256,
    invalidate_projection,
    rollback_projection,
    validate_repeat_projection,
)


def digest(label: str) -> str:
    return (label.encode().hex() * 64)[:64]


def authority(status=AuthorityStatus.ACTIVE):
    return RecoveryAuthority("authority", "1.0", digest("auth"), tuple(RecoveryAction), ("*",), status)


def test_repeat_projection_is_idempotent_and_conflicting_repeat_fails():
    assert validate_repeat_projection("projection:1", "projection:1") == "projection:1"
    with pytest.raises(ObservabilityRecoveryError) as caught:
        validate_repeat_projection("projection:1", "projection:2")
    assert caught.value.code == "CONFLICTING_REPEAT_COMMAND"


def test_invalidation_and_rollback_preserve_history():
    auth = authority()
    prior = "projection:1"
    invalidate = RecoveryCommand(
        "invalidate",
        RecoveryAction.INVALIDATE,
        prior,
        compute_transition_payload_sha256(prior, RecoveryAction.INVALIDATE),
        auth.authority_identity,
    )
    invalidated = invalidate_projection(prior, invalidate, auth)
    assert invalidated.active_after is False
    assert invalidated.historical_receipt_preserved is True

    rollback = RecoveryCommand(
        "rollback",
        RecoveryAction.ROLLBACK,
        prior,
        compute_transition_payload_sha256(prior, RecoveryAction.ROLLBACK),
        auth.authority_identity,
    )
    rolled = rollback_projection(prior, rollback, auth)
    assert rolled.active_after is False
    assert rolled.historical_receipt_preserved is True


def test_inactive_authority_and_payload_drift_fail_closed():
    prior = "projection:1"
    inactive = authority(AuthorityStatus.INVALIDATED)
    inactive_command = RecoveryCommand(
        "invalidate",
        RecoveryAction.INVALIDATE,
        prior,
        compute_transition_payload_sha256(prior, RecoveryAction.INVALIDATE),
        inactive.authority_identity,
    )
    with pytest.raises(ObservabilityRecoveryError) as inactive_error:
        invalidate_projection(prior, inactive_command, inactive)
    assert inactive_error.value.code == "INACTIVE_AUTHORITY"

    auth = authority()
    drift = RecoveryCommand("invalidate", RecoveryAction.INVALIDATE, prior, digest("wrong"), auth.authority_identity)
    with pytest.raises(ObservabilityRecoveryError) as drift_error:
        invalidate_projection(prior, drift, auth)
    assert drift_error.value.code == "COMMAND_PAYLOAD_MISMATCH"
