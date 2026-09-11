"""
CA-M041: Reactive Gate Resumption & Receipts.

This module is deliberately bounded to gate-resolution concerns.  It consumes a
previously-created suspension snapshot (CA-M040), authenticates Commander
decisions, persists an immutable approval receipt, queues a RESUME event, and
only then releases the in-process suspension lock.

State-storage/CAS mechanics remain injectable so CA-M041 does not duplicate the
atomic persistence work governed by CA-M042.
"""

from __future__ import annotations

import asyncio
import enum
import hashlib
import hmac
import json
import os
import threading
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Awaitable, Callable, Deque, Dict, Mapping, Optional, Protocol, Sequence, Tuple, Union

from ca_contracts import canonical_sha256
from ca_runtime.pi_adapter import AuthorityLane


# ============================================================================
# Errors
# ============================================================================


class GateResumptionError(Exception):
    """Base error for governed gate resumption operations."""

    reason_code = "GATE_RESUMPTION_ERROR"

    def __init__(
        self,
        message: str,
        *,
        reason_code: Optional[str] = None,
        details: Optional[Mapping[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.reason_code = reason_code or self.reason_code
        self.details = dict(details or {})


class GateNotFoundError(GateResumptionError):
    reason_code = "GATE_NOT_FOUND"


class GateAlreadyResolvedError(GateResumptionError):
    reason_code = "GATE_ALREADY_RESOLVED"


class GateConflictError(GateResumptionError):
    reason_code = "GATE_DEFINITION_CONFLICT"


class GateAuthorityError(GateResumptionError):
    reason_code = "COMMANDER_AUTHORITY_REQUIRED"


class GateStaleRevisionError(GateResumptionError):
    reason_code = "GATE_STALE_REVISION"


class GateSnapshotIntegrityError(GateResumptionError):
    reason_code = "GATE_SNAPSHOT_INTEGRITY_VIOLATION"


class ReceiptConflictError(GateResumptionError):
    reason_code = "RECEIPT_CONFLICT"


class ReceiptIntegrityError(GateResumptionError):
    reason_code = "RECEIPT_INTEGRITY_VIOLATION"


class ResumeDispatchError(GateResumptionError):
    reason_code = "RESUME_DISPATCH_ERROR"


# ============================================================================
# Domain values
# ============================================================================


class GateResolutionSource(str, enum.Enum):
    """Authoritative sources that can approve a suspended gate."""

    OPERATOR_APPROVAL = "OPERATOR_APPROVAL"
    POLICY_OVERRIDE = "POLICY_OVERRIDE"


class GateLifecycle(str, enum.Enum):
    """Lifecycle of a CA-M041 suspension record."""

    SUSPENDED = "SUSPENDED"
    APPROVAL_RECORDED = "APPROVAL_RECORDED"
    RESUMED = "RESUMED"


class ResumeEventType(str, enum.Enum):
    """Reactive event emitted after an approval is durably recorded."""

    RESUME = "RESUME"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _coerce_lane(value: Union[AuthorityLane, str]) -> AuthorityLane:
    if isinstance(value, AuthorityLane):
        return value
    try:
        return AuthorityLane(str(value))
    except ValueError as exc:
        raise GateAuthorityError(
            f"Unknown authority lane '{value}'",
            details={"actor_lane": str(value), "required_lane": AuthorityLane.COMMANDER.value},
        ) from exc


def _normalise_key(signing_key: Union[str, bytes]) -> bytes:
    if isinstance(signing_key, bytes):
        if not signing_key:
            raise ValueError("signing_key must not be empty")
        return signing_key
    encoded = signing_key.encode("utf-8")
    if not encoded:
        raise ValueError("signing_key must not be empty")
    return encoded


# ============================================================================
# Suspension and policy inputs
# ============================================================================


@dataclass(frozen=True, slots=True)
class SuspendedPipelineGate:
    """Immutable CA-M040 gate snapshot consumed by the CA-M041 resolver."""

    gate_id: str
    pipeline_id: str
    suspension_revision: int
    snapshot_hash: str
    policy_revision_hash: str
    suspended_at: str
    lock_token: str
    next_node_id: Optional[str] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.gate_id:
            raise ValueError("gate_id must not be empty")
        if not self.pipeline_id:
            raise ValueError("pipeline_id must not be empty")
        if self.suspension_revision < 0:
            raise ValueError("suspension_revision must be >= 0")
        if not self.snapshot_hash:
            raise ValueError("snapshot_hash must not be empty")
        if not self.policy_revision_hash:
            raise ValueError("policy_revision_hash must not be empty")
        if not self.suspended_at:
            raise ValueError("suspended_at must not be empty")
        if not self.lock_token:
            raise ValueError("lock_token must not be empty")

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "pipeline_id": self.pipeline_id,
            "suspension_revision": self.suspension_revision,
            "snapshot_hash": self.snapshot_hash,
            "policy_revision_hash": self.policy_revision_hash,
            "suspended_at": self.suspended_at,
            "lock_token": self.lock_token,
            "next_node_id": self.next_node_id,
            "metadata": {str(k): self.metadata[k] for k in sorted(self.metadata)},
        }

    @property
    def gate_digest(self) -> str:
        return canonical_sha256(self.canonical_dict())

    def verify_snapshot_binding(self) -> None:
        """Validate that the immutable gate identity is internally complete."""
        if self.gate_digest == "":
            raise GateSnapshotIntegrityError(
                f"Gate '{self.gate_id}' produced an empty identity digest",
                details={"gate_id": self.gate_id},
            )


@dataclass(frozen=True, slots=True)
class PolicyOverride:
    """A Commander-authorized policy exception attached to one gate decision."""

    override_id: str
    policy_revision_hash: str
    actor_id: str
    reason: str
    issued_at: str
    scope: str = "GATE_RESUMPTION"

    def __post_init__(self) -> None:
        if not self.override_id:
            raise ValueError("override_id must not be empty")
        if not self.policy_revision_hash:
            raise ValueError("policy_revision_hash must not be empty")
        if not self.actor_id:
            raise ValueError("actor_id must not be empty")
        if not self.reason.strip():
            raise ValueError("policy override reason must not be empty")
        if not self.issued_at:
            raise ValueError("issued_at must not be empty")

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "override_id": self.override_id,
            "policy_revision_hash": self.policy_revision_hash,
            "actor_id": self.actor_id,
            "reason": self.reason,
            "issued_at": self.issued_at,
            "scope": self.scope,
        }

    @property
    def override_sha256(self) -> str:
        return canonical_sha256(self.canonical_dict())


# ============================================================================
# Non-repudiable approval receipt
# ============================================================================


@dataclass(frozen=True, slots=True)
class AuthorizationDecisionReceipt:
    """
    Immutable CA-M041 approval receipt.

    The payload is canonicalized and keyed with an HMAC-SHA256 signer.  The
    resulting receipt_sha256 binds the signed material, while actor_fingerprint
    binds the receipt to the approving identity without persisting credentials.
    """

    receipt_id: str
    gate_id: str
    pipeline_id: str
    actor_id: str
    actor_fingerprint: str
    authority_lane: str
    decision: str
    source: str
    decision_at: str
    suspension_revision: int
    snapshot_hash: str
    policy_revision_hash: str
    override_policy_revision_hash: Optional[str]
    override_id: Optional[str]
    lock_token_hash: str
    actor_signature_sha256: str
    receipt_sha256: str
    notes: Optional[str] = None
    previous_receipt_sha256: Optional[str] = None

    def __post_init__(self) -> None:
        if self.decision != "APPROVE":
            raise ValueError("CA-M041 authorization receipts must have decision='APPROVE'")
        if self.authority_lane != AuthorityLane.COMMANDER.value:
            raise ValueError("CA-M041 authorization receipts require COMMANDER authority")
        if not self.receipt_id.startswith("rcpt_appr_"):
            raise ValueError("receipt_id must use the rcpt_appr_ prefix")
        if self.suspension_revision < 0:
            raise ValueError("suspension_revision must be >= 0")

    def canonical_payload(self) -> Dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "gate_id": self.gate_id,
            "pipeline_id": self.pipeline_id,
            "actor_id": self.actor_id,
            "actor_fingerprint": self.actor_fingerprint,
            "authority_lane": self.authority_lane,
            "decision": self.decision,
            "source": self.source,
            "decision_at": self.decision_at,
            "suspension_revision": self.suspension_revision,
            "snapshot_hash": self.snapshot_hash,
            "policy_revision_hash": self.policy_revision_hash,
            "override_policy_revision_hash": self.override_policy_revision_hash,
            "override_id": self.override_id,
            "lock_token_hash": self.lock_token_hash,
            "actor_signature_sha256": self.actor_signature_sha256,
            "notes": self.notes,
            "previous_receipt_sha256": self.previous_receipt_sha256,
        }

    def to_dict(self) -> Dict[str, Any]:
        data = self.canonical_payload()
        data["receipt_sha256"] = self.receipt_sha256
        return data

    @classmethod
    def create(
        cls,
        *,
        gate: SuspendedPipelineGate,
        actor_id: str,
        actor_lane: Union[AuthorityLane, str],
        source: GateResolutionSource,
        signing_key: bytes,
        decision_at: str,
        notes: Optional[str] = None,
        override: Optional[PolicyOverride] = None,
        previous_receipt_sha256: Optional[str] = None,
    ) -> "AuthorizationDecisionReceipt":
        lane = _coerce_lane(actor_lane)
        if lane != AuthorityLane.COMMANDER:
            raise GateAuthorityError(
                f"Gate '{gate.gate_id}' requires COMMANDER authority",
                details={
                    "gate_id": gate.gate_id,
                    "actor_lane": lane.value,
                    "required_lane": AuthorityLane.COMMANDER.value,
                },
            )
        if not actor_id:
            raise GateAuthorityError("actor_id must not be empty", details={"gate_id": gate.gate_id})
        if source == GateResolutionSource.POLICY_OVERRIDE and override is None:
            raise ValueError("policy override source requires an override record")
        if source == GateResolutionSource.OPERATOR_APPROVAL and override is not None:
            raise ValueError("operator approval cannot include a policy override")

        actor_fingerprint = hashlib.sha256(actor_id.encode("utf-8")).hexdigest()
        lock_token_hash = hashlib.sha256(gate.lock_token.encode("utf-8")).hexdigest()
        override_revision = override.policy_revision_hash if override else None
        override_id = override.override_id if override else None
        payload_without_id = {
            "gate_id": gate.gate_id,
            "pipeline_id": gate.pipeline_id,
            "actor_id": actor_id,
            "actor_fingerprint": actor_fingerprint,
            "authority_lane": lane.value,
            "decision": "APPROVE",
            "source": source.value,
            "decision_at": decision_at,
            "suspension_revision": gate.suspension_revision,
            "snapshot_hash": gate.snapshot_hash,
            "policy_revision_hash": gate.policy_revision_hash,
            "override_policy_revision_hash": override_revision,
            "override_id": override_id,
            "lock_token_hash": lock_token_hash,
            "notes": notes,
            "previous_receipt_sha256": previous_receipt_sha256,
        }
        stable_id_digest = hashlib.sha256(
            canonical_sha256(payload_without_id).encode("utf-8")
        ).hexdigest()[:32]
        receipt_id = f"rcpt_appr_{stable_id_digest}"
        payload = dict(payload_without_id)
        payload["receipt_id"] = receipt_id
        actor_signature = hmac.new(
            signing_key,
            canonical_sha256(payload).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        signed_payload = dict(payload)
        signed_payload["actor_signature_sha256"] = actor_signature
        receipt_sha = canonical_sha256(signed_payload)
        return cls(
            receipt_id=receipt_id,
            gate_id=gate.gate_id,
            pipeline_id=gate.pipeline_id,
            actor_id=actor_id,
            actor_fingerprint=actor_fingerprint,
            authority_lane=lane.value,
            decision="APPROVE",
            source=source.value,
            decision_at=decision_at,
            suspension_revision=gate.suspension_revision,
            snapshot_hash=gate.snapshot_hash,
            policy_revision_hash=gate.policy_revision_hash,
            override_policy_revision_hash=override_revision,
            override_id=override_id,
            lock_token_hash=lock_token_hash,
            actor_signature_sha256=actor_signature,
            receipt_sha256=receipt_sha,
            notes=notes,
            previous_receipt_sha256=previous_receipt_sha256,
        )

    def verify(self, signing_key: Union[str, bytes]) -> bool:
        key = _normalise_key(signing_key)
        payload = self.canonical_payload()
        expected_actor_signature = hmac.new(
            key,
            canonical_sha256({k: v for k, v in payload.items() if k != "actor_signature_sha256"}).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected_actor_signature, self.actor_signature_sha256):
            return False
        signed_payload = dict(payload)
        expected_receipt_sha = canonical_sha256(signed_payload)
        return hmac.compare_digest(expected_receipt_sha, self.receipt_sha256)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "AuthorizationDecisionReceipt":
        required = {
            "receipt_id",
            "gate_id",
            "pipeline_id",
            "actor_id",
            "actor_fingerprint",
            "authority_lane",
            "decision",
            "source",
            "decision_at",
            "suspension_revision",
            "snapshot_hash",
            "policy_revision_hash",
            "override_policy_revision_hash",
            "override_id",
            "lock_token_hash",
            "actor_signature_sha256",
            "receipt_sha256",
        }
        missing = sorted(required.difference(data))
        if missing:
            raise ReceiptIntegrityError(
                "Receipt payload is missing required fields",
                details={"missing_fields": missing},
            )
        return cls(
            receipt_id=str(data["receipt_id"]),
            gate_id=str(data["gate_id"]),
            pipeline_id=str(data["pipeline_id"]),
            actor_id=str(data["actor_id"]),
            actor_fingerprint=str(data["actor_fingerprint"]),
            authority_lane=str(data["authority_lane"]),
            decision=str(data["decision"]),
            source=str(data["source"]),
            decision_at=str(data["decision_at"]),
            suspension_revision=int(data["suspension_revision"]),
            snapshot_hash=str(data["snapshot_hash"]),
            policy_revision_hash=str(data["policy_revision_hash"]),
            override_policy_revision_hash=(
                str(data["override_policy_revision_hash"])
                if data["override_policy_revision_hash"] is not None
                else None
            ),
            override_id=str(data["override_id"]) if data["override_id"] is not None else None,
            lock_token_hash=str(data["lock_token_hash"]),
            actor_signature_sha256=str(data["actor_signature_sha256"]),
            receipt_sha256=str(data["receipt_sha256"]),
            notes=str(data["notes"]) if data.get("notes") is not None else None,
            previous_receipt_sha256=(
                str(data["previous_receipt_sha256"])
                if data.get("previous_receipt_sha256") is not None
                else None
            ),
        )

    def verify_receipt_hash(self) -> bool:
        """Verify the receipt's own content hash without access to the signer key."""
        expected = canonical_sha256(self.canonical_payload())
        return hmac.compare_digest(expected, self.receipt_sha256)

    def assert_valid(self, signing_key: Union[str, bytes]) -> None:
        if not self.verify(signing_key):
            raise ReceiptIntegrityError(
                f"Receipt '{self.receipt_id}' failed cryptographic verification",
                details={"receipt_id": self.receipt_id, "gate_id": self.gate_id},
            )


# Backwards-friendly semantic alias used by the mandate wording.
ApprovalReceipt = AuthorizationDecisionReceipt


# ============================================================================
# Reactive resume event
# ============================================================================


@dataclass(frozen=True, slots=True)
class ResumeEvent:
    """Immutable event emitted to the downstream pipeline resume worker."""

    event_id: str
    event_type: str
    gate_id: str
    pipeline_id: str
    receipt_id: str
    snapshot_hash: str
    next_node_id: Optional[str]
    emitted_at: str
    payload: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        gate: SuspendedPipelineGate,
        receipt: AuthorizationDecisionReceipt,
        emitted_at: str,
    ) -> "ResumeEvent":
        event_payload = {
            "gate_id": gate.gate_id,
            "pipeline_id": gate.pipeline_id,
            "receipt_id": receipt.receipt_id,
            "snapshot_hash": gate.snapshot_hash,
            "next_node_id": gate.next_node_id,
            "source": receipt.source,
            "policy_revision_hash": gate.policy_revision_hash,
            "override_policy_revision_hash": receipt.override_policy_revision_hash,
        }
        event_id = f"evt_resume_{canonical_sha256(event_payload)[:32]}"
        return cls(
            event_id=event_id,
            event_type=ResumeEventType.RESUME.value,
            gate_id=gate.gate_id,
            pipeline_id=gate.pipeline_id,
            receipt_id=receipt.receipt_id,
            snapshot_hash=gate.snapshot_hash,
            next_node_id=gate.next_node_id,
            emitted_at=emitted_at,
            payload=event_payload,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "gate_id": self.gate_id,
            "pipeline_id": self.pipeline_id,
            "receipt_id": self.receipt_id,
            "snapshot_hash": self.snapshot_hash,
            "next_node_id": self.next_node_id,
            "emitted_at": self.emitted_at,
            "payload": dict(self.payload),
        }


