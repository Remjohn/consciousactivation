"""Durable, tamper-evident authorization decision receipts.

CA-M026 / FR-AUTH-001.

This module is intentionally self-contained and uses SQLite plus standard-library
cryptography.  Every authorization grant, denial, or operator override recorded
through :class:`AuthorizationDecisionReceiptStore` is durably persisted as an
append-only, hash-chained receipt.  Each receipt also carries an HMAC-SHA256
signature over its cryptographic identity.

The signing key is supplied by the runtime authority (and must not be stored in
the receipt database).  A caller that loses the key can still inspect the
records, but cannot produce receipts that pass cryptographic verification.

The store is an evidence ledger, not an authorization policy engine: callers
must only record decisions after their canonical authorization predicate has
been evaluated.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Optional

SCHEMA_VERSION = 1
RECEIPT_VERSION = "1.0.0"
POLICY_SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


class AuthorizationDecision(str, Enum):
    """The three governed authorization outcomes covered by FR-AUTH-001."""

    GRANT = "GRANT"
    DENY = "DENY"
    OPERATOR_OVERRIDE = "OPERATOR_OVERRIDE"


class AuthorizationReceiptError(RuntimeError):
    """Base error for authorization receipt failures."""


class InvalidAuthorizationReceiptError(AuthorizationReceiptError, ValueError):
    """Raised when receipt input or a persisted receipt is structurally invalid."""


class AuthorizationReceiptIntegrityError(AuthorizationReceiptError):
    """Raised when a receipt's hash chain or cryptographic signature is invalid."""


class AuthorizationReceiptConflictError(AuthorizationReceiptError):
    """Raised when an append would create an ambiguous/conflicting decision."""


def _canonical_json(value: Mapping[str, Any]) -> bytes:
    """Encode a JSON object canonically for cryptographic hashing."""

    try:
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise InvalidAuthorizationReceiptError(
            f"Receipt payload is not canonically JSON serializable: {exc}"
        ) from exc


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_json(value: Mapping[str, Any]) -> str:
    return _sha256_bytes(_canonical_json(value))


def _normalize_timestamp(timestamp: Optional[str]) -> str:
    if timestamp is None:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    value = str(timestamp).strip()
    if not value:
        raise InvalidAuthorizationReceiptError("timestamp must be non-empty")

    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise InvalidAuthorizationReceiptError(
            "timestamp must be an RFC3339/ISO-8601 timestamp"
        ) from exc

    if parsed.tzinfo is None:
        raise InvalidAuthorizationReceiptError(
            "timestamp must include an explicit timezone"
        )

    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_key(signing_key: bytes | str) -> bytes:
    if isinstance(signing_key, str):
        signing_key = signing_key.encode("utf-8")
    if not isinstance(signing_key, bytes) or not signing_key:
        raise InvalidAuthorizationReceiptError("signing_key must be non-empty bytes")
    return signing_key


@dataclass(frozen=True)
class AuthorizationDecisionReceipt:
    """Immutable representation of one durable authorization decision."""

    receipt_id: str
    decision: AuthorizationDecision
    actor_id: str
    decision_reason: str
    policy_hash: str
    timestamp: str
    resource_id: str
    resource_revision: str
    resource_state_hash: str
    previous_receipt_hash: Optional[str]
    receipt_hash: str
    signature: str
    receipt_version: str = RECEIPT_VERSION

    @property
    def actor_identity(self) -> str:
        """Semantic alias for the required actor identity field."""

        return self.actor_id

    @property
    def reason(self) -> str:
        """Semantic alias for the required decision reason field."""

        return self.decision_reason

    def signing_payload(self) -> dict[str, Any]:
        """Return the exact immutable fields covered by the receipt signature."""

        return {
            "receipt_version": self.receipt_version,
            "receipt_id": self.receipt_id,
            "decision": self.decision.value,
            "actor_id": self.actor_id,
            "decision_reason": self.decision_reason,
            "policy_hash": self.policy_hash,
            "timestamp": self.timestamp,
            "resource_id": self.resource_id,
            "resource_revision": self.resource_revision,
            "resource_state_hash": self.resource_state_hash,
            "previous_receipt_hash": self.previous_receipt_hash,
        }

    def to_dict(self) -> dict[str, Any]:
        result = self.signing_payload()
        result.update(
            {
                "receipt_hash": self.receipt_hash,
                "signature": self.signature,
            }
        )
        return result

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "AuthorizationDecisionReceipt":
        try:
            return cls(
                receipt_id=row["receipt_id"],
                decision=AuthorizationDecision(row["decision"]),
                actor_id=row["actor_id"],
                decision_reason=row["decision_reason"],
                policy_hash=row["policy_hash"],
                timestamp=row["timestamp"],
                resource_id=row["resource_id"],
                resource_revision=row["resource_revision"],
                resource_state_hash=row["resource_state_hash"],
                previous_receipt_hash=row["previous_receipt_hash"],
                receipt_hash=row["receipt_hash"],
                signature=row["signature"],
                receipt_version=row["receipt_version"],
            )
        except (KeyError, ValueError, TypeError) as exc:
            raise InvalidAuthorizationReceiptError(
                f"Persisted authorization receipt is malformed: {exc}"
            ) from exc


