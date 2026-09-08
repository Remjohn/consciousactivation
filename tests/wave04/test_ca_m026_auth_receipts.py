"""CA-M026 / FR-AUTH-001 durable authorization receipt tests."""

from __future__ import annotations

import hashlib
import sqlite3

import pytest

from ca_runtime.auth_decision_receipts import (
    AuthorizationDecision,
    AuthorizationDecisionReceiptStore,
    AuthorizationReceiptIntegrityError,
    InvalidAuthorizationReceiptError,
)


KEY = b"CA-M026-test-signing-key"
POLICY_HASH = hashlib.sha256(b"policy-v1").hexdigest()
STATE_HASH = hashlib.sha256(b"resource-r7").hexdigest()


def make_store(tmp_path):
    return AuthorizationDecisionReceiptStore(tmp_path / "authorization.sqlite3", KEY)


def common(**overrides):
    value = {
        "actor_id": "operator-001",
        "decision_reason": "Policy and evidence checks passed",
        "policy_hash": POLICY_HASH,
        "resource_id": "execution-001",
        "resource_revision": "R7",
        "resource_state_hash": STATE_HASH,
        "timestamp": "2026-09-08T11:00:00Z",
    }
    value.update(overrides)
    return value


def test_records_grant_with_required_identity_reason_policy_and_timestamp(tmp_path):
    with make_store(tmp_path) as store:
        receipt = store.grant(**common())

        assert receipt.decision is AuthorizationDecision.GRANT
        assert receipt.actor_id == "operator-001"
        assert receipt.decision_reason == "Policy and evidence checks passed"
        assert receipt.policy_hash == POLICY_HASH
        assert receipt.timestamp == "2026-09-08T11:00:00Z"
        assert receipt.resource_revision == "R7"
        assert receipt.receipt_hash
        assert receipt.signature
        assert store.count() == 1
        assert store.verify_receipt(receipt.receipt_id) == receipt


def test_records_denial_as_a_first_class_receipt(tmp_path):
    with make_store(tmp_path) as store:
        receipt = store.deny(
            **common(
                actor_id="operator-002",
                decision_reason="Actor lacks production authorization",
            )
        )

        assert receipt.decision is AuthorizationDecision.DENY
        assert receipt.actor_id == "operator-002"
        assert receipt.decision_reason == "Actor lacks production authorization"
        assert store.verify_chain() == [receipt]


def test_records_operator_override_as_distinct_governed_outcome(tmp_path):
    with make_store(tmp_path) as store:
        receipt = store.operator_override(
            **common(
                actor_id="commander-001",
                decision_reason="Commander approved documented emergency override",
            )
        )

        assert receipt.decision is AuthorizationDecision.OPERATOR_OVERRIDE
        assert receipt.actor_id == "commander-001"
        assert receipt.policy_hash == POLICY_HASH
        assert store.verify_receipt(receipt.receipt_id)


def test_receipts_are_hash_chained_in_append_order(tmp_path):
    with make_store(tmp_path) as store:
        first = store.grant(**common())
        second = store.deny(
            **common(
                decision_reason="Second policy check denied the request",
                resource_revision="R8",
                resource_state_hash=hashlib.sha256(b"resource-r8").hexdigest(),
                timestamp="2026-09-08T11:01:00Z",
            )
        )

        assert first.previous_receipt_hash is None
        assert second.previous_receipt_hash == first.receipt_hash
        assert store.verify_chain() == [first, second]


def test_persistence_survives_close_and_fresh_process_style_reopen(tmp_path):
    db = tmp_path / "authorization.sqlite3"

    first_store = AuthorizationDecisionReceiptStore(db, KEY)
    receipt = first_store.grant(**common())
    first_store.close()

    reopened = AuthorizationDecisionReceiptStore(db, KEY)
    try:
        assert reopened.get(receipt.receipt_id) == receipt
        assert reopened.verify_chain() == [receipt]
    finally:
        reopened.close()


