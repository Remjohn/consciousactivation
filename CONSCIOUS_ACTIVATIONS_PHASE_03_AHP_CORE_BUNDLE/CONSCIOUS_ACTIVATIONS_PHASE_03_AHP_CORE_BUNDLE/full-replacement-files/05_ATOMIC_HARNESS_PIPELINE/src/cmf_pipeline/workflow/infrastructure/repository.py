from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from importlib import resources
from pathlib import Path
from typing import Any, Iterator, Mapping

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.paths import default_database_path

from ... import PRODUCT_ID, PRODUCT_VERSION
from ...domain.errors import PipelineConflict, PipelineNotFound
from ...domain.validation import reject_noncanonical, require_string


class PipelineRepository:
    """SQLite event/object store for the development Pipeline kernel."""

    def __init__(self, database_path: str | Path | None = None):
        self.path = Path(database_path) if database_path else default_database_path(PRODUCT_ID)

    def _connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path, timeout=10.0, isolation_level=None)
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
        foundation = resources.files("ca_runtime.migrations").joinpath("0001_foundation.sql").read_text(encoding="utf-8")
        pipeline = resources.files("cmf_pipeline.migrations").joinpath("0001_pipeline_core.sql").read_text(encoding="utf-8")
        with self._connect() as connection:
            connection.executescript(foundation)
            connection.execute(
                """
                INSERT INTO schema_migrations(version, name, applied_at_utc)
                VALUES(1, '0001_foundation', ?)
                ON CONFLICT(version) DO NOTHING
                """,
                (timestamp,),
            )
            row = connection.execute(
                "SELECT * FROM product_metadata WHERE product_id = ?", (PRODUCT_ID,)
            ).fetchone()
            if row is None:
                connection.execute(
                    """
                    INSERT INTO product_metadata(
                        product_id, product_version, authority_state,
                        development_authorized, production_authorized, certified,
                        initialized_at_utc
                    ) VALUES(?, ?, 'candidate_not_current', 1, 0, 0, ?)
                    """,
                    (PRODUCT_ID, PRODUCT_VERSION, timestamp),
                )
            else:
                if bool(row["production_authorized"]) or bool(row["certified"]):
                    raise PipelineConflict("Phase 3 cannot attach to a production-authorized or certified database")
                connection.execute(
                    """
                    UPDATE product_metadata
                    SET product_version = ?, authority_state = 'candidate_not_current',
                        development_authorized = 1, production_authorized = 0, certified = 0
                    WHERE product_id = ?
                    """,
                    (PRODUCT_VERSION, PRODUCT_ID),
                )
            connection.executescript(pipeline)
            connection.execute(
                """
                INSERT INTO pipeline_migrations(version, name, applied_at_utc)
                VALUES(1, '0001_pipeline_core', ?)
                ON CONFLICT(version) DO NOTHING
                """,
                (timestamp,),
            )
        return self.health()

    def execute_idempotent(
        self,
        *,
        command_type: str,
        idempotency_key: str,
        payload: Mapping[str, Any],
        callback,
        now: str | None = None,
    ) -> dict[str, Any]:
        command_type = require_string(command_type, "command_type")
        key = require_string(idempotency_key, "idempotency_key")
        reject_noncanonical(payload)
        payload_sha = canonical_sha256(payload)
        timestamp = now or utc_now_rfc3339()
        self.initialize(now=timestamp)
        with self._connect() as connection:
            existing = connection.execute(
                "SELECT payload_sha256, result_json FROM pipeline_command_results WHERE idempotency_key = ?",
                (key,),
            ).fetchone()
            if existing:
                if existing["payload_sha256"] != payload_sha:
                    raise PipelineConflict("idempotency key reused with different payload bytes")
                result = json.loads(existing["result_json"])
                result["idempotent_replay"] = True
                return result
            with self._transaction(connection):
                result = callback(connection, timestamp)
                reject_noncanonical(result)
                connection.execute(
                    """
                    INSERT INTO pipeline_command_results(
                        idempotency_key, command_type, payload_sha256, result_json, created_at_utc
                    ) VALUES(?, ?, ?, ?, ?)
                    """,
                    (key, command_type, payload_sha, canonical_json_text(result), timestamp),
                )
            return dict(result)

    def store_object(
        self,
        object_type: str,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        object_id: str,
        semantic_version: str = "1.0.0",
        lifecycle_state: str = "ACTIVE",
        authority_state: str = "candidate_not_current",
        expected_revision: int | None = None,
        now: str | None = None,
    ) -> dict[str, Any]:
        object_type = require_string(object_type, "object_type")
        object_id = require_string(object_id, "object_id")
        normalized = dict(payload)
        reject_noncanonical(normalized)
        object_sha = canonical_sha256(normalized)

        def write(connection: sqlite3.Connection, timestamp: str) -> dict[str, Any]:
            current = connection.execute(
                "SELECT * FROM pipeline_objects WHERE object_id = ? AND is_current = 1",
                (object_id,),
            ).fetchone()
            current_revision = int(current["revision"]) if current else 0
            if expected_revision is not None and expected_revision != current_revision:
                raise PipelineConflict(
                    f"expected revision {expected_revision}, current revision {current_revision}"
                )
            if current and current["canonical_sha256"] == object_sha:
                return {
                    "object": self._object_from_row(current),
                    "created": False,
                    "idempotent_replay": False,
                }
            revision = current_revision + 1
            if current:
                connection.execute(
                    "UPDATE pipeline_objects SET is_current = 0 WHERE object_id = ? AND revision = ?",
                    (object_id, current_revision),
                )
            connection.execute(
                """
                INSERT INTO pipeline_objects(
                    object_id, revision, object_type, semantic_version,
                    canonical_sha256, payload_json, lifecycle_state, authority_state,
                    is_current, idempotency_key, created_at_utc, supersedes_revision
                ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?)
                """,
                (
                    object_id,
                    revision,
                    object_type,
                    semantic_version,
                    object_sha,
                    canonical_json_text(normalized),
                    lifecycle_state,
                    authority_state,
                    idempotency_key,
                    timestamp,
                    current_revision or None,
                ),
            )
            row = connection.execute(
                "SELECT * FROM pipeline_objects WHERE object_id = ? AND revision = ?",
                (object_id, revision),
            ).fetchone()
            return {"object": self._object_from_row(row), "created": True, "idempotent_replay": False}

        return self.execute_idempotent(
            command_type=f"store:{object_type}",
            idempotency_key=idempotency_key,
            payload={"object_type": object_type, "object_id": object_id, "payload": normalized},
            callback=write,
            now=now,
        )

    @staticmethod
    def _object_from_row(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "object_id": str(row["object_id"]),
            "revision": int(row["revision"]),
            "object_type": str(row["object_type"]),
            "semantic_version": str(row["semantic_version"]),
            "canonical_sha256": str(row["canonical_sha256"]),
            "payload": json.loads(row["payload_json"]),
            "lifecycle_state": str(row["lifecycle_state"]),
            "authority_state": str(row["authority_state"]),
            "current": bool(row["is_current"]),
            "created_at_utc": str(row["created_at_utc"]),
            "supersedes_revision": row["supersedes_revision"],
        }

    def get_object(self, object_id: str, *, revision: int | None = None) -> dict[str, Any]:
        self.initialize()
        with self._connect() as connection:
            if revision is None:
                row = connection.execute(
                    "SELECT * FROM pipeline_objects WHERE object_id = ? AND is_current = 1",
                    (object_id,),
                ).fetchone()
            else:
                row = connection.execute(
                    "SELECT * FROM pipeline_objects WHERE object_id = ? AND revision = ?",
                    (object_id, revision),
                ).fetchone()
            if row is None:
                raise PipelineNotFound(f"object not found: {object_id}")
            return self._object_from_row(row)

    def list_objects(self, *, object_type: str | None = None) -> list[dict[str, Any]]:
        self.initialize()
        with self._connect() as connection:
            if object_type:
                rows = connection.execute(
                    "SELECT * FROM pipeline_objects WHERE object_type = ? AND is_current = 1 ORDER BY object_id",
                    (object_type,),
                ).fetchall()
            else:
                rows = connection.execute(
                    "SELECT * FROM pipeline_objects WHERE is_current = 1 ORDER BY object_type, object_id"
                ).fetchall()
            return [self._object_from_row(row) for row in rows]

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relation_type: str,
        *,
        evidence: Mapping[str, Any] | None = None,
        now: str | None = None,
    ) -> dict[str, Any]:
        source_id = require_string(source_id, "source_id")
        target_id = require_string(target_id, "target_id")
        relation_type = require_string(relation_type, "relation_type")
        evidence_payload = dict(evidence or {})
        reject_noncanonical(evidence_payload)
        payload = {
            "source_id": source_id,
            "target_id": target_id,
            "relation_type": relation_type,
            "evidence": evidence_payload,
        }
        edge_sha = canonical_sha256(payload)
        timestamp = now or utc_now_rfc3339()
        self.initialize(now=timestamp)
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO pipeline_edges(
                    source_id, target_id, relation_type, evidence_json,
                    edge_sha256, is_current, created_at_utc
                ) VALUES(?, ?, ?, ?, ?, 1, ?)
                ON CONFLICT(source_id, target_id, relation_type, edge_sha256) DO NOTHING
                """,
                (
                    source_id,
                    target_id,
                    relation_type,
                    canonical_json_text(evidence_payload),
                    edge_sha,
                    timestamp,
                ),
            )
        return {**payload, "edge_sha256": edge_sha}

    def descendants(self, roots: list[str], *, relation_types: set[str] | None = None) -> list[str]:
        pending = sorted(set(roots))
        seen = set(pending)
        descendants: set[str] = set()
        self.initialize()
        with self._connect() as connection:
            while pending:
                source = pending.pop(0)
                if relation_types:
                    placeholders = ",".join("?" for _ in relation_types)
                    rows = connection.execute(
                        f"SELECT target_id FROM pipeline_edges WHERE source_id = ? AND is_current = 1 AND relation_type IN ({placeholders}) ORDER BY target_id",
                        (source, *sorted(relation_types)),
                    ).fetchall()
                else:
                    rows = connection.execute(
                        "SELECT target_id FROM pipeline_edges WHERE source_id = ? AND is_current = 1 ORDER BY target_id",
                        (source,),
                    ).fetchall()
                for row in rows:
                    target = str(row["target_id"])
                    if target not in seen:
                        seen.add(target)
                        descendants.add(target)
                        pending.append(target)
        return sorted(descendants)

    def health(self) -> dict[str, Any]:
        self.initialize() if not self.path.exists() else None
        with self._connect() as connection:
            integrity = str(connection.execute("PRAGMA integrity_check").fetchone()[0])
            counts = {}
            for table in (
                "pipeline_objects",
                "pipeline_edges",
                "pipeline_workflows",
                "pipeline_runs",
                "pipeline_node_states",
                "pipeline_run_events",
                "pipeline_checkpoints",
                "pipeline_incidents",
            ):
                counts[table] = int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
            foundation_counts = {
                "command_count": int(connection.execute("SELECT COUNT(*) FROM commands").fetchone()[0]),
                "event_count": int(connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]),
                "receipt_count": int(connection.execute("SELECT COUNT(*) FROM receipts").fetchone()[0]),
            }
        return {
            "product_id": PRODUCT_ID,
            "product_version": PRODUCT_VERSION,
            "database_path": str(self.path),
            "integrity": integrity,
            "counts": counts,
            **foundation_counts,
            "authority_state": "candidate_not_current",
            "development_authorized": True,
            "production_authorized": False,
            "certified": False,
        }
