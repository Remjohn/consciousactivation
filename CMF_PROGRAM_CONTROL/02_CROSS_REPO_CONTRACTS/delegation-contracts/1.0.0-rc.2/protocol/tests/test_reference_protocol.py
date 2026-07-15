from __future__ import annotations

from copy import deepcopy
from dataclasses import replace

import pytest

from cmf_delegation_protocol import PersistenceError, ProtocolRejection, sign_envelope
from cmf_delegation_validators.canonical import canonical_hash
from cmf_delegation_validators.contracts import validate_payload

from .helpers import Harness, payload, rewrite_identity


def test_single_asset_submission_result_and_acknowledgement() -> None:
    harness = Harness()
    correlation = "corr-happy"
    harness.to_completed(correlation)

    audit = harness.store.audit(correlation)
    assert harness.store.state(correlation) == "COMPLETED"
    assert len(audit) == 7
    assert len(harness.store.outbox()) == 7
    assert [record.receipt["previous_receipt_hash"] for record in audit] == [
        None,
        *[record.record_hash for record in audit[:-1]],
    ]
    for record in audit:
        validate_payload("delegation-audit-receipt", record.receipt)


def test_exact_retry_is_idempotent_without_new_effect() -> None:
    harness = Harness()
    body = payload("visual-asset-demand")
    envelope = harness.message(
        "visual-asset-demand", body, "CONTENT_HARNESS", "corr-idempotent"
    )
    first = harness.engine.process(envelope, body)
    second = harness.engine.process(envelope, body)

    assert first.accepted and second.accepted and second.idempotent
    assert len(harness.store.audit("corr-idempotent")) == 1
    assert len(harness.store.outbox()) == 1


def test_idempotency_conflict_is_rejected_and_receipted() -> None:
    harness = Harness()
    first = payload("visual-asset-demand")
    assert harness.send(
        "visual-asset-demand",
        first,
        "CONTENT_HARNESS",
        "corr-idem-conflict",
        idempotency_key="fixed-key",
    )[0].accepted
    changed = deepcopy(first)
    changed["notes"] = "different signed command"
    rejected, _ = harness.send(
        "visual-asset-demand",
        changed,
        "CONTENT_HARNESS",
        "corr-idem-conflict",
        idempotency_key="fixed-key",
    )

    assert not rejected.accepted
    assert rejected.code == "IDEMPOTENCY_CONFLICT"
    assert len(harness.store.audit("corr-idem-conflict")) == 2


def test_message_id_and_nonce_replay_are_rejected() -> None:
    harness = Harness()
    original = payload("visual-asset-demand")
    first, first_envelope = harness.send(
        "visual-asset-demand", original, "CONTENT_HARNESS", "corr-replay"
    )
    assert first.accepted
    changed = deepcopy(original)
    changed["notes"] = "replay mutation"
    message_replay, _ = harness.send(
        "visual-asset-demand",
        changed,
        "CONTENT_HARNESS",
        "corr-replay",
        message_id=first_envelope["message_id"],
    )
    nonce_replay, _ = harness.send(
        "visual-asset-demand",
        changed,
        "CONTENT_HARNESS",
        "corr-replay",
        nonce=first_envelope["integrity"]["nonce"],
    )
    assert message_replay.code == "PROTOCOL_REPLAY_DETECTED"
    assert nonce_replay.code == "PROTOCOL_REPLAY_DETECTED"


def test_forged_and_expired_signatures_are_rejected() -> None:
    harness = Harness()
    body = payload("visual-asset-demand")
    forged = harness.message(
        "visual-asset-demand", body, "CONTENT_HARNESS", "corr-forged"
    )
    forged["integrity"]["signature"] = "A" * 86
    assert harness.engine.process(forged, body).code == "SIGNATURE_INVALID"

    expired = harness.message(
        "visual-asset-demand", body, "CONTENT_HARNESS", "corr-expired"
    )
    expired["integrity"]["expires_at"] = "2026-07-14T09:00:00Z"
    expired = sign_envelope(harness.keys["CONTENT_HARNESS"], expired, body)
    assert harness.engine.process(expired, body).code == "SIGNATURE_EXPIRED"


