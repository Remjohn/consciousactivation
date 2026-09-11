"""Transport-neutral Stage 5 reference protocol engine.

This module interprets the released contract candidate. It deliberately owns no
transport, production asset generation, workflow orchestration, or product UI.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from datetime import datetime, timezone
from typing import Any

from cmf_delegation_validators.authority import AuthorityError, validate_authority
from cmf_delegation_validators.canonical import canonical_hash
from cmf_delegation_validators.compatibility import (
    CONSTITUTIONAL_DOMAINS,
    CompatibilityError,
    negotiate,
)
from cmf_delegation_validators.contracts import (
    ContractError,
    registry_entry,
    validate_payload,
)
from cmf_delegation_validators.lifecycle import LifecycleError, transition
from jsonschema import ValidationError

from .clock import SystemClock
from .errors import ProtocolRejection
from .models import (
    AuditRecord,
    CorrelationRecord,
    DelegationSetRecord,
    IdempotencyRecord,
    OutboxEntry,
    ProcessingResult,
    ReplayRecord,
    StoredDecision,
)
from .ports import Clock, SignatureVerifier
from .store import InMemoryProtocolStore


PROTOCOL_VERSION = "1.0"
PROTOCOL_PRINCIPAL = "DELEGATION_PROTOCOL"


def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _identity_key(value: dict[str, Any]) -> tuple[str, int, str]:
    return (value["request_id"], value["version"], value["payload_hash"])


class ProtocolEngine:
    """Deterministic reference interpreter over the 1.1.0-rc.2 contract package."""

    def __init__(
        self,
        *,
        signature_verifier: SignatureVerifier,
        store: InMemoryProtocolStore | None = None,
        clock: Clock | None = None,
        recipient_type: str = PROTOCOL_PRINCIPAL,
    ) -> None:
        self.signature_verifier = signature_verifier
        self.store = store or InMemoryProtocolStore()
        self.clock = clock or SystemClock()
        self.recipient_type = recipient_type

    def pin_compatibility(
        self,
        correlation_id: str,
        requester: dict[str, Any],
        provider: dict[str, Any],
    ) -> dict[str, Any]:
        existing = self.store.correlation_copy(correlation_id).compatibility_profile
        if existing is not None:
            try:
                candidate = negotiate(requester, provider)
            except CompatibilityError as exc:
                raise ProtocolRejection(
                    "COMPATIBILITY_PROFILE_IMMUTABLE",
                    "compatibility",
                    "Compatibility profile is already pinned for this correlation",
                ) from exc
            if candidate != existing:
                raise ProtocolRejection(
                    "COMPATIBILITY_PROFILE_IMMUTABLE",
                    "compatibility",
                    "Compatibility profile is already pinned for this correlation",
                )
            return deepcopy(existing)
        try:
            profile = negotiate(requester, provider)
        except CompatibilityError as exc:
            raise ProtocolRejection(
                "COMPATIBILITY_NEGOTIATION_FAILED", "compatibility", str(exc)
            ) from exc
        try:
            self.store.pin_compatibility(correlation_id, profile)
        except ValueError as exc:
            raise ProtocolRejection(
                "COMPATIBILITY_PROFILE_IMMUTABLE", "compatibility", str(exc)
            ) from exc
        return deepcopy(profile)

    def process(self, envelope: dict[str, Any], payload: Any) -> ProcessingResult:
        fingerprint = canonical_hash({"envelope": envelope, "payload": payload})
        payload_hash = canonical_hash(payload)
        try:
            self._validate_preflight(envelope, payload, payload_hash)
        except ProtocolRejection as rejection:
            return self._record_rejection(
                envelope, payload_hash, fingerprint, rejection, replay_conflict=False
            )

        with self.store.locked():
            message_id = envelope["message_id"]
            existing_message = self.store.message(message_id)
            if existing_message is not None:
                if existing_message.fingerprint == fingerprint:
                    return replace(existing_message.result, idempotent=True)
                return self._record_rejection_locked(
                    envelope,
                    payload_hash,
                    fingerprint,
                    ProtocolRejection(
                        "PROTOCOL_REPLAY_DETECTED",
                        "replay",
                        "Message ID was reused with different signed bytes",
                    ),
                    replay_conflict=True,
                    preserve_idempotency=True,
                )

            nonce_key = self._nonce_key(envelope)
            existing_nonce = self.store.nonce(nonce_key)
            if existing_nonce is not None:
                if existing_nonce.fingerprint == fingerprint:
                    return replace(existing_nonce.result, idempotent=True)
                return self._record_rejection_locked(
                    envelope,
                    payload_hash,
                    fingerprint,
                    ProtocolRejection(
                        "PROTOCOL_REPLAY_DETECTED",
                        "replay",
                        "Signer nonce was reused with different signed bytes",
                    ),
                    replay_conflict=True,
                    preserve_idempotency=True,
                )

            idempotency_key = self._idempotency_key(envelope)
            if idempotency_key is not None:
                existing_idempotency = self.store.idempotency(idempotency_key)
                if existing_idempotency is not None:
                    if existing_idempotency.fingerprint == fingerprint:
                        return replace(existing_idempotency.result, idempotent=True)
                    return self._record_rejection_locked(
                        envelope,
                        payload_hash,
                        fingerprint,
                        ProtocolRejection(
                            "IDEMPOTENCY_CONFLICT",
                            "idempotency",
                            "Idempotency key was reused for a different message",
                        ),
                        replay_conflict=False,
                        preserve_idempotency=True,
                    )

            correlation = self.store.correlation_copy(envelope["correlation_id"])
            delegation_set: DelegationSetRecord | None = None
            try:
                trigger, delegation_set = self._apply_message(
                    correlation, envelope["message_type"], payload
                )
                lifecycle_changed = False
                if trigger is not None:
                    correlation.state = transition(
                        correlation.state,
                        trigger,
                        envelope["sender"]["principal_type"],
                    )
                    lifecycle_changed = True
            except (ProtocolRejection, LifecycleError) as exc:
                rejection = exc if isinstance(exc, ProtocolRejection) else ProtocolRejection(
                    "ILLEGAL_LIFECYCLE_TRANSITION", "lifecycle", str(exc)
                )
                return self._record_rejection_locked(
                    envelope, payload_hash, fingerprint, rejection, replay_conflict=False
                )

            return self._commit_decision(
                correlation=correlation,
                envelope=envelope,
                payload_hash=payload_hash,
                fingerprint=fingerprint,
                accepted=True,
                code="ACCEPTED",
                schema_verdict="PASS",
                authority_verdict="PASS",
                lifecycle_changed=lifecycle_changed,
                delegation_set=delegation_set,
            )

    def _validate_preflight(
        self, envelope: dict[str, Any], payload: Any, payload_hash: str
    ) -> None:
        try:
            validate_payload("delegation-envelope", envelope)
        except (ValidationError, ContractError) as exc:
            raise ProtocolRejection(
                "ENVELOPE_SCHEMA_INVALID", "schema", str(exc)
            ) from exc
        message_type = envelope["message_type"]
        try:
            entry = registry_entry(message_type)
            validate_payload(message_type, payload)
        except (ValidationError, ContractError) as exc:
            raise ProtocolRejection("PAYLOAD_SCHEMA_INVALID", "schema", str(exc)) from exc
        if envelope["protocol_version"] != PROTOCOL_VERSION:
            raise ProtocolRejection(
                "PROTOCOL_VERSION_UNSUPPORTED", "compatibility", envelope["protocol_version"]
            )
        if envelope["message_version"] != entry["message_version"]:
            raise ProtocolRejection(
                "MESSAGE_VERSION_UNSUPPORTED", "compatibility", envelope["message_version"]
            )
        if envelope["payload_hash"] != payload_hash:
            raise ProtocolRejection(
                "PAYLOAD_HASH_MISMATCH", "integrity", "Canonical payload hash differs"
            )
        if envelope["recipient"]["principal_type"] != self.recipient_type:
            raise ProtocolRejection(
                "RECIPIENT_MISMATCH", "routing", "Envelope is addressed to another principal"
            )
        now = self.clock.now()
        issued_at = _parse_time(envelope["integrity"]["issued_at"])
        expires_at_raw = envelope["integrity"]["expires_at"]
        if issued_at > now:
            raise ProtocolRejection(
                "SIGNATURE_NOT_YET_VALID", "integrity", "issued_at is in the future"
            )
        if expires_at_raw is not None and _parse_time(expires_at_raw) <= now:
            raise ProtocolRejection("SIGNATURE_EXPIRED", "integrity", "expires_at has passed")
        if not self.signature_verifier.verify(envelope, payload):
            raise ProtocolRejection(
                "SIGNATURE_INVALID", "integrity", "Ed25519 verification failed"
            )
        principal_type = envelope["sender"]["principal_type"]
        if envelope["integrity"]["signer"] != envelope["sender"]:
            raise ProtocolRejection(
                "SIGNER_SENDER_MISMATCH", "authority", "Signer must equal sender"
            )
        if envelope["authority"]["principal"] != envelope["sender"]:
            raise ProtocolRejection(
                "AUTHORITY_PRINCIPAL_MISMATCH", "authority", "Authority principal must equal sender"
            )
        try:
            validate_authority(message_type, principal_type, payload)
        except AuthorityError as exc:
            raise ProtocolRejection("AUTHORITY_DENIED", "authority", str(exc)) from exc
        if entry["idempotency"] == "REQUIRED" and envelope["idempotency_key"] is None:
            raise ProtocolRejection(
                "IDEMPOTENCY_KEY_REQUIRED", "idempotency", message_type
            )

    def _apply_message(
        self,
        correlation: CorrelationRecord,
        message_type: str,
        payload: dict[str, Any],
    ) -> tuple[str | None, DelegationSetRecord | None]:
        if message_type == "visual-asset-demand":
            identity = {
                "request_id": payload["request_id"],
                "version": payload["version"],
                "payload_hash": canonical_hash(payload),
                "canonical_ref": (
                    f"cmf-contract://demands/{payload['request_id']}/{payload['version']}"
                ),
            }
            if correlation.demand_identity not in (None, identity):
                raise ProtocolRejection(
                    "DEMAND_IDENTITY_CONFLICT", "domain", "Correlation already pins another demand"
                )
            correlation.demand_identity = identity
            return None, None

        if message_type == "delegation-set":
            return None, self._validate_delegation_set(payload)

        self._validate_embedded_demand(correlation, payload)
        if message_type == "visual-asset-submission":
            if correlation.compatibility_profile is None:
                raise ProtocolRejection(
                    "COMPATIBILITY_PROFILE_REQUIRED",
                    "compatibility",
                    "Pin compatibility before submission",
                )
            self._validate_semantic_compatibility(correlation.compatibility_profile)
            correlation.submission_id = payload["submission_id"]
            return None, None
        if message_type == "submission-validation-receipt":
            if payload["submission_id"] != correlation.submission_id:
                raise ProtocolRejection(
                    "SUBMISSION_ID_MISMATCH", "domain", payload["submission_id"]
                )
            correlation.validation_receipt_id = payload["receipt_id"]
            trigger = (
                "submission_validation_accepted"
                if payload["status"] == "ACCEPTED"
                else "submission_validation_rejected"
            )
            return trigger, None
        if message_type == "admission-receipt":
            if payload["submission_receipt_id"] != correlation.validation_receipt_id:
                raise ProtocolRejection(
                    "VALIDATION_RECEIPT_ID_MISMATCH",
                    "domain",
                    payload["submission_receipt_id"],
                )
            if payload["status"] == "ACCEPTED":
                correlation.execution_id = payload["execution"]["execution_id"]
                return "admission_accepted", None
            return "admission_rejected", None
        if message_type == "visual-asset-event":
            self._validate_execution(correlation, payload["execution"])
            trigger_by_event = {
                "STARTED": "execution_started",
                "REVALIDATION_STARTED": "revalidation_started",
            }
            return trigger_by_event.get(payload["event_type"]), None
        if message_type == "budget-escalation-request":
            self._validate_execution(correlation, payload["execution"])
            correlation.budget_escalation_request_id = payload["request_id"]
            return "budget_escalation_requested", None
        if message_type == "budget-escalation-response":
            if payload["escalation_request_id"] != correlation.budget_escalation_request_id:
                raise ProtocolRejection(
                    "BUDGET_REQUEST_ID_MISMATCH", "domain", payload["escalation_request_id"]
                )
            return (
                "budget_escalation_approved"
                if payload["decision"] == "APPROVED"
                else "budget_escalation_denied"
            ), None
        if message_type == "cancellation-request":
            if correlation.execution_id and payload["execution_id"] != correlation.execution_id:
                raise ProtocolRejection(
                    "EXECUTION_ID_MISMATCH", "domain", payload["execution_id"]
                )
            correlation.cancellation_request_id = payload["request_id"]
            return "cancellation_requested", None
        if message_type == "cancellation-receipt":
            if payload["cancellation_request_id"] != correlation.cancellation_request_id:
                raise ProtocolRejection(
                    "CANCELLATION_REQUEST_ID_MISMATCH",
                    "domain",
                    payload["cancellation_request_id"],
                )
            if payload["status"] == "REJECTED":
                raise ProtocolRejection(
                    "CANCELLATION_REJECTED", "domain", payload.get("reason") or "Rejected"
                )
            return "cancellation_receipted", None
        if message_type == "amendment-proposal":
            self._validate_execution(correlation, payload["execution"])
            correlation.pending_amendment_id = payload["proposal_id"]
            return "amendment_proposed", None
        if message_type == "amendment-response":
            if payload["proposal_id"] != correlation.pending_amendment_id:
                raise ProtocolRejection(
                    "AMENDMENT_PROPOSAL_ID_MISMATCH", "domain", payload["proposal_id"]
                )
            if payload["decision"] == "REJECTED":
                reason = (payload.get("reason") or "").upper()
                return (
                    "amendment_rejected_capability_gap"
                    if "CAPABILITY" in reason
                    else "amendment_rejected_cancelled"
                ), None
            return None, None
        if message_type == "demand-supersession":
            if payload["superseded_demand"] != correlation.demand_identity:
                raise ProtocolRejection(
                    "SUPERSEDED_DEMAND_MISMATCH", "domain", "Old identity is not pinned"
                )
            correlation.successor_demand = deepcopy(payload["replacement_demand"])
            return "demand_superseded", None
        if message_type == "asset-result-contract":
            self._validate_execution(correlation, payload["execution"])
            identity = {
                "result_id": payload["result_id"],
                "version": payload["version"],
                "payload_hash": canonical_hash(payload),
                "canonical_ref": (
                    f"cmf-contract://results/{payload['result_id']}/{payload['version']}"
                ),
            }
            correlation.current_result = identity
            return (
                "result_declared"
                if payload["completion_status"] == "COMPLETE"
                else "partial_result_declared"
            ), None
        if message_type == "result-acknowledgement":
            expected = correlation.pending_replacement or correlation.current_result
            if expected is None or payload["result"] != expected:
                raise ProtocolRejection(
                    "RESULT_IDENTITY_MISMATCH", "domain", "Acknowledged result is not current"
                )
            if correlation.pending_replacement is not None:
                correlation.current_result = correlation.pending_replacement
                correlation.pending_replacement = None
                return "replacement_acknowledged", None
            if correlation.state == "PARTIAL_RESULT_READY":
                partial = {
                    "ACCEPTED": "partial_result_accepted",
                    "ACCEPTED_WITH_CONCERNS": "partial_result_accepted",
                    "REJECTED": "partial_result_rejected",
                }
                return partial[payload["decision"]], None
            return {
                "ACCEPTED": "result_accepted",
                "ACCEPTED_WITH_CONCERNS": "result_accepted_with_concerns",
                "REJECTED": "result_rejected",
            }[payload["decision"]], None
        if message_type == "invalidation-notice":
            self._validate_result(correlation, payload["result"])
            return "result_invalidated", None
        if message_type == "revocation-notice":
            self._validate_result(correlation, payload["result"])
            return "result_revoked", None
        if message_type == "replacement-notice":
            self._validate_result(correlation, payload["replaced_result"])
            correlation.pending_replacement = deepcopy(payload["replacement_result"])
            return None, None
        if message_type == "selective-invalidation-receipt":
            return None, None
        raise ProtocolRejection(
            "MESSAGE_NOT_SUPPORTED_BY_REFERENCE_SLICE", "domain", message_type
        )

    @staticmethod
    def _validate_semantic_compatibility(profile: dict[str, Any]) -> None:
        if profile.get("behavioral_enforcement") != "PASS":
            raise ProtocolRejection(
                "SEMANTIC_ENFORCEMENT_UNSUPPORTED",
                "compatibility",
                "Parsing without behavioral enforcement is incompatible",
            )
        if profile.get("message_versions", {}).get("visual-asset-demand") != "1.1":
            raise ProtocolRejection(
                "MESSAGE_VERSION_UNSUPPORTED",
                "compatibility",
                "Visual Asset Demand 1.1 support is mandatory",
            )
        capabilities = {
            item.get("domain"): item
            for item in profile.get("semantic_capabilities", [])
            if isinstance(item, dict)
        }
        if not CONSTITUTIONAL_DOMAINS.issubset(capabilities):
            raise ProtocolRejection(
                "SEMANTIC_ENFORCEMENT_UNSUPPORTED",
                "compatibility",
                "Constitutional capability evidence is incomplete",
            )
        for domain, capability in capabilities.items():
            if domain not in CONSTITUTIONAL_DOMAINS:
                continue
            modes = set(capability.get("support_modes", []))
            if not {"PRESERVE", "ENFORCE"}.issubset(modes):
                raise ProtocolRejection(
                    "SEMANTIC_ENFORCEMENT_UNSUPPORTED",
                    "compatibility",
                    f"{domain} is not preserved and enforced",
                )
            if "EVALUATE" in modes and not capability.get("evaluator_profile_refs"):
                raise ProtocolRejection(
                    "EVALUATOR_EVIDENCE_MISSING",
                    "compatibility",
                    domain,
                )

    def _validate_embedded_demand(
        self, correlation: CorrelationRecord, payload: dict[str, Any]
    ) -> None:
        candidates: list[dict[str, Any]] = []
        if isinstance(payload.get("demand"), dict):
            candidates.append(payload["demand"])
        if isinstance(payload.get("execution"), dict):
            execution_demand = payload["execution"].get("demand")
            if isinstance(execution_demand, dict):
                candidates.append(execution_demand)
        if correlation.demand_identity is None and candidates:
            raise ProtocolRejection(
                "DEMAND_IDENTITY_REQUIRED", "domain", "Record visual-asset-demand first"
            )
        for candidate in candidates:
            if candidate != correlation.demand_identity:
                raise ProtocolRejection(
                    "DEMAND_IDENTITY_MISMATCH",
                    "domain",
                    "Request ID, version, hash, and canonical ref must all match",
                )

    def _validate_execution(
        self, correlation: CorrelationRecord, execution: dict[str, Any]
    ) -> None:
        if execution["demand"] != correlation.demand_identity:
            raise ProtocolRejection(
                "DEMAND_IDENTITY_MISMATCH", "domain", "Execution demand differs"
            )
        if correlation.execution_id and execution["execution_id"] != correlation.execution_id:
            raise ProtocolRejection(
                "EXECUTION_ID_MISMATCH", "domain", execution["execution_id"]
            )

    def _validate_result(
        self, correlation: CorrelationRecord, result: dict[str, Any]
    ) -> None:
        if correlation.current_result is None or result != correlation.current_result:
            raise ProtocolRejection(
                "RESULT_IDENTITY_MISMATCH", "domain", "Result is not current"
            )

    def _validate_delegation_set(self, payload: dict[str, Any]) -> DelegationSetRecord:
        members = {_identity_key(item) for item in payload["member_demands"]}
        if len(members) != len(payload["member_demands"]):
            raise ProtocolRejection(
                "DELEGATION_SET_DUPLICATE_MEMBER", "domain", payload["set_id"]
            )
        adjacency: dict[tuple[str, int, str], set[tuple[str, int, str]]] = {
            member: set() for member in members
        }
        for edge in payload["dependency_edges"]:
            predecessor = _identity_key(edge["predecessor"])
            successor = _identity_key(edge["successor"])
            if predecessor not in members or successor not in members:
                raise ProtocolRejection(
                    "DELEGATION_SET_EDGE_OUTSIDE_MEMBERS", "domain", payload["set_id"]
                )
            adjacency[predecessor].add(successor)
        visiting: set[tuple[str, int, str]] = set()
        visited: set[tuple[str, int, str]] = set()

        def visit(node: tuple[str, int, str]) -> None:
            if node in visiting:
                raise ProtocolRejection(
                    "DELEGATION_SET_CYCLE", "domain", payload["set_id"]
                )
            if node in visited:
                return
            visiting.add(node)
            for child in adjacency[node]:
                visit(child)
            visiting.remove(node)
            visited.add(node)

        for member in members:
            visit(member)
        return DelegationSetRecord(
            set_id=payload["set_id"],
            version=payload["version"],
            member_demands=tuple(sorted(members)),
            completion_policy=payload["completion_policy"],
            minimum_completed=payload["minimum_completed"],
        )

    def _record_rejection(
        self,
        envelope: dict[str, Any],
        payload_hash: str,
        fingerprint: str,
        rejection: ProtocolRejection,
        *,
        replay_conflict: bool,
    ) -> ProcessingResult:
        with self.store.locked():
            return self._record_rejection_locked(
                envelope, payload_hash, fingerprint, rejection, replay_conflict=replay_conflict
            )

    def _record_rejection_locked(
        self,
        envelope: dict[str, Any],
        payload_hash: str,
        fingerprint: str,
        rejection: ProtocolRejection,
        *,
        replay_conflict: bool,
        preserve_idempotency: bool = False,
    ) -> ProcessingResult:
        correlation_id = envelope.get("correlation_id") or f"invalid-{payload_hash[7:23]}"
        message_id = envelope.get("message_id") or f"invalid-{fingerprint[7:23]}"
        normalized = deepcopy(envelope)
        normalized["correlation_id"] = correlation_id
        normalized["message_id"] = message_id
        normalized.setdefault("message_type", "invalid-message")
        normalized.setdefault("sender", {"principal_type": "CONTROL_TOWER", "principal_id": "invalid"})
        normalized.setdefault("integrity", {"key_id": "invalid", "nonce": fingerprint[7:23]})
        correlation = self.store.correlation_copy(correlation_id)
        existing_message = self.store.message(message_id)
        nonce_key = self._nonce_key(normalized)
        existing_nonce = self.store.nonce(nonce_key)
        idempotency_key = self._idempotency_key(normalized)
        existing_idempotency = (
            self.store.idempotency(idempotency_key) if idempotency_key is not None else None
        )
        return self._commit_decision(
            correlation=correlation,
            envelope=normalized,
            payload_hash=payload_hash,
            fingerprint=fingerprint,
            accepted=False,
            code=rejection.code,
            schema_verdict="FAIL" if rejection.stage == "schema" else "PASS",
            authority_verdict="FAIL" if rejection.stage == "authority" else "PASS",
            lifecycle_changed=False,
            preserve_existing_message=replay_conflict or existing_message is not None,
            preserve_existing_nonce=replay_conflict or existing_nonce is not None,
            preserve_idempotency=preserve_idempotency or existing_idempotency is not None,
        )

    def _commit_decision(
        self,
        *,
        correlation: CorrelationRecord,
        envelope: dict[str, Any],
        payload_hash: str,
        fingerprint: str,
        accepted: bool,
        code: str,
        schema_verdict: str,
        authority_verdict: str,
        lifecycle_changed: bool,
        delegation_set: DelegationSetRecord | None = None,
        preserve_existing_message: bool = False,
        preserve_existing_nonce: bool = False,
        preserve_idempotency: bool = False,
    ) -> ProcessingResult:
        previous_hash = correlation.audit[-1].record_hash if correlation.audit else None
        correlation.audit_sequence += 1
        receipt = {
            "receipt_id": f"audit-{correlation.correlation_id}-{correlation.audit_sequence}",
            "message_id": envelope["message_id"],
            "correlation_id": correlation.correlation_id,
            "payload_hash": payload_hash,
            "previous_receipt_hash": previous_hash,
            "effective_state": correlation.state,
            "authority_verdict": authority_verdict,
            "schema_verdict": schema_verdict,
            "recorded_at": self.clock.now().astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        validate_payload("delegation-audit-receipt", receipt)
        record_hash = canonical_hash(
            {"receipt": receipt, "decision": "ACCEPT" if accepted else "REJECT", "code": code}
        )
        correlation.audit.append(
            AuditRecord(
                receipt=deepcopy(receipt),
                record_hash=record_hash,
                decision="ACCEPT" if accepted else "REJECT",
                code=code,
            )
        )
        outbox_sequence = self.store.next_outbox_sequence()
        result = ProcessingResult(
            accepted=accepted,
            code=code,
            correlation_id=correlation.correlation_id,
            message_id=envelope["message_id"],
            state=correlation.state,
            audit_receipt=deepcopy(receipt),
            audit_hash=record_hash,
            outbox_sequence=outbox_sequence,
            lifecycle_changed=lifecycle_changed,
        )
        decision = StoredDecision(fingerprint=fingerprint, result=result)
        nonce_key = self._nonce_key(envelope)
        replay = ReplayRecord(
            message_id=envelope["message_id"], fingerprint=fingerprint, result=result
        )
        idempotency_key = self._idempotency_key(envelope)
        idempotency_record = None
        if idempotency_key is not None and not preserve_idempotency:
            idempotency_record = IdempotencyRecord(
                message_id=envelope["message_id"],
                payload_hash=payload_hash,
                fingerprint=fingerprint,
                result=result,
            )
        self.store.commit(
            correlation=correlation,
            message_id=envelope["message_id"],
            stored_decision=decision,
            nonce_key=nonce_key,
            replay_record=replay,
            idempotency_key=None if preserve_idempotency else idempotency_key,
            idempotency_record=idempotency_record,
            outbox_entry=OutboxEntry(
                sequence=outbox_sequence,
                correlation_id=correlation.correlation_id,
                message_id=envelope["message_id"],
                kind="ACCEPTED" if accepted else "REJECTED",
                audit_hash=record_hash,
            ),
            delegation_set=delegation_set,
            preserve_existing_message=preserve_existing_message,
            preserve_existing_nonce=preserve_existing_nonce,
        )
        return result

    @staticmethod
    def _nonce_key(envelope: dict[str, Any]) -> tuple[str, str, str]:
        signer = envelope["sender"]
        integrity = envelope["integrity"]
        return (signer["principal_id"], integrity["key_id"], integrity["nonce"])

    @staticmethod
    def _idempotency_key(
        envelope: dict[str, Any],
    ) -> tuple[str, str, str, str] | None:
        key = envelope.get("idempotency_key")
        if key is None:
            return None
        return (
            envelope["sender"]["principal_id"],
            envelope["message_type"],
            envelope["correlation_id"],
            key,
        )
