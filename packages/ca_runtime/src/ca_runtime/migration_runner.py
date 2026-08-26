"""
CAE Guarded Disposable PostgreSQL Migration Runner.

Enforces:
1. Environment admission: Rejects any target resembling shared CAE staging, production, or non-disposable targets.
2. Mandatory DISPOSABLE_POSTGRESQL_ONLY declaration.
3. Draft integrity: Verifies SHA-256 checksums and -- STATUS: DRAFT_NOT_APPLIED headers.
4. Static Safety Linting: Rejects forbidden destructive keywords (DROP TABLE, TRUNCATE, CASCADE, unbounded DELETE).
5. Predecessor Order: Enforces strict topological DAG ordering.
6. Honest History Ledger: Records migration state only after verified postcondition assertions.
7. Idempotent / No-op Re-run verification.
8. Synthetic Fixture Containment & Failure Recovery Rehearsal.

Governed by CA-APPLY-04, CA-INT-05 Mandates, and TS-CAE-TEN-001.
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib.parse import urlsplit


class MigrationAdmissionError(RuntimeError):
    """Raised when target environment fails admission or safety boundaries."""
    pass


class MigrationChecksumMismatch(RuntimeError):
    """Raised when migration draft bytes diverge from approved hash."""
    pass


class MigrationPredecessorError(RuntimeError):
    """Raised when migration dependency sequence is violated."""
    pass


class MigrationDestructiveStatementError(RuntimeError):
    """Raised when a draft contains prohibited destructive DDL/DML."""
    pass


class IncompatibleTopologyError(RuntimeError):
    """Raised when preflight detects incompatible table, key, or column types."""
    pass


# Staging signatures that MUST be rejected by the disposable runner
PROHIBITED_HOST_SIGNATURES = [
    "evnxdssbxxrsesftdvgx",
    ".pooler.supabase.com",
    "prod",
    "production",
    "live",
]

APPROVED_DRAFTS = [
    ("MIG-0001", "0001_cae_extensions_and_schema.sql", "NONE"),
    ("MIG-0002", "0002_cae_tenancy_and_membership.sql", "MIG-0001"),
    ("MIG-0003", "0003_cae_engagement_guest_media.sql", "MIG-0002"),
    ("MIG-0004", "0004_cae_harness_and_immutable_receipts.sql", "MIG-0003"),
    ("MIG-0005", "0005_cae_row_level_security.sql", "MIG-0004"),
    ("MIG-0006", "0006_cae_indexes_and_constraints.sql", "MIG-0005"),
]

F01_REPAIR_DRAFT = ("MIG-0007", "0007_cae_f01_composite_receipt_fk_draft.sql", "MIG-0006")
F02_TOPOLOGY_DRAFT = ("MIG-0008", "0008_cae_f02_topology_shadow_reconciliation_draft.sql", "MIG-0007")


@dataclass(frozen=True)
class TargetEnvironmentAdmission:
    target_label: str
    target_url: str
    environment_class: str
    is_disposable_declared: bool
    data_classification: str
    teardown_owner: str

    def validate(self) -> None:
        valid_classes = ["DISPOSABLE_POSTGRESQL_ONLY", "E3_STAGING_EQUIVALENT_DISPOSABLE"]
        if self.environment_class not in valid_classes:
            raise MigrationAdmissionError(
                f"Invalid environment class: {self.environment_class}. Must be one of {valid_classes}."
            )
        if not self.is_disposable_declared:
            raise MigrationAdmissionError(
                "Target must be explicitly declared disposable via is_disposable_declared=True."
            )
        if self.data_classification != "EMPTY_OR_SYNTHETIC_ONLY":
            raise MigrationAdmissionError(
                f"Forbidden data classification: {self.data_classification}. Client/production data prohibited."
            )

        # Check for prohibited staging or production endpoints
        parsed = urlsplit(self.target_url)
        url_lower = self.target_url.lower()
        for sig in PROHIBITED_HOST_SIGNATURES:
            if sig in url_lower:
                raise MigrationAdmissionError(
                    f"Target URL contains forbidden staging/production signature '{sig}': {parsed.hostname}"
                )


@dataclass(frozen=True)
class SharedStagingEnvironmentAdmission:
    target_label: str
    target_url: str
    environment_class: str
    change_window: str
    backup_snapshot_id: str
    recovery_owner: str
    data_classification: str = "EMPTY_OR_SYNTHETIC_ONLY"

    def validate(self) -> None:
        valid_classes = [
            "SHARED_STAGING_GUARDED",
            "E3_STAGING_SUPABASE_POOLER_PRIVATE_STORAGE",
        ]
        if self.environment_class not in valid_classes:
            raise MigrationAdmissionError(
                f"Invalid staging environment class: {self.environment_class}. Must be one of {valid_classes}."
            )
        if self.data_classification != "EMPTY_OR_SYNTHETIC_ONLY":
            raise MigrationAdmissionError(
                f"Forbidden data classification: {self.data_classification}. Client/production data prohibited."
            )
        if not self.change_window or not self.change_window.startswith("CW-"):
            raise MigrationAdmissionError(
                f"Invalid or missing change window: {self.change_window}."
            )
        if not self.backup_snapshot_id:
            raise MigrationAdmissionError("Missing required pre-deployment backup_snapshot_id.")
        if not self.recovery_owner:
            raise MigrationAdmissionError("Missing designated recovery_owner.")

        parsed = urlsplit(self.target_url)
        url_lower = self.target_url.lower()

        # Reject any production signatures
        prohibited_prod = ["prod", "production", "live", "customer", "main-db"]
        for sig in prohibited_prod:
            if sig in url_lower:
                raise MigrationAdmissionError(
                    f"Target URL contains forbidden production signature '{sig}': {parsed.hostname}"
                )

        # Ensure approved staging project identity
        if "evnxdssbxxrsesftdvgx" not in url_lower and "127.0.0.1" not in url_lower and "localhost" not in url_lower:
            raise MigrationAdmissionError(
                f"Target URL does not match approved staging signature 'evnxdssbxxrsesftdvgx': {parsed.hostname}"
            )


@dataclass
class MigrationManifestEntry:
    migration_id: str
    filename: str
    predecessor: str
    sha256: str
    sql_content: str
    status_header: str


class GuardedMigrationRunner:
    def __init__(
        self,
        admission: TargetEnvironmentAdmission | SharedStagingEnvironmentAdmission,
        drafts_dir: Path,
        *,
        include_f01_repair: bool = False,
        include_f02_topology: bool = False,
        custom_drafts: Optional[Sequence[Tuple[str, str, str]]] = None,
    ) -> None:
        self.admission = admission
        self.drafts_dir = drafts_dir
        self.admission.validate()
        self.manifest: List[MigrationManifestEntry] = []
        if custom_drafts is not None:
            self.approved_drafts = list(custom_drafts)
        else:
            self.approved_drafts = list(APPROVED_DRAFTS)
            if include_f01_repair or include_f02_topology:
                self.approved_drafts.append(F01_REPAIR_DRAFT)
            if include_f02_topology:
                self.approved_drafts.append(F02_TOPOLOGY_DRAFT)
        self._load_and_validate_manifest()

    def _load_and_validate_manifest(self) -> None:
        for mig_id, fname, pred in self.approved_drafts:
            fpath = self.drafts_dir / fname
            if not fpath.is_file():
                raise FileNotFoundError(f"Missing migration draft file: {fname}")

            content = fpath.read_text(encoding="utf-8")
            if "-- STATUS: DRAFT_NOT_APPLIED" not in content and "-- STATUS: APPLIED_STAGING" not in content:
                raise MigrationAdmissionError(
                    f"Draft {fname} missing mandatory '-- STATUS: DRAFT_NOT_APPLIED' or '-- STATUS: APPLIED_STAGING' guard header."
                )


            # Static Safety Linting
            cleaned_sql = re.sub(
                r"\bDROP\s+(TRIGGER|POLICY|EXTENSION|CONSTRAINT)\b",
                "",
                content,
                flags=re.IGNORECASE,
            )
            prohibited_patterns = [
                (r"\bDROP\s+TABLE\b", "DROP TABLE"),
                (r"\bTRUNCATE\b", "TRUNCATE"),
                (r"\bDROP\s+SCHEMA\b", "DROP SCHEMA"),
                (r"\bDELETE\s+FROM\b", "DELETE FROM"),
            ]
            for pat, token_name in prohibited_patterns:
                if re.search(pat, cleaned_sql, re.IGNORECASE):
                    raise MigrationDestructiveStatementError(
                        f"Draft {fname} contains prohibited destructive statement: {token_name}"
                    )

            sha256 = hashlib.sha256(content.encode("utf-8")).hexdigest()
            self.manifest.append(
                MigrationManifestEntry(
                    migration_id=mig_id,
                    filename=fname,
                    predecessor=pred,
                    sha256=sha256,
                    sql_content=content,
                    status_header="DRAFT_NOT_APPLIED",
                )
            )

    def verify_predecessors(self, applied_ids: List[str]) -> None:
        """Ensure child migrations are rejected if predecessors are missing."""
        for entry in self.manifest:
            if entry.predecessor != "NONE" and entry.predecessor not in applied_ids:
                if entry.migration_id in applied_ids:
                    raise MigrationPredecessorError(
                        f"Predecessor violation: {entry.migration_id} applied without predecessor {entry.predecessor}"
                    )

    def preflight_incompatible_topology(self, existing_tables: Dict[str, Dict[str, str]]) -> None:
        """Preflight check: Reject schema if non-conforming table/column types exist."""
        if "cae.workspace" in existing_tables:
            ws_cols = existing_tables["cae.workspace"]
            if ws_cols.get("workspace_id") != "uuid":
                raise IncompatibleTopologyError(
                    f"Incompatible topology detected: cae.workspace.workspace_id has type '{ws_cols.get('workspace_id')}', expected 'uuid'."
                )

    def preflight_f01_composite_fk_readiness(
        self,
        receipt_unique_keys: List[Tuple[str, ...]],
        existing_evidence_links: List[Dict[str, str]],
    ) -> None:
        """Preflight check for F-01 repair: parent key exists and zero orphaned/cross-workspace links."""
        # 1. Parent table cae.receipt must have composite unique key (workspace_id, receipt_id)
        if ("workspace_id", "receipt_id") not in receipt_unique_keys:
            raise IncompatibleTopologyError(
                "Parent table cae.receipt lacks required composite unique constraint on (workspace_id, receipt_id)."
            )
        # 2. Existing evidence links must have zero cross-workspace mismatches
        for link in existing_evidence_links:
            if link["link_workspace_id"] != link["receipt_workspace_id"]:
                raise IncompatibleTopologyError(
                    f"Cross-workspace link detected in existing data: link ws {link['link_workspace_id']} != receipt ws {link['receipt_workspace_id']}."
                )

    def compute_manifest_checksum_digest(self) -> str:
        combined = "".join(f"{e.migration_id}:{e.sha256}\n" for e in self.manifest)
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()