def test_schema_hash_and_authority_failures_are_rejected() -> None:
    harness = Harness()
    body = payload("visual-asset-demand")
    invalid = deepcopy(body)
    invalid["unexpected"] = True
    envelope = harness.message(
        "visual-asset-demand", invalid, "CONTENT_HARNESS", "corr-schema"
    )
    assert harness.engine.process(envelope, invalid).code == "PAYLOAD_SCHEMA_INVALID"

    envelope = harness.message(
        "visual-asset-demand", body, "CONTENT_HARNESS", "corr-hash"
    )
    envelope["payload_hash"] = "sha256:" + "0" * 64
    envelope = sign_envelope(harness.keys["CONTENT_HARNESS"], envelope, body)
    assert harness.engine.process(envelope, body).code == "PAYLOAD_HASH_MISMATCH"

    denied = harness.message(
        "visual-asset-demand", body, "VISUAL_ASSET_EDITOR", "corr-authority"
    )
    assert harness.engine.process(denied, body).code == "AUTHORITY_DENIED"


def test_compatibility_is_required_and_immutable() -> None:
    harness = Harness()
    _, _, _, identity = harness.record_demand("corr-compatibility")
    submission = rewrite_identity(payload("visual-asset-submission"), identity)
    rejected, _ = harness.send(
        "visual-asset-submission",
        submission,
        "CONTENT_HARNESS",
        "corr-compatibility",
    )
    assert rejected.code == "COMPATIBILITY_PROFILE_REQUIRED"
    profile = harness.pin("corr-compatibility")
    assert profile["protocol_version"] == "1.0"
    with pytest.raises(ProtocolRejection, match="COMPATIBILITY_PROFILE_IMMUTABLE"):
        harness.engine.pin_compatibility(
            "corr-compatibility",
            {
                "protocol_versions": ["1.0"],
                "required_features": ["authority.registry"],
                "signature_algorithms": ["Ed25519"],
            },
            {
                "protocol_versions": ["1.0"],
                "required_features": ["authority.registry"],
                "signature_algorithms": ["Ed25519"],
            },
        )


def test_illegal_lifecycle_event_is_rejected_without_state_change() -> None:
    harness = Harness()
    _, _, _, identity = harness.record_demand("corr-illegal")
    event = rewrite_identity(payload("visual-asset-event"), identity)
    result, _ = harness.send(
        "visual-asset-event", event, "VISUAL_ASSET_EDITOR", "corr-illegal"
    )
    assert result.code == "ILLEGAL_LIFECYCLE_TRANSITION"
    assert result.state == "DRAFT"


def test_atomic_commit_failure_leaves_no_protocol_effect() -> None:
    harness = Harness()
    body = payload("visual-asset-demand")
    envelope = harness.message(
        "visual-asset-demand", body, "CONTENT_HARNESS", "corr-atomic"
    )
    before = harness.store.snapshot()
    harness.store.fail_next_commit()
    with pytest.raises(PersistenceError):
        harness.engine.process(envelope, body)
    assert harness.store.snapshot() == before


def test_cancellation_flow() -> None:
    harness = Harness()
    _, identity, _ = harness.to_accepted("corr-cancel")
    request = rewrite_identity(payload("cancellation-request"), identity)
    requested, _ = harness.send(
        "cancellation-request", request, "CONTENT_HARNESS", "corr-cancel"
    )
    assert requested.state == "CANCELLATION_REQUESTED"
    receipt = rewrite_identity(payload("cancellation-receipt"), identity)
    cancelled, _ = harness.send(
        "cancellation-receipt", receipt, "VISUAL_ASSET_EDITOR", "corr-cancel"
    )
    assert cancelled.state == "CANCELLED"


