"""CA-M045 worker restart and zombie lease reconciliation.

The reconciler is intentionally narrow: lease expiry is the durable source of truth
for worker ownership.  An expired running lease is atomically reclaimed and its
aggregate is moved to ``PAUSED`` through the repository's SQLite CAS primitive.

The mandate explicitly forbids auto-resume.  Reconciliation therefore makes the
execution safe to resume through the normal governed path later; it never invents
completion/failure and never starts a duplicate worker run.

The module supports the existing ``SqliteProgramStateStore`` and a small, generic
store interface for test doubles.  The durable proof path uses SQLite and updates
the aggregate, lease, and transition ledger in one transaction.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import sqlite3
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from ca_contracts import canonical_sha256, utc_now_rfc3339
from ca_runtime.program_state_runtime import (
    ProgramStateAggregate,
    ProgramStateLifecycle,
    SqliteProgramStateStore,
    _compute_state_hash,
)
from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.sqlite_cas_transitions import (
    SqliteCasAggregateNotFoundError,
    SqliteCasVersionMismatchError,
    cas_update_program_state_aggregate,
)


class ZombieLeaseReconciliationError(RuntimeError):
    """Raised when reconciliation cannot establish a safe atomic recovery."""


@dataclass(frozen=True, slots=True)
class LeaseReconciliationResult:
    """Deterministic summary of one reconciliation pass."""

    scanned: int
    expired: int
    reconciled: int
    skipped: int
    workspace_id: Optional[str]
    as_of: str
    receipt_ids: tuple[str, ...] = ()
    reconciled_aggregate_ids: tuple[str, ...] = ()

    @property
    def resume_ready_aggregate_ids(self) -> tuple[str, ...]:
        """Aggregates safely reclaimed and left PAUSED for governed resumption."""
        return self.reconciled_aggregate_ids


@dataclass(frozen=True, slots=True)
class ReconciledLease:
    """Durable evidence returned for one accepted recovery."""

    aggregate_id: str
    workspace_id: str
    lease_id: str
    worker_id: Optional[str]
    lease_expires_at: str
    from_lifecycle: str
    to_lifecycle: str
    version_before: int
    version_after: int
    receipt_id: str
    transition_id: str
    reconciled_at: str


def _parse_utc(value: str) -> datetime:
    """Parse an RFC-3339 timestamp and normalize it to UTC."""
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError(f"Timestamp must include timezone information: {value!r}")
    return parsed.astimezone(timezone.utc)


def _normalize_now(now: Optional[datetime | str]) -> tuple[datetime, str]:
    if now is None:
        parsed = datetime.now(timezone.utc)
        return parsed, parsed.isoformat(timespec="seconds").replace("+00:00", "Z")
    if isinstance(now, datetime):
        if now.tzinfo is None:
            raise ValueError("Reconciliation time must be timezone-aware")
        parsed = now.astimezone(timezone.utc)
        return parsed, parsed.isoformat(timespec="seconds").replace("+00:00", "Z")
    parsed = _parse_utc(now)
    return parsed, parsed.isoformat(timespec="seconds").replace("+00:00", "Z")


def _receipt_id(*, aggregate_id: str, lease_id: str, lease_version: int) -> str:
    digest = hashlib.sha256(
        f"{aggregate_id}:{lease_id}:{lease_version}:CA-M045".encode("utf-8")
    ).hexdigest()[:24]
    return f"rcpt_lease_reconcile_{digest}"


def _transition_id(*, aggregate_id: str, lease_id: str, lease_version: int) -> str:
    digest = hashlib.sha256(
        f"{aggregate_id}:{lease_id}:{lease_version}:LEASE_RECONCILE".encode("utf-8")
    ).hexdigest()[:32]
    return f"trans_lease_reconcile_{digest}"


def _ensure_sqlite_lease_columns(conn: sqlite3.Connection) -> None:
    """Add the two Q44 lease fields without changing existing rows' semantics."""
    columns = {
        str(row["name"])
        for row in conn.execute("PRAGMA table_info(cae_program_execution_leases)")
    }
    if "lease_worker_id" not in columns:
        conn.execute(
            "ALTER TABLE cae_program_execution_leases ADD COLUMN lease_worker_id TEXT"
        )
        conn.execute(
            """
            UPDATE cae_program_execution_leases
            SET lease_worker_id = holder_id
            WHERE lease_worker_id IS NULL
            """
        )
    if "lease_expires_at" not in columns:
        conn.execute(
            "ALTER TABLE cae_program_execution_leases ADD COLUMN lease_expires_at TEXT"
        )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_execution_leases_expiry
        ON cae_program_execution_leases(status, lease_expires_at)
        """
    )


def _aggregate_from_row(row: sqlite3.Row) -> ProgramStateAggregate:
    return ProgramStateAggregate(
        aggregate_id=str(row["aggregate_id"]),
        workspace_id=str(row["workspace_id"]),
        cae_run_id=str(row["cae_run_id"]),
        program_id=str(row["program_id"]),
        program_version=str(row["program_version"]),
        current_state=str(row["current_state"]),
        state_data=dict(__import__("json").loads(row["state_data"])),
        version=int(row["version"]),
        state_hash=str(row["state_hash"]),
        lifecycle=ProgramStateLifecycle(str(row["lifecycle"])),
        last_receipt_id=row["last_receipt_id"],
        created_at=str(row["created_at"]),
        updated_at=str(row["updated_at"]),
    )


def _build_reconciliation_payload(
    *,
    lease: sqlite3.Row,
    aggregate: ProgramStateAggregate,
    now: str,
) -> Dict[str, Any]:
    lease_worker_id = lease["lease_worker_id"] or lease["holder_id"]
    return {
        "operation": "cae.worker.lease_reconcile@1.0.0",
        "mandate_id": "CA-M045",
        "invariant": "INV-REC-001",
        "recovery_reason": "EXPIRED_WORKER_LEASE",
        "source_lifecycle": aggregate.lifecycle.value,
        "target_lifecycle": ProgramStateLifecycle.PAUSED.value,
        "aggregate_id": aggregate.aggregate_id,
        "workspace_id": aggregate.workspace_id,
        "lease_id": lease["lease_id"],
        "lease_worker_id": lease_worker_id,
        "lease_version_before": int(lease["lease_version"]),
        "lease_expires_at": str(lease["lease_expires_at"]),
        "reconciled_at": now,
        "resume_policy": "GOVERNED_RESUME_ONLY",
    }


class ZombieLeaseReconciler:
    """Reconcile durable expired execution leases at worker/service startup.

    ``store`` is expected to be the canonical CAE state store.  The production
    implementation path is ``SqliteProgramStateStore`` so aggregate, lease and
    transition records can be committed atomically.
    """

    RECONCILIATION_ACTOR = "cae-zombie-reconciler"
    RECONCILIATION_OPERATION = "cae.worker.lease_reconcile@1.0.0"

    def __init__(
        self,
        store: SqliteProgramStateStore | None = None,
        *,
        db_path: str | Path | None = None,
        workspace_id: Optional[str] = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if store is not None and db_path is not None:
            raise ValueError("Provide either store or db_path, not both")
        if store is None:
            if db_path is None:
                raise ValueError("A SqliteProgramStateStore or db_path is required")
            store = SqliteProgramStateStore(db_path)
        if not isinstance(store, SqliteProgramStateStore):
            raise TypeError(
                "ZombieLeaseReconciler requires SqliteProgramStateStore so recovery "
                "can atomically commit lease, aggregate, and transition evidence."
            )
        self.store = store
        self.workspace_id = str(workspace_id) if workspace_id is not None else None
        self.clock = clock or (lambda: datetime.now(timezone.utc))

    def ensure_schema(self) -> None:
        """Ensure CA-M045 lease worker/expiry metadata exists."""
        with self.store._get_connection() as conn:
            _ensure_sqlite_lease_columns(conn)
            conn.commit()

    def reconcile_expired_leases(
        self,
        *,
        now: Optional[datetime | str] = None,
    ) -> tuple[LeaseReconciliationResult, tuple[ReconciledLease, ...]]:
        """Run one idempotent, workspace-fenced reconciliation pass.

        The eligible set is intentionally strict:

        * lease status is ``LEASE_ACQUIRED``;
        * lease has a holder/worker id;
        * durable lease expiry exists and is <= ``as_of``;
        * aggregate lifecycle is ``RUNNING``;
        * optional workspace filter matches the authoritative aggregate.

        Each eligible row is re-read and conditionally mutated in one
        ``BEGIN IMMEDIATE`` transaction.  A retry sees the already-``PAUSED``
        aggregate and cannot create another recovery transition.
        """
        current_time = self.clock() if now is None else now
        as_of_dt, as_of = _normalize_now(current_time)
        self.ensure_schema()

        reconciled: list[ReconciledLease] = []
        expired_count = 0

        with self.store._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            try:
                conn.execute("BEGIN IMMEDIATE")

                base_sql = """
                    SELECT
                        l.aggregate_id,
                        l.lease_id,
                        l.status,
                        l.lease_version,
                        l.holder_id,
                        l.lease_worker_id,
                        l.lease_expires_at,
                        a.workspace_id,
                        a.current_state,
                        a.lifecycle,
                        a.version,
                        a.state_hash,
                        a.state_data,
                        a.cae_run_id,
                        a.program_id,
                        a.program_version,
                        a.last_receipt_id,
                        a.created_at,
                        a.updated_at
                    FROM cae_program_execution_leases AS l
                    JOIN cae_program_state_aggregates AS a
                      ON a.aggregate_id = l.aggregate_id
                    WHERE l.status = 'LEASE_ACQUIRED'
                      AND COALESCE(l.lease_worker_id, l.holder_id) IS NOT NULL
                      AND l.lease_expires_at IS NOT NULL
                      AND a.lifecycle = 'RUNNING'
                """
                params: list[Any] = []
                if self.workspace_id is not None:
                    base_sql += " AND a.workspace_id = ?"
                    params.append(self.workspace_id)
                base_sql += " ORDER BY l.aggregate_id"

                rows = conn.execute(base_sql, tuple(params)).fetchall()
                scanned = len(rows)

                for row in rows:
                    lease_expires_at = str(row["lease_expires_at"])
                    try:
                        expired = _parse_utc(lease_expires_at) <= as_of_dt
                    except ValueError as exc:
                        raise ZombieLeaseReconciliationError(
                            f"Invalid lease expiry for aggregate {row['aggregate_id']}: "
                            f"{lease_expires_at!r}"
                        ) from exc

                    if not expired:
                        continue

                    expired_count += 1

                    # Re-read current state immediately before mutation. This is
                    # the critical stale-owner fence for a concurrent worker.
                    current = conn.execute(
                        """
                        SELECT * FROM cae_program_state_aggregates
                        WHERE aggregate_id = ?
                        """,
                        (row["aggregate_id"],),
                    ).fetchone()
                    current_lease = conn.execute(
                        """
                        SELECT * FROM cae_program_execution_leases
                        WHERE aggregate_id = ?
                        """,
                        (row["aggregate_id"],),
                    ).fetchone()
                    if current is None or current_lease is None:
                        continue

                    current_aggregate = _aggregate_from_row(current)
                    current_expiry = current_lease["lease_expires_at"]
                    current_worker = (
                        current_lease["lease_worker_id"]
                        or current_lease["holder_id"]
                    )
                    if (
                        current_aggregate.lifecycle != ProgramStateLifecycle.RUNNING
                        or current_lease["status"] != "LEASE_ACQUIRED"
                        or current_worker is None
                        or current_expiry is None
                        or _parse_utc(str(current_expiry)) > as_of_dt
                        or (
                            self.workspace_id is not None
                            and current_aggregate.workspace_id != self.workspace_id
                        )
                    ):
                        # Another authority won the race, or the aggregate is
                        # no longer eligible. Do not mutate anything.
                        continue

                    version_before = current_aggregate.version
                    version_after = version_before + 1
                    transition_id = _transition_id(
                        aggregate_id=current_aggregate.aggregate_id,
                        lease_id=str(current_lease["lease_id"]),
                        lease_version=int(current_lease["lease_version"]),
                    )
                    receipt_id = _receipt_id(
                        aggregate_id=current_aggregate.aggregate_id,
                        lease_id=str(current_lease["lease_id"]),
                        lease_version=int(current_lease["lease_version"]),
                    )
                    payload = _build_reconciliation_payload(
                        lease=current_lease,
                        aggregate=current_aggregate,
                        now=as_of,
                    )
                    payload["previous_state_hash"] = current_aggregate.state_hash

                    new_state_data = dict(current_aggregate.state_data)
                    new_state_data["lease_status"] = "LEASE_RECLAIMED"
                    new_state_data["lease_version"] = int(current_lease["lease_version"]) + 1
                    new_state_data["lease_reconciled_at"] = as_of
                    new_state_data["lease_reconciled_worker_id"] = current_worker
                    new_state_data["lease_reconciliation_receipt_id"] = receipt_id

                    new_state_hash = _compute_state_hash(
                        aggregate_id=current_aggregate.aggregate_id,
                        program_id=current_aggregate.program_id,
                        program_version=current_aggregate.program_version,
                        current_state=current_aggregate.current_state,
                        version=version_after,
                        state_data=new_state_data,
                    )

                    try:
                        cas_update_program_state_aggregate(
                            conn,
                            aggregate_id=current_aggregate.aggregate_id,
                            expected_version=version_before,
                            workspace_id=current_aggregate.workspace_id,
                            cae_run_id=current_aggregate.cae_run_id,
                            program_id=current_aggregate.program_id,
                            program_version=current_aggregate.program_version,
                            current_state=current_aggregate.current_state,
                            state_data=new_state_data,
                            state_hash=new_state_hash,
                            lifecycle=ProgramStateLifecycle.PAUSED.value,
                            last_receipt_id=receipt_id,
                            updated_at=as_of,
                        )
                    except SqliteCasVersionMismatchError:
                        continue
                    except SqliteCasAggregateNotFoundError:
                        continue

                    lease_update = conn.execute(
                        """
                        UPDATE cae_program_execution_leases
                        SET status = 'RECLAIMED',
                            lease_version = lease_version + 1,
                            holder_id = NULL,
                            lease_worker_id = NULL,
                            updated_at = ?
                        WHERE aggregate_id = ?
                          AND status = 'LEASE_ACQUIRED'
                          AND lease_version = ?
                          AND lease_expires_at = ?
                        """,
                        (
                            as_of,
                            current_aggregate.aggregate_id,
                            int(current_lease["lease_version"]),
                            str(current_expiry),
                        ),
                    )
                    if lease_update.rowcount != 1:
                        raise ZombieLeaseReconciliationError(
                            "Lease CAS failed after aggregate CAS; transaction will roll back"
                        )

                    receipt_sha = canonical_sha256(
                        {
                            "receipt_id": receipt_id,
                            "transition_id": transition_id,
                            "aggregate_id": current_aggregate.aggregate_id,
                            "workspace_id": current_aggregate.workspace_id,
                            "source_lifecycle": current_aggregate.lifecycle.value,
                            "target_lifecycle": ProgramStateLifecycle.PAUSED.value,
                            "version_before": version_before,
                            "version_after": version_after,
                            "lease_id": current_lease["lease_id"],
                            "lease_version_before": int(current_lease["lease_version"]),
                            "lease_expires_at": str(current_expiry),
                            "reconciled_at": as_of,
                        }
                    )
                    payload["receipt_sha256"] = receipt_sha
                    payload["actor_id"] = self.RECONCILIATION_ACTOR
                    payload["lane"] = AuthorityLane.COMMANDER.value

                    conn.execute(
                        """
                        INSERT INTO cae_program_state_transitions (
                            transition_id, aggregate_id, from_state, to_state,
                            transition_name, trigger_operation, lane, actor_id,
                            payload, expected_version, committed_version,
                            receipt_id, timestamp
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            transition_id,
                            current_aggregate.aggregate_id,
                            current_aggregate.current_state,
                            current_aggregate.current_state,
                            "reconcile_expired_worker_lease",
                            self.RECONCILIATION_OPERATION,
                            AuthorityLane.COMMANDER.value,
                            self.RECONCILIATION_ACTOR,
                            __import__("json").dumps(
                                payload,
                                sort_keys=True,
                                separators=(",", ":"),
                            ),
                            version_before,
                            version_after,
                            receipt_id,
                            as_of,
                        ),
                    )

                    # Mark an existing queued dispatch as suspended/retryable
                    # without creating a second execution. A later governed
                    # resume may enqueue or re-acquire it through normal controls.
                    conn.execute(
                        """
                        UPDATE cae_program_workflow_dispatch_queue
                        SET status = 'SUSPENDED'
                        WHERE aggregate_id = ?
                          AND lease_id = ?
                          AND status = 'ENQUEUED'
                        """,
                        (current_aggregate.aggregate_id, current_lease["lease_id"]),
                    )

                    reconciled.append(
                        ReconciledLease(
                            aggregate_id=current_aggregate.aggregate_id,
                            workspace_id=current_aggregate.workspace_id,
                            lease_id=str(current_lease["lease_id"]),
                            worker_id=str(current_worker) if current_worker is not None else None,
                            lease_expires_at=str(current_expiry),
                            from_lifecycle=current_aggregate.lifecycle.value,
                            to_lifecycle=ProgramStateLifecycle.PAUSED.value,
                            version_before=version_before,
                            version_after=version_after,
                            receipt_id=receipt_id,
                            transition_id=transition_id,
                            reconciled_at=as_of,
                        )
                    )

                conn.commit()
            except Exception:
                conn.rollback()
                raise

        return (
            LeaseReconciliationResult(
                scanned=scanned,
                expired=expired_count,
                reconciled=len(reconciled),
                skipped=scanned - len(reconciled),
                workspace_id=self.workspace_id,
                as_of=as_of,
                receipt_ids=tuple(item.receipt_id for item in reconciled),
                reconciled_aggregate_ids=tuple(item.aggregate_id for item in reconciled),
            ),
            tuple(reconciled),
        )

    def scan_expired_leases(
        self,
        *,
        now: Optional[datetime | str] = None,
    ) -> tuple[LeaseReconciliationResult, tuple[ReconciledLease, ...]]:
        """Compatibility alias for the startup reconciliation scan."""
        return self.reconcile_expired_leases(now=now)

    def reconcile(
        self,
        *,
        now: Optional[datetime | str] = None,
    ) -> tuple[LeaseReconciliationResult, tuple[ReconciledLease, ...]]:
        """Compatibility alias for one bounded reconciliation pass."""
        return self.reconcile_expired_leases(now=now)

    def reconcile_on_startup(
        self,
        *,
        now: Optional[datetime | str] = None,
    ) -> tuple[LeaseReconciliationResult, tuple[ReconciledLease, ...]]:
        """Startup entry point used by the API/application lifecycle."""
        return self.reconcile_expired_leases(now=now)


def reconcile_on_startup(
    db_path: str | Path | None = None,
    *,
    store: SqliteProgramStateStore | None = None,
    workspace_id: Optional[str] = None,
    now: Optional[datetime | str] = None,
) -> tuple[LeaseReconciliationResult, tuple[ReconciledLease, ...]]:
    """Convenience startup entry point for an application lifespan hook."""
    reconciler = ZombieLeaseReconciler(
        store=store,
        db_path=db_path,
        workspace_id=workspace_id,
    )
    return reconciler.reconcile_on_startup(now=now)
