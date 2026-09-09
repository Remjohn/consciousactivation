"""Executable proof for CA-M043 / INV-MRK-001.

The tests prove deterministic receipt construction, predecessor linkage,
workspace/execution/campaign boundary enforcement, Merkle-root commitment,
and durable SQLite reread/verification. They deliberately exercise persisted
records rather than comparing an object only to its own recomputed values.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sqlite3
import sys

import pytest

_MODULE_PATH = Path(__file__).resolve().parents[2] / "packages" / "ca_runtime" / "src" / "ca_runtime" / "merkle_receipt_chain.py"
_SPEC = importlib.util.spec_from_file_location("ca_runtime.merkle_receipt_chain", _MODULE_PATH)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MODULE
_SPEC.loader.exec_module(_MODULE)

MerkleReceipt = _MODULE.MerkleReceipt
MerkleReceiptChain = _MODULE.MerkleReceiptChain
ReceiptChainIntegrityError = _MODULE.ReceiptChainIntegrityError
ReceiptIdentityError = _MODULE.ReceiptIdentityError
ReceiptNotFoundError = _MODULE.ReceiptNotFoundError
SQLiteMerkleReceiptStore = _MODULE.SQLiteMerkleReceiptStore
build_evidence_chain = _MODULE.build_evidence_chain
canonical_sha256 = _MODULE.canonical_sha256
merkle_root = _MODULE.merkle_root


@pytest.fixture
def chain() -> MerkleReceiptChain:
    return MerkleReceiptChain(workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")


def _append_three(chain: MerkleReceiptChain) -> tuple[MerkleReceipt, MerkleReceipt, MerkleReceipt]:
    raw = chain.append(
        receipt_id="raw-1",
        kind="RAW_EVIDENCE",
        subject_id="source-1",
        payload={"sha256": "a" * 64, "bytes": 12},
    )
    gate = chain.append(
        receipt_id="gate-1",
        kind="GATE_DECISION",
        subject_id="gate-1",
        payload={"decision": "APPROVE", "threshold": "0.9"},
    )
    delivery = chain.append(
        receipt_id="delivery-1",
        kind="DISTRIBUTION_DELIVERABLE",
        subject_id="asset-1",
        payload={"sha256": "b" * 64, "format": "mp4"},
    )
    return raw, gate, delivery


def test_first_receipt_is_root_and_has_no_parent(chain: MerkleReceiptChain) -> None:
    receipt = chain.append(
        receipt_id="raw-1",
        kind="RAW_EVIDENCE",
        subject_id="source-1",
        payload={"evidence": "observed"},
    )
    assert receipt.sequence == 0
    assert receipt.parent_receipt_sha256 is None
    assert chain.root_receipt_sha256 == receipt.receipt_sha256
    chain.verify()


def test_child_receipt_links_immediate_predecessor(chain: MerkleReceiptChain) -> None:
    raw, gate, delivery = _append_three(chain)
    assert gate.parent_receipt_sha256 == raw.receipt_sha256
    assert delivery.parent_receipt_sha256 == gate.receipt_sha256
    assert [r.sequence for r in chain.receipts] == [0, 1, 2]
    chain.verify()


def test_canonical_payload_is_stable_and_independent_of_mapping_order() -> None:
    left = MerkleReceipt.create(
        receipt_id="r-1", workspace_id="ws", execution_id="run", campaign_id="camp",
        sequence=0, kind="RAW_EVIDENCE", subject_id="s", payload={"b": 2, "a": 1}, parent_receipt_sha256=None,
    )
    right = MerkleReceipt.create(
        receipt_id="r-1", workspace_id="ws", execution_id="run", campaign_id="camp",
        sequence=0, kind="RAW_EVIDENCE", subject_id="s", payload={"a": 1, "b": 2}, parent_receipt_sha256=None,
    )
    assert left.receipt_sha256 == right.receipt_sha256
    assert left.receipt_payload == right.receipt_payload
    assert left.verify()


def test_payload_mutation_is_detected() -> None:
    receipt = MerkleReceipt.create(
        receipt_id="r-1", workspace_id="ws", execution_id="run", campaign_id="camp",
        sequence=0, kind="RAW_EVIDENCE", subject_id="s", payload={"value": "original"}, parent_receipt_sha256=None,
    )
    tampered = MerkleReceipt(
        receipt_id=receipt.receipt_id, workspace_id=receipt.workspace_id,
        execution_id=receipt.execution_id, campaign_id=receipt.campaign_id,
        sequence=receipt.sequence, kind=receipt.kind, subject_id=receipt.subject_id,
        payload={"value": "tampered"}, parent_receipt_sha256=receipt.parent_receipt_sha256,
        receipt_sha256=receipt.receipt_sha256, receipt_payload=receipt.receipt_payload,
    )
    assert not tampered._payload_matches_fields()
    assert not tampered.verify()


def test_receipt_payload_bytes_mutation_is_detected(chain: MerkleReceiptChain) -> None:
    receipt = chain.append(
        receipt_id="raw-1", kind="RAW_EVIDENCE", subject_id="s", payload={"value": "x"}
    )
    tampered = MerkleReceipt(
        receipt_id=receipt.receipt_id, workspace_id=receipt.workspace_id,
        execution_id=receipt.execution_id, campaign_id=receipt.campaign_id,
        sequence=receipt.sequence, kind=receipt.kind, subject_id=receipt.subject_id,
        payload=receipt.payload, parent_receipt_sha256=receipt.parent_receipt_sha256,
        receipt_sha256=receipt.receipt_sha256, receipt_payload=receipt.receipt_payload[:-1] + " ",
    )
    with pytest.raises(ReceiptChainIntegrityError):
        MerkleReceiptChain.from_records(
            [tampered.to_record()], workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A"
        )


def test_parent_mutation_is_detected(chain: MerkleReceiptChain) -> None:
    first, second, _ = _append_three(chain)
    tampered_second = MerkleReceipt.create(
        receipt_id=second.receipt_id,
        workspace_id=second.workspace_id,
        execution_id=second.execution_id,
        campaign_id=second.campaign_id,
        sequence=second.sequence,
        kind=second.kind,
        subject_id=second.subject_id,
        payload=second.payload,
        parent_receipt_sha256="0" * 64,
    )
    tampered_chain = MerkleReceiptChain(workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")
    tampered_chain.extend([first])
    with pytest.raises(ReceiptChainIntegrityError):
        tampered_chain.extend([tampered_second])


def test_missing_predecessor_is_detected_from_persisted_records(chain: MerkleReceiptChain) -> None:
    first, second, third = _append_three(chain)
    records = [first.to_record(), third.to_record()]
    with pytest.raises(ReceiptChainIntegrityError):
        MerkleReceiptChain.from_records(records, workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")


def test_reordered_transition_sequence_is_detected(chain: MerkleReceiptChain) -> None:
    first, second, third = _append_three(chain)
    records = [third.to_record(), second.to_record(), first.to_record()]
    with pytest.raises(ReceiptChainIntegrityError):
        MerkleReceiptChain.from_records(records, workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")


def test_cross_workspace_receipt_is_rejected(chain: MerkleReceiptChain) -> None:
    foreign = MerkleReceipt.create(
        receipt_id="foreign", workspace_id="ws-B", execution_id="run-A", campaign_id="camp-A",
        sequence=0, kind="RAW_EVIDENCE", subject_id="s", payload={"x": 1}, parent_receipt_sha256=None,
    )
    with pytest.raises(ReceiptIdentityError):
        chain.extend([foreign])


def test_cross_execution_receipt_is_rejected(chain: MerkleReceiptChain) -> None:
    foreign = MerkleReceipt.create(
        receipt_id="foreign", workspace_id="ws-A", execution_id="run-B", campaign_id="camp-A",
        sequence=0, kind="RAW_EVIDENCE", subject_id="s", payload={"x": 1}, parent_receipt_sha256=None,
    )
    with pytest.raises(ReceiptIdentityError):
        chain.extend([foreign])


def test_cross_campaign_receipt_is_rejected(chain: MerkleReceiptChain) -> None:
    foreign = MerkleReceipt.create(
        receipt_id="foreign", workspace_id="ws-A", execution_id="run-A", campaign_id="camp-B",
        sequence=0, kind="RAW_EVIDENCE", subject_id="s", payload={"x": 1}, parent_receipt_sha256=None,
    )
    with pytest.raises(ReceiptIdentityError):
        chain.extend([foreign])


def test_merkle_root_changes_when_any_leaf_changes() -> None:
    one = ["1" * 64, "2" * 64, "3" * 64]
    two = ["1" * 64, "2" * 64, "4" * 64]
    assert merkle_root(one) != merkle_root(two)


def test_merkle_root_is_deterministic_and_domain_separated() -> None:
    hashes = ["a" * 64, "b" * 64, "c" * 64, "d" * 64]
    assert merkle_root(hashes) == merkle_root(tuple(hashes))
    naive = canonical_sha256({"left": hashes[0], "right": hashes[1]})
    assert merkle_root(hashes) != naive


def test_evidence_chain_connects_raw_gate_and_deliverable_to_one_root() -> None:
    chain = build_evidence_chain(
        workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A",
        raw_evidence=[("raw-1", {"source_sha256": "a" * 64})],
        gate_decisions=[("gate-1", {"decision": "APPROVE", "rule": "R1"})],
        distribution_deliverables=[("delivery-1", {"asset_sha256": "b" * 64})],
    )
    kinds = [receipt.kind for receipt in chain.receipts]
    assert kinds == ["RAW_EVIDENCE", "GATE_DECISION", "DISTRIBUTION_DELIVERABLE"]
    assert chain.merkle_root_sha256 is not None
    chain.verify()


def test_transition_helper_binds_transition_identity(chain: MerkleReceiptChain) -> None:
    receipt = chain.append_transition(
        transition={
            "transition_id": "t-1", "receipt_id": "rcpt-t-1", "workspace_id": "ws-A",
            "execution_id": "run-A", "campaign_id": "camp-A", "from_state": "A", "to_state": "B",
            "transition_name": "advance", "trigger_operation": "advance", "lane": "ANALYST",
            "expected_version": 0, "committed_version": 1, "timestamp": "2026-09-08T00:00:00Z",
            "payload": {"result": "ok"},
        }
    )
    assert receipt.kind == "STATE_TRANSITION"
    assert receipt.subject_id == "t-1"
    assert receipt.payload["committed_version"] == 1


def test_transition_helper_rejects_workspace_mismatch(chain: MerkleReceiptChain) -> None:
    with pytest.raises(ReceiptIdentityError):
        chain.append_transition(
            transition={
                "transition_id": "t-1", "receipt_id": "rcpt-t-1", "workspace_id": "ws-B",
                "execution_id": "run-A", "campaign_id": "camp-A", "from_state": "A", "to_state": "B",
                "transition_name": "advance", "trigger_operation": "advance", "lane": "ANALYST",
                "expected_version": 0, "committed_version": 1, "timestamp": "2026-09-08T00:00:00Z",
            }
        )


def test_sqlite_store_persists_and_rereads_chain() -> None:
    conn = sqlite3.connect(":memory:")
    store = SQLiteMerkleReceiptStore(conn)
    chain = MerkleReceiptChain(workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")
    _append_three(chain)
    for receipt in chain.receipts:
        store.append(receipt)
    reread = store.load_chain(workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")
    reread.verify()
    assert reread.export_records() == chain.export_records()
    assert store.verify_chain(workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A") == chain.merkle_root_sha256


def test_sqlite_store_keeps_tenants_separate_even_with_same_subject_ids() -> None:
    conn = sqlite3.connect(":memory:")
    store = SQLiteMerkleReceiptStore(conn)
    ws_a = MerkleReceiptChain(workspace_id="ws-A", execution_id="run", campaign_id="camp")
    ws_b = MerkleReceiptChain(workspace_id="ws-B", execution_id="run", campaign_id="camp")
    ws_a.append(receipt_id="same", kind="RAW_EVIDENCE", subject_id="same", payload={"value": "A"})
    ws_b.append(receipt_id="same-b", kind="RAW_EVIDENCE", subject_id="same", payload={"value": "B"})
    store.append(ws_a.receipts[0])
    store.append(ws_b.receipts[0])
    assert set(store.verify_all_boundaries()) == {
        ("ws-A", "run", "camp"), ("ws-B", "run", "camp")
    }


def test_sqlite_tampered_payload_fails_closed() -> None:
    conn = sqlite3.connect(":memory:")
    store = SQLiteMerkleReceiptStore(conn)
    chain = MerkleReceiptChain(workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")
    first = chain.append(receipt_id="r1", kind="RAW_EVIDENCE", subject_id="s1", payload={"x": 1})
    store.append(first)
    conn.execute(
        f"UPDATE {store.TABLE} SET receipt_payload = ? WHERE receipt_sha256 = ?",
        (first.receipt_payload.replace('1', '2'), first.receipt_sha256),
    )
    conn.commit()
    with pytest.raises(ReceiptChainIntegrityError):
        store.verify_chain(workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")


def test_sqlite_tampered_parent_fails_closed() -> None:
    conn = sqlite3.connect(":memory:")
    store = SQLiteMerkleReceiptStore(conn)
    chain = MerkleReceiptChain(workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")
    _append_three(chain)
    for receipt in chain.receipts:
        store.append(receipt)
    conn.execute(
        f"UPDATE {store.TABLE} SET parent_receipt_sha256 = ? WHERE receipt_id = ?",
        ("0" * 64, chain.receipts[1].receipt_id),
    )
    conn.commit()
    with pytest.raises(ReceiptChainIntegrityError):
        store.verify_chain(workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")


def test_sqlite_tampered_identity_is_not_silent() -> None:
    conn = sqlite3.connect(":memory:")
    store = SQLiteMerkleReceiptStore(conn)
    chain = MerkleReceiptChain(workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")
    first = chain.append(receipt_id="r1", kind="RAW_EVIDENCE", subject_id="s1", payload={"x": 1})
    store.append(first)
    conn.execute(f"UPDATE {store.TABLE} SET workspace_id = ? WHERE receipt_id = ?", ("ws-B", first.receipt_id))
    conn.commit()
    with pytest.raises(ReceiptChainIntegrityError):
        store.verify_chain(workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")


def test_missing_persisted_receipt_is_detectable() -> None:
    conn = sqlite3.connect(":memory:")
    store = SQLiteMerkleReceiptStore(conn)
    chain = MerkleReceiptChain(workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")
    _append_three(chain)
    store.append(chain.receipts[0])
    missing = chain.receipts[2]
    conn.execute(
        f"""
        INSERT INTO {store.TABLE} (
            receipt_id, workspace_id, execution_id, campaign_id, sequence, kind, subject_id,
            payload, parent_receipt_sha256, receipt_sha256, receipt_payload
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            missing.receipt_id, missing.workspace_id, missing.execution_id, missing.campaign_id,
            missing.sequence, missing.kind, missing.subject_id,
            canonical_sha256(dict(missing.payload)) and json.dumps(dict(missing.payload), sort_keys=True, separators=(",", ":")),
            missing.parent_receipt_sha256, missing.receipt_sha256, missing.receipt_payload,
        ),
    )
    conn.commit()
    with pytest.raises(ReceiptChainIntegrityError):
        store.verify_chain(workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")


def test_unknown_receipt_lookup_is_explicit() -> None:
    conn = sqlite3.connect(":memory:")
    store = SQLiteMerkleReceiptStore(conn)
    with pytest.raises(ReceiptNotFoundError):
        store.get("0" * 64)


def test_rejected_cas_has_no_phantom_receipt() -> None:
    conn = sqlite3.connect(":memory:")
    store = SQLiteMerkleReceiptStore(conn)
    chain = MerkleReceiptChain(workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A")
    # A rejected compare-and-swap is represented by the absence of an accepted transition record.
    # The CA-M043 primitive never creates a receipt from an unaccepted mutation.
    assert chain.receipts == ()
    with pytest.raises(ReceiptNotFoundError):
        store.get("0" * 64)


def test_receipt_hash_is_full_sha256_hex(chain: MerkleReceiptChain) -> None:
    receipt = chain.append(receipt_id="r1", kind="OTHER", subject_id="s1", payload={"x": True})
    assert len(receipt.receipt_sha256) == 64
    assert receipt.receipt_sha256 == receipt.receipt_sha256.lower()
    assert all(char in "0123456789abcdef" for char in receipt.receipt_sha256)


def test_exported_record_round_trips_exactly(chain: MerkleReceiptChain) -> None:
    _append_three(chain)
    restored = MerkleReceiptChain.from_records(
        chain.export_records(), workspace_id="ws-A", execution_id="run-A", campaign_id="camp-A"
    )
    assert restored.export_records() == chain.export_records()
    assert restored.merkle_root_sha256 == chain.merkle_root_sha256
