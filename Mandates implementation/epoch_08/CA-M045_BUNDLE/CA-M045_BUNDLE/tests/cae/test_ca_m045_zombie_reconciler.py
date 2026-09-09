"""Executable proof for CA-M045 / INV-REC-001.

The tests exercise the real durable SQLite lease/aggregate/transition boundary.
They deliberately avoid directly setting lifecycle state to prove the recovery:
the startup reconciler must discover the expired lease, win the lease/aggregate
CAS predicates, reclaim the lock, persist PAUSED, and append one immutable
reconciliation transition.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3

import pytest

from ca_runtime.program_state_runtime import (
    ProgramStateAggregate,
    ProgramStateLifecycle,
    SqliteProgramStateStore,
    _compute_state_hash,
)
from ca_runtime.zombie_reconciler import (
    ZombieLeaseReconciler,
    ZombieLeaseReconciliationError,
    reconcile_on_startup,
)


AS_OF = "2026-09-08T12:00:00Z"
EXPIRED = "2026-09-08T11:59:59Z"
FUTURE = "2026-09-08T12:00:01Z"


def _make_aggregate(
    *,
    aggregate_id: str,
    workspace_id: str,
    lifecycle: ProgramStateLifecycle = ProgramStateLifecycle.RUNNING,
    version: int = 1,
) -> ProgramStateAggregate:
    state_data = {
        "lease_status": "LEASE_ACQUIRED",
        "lease_version": 1,
        "work": {"step": "run"},
    }
    state_hash = _compute_state_hash(
        aggregate_id=aggregate_id,
        program_id="interview_semantic_program",
        program_version="1.0.0",
        current_state="QUESTIONING",
        version=version,
        state_data=state_data,
    )
    return ProgramStateAggregate(
        aggregate_id=aggregate_id,
        workspace_id=workspace_id,
        cae_run_id=f"run-{aggregate_id}",
        program_id="interview_semantic_program",
        program_version="1.0.0",
        current_state="QUESTIONING",
        state_data=state_data,
        version=version,
        state_hash=state_hash,
        lifecycle=lifecycle,
        last_receipt_id=None,
        created_at="2026-09-08T11:00:00Z",
        updated_at="2026-09-08T11:00:00Z",
    )


def _seed_running_lease(
    db_path: Path,
    *,
    aggregate_id: str,
    workspace_id: str,
    lease_id: str,
    lease_expires_at: str,
    worker_id: str = "worker-1",
    lifecycle: ProgramStateLifecycle = ProgramStateLifecycle.RUNNING,
) -> None:
    store = SqliteProgramStateStore(db_path)
    aggregate = _make_aggregate(
        aggregate_id=aggregate_id,
        workspace_id=workspace_id,
        lifecycle=lifecycle,
    )
    store.save_aggregate(aggregate)
    store.register_execution_dispatch(
        # register_execution_dispatch requires INITIALIZED/version 0, so the
        # real lease is promoted through the canonical acquisition path first.
        _make_aggregate(
            aggregate_id=f"unused-{aggregate_id}",
            workspace_id=workspace_id,
            lifecycle=ProgramStateLifecycle.INITIALIZED,
            version=0,
        ),
        lease_id=f"unused-{lease_id}",
        enqueued_at="2026-09-08T10:59:00Z",
    )


def _seed_acquired_lease(
    db_path: Path,
    *,
    aggregate_id: str,
    workspace_id: str,
    lease_id: str,
    lease_expires_at: str,
    worker_id: str = "worker-1",
) -> None:
    store = SqliteProgramStateStore(db_path)
    initial_state = {
        "lease_status": "LEASE_ENQUEUED",
        "lease_version": 0,
        "work": {"step": "run"},
    }
    initial_hash = _compute_state_hash(
        aggregate_id=aggregate_id,
        program_id="interview_semantic_program",
        program_version="1.0.0",
        current_state="INITIAL",
        version=0,
        state_data=initial_state,
    )
    initial = ProgramStateAggregate(
        aggregate_id=aggregate_id,
        workspace_id=workspace_id,
        cae_run_id=f"run-{aggregate_id}",
        program_id="interview_semantic_program",
        program_version="1.0.0",
        current_state="INITIAL",
        state_data=initial_state,
        version=0,
        state_hash=initial_hash,
        lifecycle=ProgramStateLifecycle.INITIALIZED,
        last_receipt_id=None,
        created_at="2026-09-08T10:59:00Z",
        updated_at="2026-09-08T10:59:00Z",
    )
    store.register_execution_dispatch(
        initial,
        lease_id=lease_id,
        enqueued_at="2026-09-08T10:59:00Z",
    )
    store.acquire_execution_lease(
        aggregate_id=aggregate_id,
        actor_id=worker_id,
        expected_lease_version=0,
        refreshed_context_state_hash=initial.state_hash,
        lease_acquired_at="2026-09-08T11:00:00Z",
        workflow_payload={"step": "run"},
    )
    # Reconciler owns the minimum CA-M045 schema extension; the fixture then
    # seeds durable worker identity and expiry into that real lease row.
    ZombieLeaseReconciler(store).ensure_schema()
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            UPDATE cae_program_execution_leases
            SET lease_worker_id = ?, lease_expires_at = ?
            WHERE aggregate_id = ?
            """,
            (worker_id, lease_expires_at, aggregate_id),
        )
        conn.commit()