@dataclass(frozen=True, slots=True)
class GateResolutionResult:
    """Commit evidence returned from an approved gate resolution."""

    gate: SuspendedPipelineGate
    receipt: AuthorizationDecisionReceipt
    resume_event: ResumeEvent
    lifecycle: GateLifecycle

    @property
    def lock_released(self) -> bool:
        return self.lifecycle == GateLifecycle.RESUMED


# ============================================================================
# Receipt persistence
# ============================================================================


class ReceiptStore(Protocol):
    """Minimal append-only receipt persistence contract."""

    def persist(self, receipt: AuthorizationDecisionReceipt) -> None:
        ...

    def get(self, receipt_id: str) -> Optional[AuthorizationDecisionReceipt]:
        ...

    def list_for_gate(self, gate_id: str) -> Sequence[AuthorizationDecisionReceipt]:
        ...


class InMemoryReceiptStore:
    """Thread-safe immutable receipt store for unit/integration tests."""

    def __init__(self) -> None:
        self._receipts: Dict[str, AuthorizationDecisionReceipt] = {}
        self._lock = threading.RLock()

    def persist(self, receipt: AuthorizationDecisionReceipt) -> None:
        with self._lock:
            existing = self._receipts.get(receipt.receipt_id)
            if existing is not None and existing != receipt:
                raise ReceiptConflictError(
                    f"Receipt '{receipt.receipt_id}' already exists with different content",
                    details={"receipt_id": receipt.receipt_id},
                )
            self._receipts[receipt.receipt_id] = receipt

    def get(self, receipt_id: str) -> Optional[AuthorizationDecisionReceipt]:
        with self._lock:
            return self._receipts.get(receipt_id)

    def list_for_gate(self, gate_id: str) -> Sequence[AuthorizationDecisionReceipt]:
        with self._lock:
            return tuple(r for r in self._receipts.values() if r.gate_id == gate_id)


