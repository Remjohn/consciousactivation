from __future__ import annotations

import json
import sqlite3
from contextlib import closing, contextmanager
from importlib import resources
from pathlib import Path
from typing import Any, Iterator, Mapping

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339

from .errors import LeaseConflict, QueueConflict, VAEError
from .validation import reject_noncanonical, require_string, semantic_id


class VAERepository:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def _connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path, isolation_level=None, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA synchronous=FULL")
        return connection

    @contextmanager
    def _tx(self, connection: sqlite3.Connection) -> Iterator[None]:
        connection.execute("BEGIN IMMEDIATE")
        try:
            yield
        except Exception:
            connection.execute("ROLLBACK")
            raise
        else:
            connection.execute("COMMIT")

    def initialize(self) -> dict[str, Any]:
        sql = resources.files("cmf_vae.migrations").joinpath("0001_phase8.sql").read_text(encoding="utf-8")
        with closing(self._connect()) as connection:
            connection.executescript(sql)
        return self.health()

    def store_object(
        self,
        object_type: str,
        payload: Mapping[str, Any],
        *,
        object_id: str | None = None,
        version: str = "1.0.0",
        lifecycle_state: str,
        idempotency_key: str,
        created_at_utc: str | None = None,
    ) -> dict[str, Any]:
        reject_noncanonical(payload)
        oid = object_id or semantic_id(object_type.replace("_", "-"), payload)
        timestamp = created_at_utc or utc_now_rfc3339()
        payload_sha = canonical_sha256(payload)
        result = {
            "object_id": oid,
            "object_type": object_type,
            "version": version,
            "sha256": payload_sha,
            "lifecycle_state": lifecycle_state,
            "payload": dict(payload),
            "created_at_utc": timestamp,
        }
        request_sha = canonical_sha256({"object_type": object_type, "payload": payload, "object_id": oid, "version": version, "lifecycle_state": lifecycle_state})
        with closing(self._connect()) as connection:
            existing = connection.execute("SELECT payload_sha256,result_json FROM vae_idempotency WHERE idempotency_key=?", (idempotency_key,)).fetchone()
            if existing:
                if existing["payload_sha256"] != request_sha:
                    raise QueueConflict("idempotency key reused with different object bytes")
                return json.loads(existing["result_json"])
            with self._tx(connection):
                current = connection.execute("SELECT sha256,payload_json FROM vae_objects WHERE object_id=?", (oid,)).fetchone()
                if current and (current["sha256"] != payload_sha or current["payload_json"] != canonical_json_text(payload)):
                    raise QueueConflict(f"immutable object identity collision: {oid}")
                if current is None:
                    connection.execute(
                        "INSERT INTO vae_objects VALUES(?,?,?,?,?,?,?)",
                        (oid, object_type, version, canonical_json_text(payload), payload_sha, lifecycle_state, timestamp),
                    )
                connection.execute(
                    "INSERT INTO vae_idempotency VALUES(?,?,?)",
                    (idempotency_key, request_sha, canonical_json_text(result)),
                )
        return result

    def get_object(self, object_id: str) -> dict[str, Any]:
        with closing(self._connect()) as connection:
            row = connection.execute("SELECT * FROM vae_objects WHERE object_id=?", (object_id,)).fetchone()
        if row is None:
            raise VAEError(f"unknown VAE object: {object_id}")
        return {
            "object_id": row["object_id"],
            "object_type": row["object_type"],
            "version": row["version"],
            "sha256": row["sha256"],
            "lifecycle_state": row["lifecycle_state"],
            "payload": json.loads(row["payload_json"]),
            "created_at_utc": row["created_at_utc"],
        }

    def add_edge(self, parent_id: str, child_id: str, relation: str) -> None:
        with closing(self._connect()) as connection:
            connection.execute("INSERT OR IGNORE INTO vae_edges VALUES(?,?,?)", (parent_id, child_id, relation))

    def descendants(self, object_id: str) -> list[dict[str, str]]:
        query = """
        WITH RECURSIVE walk(parent_id,child_id,relation,depth) AS (
          SELECT parent_id,child_id,relation,1 FROM vae_edges WHERE parent_id=?
          UNION ALL
          SELECT e.parent_id,e.child_id,e.relation,w.depth+1 FROM vae_edges e JOIN walk w ON e.parent_id=w.child_id
        ) SELECT parent_id,child_id,relation,MIN(depth) AS depth FROM walk GROUP BY parent_id,child_id,relation ORDER BY depth,child_id
        """
        with closing(self._connect()) as connection:
            rows = connection.execute(query, (object_id,)).fetchall()
        return [{"parent_id": r["parent_id"], "child_id": r["child_id"], "relation": r["relation"], "depth": r["depth"]} for r in rows]

    def register_worker(self, worker_id: str, capability_ids: list[str], attestation_sha256: str, *, now: str | None = None) -> dict[str, Any]:
        timestamp = now or utc_now_rfc3339()
        caps = sorted(set(require_string(item, "capability_id") for item in capability_ids))
        with closing(self._connect()) as connection:
            row = connection.execute("SELECT * FROM vae_workers WHERE worker_id=?", (worker_id,)).fetchone()
            if row and (json.loads(row["capability_ids_json"]) != caps or row["attestation_sha256"] != attestation_sha256):
                raise QueueConflict("worker identity reused with different attestation")
            connection.execute(
                "INSERT INTO vae_workers VALUES(?,?,?,?,?) ON CONFLICT(worker_id) DO UPDATE SET state='READY'",
                (worker_id, canonical_json_text(caps), attestation_sha256, "READY", timestamp),
            )
        return {"worker_id": worker_id, "capability_ids": caps, "attestation_sha256": attestation_sha256, "state": "READY"}

    def _event(self, connection: sqlite3.Connection, job_id: str, event_type: str, payload: Mapping[str, Any], timestamp: str) -> dict[str, Any]:
        event = {"job_id": job_id, "event_type": event_type, "payload": dict(payload), "occurred_at_utc": timestamp}
        event_id = semantic_id("vae-event", event)
        payload_sha = canonical_sha256(payload)
        connection.execute(
            "INSERT INTO vae_job_events(event_id,job_id,event_type,payload_json,payload_sha256,occurred_at_utc) VALUES(?,?,?,?,?,?)",
            (event_id, job_id, event_type, canonical_json_text(payload), payload_sha, timestamp),
        )
        sequence = connection.execute("SELECT sequence FROM vae_job_events WHERE event_id=?", (event_id,)).fetchone()["sequence"]
        outbox_payload = {"event_id": event_id, "job_id": job_id, "sequence": sequence, "event_type": event_type, "payload_sha256": payload_sha}
        connection.execute(
            "INSERT INTO vae_outbox VALUES(?,?,?,?,?,?)",
            (semantic_id("outbox", outbox_payload), job_id, sequence, canonical_json_text(outbox_payload), 0, timestamp),
        )
        return {**outbox_payload, "occurred_at_utc": timestamp}

    def submit_job(self, request: Mapping[str, Any], required_capabilities: list[str], *, idempotency_key: str, maximum_attempts: int = 3, now: str | None = None) -> dict[str, Any]:
        reject_noncanonical(request)
        timestamp = now or utc_now_rfc3339()
        request_sha = canonical_sha256(request)
        job_id = semantic_id("vae-job", {"request_sha256": request_sha, "idempotency_key": idempotency_key})
        capabilities = sorted(set(required_capabilities))
        with closing(self._connect()) as connection:
            existing = connection.execute("SELECT * FROM vae_jobs WHERE idempotency_key=?", (idempotency_key,)).fetchone()
            if existing:
                if existing["request_sha256"] != request_sha:
                    raise QueueConflict("job idempotency key reused with different request bytes")
                return self._job_row(existing)
            with self._tx(connection):
                connection.execute(
                    "INSERT INTO vae_jobs(job_id,idempotency_key,request_sha256,request_json,required_capabilities_json,state,attempt_number,maximum_attempts,created_at_utc,updated_at_utc) VALUES(?,?,?,?,?,'QUEUED',0,?,?,?)",
                    (job_id, idempotency_key, request_sha, canonical_json_text(request), canonical_json_text(capabilities), maximum_attempts, timestamp, timestamp),
                )
                self._event(connection, job_id, "SUBMITTED", {"state": "QUEUED", "required_capabilities": capabilities}, timestamp)
        return self.get_job(job_id)

    def lease_next(self, worker_id: str, *, now_ms: int, lease_ms: int = 30000, now: str | None = None) -> dict[str, Any] | None:
        timestamp = now or utc_now_rfc3339()
        with closing(self._connect()) as connection:
            worker = connection.execute("SELECT * FROM vae_workers WHERE worker_id=? AND state='READY'", (worker_id,)).fetchone()
            if not worker:
                raise LeaseConflict("worker is not registered and ready")
            worker_caps = set(json.loads(worker["capability_ids_json"]))
            rows = connection.execute("SELECT * FROM vae_jobs WHERE state IN ('QUEUED','RETRY_READY') ORDER BY created_at_utc,job_id").fetchall()
            selected = None
            for row in rows:
                if set(json.loads(row["required_capabilities_json"])) <= worker_caps:
                    selected = row
                    break
            if selected is None:
                return None
            token = semantic_id("fence", {"job_id": selected["job_id"], "worker_id": worker_id, "lease_generation": selected["attempt_number"] + 1, "now_ms": now_ms})
            with self._tx(connection):
                connection.execute(
                    "UPDATE vae_jobs SET state='LEASED',attempt_number=attempt_number+1,lease_owner=?,fencing_token=?,lease_until_ms=?,updated_at_utc=? WHERE job_id=? AND state IN ('QUEUED','RETRY_READY')",
                    (worker_id, token, now_ms + lease_ms, timestamp, selected["job_id"]),
                )
                if connection.total_changes < 1:
                    raise LeaseConflict("job lease lost to another worker")
                self._event(connection, selected["job_id"], "LEASED", {"worker_id": worker_id, "fencing_token": token, "lease_until_ms": now_ms + lease_ms}, timestamp)
        return self.get_job(selected["job_id"])

    def renew_lease(self, job_id: str, worker_id: str, token: str, *, now_ms: int, lease_ms: int = 30000, now: str | None = None) -> dict[str, Any]:
        timestamp = now or utc_now_rfc3339()
        with closing(self._connect()) as connection:
            row = connection.execute("SELECT * FROM vae_jobs WHERE job_id=?", (job_id,)).fetchone()
            self._assert_lease(row, worker_id, token, now_ms, allow_expired=False)
            with self._tx(connection):
                connection.execute("UPDATE vae_jobs SET lease_until_ms=?,updated_at_utc=? WHERE job_id=?", (now_ms + lease_ms, timestamp, job_id))
                self._event(connection, job_id, "LEASE_RENEWED", {"lease_until_ms": now_ms + lease_ms}, timestamp)
        return self.get_job(job_id)

    def checkpoint(self, job_id: str, worker_id: str, token: str, checkpoint: Mapping[str, Any], *, now_ms: int, now: str | None = None) -> dict[str, Any]:
        timestamp = now or utc_now_rfc3339(); reject_noncanonical(checkpoint)
        with closing(self._connect()) as connection:
            row = connection.execute("SELECT * FROM vae_jobs WHERE job_id=?", (job_id,)).fetchone()
            self._assert_lease(row, worker_id, token, now_ms, allow_expired=False)
            with self._tx(connection):
                connection.execute("UPDATE vae_jobs SET checkpoint_json=?,updated_at_utc=? WHERE job_id=?", (canonical_json_text(checkpoint), timestamp, job_id))
                self._event(connection, job_id, "CHECKPOINTED", {"checkpoint_sha256": canonical_sha256(checkpoint)}, timestamp)
        return self.get_job(job_id)

    def request_cancel(self, job_id: str, *, reason: str, now: str | None = None) -> dict[str, Any]:
        timestamp = now or utc_now_rfc3339()
        with closing(self._connect()) as connection:
            row = connection.execute("SELECT * FROM vae_jobs WHERE job_id=?", (job_id,)).fetchone()
            if row is None: raise VAEError(f"unknown job: {job_id}")
            if row["state"] in {"COMPLETED", "FAILED", "CANCELLED"}:
                raise QueueConflict("terminal job cannot be cancelled")
            with self._tx(connection):
                connection.execute("UPDATE vae_jobs SET cancellation_requested=1,state='CANCELLATION_REQUESTED',updated_at_utc=? WHERE job_id=?", (timestamp, job_id))
                self._event(connection, job_id, "CANCELLATION_REQUESTED", {"reason": require_string(reason, "reason")}, timestamp)
        return self.get_job(job_id)

    def complete_job(self, job_id: str, worker_id: str, token: str, result: Mapping[str, Any], *, now_ms: int, now: str | None = None) -> dict[str, Any]:
        timestamp = now or utc_now_rfc3339(); reject_noncanonical(result)
        with closing(self._connect()) as connection:
            row = connection.execute("SELECT * FROM vae_jobs WHERE job_id=?", (job_id,)).fetchone()
            if row is None: raise VAEError(f"unknown job: {job_id}")
            if row["cancellation_requested"] or row["state"] == "CANCELLATION_REQUESTED":
                with self._tx(connection):
                    connection.execute("UPDATE vae_jobs SET state='LATE_RESULT_QUARANTINED',result_json=?,updated_at_utc=? WHERE job_id=?", (canonical_json_text(result), timestamp, job_id))
                    self._event(connection, job_id, "LATE_RESULT_QUARANTINED", {"result_sha256": canonical_sha256(result)}, timestamp)
                return self.get_job(job_id)
            self._assert_lease(row, worker_id, token, now_ms, allow_expired=False)
            with self._tx(connection):
                connection.execute("UPDATE vae_jobs SET state='COMPLETED',result_json=?,lease_owner=NULL,fencing_token=NULL,lease_until_ms=NULL,updated_at_utc=? WHERE job_id=?", (canonical_json_text(result), timestamp, job_id))
                self._event(connection, job_id, "COMPLETED", {"result_sha256": canonical_sha256(result)}, timestamp)
        return self.get_job(job_id)

    def fail_job(self, job_id: str, worker_id: str, token: str, failure: Mapping[str, Any], *, now_ms: int, retryable: bool, now: str | None = None) -> dict[str, Any]:
        timestamp = now or utc_now_rfc3339(); reject_noncanonical(failure)
        with closing(self._connect()) as connection:
            row = connection.execute("SELECT * FROM vae_jobs WHERE job_id=?", (job_id,)).fetchone()
            self._assert_lease(row, worker_id, token, now_ms, allow_expired=True)
            next_state = "RETRY_READY" if retryable and row["attempt_number"] < row["maximum_attempts"] else "FAILED"
            with self._tx(connection):
                connection.execute("UPDATE vae_jobs SET state=?,failure_json=?,lease_owner=NULL,fencing_token=NULL,lease_until_ms=NULL,updated_at_utc=? WHERE job_id=?", (next_state, canonical_json_text(failure), timestamp, job_id))
                self._event(connection, job_id, next_state, {"failure_sha256": canonical_sha256(failure), "retryable": retryable}, timestamp)
        return self.get_job(job_id)

    def recover_expired(self, *, now_ms: int, now: str | None = None) -> list[dict[str, Any]]:
        timestamp = now or utc_now_rfc3339(); recovered=[]
        with closing(self._connect()) as connection:
            rows=connection.execute("SELECT * FROM vae_jobs WHERE state IN ('LEASED','CANCELLATION_REQUESTED') AND lease_until_ms IS NOT NULL AND lease_until_ms<? ORDER BY job_id", (now_ms,)).fetchall()
            with self._tx(connection):
                for row in rows:
                    state = "CANCELLED" if row["cancellation_requested"] else "RETRY_READY"
                    connection.execute("UPDATE vae_jobs SET state=?,lease_owner=NULL,fencing_token=NULL,lease_until_ms=NULL,updated_at_utc=? WHERE job_id=?", (state,timestamp,row["job_id"]))
                    self._event(connection,row["job_id"],"LEASE_EXPIRED_RECOVERED",{"next_state":state,"checkpoint_preserved":row["checkpoint_json"] is not None},timestamp)
                    recovered.append({"job_id":row["job_id"],"state":state})
        return recovered

    def get_job(self, job_id: str) -> dict[str, Any]:
        with closing(self._connect()) as connection:
            row=connection.execute("SELECT * FROM vae_jobs WHERE job_id=?",(job_id,)).fetchone()
        if row is None: raise VAEError(f"unknown job: {job_id}")
        return self._job_row(row)

    def list_job_events(self, job_id: str) -> list[dict[str, Any]]:
        with closing(self._connect()) as connection:
            rows=connection.execute("SELECT * FROM vae_job_events WHERE job_id=? ORDER BY sequence",(job_id,)).fetchall()
        return [{"sequence":r["sequence"],"event_id":r["event_id"],"event_type":r["event_type"],"payload":json.loads(r["payload_json"]),"payload_sha256":r["payload_sha256"],"occurred_at_utc":r["occurred_at_utc"]} for r in rows]

    def outbox(self, *, undelivered_only: bool = False) -> list[dict[str, Any]]:
        where="WHERE delivered=0" if undelivered_only else ""
        with closing(self._connect()) as connection:
            rows=connection.execute(f"SELECT * FROM vae_outbox {where} ORDER BY event_sequence").fetchall()
        return [{"outbox_id":r["outbox_id"],"job_id":r["job_id"],"event_sequence":r["event_sequence"],"payload":json.loads(r["payload_json"]),"delivered":bool(r["delivered"])} for r in rows]

    def health(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"database_path":str(self.path),"integrity":"NOT_INITIALIZED","object_count":0,"job_count":0,"worker_count":0,"event_count":0}
        with closing(self._connect()) as connection:
            integrity=connection.execute("PRAGMA integrity_check").fetchone()[0]
            counts={name:connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] for name,table in {"object_count":"vae_objects","job_count":"vae_jobs","worker_count":"vae_workers","event_count":"vae_job_events"}.items()}
        return {"database_path":str(self.path),"integrity":integrity,**counts}

    @staticmethod
    def _assert_lease(row: sqlite3.Row | None, worker_id: str, token: str, now_ms: int, *, allow_expired: bool) -> None:
        if row is None: raise LeaseConflict("job missing")
        if row["state"] != "LEASED": raise LeaseConflict(f"job not leased: {row['state']}")
        if row["lease_owner"] != worker_id or row["fencing_token"] != token: raise LeaseConflict("worker or fencing token mismatch")
        if not allow_expired and row["lease_until_ms"] is not None and row["lease_until_ms"] < now_ms: raise LeaseConflict("lease expired")

    @staticmethod
    def _job_row(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "job_id":row["job_id"],"idempotency_key":row["idempotency_key"],"request_sha256":row["request_sha256"],"request":json.loads(row["request_json"]),"required_capabilities":json.loads(row["required_capabilities_json"]),"state":row["state"],"attempt_number":row["attempt_number"],"maximum_attempts":row["maximum_attempts"],"lease_owner":row["lease_owner"],"fencing_token":row["fencing_token"],"lease_until_ms":row["lease_until_ms"],"cancellation_requested":bool(row["cancellation_requested"]),"checkpoint":json.loads(row["checkpoint_json"]) if row["checkpoint_json"] else None,"result":json.loads(row["result_json"]) if row["result_json"] else None,"failure":json.loads(row["failure_json"]) if row["failure_json"] else None,"created_at_utc":row["created_at_utc"],"updated_at_utc":row["updated_at_utc"]}