def _read_lease(db_path: Path, aggregate_id: str) -> dict[str, object]:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM cae_program_execution_leases WHERE aggregate_id = ?",
            (aggregate_id,),
        ).fetchone()
        assert row is not None
        return dict(row)


def test_expired_running_lease_is_reconciled_to_paused_with_durable_evidence(tmp_path: Path) -> None:
    db = tmp_path / "expired.db"
    _seed_acquired_lease(
        db,
        aggregate_id="agg-expired",
        workspace_id="ws-A",
        lease_id="lease-expired",
        lease_expires_at=EXPIRED,
        worker_id="worker-42",
    )

    result, evidence = reconcile_on_startup(db, now=AS_OF)

    assert result.scanned == 1
    assert result.expired == 1
    assert result.reconciled == 1
    assert len(evidence) == 1
    assert evidence[0].worker_id == "worker-42"

    store = SqliteProgramStateStore(db)
    aggregate = store.get_aggregate("agg-expired")
    assert aggregate is not None
    assert aggregate.lifecycle == ProgramStateLifecycle.PAUSED
    assert aggregate.version == 2
    assert aggregate.state_data["lease_status"] == "LEASE_RECLAIMED"
    assert aggregate.state_data["lease_reconciled_worker_id"] == "worker-42"
    assert aggregate.last_receipt_id == evidence[0].receipt_id

    lease = _read_lease(db, "agg-expired")
    assert lease["status"] == "RECLAIMED"
    assert lease["holder_id"] is None
    assert lease["lease_worker_id"] is None
    assert int(lease["lease_version"]) == 2

    transitions = store.list_transitions("agg-expired")
    assert len(transitions) == 1
    assert transitions[0].transition_name == "reconcile_expired_worker_lease"
    assert transitions[0].expected_version == 1
    assert transitions[0].committed_version == 2
    assert transitions[0].receipt_id == evidence[0].receipt_id
    assert transitions[0].payload["invariant"] == "INV-REC-001"
    assert transitions[0].payload["resume_policy"] == "GOVERNED_RESUME_ONLY"


def test_unexpired_lease_is_preserved(tmp_path: Path) -> None:
    db = tmp_path / "unexpired.db"
    _seed_acquired_lease(
        db,
        aggregate_id="agg-live",
        workspace_id="ws-A",
        lease_id="lease-live",
        lease_expires_at=FUTURE,
    )

    result, evidence = ZombieLeaseReconciler(
        SqliteProgramStateStore(db),
    ).reconcile_on_startup(now=AS_OF)

    assert result.scanned == 1
    assert result.expired == 0
    assert result.reconciled == 0
    assert evidence == ()

    store = SqliteProgramStateStore(db)
    aggregate = store.get_aggregate("agg-live")
    assert aggregate is not None
    assert aggregate.lifecycle == ProgramStateLifecycle.RUNNING
    assert aggregate.version == 1
    assert store.list_transitions("agg-live") == []
    lease = _read_lease(db, "agg-live")
    assert lease["status"] == "LEASE_ACQUIRED"
    assert lease["holder_id"] == "worker-1"
    assert lease["lease_worker_id"] == "worker-1"


