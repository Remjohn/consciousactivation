from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any, Iterator

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339, validate_payload


class ProductDatabaseError(RuntimeError):
    pass


class IdempotencyConflict(ProductDatabaseError):
    pass


@dataclass(frozen=True, slots=True)
class ProductHealth:
    product_id: str
    product_version: str
    authority_state: str
    database_path: str
    integrity: str
    command_count: int
    event_count: int
    receipt_count: int

    def to_dict(self) -> dict[str, object]:
        return {
            "product_id": self.product_id,
            "product_version": self.product_version,
            "authority_state": self.authority_state,
            "database_path": self.database_path,
            "integrity": self.integrity,
            "command_count": self.command_count,
            "event_count": self.event_count,
            "receipt_count": self.receipt_count,
        }


class ProductDatabase:
    def __init__(
        self,
        path: str | Path,
        *,
        product_id: str,
        product_version: str,
        authority_state: str,
        development_authorized: bool,
        production_authorized: bool = False,
        certified: bool = False,
        timeout_seconds: float = 10.0,
    ):
        self.path = Path(path)
        self.product_id = product_id
        self.product_version = product_version
        self.authority_state = authority_state
        self.development_authorized = development_authorized
        self.production_authorized = production_authorized
        self.certified = certified
        self.timeout_seconds = timeout_seconds

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(
            self.path,
            timeout=self.timeout_seconds,
            isolation_level=None,
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = FULL")
        try:
            yield connection
        finally:
            connection.close()

    @contextmanager
    def _transaction(self, connection: sqlite3.Connection) -> Iterator[None]:
        connection.execute("BEGIN IMMEDIATE")
        try:
            yield
        except Exception:
            connection.execute("ROLLBACK")
            raise
        else:
            connection.execute("COMMIT")

    def initialize(self, *, initialized_at_utc: str | None = None) -> ProductHealth:
        timestamp = initialized_at_utc or utc_now_rfc3339()
        migration = resources.files("ca_runtime.migrations").joinpath("0001_foundation.sql").read_text(encoding="utf-8")
        with self._connect() as connection:
            connection.executescript(migration)
            connection.execute(
                """
                INSERT INTO schema_migrations(version, name, applied_at_utc)
                VALUES(1, '0001_foundation', ?)
                ON CONFLICT(version) DO NOTHING
                """,
                (timestamp,),
            )
            current = connection.execute(
                "SELECT * FROM product_metadata WHERE product_id = ?",
                (self.product_id,),
            ).fetchone()
            expected = (
                self.product_version,
                self.authority_state,
                int(self.development_authorized),
                int(self.production_authorized),
                int(self.certified),
            )
            if current is None:
                connection.execute(
                    """
                    INSERT INTO product_metadata(
                        product_id, product_version, authority_state,
                        development_authorized, production_authorized, certified,
                        initialized_at_utc
                    ) VALUES(?, ?, ?, ?, ?, ?, ?)
                    """,
                    (self.product_id, *expected, timestamp),
                )
            else:
                observed = (
                    current["product_version"],
                    current["authority_state"],
                    current["development_authorized"],
                    current["production_authorized"],
                    current["certified"],
                )
                if observed != expected:
                    raise ProductDatabaseError(
                        f"database metadata mismatch for {self.product_id}: expected {expected}, observed {observed}"
                    )
        return self.health()

    def record_transition(
        self,
        *,
        command_envelope: dict[str, Any],
        command_payload: dict[str, Any],
        event_envelope: dict[str, Any],
        event_payload: dict[str, Any],
        receipt_envelope: dict[str, Any],
    ) -> dict[str, Any]:
        validate_payload("command-envelope", command_envelope)
        validate_payload("event-envelope", event_envelope)
        validate_payload("receipt-envelope", receipt_envelope)

        command_payload_sha = canonical_sha256(command_payload)
        event_payload_sha = canonical_sha256(event_payload)
        if command_payload_sha != command_envelope["payload_sha256"]:
            raise ProductDatabaseError("command payload hash does not match envelope")
        if event_payload_sha != event_envelope["payload_sha256"]:
            raise ProductDatabaseError("event payload hash does not match envelope")

        command_json = canonical_json_text(command_envelope)
        command_payload_json = canonical_json_text(command_payload)
        event_json = canonical_json_text(event_envelope)
        event_payload_json = canonical_json_text(event_payload)
        receipt_json = canonical_json_text(receipt_envelope)

        with self._connect() as connection:
            existing = connection.execute(
                "SELECT command_id, envelope_json, payload_sha256 FROM commands WHERE idempotency_key = ?",
                (command_envelope["idempotency_key"],),
            ).fetchone()
            if existing is not None:
                if existing["payload_sha256"] != command_payload_sha or existing["envelope_json"] != command_json:
                    raise IdempotencyConflict(
                        f"idempotency key reused with different bytes: {command_envelope['idempotency_key']}"
                    )
                receipt = connection.execute(
                    "SELECT envelope_json FROM receipts WHERE command_id = ?",
                    (existing["command_id"],),
                ).fetchone()
                if receipt is None:
                    raise ProductDatabaseError("idempotent command exists without receipt")
                return json.loads(receipt["envelope_json"])

            if event_envelope["causation_id"] != command_envelope["command_id"]:
                raise ProductDatabaseError("event causation_id must equal command_id")
            if event_envelope["correlation_id"] != command_envelope["correlation_id"]:
                raise ProductDatabaseError("event correlation_id must equal command correlation_id")
            expected_command_ref_sha = canonical_sha256({"envelope": command_envelope, "payload": command_payload})
            if receipt_envelope["command_ref"]["object_id"] != command_envelope["command_id"]:
                raise ProductDatabaseError("receipt command_ref does not identify the command")
            if receipt_envelope["command_ref"]["sha256"] != expected_command_ref_sha:
                raise ProductDatabaseError("receipt command_ref hash does not match command bytes")
            receipt_without_hash = dict(receipt_envelope)
            receipt_without_hash.pop("receipt_sha256", None)
            if canonical_sha256(receipt_without_hash) != receipt_envelope["receipt_sha256"]:
                raise ProductDatabaseError("receipt hash does not match receipt bytes")

            try:
                with self._transaction(connection):
                    connection.execute(
                        """
                        INSERT INTO commands(
                            command_id, command_type, idempotency_key, envelope_json,
                            payload_json, payload_sha256, submitted_at_utc
                        ) VALUES(?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            command_envelope["command_id"],
                            command_envelope["command_type"],
                            command_envelope["idempotency_key"],
                            command_json,
                            command_payload_json,
                            command_payload_sha,
                            command_envelope["submitted_at_utc"],
                        ),
                    )
                    connection.execute(
                        """
                        INSERT INTO events(
                            event_id, aggregate_id, aggregate_version, event_type,
                            envelope_json, payload_json, payload_sha256, causation_id,
                            correlation_id, occurred_at_utc
                        ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            event_envelope["event_id"],
                            event_envelope["aggregate_id"],
                            event_envelope["aggregate_version"],
                            event_envelope["event_type"],
                            event_json,
                            event_payload_json,
                            event_payload_sha,
                            event_envelope["causation_id"],
                            event_envelope["correlation_id"],
                            event_envelope["occurred_at_utc"],
                        ),
                    )
                    connection.execute(
                        """
                        INSERT INTO receipts(
                            receipt_id, command_id, envelope_json, outcome,
                            recorded_at_utc, receipt_sha256
                        ) VALUES(?, ?, ?, ?, ?, ?)
                        """,
                        (
                            receipt_envelope["receipt_id"],
                            command_envelope["command_id"],
                            receipt_json,
                            receipt_envelope["outcome"],
                            receipt_envelope["recorded_at_utc"],
                            receipt_envelope["receipt_sha256"],
                        ),
                    )
            except sqlite3.IntegrityError as error:
                raise ProductDatabaseError(f"atomic transition rejected: {error}") from error
        return receipt_envelope

    def list_events(self, aggregate_id: str) -> tuple[dict[str, Any], ...]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT envelope_json, payload_json
                FROM events
                WHERE aggregate_id = ?
                ORDER BY aggregate_version ASC
                """,
                (aggregate_id,),
            ).fetchall()
        return tuple(
            {
                "envelope": json.loads(row["envelope_json"]),
                "payload": json.loads(row["payload_json"]),
            }
            for row in rows
        )

    def health(self) -> ProductHealth:
        if not self.path.exists():
            return ProductHealth(
                product_id=self.product_id,
                product_version=self.product_version,
                authority_state=self.authority_state,
                database_path=str(self.path),
                integrity="not_initialized",
                command_count=0,
                event_count=0,
                receipt_count=0,
            )
        with self._connect() as connection:
            integrity_rows = connection.execute("PRAGMA integrity_check").fetchall()
            integrity = ",".join(str(row[0]) for row in integrity_rows)
            metadata = connection.execute(
                "SELECT * FROM product_metadata WHERE product_id = ?",
                (self.product_id,),
            ).fetchone()
            if metadata is None:
                raise ProductDatabaseError("database is initialized without product metadata")
            counts = {
                table: int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
                for table in ("commands", "events", "receipts")
            }
        return ProductHealth(
            product_id=metadata["product_id"],
            product_version=metadata["product_version"],
            authority_state=metadata["authority_state"],
            database_path=str(self.path),
            integrity=integrity,
            command_count=counts["commands"],
            event_count=counts["events"],
            receipt_count=counts["receipts"],
        )
