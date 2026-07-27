from __future__ import annotations

from hashlib import sha256
import re
import sqlite3

from cmf_builder.adapters.sqlite_schema import MIGRATION_1_DIGEST, SCHEMA_VERSION


_SHA256_PATTERN = re.compile(r"sha256:[0-9a-f]{64}\Z")


def payload_sha256(payload: bytes) -> str:
    return f"sha256:{sha256(payload).hexdigest()}"


def is_sha256(value: str) -> bool:
    return bool(_SHA256_PATTERN.fullmatch(value))


def integrity_issues(connection: sqlite3.Connection) -> tuple[str, ...]:
    issues: list[str] = []

    quick_check = tuple(row[0] for row in connection.execute("PRAGMA quick_check"))
    if quick_check != ("ok",):
        issues.extend(f"SQLITE_QUICK_CHECK:{item}" for item in quick_check)

    for row in connection.execute("PRAGMA foreign_key_check"):
        issues.append(
            "FOREIGN_KEY_VIOLATION:"
            + ":".join(str(item) for item in tuple(row))
        )

    migration_rows = connection.execute(
        "SELECT version, migration_digest FROM schema_migrations ORDER BY version"
    ).fetchall()
    observed_migrations = tuple(
        (int(row["version"]), str(row["migration_digest"]))
        for row in migration_rows
    )
    expected_migrations = ((SCHEMA_VERSION, MIGRATION_1_DIGEST),)
    if observed_migrations != expected_migrations:
        issues.append("SCHEMA_MIGRATION_HISTORY_MISMATCH")

    for row in connection.execute(
        """
        SELECT record_kind, record_id, version, payload, payload_hash
        FROM durable_records
        ORDER BY record_kind, record_id, version
        """
    ):
        payload = bytes(row["payload"])
        observed_hash = str(row["payload_hash"])
        if payload_sha256(payload) != observed_hash:
            issues.append(
                f"RECORD_HASH_MISMATCH:{row['record_kind']}:{row['record_id']}:{row['version']}"
            )

    for row in connection.execute(
        """
        SELECT
            receipt.command_id,
            receipt.result_hash,
            record.payload_hash
        FROM durable_command_receipts AS receipt
        JOIN durable_records AS record
          ON record.record_kind = receipt.result_kind
         AND record.record_id = receipt.result_id
         AND record.version = receipt.result_version
        ORDER BY receipt.command_id
        """
    ):
        if row["result_hash"] != row["payload_hash"]:
            issues.append(f"RECEIPT_RESULT_HASH_MISMATCH:{row['command_id']}")

    return tuple(sorted(set(issues)))