def test_tampering_with_persisted_content_is_detected(tmp_path):
    db = tmp_path / "authorization.sqlite3"
    with make_store(tmp_path) as store:
        receipt = store.grant(**common())

    # Direct DB tampering is deliberately performed outside the normal API.
    connection = sqlite3.connect(db)
    # SQLite's trigger blocks normal UPDATE, so simulate an attacker that has
    # already bypassed the application layer by disabling the guard.
    connection.execute("DROP TRIGGER trg_cae_auth_receipt_no_update")
    connection.execute(
        """
        UPDATE cae_authorization_decision_receipt
        SET decision_reason = ?
        WHERE receipt_id = ?
        """,
        ("tampered reason", receipt.receipt_id),
    )
    connection.commit()
    connection.close()

    with AuthorizationDecisionReceiptStore(db, KEY) as verifier:
        with pytest.raises(AuthorizationReceiptIntegrityError):
            verifier.verify_chain()


def test_wrong_signing_key_is_detected_after_restart(tmp_path):
    db = tmp_path / "authorization.sqlite3"
    with make_store(tmp_path) as store:
        receipt = store.grant(**common())

    with AuthorizationDecisionReceiptStore(db, b"a-different-key") as verifier:
        with pytest.raises(AuthorizationReceiptIntegrityError):
            verifier.verify_receipt(receipt.receipt_id)


def test_append_only_database_guard_rejects_update_and_delete(tmp_path):
    with make_store(tmp_path) as store:
        receipt = store.grant(**common())

        with pytest.raises(sqlite3.IntegrityError, match="IMMUTABLE"):
            store._conn.execute(
                "UPDATE cae_authorization_decision_receipt SET actor_id = ? WHERE receipt_id = ?",
                ("attacker", receipt.receipt_id),
            )

        with pytest.raises(sqlite3.IntegrityError, match="IMMUTABLE"):
            store._conn.execute(
                "DELETE FROM cae_authorization_decision_receipt WHERE receipt_id = ?",
                (receipt.receipt_id,),
            )

        assert store.verify_chain() == [receipt]


@pytest.mark.parametrize(
    "missing",
    ["actor_id", "decision_reason", "policy_hash", "resource_id", "resource_revision", "resource_state_hash"],
)
def test_required_receipt_fields_fail_closed(tmp_path, missing):
    values = common()
    values[missing] = ""
    with make_store(tmp_path) as store:
        with pytest.raises(InvalidAuthorizationReceiptError):
            store.grant(**values)


def test_invalid_policy_hash_fails_closed(tmp_path):
    with make_store(tmp_path) as store:
        with pytest.raises(InvalidAuthorizationReceiptError, match="policy_hash"):
            store.grant(**common(policy_hash="not-a-sha256"))


def test_revision_binding_distinguishes_stale_inspection_from_current_revision(tmp_path):
    with make_store(tmp_path) as store:
        inspected = store.grant(**common())

        current_hash = hashlib.sha256(b"resource-r8").hexdigest()
        assert store.verify_resource_revision(
            resource_id="execution-001",
            resource_revision="R7",
            resource_state_hash=STATE_HASH,
        )
        assert not store.verify_resource_revision(
            resource_id="execution-001",
            resource_revision="R8",
            resource_state_hash=current_hash,
        )
        assert inspected.resource_revision == "R7"


def test_conflicting_duplicate_receipt_id_does_not_overwrite_history(tmp_path):
    with make_store(tmp_path) as store:
        first = store.grant(**common(receipt_id="stable-receipt"))
        with pytest.raises(Exception):
            store.deny(
                **common(
                    receipt_id="stable-receipt",
                    decision_reason="Conflicting later decision",
                )
            )

        assert store.count() == 1
        assert store.get("stable-receipt") == first


def test_false_proof_countercase_actor_and_decision_strings_do_not_prove_integrity(tmp_path):
    """A UI/parser can display valid-looking fields without a valid receipt.

    The verifier must reject a forged hash/signature rather than trusting the
    actor, decision, or reason strings alone.
    """
    with make_store(tmp_path) as store:
        receipt = store.grant(**common())
        forged = receipt.to_dict()
        forged["actor_id"] = "spoofed-operator"
        forged["decision"] = "GRANT"

        connection = sqlite3.connect(store.db_path)
        connection.execute("DROP TRIGGER trg_cae_auth_receipt_no_update")
        connection.execute(
            """
            UPDATE cae_authorization_decision_receipt
            SET actor_id = ?
            WHERE receipt_id = ?
            """,
            (forged["actor_id"], receipt.receipt_id),
        )
        connection.commit()
        connection.close()

        with pytest.raises(AuthorizationReceiptIntegrityError):
            store.verify_receipt(receipt.receipt_id)
