import pytest

from cmf_builder.workflow.candidate_routing import (
    AuthorityStatus,
    CandidateAction,
    CandidateAuthority,
    CandidateCommand,
    CandidateRoutingError,
    compute_transition_payload_sha256,
    invalidate_candidate_decision,
    rollback_candidate_decision,
    validate_repeat_decision,
)


def digest(label: str) -> str:
    return (label.encode().hex() * 64)[:64]


def authority(status=AuthorityStatus.ACTIVE):
    return CandidateAuthority("authority", "1.0", digest("auth"), tuple(CandidateAction), ("*",), status)


def test_repeat_decision_is_idempotent_and_conflicting_repeat_fails():
    assert validate_repeat_decision("decision:1", "decision:1") == "decision:1"

    with pytest.raises(CandidateRoutingError) as caught:
        validate_repeat_decision("decision:1", "decision:2")
    assert caught.value.code == "CONFLICTING_REPEAT_COMMAND"


def test_invalidation_and_rollback_preserve_history():
    auth = authority()
    prior = "candidate-decision:1"
    invalidate = CandidateCommand(
        "invalidate",
        CandidateAction.INVALIDATE,
        prior,
        compute_transition_payload_sha256(prior, CandidateAction.INVALIDATE),
        auth.authority_identity,
    )
    invalidated = invalidate_candidate_decision(prior, invalidate, auth)
    assert invalidated.active_after is False
    assert invalidated.historical_receipt_preserved is True

    rollback = CandidateCommand(
        "rollback",
        CandidateAction.ROLLBACK,
        prior,
        compute_transition_payload_sha256(prior, CandidateAction.ROLLBACK),
        auth.authority_identity,
    )
    rolled = rollback_candidate_decision(prior, rollback, auth)
    assert rolled.active_after is False
    assert rolled.historical_receipt_preserved is True


def test_authority_or_payload_drift_fails_closed():
    inactive = authority(AuthorityStatus.INVALIDATED)
    prior = "candidate-decision:1"
    command = CandidateCommand(
        "invalidate",
        CandidateAction.INVALIDATE,
        prior,
        compute_transition_payload_sha256(prior, CandidateAction.INVALIDATE),
        inactive.authority_identity,
    )
    with pytest.raises(CandidateRoutingError) as inactive_error:
        invalidate_candidate_decision(prior, command, inactive)
    assert inactive_error.value.code == "INACTIVE_AUTHORITY"

    auth = authority()
    drift = CandidateCommand("invalidate", CandidateAction.INVALIDATE, prior, digest("wrong"), auth.authority_identity)
    with pytest.raises(CandidateRoutingError) as drift_error:
        invalidate_candidate_decision(prior, drift, auth)
    assert drift_error.value.code == "COMMAND_PAYLOAD_MISMATCH"
