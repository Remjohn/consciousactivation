"""SQLite compare-and-swap primitives for CAE program-state aggregates.

CA-M042 / INV-CAS-001

The authoritative success predicate for a state mutation is the database
operation itself: the aggregate is updated only when its persisted version
matches the executor's expected version, and the version is incremented by
SQLite in the same UPDATE statement. Callers are responsible for enclosing
this primitive in the repository transaction boundary (BEGIN IMMEDIATE).
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import sqlite3
from typing import Any


class SqliteCasError(RuntimeError):
    """Base error for SQLite CAS transition failures."""


class SqliteCasVersionMismatchError(SqliteCasError):
    """Raised when a CAS predicate matches zero rows because the version is stale."""

    def __init__(self, aggregate_id: str, expected_version: int, actual_version: int):
        self.aggregate_id = aggregate_id
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(
            f"SQLite CAS conflict on aggregate '{aggregate_id}': "
            f"expected version {expected_version}, but current version is {actual_version}"
        )


class SqliteCasAggregateNotFoundError(SqliteCasError):
    """Raised when a CAS targets an aggregate that does not exist."""

    def __init__(self, aggregate_id: str):
        self.aggregate_id = aggregate_id
        super().__init__(f"SQLite CAS aggregate '{aggregate_id}' not found")


@dataclass(frozen=True, slots=True)
class SqliteCasUpdateResult:
    """Evidence returned by a successful database-level compare-and-swap."""

    aggregate_id: str
    expected_version: int
    committed_version: int
    affected_rows: int


def cas_update_program_state_aggregate(
    connection: sqlite3.Connection,
    *,
    aggregate_id: str,
    expected_version: int,
    workspace_id: str,
    cae_run_id: str,
    program_id: str,
    program_version: str,
    current_state: str,
    state_data: dict[str, Any],
    state_hash: str,
    lifecycle: str,
    last_receipt_id: str | None,
    updated_at: str,
) -> SqliteCasUpdateResult:
    """Atomically update one aggregate when its persisted version matches.

    The connection must already be inside the repository's write transaction.
    The database operation itself is the concurrency predicate; no read-before-
    write version check is used to decide success.
    """

    committed_version = expected_version + 1
    cursor = connection.execute(
        """
        UPDATE cae_program_state_aggregates
        SET workspace_id = ?,
            cae_run_id = ?,
            program_id = ?,
            program_version = ?,
            current_state = ?,
            state_data = ?,
            version = version + 1,
            state_hash = ?,
            lifecycle = ?,
            last_receipt_id = ?,
            updated_at = ?
        WHERE aggregate_id = ?
          AND version = ?
        """,
        (
            workspace_id,
            cae_run_id,
            program_id,
            program_version,
            current_state,
            json.dumps(state_data),
            state_hash,
            lifecycle,
            last_receipt_id,
            updated_at,
            aggregate_id,
            expected_version,
        ),
    )

    if cursor.rowcount == 1:
        return SqliteCasUpdateResult(
            aggregate_id=aggregate_id,
            expected_version=expected_version,
            committed_version=committed_version,
            affected_rows=cursor.rowcount,
        )

    row = connection.execute(
        "SELECT version FROM cae_program_state_aggregates WHERE aggregate_id = ?",
        (aggregate_id,),
    ).fetchone()
    if row is None:
        raise SqliteCasAggregateNotFoundError(aggregate_id)

    raise SqliteCasVersionMismatchError(
        aggregate_id=aggregate_id,
        expected_version=expected_version,
        actual_version=int(row[0]),
    )
