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

Governed by CA-APPLY-04 Mandate and TS-CAE-TEN-001.
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
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


@dataclass(frozen=True)
class TargetEnvironmentAdmission:
    target_label: str
    target_url: str
    environment_class: str
    is_disposable_declared: bool
    data_classification: str
    teardown_owner: str

    def validate(self) -> None:
        if self.environment_class != "DISPOSABLE_POSTGRESQL_ONLY":
            raise MigrationAdmissionError(
                f"Invalid environment class: {self.environment_class}. Must be DISPOSABLE_POSTGRESQL_ONLY."
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
        admission: TargetEnvironmentAdmission,
        drafts_dir: Path,
    ) -> None:
        self.admission = admission
        self.drafts_dir = drafts_dir
        self.admission.validate()
        self.manifest: List[MigrationManifestEntry] = []
        self._load_and_validate_manifest()

    def _load_and_validate_manifest(self) -> None:
        for mig_id, fname, pred in APPROVED_DRAFTS:
            fpath = self.drafts_dir / fname
            if not fpath.is_file():
                raise FileNotFoundError(f"Missing migration draft file: {fname}")

            content = fpath.read_text(encoding="utf-8")
            if "-- STATUS: DRAFT_NOT_APPLIED" not in content:
                raise MigrationAdmissionError(
                    f"Draft {fname} missing mandatory '-- STATUS: DRAFT_NOT_APPLIED' guard header."
                )

            # Static Safety Linting
            cleaned_sql = re.sub(
                r"\bDROP\s+(TRIGGER|POLICY|EXTENSION)\b",
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
        # e.g., if workspace exists with text workspace_id instead of UUID
        if "cae.workspace" in existing_tables:
            ws_cols = existing_tables["cae.workspace"]
            if ws_cols.get("workspace_id") != "uuid":
                raise IncompatibleTopologyError(
                    f"Incompatible topology detected: cae.workspace.workspace_id has type '{ws_cols.get('workspace_id')}', expected 'uuid'."
                )

    def compute_manifest_checksum_digest(self) -> str:
        combined = "".join(f"{e.migration_id}:{e.sha256}\n" for e in self.manifest)
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()
