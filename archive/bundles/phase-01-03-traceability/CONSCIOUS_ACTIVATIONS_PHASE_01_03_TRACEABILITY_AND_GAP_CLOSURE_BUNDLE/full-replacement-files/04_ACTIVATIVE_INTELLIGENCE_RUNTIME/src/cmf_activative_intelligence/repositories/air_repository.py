from __future__ import annotations

import json
import sqlite3
from contextlib import closing, contextmanager
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any, Iterator, Mapping

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.database import IdempotencyConflict, ProductDatabaseError
from ca_runtime.paths import default_database_path

from .. import PRODUCT_ID, PRODUCT_VERSION
from ..domain import (
    object_epistemic_state,
    object_identity,
    object_lifecycle_state,
    object_semantic_version,
    validate_air_object,
)
from ..services.common import make_transition

AUTHORITY_STATE = "candidate_not_current"
PHASE1_VERSION = "0.1.0-dev.1"


class AirRepositoryError(ProductDatabaseError):
    pass


class ObjectVersionConflict(AirRepositoryError):
    pass


class ObjectNotFound(AirRepositoryError):
    pass


@dataclass(frozen=True, slots=True)
class StoredAirObject:
    object_id: str
    revision: int
    object_type: str
    semantic_version: str
    canonical_sha256: str
    payload: dict[str, Any]
    epistemic_state: str | None
    lifecycle_state: str | None
    authority_state: str
    current: bool
    created_at_utc: str
    command_id: str
    supersedes_object_id: str | None
    supersedes_revision: int | None

    def immutable_ref(self) -> dict[str, str]:
        return {
            "object_id": self.object_id,
            "version": self.semantic_version,
            "sha256": self.canonical_sha256,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "object_id": self.object_id,
            "revision": self.revision,
            "object_type": self.object_type,
            "semantic_version": self.semantic_version,
            "canonical_sha256": self.canonical_sha256,
            "payload": self.payload,
            "epistemic_state": self.epistemic_state,
            "lifecycle_state": self.lifecycle_state,
            "authority_state": self.authority_state,
            "current": self.current,
            "created_at_utc": self.created_at_utc,
            "command_id": self.command_id,
            "supersedes_object_id": self.supersedes_object_id,
            "supersedes_revision": self.supersedes_revision,
        }


