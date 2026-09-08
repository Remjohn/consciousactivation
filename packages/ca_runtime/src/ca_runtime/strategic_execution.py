"""
CA-M007 — Activative Strategic Execution Object.

The StrategicExecutionPayload is a derived, fail-closed execution object. It
cannot be created from a raw topic or an unapproved hypothesis. Admission
requires the exact upstream convergence chain already established by the
canonical convergence gate:

    Guest Genesis + Audience Tensions -> ConvergenceReceipt -> Strategic Execution

A StrategicExecutionPayload also requires a signed operator intent. The
repository's existing CAE receipt/signature convention is deterministic
SHA-256 content addressing, so operator intent uses the same convention: the
signature is the SHA-256 digest of the exact canonical intent fields with the
signature field excluded. Any post-signature mutation therefore invalidates
admission.

This module intentionally does not persist or mutate upstream artifacts. It
stores immutable references to their exact revisions/digests and the exact
convergence receipt. Downstream callers can re-validate the ancestry before
execution.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional

from ca_contracts import canonical_sha256, utc_now_rfc3339

from .convergence_gate import (
    AudienceTensionsRef,
    ConvergenceReceipt,
    ConvergenceStatus,
    GuestGenesisRef,
)


PROGRAM_ID = "activative_strategic_execution"
PROGRAM_VERSION = "1.0.0"
INVARIANT_ID = "FR-007 / INV-ACT-001"
SIGNATURE_PREFIX = "SIG-OPERATOR-"


class StrategicExecutionError(RuntimeError):
    """Base error for CA-M007 Strategic Execution admission violations."""


class MissingLineageError(StrategicExecutionError):
    """Raised when one or more required upstream ancestry links are absent."""


class InvalidLineageError(StrategicExecutionError):
    """Raised when lineage exists but is incomplete, stale, or inconsistent."""


class InvalidOperatorIntentError(StrategicExecutionError):
    """Raised when signed operator intent is absent, malformed, or invalid."""


class RawTopicInsertionError(StrategicExecutionError):
    """Raised when a caller attempts to instantiate execution from a raw topic."""


class CrossWorkspaceStrategicExecutionError(StrategicExecutionError):
    """Raised when an execution object crosses a workspace boundary."""


class StaleConvergenceReceiptError(InvalidLineageError):
    """Raised when a convergence receipt no longer matches current upstream refs."""


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value


def _require_sha256(value: str, field_name: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise ValueError(f"{field_name} must be a 64-character SHA-256 hex digest")
    try:
        int(value, 16)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be hexadecimal") from exc
    return value


def _require_revision(value: str, field_name: str) -> str:
    return _require_non_empty(value, field_name)


def _intent_signature_payload(
    *,
    workspace_id: str,
    intent_id: str,
    operator_id: str,
    action: str,
    rationale: str,
    target_execution_id: str,
    signed_at_utc: str,
) -> dict[str, str]:
    return {
        "schema": "CA-M007.operator-intent.v1",
        "workspace_id": workspace_id,
        "intent_id": intent_id,
        "operator_id": operator_id,
        "action": action,
        "rationale": rationale,
        "target_execution_id": target_execution_id,
        "signed_at_utc": signed_at_utc,
    }


def _execution_digest_payload(
    *,
    execution_id: str,
    workspace_id: str,
    strategic_objective: str,
    transformation_vector: Mapping[str, Any],
    genesis: "LineageRef",
    tensions: "LineageRef",
    convergence: "ConvergenceLineageRef",
    operator_intent: "OperatorIntent",
) -> dict[str, Any]:
    return {
        "schema": "CA-M007.strategic-execution.v1",
        "program_id": PROGRAM_ID,
        "program_version": PROGRAM_VERSION,
        "execution_id": execution_id,
        "workspace_id": workspace_id,
        "strategic_objective": strategic_objective,
        "transformation_vector": dict(transformation_vector),
        "genesis": genesis.to_dict(),
        "tensions": tensions.to_dict(),
        "convergence": convergence.to_dict(),
        "operator_intent": operator_intent.to_dict(include_signature=True),
    }


@dataclass(frozen=True, slots=True)
class LineageRef:
    """Immutable identity/revision/digest reference to an upstream artifact."""

    object_id: str
    revision_id: str
    sha256_digest: str

    def __post_init__(self) -> None:
        _require_non_empty(self.object_id, "object_id")
        _require_revision(self.revision_id, "revision_id")
        _require_sha256(self.sha256_digest, "sha256_digest")

    def to_dict(self) -> dict[str, str]:
        return {
            "object_id": self.object_id,
            "revision_id": self.revision_id,
            "sha256_digest": self.sha256_digest,
        }


@dataclass(frozen=True, slots=True)
class ConvergenceLineageRef:
    """Exact convergence receipt reference embedded in the execution ancestry."""

    receipt_id: str
    workspace_id: str
    status: str
    convergence_digest: str
    convergence_signature: str
    gate_version: str
    guest_genesis_revision_id: str
    guest_genesis_sha256: str
    audience_tensions_revision_id: str
    audience_tensions_sha256: str

    @classmethod
    def from_receipt(cls, receipt: ConvergenceReceipt) -> "ConvergenceLineageRef":
        if not isinstance(receipt, ConvergenceReceipt):
            raise TypeError("receipt must be a ConvergenceReceipt")
        return cls(
            receipt_id=_require_non_empty(receipt.receipt_id, "receipt_id"),
            workspace_id=_require_non_empty(receipt.workspace_id, "workspace_id"),
            status=receipt.status.value if isinstance(receipt.status, ConvergenceStatus) else str(receipt.status),
            convergence_digest=_require_sha256(receipt.convergence_digest, "convergence_digest"),
            convergence_signature=_require_non_empty(receipt.convergence_signature, "convergence_signature"),
            gate_version=_require_non_empty(receipt.gate_version, "gate_version"),
            guest_genesis_revision_id=_require_revision(receipt.guest_genesis_revision_id, "guest_genesis_revision_id"),
            guest_genesis_sha256=_require_sha256(receipt.guest_genesis_sha256, "guest_genesis_sha256"),
            audience_tensions_revision_id=_require_revision(receipt.audience_tensions_revision_id, "audience_tensions_revision_id"),
            audience_tensions_sha256=_require_sha256(receipt.audience_tensions_sha256, "audience_tensions_sha256"),
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "receipt_id": self.receipt_id,
            "workspace_id": self.workspace_id,
            "status": self.status,
            "convergence_digest": self.convergence_digest,
            "convergence_signature": self.convergence_signature,
            "gate_version": self.gate_version,
            "guest_genesis_revision_id": self.guest_genesis_revision_id,
            "guest_genesis_sha256": self.guest_genesis_sha256,
            "audience_tensions_revision_id": self.audience_tensions_revision_id,
            "audience_tensions_sha256": self.audience_tensions_sha256,
        }


@dataclass(frozen=True, slots=True)
class OperatorIntent:
    """Immutable signed human intent authorizing a specific execution object."""

    intent_id: str
    workspace_id: str
    operator_id: str
    action: str
    rationale: str
    target_execution_id: str
    signed_at_utc: str
    signature_sha256: str

    @classmethod
    def sign(
        cls,
        *,
        intent_id: str,
        workspace_id: str,
        operator_id: str,
        action: str,
        rationale: str,
        target_execution_id: str,
        signed_at_utc: Optional[str] = None,
    ) -> "OperatorIntent":
        workspace_id = _require_non_empty(workspace_id, "workspace_id")
        intent_id = _require_non_empty(intent_id, "intent_id")
        operator_id = _require_non_empty(operator_id, "operator_id")
        action = _require_non_empty(action, "action")
        rationale = _require_non_empty(rationale, "rationale")
        target_execution_id = _require_non_empty(target_execution_id, "target_execution_id")
        signed_at_utc = _require_non_empty(signed_at_utc or utc_now_rfc3339(), "signed_at_utc")
        signature_sha256 = canonical_sha256(
            _intent_signature_payload(
                workspace_id=workspace_id,
                intent_id=intent_id,
                operator_id=operator_id,
                action=action,
                rationale=rationale,
                target_execution_id=target_execution_id,
                signed_at_utc=signed_at_utc,
            )
        )
        return cls(
            intent_id=intent_id,
            workspace_id=workspace_id,
            operator_id=operator_id,
            action=action,
            rationale=rationale,
            target_execution_id=target_execution_id,
            signed_at_utc=signed_at_utc,
            signature_sha256=f"{SIGNATURE_PREFIX}{signature_sha256}",
        )

    def to_dict(self, *, include_signature: bool = True) -> dict[str, str]:
        result = _intent_signature_payload(
            workspace_id=self.workspace_id,
            intent_id=self.intent_id,
            operator_id=self.operator_id,
            action=self.action,
            rationale=self.rationale,
            target_execution_id=self.target_execution_id,
            signed_at_utc=self.signed_at_utc,
        )
        if include_signature:
            result["signature_sha256"] = self.signature_sha256
        return result

    def verify(self) -> bool:
        if not isinstance(self.signature_sha256, str) or not self.signature_sha256.startswith(SIGNATURE_PREFIX):
            return False
        actual = self.signature_sha256[len(SIGNATURE_PREFIX) :]
        expected = canonical_sha256(
            _intent_signature_payload(
                workspace_id=self.workspace_id,
                intent_id=self.intent_id,
                operator_id=self.operator_id,
                action=self.action,
                rationale=self.rationale,
                target_execution_id=self.target_execution_id,
                signed_at_utc=self.signed_at_utc,
            )
        )
        return actual == expected


@dataclass(frozen=True, slots=True)
class StrategicExecutionPayload:
    """Derived strategic execution object with complete upstream ancestry."""

    execution_id: str
    workspace_id: str
    strategic_objective: str
    transformation_vector: Mapping[str, Any]
    genesis: LineageRef
    tensions: LineageRef
    convergence: ConvergenceLineageRef
    operator_intent: OperatorIntent
    payload_sha256: str
    created_at: str
    program_id: str = PROGRAM_ID
    program_version: str = PROGRAM_VERSION
    invariant_id: str = INVARIANT_ID

    @classmethod
    def derive(
        cls,
        *,
        execution_id: str,
        workspace_id: str,
        strategic_objective: str,
        transformation_vector: Mapping[str, Any],
        genesis: GuestGenesisRef,
        tensions: AudienceTensionsRef,
        convergence_receipt: ConvergenceReceipt,
        operator_intent: OperatorIntent,
    ) -> "StrategicExecutionPayload":
        if not strategic_objective or not strategic_objective.strip():
            raise ValueError("strategic_objective must be non-empty")
        if not isinstance(transformation_vector, Mapping) or not transformation_vector:
            raise ValueError("transformation_vector must be a non-empty mapping")
        if not isinstance(genesis, GuestGenesisRef):
            raise MissingLineageError("Guest Genesis ancestry is required")
        if not isinstance(tensions, AudienceTensionsRef):
            raise MissingLineageError("Audience Tensions ancestry is required")
        if not isinstance(convergence_receipt, ConvergenceReceipt):
            raise MissingLineageError("Convergence receipt ancestry is required")
        if not isinstance(operator_intent, OperatorIntent):
            raise InvalidOperatorIntentError("signed operator intent is required")

        workspace_id = _require_non_empty(workspace_id, "workspace_id")
        execution_id = _require_non_empty(execution_id, "execution_id")
        strategic_objective = strategic_objective.strip()

        if genesis.workspace_id != workspace_id:
            raise CrossWorkspaceStrategicExecutionError(
                f"Guest Genesis workspace '{genesis.workspace_id}' does not match '{workspace_id}'"
            )
        if tensions.workspace_id != workspace_id:
            raise CrossWorkspaceStrategicExecutionError(
                f"Audience Tensions workspace '{tensions.workspace_id}' does not match '{workspace_id}'"
            )
        if convergence_receipt.workspace_id != workspace_id:
            raise CrossWorkspaceStrategicExecutionError(
                f"Convergence receipt workspace '{convergence_receipt.workspace_id}' does not match '{workspace_id}'"
            )
        if operator_intent.workspace_id != workspace_id:
            raise CrossWorkspaceStrategicExecutionError(
                f"Operator intent workspace '{operator_intent.workspace_id}' does not match '{workspace_id}'"
            )
        if operator_intent.target_execution_id != execution_id:
            raise InvalidOperatorIntentError(
                "operator intent is not signed for this execution_id"
            )
        if not operator_intent.verify():
            raise InvalidOperatorIntentError("operator intent signature is invalid")

        if convergence_receipt.status != ConvergenceStatus.CONVERGED:
            raise InvalidLineageError(
                f"convergence receipt must be CONVERGED, got '{convergence_receipt.status}'"
            )
        try:
            convergence_receipt.validate_upstream_digests(genesis, tensions)
        except Exception as exc:
            raise StaleConvergenceReceiptError(
                "convergence receipt does not match the exact supplied upstream artifact digests"
            ) from exc

        if convergence_receipt.guest_genesis_revision_id != genesis.revision_id:
            raise InvalidLineageError("convergence receipt Guest Genesis revision does not match")
        if convergence_receipt.audience_tensions_revision_id != tensions.revision_id:
            raise InvalidLineageError("convergence receipt Audience Tensions revision does not match")

        genesis_ref = LineageRef(
            object_id=genesis.territory_id,
            revision_id=genesis.revision_id,
            sha256_digest=genesis.sha256_digest,
        )
        tensions_ref = LineageRef(
            object_id=tensions.audience_id,
            revision_id=tensions.revision_id,
            sha256_digest=tensions.sha256_digest,
        )
        convergence_ref = ConvergenceLineageRef.from_receipt(convergence_receipt)

        digest_payload = _execution_digest_payload(
            execution_id=execution_id,
            workspace_id=workspace_id,
            strategic_objective=strategic_objective,
            transformation_vector=transformation_vector,
            genesis=genesis_ref,
            tensions=tensions_ref,
            convergence=convergence_ref,
            operator_intent=operator_intent,
        )
        payload_sha256 = canonical_sha256(digest_payload)

        return cls(
            execution_id=execution_id,
            workspace_id=workspace_id,
            strategic_objective=strategic_objective,
            transformation_vector=dict(transformation_vector),
            genesis=genesis_ref,
            tensions=tensions_ref,
            convergence=convergence_ref,
            operator_intent=operator_intent,
            payload_sha256=payload_sha256,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    @classmethod
    def from_raw_topic(cls, *, topic: str, **_: Any) -> "StrategicExecutionPayload":
        """Explicitly prohibited compatibility surface for raw-topic insertion."""
        raise RawTopicInsertionError(
            "StrategicExecutionPayload cannot be instantiated from a raw topic; "
            "derive it from an approved ConvergenceReceipt and signed OperatorIntent"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "workspace_id": self.workspace_id,
            "strategic_objective": self.strategic_objective,
            "transformation_vector": dict(self.transformation_vector),
            "genesis": self.genesis.to_dict(),
            "tensions": self.tensions.to_dict(),
            "convergence": self.convergence.to_dict(),
            "operator_intent": self.operator_intent.to_dict(include_signature=True),
            "payload_sha256": self.payload_sha256,
            "created_at": self.created_at,
            "program_id": self.program_id,
            "program_version": self.program_version,
            "invariant_id": self.invariant_id,
        }

    def verify_integrity(
        self,
        *,
        genesis: GuestGenesisRef,
        tensions: AudienceTensionsRef,
        convergence_receipt: ConvergenceReceipt,
    ) -> None:
        """Re-verify exact ancestry and content address before downstream use."""
        if not self.operator_intent.verify():
            raise InvalidOperatorIntentError("stored operator intent signature is invalid")
        if self.operator_intent.target_execution_id != self.execution_id:
            raise InvalidOperatorIntentError("stored operator intent targets a different execution")
        if self.workspace_id != genesis.workspace_id or self.workspace_id != tensions.workspace_id:
            raise CrossWorkspaceStrategicExecutionError("upstream refs are not workspace aligned")
        if convergence_receipt.workspace_id != self.workspace_id:
            raise CrossWorkspaceStrategicExecutionError("convergence receipt workspace mismatch")
        if convergence_receipt.status != ConvergenceStatus.CONVERGED:
            raise InvalidLineageError("stored convergence lineage is not converged")

        if self.genesis != LineageRef(genesis.territory_id, genesis.revision_id, genesis.sha256_digest):
            raise StaleConvergenceReceiptError("Guest Genesis lineage changed")
        if self.tensions != LineageRef(tensions.audience_id, tensions.revision_id, tensions.sha256_digest):
            raise StaleConvergenceReceiptError("Audience Tensions lineage changed")

        current_convergence = ConvergenceLineageRef.from_receipt(convergence_receipt)
        if current_convergence != self.convergence:
            raise StaleConvergenceReceiptError("Convergence receipt lineage changed")

        try:
            convergence_receipt.validate_upstream_digests(genesis, tensions)
        except Exception as exc:
            raise StaleConvergenceReceiptError(
                "convergence receipt no longer matches upstream digests"
            ) from exc

        expected_payload_sha256 = canonical_sha256(
            _execution_digest_payload(
                execution_id=self.execution_id,
                workspace_id=self.workspace_id,
                strategic_objective=self.strategic_objective,
                transformation_vector=self.transformation_vector,
                genesis=self.genesis,
                tensions=self.tensions,
                convergence=self.convergence,
                operator_intent=self.operator_intent,
            )
        )
        if self.payload_sha256 != expected_payload_sha256:
            raise InvalidLineageError("Strategic Execution payload digest does not match its content")


def require_admitted_strategic_execution(
    payload: StrategicExecutionPayload,
    *,
    genesis: GuestGenesisRef,
    tensions: AudienceTensionsRef,
    convergence_receipt: ConvergenceReceipt,
) -> StrategicExecutionPayload:
    """Fail-closed downstream admission helper."""
    if not isinstance(payload, StrategicExecutionPayload):
        raise StrategicExecutionError("downstream admission requires a StrategicExecutionPayload")
    payload.verify_integrity(
        genesis=genesis,
        tensions=tensions,
        convergence_receipt=convergence_receipt,
    )
    return payload
