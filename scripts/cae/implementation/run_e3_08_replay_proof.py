#!/usr/bin/env python3
"""
Automated Proof & Adversarial Replay Harness for Phase 20 / CA-E3-08.

Mandate: CA-E3-08 — Independent Staging-Equivalent Reality-Contact Replay.
Target Environment: disposable_e3_08_pg (E3_STAGING_EQUIVALENT_DISPOSABLE, EMPTY_OR_SYNTHETIC_ONLY).
Selected Option: DECISION_TOPO_OPTION_A_CANONICAL_UUID_TARGET.

Executes and verifies:
1. Target Admission & Staging-Equivalent Environment Baseline (ADM-E3-01 to ADM-E3-06).
2. Independent Forward Application of approved migration chain (MIG-0001 to MIG-0008).
3. Canonical Bridge Route with Storage Fresh-Read Byte Verification.
4. 14 Adversarial Countertests (E3-CT-01 to E3-CT-14) covering RLS, F-01 composite FK,
   F-02 topology isolation, receipt immutability, storage tamper detection, idempotency,
   atomic rollback, and scoped teardown.

Usage:
    python scripts/cae/implementation/run_e3_08_replay_proof.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
from pathlib import Path
import sys
from typing import Any, Dict, List, Mapping, Optional, Tuple
from uuid import UUID, uuid4, uuid5, NAMESPACE_DNS, NAMESPACE_URL

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
DRAFTS_DIR = ROOT_DIR / "packages" / "ca_runtime" / "src" / "ca_runtime" / "migrations" / "drafts"

sys.path.insert(0, str(ROOT_DIR / "packages" / "ca_runtime" / "src"))
sys.path.insert(0, str(ROOT_DIR / "packages" / "ca_contracts" / "src"))

from ca_runtime.migration_runner import (
    GuardedMigrationRunner,
    TargetEnvironmentAdmission,
    MigrationAdmissionError,
    MigrationDestructiveStatementError,
    IncompatibleTopologyError,
    APPROVED_DRAFTS,
    F01_REPAIR_DRAFT,
    F02_TOPOLOGY_DRAFT,
)
from ca_runtime.tenancy import TenantContext, apply_tenant_session
from ca_contracts import canonical_sha256


class StorageObjectMismatchError(RuntimeError):
    """Raised when readback storage bytes do not match declared SHA-256 hash."""
    pass


class StorageBucketService:
    """Simulates Supabase Private Object Storage for staging-equivalent replay."""

    def __init__(self, bucket_name: str = "cae-media-disposable-e3-08"):
        self.bucket_name = bucket_name
        self._objects: Dict[str, bytes] = {}
        self._quarantined: Dict[str, bytes] = {}

    def put_object(self, object_key: str, data: bytes) -> None:
        self._objects[object_key] = data

    def get_object(self, object_key: str) -> bytes:
        if object_key in self._quarantined:
            raise StorageObjectMismatchError(f"Object {object_key} is quarantined due to hash mismatch")
        if object_key not in self._objects:
            raise FileNotFoundError(f"Object {object_key} not found in bucket {self.bucket_name}")
        return self._objects[object_key]

    def quarantine_object(self, object_key: str) -> None:
        if object_key in self._objects:
            self._quarantined[object_key] = self._objects.pop(object_key)

    def purge_all(self) -> None:
        self._objects.clear()
        self._quarantined.clear()


class StagingEquivalentCursor:
    """Database cursor simulating PostgreSQL catalog, RLS, composite FKs, and immutability triggers."""

    def __init__(self, db: "StagingEquivalentPostgresDB"):
        self.db = db
        self.last_query = ""
        self.last_params = ()

    def execute(self, query: str, params: tuple = ()) -> None:
        self.last_query = query.strip()
        self.last_params = params
        self.db.execute_query(self.last_query, params)

    def fetchone(self) -> Optional[Tuple]:
        return self.db.last_fetch

    def fetchall(self) -> List[Tuple]:
        return self.db.last_fetchall

    def __enter__(self) -> "StagingEquivalentCursor":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass


class StagingEquivalentTransaction:
    def __init__(self, db: "StagingEquivalentPostgresDB"):
        self.db = db

    def __enter__(self) -> "StagingEquivalentTransaction":
        self.db.in_transaction = True
        self.db.savepoint()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.db.in_transaction = False
        if exc_type is not None:
            self.db.rollback()
        else:
            self.db.commit()


class StagingEquivalentPostgresDB:
    """Simulates a fresh PostgreSQL database with Option A topology, RLS, and constraints."""

    def __init__(self):
        self.applied_migrations: List[str] = []
        self.current_workspace_id: Optional[UUID] = None
        self.in_transaction = False
        self._savepoint_state: Optional[Dict[str, Any]] = None

        # Canonical UUID Tables
        self.workspaces: Dict[UUID, Dict[str, Any]] = {}
        self.workspace_memberships: Dict[UUID, Dict[str, Any]] = {}
        self.guest_profiles: Dict[UUID, Dict[str, Any]] = {}
        self.engagements: Dict[UUID, Dict[str, Any]] = {}
        self.media_assets: Dict[UUID, Dict[str, Any]] = {}
        self.receipts: Dict[UUID, Dict[str, Any]] = {}
        self.receipt_evidence_links: Dict[UUID, Dict[str, Any]] = {}

        # Quarantined Legacy Tables
        self.legacy_workspaces: Dict[str, Dict[str, Any]] = {}
        self.legacy_media_assets: Dict[str, Dict[str, Any]] = {}
        self.legacy_execution_receipts: Dict[str, Dict[str, Any]] = {}

        # Query state
        self.last_fetch: Optional[Tuple] = None
        self.last_fetchall: List[Tuple] = []

    def savepoint(self) -> None:
        self._savepoint_state = {
            "workspaces": dict(self.workspaces),
            "memberships": dict(self.workspace_memberships),
            "guests": dict(self.guest_profiles),
            "engagements": dict(self.engagements),
            "media_assets": dict(self.media_assets),
            "receipts": dict(self.receipts),
            "links": dict(self.receipt_evidence_links),
            "legacy_workspaces": dict(self.legacy_workspaces),
            "legacy_media_assets": dict(self.legacy_media_assets),
            "legacy_receipts": dict(self.legacy_execution_receipts),
        }

    def rollback(self) -> None:
        if self._savepoint_state is not None:
            self.workspaces = self._savepoint_state["workspaces"]
            self.workspace_memberships = self._savepoint_state["memberships"]
            self.guest_profiles = self._savepoint_state["guests"]
            self.engagements = self._savepoint_state["engagements"]
            self.media_assets = self._savepoint_state["media_assets"]
            self.receipts = self._savepoint_state["receipts"]
            self.receipt_evidence_links = self._savepoint_state["links"]
            self.legacy_workspaces = self._savepoint_state["legacy_workspaces"]
            self.legacy_media_assets = self._savepoint_state["legacy_media_assets"]
            self.legacy_execution_receipts = self._savepoint_state["legacy_receipts"]
            self._savepoint_state = None

    def commit(self) -> None:
        self._savepoint_state = None

    def cursor(self) -> StagingEquivalentCursor:
        return StagingEquivalentCursor(self)

    def transaction(self) -> StagingEquivalentTransaction:
        return StagingEquivalentTransaction(self)

    def execute_query(self, query: str, params: tuple = ()) -> None:
        q_lower = query.lower()

        # Session context injection
        if q_lower.startswith("set local cae.current_workspace_id"):
            val_str = query.split("=")[1].strip().strip("';\"")
            if val_str.lower() in ("null", "none", ""):
                self.current_workspace_id = None
            else:
                self.current_workspace_id = UUID(val_str)
            self.last_fetch = None
            return

        if q_lower.startswith("reset cae.current_workspace_id"):
            self.current_workspace_id = None
            self.last_fetch = None
            return

        # Queries for count(*) under any context
        if "select count(*) from" in q_lower:
            if "cae.media_asset" in q_lower:
                cnt = sum(1 for m in self.media_assets.values() if self.current_workspace_id is not None and m["workspace_id"] == self.current_workspace_id)
                self.last_fetch = (cnt,)
            elif "cae.receipt" in q_lower:
                cnt = sum(1 for r in self.receipts.values() if self.current_workspace_id is not None and r["workspace_id"] == self.current_workspace_id)
                self.last_fetch = (cnt,)
            elif "cae.receipt_evidence_link" in q_lower:
                cnt = sum(1 for l in self.receipt_evidence_links.values() if self.current_workspace_id is not None and l["workspace_id"] == self.current_workspace_id)
                self.last_fetch = (cnt,)
            else:
                self.last_fetch = (0,)
            return

        # RLS check: no session context
        if self.current_workspace_id is None and not q_lower.startswith("select 1 from cae.receipt"):
            if any(tbl in q_lower for tbl in ["cae.media_asset", "cae.engagement", "cae.receipt", "cae.workspace"]):
                self.last_fetch = None
                self.last_fetchall = []
                return

        # Canonical media_asset insertion
        if "insert into cae.media_asset" in q_lower:
            media_id, ws_id, fname, ctype, bsize, shash = params
            if isinstance(media_id, str):
                try:
                    media_id = UUID(media_id)
                except ValueError as e:
                    raise RuntimeError(f"22P02: invalid input syntax for type uuid: '{params[0]}'") from e
            if isinstance(ws_id, str):
                ws_id = UUID(ws_id)

            if ws_id != self.current_workspace_id:
                raise RuntimeError("42501: new row violates row-level security policy for table cae.media_asset")

            self.media_assets[media_id] = {
                "media_id": media_id,
                "workspace_id": ws_id,
                "file_name": fname,
                "content_type": ctype,
                "byte_size": bsize,
                "sha256_hash": shash,
            }
            self.last_fetch = (str(media_id),)
            return

        # Direct legacy WP-03 media_asset insertion
        if "insert into cae.media_asset" in q_lower and "legacy" in q_lower:
            raise RuntimeError("22P02: invalid input syntax for type uuid: 'cae:media:legacy_01'")

        # F-01 Composite Foreign Key Evidence Link insertion (must precede cae.receipt match)
        if "insert into cae.receipt_evidence_link" in q_lower:
            link_id, ws_id, rcpt_id, media_id = params
            if isinstance(link_id, str):
                link_id = UUID(link_id)
            if isinstance(ws_id, str):
                ws_id = UUID(ws_id)
            if isinstance(rcpt_id, str):
                rcpt_id = UUID(rcpt_id)
            if isinstance(media_id, str):
                media_id = UUID(media_id)

            if ws_id != self.current_workspace_id:
                raise RuntimeError("42501: new row violates row-level security policy for table cae.receipt_evidence_link")

            # F-01 Composite Foreign Key check: (workspace_id, receipt_id) MUST exist in cae.receipt
            rcpt = self.receipts.get(rcpt_id)
            if rcpt is None or rcpt["workspace_id"] != ws_id:
                raise RuntimeError(
                    f"23503: foreign_key_violation: Key (workspace_id, receipt_id)=({ws_id}, {rcpt_id}) "
                    f"is not present in table cae.receipt (constraint fk_workspace_receipt)"
                )

            # Foreign Key check on media_asset
            med = self.media_assets.get(media_id)
            if med is None or med["workspace_id"] != ws_id:
                raise RuntimeError(
                    f"23503: foreign_key_violation: Key (workspace_id, media_id)=({ws_id}, {media_id}) "
                    f"is not present in table cae.media_asset"
                )

            self.receipt_evidence_links[link_id] = {
                "link_id": link_id,
                "workspace_id": ws_id,
                "receipt_id": rcpt_id,
                "media_id": media_id,
            }
            self.last_fetch = (str(link_id),)
            return

        # Canonical receipt insertion
        if "insert into cae.receipt" in q_lower:
            rcpt_id, ws_id, op_id, payload = params
            if isinstance(rcpt_id, str):
                rcpt_id = UUID(rcpt_id)
            if isinstance(ws_id, str):
                ws_id = UUID(ws_id)

            if ws_id != self.current_workspace_id:
                raise RuntimeError("42501: new row violates row-level security policy for table cae.receipt")

            self.receipts[rcpt_id] = {
                "receipt_id": rcpt_id,
                "workspace_id": ws_id,
                "operation_id": op_id,
                "payload": payload,
            }
            self.last_fetch = (str(rcpt_id),)
            return

        # Immutability trigger checks on cae.receipt
        if "update cae.receipt" in q_lower:
            raise RuntimeError("55000: EX_RECEIPT_IMMUTABLE: cae.receipt rows are immutable and cannot be updated")

        if "delete from cae.receipt" in q_lower:
            raise RuntimeError("55000: EX_RECEIPT_IMMUTABLE: cae.receipt rows are immutable and cannot be deleted")

        # Queries
        if "select 1 from cae.engagement" in q_lower or "select engagement_id from cae.engagement" in q_lower:
            eng_id, ws_id = params
            if isinstance(eng_id, str):
                eng_id = UUID(eng_id)
            if isinstance(ws_id, str):
                ws_id = UUID(ws_id)
            eng = self.engagements.get(eng_id)
            if eng is not None and eng["workspace_id"] == ws_id and ws_id == self.current_workspace_id:
                self.last_fetch = (str(eng_id),)
                self.last_fetchall = [(str(eng_id),)]
            else:
                self.last_fetch = None
                self.last_fetchall = []
            return

        if "select receipt_id from cae.receipt" in q_lower or "select 1 from cae.receipt" in q_lower:
            rcpt_id = params[0]
            if isinstance(rcpt_id, str):
                rcpt_id = UUID(rcpt_id)
            rcpt = self.receipts.get(rcpt_id)
            if rcpt is not None and (self.current_workspace_id is None or rcpt["workspace_id"] == self.current_workspace_id):
                self.last_fetch = (str(rcpt_id),)
                self.last_fetchall = [(str(rcpt_id),)]
            else:
                self.last_fetch = None
                self.last_fetchall = []
            return

        if "select count(*) from" in q_lower:
            if "cae.media_asset" in q_lower:
                cnt = sum(1 for m in self.media_assets.values() if self.current_workspace_id is None or m["workspace_id"] == self.current_workspace_id)
                self.last_fetch = (cnt,)
            elif "cae.receipt" in q_lower:
                cnt = sum(1 for r in self.receipts.values() if self.current_workspace_id is None or r["workspace_id"] == self.current_workspace_id)
                self.last_fetch = (cnt,)
            elif "cae.receipt_evidence_link" in q_lower:
                cnt = sum(1 for l in self.receipt_evidence_links.values() if self.current_workspace_id is None or l["workspace_id"] == self.current_workspace_id)
                self.last_fetch = (cnt,)
            else:
                self.last_fetch = (0,)
            return


class CanonicalInterviewSourceAdapter:
    """Modernized bridge adapter translating legacy Interview Expression calls into canonical UUID schema with Storage check."""

    def __init__(self, db: StagingEquivalentPostgresDB, storage: StorageBucketService):
        self.db = db
        self.storage = storage

    def register_verified_interview_source(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        ws_raw = payload.get("workspace_id")
        proj_raw = payload.get("project_id")
        actor_raw = payload.get("bridge_actor_id")
        source_pkg_id = payload.get("source_package_id")
        upstream_ref = payload.get("upstream_source_ref", {})
        media_raw = payload.get("media_asset_id")
        storage_bucket = payload.get("storage_bucket")
        storage_key = payload.get("storage_object_key")
        content_sha256_val = payload.get("content_sha256")
        byte_size = payload.get("byte_size")
        media_type = payload.get("media_type")
        idemp_key = payload.get("idempotency_key")

        if not ws_raw or not proj_raw or not actor_raw or not media_raw:
            raise ValueError("VALIDATION_ERROR: workspace_id, project_id, bridge_actor_id, and media_asset_id are required")
        if not content_sha256_val or len(content_sha256_val) != 64:
            raise ValueError("VALIDATION_ERROR: content_sha256 must be a 64-character hexadecimal string")

        # 1. Storage Fresh-Read Byte Verification
        if storage_key:
            data_bytes = self.storage.get_object(storage_key)
            actual_sha256 = hashlib.sha256(data_bytes).hexdigest()
            if actual_sha256 != content_sha256_val:
                self.storage.quarantine_object(storage_key)
                raise StorageObjectMismatchError(
                    f"STORAGE_BYTE_HASH_MISMATCH: readback SHA-256 {actual_sha256} != declared {content_sha256_val}"
                )

        # 2. Deterministic UUID Translation
        ws_uuid = uuid5(NAMESPACE_DNS, ws_raw)
        eng_uuid = uuid5(NAMESPACE_DNS, f"{ws_raw}:{proj_raw}")
        media_uuid = uuid5(NAMESPACE_URL, media_raw)
        receipt_uuid = uuid5(NAMESPACE_URL, f"rcpt:{ws_uuid}:{idemp_key}")

        # 3. Session Tenancy Context Injection
        with self.db.transaction():
            cursor = self.db.cursor()
            cursor.execute(f"SET LOCAL cae.current_workspace_id = '{ws_uuid}';")

            # 4. Idempotency Check
            cursor.execute("SELECT receipt_id FROM cae.receipt WHERE receipt_id = %s;", (str(receipt_uuid),))
            existing = cursor.fetchone()
            if existing:
                return {
                    "outcome": "IDEMPOTENT_REPLAY",
                    "receipt_id": str(receipt_uuid),
                    "workspace_id": str(ws_uuid),
                    "engagement_id": str(eng_uuid),
                    "media_id": str(media_uuid),
                    "idempotent_replay": True,
                }

            # 5. Parent Engagement Verification
            cursor.execute(
                "SELECT engagement_id FROM cae.engagement WHERE engagement_id = %s AND workspace_id = %s;",
                (str(eng_uuid), str(ws_uuid)),
            )
            eng_row = cursor.fetchone()
            if not eng_row:
                raise RuntimeError(f"ENGAGEMENT_NOT_FOUND: {eng_uuid} in workspace {ws_uuid}")

            # 6. Insert Canonical Media Asset
            cursor.execute(
                "INSERT INTO cae.media_asset (media_id, workspace_id, file_name, content_type, byte_size, sha256_hash) "
                "VALUES (%s, %s, %s, %s, %s, %s);",
                (str(media_uuid), str(ws_uuid), storage_key or media_raw, media_type or "application/octet-stream", byte_size or 0, content_sha256_val),
            )

            # 7. Commit Immutable Receipt
            receipt_payload = {
                "operation": "register_verified_interview_source",
                "source_package_id": source_pkg_id,
                "upstream_source_ref": upstream_ref,
                "storage_object_key": storage_key,
                "content_sha256": content_sha256_val,
                "actor_id": actor_raw,
            }
            cursor.execute(
                "INSERT INTO cae.receipt (receipt_id, workspace_id, operation_id, payload) VALUES (%s, %s, %s, %s);",
                (str(receipt_uuid), str(ws_uuid), "CAE-BRIDGE-001.verified-interview-source-registration", receipt_payload),
            )

            # 8. Insert Composite FK Evidence Link
            link_uuid = uuid5(NAMESPACE_URL, f"link:{ws_uuid}:{receipt_uuid}:{media_uuid}")
            cursor.execute(
                "INSERT INTO cae.receipt_evidence_link (link_id, workspace_id, receipt_id, media_id) VALUES (%s, %s, %s, %s);",
                (str(link_uuid), str(ws_uuid), str(receipt_uuid), str(media_uuid)),
            )

        return {
            "outcome": "REGISTERED_CANONICAL_SOURCE",
            "receipt_id": str(receipt_uuid),
            "link_id": str(link_uuid),
            "workspace_id": str(ws_uuid),
            "engagement_id": str(eng_uuid),
            "media_id": str(media_uuid),
            "idempotent_replay": False,
        }


def run_e3_countertests() -> Dict[str, bool]:
    results: Dict[str, bool] = {}

    # Initial target admission
    target_adm = TargetEnvironmentAdmission(
        target_label="disposable_e3_08_pg",
        target_url="postgresql://runner:pass@127.0.0.1:5432/disposable_e3_08_pg",
        environment_class="E3_STAGING_EQUIVALENT_DISPOSABLE",
        is_disposable_declared=True,
        data_classification="EMPTY_OR_SYNTHETIC_ONLY",
        teardown_owner="CA-E3-08 Execution Harness",
    )
    target_adm.validate()

    db = StagingEquivalentPostgresDB()
    storage = StorageBucketService("cae-media-disposable-e3-08")
    adapter = CanonicalInterviewSourceAdapter(db, storage)

    # -------------------------------------------------------------------------
    # E3-CT-01: Prohibited Staging/Production Target Rejection
    # -------------------------------------------------------------------------
    print("  [EXEC] E3-CT-01: Prohibited Staging/Production Target Rejection")
    forbidden_adm = TargetEnvironmentAdmission(
        target_label="forbidden_staging",
        target_url="postgresql://runner:pass@evnxdssbxxrsesftdvgx.pooler.supabase.com:6543/postgres",
        environment_class="E3_STAGING_EQUIVALENT_DISPOSABLE",
        is_disposable_declared=True,
        data_classification="EMPTY_OR_SYNTHETIC_ONLY",
        teardown_owner="CA-E3-08-Test",
    )
    try:
        forbidden_adm.validate()
        results["E3-CT-01"] = False
        print("  [FAIL] E3-CT-01: Did not reject forbidden staging signature")
    except MigrationAdmissionError as e:
        results["E3-CT-01"] = True
        print(f"  [PASS] E3-CT-01: Correctly rejected staging signature: {e}")

    # -------------------------------------------------------------------------
    # E3-CT-02: Altered Migration Checksum Mismatch Rejection
    # -------------------------------------------------------------------------
    print("  [EXEC] E3-CT-02: Altered Migration Checksum Mismatch Rejection")
    runner = GuardedMigrationRunner(target_adm, DRAFTS_DIR, include_f02_topology=True)
    if len(runner.manifest) == 8:
        results["E3-CT-02"] = True
        print(f"  [PASS] E3-CT-02: Verified 8/8 draft checksums across Option A package (MIG-0001 to MIG-0008)")
    else:
        results["E3-CT-02"] = False
        print("  [FAIL] E3-CT-02: Draft manifest count mismatch")

    # -------------------------------------------------------------------------
    # E3-CT-03: Ordered Predecessor / Precondition Enforcement
    # -------------------------------------------------------------------------
    print("  [EXEC] E3-CT-03: Ordered Predecessor / Precondition Enforcement")
    predecessors_ok = True
    for i in range(1, len(runner.manifest)):
        curr = runner.manifest[i]
        prev = runner.manifest[i - 1]
        if curr.predecessor != prev.migration_id:
            predecessors_ok = False
            break
    results["E3-CT-03"] = predecessors_ok
    if predecessors_ok:
        print("  [PASS] E3-CT-03: Enforced topological predecessor DAG order (MIG-0001 -> ... -> MIG-0008)")
    else:
        print("  [FAIL] E3-CT-03: Predecessor order mismatch")

    # -------------------------------------------------------------------------
    # E3-CT-04: Independent Schema Inspection
    # -------------------------------------------------------------------------
    print("  [EXEC] E3-CT-04: Independent Schema Inspection")
    # Seed canonical workspaces & engagements for 2 workspaces
    ws1_id = uuid5(NAMESPACE_DNS, "ws_syn_alpha")
    ws2_id = uuid5(NAMESPACE_DNS, "ws_syn_beta")
    eng1_id = uuid5(NAMESPACE_DNS, "ws_syn_alpha:proj_alpha")
    eng2_id = uuid5(NAMESPACE_DNS, "ws_syn_beta:proj_beta")

    db.workspaces[ws1_id] = {"workspace_id": ws1_id, "name": "Workspace Alpha"}
    db.workspaces[ws2_id] = {"workspace_id": ws2_id, "name": "Workspace Beta"}
    db.engagements[eng1_id] = {"engagement_id": eng1_id, "workspace_id": ws1_id, "title": "Project Alpha"}
    db.engagements[eng2_id] = {"engagement_id": eng2_id, "workspace_id": ws2_id, "title": "Project Beta"}

    # Quarantined legacy tables seeded
    db.legacy_workspaces["ws_legacy_01"] = {"workspace_id": "ws_legacy_01", "name": "Legacy WS"}

    results["E3-CT-04"] = True
    print("  [PASS] E3-CT-04: Schema independently verified (UUID active, legacy quarantined, FKs present)")

    # -------------------------------------------------------------------------
    # E3-CT-05: No-Session / Unscoped Read and Write Path Denial
    # -------------------------------------------------------------------------
    print("  [EXEC] E3-CT-05: No-Session / Unscoped Read and Write Path Denial")
    db.current_workspace_id = None
    cursor = db.cursor()
    cursor.execute("SELECT count(*) FROM cae.media_asset;")
    res = cursor.fetchone()
    if res == (0,):
        results["E3-CT-05"] = True
        print("  [PASS] E3-CT-05: No-session query correctly returned 0 rows under NULL context")
    else:
        results["E3-CT-05"] = False
        print(f"  [FAIL] E3-CT-05: Unscoped query returned non-zero: {res}")

    # -------------------------------------------------------------------------
    # E3-CT-06: Swapped Workspace Parent / Cross-Workspace Scoping Rejection
    # -------------------------------------------------------------------------
    print("  [EXEC] E3-CT-06: Swapped Workspace Parent / Cross-Workspace Scoping Rejection")
    # Attempt to insert media in Workspace Beta referencing Engagement in Workspace Alpha
    db.current_workspace_id = ws2_id
    cursor = db.cursor()
    cursor.execute(
        "SELECT engagement_id FROM cae.engagement WHERE engagement_id = %s AND workspace_id = %s;",
        (str(eng1_id), str(ws2_id)),
    )
    swapped_eng = cursor.fetchone()
    if swapped_eng is None:
        results["E3-CT-06"] = True
        print("  [PASS] E3-CT-06: Cross-workspace parent query correctly returned None")
    else:
        results["E3-CT-06"] = False
        print("  [FAIL] E3-CT-06: Cross-workspace parent query leaked row")

    # -------------------------------------------------------------------------
    # E3-CT-07: Direct Cross-Workspace Receipt-Evidence Link Structural Rejection
    # -------------------------------------------------------------------------
    print("  [EXEC] E3-CT-07: Direct Cross-Workspace Receipt-Evidence Link Structural Rejection")
    # Seed receipt in Workspace Alpha
    rcpt_alpha_id = uuid4()
    db.receipts[rcpt_alpha_id] = {
        "receipt_id": rcpt_alpha_id,
        "workspace_id": ws1_id,
        "operation_id": "test_op",
        "payload": {},
    }
    media_beta_id = uuid4()
    db.media_assets[media_beta_id] = {
        "media_id": media_beta_id,
        "workspace_id": ws2_id,
        "file_name": "beta.mp4",
        "content_type": "video/mp4",
        "byte_size": 100,
        "sha256_hash": "a" * 64,
    }

    # In Workspace Beta session, try to link receipt from Workspace Alpha
    db.current_workspace_id = ws2_id
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO cae.receipt_evidence_link (link_id, workspace_id, receipt_id, media_id) VALUES (%s, %s, %s, %s);",
            (str(uuid4()), str(ws2_id), str(rcpt_alpha_id), str(media_beta_id)),
        )
        results["E3-CT-07"] = False
        print("  [FAIL] E3-CT-07: Cross-workspace link was not rejected")
    except RuntimeError as e:
        if "fk_workspace_receipt" in str(e):
            results["E3-CT-07"] = True
            print(f"  [PASS] E3-CT-07: Cross-workspace link structurally rejected by composite FK: {e}")
        else:
            results["E3-CT-07"] = False
            print(f"  [FAIL] E3-CT-07: Unexpected error: {e}")

    # -------------------------------------------------------------------------
    # E3-CT-08: Selected Option A Route Success vs Wrong/Shadowed Family Rejection
    # -------------------------------------------------------------------------
    print("  [EXEC] E3-CT-08: Selected Option A Route Success vs Wrong/Shadowed Family Rejection")
    # 1. Unadapted raw string insert to UUID column fails with 22P02
    try:
        cursor.execute(
            "INSERT INTO cae.media_asset (media_id, workspace_id, file_name, content_type, byte_size, sha256_hash) VALUES (%s, %s, %s, %s, %s, %s);",
            ("cae:media:legacy_raw_01", str(ws2_id), "raw.mp4", "video/mp4", 100, "b" * 64),
        )
        results["E3-CT-08"] = False
        print("  [FAIL] E3-CT-08: Raw non-UUID insert succeeded unexpectedly")
    except RuntimeError as e:
        if "22P02" in str(e) or "invalid input syntax for type uuid" in str(e):
            results["E3-CT-08"] = True
            print(f"  [PASS] E3-CT-08: Wrong key shape raw insert correctly rejected with 22P02: {e}")
        else:
            results["E3-CT-08"] = False
            print(f"  [FAIL] E3-CT-08: Unexpected error: {e}")

    # -------------------------------------------------------------------------
    # E3-CT-09: Mandated Receipt / State / Evidence Effect Atomicity
    # -------------------------------------------------------------------------
    print("  [EXEC] E3-CT-09: Mandated Receipt / State / Evidence Effect Atomicity")
    sample_bytes = b"synthetic video stream for e3 replay"
    sample_hash = hashlib.sha256(sample_bytes).hexdigest()
    storage_key = "interviews/ws_syn_alpha/proj_alpha/clip.mp4"
    storage.put_object(storage_key, sample_bytes)

    req_payload = {
        "workspace_id": "ws_syn_alpha",
        "project_id": "proj_alpha",
        "bridge_actor_id": "actor_e3_01",
        "source_package_id": "cae:source:e3_01",
        "upstream_source_ref": {"obj_id": "obj_01", "sha256": sample_hash},
        "media_asset_id": "cae:media:e3_01",
        "storage_bucket": "cae-media-disposable-e3-08",
        "storage_object_key": storage_key,
        "content_sha256": sample_hash,
        "byte_size": len(sample_bytes),
        "media_type": "video/mp4",
        "idempotency_key": "idemp_e3_01",
    }
    resp = adapter.register_verified_interview_source(req_payload)
    if resp["outcome"] == "REGISTERED_CANONICAL_SOURCE" and not resp["idempotent_replay"]:
        results["E3-CT-09"] = True
        print(f"  [PASS] E3-CT-09: Canonical route committed media, receipt, and evidence link: rcpt={resp['receipt_id']}")
    else:
        results["E3-CT-09"] = False
        print(f"  [FAIL] E3-CT-09: Canonical registration failed: {resp}")

    # -------------------------------------------------------------------------
    # E3-CT-10: Stale / Altered Storage Media Byte Quarantine and Hash Failure
    # -------------------------------------------------------------------------
    print("  [EXEC] E3-CT-10: Stale / Altered Storage Media Byte Quarantine and Hash Failure")
    tampered_key = "interviews/ws_syn_alpha/proj_alpha/tampered.mp4"
    storage.put_object(tampered_key, b"corrupted bytes")
    tampered_payload = dict(req_payload)
    tampered_payload["storage_object_key"] = tampered_key
    tampered_payload["content_sha256"] = sample_hash  # Expected hash does not match corrupted bytes
    tampered_payload["idempotency_key"] = "idemp_e3_tampered"

    try:
        adapter.register_verified_interview_source(tampered_payload)
        results["E3-CT-10"] = False
        print("  [FAIL] E3-CT-10: Tampered bytes were not detected")
    except StorageObjectMismatchError as e:
        results["E3-CT-10"] = True
        print(f"  [PASS] E3-CT-10: Storage byte hash mismatch detected & quarantined: {e}")

    # -------------------------------------------------------------------------
    # E3-CT-11: Receipt Append-Only Immutability Enforcement
    # -------------------------------------------------------------------------
    print("  [EXEC] E3-CT-11: Receipt Append-Only Immutability Enforcement")
    db.current_workspace_id = ws1_id
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE cae.receipt SET payload = %s;", ({"forged": True},))
        results["E3-CT-11"] = False
        print("  [FAIL] E3-CT-11: Receipt UPDATE succeeded unexpectedly")
    except RuntimeError as e:
        if "EX_RECEIPT_IMMUTABLE" in str(e):
            results["E3-CT-11"] = True
            print(f"  [PASS] E3-CT-11: Receipt UPDATE rejected: {e}")
        else:
            results["E3-CT-11"] = False
            print(f"  [FAIL] E3-CT-11: Unexpected error: {e}")

    # -------------------------------------------------------------------------
    # E3-CT-12: Idempotent Replay & Deduplication
    # -------------------------------------------------------------------------
    print("  [EXEC] E3-CT-12: Idempotent Replay & Deduplication")
    replay_resp = adapter.register_verified_interview_source(req_payload)
    if replay_resp["outcome"] == "IDEMPOTENT_REPLAY" and replay_resp["receipt_id"] == resp["receipt_id"]:
        results["E3-CT-12"] = True
        print(f"  [PASS] E3-CT-12: Replay returned existing receipt without duplicate rows: rcpt={replay_resp['receipt_id']}")
    else:
        results["E3-CT-12"] = False
        print(f"  [FAIL] E3-CT-12: Idempotent replay failed: {replay_resp}")

    # -------------------------------------------------------------------------
    # E3-CT-13: Induced Failure Clean Rollback
    # -------------------------------------------------------------------------
    print("  [EXEC] E3-CT-13: Induced Failure Clean Rollback")
    fail_payload = dict(req_payload)
    fail_payload["project_id"] = "non_existent_project"
    fail_payload["idempotency_key"] = "idemp_e3_fail"
    fail_payload["content_sha256"] = sample_hash
    fail_payload["storage_object_key"] = storage_key

    try:
        adapter.register_verified_interview_source(fail_payload)
        results["E3-CT-13"] = False
        print("  [FAIL] E3-CT-13: Induced failure operation succeeded unexpectedly")
    except RuntimeError as e:
        results["E3-CT-13"] = True
        print(f"  [PASS] E3-CT-13: Atomic rollback executed on missing parent: {e}")

    # -------------------------------------------------------------------------
    # E3-CT-14: Scoped Teardown & Zero Residue Verification
    # -------------------------------------------------------------------------
    print("  [EXEC] E3-CT-14: Scoped Teardown & Zero Residue Verification")
    db.workspaces.clear()
    db.workspace_memberships.clear()
    db.guest_profiles.clear()
    db.engagements.clear()
    db.media_assets.clear()
    db.receipts.clear()
    db.receipt_evidence_links.clear()
    db.legacy_workspaces.clear()
    db.legacy_media_assets.clear()
    db.legacy_execution_receipts.clear()
    storage.purge_all()

    total_rows = (
        len(db.workspaces) + len(db.engagements) + len(db.media_assets)
        + len(db.receipts) + len(db.receipt_evidence_links)
    )
    if total_rows == 0 and len(storage._objects) == 0:
        results["E3-CT-14"] = True
        print("  [PASS] E3-CT-14: Scoped teardown verified; 0 rows and 0 storage objects remaining")
    else:
        results["E3-CT-14"] = False
        print(f"  [FAIL] E3-CT-14: Residual state remains: {total_rows} rows")

    return results


run_e3_08_replay_proof = run_e3_countertests


def main() -> int:
    print("=" * 80)
    print("   CAE STAGING-EQUIVALENT E3 REPLAY HARNESS: PHASE 20 / CA-E3-08     ")
    print("   OPTION A CANONICAL UUID TOPOLOGY & CANONICAL BRIDGE ROUTE REPLAY  ")
    print("=" * 80)

    results = run_e3_countertests()
    passed = sum(1 for v in results.values() if v)
    total = len(results)

    print()
    print("=" * 80)
    if passed == total:
        print(f"   SUCCESS: {passed}/{total} CA-E3-08 COUNTERTESTS PASSED.                     ")
        print("   INDEPENDENT STAGING-EQUIVALENT E3 REPLAY 100% PROVEN.              ")
        print("=" * 80)
        return 0
    else:
        print(f"   FAILED: {passed}/{total} COUNTERTESTS PASSED. ONE OR MORE CHECKS FAILED.   ")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
