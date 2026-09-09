"""Governed shared-workspace memory write-back (CA-M032 / INV-MEM-001).

This module is the canonical runtime boundary for durable memory promotion.
Raw observations are never accepted as memory writes. Durable memory may be
changed only by a typed :class:`LearningCandidate` carrying explicit evidence,
attribution, confidence, merge consensus, and provenance.

The SQLite persistence boundary is deliberately small and fail-closed:
- candidate payloads are schema validated before persistence;
- promotion policy requires configured evidence/confidence thresholds;
- merge consensus is explicit and hash-bound to the candidate value;
- stale workspace versions are rejected instead of overwritten;
- every successful persisted memory item receives immutable provenance rows and
  an auditable promotion receipt;
- a candidate ID is idempotent only when the candidate bytes are identical.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from typing import Any, Iterator, Literal, Mapping, Optional, Sequence, Tuple, Union
from uuid import uuid4


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class MemoryWritebackError(RuntimeError):
    """Base class for governed memory write-back failures."""


class MemorySchemaError(MemoryWritebackError):
    """Raised when a candidate or persisted payload violates the contract."""


class MemoryProvenanceError(MemoryWritebackError):
    """Raised when evidence or attribution provenance is invalid."""


class MemoryPolicyError(MemoryWritebackError):
    """Raised when a candidate does not satisfy the configured promotion policy."""


class MemoryConsensusError(MemoryWritebackError):
    """Raised when a merge consensus is missing, stale, or hash-inconsistent."""


class MemoryConflictError(MemoryWritebackError):
    """Raised when a concurrent/stale writer would overwrite newer memory."""


class RawObservationWriteRejected(MemoryWritebackError):
    """Raised whenever a raw observation attempts to cross the durable boundary."""


# ---------------------------------------------------------------------------
# Canonical serialization / hashing helpers
# ---------------------------------------------------------------------------


_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _canonical_json(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise MemorySchemaError("memory values must be JSON-serializable") from exc


def _sha256_json(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _require_text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MemorySchemaError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_sha256(value: Any, field_name: str) -> str:
    value = _require_text(value, field_name).lower()
    if not _SHA256_RE.fullmatch(value):
        raise MemoryProvenanceError(f"{field_name} must be a lowercase SHA-256 digest")
    return value


def _normalize_workspace_id(value: Any) -> str:
    return _require_text(value, "workspace_id").lower()


# ---------------------------------------------------------------------------
# Typed contract
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ProvenanceRef:
    """Immutable provenance reference bound to an evidence source."""

    source_id: str
    source_sha256: str
    source_kind: str
    locator: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_id", _require_text(self.source_id, "source_id"))
        object.__setattr__(self, "source_kind", _require_text(self.source_kind, "source_kind"))
        object.__setattr__(self, "source_sha256", _require_sha256(self.source_sha256, "source_sha256"))
        if not isinstance(self.locator, str):
            raise MemoryProvenanceError("locator must be a string")

    def to_dict(self) -> dict[str, str]:
        return {
            "source_id": self.source_id,
            "source_sha256": self.source_sha256,
            "source_kind": self.source_kind,
            "locator": self.locator,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ProvenanceRef":
        if not isinstance(payload, Mapping):
            raise MemorySchemaError("provenance entries must be objects")
        allowed = {"source_id", "source_sha256", "source_kind", "locator"}
        unknown = set(payload) - allowed
        missing = {"source_id", "source_sha256", "source_kind"} - set(payload)
        if unknown:
            raise MemorySchemaError(f"unknown provenance fields: {sorted(unknown)}")
        if missing:
            raise MemorySchemaError(f"missing provenance fields: {sorted(missing)}")
        return cls(
            source_id=payload["source_id"],
            source_sha256=payload["source_sha256"],
            source_kind=payload["source_kind"],
            locator=payload.get("locator", ""),
        )


@dataclass(frozen=True, slots=True)
class MergeConsensus:
    """Explicit decision proving that the proposed value is agreed for a version."""

    mode: Literal["INSERT", "MERGE"]
    expected_memory_version: int
    basis_refs: Tuple[str, ...]
    resolved_value_sha256: str
    rationale: str

    def __post_init__(self) -> None:
        if self.mode not in {"INSERT", "MERGE"}:
            raise MemoryConsensusError("merge consensus mode must be INSERT or MERGE")
        if not isinstance(self.expected_memory_version, int) or self.expected_memory_version < 0:
            raise MemoryConsensusError("expected_memory_version must be a non-negative integer")
        if not self.basis_refs or any(not isinstance(ref, str) or not ref.strip() for ref in self.basis_refs):
            raise MemoryConsensusError("merge consensus requires at least one non-empty basis reference")
        if len(set(self.basis_refs)) != len(self.basis_refs):
            raise MemoryConsensusError("merge consensus basis references must be unique")
        object.__setattr__(
            self,
            "resolved_value_sha256",
            _require_sha256(self.resolved_value_sha256, "resolved_value_sha256"),
        )
        object.__setattr__(self, "rationale", _require_text(self.rationale, "rationale"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "expected_memory_version": self.expected_memory_version,
            "basis_refs": list(self.basis_refs),
            "resolved_value_sha256": self.resolved_value_sha256,
            "rationale": self.rationale,
        }


@dataclass(frozen=True, slots=True)
class LearningCandidate:
    """Schema-conformant intermediate object eligible for governed promotion."""

    candidate_id: str
    workspace_id: str
    memory_key: str
    value: Any
    evidence_refs: Tuple[ProvenanceRef, ...]
    attribution_ref: ProvenanceRef
    confidence_bps: int
    merge_consensus: MergeConsensus
    actor_id: str
    created_at: str = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidate_id", _require_text(self.candidate_id, "candidate_id"))
        object.__setattr__(self, "workspace_id", _normalize_workspace_id(self.workspace_id))
        object.__setattr__(self, "memory_key", _require_text(self.memory_key, "memory_key"))
        object.__setattr__(self, "actor_id", _require_text(self.actor_id, "actor_id"))
        if not self.evidence_refs:
            raise MemorySchemaError("evidence_refs must contain at least one provenance reference")
        if not isinstance(self.confidence_bps, int) or not 0 <= self.confidence_bps <= 10_000:
            raise MemorySchemaError("confidence_bps must be an integer from 0 through 10000")
        if not isinstance(self.created_at, str) or not self.created_at.strip():
            raise MemorySchemaError("created_at must be a non-empty timestamp string")
        # Validate serializability at the typed boundary rather than discovering it during SQL execution.
        _canonical_json(self.value)

    @property
    def value_sha256(self) -> str:
        return _sha256_json(self.value)

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "workspace_id": self.workspace_id,
            "memory_key": self.memory_key,
            "value": self.value,
            "evidence_refs": [ref.to_dict() for ref in self.evidence_refs],
            "attribution_ref": self.attribution_ref.to_dict(),
            "confidence_bps": self.confidence_bps,
            "merge_consensus": self.merge_consensus.to_dict(),
            "actor_id": self.actor_id,
            "created_at": self.created_at,
        }

    def canonical_bytes(self) -> str:
        return _canonical_json(self.to_dict())

    @property
    def candidate_sha256(self) -> str:
        return _sha256_text(self.canonical_bytes())

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "LearningCandidate":
        if not isinstance(payload, Mapping):
            raise MemorySchemaError("LearningCandidate payload must be an object")
        required = {
            "candidate_id",
            "workspace_id",
            "memory_key",
            "value",
            "evidence_refs",
            "attribution_ref",
            "confidence_bps",
            "merge_consensus",
            "actor_id",
            "created_at",
        }
        unknown = set(payload) - required
        missing = required - set(payload)
        if unknown:
            raise MemorySchemaError(f"unknown LearningCandidate fields: {sorted(unknown)}")
        if missing:
            raise MemorySchemaError(f"missing LearningCandidate fields: {sorted(missing)}")
        raw_evidence = payload["evidence_refs"]
        if not isinstance(raw_evidence, Sequence) or isinstance(raw_evidence, (str, bytes, bytearray)):
            raise MemorySchemaError("evidence_refs must be a list of objects")
        evidence_refs = tuple(ProvenanceRef.from_dict(item) for item in raw_evidence)
        raw_consensus = payload["merge_consensus"]
        if not isinstance(raw_consensus, Mapping):
            raise MemorySchemaError("merge_consensus must be an object")
        consensus_allowed = {
            "mode",
            "expected_memory_version",
            "basis_refs",
            "resolved_value_sha256",
            "rationale",
        }
        unknown_consensus = set(raw_consensus) - consensus_allowed
        missing_consensus = consensus_allowed - set(raw_consensus)
        if unknown_consensus:
            raise MemorySchemaError(f"unknown merge consensus fields: {sorted(unknown_consensus)}")
        if missing_consensus:
            raise MemorySchemaError(f"missing merge consensus fields: {sorted(missing_consensus)}")
        consensus = MergeConsensus(
            mode=raw_consensus["mode"],
            expected_memory_version=raw_consensus["expected_memory_version"],
            basis_refs=tuple(raw_consensus["basis_refs"]),
            resolved_value_sha256=raw_consensus["resolved_value_sha256"],
            rationale=raw_consensus["rationale"],
        )
        return cls(
            candidate_id=payload["candidate_id"],
            workspace_id=payload["workspace_id"],
            memory_key=payload["memory_key"],
            value=payload["value"],
            evidence_refs=evidence_refs,
            attribution_ref=ProvenanceRef.from_dict(payload["attribution_ref"]),
            confidence_bps=payload["confidence_bps"],
            merge_consensus=consensus,
            actor_id=payload["actor_id"],
            created_at=payload["created_at"],
        )


@dataclass(frozen=True, slots=True)
class MemoryWritebackPolicy:
    """Explicit, runtime-supplied promotion thresholds and requirements."""

    minimum_confidence_bps: int
    minimum_evidence_refs: int = 1
    require_attribution: bool = True
    require_consensus: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.minimum_confidence_bps, int) or not 0 <= self.minimum_confidence_bps <= 10_000:
            raise MemoryPolicyError("minimum_confidence_bps must be an integer from 0 through 10000")
        if not isinstance(self.minimum_evidence_refs, int) or self.minimum_evidence_refs < 1:
            raise MemoryPolicyError("minimum_evidence_refs must be at least one")
        if not self.require_attribution:
            raise MemoryPolicyError("attribution is mandatory for governed memory promotion")
        if not self.require_consensus:
            raise MemoryPolicyError("merge consensus is mandatory for governed memory promotion")


@dataclass(frozen=True, slots=True)
class MemoryItem:
    item_id: str
    workspace_id: str
    memory_key: str
    value: Any
    version: int
    provenance: Tuple[ProvenanceRef, ...]
    created_at: str
    updated_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "workspace_id": self.workspace_id,
            "memory_key": self.memory_key,
            "value": self.value,
            "version": self.version,
            "provenance": [ref.to_dict() for ref in self.provenance],
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass(frozen=True, slots=True)
class PromotionReceipt:
    receipt_id: str
    workspace_id: str
    candidate_id: str
    candidate_sha256: str
    outcome: Literal["PROMOTED", "REJECTED"]
    item_id: Optional[str]
    resulting_version: Optional[int]
    reason: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "workspace_id": self.workspace_id,
            "candidate_id": self.candidate_id,
            "candidate_sha256": self.candidate_sha256,
            "outcome": self.outcome,
            "item_id": self.item_id,
            "resulting_version": self.resulting_version,
            "reason": self.reason,
            "created_at": self.created_at,
        }


# ---------------------------------------------------------------------------
# SQLite write-back store
# ---------------------------------------------------------------------------


class MemoryWritebackStore:
    """Canonical durable-memory boundary for governed Learning Candidate promotion."""

    def __init__(
        self,
        db_path: Union[str, Path, None] = None,
        *,
        policy: MemoryWritebackPolicy,
        connection: Optional[sqlite3.Connection] = None,
    ) -> None:
        if not isinstance(policy, MemoryWritebackPolicy):
            raise TypeError("policy must be a MemoryWritebackPolicy")
        self.policy = policy
        self._shared_connection = connection
        self._db_path = None if db_path in (None, ":memory:") else Path(db_path)
        if connection is not None:
            connection.row_factory = sqlite3.Row
            self._init_schema(connection)
        elif db_path in (None, ":memory:"):
            self._shared_connection = sqlite3.connect(":memory:", check_same_thread=False)
            self._shared_connection.row_factory = sqlite3.Row
            self._init_schema(self._shared_connection)
        else:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            with self._connect() as conn:
                self._init_schema(conn)

    def _connect(self) -> sqlite3.Connection:
        if self._shared_connection is not None:
            return self._shared_connection
        conn = sqlite3.connect(self._db_path.as_posix(), timeout=10.0, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA busy_timeout = 10000")
        return conn

    @staticmethod
    def _init_schema(conn: sqlite3.Connection) -> None:
        conn.executescript(
            """
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS memory_items (
                item_id TEXT NOT NULL,
                workspace_id TEXT NOT NULL,
                memory_key TEXT NOT NULL,
                value_json TEXT NOT NULL,
                value_sha256 TEXT NOT NULL,
                version INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (workspace_id, memory_key),
                UNIQUE (item_id)
            );

            CREATE TABLE IF NOT EXISTS memory_provenance (
                item_id TEXT NOT NULL,
                provenance_role TEXT NOT NULL,
                source_id TEXT NOT NULL,
                source_sha256 TEXT NOT NULL,
                source_kind TEXT NOT NULL,
                locator TEXT NOT NULL,
                recorded_at TEXT NOT NULL,
                PRIMARY KEY (item_id, provenance_role, source_id),
                FOREIGN KEY (item_id) REFERENCES memory_items(item_id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS memory_writeback_receipts (
                receipt_id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                candidate_id TEXT NOT NULL,
                candidate_sha256 TEXT NOT NULL,
                outcome TEXT NOT NULL CHECK(outcome IN ('PROMOTED', 'REJECTED')),
                item_id TEXT,
                resulting_version INTEGER,
                reason TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE (workspace_id, candidate_id)
            );

            CREATE INDEX IF NOT EXISTS idx_memory_items_workspace
                ON memory_items(workspace_id, memory_key);
            CREATE INDEX IF NOT EXISTS idx_memory_provenance_item
                ON memory_provenance(item_id);
            """
        )

    @contextmanager
    def _transaction(self) -> Iterator[sqlite3.Connection]:
        conn = self._connect()
        owns_transaction = conn.in_transaction is False
        try:
            if owns_transaction:
                conn.execute("BEGIN IMMEDIATE")
            yield conn
            if owns_transaction:
                conn.commit()
        except Exception:
            if owns_transaction and conn.in_transaction:
                conn.rollback()
            raise
        finally:
            if self._shared_connection is None:
                conn.close()

    def close(self) -> None:
        if self._shared_connection is not None:
            self._shared_connection.close()
            self._shared_connection = None

    # ----- validation -----------------------------------------------------

    def _validate_candidate(self, candidate: LearningCandidate) -> None:
        if not isinstance(candidate, LearningCandidate):
            raise MemorySchemaError(
                "durable memory accepts only LearningCandidate objects; raw dictionaries/observations are rejected"
            )
        if len(candidate.evidence_refs) < self.policy.minimum_evidence_refs:
            raise MemoryPolicyError(
                f"candidate requires at least {self.policy.minimum_evidence_refs} evidence references"
            )
        if candidate.confidence_bps < self.policy.minimum_confidence_bps:
            raise MemoryPolicyError(
                f"candidate confidence {candidate.confidence_bps} is below required "
                f"threshold {self.policy.minimum_confidence_bps}"
            )
        if self.policy.require_attribution and not candidate.attribution_ref.source_id:
            raise MemoryProvenanceError("attribution reference is required")
        consensus = candidate.merge_consensus
        if self.policy.require_consensus:
            if consensus.mode not in {"INSERT", "MERGE"}:
                raise MemoryConsensusError("invalid merge consensus mode")
            if consensus.resolved_value_sha256 != candidate.value_sha256:
                raise MemoryConsensusError("merge consensus hash does not match candidate value")
            known_basis = {ref.source_id for ref in candidate.evidence_refs}
            if not set(consensus.basis_refs).issubset(known_basis):
                raise MemoryConsensusError("merge consensus basis refs must be backed by candidate evidence")
        # Attribution must itself be content-hash bound; no weak labels are accepted.
        _require_sha256(candidate.attribution_ref.source_sha256, "attribution_ref.source_sha256")

    # ----- read ----------------------------------------------------------

    def get_memory(self, workspace_id: str, memory_key: str) -> Optional[MemoryItem]:
        ws = _normalize_workspace_id(workspace_id)
        key = _require_text(memory_key, "memory_key")
        conn = self._connect()
        try:
            row = conn.execute(
                """
                SELECT item_id, workspace_id, memory_key, value_json, version, created_at, updated_at
                FROM memory_items
                WHERE workspace_id = ? AND memory_key = ?
                """,
                (ws, key),
            ).fetchone()
            if row is None:
                return None
            provenance_rows = conn.execute(
                """
                SELECT source_id, source_sha256, source_kind, locator
                FROM memory_provenance
                WHERE item_id = ?
                ORDER BY provenance_role, source_id
                """,
                (row["item_id"],),
            ).fetchall()
            return MemoryItem(
                item_id=row["item_id"],
                workspace_id=row["workspace_id"],
                memory_key=row["memory_key"],
                value=json.loads(row["value_json"]),
                version=row["version"],
                provenance=tuple(
                    ProvenanceRef(
                        source_id=prov["source_id"],
                        source_sha256=prov["source_sha256"],
                        source_kind=prov["source_kind"],
                        locator=prov["locator"],
                    )
                    for prov in provenance_rows
                ),
                created_at=row["created_at"],
                updated_at=row["updated_at"],
            )
        finally:
            if self._shared_connection is None:
                conn.close()

    def get_receipt(self, workspace_id: str, candidate_id: str) -> Optional[PromotionReceipt]:
        ws = _normalize_workspace_id(workspace_id)
        cid = _require_text(candidate_id, "candidate_id")
        conn = self._connect()
        try:
            row = conn.execute(
                """
                SELECT receipt_id, workspace_id, candidate_id, candidate_sha256,
                       outcome, item_id, resulting_version, reason, created_at
                FROM memory_writeback_receipts
                WHERE workspace_id = ? AND candidate_id = ?
                """,
                (ws, cid),
            ).fetchone()
            if row is None:
                return None
            return PromotionReceipt(
                receipt_id=row["receipt_id"],
                workspace_id=row["workspace_id"],
                candidate_id=row["candidate_id"],
                candidate_sha256=row["candidate_sha256"],
                outcome=row["outcome"],
                item_id=row["item_id"],
                resulting_version=row["resulting_version"],
                reason=row["reason"],
                created_at=row["created_at"],
            )
        finally:
            if self._shared_connection is None:
                conn.close()

    # ----- authoritative write boundary --------------------------------

    def promote(self, candidate: LearningCandidate) -> PromotionReceipt:
        """Promote one Learning Candidate into durable memory, atomically.

        A stale writer is rejected by the version predicate. A candidate ID is
        idempotent only when the exact candidate bytes match an existing receipt.
        """

        self._validate_candidate(candidate)
        now = _utc_now()
        candidate_sha = candidate.candidate_sha256
        consensus = candidate.merge_consensus

        with self._transaction() as conn:
            prior_receipt = conn.execute(
                """
                SELECT receipt_id, workspace_id, candidate_id, candidate_sha256,
                       outcome, item_id, resulting_version, reason, created_at
                FROM memory_writeback_receipts
                WHERE workspace_id = ? AND candidate_id = ?
                """,
                (candidate.workspace_id, candidate.candidate_id),
            ).fetchone()
            if prior_receipt is not None:
                if prior_receipt["candidate_sha256"] != candidate_sha:
                    raise MemoryConflictError("candidate_id already exists for different candidate bytes")
                return PromotionReceipt(
                    receipt_id=prior_receipt["receipt_id"],
                    workspace_id=prior_receipt["workspace_id"],
                    candidate_id=prior_receipt["candidate_id"],
                    candidate_sha256=prior_receipt["candidate_sha256"],
                    outcome=prior_receipt["outcome"],
                    item_id=prior_receipt["item_id"],
                    resulting_version=prior_receipt["resulting_version"],
                    reason=prior_receipt["reason"],
                    created_at=prior_receipt["created_at"],
                )

            existing = conn.execute(
                """
                SELECT item_id, value_json, version, created_at
                FROM memory_items
                WHERE workspace_id = ? AND memory_key = ?
                """,
                (candidate.workspace_id, candidate.memory_key),
            ).fetchone()
            current_version = 0 if existing is None else int(existing["version"])

            if consensus.expected_memory_version != current_version:
                raise MemoryConflictError(
                    f"memory version mismatch for {candidate.memory_key}: "
                    f"expected {consensus.expected_memory_version}, current {current_version}"
                )

            if existing is None:
                if consensus.mode != "INSERT":
                    raise MemoryConsensusError("new memory requires INSERT consensus")
                item_id = f"mem_{uuid4().hex}"
                next_version = 1
                created_at = now
                updated_at = now
                conn.execute(
                    """
                    INSERT INTO memory_items(
                        item_id, workspace_id, memory_key, value_json,
                        value_sha256, version, created_at, updated_at
                    ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item_id,
                        candidate.workspace_id,
                        candidate.memory_key,
                        _canonical_json(candidate.value),
                        candidate.value_sha256,
                        next_version,
                        created_at,
                        updated_at,
                    ),
                )
            else:
                if consensus.mode != "MERGE":
                    raise MemoryConsensusError("existing memory requires MERGE consensus")
                item_id = existing["item_id"]
                next_version = current_version + 1
                updated_at = now
                cursor = conn.execute(
                    """
                    UPDATE memory_items
                    SET value_json = ?, value_sha256 = ?, version = ?, updated_at = ?
                    WHERE workspace_id = ? AND memory_key = ? AND version = ?
                    """,
                    (
                        _canonical_json(candidate.value),
                        candidate.value_sha256,
                        next_version,
                        updated_at,
                        candidate.workspace_id,
                        candidate.memory_key,
                        current_version,
                    ),
                )
                if cursor.rowcount != 1:
                    raise MemoryConflictError(
                        f"concurrent memory mutation detected for {candidate.memory_key}"
                    )
                created_at = existing["created_at"]

            provenance_at = now
            for ref in candidate.evidence_refs:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO memory_provenance(
                        item_id, provenance_role, source_id, source_sha256,
                        source_kind, locator, recorded_at
                    ) VALUES(?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        item_id,
                        "EVIDENCE",
                        ref.source_id,
                        ref.source_sha256,
                        ref.source_kind,
                        ref.locator,
                        provenance_at,
                    ),
                )

            ref = candidate.attribution_ref
            conn.execute(
                """
                INSERT OR IGNORE INTO memory_provenance(
                    item_id, provenance_role, source_id, source_sha256,
                    source_kind, locator, recorded_at
                ) VALUES(?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item_id,
                    "ATTRIBUTION",
                    ref.source_id,
                    ref.source_sha256,
                    ref.source_kind,
                    ref.locator,
                    provenance_at,
                ),
            )

            receipt_id = f"mwb_{uuid4().hex}"
            conn.execute(
                """
                INSERT INTO memory_writeback_receipts(
                    receipt_id, workspace_id, candidate_id, candidate_sha256,
                    outcome, item_id, resulting_version, reason, created_at
                ) VALUES(?, ?, ?, ?, 'PROMOTED', ?, ?, ?, ?)
                """,
                (
                    receipt_id,
                    candidate.workspace_id,
                    candidate.candidate_id,
                    candidate_sha,
                    item_id,
                    next_version,
                    "Learning Candidate promoted after schema, policy, attribution, and consensus validation",
                    now,
                ),
            )
            return PromotionReceipt(
                receipt_id=receipt_id,
                workspace_id=candidate.workspace_id,
                candidate_id=candidate.candidate_id,
                candidate_sha256=candidate_sha,
                outcome="PROMOTED",
                item_id=item_id,
                resulting_version=next_version,
                reason="Learning Candidate promoted after schema, policy, attribution, and consensus validation",
                created_at=now,
            )

    def write_raw_observation(self, observation: Any, *, workspace_id: str = "") -> None:
        """Explicitly reject raw observations at the durable boundary."""

        raise RawObservationWriteRejected(
            "raw observations cannot be written to durable memory; construct a governed LearningCandidate"
        )

    def list_provenance(self, workspace_id: str, memory_key: str) -> Tuple[ProvenanceRef, ...]:
        item = self.get_memory(workspace_id, memory_key)
        return tuple() if item is None else item.provenance


__all__ = [
    "LearningCandidate",
    "MemoryConflictError",
    "MemoryConsensusError",
    "MemoryItem",
    "MemoryPolicyError",
    "MemoryProvenanceError",
    "MemorySchemaError",
    "MemoryWritebackError",
    "MemoryWritebackPolicy",
    "MemoryWritebackStore",
    "MergeConsensus",
    "PromotionReceipt",
    "ProvenanceRef",
    "RawObservationWriteRejected",
]
