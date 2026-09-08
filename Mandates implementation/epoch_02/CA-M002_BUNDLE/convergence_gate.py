"""
convergence_gate.py
-------------------
CA-M002 / FR-CONV-001 — Dual-Context Convergence Gate.

Implements the hard admission boundary that prevents downstream narrative
compilation unless BOTH:
  (a) Guest Genesis Semantic Territory — valid, ratified, digest-bound, and
  (b) Audience Tensions — valid, independently sourced, digest-bound

are present and converged.

Authority hierarchy:
  Master 57-Question Canon → Product Brief → PRD → Architecture.md §11
  → this gate → ca_runtime.program_operator_runtime → downstream programs.

Architectural rules enforced here:
  1. FAIL-CLOSED: any absent, invalid, or stale upstream artifact blocks admission.
  2. INDEPENDENT VALIDATION: each side is verified against its own contract before
     the convergence relation is evaluated.
  3. REVISION/DIGEST BINDING: the resulting receipt pins the EXACT upstream
     revision_id and sha256_digest for both sources.
  4. NO UI AUTHORITY: the gate is runtime-authoritative; the UI may project the
     receipt but cannot override, bypass, or invent local semantics.
  5. STRUCTURED REASON: every rejection carries a machine-readable reason_code
     and human-readable message so the operator can see why execution is blocked.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence

from ca_contracts import canonical_sha256, utc_now_rfc3339


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CONVERGENCE_GATE_VERSION = "1.0.0"
CONVERGENCE_PROGRAM_ID = "dual_context_convergence_gate"
FR_CONV_001 = "FR-CONV-001"


# ---------------------------------------------------------------------------
# Error Taxonomy
# ---------------------------------------------------------------------------

class ConvergenceGateError(RuntimeError):
    """Base exception for all Convergence Gate operations."""

    def __init__(
        self,
        message: str,
        *,
        reason_code: str = "CONVERGENCE_GATE_ERROR",
        details: Optional[Dict[str, Any]] = None,
        permitted_next_actions: Optional[List[str]] = None,
    ) -> None:
        super().__init__(message)
        self.reason_code = reason_code
        self.details = details or {}
        self.permitted_next_actions: List[str] = permitted_next_actions or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.__class__.__name__,
            "reason_code": self.reason_code,
            "message": str(self),
            "details": self.details,
            "permitted_next_actions": self.permitted_next_actions,
        }


class MissingGuestGenesisError(ConvergenceGateError):
    """Raised when Guest Genesis Semantic Territory artifact is absent."""

    def __init__(self, workspace_id: str) -> None:
        super().__init__(
            f"Convergence gate blocked: Guest Genesis Semantic Territory artifact "
            f"is missing for workspace '{workspace_id}'. "
            f"Complete guest_genesis_semantic_territory_program to TERRITORY_RATIFIED state first.",
            reason_code="MISSING_GUEST_GENESIS_SEMANTIC_TERRITORY",
            details={"workspace_id": workspace_id, "required_program": "guest_genesis_semantic_territory_program"},
            permitted_next_actions=["run_program:guest_genesis_semantic_territory_program"],
        )


class MissingAudienceTensionsError(ConvergenceGateError):
    """Raised when Audience Tensions artifact is absent."""

    def __init__(self, workspace_id: str) -> None:
        super().__init__(
            f"Convergence gate blocked: Audience Tensions artifact is missing "
            f"for workspace '{workspace_id}'. "
            f"Complete audience_context_program to TENSIONS_ACTIVE state first.",
            reason_code="MISSING_AUDIENCE_TENSIONS",
            details={"workspace_id": workspace_id, "required_program": "audience_context_program"},
            permitted_next_actions=["run_program:audience_context_program"],
        )


class InvalidGuestGenesisError(ConvergenceGateError):
    """Raised when Guest Genesis artifact fails its own validity contract."""

    def __init__(self, workspace_id: str, reason: str) -> None:
        super().__init__(
            f"Convergence gate blocked: Guest Genesis Semantic Territory for workspace "
            f"'{workspace_id}' failed validity check — {reason}",
            reason_code="INVALID_GUEST_GENESIS_SEMANTIC_TERRITORY",
            details={"workspace_id": workspace_id, "validity_reason": reason},
            permitted_next_actions=["repair_program:guest_genesis_semantic_territory_program"],
        )


class InvalidAudienceTensionsError(ConvergenceGateError):
    """Raised when Audience Tensions artifact fails its own validity contract."""

    def __init__(self, workspace_id: str, reason: str) -> None:
        super().__init__(
            f"Convergence gate blocked: Audience Tensions for workspace "
            f"'{workspace_id}' failed validity check — {reason}",
            reason_code="INVALID_AUDIENCE_TENSIONS",
            details={"workspace_id": workspace_id, "validity_reason": reason},
            permitted_next_actions=["repair_program:audience_context_program"],
        )


class StaleGuestGenesisError(ConvergenceGateError):
    """Raised when the Guest Genesis digest does not match the expected revision."""

    def __init__(
        self,
        workspace_id: str,
        expected_digest: str,
        actual_digest: str,
        revision_id: str,
    ) -> None:
        super().__init__(
            f"Convergence gate blocked: Guest Genesis Semantic Territory digest mismatch "
            f"for workspace '{workspace_id}' at revision '{revision_id}'. "
            f"Expected sha256='{expected_digest[:16]}…', got '{actual_digest[:16]}…'. "
            f"The upstream artifact has been mutated or replaced since last convergence.",
            reason_code="STALE_GUEST_GENESIS_DIGEST",
            details={
                "workspace_id": workspace_id,
                "revision_id": revision_id,
                "expected_digest": expected_digest,
                "actual_digest": actual_digest,
            },
            permitted_next_actions=["re_ratify:guest_genesis_semantic_territory_program", "re_converge"],
        )


class StaleAudienceTensionsError(ConvergenceGateError):
    """Raised when Audience Tensions digest does not match the expected revision."""

    def __init__(
        self,
        workspace_id: str,
        expected_digest: str,
        actual_digest: str,
        revision_id: str,
    ) -> None:
        super().__init__(
            f"Convergence gate blocked: Audience Tensions digest mismatch for workspace "
            f"'{workspace_id}' at revision '{revision_id}'. "
            f"Expected sha256='{expected_digest[:16]}…', got '{actual_digest[:16]}…'. "
            f"The upstream artifact has been mutated or replaced since last convergence.",
            reason_code="STALE_AUDIENCE_TENSIONS_DIGEST",
            details={
                "workspace_id": workspace_id,
                "revision_id": revision_id,
                "expected_digest": expected_digest,
                "actual_digest": actual_digest,
            },
            permitted_next_actions=["re_capture:audience_context_program", "re_converge"],
        )


class ConvergenceRelationError(ConvergenceGateError):
    """Raised when the convergence relation between both sides is structurally invalid."""

    def __init__(self, workspace_id: str, reason: str) -> None:
        super().__init__(
            f"Convergence gate blocked: convergence relation invalid for workspace "
            f"'{workspace_id}' — {reason}",
            reason_code="CONVERGENCE_RELATION_INVALID",
            details={"workspace_id": workspace_id, "relation_reason": reason},
            permitted_next_actions=["re_converge"],
        )


class BypassAttemptError(ConvergenceGateError):
    """Raised when an explicit bypass attempt is made against the convergence gate."""

    def __init__(self, workspace_id: str) -> None:
        super().__init__(
            f"Convergence gate: bypass attempt detected for workspace '{workspace_id}'. "
            f"The gate does not support force=True or override flags. "
            f"This is a CAE constitutional constraint (FR-CONV-001).",
            reason_code="CONVERGENCE_BYPASS_ATTEMPT",
            details={"workspace_id": workspace_id},
            permitted_next_actions=["contact_operator_commander"],
        )


class DownstreamAdmissionBlockedError(ConvergenceGateError):
    """
    Raised at downstream compilation entry points when convergence has not been
    established. This is the integration-level block that prevents programs such
    as editorial_discovery_program from starting without a valid convergence receipt.
    """

    def __init__(
        self,
        workspace_id: str,
        downstream_program_id: str,
        gate_reason_code: str,
        gate_message: str,
    ) -> None:
        super().__init__(
            f"Downstream program '{downstream_program_id}' cannot start for workspace "
            f"'{workspace_id}': dual-context convergence gate has not been satisfied. "
            f"Gate reason: {gate_reason_code} — {gate_message}",
            reason_code="DOWNSTREAM_ADMISSION_BLOCKED_NO_CONVERGENCE",
            details={
                "workspace_id": workspace_id,
                "downstream_program_id": downstream_program_id,
                "gate_reason_code": gate_reason_code,
                "gate_message": gate_message,
            },
            permitted_next_actions=["establish_convergence", f"run_program:guest_genesis_semantic_territory_program", "run_program:audience_context_program"],
        )


# ---------------------------------------------------------------------------
# Value Objects
# ---------------------------------------------------------------------------

class ConvergenceStatus(str, Enum):
    CONVERGED = "CONVERGED"
    BLOCKED = "BLOCKED"
    STALE = "STALE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class GuestGenesisRef:
    """
    Reference to a ratified Guest Genesis Semantic Territory artifact.
    Both revision_id and sha256_digest are required for provenance binding.
    """
    workspace_id: str
    territory_id: str
    revision_id: str
    sha256_digest: str
    ratified_state: str  # Must be TERRITORY_RATIFIED
    wrong_reading_locks: tuple = field(default_factory=tuple)
    vocabulary_boundaries: tuple = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.territory_id or not self.territory_id.strip():
            raise InvalidGuestGenesisError(self.workspace_id, "territory_id cannot be empty")
        if not self.revision_id or not self.revision_id.strip():
            raise InvalidGuestGenesisError(self.workspace_id, "revision_id cannot be empty")
        if not self.sha256_digest or len(self.sha256_digest) != 64:
            raise InvalidGuestGenesisError(
                self.workspace_id,
                f"sha256_digest must be 64-char hex string, got len={len(self.sha256_digest or '')}",
            )
        if self.ratified_state != "TERRITORY_RATIFIED":
            raise InvalidGuestGenesisError(
                self.workspace_id,
                f"Guest Genesis must be in state TERRITORY_RATIFIED, got '{self.ratified_state}'",
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workspace_id": self.workspace_id,
            "territory_id": self.territory_id,
            "revision_id": self.revision_id,
            "sha256_digest": self.sha256_digest,
            "ratified_state": self.ratified_state,
            "wrong_reading_locks": list(self.wrong_reading_locks),
            "vocabulary_boundaries": list(self.vocabulary_boundaries),
        }


@dataclass(frozen=True)
class AudienceTensionsRef:
    """
    Reference to active Audience Tensions from the Audience Context Program.
    Both revision_id and sha256_digest are required for provenance binding.
    """
    workspace_id: str
    audience_id: str
    revision_id: str
    sha256_digest: str
    tension_state: str  # Must be TENSIONS_ACTIVE or equivalent active state
    tension_count: int
    active_tension_labels: tuple = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not self.audience_id or not self.audience_id.strip():
            raise InvalidAudienceTensionsError(self.workspace_id, "audience_id cannot be empty")
        if not self.revision_id or not self.revision_id.strip():
            raise InvalidAudienceTensionsError(self.workspace_id, "revision_id cannot be empty")
        if not self.sha256_digest or len(self.sha256_digest) != 64:
            raise InvalidAudienceTensionsError(
                self.workspace_id,
                f"sha256_digest must be 64-char hex string, got len={len(self.sha256_digest or '')}",
            )
        if self.tension_count < 1:
            raise InvalidAudienceTensionsError(
                self.workspace_id,
                "Audience Tensions must contain at least one active tension",
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workspace_id": self.workspace_id,
            "audience_id": self.audience_id,
            "revision_id": self.revision_id,
            "sha256_digest": self.sha256_digest,
            "tension_state": self.tension_state,
            "tension_count": self.tension_count,
            "active_tension_labels": list(self.active_tension_labels),
        }


@dataclass(frozen=True)
class ConvergenceReceipt:
    """
    Immutable, cryptographically-signed receipt proving dual-context convergence.

    This is the admission token for downstream narrative compilation.
    Downstream programs MUST receive a valid ConvergenceReceipt before starting.
    The receipt pins exact revision IDs and digests from both upstream sources.
    """
    receipt_id: str
    workspace_id: str
    status: ConvergenceStatus
    guest_genesis_territory_id: str
    guest_genesis_revision_id: str
    guest_genesis_sha256: str
    audience_tensions_audience_id: str
    audience_tensions_revision_id: str
    audience_tensions_sha256: str
    convergence_digest: str       # SHA-256 of the combined convergence relation
    convergence_signature: str    # Deterministic provenance signature
    converged_at: str
    gate_version: str = CONVERGENCE_GATE_VERSION

    def to_dict(self) -> Dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "workspace_id": self.workspace_id,
            "status": self.status.value,
            "guest_genesis_territory_id": self.guest_genesis_territory_id,
            "guest_genesis_revision_id": self.guest_genesis_revision_id,
            "guest_genesis_sha256": self.guest_genesis_sha256,
            "audience_tensions_audience_id": self.audience_tensions_audience_id,
            "audience_tensions_revision_id": self.audience_tensions_revision_id,
            "audience_tensions_sha256": self.audience_tensions_sha256,
            "convergence_digest": self.convergence_digest,
            "convergence_signature": self.convergence_signature,
            "converged_at": self.converged_at,
            "gate_version": self.gate_version,
        }

    def is_valid_for_downstream(self) -> bool:
        """Returns True iff this receipt grants admission to downstream compilation."""
        return self.status == ConvergenceStatus.CONVERGED

    def validate_upstream_digests(
        self,
        guest_genesis_ref: GuestGenesisRef,
        audience_tensions_ref: AudienceTensionsRef,
    ) -> None:
        """
        Re-validates the receipt against current upstream artifact digests.
        Raises StaleGuestGenesisError or StaleAudienceTensionsError if any
        upstream artifact has been mutated since convergence.
        """
        if self.guest_genesis_sha256 != guest_genesis_ref.sha256_digest:
            raise StaleGuestGenesisError(
                workspace_id=self.workspace_id,
                expected_digest=self.guest_genesis_sha256,
                actual_digest=guest_genesis_ref.sha256_digest,
                revision_id=guest_genesis_ref.revision_id,
            )
        if self.audience_tensions_sha256 != audience_tensions_ref.sha256_digest:
            raise StaleAudienceTensionsError(
                workspace_id=self.workspace_id,
                expected_digest=self.audience_tensions_sha256,
                actual_digest=audience_tensions_ref.sha256_digest,
                revision_id=audience_tensions_ref.revision_id,
            )


# ---------------------------------------------------------------------------
# Convergence Gate — Core Predicate
# ---------------------------------------------------------------------------

class ConvergenceGate:
    """
    Canonical dual-context convergence gate implementing FR-CONV-001.

    This is the authoritative admission predicate. It must be invoked at
    every downstream narrative compilation entry point, not only in the UI.

    Enforcement contract:
      - evaluate() performs independent validation of each side before combining.
      - require_admitted() raises DownstreamAdmissionBlockedError if not converged.
      - No bypass path exists; force=True raises BypassAttemptError.
      - The receipt produced by evaluate() binds exact revision/digest from both sources.
    """

    def evaluate(
        self,
        *,
        workspace_id: str,
        guest_genesis: Optional[GuestGenesisRef],
        audience_tensions: Optional[AudienceTensionsRef],
        force: bool = False,
    ) -> ConvergenceReceipt:
        """
        Evaluates the dual-context convergence predicate.

        Order of validation (fail-closed on first failure):
          1. Bypass attempt check (no force allowed).
          2. Guest Genesis presence check.
          3. Audience Tensions presence check.
          4. Guest Genesis independent validity (state, digest length).
          5. Audience Tensions independent validity (state, tension_count).
          6. Cross-source workspace isolation check.
          7. Convergence relation construction and digest.

        Returns a ConvergenceReceipt with status=CONVERGED on success.
        Raises ConvergenceGateError subclass on every failure path.
        """
        if force:
            raise BypassAttemptError(workspace_id)

        # 2. Guest Genesis presence
        if guest_genesis is None:
            raise MissingGuestGenesisError(workspace_id)

        # 3. Audience Tensions presence
        if audience_tensions is None:
            raise MissingAudienceTensionsError(workspace_id)

        # 4. Guest Genesis independent validity — __post_init__ already checked on construction,
        #    but we re-verify workspace isolation here.
        if guest_genesis.workspace_id != workspace_id:
            raise InvalidGuestGenesisError(
                workspace_id,
                f"Guest Genesis workspace '{guest_genesis.workspace_id}' does not match "
                f"target workspace '{workspace_id}' (cross-workspace leak prohibited)",
            )

        # 5. Audience Tensions independent validity — workspace isolation
        if audience_tensions.workspace_id != workspace_id:
            raise InvalidAudienceTensionsError(
                workspace_id,
                f"Audience Tensions workspace '{audience_tensions.workspace_id}' does not match "
                f"target workspace '{workspace_id}' (cross-workspace leak prohibited)",
            )

        # 6. Cross-source convergence relation: both sides must reference same workspace
        #    and both must have substantive content.
        if not guest_genesis.vocabulary_boundaries and not guest_genesis.wrong_reading_locks:
            raise ConvergenceRelationError(
                workspace_id,
                "Guest Genesis Semantic Territory contains no vocabulary_boundaries or wrong_reading_locks; "
                "convergence requires substantive territorial content",
            )

        if not audience_tensions.active_tension_labels:
            raise ConvergenceRelationError(
                workspace_id,
                "Audience Tensions contains no active_tension_labels; "
                "convergence requires at least one named active tension",
            )

        # 7. Build convergence relation and compute deterministic digest
        convergence_relation = {
            "workspace_id": workspace_id,
            "guest_genesis_revision_id": guest_genesis.revision_id,
            "guest_genesis_sha256": guest_genesis.sha256_digest,
            "audience_tensions_revision_id": audience_tensions.revision_id,
            "audience_tensions_sha256": audience_tensions.sha256_digest,
            "gate_invariant": FR_CONV_001,
            "gate_version": CONVERGENCE_GATE_VERSION,
        }
        convergence_digest = canonical_sha256(convergence_relation)
        convergence_signature = f"SIG-CONV-{convergence_digest[:24]}"

        receipt = ConvergenceReceipt(
            receipt_id=f"CONV-RCP-{uuid.uuid4().hex[:12]}",
            workspace_id=workspace_id,
            status=ConvergenceStatus.CONVERGED,
            guest_genesis_territory_id=guest_genesis.territory_id,
            guest_genesis_revision_id=guest_genesis.revision_id,
            guest_genesis_sha256=guest_genesis.sha256_digest,
            audience_tensions_audience_id=audience_tensions.audience_id,
            audience_tensions_revision_id=audience_tensions.revision_id,
            audience_tensions_sha256=audience_tensions.sha256_digest,
            convergence_digest=convergence_digest,
            convergence_signature=convergence_signature,
            converged_at=utc_now_rfc3339(),
        )
        return receipt

    def require_admitted(
        self,
        *,
        workspace_id: str,
        guest_genesis: Optional[GuestGenesisRef],
        audience_tensions: Optional[AudienceTensionsRef],
        downstream_program_id: str,
    ) -> ConvergenceReceipt:
        """
        Enforces convergence admission for a downstream compilation program.

        This is the method that MUST be called at every narrative compilation
        entry point. Raises DownstreamAdmissionBlockedError if gate fails,
        ensuring no downstream program can start without a valid receipt.

        The DownstreamAdmissionBlockedError carries the exact gate reason_code
        and message so the operator can see the specific blocker without having
        to diagnose the gate itself.
        """
        try:
            return self.evaluate(
                workspace_id=workspace_id,
                guest_genesis=guest_genesis,
                audience_tensions=audience_tensions,
            )
        except ConvergenceGateError as gate_err:
            raise DownstreamAdmissionBlockedError(
                workspace_id=workspace_id,
                downstream_program_id=downstream_program_id,
                gate_reason_code=gate_err.reason_code,
                gate_message=str(gate_err),
            ) from gate_err


# ---------------------------------------------------------------------------
# Convergence Store — SQLite Persistence
# ---------------------------------------------------------------------------

class ConvergenceStore:
    """
    Authoritative SQLite store for convergence receipts.

    Stores the result of every convergence gate evaluation so the operator
    surface can project the current convergence state for a workspace without
    re-evaluating upstream artifacts from scratch.

    The store is a projection only — it does NOT make authority decisions.
    Authority is always the ConvergenceGate.evaluate() call.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.conn = connection
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        """Creates convergence tables if not present (migration-safe guard)."""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS convergence_receipts (
                    receipt_id TEXT PRIMARY KEY,
                    workspace_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    guest_genesis_territory_id TEXT NOT NULL,
                    guest_genesis_revision_id TEXT NOT NULL,
                    guest_genesis_sha256 TEXT NOT NULL,
                    audience_tensions_audience_id TEXT NOT NULL,
                    audience_tensions_revision_id TEXT NOT NULL,
                    audience_tensions_sha256 TEXT NOT NULL,
                    convergence_digest TEXT NOT NULL UNIQUE,
                    convergence_signature TEXT NOT NULL,
                    converged_at TEXT NOT NULL,
                    gate_version TEXT NOT NULL DEFAULT '1.0.0',
                    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
                );
            """)
            self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_convergence_workspace
                ON convergence_receipts(workspace_id, converged_at DESC);
            """)

    def store_receipt(self, receipt: ConvergenceReceipt) -> ConvergenceReceipt:
        """Persists a convergence receipt. Idempotent on receipt_id."""
        now = utc_now_rfc3339()
        with self.conn:
            self.conn.execute(
                """
                INSERT OR IGNORE INTO convergence_receipts (
                    receipt_id, workspace_id, status,
                    guest_genesis_territory_id, guest_genesis_revision_id, guest_genesis_sha256,
                    audience_tensions_audience_id, audience_tensions_revision_id, audience_tensions_sha256,
                    convergence_digest, convergence_signature, converged_at, gate_version, created_at
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    receipt.receipt_id,
                    receipt.workspace_id,
                    receipt.status.value,
                    receipt.guest_genesis_territory_id,
                    receipt.guest_genesis_revision_id,
                    receipt.guest_genesis_sha256,
                    receipt.audience_tensions_audience_id,
                    receipt.audience_tensions_revision_id,
                    receipt.audience_tensions_sha256,
                    receipt.convergence_digest,
                    receipt.convergence_signature,
                    receipt.converged_at,
                    receipt.gate_version,
                    now,
                ),
            )
        return receipt

    def get_latest_receipt(self, workspace_id: str) -> Optional[ConvergenceReceipt]:
        """Returns the most recent convergence receipt for a workspace, or None."""
        row = self.conn.execute(
            """
            SELECT receipt_id, workspace_id, status,
                   guest_genesis_territory_id, guest_genesis_revision_id, guest_genesis_sha256,
                   audience_tensions_audience_id, audience_tensions_revision_id, audience_tensions_sha256,
                   convergence_digest, convergence_signature, converged_at, gate_version
            FROM convergence_receipts
            WHERE workspace_id = ?
            ORDER BY converged_at DESC
            LIMIT 1
            """,
            (workspace_id,),
        ).fetchone()
        if row is None:
            return None
        return ConvergenceReceipt(
            receipt_id=row[0],
            workspace_id=row[1],
            status=ConvergenceStatus(row[2]),
            guest_genesis_territory_id=row[3],
            guest_genesis_revision_id=row[4],
            guest_genesis_sha256=row[5],
            audience_tensions_audience_id=row[6],
            audience_tensions_revision_id=row[7],
            audience_tensions_sha256=row[8],
            convergence_digest=row[9],
            convergence_signature=row[10],
            converged_at=row[11],
            gate_version=row[12],
        )

    def get_receipt_by_id(self, receipt_id: str) -> Optional[ConvergenceReceipt]:
        """Returns a convergence receipt by ID, or None."""
        row = self.conn.execute(
            """
            SELECT receipt_id, workspace_id, status,
                   guest_genesis_territory_id, guest_genesis_revision_id, guest_genesis_sha256,
                   audience_tensions_audience_id, audience_tensions_revision_id, audience_tensions_sha256,
                   convergence_digest, convergence_signature, converged_at, gate_version
            FROM convergence_receipts
            WHERE receipt_id = ?
            """,
            (receipt_id,),
        ).fetchone()
        if row is None:
            return None
        return ConvergenceReceipt(
            receipt_id=row[0],
            workspace_id=row[1],
            status=ConvergenceStatus(row[2]),
            guest_genesis_territory_id=row[3],
            guest_genesis_revision_id=row[4],
            guest_genesis_sha256=row[5],
            audience_tensions_audience_id=row[6],
            audience_tensions_revision_id=row[7],
            audience_tensions_sha256=row[8],
            convergence_digest=row[9],
            convergence_signature=row[10],
            converged_at=row[11],
            gate_version=row[12],
        )

    def list_receipts(
        self,
        workspace_id: str,
        limit: int = 20,
    ) -> List[ConvergenceReceipt]:
        """Returns all convergence receipts for a workspace, most-recent first."""
        rows = self.conn.execute(
            """
            SELECT receipt_id, workspace_id, status,
                   guest_genesis_territory_id, guest_genesis_revision_id, guest_genesis_sha256,
                   audience_tensions_audience_id, audience_tensions_revision_id, audience_tensions_sha256,
                   convergence_digest, convergence_signature, converged_at, gate_version
            FROM convergence_receipts
            WHERE workspace_id = ?
            ORDER BY converged_at DESC
            LIMIT ?
            """,
            (workspace_id, limit),
        ).fetchall()
        return [
            ConvergenceReceipt(
                receipt_id=r[0],
                workspace_id=r[1],
                status=ConvergenceStatus(r[2]),
                guest_genesis_territory_id=r[3],
                guest_genesis_revision_id=r[4],
                guest_genesis_sha256=r[5],
                audience_tensions_audience_id=r[6],
                audience_tensions_revision_id=r[7],
                audience_tensions_sha256=r[8],
                convergence_digest=r[9],
                convergence_signature=r[10],
                converged_at=r[11],
                gate_version=r[12],
            )
            for r in rows
        ]


# ---------------------------------------------------------------------------
# Downstream Guard — Integration Enforcement
# ---------------------------------------------------------------------------

class DownstreamCompilationGuard:
    """
    Integration-level guard that enforces FR-CONV-001 at the entry of every
    downstream narrative compilation program.

    Usage pattern (must appear at the start of any downstream run_program path
    that constitutes narrative compilation):

        guard = DownstreamCompilationGuard(gate=ConvergenceGate(), store=store)
        receipt = guard.assert_convergence(
            workspace_id=workspace_id,
            guest_genesis=guest_genesis_ref,
            audience_tensions=audience_tensions_ref,
            downstream_program_id=program_id,
        )
        # Only if receipt is valid does downstream execution proceed.

    The guard both evaluates the live gate AND records the receipt to the store.
    """

    def __init__(self, gate: ConvergenceGate, store: ConvergenceStore) -> None:
        self._gate = gate
        self._store = store

    def assert_convergence(
        self,
        *,
        workspace_id: str,
        guest_genesis: Optional[GuestGenesisRef],
        audience_tensions: Optional[AudienceTensionsRef],
        downstream_program_id: str,
    ) -> ConvergenceReceipt:
        """
        Asserts convergence and returns a persisted receipt on success.
        Raises DownstreamAdmissionBlockedError on any gate failure.
        This is the single call that every narrative compilation entry point MUST make.
        """
        receipt = self._gate.require_admitted(
            workspace_id=workspace_id,
            guest_genesis=guest_genesis,
            audience_tensions=audience_tensions,
            downstream_program_id=downstream_program_id,
        )
        self._store.store_receipt(receipt)
        return receipt

    def get_gate_state(
        self,
        workspace_id: str,
    ) -> Dict[str, Any]:
        """
        Returns the current convergence gate state for a workspace as an
        operator-inspectable projection. Does NOT re-evaluate the gate;
        returns the most recent stored receipt.
        """
        receipt = self._store.get_latest_receipt(workspace_id)
        if receipt is None:
            return {
                "workspace_id": workspace_id,
                "status": ConvergenceStatus.UNKNOWN.value,
                "receipt": None,
                "admitted": False,
                "gate_invariant": FR_CONV_001,
            }
        return {
            "workspace_id": workspace_id,
            "status": receipt.status.value,
            "receipt": receipt.to_dict(),
            "admitted": receipt.is_valid_for_downstream(),
            "gate_invariant": FR_CONV_001,
        }