def test_non_running_aggregate_is_not_reclaimed_even_when_expired(tmp_path: Path) -> None:
    db = tmp_path / "paused.db"
    _seed_acquired_lease(
        db,
        aggregate_id="agg-paused",
        workspace_id="ws-A",
        lease_id="lease-paused",
        lease_expires_at=EXPIRED,
    )
    with sqlite3.connect(db) as conn:
        # This is only a fixture setup for the negative case; reconciliation is
        # still exercised through the startup entry point.
        conn.execute(
            "UPDATE cae_program_state_aggregates SET lifecycle = 'PAUSED' WHERE aggregate_id = ?",
            ("agg-paused",),
        )
        conn.commit()

    result, _ = reconcile_on_startup(db, now=AS_OF)

    assert result.scanned == 0
    assert result.reconciled == 0
    assert _read_lease(db, "agg-paused")["status"] == "LEASE_ACQUIRED"


def test_startup_reconciliation_is_idempotent_and_does_not_duplicate_runs(tmp_path: Path) -> None:
    db = tmp_path / "idempotent.db"
    _seed_acquired_lease(
        db,
        aggregate_id="agg-idempotent",
        workspace_id="ws-A",
        lease_id="lease-idempotent",
        lease_expires_at=EXPIRED,
    )

    first, first_evidence = reconcile_on_startup(db, now=AS_OF)
    second, second_evidence = reconcile_on_startup(db, now=AS_OF)

    assert first.reconciled == 1
    assert len(first_evidence) == 1
    assert second.reconciled == 0
    assert second_evidence == ()

    store = SqliteProgramStateStore(db)
    aggregate = store.get_aggregate("agg-idempotent")
    assert aggregate is not None
    assert aggregate.lifecycle == ProgramStateLifecycle.PAUSED
    assert aggregate.version == 2
    assert len(store.list_transitions("agg-idempotent")) == 1

    with sqlite3.connect(db) as conn:
        dispatch = conn.execute(
            """
            SELECT status, COUNT(*)
            FROM cae_program_workflow_dispatch_queue
            WHERE aggregate_id = ?
            GROUP BY status
            """,
            ("agg-idempotent",),
        ).fetchone()
    assert dispatch == ("SUSPENDED", 1)


def test_workspace_fencing_prevents_cross_workspace_reconciliation(tmp_path: Path) -> None:
    db = tmp_path / "workspace.db"
    _seed_acquired_lease(
        db,
        aggregate_id="agg-foreign",
        workspace_id="ws-B",
        lease_id="lease-foreign",
        lease_expires_at=EXPIRED,
    )

    result, _ = ZombieLeaseReconciler(
        SqliteProgramStateStore(db),
        workspace_id="ws-A",
    ).reconcile_on_startup(now=AS_OF)

    assert result.scanned == 0
    aggregate = SqliteProgramStateStore(db).get_aggregate("agg-foreign")
    assert aggregate is not None
    assert aggregate.workspace_id == "ws-B"
    assert aggregate.lifecycle == ProgramStateLifecycle.RUNNING
    assert _read_lease(db, "agg-foreign")["status"] == "LEASE_ACQUIRED"