def test_amendment_and_supersession_flow() -> None:
    harness = Harness()
    _, identity, _ = harness.to_accepted("corr-amend")
    proposal = rewrite_identity(payload("amendment-proposal"), identity)
    proposed, _ = harness.send(
        "amendment-proposal", proposal, "VISUAL_ASSET_EDITOR", "corr-amend"
    )
    assert proposed.state == "AMENDMENT_REQUIRED"
    response = payload("amendment-response")
    responded, _ = harness.send(
        "amendment-response", response, "CONTENT_HARNESS", "corr-amend"
    )
    assert responded.accepted and responded.state == "AMENDMENT_REQUIRED"
    supersession = payload("demand-supersession")
    supersession["superseded_demand"] = deepcopy(identity)
    superseded, _ = harness.send(
        "demand-supersession", supersession, "CONTENT_HARNESS", "corr-amend"
    )
    assert superseded.state == "SUPERSEDED"


def test_invalidation_replacement_and_acknowledgement() -> None:
    harness = Harness()
    _, demand_identity, result_identity = harness.to_completed("corr-replace")
    invalidation = rewrite_identity(
        rewrite_identity(payload("invalidation-notice"), demand_identity),
        result_identity,
        "result",
    )
    invalidated, _ = harness.send(
        "invalidation-notice", invalidation, "CONTENT_HARNESS", "corr-replace"
    )
    assert invalidated.state == "INVALIDATED"

    replacement = rewrite_identity(
        rewrite_identity(payload("replacement-notice"), demand_identity),
        result_identity,
        "result",
    )
    replacement_identity = deepcopy(replacement["replacement_result"])
    replacement["replaced_result"] = deepcopy(result_identity)
    noticed, _ = harness.send(
        "replacement-notice", replacement, "VISUAL_ASSET_EDITOR", "corr-replace"
    )
    assert noticed.state == "INVALIDATED"
    acknowledgement = rewrite_identity(
        rewrite_identity(payload("result-acknowledgement"), demand_identity),
        replacement_identity,
        "result",
    )
    acknowledged, _ = harness.send(
        "result-acknowledgement",
        acknowledgement,
        "CONTENT_HARNESS",
        "corr-replace",
    )
    assert acknowledged.state == "REPLACED"


def test_delegation_set_is_stored_and_cycles_are_rejected() -> None:
    harness = Harness()
    body = payload("delegation-set")
    accepted, _ = harness.send(
        "delegation-set", body, "CONTENT_HARNESS", "corr-set"
    )
    assert accepted.accepted
    stored = harness.store.delegation_set(body["set_id"])
    assert stored is not None and len(stored.member_demands) == 3

    cyclic = deepcopy(body)
    cyclic["set_id"] = "set-format02-cycle"
    cyclic["dependency_edges"].append(
        {
            "kind": "ORDER_BEFORE",
            "predecessor": deepcopy(cyclic["member_demands"][2]),
            "successor": deepcopy(cyclic["member_demands"][0]),
        }
    )
    rejected, _ = harness.send(
        "delegation-set", cyclic, "CONTENT_HARNESS", "corr-set-cycle"
    )
    assert rejected.code == "DELEGATION_SET_CYCLE"


def test_result_identity_mismatch_is_rejected() -> None:
    harness = Harness()
    _, demand_identity, _ = harness.to_in_progress("corr-result-mismatch")
    contract = rewrite_identity(payload("asset-result-contract"), demand_identity)
    result, _ = harness.send(
        "asset-result-contract",
        contract,
        "VISUAL_ASSET_EDITOR",
        "corr-result-mismatch",
    )
    assert result.state == "RESULT_READY"
    acknowledgement = rewrite_identity(
        payload("result-acknowledgement"), demand_identity
    )
    rejected, _ = harness.send(
        "result-acknowledgement",
        acknowledgement,
        "CONTENT_HARNESS",
        "corr-result-mismatch",
    )
    assert rejected.code == "RESULT_IDENTITY_MISMATCH"

