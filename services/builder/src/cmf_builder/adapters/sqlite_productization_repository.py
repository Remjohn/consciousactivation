from __future__ import annotations

from contextlib import closing
from pathlib import Path
import sqlite3
from threading import Lock

from cmf_builder.adapters.sqlite_schema import apply_migrations, open_connection
from cmf_builder.adapters.sqlite_transactions import immediate_transaction
from cmf_builder.adapters.storage_integrity import (
    integrity_issues,
    is_sha256,
    payload_sha256,
)
from cmf_builder.application.productization_contracts import (
    DurableCommandReceipt,
    DurableRecord,
    ProductizationError,
    ProductizationErrorCode,
)


class SQLiteProductizationRepository:
    """SQLite durability adapter for the bounded PX-AM-001 productization path."""

    _FAILURE_BOUNDARIES = frozenset({"after_record", "after_receipt"})

    def __init__(
        self,
        database_path: str | Path,
        *,
        timeout_seconds: float = 5.0,
    ) -> None:
        self.database_path = Path(database_path)
        self._timeout_seconds = timeout_seconds
        self._failure_lock = Lock()
        self._fail_next_boundary: str | None = None

    def initialize(self) -> None:
        try:
            with closing(self._connect()) as connection:
                apply_migrations(connection)
        except ProductizationError:
            raise
        except sqlite3.Error as error:
            raise self._storage_error("Could not initialize durable storage.", error) from error

    def commit_record(
        self,
        record: DurableRecord,
        *,
        command_receipt: DurableCommandReceipt,
        expected_version: int | None,
    ) -> DurableCommandReceipt:
        self._validate_commit(record, command_receipt, expected_version)
        try:
            with closing(self._connect()) as connection:
                with immediate_transaction(connection):
                    duplicate = self._load_receipt_row(connection, command_receipt.command_id)
                    if duplicate is not None:
                        return self._validate_duplicate(
                            connection,
                            duplicate,
                            record,
                            command_receipt,
                        )

                    current = connection.execute(
                        """
                        SELECT version
                        FROM durable_records
                        WHERE record_kind = ? AND record_id = ?
                        ORDER BY version DESC
                        LIMIT 1
                        """,
                        (record.record_kind, record.record_id),
                    ).fetchone()
                    self._validate_expected_version(current, record, expected_version)

                    connection.execute(
                        """
                        INSERT INTO durable_records(
                            record_kind, record_id, version, payload, payload_hash
                        ) VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            record.record_kind,
                            record.record_id,
                            record.version,
                            record.payload,
                            record.payload_hash,
                        ),
                    )
                    self._raise_injected_failure("after_record")
                    connection.execute(
                        """
                        INSERT INTO durable_command_receipts(
                            command_id, payload_hash, result_kind, result_id,
                            result_version, result_hash
                        ) VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            command_receipt.command_id,
                            command_receipt.payload_hash,
                            command_receipt.result_kind,
                            command_receipt.result_id,
                            record.version,
                            command_receipt.result_hash,
                        ),
                    )
                    self._raise_injected_failure("after_receipt")
                return command_receipt
        except ProductizationError:
            raise
        except sqlite3.IntegrityError as error:
            raise ProductizationError(
                ProductizationErrorCode.CONFLICT,
                "Durable record or command identity conflicts with committed state.",
                context={
                    "record_kind": record.record_kind,
                    "record_id": record.record_id,
                    "command_id": command_receipt.command_id,
                },
            ) from error
        except sqlite3.Error as error:
            raise self._storage_error("Durable record commit failed.", error) from error

    def get_record(self, record_kind: str, record_id: str) -> DurableRecord | None:
        self._validate_identity(record_kind, "record_kind")
        self._validate_identity(record_id, "record_id")
        try:
            with closing(self._connect()) as connection:
                row = connection.execute(
                    """
                    SELECT record_kind, record_id, version, payload, payload_hash
                    FROM durable_records
                    WHERE record_kind = ? AND record_id = ?
                    ORDER BY version DESC
                    LIMIT 1
                    """,
                    (record_kind, record_id),
                ).fetchone()
                if row is None:
                    return None
                return self._record_from_row(row)
        except ProductizationError:
            raise
        except sqlite3.Error as error:
            raise self._storage_error("Could not load durable record.", error) from error

    def get_command_receipt(self, command_id: str) -> DurableCommandReceipt | None:
        self._validate_identity(command_id, "command_id")
        try:
            with closing(self._connect()) as connection:
                row = self._load_receipt_row(connection, command_id)
                if row is None:
                    return None
                self._validate_receipt_binding(connection, row)
                return self._receipt_from_row(row)
        except ProductizationError:
            raise
        except sqlite3.Error as error:
            raise self._storage_error("Could not load durable command receipt.", error) from error

    def verify_integrity(self) -> tuple[str, ...]:
        try:
            with closing(self._connect()) as connection:
                return integrity_issues(connection)
        except sqlite3.Error as error:
            raise self._storage_error("Durable storage integrity verification failed.", error) from error

    def inject_next_commit_failure(self, boundary: str) -> None:
        if boundary not in self._FAILURE_BOUNDARIES:
            raise ValueError(f"Unsupported durable commit failure boundary: {boundary}")
        with self._failure_lock:
            self._fail_next_boundary = boundary

    def _connect(self) -> sqlite3.Connection:
        return open_connection(self.database_path, timeout_seconds=self._timeout_seconds)

    def _raise_injected_failure(self, boundary: str) -> None:
        with self._failure_lock:
            if self._fail_next_boundary != boundary:
                return
            self._fail_next_boundary = None
        raise ProductizationError(
            ProductizationErrorCode.STORAGE_INTEGRITY,
            "Injected durable transaction failure.",
            context={"boundary": boundary},
        )

    @staticmethod
    def _validate_commit(
        record: DurableRecord,
        receipt: DurableCommandReceipt,
        expected_version: int | None,
    ) -> None:
        SQLiteProductizationRepository._validate_identity(record.record_kind, "record_kind")
        SQLiteProductizationRepository._validate_identity(record.record_id, "record_id")
        SQLiteProductizationRepository._validate_identity(receipt.command_id, "command_id")
        if (
            not isinstance(record.version, int)
            or isinstance(record.version, bool)
            or record.version < 1
        ):
            raise ProductizationError(
                ProductizationErrorCode.CONFLICT,
                "Durable record version must be a positive integer.",
                context={"version": record.version},
            )
        if expected_version is not None and (
            not isinstance(expected_version, int)
            or isinstance(expected_version, bool)
            or expected_version < 1
        ):
            raise ProductizationError(
                ProductizationErrorCode.CONFLICT,
                "Expected version must be a positive integer or null for creation.",
                context={"expected_version": expected_version},
            )
        if not isinstance(record.payload, bytes):
            raise ProductizationError(
                ProductizationErrorCode.STORAGE_INTEGRITY,
                "Durable record payload must be immutable bytes.",
            )
        for field, value in (
            ("record.payload_hash", record.payload_hash),
            ("receipt.payload_hash", receipt.payload_hash),
            ("receipt.result_hash", receipt.result_hash),
        ):
            if not is_sha256(value):
                raise ProductizationError(
                    ProductizationErrorCode.HASH_MISMATCH,
                    "A durable hash is not a canonical SHA-256 value.",
                    field_path=field,
                )
        calculated = payload_sha256(record.payload)
        if calculated != record.payload_hash:
            raise ProductizationError(
                ProductizationErrorCode.HASH_MISMATCH,
                "Durable record bytes do not match their declared hash.",
                context={"expected": record.payload_hash, "observed": calculated},
            )
        if (
            receipt.result_kind != record.record_kind
            or receipt.result_id != record.record_id
            or receipt.result_hash != record.payload_hash
        ):
            raise ProductizationError(
                ProductizationErrorCode.CONFLICT,
                "The command receipt is not bound to the exact durable record.",
                context={"command_id": receipt.command_id},
            )

    @staticmethod
    def _validate_identity(value: str, field: str) -> None:
        if not isinstance(value, str) or not value or "\x00" in value:
            raise ProductizationError(
                ProductizationErrorCode.STORAGE_INTEGRITY,
                "Durable identities must be non-empty text without NUL bytes.",
                field_path=field,
            )

    @staticmethod
    def _validate_expected_version(
        current: sqlite3.Row | None,
        record: DurableRecord,
        expected_version: int | None,
    ) -> None:
        if current is None:
            if expected_version is not None:
                raise ProductizationError(
                    ProductizationErrorCode.CONFLICT,
                    "A new durable record requires a null expected version.",
                    context={"expected_version": expected_version},
                )
            return
        current_version = int(current["version"])
        if expected_version != current_version or record.version != current_version + 1:
            raise ProductizationError(
                ProductizationErrorCode.CONFLICT,
                "Durable record expected-version check failed.",
                context={
                    "expected_version": expected_version,
                    "current_version": current_version,
                    "record_version": record.version,
                },
            )

    @staticmethod
    def _load_receipt_row(
        connection: sqlite3.Connection, command_id: str
    ) -> sqlite3.Row | None:
        return connection.execute(
            """
            SELECT command_id, payload_hash, result_kind, result_id,
                   result_version, result_hash
            FROM durable_command_receipts
            WHERE command_id = ?
            """,
            (command_id,),
        ).fetchone()

    def _validate_duplicate(
        self,
        connection: sqlite3.Connection,
        row: sqlite3.Row,
        record: DurableRecord,
        receipt: DurableCommandReceipt,
    ) -> DurableCommandReceipt:
        existing = self._receipt_from_row(row)
        if existing != receipt or int(row["result_version"]) != record.version:
            raise ProductizationError(
                ProductizationErrorCode.CONFLICT,
                "A command identity was reused with a different payload or result.",
                context={"command_id": receipt.command_id},
            )
        self._validate_receipt_binding(connection, row)
        stored = connection.execute(
            """
            SELECT record_kind, record_id, version, payload, payload_hash
            FROM durable_records
            WHERE record_kind = ? AND record_id = ? AND version = ?
            """,
            (record.record_kind, record.record_id, record.version),
        ).fetchone()
        if stored is None or self._record_from_row(stored) != record:
            raise ProductizationError(
                ProductizationErrorCode.CONFLICT,
                "A repeated command does not reproduce its immutable stored record.",
                context={"command_id": receipt.command_id},
            )
        return existing

    @staticmethod
    def _validate_receipt_binding(
        connection: sqlite3.Connection, row: sqlite3.Row
    ) -> None:
        record = connection.execute(
            """
            SELECT payload, payload_hash
            FROM durable_records
            WHERE record_kind = ? AND record_id = ? AND version = ?
            """,
            (row["result_kind"], row["result_id"], row["result_version"]),
        ).fetchone()
        if record is None:
            raise ProductizationError(
                ProductizationErrorCode.STORAGE_INTEGRITY,
                "A durable receipt references a missing result record.",
                context={"command_id": row["command_id"]},
            )
        observed = payload_sha256(bytes(record["payload"]))
        if observed != record["payload_hash"] or row["result_hash"] != record["payload_hash"]:
            raise ProductizationError(
                ProductizationErrorCode.HASH_MISMATCH,
                "A durable receipt or referenced record failed hash verification.",
                context={"command_id": row["command_id"]},
            )

    @staticmethod
    def _record_from_row(row: sqlite3.Row) -> DurableRecord:
        payload = bytes(row["payload"])
        observed = payload_sha256(payload)
        if observed != row["payload_hash"]:
            raise ProductizationError(
                ProductizationErrorCode.HASH_MISMATCH,
                "Stored durable record bytes failed hash verification.",
                context={
                    "record_kind": row["record_kind"],
                    "record_id": row["record_id"],
                    "version": row["version"],
                },
            )
        return DurableRecord(
            record_kind=str(row["record_kind"]),
            record_id=str(row["record_id"]),
            version=int(row["version"]),
            payload=payload,
            payload_hash=str(row["payload_hash"]),
        )

    @staticmethod
    def _receipt_from_row(row: sqlite3.Row) -> DurableCommandReceipt:
        return DurableCommandReceipt(
            command_id=str(row["command_id"]),
            payload_hash=str(row["payload_hash"]),
            result_kind=str(row["result_kind"]),
            result_id=str(row["result_id"]),
            result_hash=str(row["result_hash"]),
        )

    @staticmethod
    def _storage_error(message: str, error: sqlite3.Error) -> ProductizationError:
        return ProductizationError(
            ProductizationErrorCode.STORAGE_INTEGRITY,
            message,
            context={"sqlite_error": type(error).__name__},
        )
