from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import sqlite3

from cmf_builder.adapters.sqlite_transactions import immediate_transaction


SCHEMA_VERSION = 1

_MIGRATION_1 = (
    """
    CREATE TABLE IF NOT EXISTS durable_records (
        record_kind TEXT NOT NULL CHECK(length(record_kind) > 0),
        record_id TEXT NOT NULL CHECK(length(record_id) > 0),
        version INTEGER NOT NULL CHECK(version > 0),
        payload BLOB NOT NULL,
        payload_hash TEXT NOT NULL CHECK(length(payload_hash) = 71),
        PRIMARY KEY (record_kind, record_id, version)
    ) WITHOUT ROWID
    """,
    """
    CREATE TABLE IF NOT EXISTS durable_command_receipts (
        command_id TEXT PRIMARY KEY CHECK(length(command_id) > 0),
        payload_hash TEXT NOT NULL CHECK(length(payload_hash) = 71),
        result_kind TEXT NOT NULL,
        result_id TEXT NOT NULL,
        result_version INTEGER NOT NULL,
        result_hash TEXT NOT NULL CHECK(length(result_hash) = 71),
        FOREIGN KEY (result_kind, result_id, result_version)
            REFERENCES durable_records(record_kind, record_id, version)
            ON UPDATE RESTRICT ON DELETE RESTRICT
    ) WITHOUT ROWID
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_durable_records_latest
    ON durable_records(record_kind, record_id, version DESC)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_durable_receipts_result
    ON durable_command_receipts(result_kind, result_id, result_version)
    """,
)

MIGRATION_1_DIGEST = "sha256:" + sha256(
    "\n".join(statement.strip() for statement in _MIGRATION_1).encode("utf-8")
).hexdigest()


def open_connection(database_path: str | Path, *, timeout_seconds: float) -> sqlite3.Connection:
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(
        path,
        timeout=timeout_seconds,
        isolation_level=None,
    )
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA synchronous = FULL")
    connection.execute(f"PRAGMA busy_timeout = {max(1, int(timeout_seconds * 1000))}")
    return connection


def apply_migrations(connection: sqlite3.Connection) -> None:
    with immediate_transaction(connection):
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                migration_digest TEXT NOT NULL
            ) WITHOUT ROWID
            """
        )
        rows = connection.execute(
            "SELECT version, migration_digest FROM schema_migrations ORDER BY version"
        ).fetchall()
        for row in rows:
            if row["version"] != SCHEMA_VERSION or row["migration_digest"] != MIGRATION_1_DIGEST:
                raise sqlite3.DatabaseError(
                    "The durable storage schema migration history is unsupported or altered."
                )
        if not rows:
            for statement in _MIGRATION_1:
                connection.execute(statement)
            connection.execute(
                "INSERT INTO schema_migrations(version, migration_digest) VALUES (?, ?)",
                (SCHEMA_VERSION, MIGRATION_1_DIGEST),
            )