class JsonlReceiptStore:
    """
    Append-only receipt store with fsync-backed persistence.

    It intentionally does not alter the CAE relational schema; deployments that
    need canonical SQLite persistence can implement ReceiptStore against the
    existing CAE state-transition tables without changing this coordinator.
    """

    def __init__(
        self,
        path: Union[str, Path],
        *,
        signing_key: Optional[Union[str, bytes]] = None,
    ) -> None:
        self.path = Path(path)
        self._signing_key = _normalise_key(signing_key) if signing_key is not None else None
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        self._receipts: Dict[str, AuthorizationDecisionReceipt] = {}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    receipt = AuthorizationDecisionReceipt.from_dict(json.loads(line))
                except Exception as exc:
                    raise ReceiptIntegrityError(
                        f"Invalid persisted receipt at {self.path}:{line_number}",
                        details={"path": str(self.path), "line": line_number},
                    ) from exc
                if not receipt.verify_receipt_hash():
                    raise ReceiptIntegrityError(
                        f"Persisted receipt '{receipt.receipt_id}' has an invalid receipt hash",
                        details={"receipt_id": receipt.receipt_id, "path": str(self.path)},
                    )
                if self._signing_key is not None and not receipt.verify(self._signing_key):
                    raise ReceiptIntegrityError(
                        f"Persisted receipt '{receipt.receipt_id}' failed signer verification",
                        details={"receipt_id": receipt.receipt_id, "path": str(self.path)},
                    )
                existing = self._receipts.get(receipt.receipt_id)
                if existing is not None and existing != receipt:
                    raise ReceiptConflictError(
                        f"Receipt '{receipt.receipt_id}' is duplicated with different content",
                        details={"receipt_id": receipt.receipt_id, "path": str(self.path)},
                    )
                self._receipts[receipt.receipt_id] = receipt

    def persist(self, receipt: AuthorizationDecisionReceipt) -> None:
        if not receipt.verify_receipt_hash():
            raise ReceiptIntegrityError(
                f"Receipt '{receipt.receipt_id}' has an invalid receipt hash",
                details={"receipt_id": receipt.receipt_id},
            )
        if self._signing_key is not None:
            receipt.assert_valid(self._signing_key)
        encoded = json.dumps(receipt.to_dict(), sort_keys=True, separators=(",", ":"))
        with self._lock:
            existing = self._receipts.get(receipt.receipt_id)
            if existing is not None:
                if existing != receipt:
                    raise ReceiptConflictError(
                        f"Receipt '{receipt.receipt_id}' already exists with different content",
                        details={"receipt_id": receipt.receipt_id},
                    )
                return
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(encoded + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            self._receipts[receipt.receipt_id] = receipt

    def get(self, receipt_id: str) -> Optional[AuthorizationDecisionReceipt]:
        with self._lock:
            return self._receipts.get(receipt_id)

    def list_for_gate(self, gate_id: str) -> Sequence[AuthorizationDecisionReceipt]:
        with self._lock:
            return tuple(r for r in self._receipts.values() if r.gate_id == gate_id)


# ============================================================================
# Gate registry
# ============================================================================


@dataclass
class _GateRecord:
    gate: SuspendedPipelineGate
    lifecycle: GateLifecycle = GateLifecycle.SUSPENDED
    receipt: Optional[AuthorizationDecisionReceipt] = None
    resume_event: Optional[ResumeEvent] = None


class GateRegistry(Protocol):
    """Lock/suspension registry contract used by the coordinator."""

    def register(self, gate: SuspendedPipelineGate) -> None:
        ...

    def get(self, gate_id: str) -> Optional[_GateRecord]:
        ...

    def record_approval(
        self,
        gate_id: str,
        receipt: AuthorizationDecisionReceipt,
        resume_event: ResumeEvent,
    ) -> _GateRecord:
        ...

    def release_lock(self, gate_id: str, receipt_id: str) -> _GateRecord:
        ...

    def is_locked(self, gate_id: str) -> bool:
        ...


class InMemoryGateRegistry:
    """Thread-safe lock registry; the suspension lock is never released early."""

    def __init__(
        self,
        *,
        before_lock_release: Optional[Callable[[str, AuthorizationDecisionReceipt], None]] = None,
        after_lock_release: Optional[Callable[[str, AuthorizationDecisionReceipt], None]] = None,
    ) -> None:
        self._records: Dict[str, _GateRecord] = {}
        self._lock = threading.RLock()
        self.before_lock_release = before_lock_release
        self.after_lock_release = after_lock_release

    def register(self, gate: SuspendedPipelineGate) -> None:
        gate.verify_snapshot_binding()
        with self._lock:
            existing = self._records.get(gate.gate_id)
            if existing is not None:
                if existing.gate != gate:
                    raise GateConflictError(
                        f"Gate '{gate.gate_id}' is already registered with different suspension data",
                        details={"gate_id": gate.gate_id},
                    )
                return
            self._records[gate.gate_id] = _GateRecord(gate=gate)

    def get(self, gate_id: str) -> Optional[_GateRecord]:
        with self._lock:
            record = self._records.get(gate_id)
            if record is None:
                return None
            return _GateRecord(
                gate=record.gate,
                lifecycle=record.lifecycle,
                receipt=record.receipt,
                resume_event=record.resume_event,
            )

    def record_approval(
        self,
        gate_id: str,
        receipt: AuthorizationDecisionReceipt,
        resume_event: ResumeEvent,
    ) -> _GateRecord:
        with self._lock:
            record = self._records.get(gate_id)
            if record is None:
                raise GateNotFoundError(f"Gate '{gate_id}' not found", details={"gate_id": gate_id})
            if record.lifecycle != GateLifecycle.SUSPENDED:
                if record.receipt == receipt:
                    return _GateRecord(
                        gate=record.gate,
                        lifecycle=record.lifecycle,
                        receipt=record.receipt,
                        resume_event=record.resume_event,
                    )
                raise GateAlreadyResolvedError(
                    f"Gate '{gate_id}' has already been resolved",
                    details={
                        "gate_id": gate_id,
                        "lifecycle": record.lifecycle.value,
                        "receipt_id": record.receipt.receipt_id if record.receipt else None,
                    },
                )
            if receipt.snapshot_hash != record.gate.snapshot_hash:
                raise GateSnapshotIntegrityError(
                    f"Receipt '{receipt.receipt_id}' is bound to a different snapshot",
                    details={
                        "gate_id": gate_id,
                        "expected": record.gate.snapshot_hash,
                        "actual": receipt.snapshot_hash,
                    },
                )
            record.receipt = receipt
            record.resume_event = resume_event
            record.lifecycle = GateLifecycle.APPROVAL_RECORDED
            return _GateRecord(
                gate=record.gate,
                lifecycle=record.lifecycle,
                receipt=record.receipt,
                resume_event=record.resume_event,
            )

    def release_lock(self, gate_id: str, receipt_id: str) -> _GateRecord:
        with self._lock:
            record = self._records.get(gate_id)
            if record is None:
                raise GateNotFoundError(f"Gate '{gate_id}' not found", details={"gate_id": gate_id})
            if record.receipt is None or record.receipt.receipt_id != receipt_id:
                raise GateConflictError(
                    f"Gate '{gate_id}' cannot release its lock without the committed receipt",
                    details={"gate_id": gate_id, "receipt_id": receipt_id},
                )
            if record.lifecycle == GateLifecycle.RESUMED:
                return _GateRecord(
                    gate=record.gate,
                    lifecycle=record.lifecycle,
                    receipt=record.receipt,
                    resume_event=record.resume_event,
                )
            if record.lifecycle != GateLifecycle.APPROVAL_RECORDED:
                raise GateConflictError(
                    f"Gate '{gate_id}' cannot release lock from lifecycle '{record.lifecycle.value}'",
                    details={"gate_id": gate_id, "lifecycle": record.lifecycle.value},
                )
            if self.before_lock_release is not None:
                self.before_lock_release(gate_id, record.receipt)
            record.lifecycle = GateLifecycle.RESUMED
            result = _GateRecord(
                gate=record.gate,
                lifecycle=record.lifecycle,
                receipt=record.receipt,
                resume_event=record.resume_event,
            )
            if self.after_lock_release is not None:
                self.after_lock_release(gate_id, record.receipt)
            return result

    def is_locked(self, gate_id: str) -> bool:
        with self._lock:
            record = self._records.get(gate_id)
            if record is None:
                raise GateNotFoundError(f"Gate '{gate_id}' not found", details={"gate_id": gate_id})
            return record.lifecycle != GateLifecycle.RESUMED


# ============================================================================
# Reactive coordinator
# ============================================================================


ResumeHandler = Union[
    Callable[[ResumeEvent], None],
    Callable[[ResumeEvent], Awaitable[None]],
]


class GateResumptionCoordinator:
    """
    CA-M041 reactive gate resolver.

    Resolution order is fail-closed and explicit:

        validate Commander + freshness
          -> build approval receipt
          -> persist receipt
          -> queue RESUME event while lock is still held
          -> release suspension lock
          -> dispatch reactive RESUME handler(s)

    The coordinator never performs state CAS itself.  A downstream runtime
    handler can use the event and receipt to perform the atomic resume operation
    owned by the next mandate.
    """

    def __init__(
        self,
        *,
        signing_key: Union[str, bytes] = "ca-m041-development-signing-key",
        receipt_store: Optional[ReceiptStore] = None,
        gate_registry: Optional[GateRegistry] = None,
        resume_handlers: Optional[Sequence[ResumeHandler]] = None,
    ) -> None:
        self._signing_key = _normalise_key(signing_key)
        self.receipt_store = receipt_store or InMemoryReceiptStore()
        self.gate_registry = gate_registry or InMemoryGateRegistry()
        self._resume_handlers: Tuple[ResumeHandler, ...] = tuple(resume_handlers or ())
        self._events: Deque[ResumeEvent] = deque()
        self._events_lock = threading.RLock()
        self._resolution_condition = threading.Condition(threading.RLock())

    @property
    def signing_key_fingerprint(self) -> str:
        """Non-secret fingerprint for audit configuration."""
        return hashlib.sha256(self._signing_key).hexdigest()

    def register_suspended_gate(self, gate: SuspendedPipelineGate) -> None:
        """Register a previously-suspended gate exactly once."""
        self.gate_registry.register(gate)

    def get_gate(self, gate_id: str) -> GateLifecycle:
        record = self.gate_registry.get(gate_id)
        if record is None:
            raise GateNotFoundError(f"Gate '{gate_id}' not found", details={"gate_id": gate_id})
        return record.lifecycle

    def is_gate_locked(self, gate_id: str) -> bool:
        return self.gate_registry.is_locked(gate_id)

    def get_receipt(self, receipt_id: str) -> Optional[AuthorizationDecisionReceipt]:
        return self.receipt_store.get(receipt_id)

    def list_receipts(self, gate_id: str) -> Sequence[AuthorizationDecisionReceipt]:
        return self.receipt_store.list_for_gate(gate_id)

    async def submit_approval(
        self,
        *,
        gate_id: str,
        actor_id: str,
        actor_lane: Union[AuthorityLane, str] = AuthorityLane.COMMANDER,
        expected_suspension_revision: Optional[int] = None,
        expected_snapshot_hash: Optional[str] = None,
        notes: Optional[str] = None,
        decision_at: Optional[str] = None,
    ) -> GateResolutionResult:
        """Asynchronously submit and process an operator approval."""
        return await self._resolve(
            gate_id=gate_id,
            actor_id=actor_id,
            actor_lane=actor_lane,
            source=GateResolutionSource.OPERATOR_APPROVAL,
            expected_suspension_revision=expected_suspension_revision,
            expected_snapshot_hash=expected_snapshot_hash,
            notes=notes,
            decision_at=decision_at,
            override=None,
        )

    async def submit_policy_override(
        self,
        *,
        gate_id: str,
        override: PolicyOverride,
        actor_lane: Union[AuthorityLane, str] = AuthorityLane.COMMANDER,
        expected_suspension_revision: Optional[int] = None,
        expected_snapshot_hash: Optional[str] = None,
    ) -> GateResolutionResult:
        """Asynchronously submit a Commander-authorized policy override."""
        if override.scope != "GATE_RESUMPTION":
            raise GateConflictError(
                f"Policy override '{override.override_id}' is outside gate-resumption scope",
                details={"scope": override.scope},
            )
        if override.actor_id == "":
            raise GateAuthorityError("Policy override actor_id must not be empty")
        return await self._resolve(
            gate_id=gate_id,
            actor_id=override.actor_id,
            actor_lane=actor_lane,
            source=GateResolutionSource.POLICY_OVERRIDE,
            expected_suspension_revision=expected_suspension_revision,
            expected_snapshot_hash=expected_snapshot_hash,
            notes=override.reason,
            decision_at=override.issued_at,
            override=override,
        )

    async def _resolve(
        self,
        *,
        gate_id: str,
        actor_id: str,
        actor_lane: Union[AuthorityLane, str],
        source: GateResolutionSource,
        expected_suspension_revision: Optional[int],
        expected_snapshot_hash: Optional[str],
        notes: Optional[str],
        decision_at: Optional[str],
        override: Optional[PolicyOverride],
    ) -> GateResolutionResult:
        lane = _coerce_lane(actor_lane)
        if lane != AuthorityLane.COMMANDER:
            raise GateAuthorityError(
                f"Gate '{gate_id}' requires COMMANDER authority for resumption",
                details={
                    "gate_id": gate_id,
                    "actor_lane": lane.value,
                    "required_lane": AuthorityLane.COMMANDER.value,
                },
            )

        with self._resolution_condition:
            record = self.gate_registry.get(gate_id)
            if record is None:
                raise GateNotFoundError(f"Gate '{gate_id}' not found", details={"gate_id": gate_id})
            gate = record.gate

            expected_revision = (
                gate.suspension_revision
                if expected_suspension_revision is None
                else expected_suspension_revision
            )
            if gate.suspension_revision != expected_revision:
                raise GateStaleRevisionError(
                    f"Gate '{gate_id}' has moved to revision {gate.suspension_revision}",
                    details={
                        "gate_id": gate_id,
                        "expected_revision": expected_revision,
                        "actual_revision": gate.suspension_revision,
                    },
                )

            if expected_snapshot_hash is not None and gate.snapshot_hash != expected_snapshot_hash:
                raise GateStaleRevisionError(
                    f"Gate '{gate_id}' snapshot hash is stale",
                    details={
                        "gate_id": gate_id,
                        "expected_snapshot_hash": expected_snapshot_hash,
                        "actual_snapshot_hash": gate.snapshot_hash,
                    },
                )

            if record.lifecycle != GateLifecycle.SUSPENDED:
                existing = record.receipt
                if existing is not None:
                    if (
                        existing.actor_id == actor_id
                        and existing.source == source.value
                        and existing.snapshot_hash == gate.snapshot_hash
                        and (
                            existing.override_id == (override.override_id if override else None)
                        )
                    ):
                        event = record.resume_event
                        if event is None:
                            raise ResumeDispatchError(
                                f"Resolved gate '{gate_id}' has no RESUME event",
                                details={"gate_id": gate_id, "receipt_id": existing.receipt_id},
                            )
                        return GateResolutionResult(
                            gate=gate,
                            receipt=existing,
                            resume_event=event,
                            lifecycle=record.lifecycle,
                        )
                raise GateAlreadyResolvedError(
                    f"Gate '{gate_id}' has already been resolved",
                    details={
                        "gate_id": gate_id,
                        "lifecycle": record.lifecycle.value,
                        "receipt_id": existing.receipt_id if existing else None,
                    },
                )

            receipt = AuthorizationDecisionReceipt.create(
                gate=gate,
                actor_id=actor_id,
                actor_lane=lane,
                source=source,
                signing_key=self._signing_key,
                decision_at=decision_at or _utc_now(),
                notes=notes,
                override=override,
                previous_receipt_sha256=None,
            )

            # Integrity is verified before any state/lock mutation.
            receipt.assert_valid(self._signing_key)
            existing_receipt = self.receipt_store.get(receipt.receipt_id)
            if existing_receipt is not None and existing_receipt != receipt:
                raise ReceiptConflictError(
                    f"Receipt id '{receipt.receipt_id}' is already committed with different content",
                    details={"receipt_id": receipt.receipt_id},
                )

            # Receipt persistence is the first irreversible CA-M041 side effect.
            # The suspension lock is still held here.
            self.receipt_store.persist(receipt)

            resume_event = ResumeEvent.create(
                gate=gate,
                receipt=receipt,
                emitted_at=_utc_now(),
            )

            # Keep the gate locked until the RESUME event has been durably queued.
            updated_record = self.gate_registry.record_approval(
                gate_id,
                receipt,
                resume_event,
            )

            with self._events_lock:
                if not any(event.event_id == resume_event.event_id for event in self._events):
                    self._events.append(resume_event)

            released = self.gate_registry.release_lock(
                gate_id,
                receipt.receipt_id,
            )
            with self._resolution_condition:
                self._resolution_condition.notify_all()

        # Handler dispatch happens outside the critical section.  The lock is
        # already released, but the receipt and event remain durable/queued.
        await self.dispatch_pending_resumes()
        return GateResolutionResult(
            gate=released.gate,
            receipt=receipt,
            resume_event=resume_event,
            lifecycle=released.lifecycle,
        )

    async def wait_for_resolution(
        self,
        gate_id: str,
        *,
        timeout: Optional[float] = None,
    ) -> GateResolutionResult:
        """
        Await the committed approval of a gate.

        This uses a condition-backed thread wait in an asyncio worker so the
        API remains safe when an approval arrives from another task/thread.
        """

        def _wait() -> GateResolutionResult:
            with self._resolution_condition:
                while True:
                    record = self.gate_registry.get(gate_id)
                    if record is None:
                        raise GateNotFoundError(
                            f"Gate '{gate_id}' not found",
                            details={"gate_id": gate_id},
                        )
                    if record.lifecycle == GateLifecycle.RESUMED and record.receipt and record.resume_event:
                        return GateResolutionResult(
                            gate=record.gate,
                            receipt=record.receipt,
                            resume_event=record.resume_event,
                            lifecycle=record.lifecycle,
                        )
                    self._resolution_condition.wait(timeout=timeout)

        if timeout is None:
            return await asyncio.to_thread(_wait)
        try:
            return await asyncio.wait_for(asyncio.to_thread(_wait), timeout=timeout)
        except asyncio.TimeoutError:
            raise ResumeDispatchError(
                f"Timed out waiting for gate '{gate_id}' resolution",
                reason_code="GATE_RESOLUTION_TIMEOUT",
                details={"gate_id": gate_id, "timeout_seconds": timeout},
            ) from None

    async def dispatch_pending_resumes(self) -> None:
        """
        Run registered resume handlers while retaining undelivered events.

        A coordinator with no handler is intentionally an event-emitting
        boundary: the RESUME event remains queued for the external worker.
        Failed handlers also leave the event at the queue head for retry.
        """
        if not self._resume_handlers:
            return

        while True:
            with self._events_lock:
                if not self._events:
                    return
                event = self._events[0]

            for handler in self._resume_handlers:
                result = handler(event)
                if asyncio.iscoroutine(result):
                    await result

            with self._events_lock:
                if self._events and self._events[0].event_id == event.event_id:
                    self._events.popleft()

    def pending_resume_events(self) -> Sequence[ResumeEvent]:
        with self._events_lock:
            return tuple(self._events)


# Semantic aliases for integrators that prefer "service" terminology.
GateResumptionService = GateResumptionCoordinator
ReactiveGateResumptionEngine = GateResumptionCoordinator


__all__ = [
    "ApprovalReceipt",
    "AuthorizationDecisionReceipt",
    "GateAlreadyResolvedError",
    "GateAuthorityError",
    "GateConflictError",
    "GateLifecycle",
    "GateNotFoundError",
    "GateResolutionError",
    "GateResolutionResult",
    "GateResolutionSource",
    "GateResumptionCoordinator",
    "GateResumptionError",
    "GateResumptionService",
    "GateSnapshotIntegrityError",
    "GateStaleRevisionError",
    "InMemoryGateRegistry",
    "InMemoryReceiptStore",
    "JsonlReceiptStore",
    "PolicyOverride",
    "ReceiptConflictError",
    "ReceiptIntegrityError",
    "ReceiptStore",
    "ReactiveGateResumptionEngine",
    "ResumeEvent",
    "ResumeEventType",
    "SuspendedPipelineGate",
]
