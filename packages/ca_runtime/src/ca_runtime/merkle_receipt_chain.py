"""Deterministic receipt chaining and Merkle commitment for CA-M043.

The ratified Q42 contract calls for a predecessor-linked SHA-256 receipt chain.
This module keeps that authoritative invariant explicit while also providing a
binary Merkle root over the ordered receipt digests so callers can commit the
complete evidence lineage (raw evidence -> gate decisions -> deliverables) to a
single digest without replacing the canonical transition ledger.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
import sqlite3
from typing import Any, Iterable, Mapping, Optional, Sequence

try:
    from ca_contracts import canonical_json_text, canonical_sha256
except ImportError:  # pragma: no cover - project installs ca-contracts; fallback keeps module standalone.
    def canonical_json_text(value: Any) -> str:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)

    def canonical_sha256(value: Any) -> str:
        return hashlib.sha256(canonical_json_text(value).encode("utf-8")).hexdigest()


class MerkleReceiptError(ValueError):
    """Base class for receipt construction and verification failures."""


class ReceiptIdentityError(MerkleReceiptError):
    """Raised when receipts from different execution boundaries are mixed."""


class ReceiptChainIntegrityError(MerkleReceiptError):
    """Raised when a receipt chain or Merkle commitment is not internally valid."""


class ReceiptNotFoundError(MerkleReceiptError):
    """Raised when a required parent receipt is absent."""


class ReceiptAlreadyExistsError(MerkleReceiptError):
    """Raised when a receipt id or transition id is reused with different content."""


_ALLOWED_KINDS = frozenset(
    {
        "RAW_EVIDENCE",
        "GATE_DECISION",
        "DISTRIBUTION_DELIVERABLE",
        "STATE_TRANSITION",
        "OTHER",
    }
)


@dataclass(frozen=True, slots=True)
class MerkleReceipt:
    """Immutable receipt leaf in the canonical predecessor-linked chain."""

    receipt_id: str
    workspace_id: str
    execution_id: str
    campaign_id: str
    sequence: int
    kind: str
    subject_id: str
    payload: Mapping[str, Any]
    parent_receipt_sha256: Optional[str]
    receipt_sha256: str
    receipt_payload: str

    @classmethod
    def create(
        cls,
        *,
        receipt_id: str,
        workspace_id: str,
        execution_id: str,
        campaign_id: str,
        sequence: int,
        kind: str,
        subject_id: str,
        payload: Mapping[str, Any],
        parent_receipt_sha256: Optional[str],
    ) -> "MerkleReceipt":
        _require_text(receipt_id, "receipt_id")
        _require_text(workspace_id, "workspace_id")
        _require_text(execution_id, "execution_id")
        _require_text(campaign_id, "campaign_id")
        _require_text(subject_id, "subject_id")
        if sequence < 0:
            raise MerkleReceiptError("sequence must be >= 0")
        if kind not in _ALLOWED_KINDS:
            raise MerkleReceiptError(f"unsupported receipt kind: {kind!r}")
        if parent_receipt_sha256 is not None:
            _require_sha256(parent_receipt_sha256, "parent_receipt_sha256")

        core = {
            "schema": "cae.merkle_receipt.v1",
            "receipt_id": receipt_id,
            "workspace_id": workspace_id,
            "execution_id": execution_id,
            "campaign_id": campaign_id,
            "sequence": sequence,
            "kind": kind,
            "subject_id": subject_id,
            "parent_receipt_sha256": parent_receipt_sha256,
            "payload": dict(payload),
        }
        canonical = canonical_json_text(core)
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return cls(
            receipt_id=receipt_id,
            workspace_id=workspace_id,
            execution_id=execution_id,
            campaign_id=campaign_id,
            sequence=sequence,
            kind=kind,
            subject_id=subject_id,
            payload=dict(payload),
            parent_receipt_sha256=parent_receipt_sha256,
            receipt_sha256=digest,
            receipt_payload=canonical,
        )

    def verify(self) -> bool:
        expected = hashlib.sha256(self.receipt_payload.encode("utf-8")).hexdigest()
        return hmac.compare_digest(expected, self.receipt_sha256) and self._payload_matches_fields()

    def _payload_matches_fields(self) -> bool:
        try:
            payload = json.loads(self.receipt_payload)
        except (TypeError, ValueError):
            return False
        expected = {
            "schema": "cae.merkle_receipt.v1",
            "receipt_id": self.receipt_id,
            "workspace_id": self.workspace_id,
            "execution_id": self.execution_id,
            "campaign_id": self.campaign_id,
            "sequence": self.sequence,
            "kind": self.kind,
            "subject_id": self.subject_id,
            "parent_receipt_sha256": self.parent_receipt_sha256,
            "payload": dict(self.payload),
        }
        return payload == expected

    def to_record(self) -> dict[str, Any]:
        return {
            "receipt_id": self.receipt_id,
            "workspace_id": self.workspace_id,
            "execution_id": self.execution_id,
            "campaign_id": self.campaign_id,
            "sequence": self.sequence,
            "kind": self.kind,
            "subject_id": self.subject_id,
            "payload": dict(self.payload),
            "parent_receipt_sha256": self.parent_receipt_sha256,
            "receipt_sha256": self.receipt_sha256,
            "receipt_payload": self.receipt_payload,
        }

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "MerkleReceipt":
        try:
            payload = record["payload"]
            if isinstance(payload, str):
                payload = json.loads(payload)
            return cls(
                receipt_id=str(record["receipt_id"]),
                workspace_id=str(record["workspace_id"]),
                execution_id=str(record["execution_id"]),
                campaign_id=str(record.get("campaign_id", "")),
                sequence=int(record["sequence"]),
                kind=str(record["kind"]),
                subject_id=str(record["subject_id"]),
                payload=dict(payload),
                parent_receipt_sha256=(
                    None
                    if record.get("parent_receipt_sha256") is None
                    else str(record["parent_receipt_sha256"])
                ),
                receipt_sha256=str(record["receipt_sha256"]),
                receipt_payload=str(record["receipt_payload"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise MerkleReceiptError("invalid persisted receipt record") from exc


class MerkleReceiptChain:
    """Append-only receipt chain plus deterministic binary Merkle commitment."""

    def __init__(self, *, workspace_id: str, execution_id: str, campaign_id: str) -> None:
        _require_text(workspace_id, "workspace_id")
        _require_text(execution_id, "execution_id")
        _require_text(campaign_id, "campaign_id")
        self.workspace_id = workspace_id
        self.execution_id = execution_id
        self.campaign_id = campaign_id
        self._receipts: list[MerkleReceipt] = []

    @property
    def receipts(self) -> tuple[MerkleReceipt, ...]:
        return tuple(self._receipts)

    @property
    def root_receipt_sha256(self) -> Optional[str]:
        return self._receipts[-1].receipt_sha256 if self._receipts else None

    @property
    def merkle_root_sha256(self) -> Optional[str]:
        if not self._receipts:
            return None
        return merkle_root([receipt.receipt_sha256 for receipt in self._receipts])

    def append(
        self,
        *,
        receipt_id: str,
        kind: str,
        subject_id: str,
        payload: Mapping[str, Any],
    ) -> MerkleReceipt:
        parent = self._receipts[-1] if self._receipts else None
        receipt = MerkleReceipt.create(
            receipt_id=receipt_id,
            workspace_id=self.workspace_id,
            execution_id=self.execution_id,
            campaign_id=self.campaign_id,
            sequence=len(self._receipts),
            kind=kind,
            subject_id=subject_id,
            payload=payload,
            parent_receipt_sha256=parent.receipt_sha256 if parent else None,
        )
        self._append_verified(receipt)
        return receipt

    def append_transition(
        self,
        *,
        transition: Mapping[str, Any],
        actor_id: Optional[str] = None,
        payload: Optional[Mapping[str, Any]] = None,
    ) -> MerkleReceipt:
        """Build a receipt directly from an accepted persisted transition record."""
        transition_id = str(transition["transition_id"])
        transition_payload = dict(payload if payload is not None else transition.get("payload", {}))
        if actor_id is not None:
            transition_payload["actor_id"] = actor_id
        required_identity = {
            "workspace_id": self.workspace_id,
            "execution_id": self.execution_id,
            "campaign_id": self.campaign_id,
        }
        for field, expected in required_identity.items():
            actual = transition.get(field, expected)
            if str(actual) != expected:
                raise ReceiptIdentityError(
                    f"transition {transition_id!r} belongs to {field}={actual!r}, not {expected!r}"
                )
        return self.append(
            receipt_id=str(transition.get("receipt_id", f"rcpt_{transition_id}")),
            kind="STATE_TRANSITION",
            subject_id=transition_id,
            payload={
                "from_state": str(transition["from_state"]),
                "to_state": str(transition["to_state"]),
                "transition_name": str(transition["transition_name"]),
                "trigger_operation": str(transition["trigger_operation"]),
                "lane": str(transition["lane"]),
                "expected_version": int(transition["expected_version"]),
                "committed_version": int(transition["committed_version"]),
                "timestamp": str(transition["timestamp"]),
                "payload": transition_payload,
            },
        )

    def extend(self, receipts: Iterable[MerkleReceipt]) -> None:
        for receipt in receipts:
            self._append_verified(receipt)

    def _append_verified(self, receipt: MerkleReceipt) -> None:
        if receipt.workspace_id != self.workspace_id or receipt.execution_id != self.execution_id or receipt.campaign_id != self.campaign_id:
            raise ReceiptIdentityError("receipt crosses the chain's workspace/execution/campaign boundary")
        if not receipt.verify():
            raise ReceiptChainIntegrityError(f"receipt {receipt.receipt_id!r} fails digest verification")
        expected_sequence = len(self._receipts)
        expected_parent = self._receipts[-1].receipt_sha256 if self._receipts else None
        if receipt.sequence != expected_sequence:
            raise ReceiptChainIntegrityError(
                f"expected sequence {expected_sequence}, got {receipt.sequence} for {receipt.receipt_id!r}"
            )
        if receipt.parent_receipt_sha256 != expected_parent:
            raise ReceiptChainIntegrityError(
                f"receipt {receipt.receipt_id!r} does not reference its immediate predecessor"
            )
        if any(existing.receipt_id == receipt.receipt_id for existing in self._receipts):
            raise ReceiptAlreadyExistsError(f"duplicate receipt_id {receipt.receipt_id!r}")
        self._receipts.append(receipt)

    def verify(self) -> None:
        """Fail closed on any digest, identity, sequence, parent, or branch anomaly."""
        by_hash: dict[str, MerkleReceipt] = {}
        by_sequence: dict[int, MerkleReceipt] = {}
        for index, receipt in enumerate(self._receipts):
            if not receipt.verify():
                raise ReceiptChainIntegrityError(f"digest mismatch at sequence {receipt.sequence}")
            if receipt.sequence != index:
                raise ReceiptChainIntegrityError("receipt sequence is not contiguous")
            if receipt.workspace_id != self.workspace_id or receipt.execution_id != self.execution_id or receipt.campaign_id != self.campaign_id:
                raise ReceiptIdentityError("chain contains a cross-boundary receipt")
            expected_parent = None if index == 0 else self._receipts[index - 1].receipt_sha256
            if receipt.parent_receipt_sha256 != expected_parent:
                raise ReceiptChainIntegrityError(
                    f"parent mismatch at sequence {receipt.sequence}: "
                    f"expected {expected_parent!r}, got {receipt.parent_receipt_sha256!r}"
                )
            if receipt.receipt_sha256 in by_hash:
                raise ReceiptChainIntegrityError("receipt hash is reused in the same chain")
            if receipt.sequence in by_sequence:
                raise ReceiptChainIntegrityError("receipt sequence is duplicated")
            by_hash[receipt.receipt_sha256] = receipt
            by_sequence[receipt.sequence] = receipt

    def export_records(self) -> list[dict[str, Any]]:
        self.verify()
        return [receipt.to_record() for receipt in self._receipts]

    @classmethod
    def from_records(
        cls,
        records: Sequence[Mapping[str, Any]],
        *,
        workspace_id: str,
        execution_id: str,
        campaign_id: str,
    ) -> "MerkleReceiptChain":
        chain = cls(workspace_id=workspace_id, execution_id=execution_id, campaign_id=campaign_id)
        chain.extend(MerkleReceipt.from_record(record) for record in records)
        chain.verify()
        return chain


class SQLiteMerkleReceiptStore:
    """Small persistence adapter for CA-M043 receipt records.

    The adapter intentionally uses its own table so it can be adopted without
    silently rewriting the Q41 transition transaction. Integration into the
    canonical state runtime remains the caller's responsibility.
    """

    TABLE = "cae_merkle_receipts"

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.connection.row_factory = sqlite3.Row
        self.connection.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.TABLE} (
                receipt_id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                execution_id TEXT NOT NULL,
                campaign_id TEXT NOT NULL,
                sequence INTEGER NOT NULL,
                kind TEXT NOT NULL,
                subject_id TEXT NOT NULL,
                payload TEXT NOT NULL,
                parent_receipt_sha256 TEXT,
                receipt_sha256 TEXT NOT NULL UNIQUE,
                receipt_payload TEXT NOT NULL,
                UNIQUE(workspace_id, execution_id, campaign_id, sequence),
                UNIQUE(workspace_id, execution_id, campaign_id, subject_id)
            )
            """
        )
        self.connection.commit()

    def append(self, receipt: MerkleReceipt) -> None:
        chain = self.load_chain(
            workspace_id=receipt.workspace_id,
            execution_id=receipt.execution_id,
            campaign_id=receipt.campaign_id,
        )
        chain._append_verified(receipt)
        self.connection.execute(
            f"""
            INSERT INTO {self.TABLE} (
                receipt_id, workspace_id, execution_id, campaign_id, sequence,
                kind, subject_id, payload, parent_receipt_sha256,
                receipt_sha256, receipt_payload
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                receipt.receipt_id,
                receipt.workspace_id,
                receipt.execution_id,
                receipt.campaign_id,
                receipt.sequence,
                receipt.kind,
                receipt.subject_id,
                canonical_json_text(dict(receipt.payload)),
                receipt.parent_receipt_sha256,
                receipt.receipt_sha256,
                receipt.receipt_payload,
            ),
        )
        self.connection.commit()

    def get(self, receipt_sha256: str) -> MerkleReceipt:
        _require_sha256(receipt_sha256, "receipt_sha256")
        row = self.connection.execute(
            f"SELECT * FROM {self.TABLE} WHERE receipt_sha256 = ?",
            (receipt_sha256,),
        ).fetchone()
        if row is None:
            raise ReceiptNotFoundError(f"receipt {receipt_sha256!r} not found")
        return MerkleReceipt.from_record(dict(row))

    def load_chain(self, *, workspace_id: str, execution_id: str, campaign_id: str) -> MerkleReceiptChain:
        rows = self.connection.execute(
            f"""
            SELECT * FROM {self.TABLE}
            WHERE workspace_id = ? AND execution_id = ? AND campaign_id = ?
            ORDER BY sequence ASC
            """,
            (workspace_id, execution_id, campaign_id),
        ).fetchall()
        return MerkleReceiptChain.from_records(
            [dict(row) for row in rows],
            workspace_id=workspace_id,
            execution_id=execution_id,
            campaign_id=campaign_id,
        )

    def verify_chain(self, *, workspace_id: str, execution_id: str, campaign_id: str) -> str:
        chain = self.load_chain(workspace_id=workspace_id, execution_id=execution_id, campaign_id=campaign_id)
        chain.verify()
        root = chain.merkle_root_sha256
        if root is None:
            raise ReceiptChainIntegrityError("cannot verify an empty receipt chain")
        return root

    def verify_all_boundaries(self) -> dict[tuple[str, str, str], str]:
        scopes = self.connection.execute(
            f"SELECT DISTINCT workspace_id, execution_id, campaign_id FROM {self.TABLE}"
        ).fetchall()
        return {
            (str(row["workspace_id"]), str(row["execution_id"]), str(row["campaign_id"])): self.verify_chain(
                workspace_id=str(row["workspace_id"]),
                execution_id=str(row["execution_id"]),
                campaign_id=str(row["campaign_id"]),
            )
            for row in scopes
        }


def merkle_root(receipt_hashes: Sequence[str]) -> str:
    """Compute a domain-separated binary Merkle root over ordered receipt hashes."""
    if not receipt_hashes:
        raise ValueError("receipt_hashes must not be empty")
    for index, digest in enumerate(receipt_hashes):
        _require_sha256(digest, f"receipt_hashes[{index}]")
    level = list(receipt_hashes)
    while len(level) > 1:
        next_level: list[str] = []
        for index in range(0, len(level), 2):
            left = level[index]
            right = level[index + 1] if index + 1 < len(level) else left
            next_level.append(_merkle_pair(left, right))
        level = next_level
    return level[0]


def build_evidence_chain(
    *,
    workspace_id: str,
    execution_id: str,
    campaign_id: str,
    raw_evidence: Iterable[tuple[str, Mapping[str, Any]]],
    gate_decisions: Iterable[tuple[str, Mapping[str, Any]]],
    distribution_deliverables: Iterable[tuple[str, Mapping[str, Any]]],
) -> MerkleReceiptChain:
    """Build one ordered commitment spanning raw evidence, gates, and deliverables."""
    chain = MerkleReceiptChain(
        workspace_id=workspace_id,
        execution_id=execution_id,
        campaign_id=campaign_id,
    )
    for receipt_id, payload in raw_evidence:
        chain.append(
            receipt_id=receipt_id,
            kind="RAW_EVIDENCE",
            subject_id=receipt_id,
            payload=payload,
        )
    for receipt_id, payload in gate_decisions:
        chain.append(
            receipt_id=receipt_id,
            kind="GATE_DECISION",
            subject_id=receipt_id,
            payload=payload,
        )
    for receipt_id, payload in distribution_deliverables:
        chain.append(
            receipt_id=receipt_id,
            kind="DISTRIBUTION_DELIVERABLE",
            subject_id=receipt_id,
            payload=payload,
        )
    chain.verify()
    return chain


def _merkle_pair(left: str, right: str) -> str:
    domain = b"CA-M043-MERKLE-NODE-v1\x00"
    return hashlib.sha256(domain + bytes.fromhex(left) + bytes.fromhex(right)).hexdigest()


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise MerkleReceiptError(f"{field_name} must be a non-empty string")


def _require_sha256(value: str, field_name: str) -> None:
    if not isinstance(value, str) or len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value.lower()):
        raise MerkleReceiptError(f"{field_name} must be a 64-character hexadecimal SHA-256 digest")
