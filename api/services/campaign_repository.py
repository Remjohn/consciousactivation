from __future__ import annotations

"""TS-APP-API-004 Stage 2 -- SQLite persistence for CampaignOrder /
CampaignState, following the exact idempotent-object-store pattern
InterviewRepository and ca_runtime.database.ProductDatabase already
establish elsewhere in this codebase."""

import json
import sqlite3
from contextlib import closing, contextmanager
from pathlib import Path
from typing import Any, Iterator

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339
from ca_runtime.database import ProductDatabase

PRODUCT_ID = "ca-campaigns-api"
PRODUCT_VERSION = "0.1.0.dev1"
AUTHORITY_STATE = "phase_09_development_release_candidate"

MIGRATION_SQL = """
CREATE TABLE IF NOT EXISTS campaign_migrations(
  version INTEGER PRIMARY KEY, name TEXT NOT NULL, applied_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS campaign_command_results(
  idempotency_key TEXT PRIMARY KEY, command_type TEXT NOT NULL,
  payload_sha256 TEXT NOT NULL, result_json TEXT NOT NULL, created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS campaign_orders(
  order_id TEXT PRIMARY KEY, workspace_id TEXT NOT NULL, project_id TEXT NOT NULL,
  canonical_sha256 TEXT NOT NULL, payload_json TEXT NOT NULL, created_at_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS campaign_states(
  campaign_id TEXT PRIMARY KEY, order_id TEXT NOT NULL REFERENCES campaign_orders(order_id),
  lifecycle_state TEXT NOT NULL, payload_json TEXT NOT NULL, version INTEGER NOT NULL,
  updated_at_utc TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS campaign_states_by_lifecycle ON campaign_states(lifecycle_state);
"""


class CampaignConflictError(RuntimeError):
    code = "CONFLICT"


class CampaignNotFoundError(RuntimeError):
    code = "CAMPAIGN_NOT_FOUND"


