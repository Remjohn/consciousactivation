"""CA-M044 persisted replay verification proof suite."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

from ca_contracts import canonical_sha256
from ca_runtime.merkle_receipt_chain import MerkleReceiptChain, SQLiteMerkleReceiptStore
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_state_runtime import ProgramStateTransition, _compute_state_hash
from ca_runtime.replay_engine import replay_and_verify_run


DB_SCHEMA = """
CREATE TABLE cae_program_state_aggregates (
    aggregate_id TEXT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    cae_run_id TEXT NOT NULL,
    program_id TEXT NOT NULL,
    program_version TEXT NOT NULL,
    current_state TEXT NOT NULL,
    state_data TEXT NOT NULL,
    version INTEGER NOT NULL,
    state_hash TEXT NOT NULL,
    lifecycle TEXT NOT NULL,
    last_receipt_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE cae_program_state_transitions (
    transition_id TEXT PRIMARY KEY,
    aggregate_id TEXT NOT NULL,
    from_state TEXT NOT NULL,
    to_state TEXT NOT NULL,
    transition_name TEXT NOT NULL,
    trigger_operation TEXT NOT NULL,
    lane TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    payload TEXT NOT NULL,
    expected_version INTEGER NOT NULL,
    committed_version INTEGER NOT NULL,
    receipt_id TEXT NOT NULL,
    timestamp TEXT NOT NULL
);

CREATE TABLE cae_program_state_replay_snapshots (
    aggregate_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    current_state TEXT NOT NULL,
    state_data TEXT NOT NULL,
    state_hash TEXT NOT NULL,
    lifecycle TEXT,
    last_receipt_id TEXT,
    PRIMARY KEY (aggregate_id, version)
);
"""


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(DB_SCHEMA)
    yield conn
    conn.close()


def _seed_run(conn: sqlite3.Connection) -> tuple[str, dict[str, str]]:
    aggregate_id = "prog-state:ws-a:demo:run-a"
    workspace_id = "ws-a"
    run_id = "run-a"
    campaign_id = "camp-a"
    initial = {"answer": "seed"}
    v1_hash = _compute_state_hash(aggregate_id, "demo", "1.0.0", "INITIAL", 1, initial)
    conn.execute(
        "INSERT INTO cae_program_state_aggregates VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (aggregate_id, workspace_id, run_id, "demo", "1.0.0", "COMPLETED", json.dumps({"answer": "final", "score": 7}), 3,
         _compute_state_hash(aggregate_id, "demo", "1.0.0", "COMPLETED", 3, {"answer": "final", "score": 7}),
         "COMPLETED", "r2", "2026-09-08T12:00:00Z", "2026-09-08T12:02:00Z"),
    )
    snapshots = [
        (1, "INITIAL", initial, v1_hash, "INITIALIZED", "r-init"),
        (2, "RUNNING", {"answer": "final"}, _compute_state_hash(aggregate_id, "demo", "1.0.0", "RUNNING", 2, {"answer": "final"}), "RUNNING", "r1"),
        (3, "COMPLETED", {"answer": "final", "score": 7}, _compute_state_hash(aggregate_id, "demo", "1.0.0", "COMPLETED", 3, {"answer": "final", "score": 7}), "COMPLETED", "r2"),
    ]
    for version, state, data, state_hash, lifecycle, receipt_id in snapshots:
        conn.execute(
            "INSERT INTO cae_program_state_replay_snapshots VALUES (?, ?, ?, ?, ?, ?, ?)",
            (aggregate_id, version, state, json.dumps(data), state_hash, lifecycle, receipt_id),
        )

    transitions = [
        {
            "transition_id": "t1", "from_state": "INITIAL", "to_state": "RUNNING", "name": "advance1",
            "receipt_id": "r1", "expected": 1, "committed": 2,
            "payload": {"state_updates": {"answer": "final"}},
        },
        {
            "transition_id": "t2", "from_state": "RUNNING", "to_state": "COMPLETED", "name": "advance2",
            "receipt_id": "r2", "expected": 2, "committed": 3,
            "payload": {"model_cache_key": "completion-2", "model_response_sha256": canonical_sha256({"state_updates": {"score": 7}})},
        },
    ]
    for item in transitions:
        conn.execute(
            "INSERT INTO cae_program_state_transitions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                item["transition_id"], aggregate_id, item["from_state"], item["to_state"], item["name"],
                "demo.op@1.0.0", AuthorityLane.ANALYST.value, "actor", json.dumps(item["payload"]),
                item["expected"], item["committed"], item["receipt_id"], "2026-09-08T12:00:00Z",
            ),
        )

    chain = MerkleReceiptChain(workspace_id=workspace_id, execution_id=run_id, campaign_id=campaign_id)
    chain.append(receipt_id="r0", kind="OTHER", subject_id="init", payload={"version": 1})
    for item in transitions:
        chain.append_transition(
            transition={
                "transition_id": item["transition_id"], "receipt_id": item["receipt_id"],
                "workspace_id": workspace_id, "execution_id": run_id, "campaign_id": campaign_id,
                "from_state": item["from_state"], "to_state": item["to_state"],
                "transition_name": item["name"], "trigger_operation": "demo.op@1.0.0",
                "lane": AuthorityLane.ANALYST.value, "expected_version": item["expected"],
                "committed_version": item["committed"], "timestamp": "2026-09-08T12:00:00Z",
                "payload": item["payload"],
            }
        )
    store = SQLiteMerkleReceiptStore(conn)
    for receipt in chain.receipts:
        store.append(receipt)
    conn.commit()
    return aggregate_id, {"completion-2": {"state_updates": {"score": 7}}}


def test_positive_multistep_replay_is_bit_for_bit_and_uses_reopened_storage(db):
    aggregate_id, cache = _seed_run(db)
    result = replay_and_verify_run(db, aggregate_id=aggregate_id, campaign_id="camp-a", model_response_cache=cache)
    assert result.passed
    assert result.verified_versions == (1, 2, 3)
    assert result.final_state_hash == result.persisted_final_state_hash
    assert result.model_responses_verified
    assert [step.version for step in result.steps] == [2, 3]


def test_replay_reports_first_single_field_snapshot_corruption(db):
    aggregate_id, cache = _seed_run(db)
    db.execute(
        "UPDATE cae_program_state_replay_snapshots SET state_data = ? WHERE aggregate_id = ? AND version = 3",
        (json.dumps({"answer": "final", "score": 8}), aggregate_id),
    )
    result = replay_and_verify_run(db, aggregate_id=aggregate_id, campaign_id="camp-a", model_response_cache=cache)
    assert not result.passed
    assert result.status == "FAIL"
    assert result.mismatch is not None
    assert result.mismatch.reason_code == "PERSISTED_SNAPSHOT_TAMPER"
    assert result.mismatch.version == 3


def test_replay_fails_at_first_missing_transition(db):
    aggregate_id, cache = _seed_run(db)
    db.execute("DELETE FROM cae_program_state_transitions WHERE transition_id = 't1'")
    db.commit()
    result = replay_and_verify_run(db, aggregate_id=aggregate_id, campaign_id="camp-a", model_response_cache=cache)
    assert result.status == "FAIL"
    assert result.mismatch is not None
    assert result.mismatch.reason_code == "TRANSITION_VERSION_GAP"


def test_reordered_transition_is_detected_without_skipping_it(db):
    aggregate_id, cache = _seed_run(db)
    db.execute("UPDATE cae_program_state_transitions SET committed_version = 4 WHERE transition_id = 't1'")
    db.commit()
    result = replay_and_verify_run(db, aggregate_id=aggregate_id, campaign_id="camp-a", model_response_cache=cache)
    assert result.status in {"FAIL", "EVIDENCE_GAP"}
    assert result.mismatch is not None
    assert result.mismatch.reason_code in {"TRANSITION_VERSION_GAP", "REPLAY_EVIDENCE_GAP", "FINAL_VERSION_MISMATCH"}


def test_receipt_parent_tampering_fails_closed(db):
    aggregate_id, cache = _seed_run(db)
    db.execute(
        "UPDATE cae_merkle_receipts SET parent_receipt_sha256 = ? WHERE receipt_id = 'r1'",
        ("0" * 64,),
    )
    db.commit()
    result = replay_and_verify_run(db, aggregate_id=aggregate_id, campaign_id="camp-a", model_response_cache=cache)
    assert result.status == "FAIL"
    assert result.mismatch is not None
    assert result.mismatch.reason_code == "RECEIPT_CHAIN_INTEGRITY_FAILURE"


def test_model_completion_cache_tampering_fails_closed(db):
    aggregate_id, _ = _seed_run(db)
    cache = {"completion-2": {"state_updates": {"score": 8}}}
    result = replay_and_verify_run(db, aggregate_id=aggregate_id, campaign_id="camp-a", model_response_cache=cache)
    assert result.status == "FAIL"
    assert result.mismatch is not None
    assert result.mismatch.reason_code == "MODEL_RESPONSE_TAMPER"


def test_missing_model_completion_is_an_evidence_gap(db):
    aggregate_id, _ = _seed_run(db)
    result = replay_and_verify_run(db, aggregate_id=aggregate_id, campaign_id="camp-a", model_response_cache={})
    assert result.status == "EVIDENCE_GAP"
    assert result.mismatch is not None
    assert result.mismatch.reason_code == "REPLAY_EVIDENCE_GAP"


def test_current_runtime_schema_without_historical_snapshots_is_not_accepted_as_proof(tmp_path: Path):
    db_path = tmp_path / "current-runtime.sqlite"
    conn = sqlite3.connect(db_path)
    conn.executescript(
        """
        CREATE TABLE cae_program_state_aggregates (
            aggregate_id TEXT PRIMARY KEY, workspace_id TEXT, cae_run_id TEXT, program_id TEXT,
            program_version TEXT, current_state TEXT, state_data TEXT, version INTEGER,
            state_hash TEXT, lifecycle TEXT, last_receipt_id TEXT, created_at TEXT, updated_at TEXT
        );
        CREATE TABLE cae_program_state_transitions (
            transition_id TEXT PRIMARY KEY, aggregate_id TEXT, from_state TEXT, to_state TEXT,
            transition_name TEXT, trigger_operation TEXT, lane TEXT, actor_id TEXT, payload TEXT,
            expected_version INTEGER, committed_version INTEGER, receipt_id TEXT, timestamp TEXT
        );
        """
    )
    aggregate_id = "a"
    state = {"x": 2}
    final_hash = _compute_state_hash(aggregate_id, "demo", "1.0.0", "DONE", 2, state)
    conn.execute(
        "INSERT INTO cae_program_state_aggregates VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (aggregate_id, "ws", "run", "demo", "1.0.0", "DONE", json.dumps(state), 2, final_hash, "COMPLETED", "r1", "t", "t"),
    )
    conn.execute(
        "INSERT INTO cae_program_state_transitions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("t1", aggregate_id, "INITIAL", "DONE", "done", "op", AuthorityLane.ANALYST.value, "actor", json.dumps({"state_updates": {"x": 2}}), 1, 2, "r1", "t"),
    )
    conn.commit()
    conn.close()
    result = replay_and_verify_run(db_path, aggregate_id=aggregate_id)
    assert result.status == "EVIDENCE_GAP"
    assert result.mismatch is not None
    assert result.mismatch.reason_code == "PERSISTED_SNAPSHOT_LEDGER_MISSING"


def test_replay_is_read_only(db):
    aggregate_id, cache = _seed_run(db)
    before = dict(db.execute("SELECT * FROM cae_program_state_aggregates WHERE aggregate_id = ?", (aggregate_id,)).fetchone())
    transition_count_before = db.execute("SELECT COUNT(*) FROM cae_program_state_transitions").fetchone()[0]
    receipt_count_before = db.execute("SELECT COUNT(*) FROM cae_merkle_receipts").fetchone()[0]
    result = replay_and_verify_run(db, aggregate_id=aggregate_id, campaign_id="camp-a", model_response_cache=cache)
    after = dict(db.execute("SELECT * FROM cae_program_state_aggregates WHERE aggregate_id = ?", (aggregate_id,)).fetchone())
    assert result.passed
    assert after == before
    assert db.execute("SELECT COUNT(*) FROM cae_program_state_transitions").fetchone()[0] == transition_count_before
    assert db.execute("SELECT COUNT(*) FROM cae_merkle_receipts").fetchone()[0] == receipt_count_before


def test_replay_result_serialization_is_canonical_and_rerunnable(db):
    aggregate_id, cache = _seed_run(db)
    first = replay_and_verify_run(db, aggregate_id=aggregate_id, campaign_id="camp-a", model_response_cache=cache)
    second = replay_and_verify_run(db, aggregate_id=aggregate_id, campaign_id="camp-a", model_response_cache=cache)
    assert canonical_sha256(first.to_dict()) == canonical_sha256(second.to_dict())
    assert first.to_dict() == second.to_dict()
