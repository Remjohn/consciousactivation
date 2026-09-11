from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import replace

import pytest

from cmf_delegation_protocol import PersistenceError, ProtocolRejection, sign_envelope
from cmf_delegation_validators.canonical import canonical_hash
from cmf_delegation_validators.contracts import validate_payload

from .helpers import ROOT, Harness, payload, rewrite_identity


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


def test_envelope_protocol_and_visual_demand_message_versions_are_independent() -> None:
    harness = Harness()
    body = payload("visual-asset-demand")
    envelope = harness.message(
        "visual-asset-demand", body, "CONTENT_HARNESS", "corr-version-axes"
    )
    assert envelope["protocol_version"] == "1.0"
    assert envelope["message_version"] == "1.1"
    assert harness.engine.process(envelope, body).accepted


def test_wrong_reading_locks_are_mandatory_and_non_empty() -> None:
    harness = Harness()
    for index, invalid in enumerate(
        (
            {key: value for key, value in payload("visual-asset-demand").items() if key != "wrong_reading_locks"},
            {**payload("visual-asset-demand"), "wrong_reading_locks": []},
        ),
        start=1,
    ):
        rejected, _ = harness.send(
            "visual-asset-demand",
            invalid,
            "CONTENT_HARNESS",
            f"corr-wrong-reading-{index}",
        )
        assert rejected.code == "PAYLOAD_SCHEMA_INVALID"
        assert rejected.state == "DRAFT"


def test_semantic_lineage_survives_retry_and_mutation_replay_is_rejected() -> None:
    harness = Harness()
    body = payload("visual-asset-demand")
    original_lineage = deepcopy(body["activative_semantic_lineage"])
    envelope = harness.message(
        "visual-asset-demand", body, "CONTENT_HARNESS", "corr-lineage-replay"
    )
    first = harness.engine.process(envelope, body)
    retry = harness.engine.process(envelope, body)
    assert first.accepted and retry.accepted and retry.idempotent
    assert body["activative_semantic_lineage"] == original_lineage
    assert len(harness.store.audit("corr-lineage-replay")) == 1

    changed = deepcopy(body)
    changed["activative_semantic_lineage"]["expression_moment_refs"][0]["version"] = "2.0"
    replay = harness.message(
        "visual-asset-demand",
        changed,
        "CONTENT_HARNESS",
        "corr-lineage-replay",
        message_id=envelope["message_id"],
    )
    rejected = harness.engine.process(replay, changed)
    assert rejected.code == "PROTOCOL_REPLAY_DETECTED"
    assert harness.store.state("corr-lineage-replay") == "DRAFT"
    assert body["activative_semantic_lineage"]["reaction_receipt_refs"] == original_lineage[
        "reaction_receipt_refs"
    ]
    assert body["activative_semantic_lineage"]["expression_moment_refs"] == original_lineage[
        "expression_moment_refs"
    ]


def test_vae_protected_semantic_mutation_is_rejected_without_domain_effect() -> None:
    harness = Harness()
    body = payload("visual-asset-demand")
    body["visual_semantic_pack"]["recognition_intent"] = "VAE-authored reinterpretation"
    body["activation_contract"]["stance"] = "VAE-authored stance"
    rejected, _ = harness.send(
        "visual-asset-demand", body, "VISUAL_ASSET_EDITOR", "corr-constitutional-authority"
    )
    assert rejected.code == "AUTHORITY_DENIED"
    assert rejected.state == "DRAFT"
    assert harness.store.state("corr-constitutional-authority") == "DRAFT"
    assert len(harness.store.audit("corr-constitutional-authority")) == 1


@pytest.mark.parametrize(
    ("fixture_name", "failure_code"),
    [
        ("wrong-reading-unsupported.invalid.json", "SEMANTIC_ENFORCEMENT_UNSUPPORTED"),
        ("evaluator-gap.invalid.json", "EVALUATOR_EVIDENCE_MISSING"),
    ],
)
def test_behavioral_compatibility_gaps_fail_before_admission(
    fixture_name: str, failure_code: str
) -> None:
    harness = Harness()
    fixture_path = (
        ROOT
        / "packages"
        / "fixtures"
        / "compatibility"
        / "constitutional"
        / fixture_name
    )
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    with pytest.raises(ProtocolRejection, match="COMPATIBILITY_NEGOTIATION_FAILED") as exc:
        harness.engine.pin_compatibility(
            f"corr-{failure_code.lower()}", fixture["requester"], fixture["provider"]
        )
    assert failure_code in str(exc.value)