class CampaignRepository:
    def __init__(self, database_path: str | Path):
        self.path = Path(database_path)

    def _connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.path, timeout=10.0, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = FULL")
        return conn

    def initialize(self) -> None:
        ProductDatabase(
            self.path, product_id=PRODUCT_ID, product_version=PRODUCT_VERSION,
            authority_state=AUTHORITY_STATE, development_authorized=True,
        ).initialize(initialized_at_utc=utc_now_rfc3339())
        with closing(self._connect()) as conn:
            conn.executescript(MIGRATION_SQL)
            conn.execute(
                "INSERT OR IGNORE INTO campaign_migrations(version, name, applied_at_utc) VALUES (1, 'campaign_core', ?)",
                (utc_now_rfc3339(),),
            )

    def status(self) -> dict[str, Any]:
        with closing(self._connect()) as conn:
            orders = conn.execute("SELECT COUNT(*) FROM campaign_orders").fetchone()[0]
            states = conn.execute("SELECT COUNT(*) FROM campaign_states").fetchone()[0]
        return {
            "product_id": PRODUCT_ID, "product_version": PRODUCT_VERSION, "authority_state": AUTHORITY_STATE,
            "database_path": str(self.path), "integrity": "ok", "command_count": orders,
            "event_count": states, "receipt_count": 0, "production_authorized": False, "certified": False,
            "claim_ceiling": "CAMPAIGN_ORDER_PRE_PUBLICATION_SOURCE_EVIDENCE",
        }

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

    def create(self, order: dict[str, Any], state: dict[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        """Two independent idempotency layers, matching InterviewRepository's
        established pattern: (1) exact idempotency_key replay via the command
        log; (2) content-addressed replay when order_id/campaign_id already
        exist under a *different* key -- returns the EXISTING stored state,
        never a freshly re-launched one, so a duplicate create can never roll
        back a campaign that has already transitioned."""
        timestamp = utc_now_rfc3339()
        with closing(self._connect()) as conn:
            cached = conn.execute(
                "SELECT result_json FROM campaign_command_results WHERE idempotency_key=?", (idempotency_key,)
            ).fetchone()
            if cached is not None:
                result = json.loads(cached["result_json"])
                result["idempotent_replay"] = True
                return result
            with self._transaction(conn):
                order_row = conn.execute(
                    "SELECT payload_json FROM campaign_orders WHERE order_id=?", (order["order_id"],)
                ).fetchone()
                state_row = conn.execute(
                    "SELECT payload_json FROM campaign_states WHERE campaign_id=?", (state["campaign_id"],)
                ).fetchone()
                content_addressed_replay = order_row is not None and state_row is not None
                if order_row is None:
                    conn.execute(
                        "INSERT INTO campaign_orders(order_id, workspace_id, project_id, canonical_sha256, payload_json, created_at_utc) VALUES (?,?,?,?,?,?)",
                        (order["order_id"], order["workspace_id"], order["project_id"], canonical_sha256(order), canonical_json_text(order), timestamp),
                    )
                if state_row is None:
                    conn.execute(
                        "INSERT INTO campaign_states(campaign_id, order_id, lifecycle_state, payload_json, version, updated_at_utc) VALUES (?,?,?,?,?,?)",
                        (state["campaign_id"], order["order_id"], state["lifecycle_state"], canonical_json_text(state), state["version"], timestamp),
                    )
                final_order = json.loads(order_row["payload_json"]) if order_row is not None else order
                final_state = json.loads(state_row["payload_json"]) if state_row is not None else state
                result = {"order": final_order, "state": final_state, "idempotent_replay": content_addressed_replay}
                conn.execute(
                    "INSERT INTO campaign_command_results(idempotency_key, command_type, payload_sha256, result_json, created_at_utc) VALUES (?,?,?,?,?)",
                    (idempotency_key, "create_campaign", order["order_id"], canonical_json_text(result), timestamp),
                )
            return result

    def get(self, campaign_id: str) -> dict[str, Any]:
        with closing(self._connect()) as conn:
            row = conn.execute(
                "SELECT cs.payload_json AS state_json, co.payload_json AS order_json "
                "FROM campaign_states cs JOIN campaign_orders co ON co.order_id = cs.order_id "
                "WHERE cs.campaign_id=?", (campaign_id,),
            ).fetchone()
        if row is None:
            raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
        return {"order": json.loads(row["order_json"]), "state": json.loads(row["state_json"])}

    def list(
        self, *, workspace_id: str | None = None, project_id: str | None = None, lifecycle_state: str | None = None
    ) -> list[dict[str, Any]]:
        clauses, params = [], []
        if workspace_id is not None:
            clauses.append("co.workspace_id = ?"); params.append(workspace_id)
        if project_id is not None:
            clauses.append("co.project_id = ?"); params.append(project_id)
        if lifecycle_state is not None:
            clauses.append("cs.lifecycle_state = ?"); params.append(lifecycle_state)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with closing(self._connect()) as conn:
            rows = conn.execute(
                f"SELECT cs.payload_json AS state_json, co.payload_json AS order_json "
                f"FROM campaign_states cs JOIN campaign_orders co ON co.order_id = cs.order_id "
                f"{where} ORDER BY co.created_at_utc DESC",
                params,
            ).fetchall()
        return [{"order": json.loads(r["order_json"]), "state": json.loads(r["state_json"])} for r in rows]

    def update_state(self, campaign_id: str, new_state: dict[str, Any], *, expected_version: int) -> dict[str, Any]:
        timestamp = utc_now_rfc3339()
        with closing(self._connect()) as conn:
            with self._transaction(conn):
                row = conn.execute("SELECT version FROM campaign_states WHERE campaign_id=?", (campaign_id,)).fetchone()
                if row is None:
                    raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
                if int(row["version"]) != expected_version:
                    raise CampaignConflictError(f"expected version {expected_version}, current {row['version']}")
                conn.execute(
                    "UPDATE campaign_states SET lifecycle_state=?, payload_json=?, version=?, updated_at_utc=? WHERE campaign_id=?",
                    (new_state["lifecycle_state"], canonical_json_text(new_state), new_state["version"], timestamp, campaign_id),
                )
        return new_state