class AuthorizationDecisionReceiptStore:
    """Durable append-only authorization receipt ledger.

    ``db_path`` may be a filesystem path or ``":memory:"``.  The latter is
    useful for unit tests but does not provide durability across connections.

    ``signing_key`` is deliberately external to the database.  It is the
    cryptographic authority used to attribute receipts to the trusted runtime.
    """

    def __init__(self, db_path: str | Path, signing_key: bytes | str) -> None:
        self.db_path = str(db_path)
        self._signing_key = _normalize_key(signing_key)
        self._conn = sqlite3.connect(
            self.db_path,
            isolation_level=None,
            check_same_thread=False,
        )
        self._conn.row_factory = sqlite3.Row
        self._configure()

    def _configure(self) -> None:
        self._conn.execute("PRAGMA foreign_keys = ON")
        if self.db_path != ":memory:":
            self._conn.execute("PRAGMA journal_mode = WAL")
            self._conn.execute("PRAGMA synchronous = FULL")

        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS cae_authorization_receipt_meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS cae_authorization_decision_receipt (
                receipt_id TEXT PRIMARY KEY,
                receipt_version TEXT NOT NULL,
                decision TEXT NOT NULL CHECK (
                    decision IN ('GRANT', 'DENY', 'OPERATOR_OVERRIDE')
                ),
                actor_id TEXT NOT NULL,
                decision_reason TEXT NOT NULL,
                policy_hash TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                resource_id TEXT NOT NULL,
                resource_revision TEXT NOT NULL,
                resource_state_hash TEXT NOT NULL,
                previous_receipt_hash TEXT,
                receipt_hash TEXT NOT NULL UNIQUE,
                signature TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_cae_auth_receipt_resource
                ON cae_authorization_decision_receipt(resource_id, resource_revision);

            CREATE INDEX IF NOT EXISTS idx_cae_auth_receipt_timestamp
                ON cae_authorization_decision_receipt(timestamp);

            CREATE TRIGGER IF NOT EXISTS trg_cae_auth_receipt_no_update
            BEFORE UPDATE ON cae_authorization_decision_receipt
            BEGIN
                SELECT RAISE(ABORT, 'EX_AUTH_RECEIPT_IMMUTABLE: UPDATE prohibited');
            END;

            CREATE TRIGGER IF NOT EXISTS trg_cae_auth_receipt_no_delete
            BEFORE DELETE ON cae_authorization_decision_receipt
            BEGIN
                SELECT RAISE(ABORT, 'EX_AUTH_RECEIPT_IMMUTABLE: DELETE prohibited');
            END;
            """
        )

        existing = self._conn.execute(
            "SELECT value FROM cae_authorization_receipt_meta WHERE key = 'schema_version'"
        ).fetchone()
        if existing is None:
            self._conn.execute(
                "INSERT INTO cae_authorization_receipt_meta(key, value) VALUES (?, ?)",
                ("schema_version", str(SCHEMA_VERSION)),
            )
        elif int(existing["value"]) != SCHEMA_VERSION:
            raise InvalidAuthorizationReceiptError(
                f"Unsupported authorization receipt schema version: {existing['value']}"
            )

    def close(self) -> None:
        self._conn.close()

    def __enter__(self) -> "AuthorizationDecisionReceiptStore":
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    @staticmethod
    def _validate_inputs(
        *,
        actor_id: str,
        decision_reason: str,
        policy_hash: str,
        resource_id: str,
        resource_revision: str,
        resource_state_hash: str,
    ) -> None:
        fields = {
            "actor_id": actor_id,
            "decision_reason": decision_reason,
            "policy_hash": policy_hash,
            "resource_id": resource_id,
            "resource_revision": resource_revision,
            "resource_state_hash": resource_state_hash,
        }
        for name, value in fields.items():
            if not isinstance(value, str) or not value.strip():
                raise InvalidAuthorizationReceiptError(f"{name} must be non-empty")

        if not POLICY_SHA256_RE.fullmatch(policy_hash):
            raise InvalidAuthorizationReceiptError(
                "policy_hash must be a 64-character hexadecimal SHA-256 digest"
            )
        if not POLICY_SHA256_RE.fullmatch(resource_state_hash):
            raise InvalidAuthorizationReceiptError(
                "resource_state_hash must be a 64-character hexadecimal digest"
            )

    def _sign(self, receipt_hash: str) -> str:
        return hmac.new(
            self._signing_key,
            receipt_hash.encode("ascii"),
            hashlib.sha256,
        ).hexdigest()

    def _verify_signature(self, receipt: AuthorizationDecisionReceipt) -> bool:
        expected = self._sign(receipt.receipt_hash)
        return hmac.compare_digest(expected, receipt.signature)

    def _last_receipt_hash(self) -> Optional[str]:
        row = self._conn.execute(
            """
            SELECT receipt_hash
            FROM cae_authorization_decision_receipt
            ORDER BY rowid DESC
            LIMIT 1
            """
        ).fetchone()
        return None if row is None else row["receipt_hash"]

    def record(
        self,
        *,
        decision: AuthorizationDecision | str,
        actor_id: str,
        decision_reason: str,
        policy_hash: str,
        resource_id: str,
        resource_revision: str,
        resource_state_hash: str,
        timestamp: Optional[str] = None,
        receipt_id: Optional[str] = None,
    ) -> AuthorizationDecisionReceipt:
        """Atomically append one grant, denial, or operator override.

        The receipt binds the actor, reason, policy revision, exact resource
        revision/state digest, timestamp, and previous ledger entry.
        """

        try:
            decision_value = (
                decision
                if isinstance(decision, AuthorizationDecision)
                else AuthorizationDecision(str(decision).strip().upper())
            )
        except ValueError as exc:
            raise InvalidAuthorizationReceiptError(
                f"Unsupported authorization decision: {decision!r}"
            ) from exc

        self._validate_inputs(
            actor_id=actor_id,
            decision_reason=decision_reason,
            policy_hash=policy_hash,
            resource_id=resource_id,
            resource_revision=resource_revision,
            resource_state_hash=resource_state_hash,
        )
        normalized_timestamp = _normalize_timestamp(timestamp)
        normalized_receipt_id = (receipt_id or str(uuid.uuid4())).strip()
        if not normalized_receipt_id:
            raise InvalidAuthorizationReceiptError("receipt_id must be non-empty")

        # The chain tip is read and the row is inserted in one IMMEDIATE
        # transaction, preventing two writers from creating the same predecessor.
        self._conn.execute("BEGIN IMMEDIATE")
        try:
            previous_hash = self._last_receipt_hash()
            signing_payload = {
                "receipt_version": RECEIPT_VERSION,
                "receipt_id": normalized_receipt_id,
                "decision": decision_value.value,
                "actor_id": actor_id.strip(),
                "decision_reason": decision_reason.strip(),
                "policy_hash": policy_hash.lower(),
                "timestamp": normalized_timestamp,
                "resource_id": resource_id.strip(),
                "resource_revision": resource_revision.strip(),
                "resource_state_hash": resource_state_hash.lower(),
                "previous_receipt_hash": previous_hash,
            }
            receipt_hash = _sha256_json(signing_payload)
            signature = self._sign(receipt_hash)

            try:
                self._conn.execute(
                    """
                    INSERT INTO cae_authorization_decision_receipt (
                        receipt_id, receipt_version, decision, actor_id,
                        decision_reason, policy_hash, timestamp, resource_id,
                        resource_revision, resource_state_hash,
                        previous_receipt_hash, receipt_hash, signature
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        normalized_receipt_id,
                        RECEIPT_VERSION,
                        decision_value.value,
                        actor_id.strip(),
                        decision_reason.strip(),
                        policy_hash.lower(),
                        normalized_timestamp,
                        resource_id.strip(),
                        resource_revision.strip(),
                        resource_state_hash.lower(),
                        previous_hash,
                        receipt_hash,
                        signature,
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise AuthorizationReceiptConflictError(
                    f"Authorization receipt append conflicts with existing receipt: {exc}"
                ) from exc
            self._conn.execute("COMMIT")
        except Exception:
            self._conn.execute("ROLLBACK")
            raise

        return AuthorizationDecisionReceipt(
            receipt_id=normalized_receipt_id,
            decision=decision_value,
            actor_id=actor_id.strip(),
            decision_reason=decision_reason.strip(),
            policy_hash=policy_hash.lower(),
            timestamp=normalized_timestamp,
            resource_id=resource_id.strip(),
            resource_revision=resource_revision.strip(),
            resource_state_hash=resource_state_hash.lower(),
            previous_receipt_hash=previous_hash,
            receipt_hash=receipt_hash,
            signature=signature,
        )

    def grant(self, **kwargs: Any) -> AuthorizationDecisionReceipt:
        """Convenience method for recording an authorization grant."""

        return self.record(decision=AuthorizationDecision.GRANT, **kwargs)

    def deny(self, **kwargs: Any) -> AuthorizationDecisionReceipt:
        """Convenience method for recording an authorization denial."""

        return self.record(decision=AuthorizationDecision.DENY, **kwargs)

    def operator_override(self, **kwargs: Any) -> AuthorizationDecisionReceipt:
        """Convenience method for recording an operator override."""

        return self.record(decision=AuthorizationDecision.OPERATOR_OVERRIDE, **kwargs)

    def get(self, receipt_id: str) -> AuthorizationDecisionReceipt:
        row = self._conn.execute(
            """
            SELECT * FROM cae_authorization_decision_receipt
            WHERE receipt_id = ?
            """,
            (receipt_id,),
        ).fetchone()
        if row is None:
            raise KeyError(receipt_id)
        return AuthorizationDecisionReceipt.from_row(row)

    def list_receipts(self, *, resource_id: Optional[str] = None) -> list[AuthorizationDecisionReceipt]:
        if resource_id is None:
            rows = self._conn.execute(
                """
                SELECT * FROM cae_authorization_decision_receipt
                ORDER BY rowid ASC
                """
            ).fetchall()
        else:
            rows = self._conn.execute(
                """
                SELECT * FROM cae_authorization_decision_receipt
                WHERE resource_id = ?
                ORDER BY rowid ASC
                """,
                (resource_id,),
            ).fetchall()
        return [AuthorizationDecisionReceipt.from_row(row) for row in rows]

    def verify_receipt(self, receipt_id: str) -> AuthorizationDecisionReceipt:
        """Verify one receipt's content and signature against the supplied key."""

        receipt = self.get(receipt_id)
        expected_hash = _sha256_json(receipt.signing_payload())
        if not hmac.compare_digest(expected_hash, receipt.receipt_hash):
            raise AuthorizationReceiptIntegrityError(
                f"Receipt {receipt_id!r} content hash does not match its persisted hash"
            )
        if not self._verify_signature(receipt):
            raise AuthorizationReceiptIntegrityError(
                f"Receipt {receipt_id!r} signature verification failed"
            )
        return receipt

    def verify_chain(self) -> list[AuthorizationDecisionReceipt]:
        """Verify every receipt, predecessor linkage, and HMAC signature.

        This is intentionally a fresh read from the durable database so callers
        can run it after a process restart or independently of the writer object.
        """

        receipts = self.list_receipts()
        previous_hash: Optional[str] = None
        for receipt in receipts:
            if receipt.previous_receipt_hash != previous_hash:
                raise AuthorizationReceiptIntegrityError(
                    f"Receipt chain broken at {receipt.receipt_id!r}: "
                    f"expected predecessor {previous_hash!r}, "
                    f"found {receipt.previous_receipt_hash!r}"
                )

            expected_hash = _sha256_json(receipt.signing_payload())
            if not hmac.compare_digest(expected_hash, receipt.receipt_hash):
                raise AuthorizationReceiptIntegrityError(
                    f"Receipt {receipt.receipt_id!r} content hash does not match"
                )
            if not self._verify_signature(receipt):
                raise AuthorizationReceiptIntegrityError(
                    f"Receipt {receipt.receipt_id!r} signature verification failed"
                )
            previous_hash = receipt.receipt_hash

        return receipts

    def verify_resource_revision(
        self,
        *,
        resource_id: str,
        resource_revision: str,
        resource_state_hash: str,
    ) -> bool:
        """Check that a persisted receipt refers to the exact inspected revision."""

        receipts = self.list_receipts(resource_id=resource_id)
        return any(
            r.resource_revision == resource_revision
            and hmac.compare_digest(r.resource_state_hash, resource_state_hash.lower())
            for r in receipts
        )

    def count(self) -> int:
        row = self._conn.execute(
            "SELECT COUNT(*) AS count FROM cae_authorization_decision_receipt"
        ).fetchone()
        return int(row["count"])