class AirRepository:
    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path is not None else default_database_path(PRODUCT_ID)

    def _connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path, timeout=15.0, isolation_level=None)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = FULL")
        return connection

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

    def initialize(self, *, now: str | None = None) -> dict[str, Any]:
        timestamp = now or utc_now_rfc3339()
        foundation = resources.files("ca_runtime.migrations").joinpath(
            "0001_foundation.sql"
        ).read_text(encoding="utf-8")
        air_migration = resources.files(
            "cmf_activative_intelligence.migrations"
        ).joinpath("0002_air_core.sql").read_text(encoding="utf-8")

        with closing(self._connect()) as connection:
            connection.executescript(foundation)
            connection.execute(
                """
                INSERT INTO schema_migrations(version, name, applied_at_utc)
                VALUES(1, '0001_foundation', ?)
                ON CONFLICT(version) DO NOTHING
                """,
                (timestamp,),
            )
            metadata = connection.execute(
                "SELECT * FROM product_metadata WHERE product_id = ?",
                (PRODUCT_ID,),
            ).fetchone()
            if metadata is None:
                connection.execute(
                    """
                    INSERT INTO product_metadata(
                        product_id, product_version, authority_state,
                        development_authorized, production_authorized, certified,
                        initialized_at_utc
                    ) VALUES(?, ?, ?, 1, 0, 0, ?)
                    """,
                    (PRODUCT_ID, PRODUCT_VERSION, AUTHORITY_STATE, timestamp),
                )
            else:
                observed_version = str(metadata["product_version"])
                if observed_version not in {PHASE1_VERSION, PRODUCT_VERSION}:
                    raise AirRepositoryError(
                        f"unsupported AIR database product version: {observed_version}"
                    )
                if str(metadata["authority_state"]) != AUTHORITY_STATE:
                    raise AirRepositoryError("AIR database authority_state drift")
                if int(metadata["production_authorized"]) != 0 or int(metadata["certified"]) != 0:
                    raise AirRepositoryError(
                        "AIR Phase 2 cannot open a database claiming production or certification"
                    )
                if observed_version == PHASE1_VERSION:
                    connection.execute(
                        """
                        UPDATE product_metadata
                        SET product_version = ?, development_authorized = 1
                        WHERE product_id = ?
                        """,
                        (PRODUCT_VERSION, PRODUCT_ID),
                    )

            connection.executescript(air_migration)
            connection.execute(
                """
                INSERT INTO air_product_migrations(version, name, applied_at_utc)
                VALUES(2, '0002_air_core', ?)
                ON CONFLICT(version) DO NOTHING
                """,
                (timestamp,),
            )
            from ..domain import AIR_OWNED_LAYERS, ResponsibleLayer, expected_owner_for_layer

            for layer in ResponsibleLayer:
                connection.execute(
                    """
                    INSERT INTO air_failure_layers(
                        layer_id, owner_product, local_repair_authorized
                    ) VALUES(?, ?, ?)
                    ON CONFLICT(layer_id) DO UPDATE SET
                        owner_product = excluded.owner_product,
                        local_repair_authorized = excluded.local_repair_authorized
                    """,
                    (
                        layer.value,
                        expected_owner_for_layer(layer.value),
                        int(layer.value in AIR_OWNED_LAYERS),
                    ),
                )
        return self.health()


    def record_foundation_transition(
        self,
        *,
        command_envelope: Mapping[str, Any],
        command_payload: Mapping[str, Any],
        event_envelope: Mapping[str, Any],
        event_payload: Mapping[str, Any],
        receipt_envelope: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Preserve the Phase 1 product-shell bootstrap contract after the AIR core upgrade."""
        from ca_contracts import validate_payload

        validate_payload("command-envelope", command_envelope)
        validate_payload("event-envelope", event_envelope)
        validate_payload("receipt-envelope", receipt_envelope)
        self.initialize()
        command_payload_sha = canonical_sha256(command_payload)
        event_payload_sha = canonical_sha256(event_payload)
        if command_payload_sha != command_envelope["payload_sha256"]:
            raise AirRepositoryError("command payload hash does not match envelope")
        if event_payload_sha != event_envelope["payload_sha256"]:
            raise AirRepositoryError("event payload hash does not match envelope")
        command_json = canonical_json_text(command_envelope)
        command_payload_json = canonical_json_text(command_payload)
        event_json = canonical_json_text(event_envelope)
        event_payload_json = canonical_json_text(event_payload)
        receipt_json = canonical_json_text(receipt_envelope)
        with closing(self._connect()) as connection:
            existing = connection.execute(
                "SELECT command_id, envelope_json, payload_sha256 FROM commands WHERE idempotency_key = ?",
                (command_envelope["idempotency_key"],),
            ).fetchone()
            if existing is not None:
                if existing["payload_sha256"] != command_payload_sha or existing["envelope_json"] != command_json:
                    raise IdempotencyConflict("foundation idempotency key reused with different bytes")
                row = connection.execute(
                    "SELECT envelope_json FROM receipts WHERE command_id = ?",
                    (existing["command_id"],),
                ).fetchone()
                if row is None:
                    raise AirRepositoryError("foundation command exists without receipt")
                return json.loads(row["envelope_json"])
            expected_command_ref_sha = canonical_sha256(
                {"envelope": dict(command_envelope), "payload": dict(command_payload)}
            )
            if receipt_envelope["command_ref"]["sha256"] != expected_command_ref_sha:
                raise AirRepositoryError("receipt command_ref hash does not match command bytes")
            with self._transaction(connection):
                connection.execute(
                    """INSERT INTO commands(command_id, command_type, idempotency_key, envelope_json, payload_json, payload_sha256, submitted_at_utc) VALUES(?, ?, ?, ?, ?, ?, ?)""",
                    (command_envelope["command_id"], command_envelope["command_type"], command_envelope["idempotency_key"], command_json, command_payload_json, command_payload_sha, command_envelope["submitted_at_utc"]),
                )
                connection.execute(
                    """INSERT INTO events(event_id, aggregate_id, aggregate_version, event_type, envelope_json, payload_json, payload_sha256, causation_id, correlation_id, occurred_at_utc) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (event_envelope["event_id"], event_envelope["aggregate_id"], event_envelope["aggregate_version"], event_envelope["event_type"], event_json, event_payload_json, event_payload_sha, event_envelope["causation_id"], event_envelope["correlation_id"], event_envelope["occurred_at_utc"]),
                )
                connection.execute(
                    """INSERT INTO receipts(receipt_id, command_id, envelope_json, outcome, recorded_at_utc, receipt_sha256) VALUES(?, ?, ?, ?, ?, ?)""",
                    (receipt_envelope["receipt_id"], command_envelope["command_id"], receipt_json, receipt_envelope["outcome"], receipt_envelope["recorded_at_utc"], receipt_envelope["receipt_sha256"]),
                )
        return dict(receipt_envelope)

    def _row_to_object(self, row: sqlite3.Row) -> StoredAirObject:
        return StoredAirObject(
            object_id=str(row["object_id"]),
            revision=int(row["revision"]),
            object_type=str(row["object_type"]),
            semantic_version=str(row["semantic_version"]),
            canonical_sha256=str(row["canonical_sha256"]),
            payload=json.loads(row["payload_json"]),
            epistemic_state=row["epistemic_state"],
            lifecycle_state=row["lifecycle_state"],
            authority_state=str(row["authority_state"]),
            current=bool(row["is_current"]),
            created_at_utc=str(row["created_at_utc"]),
            command_id=str(row["command_id"]),
            supersedes_object_id=row["supersedes_object_id"],
            supersedes_revision=(
                int(row["supersedes_revision"])
                if row["supersedes_revision"] is not None
                else None
            ),
        )

    def store_object(
        self,
        object_type: str,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
        now: str | None = None,
    ) -> dict[str, Any]:
        normalized = validate_air_object(object_type, payload)
        if not isinstance(idempotency_key, str) or not idempotency_key.strip():
            raise AirRepositoryError("idempotency_key must be a non-empty string")
        if len(idempotency_key) != 64 or any(ch not in "0123456789abcdef" for ch in idempotency_key):
            idempotency_key = canonical_sha256(
                {
                    "scope": "ca.air.semantic-command-idempotency",
                    "key": idempotency_key,
                    "object_type": object_type,
                }
            )
        object_id = object_identity(object_type, normalized)
        semantic_version = object_semantic_version(normalized)
        object_sha = canonical_sha256(normalized)
        timestamp = now or utc_now_rfc3339()

        self.initialize(now=timestamp)
        with closing(self._connect()) as connection:
            existing_command = connection.execute(
                """
                SELECT command_id, payload_sha256
                FROM commands
                WHERE idempotency_key = ?
                """,
                (idempotency_key,),
            ).fetchone()
            if existing_command is not None:
                receipt_row = connection.execute(
                    """
                    SELECT envelope_json
                    FROM receipts
                    WHERE command_id = ?
                    """,
                    (existing_command["command_id"],),
                ).fetchone()
                if receipt_row is None:
                    raise AirRepositoryError(
                        "idempotent command exists without receipt"
                    )
                object_row = connection.execute(
                    """
                    SELECT *
                    FROM air_objects
                    WHERE object_id = ? AND canonical_sha256 = ?
                    ORDER BY revision DESC
                    LIMIT 1
                    """,
                    (object_id, object_sha),
                ).fetchone()
                if object_row is None:
                    raise IdempotencyConflict(
                        "idempotency key is already bound to different semantic bytes"
                    )
                return {
                    "object": self._row_to_object(object_row).to_dict(),
                    "receipt": json.loads(receipt_row["envelope_json"]),
                    "idempotent_replay": True,
                }

            current = connection.execute(
                """
                SELECT *
                FROM air_objects
                WHERE object_id = ? AND is_current = 1
                """,
                (object_id,),
            ).fetchone()
            current_revision = int(current["revision"]) if current else 0
            if expected_revision is not None and expected_revision != current_revision:
                raise ObjectVersionConflict(
                    f"expected revision {expected_revision}, current revision {current_revision}"
                )
            next_revision = current_revision + 1

            supersedes_ref = normalized.get("supersedes_ref")
            if current is None and supersedes_ref is not None:
                raise ObjectVersionConflict(
                    "supersedes_ref is invalid because no current object exists"
                )
            if current is not None:
                if not isinstance(supersedes_ref, Mapping):
                    raise ObjectVersionConflict(
                        "a revision of an existing object requires supersedes_ref"
                    )
                expected_ref = {
                    "object_id": str(current["object_id"]),
                    "version": str(current["semantic_version"]),
                    "sha256": str(current["canonical_sha256"]),
                }
                if dict(supersedes_ref) != expected_ref:
                    raise ObjectVersionConflict(
                        "supersedes_ref does not identify the current object bytes"
                    )

            command, command_payload, event, event_payload, receipt = make_transition(
                object_type=object_type,
                object_id=object_id,
                revision=next_revision,
                object_payload=normalized,
                idempotency_key=idempotency_key,
                now=timestamp,
            )
            command_json = canonical_json_text(command)
            command_payload_json = canonical_json_text(command_payload)
            event_json = canonical_json_text(event)
            event_payload_json = canonical_json_text(event_payload)
            receipt_json = canonical_json_text(receipt)

            try:
                with self._transaction(connection):
                    if current is not None:
                        connection.execute(
                            """
                            UPDATE air_objects
                            SET is_current = 0
                            WHERE object_id = ? AND revision = ?
                            """,
                            (object_id, current_revision),
                        )
                    connection.execute(
                        """
                        INSERT INTO commands(
                            command_id, command_type, idempotency_key,
                            envelope_json, payload_json, payload_sha256,
                            submitted_at_utc
                        ) VALUES(?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            command["command_id"],
                            command["command_type"],
                            command["idempotency_key"],
                            command_json,
                            command_payload_json,
                            command["payload_sha256"],
                            command["submitted_at_utc"],
                        ),
                    )
                    connection.execute(
                        """
                        INSERT INTO events(
                            event_id, aggregate_id, aggregate_version,
                            event_type, envelope_json, payload_json,
                            payload_sha256, causation_id, correlation_id,
                            occurred_at_utc
                        ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            event["event_id"],
                            event["aggregate_id"],
                            event["aggregate_version"],
                            event["event_type"],
                            event_json,
                            event_payload_json,
                            event["payload_sha256"],
                            event["causation_id"],
                            event["correlation_id"],
                            event["occurred_at_utc"],
                        ),
                    )
                    connection.execute(
                        """
                        INSERT INTO receipts(
                            receipt_id, command_id, envelope_json,
                            outcome, recorded_at_utc, receipt_sha256
                        ) VALUES(?, ?, ?, ?, ?, ?)
                        """,
                        (
                            receipt["receipt_id"],
                            command["command_id"],
                            receipt_json,
                            receipt["outcome"],
                            receipt["recorded_at_utc"],
                            receipt["receipt_sha256"],
                        ),
                    )
                    connection.execute(
                        """
                        INSERT INTO air_objects(
                            object_id, revision, object_type, semantic_version,
                            canonical_sha256, payload_json, epistemic_state,
                            lifecycle_state, authority_state, is_current,
                            created_at_utc, command_id, supersedes_object_id,
                            supersedes_revision
                        ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?)
                        """,
                        (
                            object_id,
                            next_revision,
                            object_type,
                            semantic_version,
                            object_sha,
                            canonical_json_text(normalized),
                            object_epistemic_state(normalized),
                            object_lifecycle_state(normalized),
                            AUTHORITY_STATE,
                            timestamp,
                            command["command_id"],
                            str(current["object_id"]) if current else None,
                            current_revision if current else None,
                        ),
                    )
                    if current is not None:
                        connection.execute(
                            """
                            INSERT INTO air_object_edges(
                                source_object_id, source_revision, relation_type,
                                target_object_id, target_revision, evidence_json,
                                created_at_utc
                            ) VALUES(?, ?, 'supersedes', ?, ?, ?, ?)
                            """,
                            (
                                object_id,
                                next_revision,
                                object_id,
                                current_revision,
                                canonical_json_text(
                                    {
                                        "current_sha256": object_sha,
                                        "superseded_sha256": str(
                                            current["canonical_sha256"]
                                        ),
                                    }
                                ),
                                timestamp,
                            ),
                        )
            except sqlite3.IntegrityError as exc:
                raise AirRepositoryError(
                    f"atomic AIR object transition rejected: {exc}"
                ) from exc

        return {
            "object": self.get_object(object_id).to_dict(),
            "receipt": receipt,
            "idempotent_replay": False,
        }

    def get_object(
        self, object_id: str, *, revision: int | None = None
    ) -> StoredAirObject:
        self.initialize()
        with closing(self._connect()) as connection:
            if revision is None:
                row = connection.execute(
                    """
                    SELECT *
                    FROM air_objects
                    WHERE object_id = ? AND is_current = 1
                    """,
                    (object_id,),
                ).fetchone()
            else:
                row = connection.execute(
                    """
                    SELECT *
                    FROM air_objects
                    WHERE object_id = ? AND revision = ?
                    """,
                    (object_id, revision),
                ).fetchone()
        if row is None:
            raise ObjectNotFound(object_id)
        return self._row_to_object(row)

    def history(self, object_id: str) -> tuple[StoredAirObject, ...]:
        self.initialize()
        with closing(self._connect()) as connection:
            rows = connection.execute(
                """
                SELECT *
                FROM air_objects
                WHERE object_id = ?
                ORDER BY revision ASC
                """,
                (object_id,),
            ).fetchall()
        return tuple(self._row_to_object(row) for row in rows)

    def list_current(
        self, *, object_type: str | None = None
    ) -> tuple[StoredAirObject, ...]:
        self.initialize()
        with closing(self._connect()) as connection:
            if object_type is None:
                rows = connection.execute(
                    """
                    SELECT *
                    FROM air_objects
                    WHERE is_current = 1
                    ORDER BY object_type, object_id
                    """
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT *
                    FROM air_objects
                    WHERE is_current = 1 AND object_type = ?
                    ORDER BY object_id
                    """,
                    (object_type,),
                ).fetchall()
        return tuple(self._row_to_object(row) for row in rows)

    def health(self) -> dict[str, Any]:
        if not self.path.exists():
            return {
                "product_id": PRODUCT_ID,
                "product_version": PRODUCT_VERSION,
                "authority_state": AUTHORITY_STATE,
                "database_path": str(self.path),
                "integrity": "not_initialized",
                "semantic_object_count": 0,
                "current_object_count": 0,
                "primitive_count": 0,
                "archetype_count": 0,
                "production_authorized": False,
                "certified": False,
            }
        with closing(self._connect()) as connection:
            integrity = ",".join(
                str(row[0])
                for row in connection.execute("PRAGMA integrity_check").fetchall()
            )
            metadata = connection.execute(
                "SELECT * FROM product_metadata WHERE product_id = ?",
                (PRODUCT_ID,),
            ).fetchone()
            counts = {}
            for table in (
                "commands",
                "events",
                "receipts",
                "air_objects",
                "air_primitives",
                "air_archetypes",
            ):
                try:
                    counts[table] = int(
                        connection.execute(
                            f"SELECT COUNT(*) FROM {table}"
                        ).fetchone()[0]
                    )
                except sqlite3.OperationalError:
                    counts[table] = 0
            current_count = 0
            try:
                current_count = int(
                    connection.execute(
                        "SELECT COUNT(*) FROM air_objects WHERE is_current = 1"
                    ).fetchone()[0]
                )
            except sqlite3.OperationalError:
                pass
        return {
            "product_id": PRODUCT_ID,
            "product_version": (
                str(metadata["product_version"]) if metadata else PRODUCT_VERSION
            ),
            "authority_state": (
                str(metadata["authority_state"]) if metadata else AUTHORITY_STATE
            ),
            "database_path": str(self.path),
            "integrity": integrity,
            "command_count": counts["commands"],
            "event_count": counts["events"],
            "receipt_count": counts["receipts"],
            "semantic_object_count": counts["air_objects"],
            "current_object_count": current_count,
            "primitive_count": counts["air_primitives"],
            "archetype_count": counts["air_archetypes"],
            "production_authorized": False,
            "certified": False,
        }