def test_reconciliation_preserves_state_and_recomputes_committed_hash(tmp_path: Path) -> None:
    db = tmp_path / "hash.db"
    _seed_acquired_lease(
        db,
        aggregate_id="agg-hash",
        workspace_id="ws-A",
        lease_id="lease-hash",
        lease_expires_at=EXPIRED,
    )

    _, evidence = reconcile_on_startup(db, now=AS_OF)

    store = SqliteProgramStateStore(db)
    aggregate = store.get_aggregate("agg-hash")
    assert aggregate is not None
    expected = _compute_state_hash(
        aggregate_id=aggregate.aggregate_id,
        program_id=aggregate.program_id,
        program_version=aggregate.program_version,
        current_state=aggregate.current_state,
        version=aggregate.version,
        state_data=aggregate.state_data,
    )
    assert aggregate.state_hash == expected
    assert evidence[0].version_before + 1 == aggregate.version
    assert aggregate.state_data["work"] == {"step": "run"}


def test_reconciliation_records_worker_and_expiry_as_immutable_evidence(tmp_path: Path) -> None:
    db = tmp_path / "evidence.db"
    _seed_acquired_lease(
        db,
        aggregate_id="agg-evidence",
        workspace_id="ws-A",
        lease_id="lease-evidence",
        lease_expires_at=EXPIRED,
        worker_id="worker-zombie",
    )

    _, evidence = reconcile_on_startup(db, now=AS_OF)
    assert len(evidence) == 1

    transition = SqliteProgramStateStore(db).list_transitions("agg-evidence")[0]
    assert transition.payload["lease_id"] == "lease-evidence"
    assert transition.payload["lease_worker_id"] == "worker-zombie"
    assert transition.payload["lease_expires_at"] == EXPIRED
    assert transition.payload["recovery_reason"] == "EXPIRED_WORKER_LEASE"
    assert transition.payload["source_lifecycle"] == "RUNNING"
    assert transition.payload["target_lifecycle"] == "PAUSED"
    assert len(transition.payload["receipt_sha256"]) == 64
    assert transition.payload["receipt_sha256"] == transition.payload["receipt_sha256"].lower()


def test_invalid_expiry_fails_closed_without_mutation(tmp_path: Path) -> None:
    db = tmp_path / "invalid-expiry.db"
    _seed_acquired_lease(
        db,
        aggregate_id="agg-invalid",
        workspace_id="ws-A",
        lease_id="lease-invalid",
        lease_expires_at=EXPIRED,
    )
    with sqlite3.connect(db) as conn:
        conn.execute(
            """
            UPDATE cae_program_execution_leases
            SET lease_expires_at = ?
            WHERE aggregate_id = ?
            """,
            ("not-a-timestamp", "agg-invalid"),
        )
        conn.commit()

    with pytest.raises(ZombieLeaseReconciliationError):
        reconcile_on_startup(db, now=AS_OF)

    store = SqliteProgramStateStore(db)
    aggregate = store.get_aggregate("agg-invalid")
    assert aggregate is not None
    assert aggregate.lifecycle == ProgramStateLifecycle.RUNNING
    assert aggregate.version == 1
    assert store.list_transitions("agg-invalid") == []
    assert _read_lease(db, "agg-invalid")["status"] == "LEASE_ACQUIRED"


def test_concurrent_reconciliation_has_one_winner(tmp_path: Path) -> None:
    # Two independent SQLite store instances mimic two startup paths racing.
    # SQLite's transaction boundary, not a process-local mutex, decides the winner.
    from concurrent.futures import ThreadPoolExecutor

    db = tmp_path / "concurrent.db"
    _seed_acquired_lease(
        db,
        aggregate_id="agg-concurrent",
        workspace_id="ws-A",
        lease_id="lease-concurrent",
        lease_expires_at=EXPIRED,
    )

    def invoke() -> int:
        result, _ = reconcile_on_startup(db, now=AS_OF)
        return result.reconciled

    with ThreadPoolExecutor(max_workers=2) as executor:
        winners = list(executor.map(lambda _: invoke(), range(2)))

    assert sorted(winners) == [0, 1]

    store = SqliteProgramStateStore(db)
    assert store.get_aggregate("agg-concurrent").version == 2
    assert len(store.list_transitions("agg-concurrent")) == 1
    assert _read_lease(db, "agg-concurrent")["status"] == "RECLAIMED"
