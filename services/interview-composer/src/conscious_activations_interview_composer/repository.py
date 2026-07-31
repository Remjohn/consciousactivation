from __future__ import annotations

import json
import sqlite3
from contextlib import closing, contextmanager
from importlib import resources
from pathlib import Path
from typing import Any, Callable, Iterator, Mapping

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.paths import default_database_path
from ca_runtime.database import ProductDatabase

from . import AUTHORITY_STATE, PRODUCT_ID, PRODUCT_VERSION
from .canonical import require_string
from .errors import ConflictError, NotFoundError, ValidationError


class InterviewComposerRepository:
    """Content-addressed, idempotency-keyed SQLite storage for the Composer
    product. A structural sibling of
    ``conscious_activations_interview_expression.repository.InterviewRepository``
    (``ie_`` table prefixes become ``ic_``), with no events/snapshots tables --
    Composer has no live in-session state to event-source (that belongs to
    ``services/interview``)."""

    def __init__(self, database_path: str | Path | None = None):
        self.path = Path(database_path) if database_path else default_database_path(PRODUCT_ID)

    def _connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.path, timeout=10.0, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = FULL")
        return conn

    def foundation_database(self) -> ProductDatabase:
        return ProductDatabase(
            self.path,
            product_id=PRODUCT_ID,
            product_version=PRODUCT_VERSION,
            authority_state=AUTHORITY_STATE,
            development_authorized=True,
            production_authorized=False,
            certified=False,
        )

    @contextmanager
    def _transaction(self, conn: sqlite3.Connection) -> Iterator[None]:
        conn.execute("BEGIN IMMEDIATE")
        try:
            yield
        except Exception:
            conn.execute("ROLLBACK")
            raise
        else:
            conn.execute("COMMIT")

    def initialize(self, *, now: str | None = None) -> dict[str, Any]:
        timestamp = now or utc_now_rfc3339()
        self.foundation_database().initialize(initialized_at_utc=timestamp)
        migration = resources.files("conscious_activations_interview_composer.migrations").joinpath("0001_interview_composer.sql").read_text(encoding="utf-8")
        with closing(self._connect()) as conn:
            metadata = conn.execute("SELECT * FROM product_metadata WHERE product_id=?", (PRODUCT_ID,)).fetchone()
            if metadata is None:
                raise ConflictError("foundation metadata missing after initialization")
            if bool(metadata["production_authorized"]) or bool(metadata["certified"]):
                raise ConflictError("Interview Composer cannot attach to a production-authorized or certified database")
            conn.executescript(migration)
            conn.execute("INSERT INTO ic_migrations(version,name,applied_at_utc) VALUES(1,'0001_interview_composer',?) ON CONFLICT(version) DO NOTHING", (timestamp,))
        return self._health_initialized()

    def execute_idempotent(self, *, command_type: str, idempotency_key: str, payload: Mapping[str, Any], callback: Callable[[sqlite3.Connection, str], dict[str, Any]], now: str | None = None) -> dict[str, Any]:
        key = require_string(idempotency_key, "idempotency_key")
        payload_sha = canonical_sha256(dict(payload))
        timestamp = now or utc_now_rfc3339()
        self.initialize(now=timestamp)
        with closing(self._connect()) as conn:
            existing = conn.execute("SELECT payload_sha256,result_json FROM ic_command_results WHERE idempotency_key=?", (key,)).fetchone()
            if existing:
                if existing["payload_sha256"] != payload_sha:
                    raise ConflictError("idempotency key reused with different payload")
                result = json.loads(existing["result_json"])
                result["idempotent_replay"] = True
                return result
            with self._transaction(conn):
                result = callback(conn, timestamp)
                conn.execute("INSERT INTO ic_command_results(idempotency_key,command_type,payload_sha256,result_json,created_at_utc) VALUES(?,?,?,?,?)", (key, command_type, payload_sha, canonical_json_text(result), timestamp))
            return dict(result)

    def store_object(self, object_type: str, payload: Mapping[str, Any], *, object_id: str, idempotency_key: str, lifecycle_state: str = "ACTIVE", expected_revision: int | None = None, now: str | None = None) -> dict[str, Any]:
        normalized = dict(payload)
        object_sha = canonical_sha256(normalized)

        def write(conn: sqlite3.Connection, timestamp: str) -> dict[str, Any]:
            current = conn.execute("SELECT * FROM ic_objects WHERE object_id=? AND is_current=1", (object_id,)).fetchone()
            current_revision = int(current["revision"]) if current else 0
            if expected_revision is not None and expected_revision != current_revision:
                raise ConflictError(f"expected revision {expected_revision}, current {current_revision}")
            if current and current["canonical_sha256"] == object_sha:
                return {"object": self._row(current), "created": False, "idempotent_replay": False}
            revision = current_revision + 1
            if current:
                conn.execute("UPDATE ic_objects SET is_current=0 WHERE object_id=? AND revision=?", (object_id, current_revision))
            conn.execute("INSERT INTO ic_objects(object_id,revision,object_type,semantic_version,canonical_sha256,payload_json,lifecycle_state,authority_state,is_current,idempotency_key,created_at_utc,supersedes_revision) VALUES(?,?,?,?,?,?,?,?,1,?,?,?)", (object_id, revision, object_type, "1.0.0", object_sha, canonical_json_text(normalized), lifecycle_state, AUTHORITY_STATE, idempotency_key, timestamp, current_revision or None))
            row = conn.execute("SELECT * FROM ic_objects WHERE object_id=? AND revision=?", (object_id, revision)).fetchone()
            return {"object": self._row(row), "created": True, "idempotent_replay": False}

        return self.execute_idempotent(command_type=f"store:{object_type}", idempotency_key=idempotency_key, payload={"object_type": object_type, "object_id": object_id, "payload": normalized}, callback=write, now=now)

    @staticmethod
    def _row(row: sqlite3.Row) -> dict[str, Any]:
        return {"object_id": row["object_id"], "revision": int(row["revision"]), "object_type": row["object_type"], "version": row["semantic_version"], "sha256": row["canonical_sha256"], "payload": json.loads(row["payload_json"]), "lifecycle_state": row["lifecycle_state"], "authority_state": row["authority_state"], "current": bool(row["is_current"]), "created_at_utc": row["created_at_utc"], "supersedes_revision": row["supersedes_revision"]}

    def get_object(self, object_id: str, *, revision: int | None = None) -> dict[str, Any]:
        self.initialize()
        with closing(self._connect()) as conn:
            if revision is None:
                row = conn.execute("SELECT * FROM ic_objects WHERE object_id=? AND is_current=1", (object_id,)).fetchone()
            else:
                row = conn.execute("SELECT * FROM ic_objects WHERE object_id=? AND revision=?", (object_id, revision)).fetchone()
            if row is None:
                raise NotFoundError(f"object not found: {object_id}")
            return self._row(row)

    def list_objects(self, object_type: str | None = None) -> list[dict[str, Any]]:
        self.initialize()
        with closing(self._connect()) as conn:
            if object_type:
                rows = conn.execute("SELECT * FROM ic_objects WHERE object_type=? AND is_current=1 ORDER BY object_id", (object_type,)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM ic_objects WHERE is_current=1 ORDER BY object_type,object_id").fetchall()
            return [self._row(r) for r in rows]

    def add_edge(self, parent_id: str, child_id: str, relation: str) -> None:
        self.initialize()
        with closing(self._connect()) as conn:
            conn.execute("INSERT OR IGNORE INTO ic_edges(parent_id,child_id,relation) VALUES(?,?,?)", (parent_id, child_id, relation))

    def _health_initialized(self) -> dict[str, Any]:
        foundation = self.foundation_database().health().to_dict()
        with closing(self._connect()) as conn:
            counts = {table: int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]) for table in ["ic_objects", "ic_edges", "ic_command_results"]}
        return {
            **foundation,
            "development_authorized": True,
            "production_authorized": False,
            "certified": False,
            **counts,
        }

    def health(self) -> dict[str, Any]:
        self.initialize()
        return self._health_initialized()
