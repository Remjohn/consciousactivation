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


class InterviewRepository:
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
        migration = resources.files("conscious_activations_interview_expression.migrations").joinpath("0001_interview_expression.sql").read_text(encoding="utf-8")
        with closing(self._connect()) as conn:
            metadata = conn.execute("SELECT * FROM product_metadata WHERE product_id=?", (PRODUCT_ID,)).fetchone()
            if metadata is None:
                raise ConflictError("foundation metadata missing after initialization")
            if bool(metadata["production_authorized"]) or bool(metadata["certified"]):
                raise ConflictError("Phase 4 cannot attach to a production-authorized or certified database")
            conn.executescript(migration)
            conn.execute("INSERT INTO ie_migrations(version,name,applied_at_utc) VALUES(1,'0001_interview_expression',?) ON CONFLICT(version) DO NOTHING", (timestamp,))
        return self._health_initialized()

    def execute_idempotent(self, *, command_type: str, idempotency_key: str, payload: Mapping[str, Any], callback: Callable[[sqlite3.Connection,str], dict[str,Any]], now: str | None = None) -> dict[str, Any]:
        key = require_string(idempotency_key, "idempotency_key")
        payload_sha = canonical_sha256(dict(payload))
        timestamp = now or utc_now_rfc3339()
        self.initialize(now=timestamp)
        with closing(self._connect()) as conn:
            existing = conn.execute("SELECT payload_sha256,result_json FROM ie_command_results WHERE idempotency_key=?", (key,)).fetchone()
            if existing:
                if existing["payload_sha256"] != payload_sha:
                    raise ConflictError("idempotency key reused with different payload")
                result = json.loads(existing["result_json"])
                result["idempotent_replay"] = True
                return result
            with self._transaction(conn):
                result = callback(conn, timestamp)
                conn.execute("INSERT INTO ie_command_results(idempotency_key,command_type,payload_sha256,result_json,created_at_utc) VALUES(?,?,?,?,?)", (key, command_type, payload_sha, canonical_json_text(result), timestamp))
            return dict(result)

    def store_object(self, object_type: str, payload: Mapping[str, Any], *, object_id: str, idempotency_key: str, lifecycle_state: str = "ACTIVE", expected_revision: int | None = None, now: str | None = None) -> dict[str, Any]:
        normalized = dict(payload)
        object_sha = canonical_sha256(normalized)
        def write(conn: sqlite3.Connection, timestamp: str) -> dict[str, Any]:
            current = conn.execute("SELECT * FROM ie_objects WHERE object_id=? AND is_current=1", (object_id,)).fetchone()
            current_revision = int(current["revision"]) if current else 0
            if expected_revision is not None and expected_revision != current_revision:
                raise ConflictError(f"expected revision {expected_revision}, current {current_revision}")
            if current and current["canonical_sha256"] == object_sha:
                return {"object": self._row(current), "created": False, "idempotent_replay": False}
            revision = current_revision + 1
            if current:
                conn.execute("UPDATE ie_objects SET is_current=0 WHERE object_id=? AND revision=?", (object_id, current_revision))
            conn.execute("INSERT INTO ie_objects(object_id,revision,object_type,semantic_version,canonical_sha256,payload_json,lifecycle_state,authority_state,is_current,idempotency_key,created_at_utc,supersedes_revision) VALUES(?,?,?,?,?,?,?,?,1,?,?,?)", (object_id, revision, object_type, "1.0.0", object_sha, canonical_json_text(normalized), lifecycle_state, AUTHORITY_STATE, idempotency_key, timestamp, current_revision or None))
            row = conn.execute("SELECT * FROM ie_objects WHERE object_id=? AND revision=?", (object_id, revision)).fetchone()
            return {"object": self._row(row), "created": True, "idempotent_replay": False}
        return self.execute_idempotent(command_type=f"store:{object_type}", idempotency_key=idempotency_key, payload={"object_type": object_type, "object_id": object_id, "payload": normalized}, callback=write, now=now)

    @staticmethod
    def _row(row: sqlite3.Row) -> dict[str, Any]:
        return {"object_id": row["object_id"], "revision": int(row["revision"]), "object_type": row["object_type"], "version": row["semantic_version"], "sha256": row["canonical_sha256"], "payload": json.loads(row["payload_json"]), "lifecycle_state": row["lifecycle_state"], "authority_state": row["authority_state"], "current": bool(row["is_current"]), "created_at_utc": row["created_at_utc"], "supersedes_revision": row["supersedes_revision"]}

    def get_object(self, object_id: str, *, revision: int | None = None) -> dict[str, Any]:
        self.initialize()
        with closing(self._connect()) as conn:
            if revision is None:
                row = conn.execute("SELECT * FROM ie_objects WHERE object_id=? AND is_current=1", (object_id,)).fetchone()
            else:
                row = conn.execute("SELECT * FROM ie_objects WHERE object_id=? AND revision=?", (object_id, revision)).fetchone()
            if row is None:
                raise NotFoundError(f"object not found: {object_id}")
            return self._row(row)

    def get_object_by_sha(self, object_id: str, sha256: str) -> dict[str, Any]:
        self.initialize()
        with closing(self._connect()) as conn:
            row = conn.execute("SELECT * FROM ie_objects WHERE object_id=? AND canonical_sha256=? ORDER BY revision DESC LIMIT 1", (object_id, sha256)).fetchone()
            if row is None:
                raise NotFoundError(f"object version not found: {object_id}@{sha256}")
            return self._row(row)

    def list_objects(self, object_type: str | None = None) -> list[dict[str, Any]]:
        self.initialize()
        with closing(self._connect()) as conn:
            if object_type:
                rows = conn.execute("SELECT * FROM ie_objects WHERE object_type=? AND is_current=1 ORDER BY object_id", (object_type,)).fetchall()
            else:
                rows = conn.execute("SELECT * FROM ie_objects WHERE is_current=1 ORDER BY object_type,object_id").fetchall()
            return [self._row(r) for r in rows]

    def add_edge(self, parent_id: str, child_id: str, relation: str) -> None:
        self.initialize()
        with closing(self._connect()) as conn:
            conn.execute("INSERT OR IGNORE INTO ie_edges(parent_id,child_id,relation) VALUES(?,?,?)", (parent_id, child_id, relation))

    def descendants(self, object_id: str) -> list[dict[str, str]]:
        self.initialize()
        with closing(self._connect()) as conn:
            rows = conn.execute("WITH RECURSIVE d(parent_id,child_id,relation) AS (SELECT parent_id,child_id,relation FROM ie_edges WHERE parent_id=? UNION SELECT e.parent_id,e.child_id,e.relation FROM ie_edges e JOIN d ON e.parent_id=d.child_id) SELECT DISTINCT parent_id,child_id,relation FROM d ORDER BY parent_id,child_id,relation", (object_id,)).fetchall()
            return [dict(r) for r in rows]

    def append_event(self, *, aggregate_id: str, event_type: str, payload: Mapping[str, Any], snapshot: Mapping[str, Any], expected_sequence: int, idempotency_key: str, now: str | None = None) -> dict[str, Any]:
        normalized = dict(payload); snap = dict(snapshot)
        def write(conn: sqlite3.Connection, timestamp: str) -> dict[str, Any]:
            last = conn.execute("SELECT * FROM ie_events WHERE aggregate_id=? ORDER BY sequence DESC LIMIT 1", (aggregate_id,)).fetchone()
            current = int(last["sequence"]) if last else 0
            if current != expected_sequence:
                raise ConflictError(f"STALE_PROJECTION expected {expected_sequence}, current {current}")
            previous_sha = last["payload_sha256"] if last else None
            sequence = current + 1
            event_core = {"aggregate_id": aggregate_id, "sequence": sequence, "event_type": event_type, "payload": normalized, "previous_event_sha256": previous_sha}
            event_id = f"ie:event:{canonical_sha256(event_core)[:32]}"
            event_sha = canonical_sha256(event_core)
            conn.execute("INSERT INTO ie_events(event_id,aggregate_id,sequence,event_type,payload_sha256,payload_json,previous_event_sha256,occurred_at_utc,idempotency_key) VALUES(?,?,?,?,?,?,?,?,?)", (event_id, aggregate_id, sequence, event_type, event_sha, canonical_json_text(normalized), previous_sha, timestamp, idempotency_key))
            snapshot_sha = canonical_sha256(snap)
            conn.execute("INSERT INTO ie_session_snapshots(session_id,sequence,snapshot_sha256,snapshot_json,created_at_utc) VALUES(?,?,?,?,?)", (aggregate_id, sequence, snapshot_sha, canonical_json_text(snap), timestamp))
            return {"event_id": event_id, "event_sha256": event_sha, "sequence": sequence, "snapshot_sha256": snapshot_sha, "snapshot": snap, "idempotent_replay": False}
        return self.execute_idempotent(command_type=f"event:{event_type}", idempotency_key=idempotency_key, payload={"aggregate_id": aggregate_id, "expected_sequence": expected_sequence, "event_type": event_type, "payload": normalized, "snapshot": snap}, callback=write, now=now)

    def events(self, aggregate_id: str) -> list[dict[str, Any]]:
        self.initialize()
        with closing(self._connect()) as conn:
            rows = conn.execute("SELECT * FROM ie_events WHERE aggregate_id=? ORDER BY sequence", (aggregate_id,)).fetchall()
            return [{"event_id": r["event_id"], "sequence": int(r["sequence"]), "event_type": r["event_type"], "payload_sha256": r["payload_sha256"], "payload": json.loads(r["payload_json"]), "previous_event_sha256": r["previous_event_sha256"], "occurred_at_utc": r["occurred_at_utc"]} for r in rows]

    def latest_snapshot(self, session_id: str) -> dict[str, Any] | None:
        self.initialize()
        with closing(self._connect()) as conn:
            row = conn.execute("SELECT * FROM ie_session_snapshots WHERE session_id=? ORDER BY sequence DESC LIMIT 1", (session_id,)).fetchone()
            if row is None: return None
            return {"session_id": session_id, "sequence": int(row["sequence"]), "sha256": row["snapshot_sha256"], "snapshot": json.loads(row["snapshot_json"]), "created_at_utc": row["created_at_utc"]}

    def _health_initialized(self) -> dict[str, Any]:
        foundation = self.foundation_database().health().to_dict()
        with closing(self._connect()) as conn:
            counts = {table: int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]) for table in ["ie_objects","ie_edges","ie_events","ie_command_results"]}
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

