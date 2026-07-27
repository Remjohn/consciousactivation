"""Command Bus implementation for TS-CMF-001."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import UUID

from ccp_studio.contracts.commands import (
    CommandEnvelope,
    CommandResult,
    CommandStatus,
    ValidationResult,
)
from ccp_studio.contracts.events import DomainEventEnvelope, new_domain_event
from ccp_studio.contracts.receipts import new_audit_receipt
from ccp_studio.repositories.command_log import (
    InMemoryAuditReceiptRepository,
    InMemoryBrandRepository,
    InMemoryCommandLogRepository,
    InMemoryDomainEventOutbox,
    InMemoryIdempotencyRepository,
)


VALIDATION_ORDER = [
    "SCHEMA_VERSION",
    "AUTHENTICATION",
    "ROLE_PERMISSION",
    "BRAND_SCOPE",
    "OBJECT_EXISTENCE",
    "STATE_TRANSITION",
    "CONSENT_POLICY",
    "COST_QUOTA_POLICY",
    "IDEMPOTENCY",
    "PROVIDER_POLICY",
    "HUMAN_CONFIRMATION",
    "RECEIPT_WRITER_READY",
]


class CommandHandler(Protocol):
    command_type: str
    aggregate_type: str
    allowed_roles: set[str]
    requires_existing_brand_scope: bool

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        ...

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        ...


class CommandValidationError(Exception):
    def __init__(self, result: ValidationResult):
        self.result = result
        super().__init__(result.message)


@dataclass
class ReferenceCommandHandler:
    """Small handler used for foundation commands and tests."""

    command_type: str
    aggregate_type: str = "command"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        return {
            "handled": True,
            "command_type": envelope.command_type,
            "payload": envelope.payload,
        }

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("aggregate_id")
        if isinstance(raw, UUID):
            return raw
        if isinstance(raw, str):
            return UUID(raw)
        return envelope.brand_id


@dataclass
class CommandBus:
    command_log: InMemoryCommandLogRepository
    event_outbox: InMemoryDomainEventOutbox
    audit_receipts: InMemoryAuditReceiptRepository
    idempotency: InMemoryIdempotencyRepository
    brands: InMemoryBrandRepository
    handlers: dict[str, CommandHandler] = field(default_factory=dict)
    permission_policy: Any | None = None
    consent_policy: Any | None = None
    commercial_policy: Any | None = None

    def register_handler(self, handler: CommandHandler) -> None:
        self.handlers[handler.command_type] = handler

    def submit(self, envelope: CommandEnvelope) -> CommandResult:
        validation_results: list[ValidationResult] = []

        try:
            self._run_pre_idempotency_validations(envelope, validation_results)
        except CommandValidationError as exc:
            validation_results.append(exc.result)
            return self._reject(envelope, validation_results)

        prior = self.idempotency.get(
            envelope.organization_id,
            envelope.brand_id,
            envelope.idempotency_key,
        )
        if prior is not None:
            replay_checks = validation_results + [
                ValidationResult(
                    passed=True,
                    code="IDEMPOTENCY_REPLAYED",
                    message="Duplicate idempotency key returned the prior command result.",
                    evidence={"original_status": prior.status.value},
                )
            ]
            return CommandResult(
                command_id=envelope.command_id,
                status=CommandStatus.replayed,
                result_payload=prior.result_payload,
                validation_results=replay_checks,
                domain_event_id=prior.domain_event_id,
                audit_receipt_id=prior.audit_receipt_id,
            )

        validation_results.append(self._pass("IDEMPOTENCY", "No prior command for idempotency key."))

        try:
            self._run_pre_execution_validations(envelope, validation_results)
        except CommandValidationError as exc:
            validation_results.append(exc.result)
            return self._reject(envelope, validation_results)

        handler = self.handlers.get(envelope.command_type)
        if handler is None:
            return self._reject(
                envelope,
                validation_results
                + [
                    ValidationResult(
                        passed=False,
                        code="COMMAND_HANDLER_NOT_REGISTERED",
                        message=f"No handler registered for {envelope.command_type}.",
                    )
                ],
            )

        try:
            payload = handler.handle(envelope)
            event = self._record_event(envelope, handler, payload)
            result = CommandResult(
                command_id=envelope.command_id,
                status=CommandStatus.succeeded,
                result_payload=payload,
                validation_results=validation_results,
                domain_event_id=event.event_id,
            )
            receipt = new_audit_receipt(
                command_id=envelope.command_id,
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                actor_id=envelope.actor.actor_id,
                action=envelope.command_type,
                status=result.status,
                policy_checks=validation_results,
                event_id=event.event_id,
                evidence_refs=[f"domain_event:{event.event_id}"],
            )
            self.audit_receipts.append(receipt)
            result.audit_receipt_id = receipt.receipt_id
            self.command_log.put(envelope, result)
            self.idempotency.put(
                envelope.organization_id,
                envelope.brand_id,
                envelope.idempotency_key,
                result,
            )
            return result
        except Exception as exc:
            failure = CommandResult(
                command_id=envelope.command_id,
                status=CommandStatus.failed,
                result_payload={"error": str(exc)},
                validation_results=validation_results,
            )
            self.command_log.put(envelope, failure)
            return failure

    def _run_pre_idempotency_validations(
        self,
        envelope: CommandEnvelope,
        results: list[ValidationResult],
    ) -> None:
        results.append(self._pass("SCHEMA_VERSION", "Command schema version accepted."))

        if not envelope.actor.actor_id:
            raise CommandValidationError(
                ValidationResult(
                    passed=False,
                    code="AUTHENTICATION_REQUIRED",
                    message="Actor context is missing actor_id.",
                )
            )
        results.append(self._pass("AUTHENTICATION", "Actor context present."))

        handler = self.handlers.get(envelope.command_type)
        if self.permission_policy is not None:
            decision = self.permission_policy.evaluate(
                actor_id=envelope.actor.actor_id,
                command_type=envelope.command_type,
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                source_surface=envelope.source_surface,
            )
            if not decision.allowed:
                raise CommandValidationError(
                    ValidationResult(
                        passed=False,
                        code=decision.decision_code,
                        message="Actor lacks permission for this command.",
                        evidence={
                            "matched_role_assignment_ids": [
                                str(item) for item in decision.matched_role_assignment_ids
                            ]
                        },
                    )
                )
            results.append(
                ValidationResult(
                    passed=True,
                    code="ROLE_PERMISSION",
                    message="Actor role accepted by permission policy.",
                    evidence={
                        "matched_role_assignment_ids": [
                            str(item) for item in decision.matched_role_assignment_ids
                        ]
                    },
                )
            )
        else:
            allowed_roles = handler.allowed_roles if handler else {"owner", "admin", "operator"}
            if not set(envelope.actor.role_ids).intersection(allowed_roles):
                raise CommandValidationError(
                    ValidationResult(
                        passed=False,
                        code="ROLE_PERMISSION_DENIED",
                        message="Actor lacks a role allowed to submit this command.",
                        evidence={"required_any": sorted(allowed_roles)},
                    )
                )
            results.append(self._pass("ROLE_PERMISSION", "Actor role accepted."))

        requires_existing_scope = (
            handler.requires_existing_brand_scope if handler else True
        )
        if requires_existing_scope and not self.brands.contains_scope(envelope.organization_id, envelope.brand_id):
            raise CommandValidationError(
                ValidationResult(
                    passed=False,
                    code="BRAND_SCOPE_VIOLATION",
                    message="Command organization_id and brand_id are not an active known scope.",
                )
            )
        results.append(
            self._pass(
                "BRAND_SCOPE",
                "Organization and brand scope accepted."
                if requires_existing_scope
                else "Brand scope creation command accepted.",
            )
        )

        results.append(self._pass("OBJECT_EXISTENCE", "Object existence deferred to registered handler."))
        results.append(self._pass("STATE_TRANSITION", "State transition deferred to registered handler."))
        if self.consent_policy is not None:
            decision = self.consent_policy.evaluate_command(envelope)
            if not decision.allowed:
                raise CommandValidationError(
                    ValidationResult(
                        passed=False,
                        code=decision.decision_code,
                        message="Consent policy blocked this command.",
                        evidence={
                            "consent_record_version_id": str(decision.consent_record_version_id)
                            if decision.consent_record_version_id
                            else None,
                            "blocked_scope": decision.blocked_scope,
                        },
                    )
                )
            results.append(
                ValidationResult(
                    passed=True,
                    code="CONSENT_POLICY",
                    message="Consent policy accepted this command.",
                    evidence={
                        "decision_code": decision.decision_code,
                        "consent_record_version_id": str(decision.consent_record_version_id)
                        if decision.consent_record_version_id
                        else None,
                    },
                )
            )
        else:
            results.append(self._pass("CONSENT_POLICY", "No consent blocker registered for this command."))
        if self.commercial_policy is not None:
            decision = self.commercial_policy.evaluate_command(envelope)
            if not decision.allowed:
                raise CommandValidationError(
                    ValidationResult(
                        passed=False,
                        code=decision.decision_code,
                        message="Commercial policy blocked this command.",
                        evidence={
                            "entitlement_id": str(decision.entitlement_id)
                            if decision.entitlement_id
                            else None,
                            "estimated_cost_cents": decision.estimated_cost_cents,
                        },
                    )
                )
            results.append(
                ValidationResult(
                    passed=True,
                    code="COST_QUOTA_POLICY",
                    message="Commercial policy accepted this command.",
                    evidence={
                        "decision_code": decision.decision_code,
                        "entitlement_id": str(decision.entitlement_id)
                        if decision.entitlement_id
                        else None,
                    },
                )
            )
        else:
            results.append(self._pass("COST_QUOTA_POLICY", "No cost/quota blocker registered for this command."))

    def _run_pre_execution_validations(
        self,
        envelope: CommandEnvelope,
        results: list[ValidationResult],
    ) -> None:
        results.append(self._pass("PROVIDER_POLICY", "No provider policy applies to this command."))

        if envelope.payload.get("requires_human_confirmation") and not envelope.payload.get("confirmed_by_human"):
            raise CommandValidationError(
                ValidationResult(
                    passed=False,
                    code="HUMAN_CONFIRMATION_REQUIRED",
                    message="Command requires human confirmation before handler execution.",
                )
            )
        results.append(self._pass("HUMAN_CONFIRMATION", "Human confirmation not required or present."))

        if not self.audit_receipts.is_ready():
            raise CommandValidationError(
                ValidationResult(
                    passed=False,
                    code="RECEIPT_WRITER_UNAVAILABLE",
                    message="Audit receipt writer is unavailable.",
                )
            )
        results.append(self._pass("RECEIPT_WRITER_READY", "Audit receipt writer is ready."))

    def _record_event(
        self,
        envelope: CommandEnvelope,
        handler: CommandHandler,
        payload: dict[str, Any],
    ) -> DomainEventEnvelope:
        event = new_domain_event(
            event_type=f"{envelope.command_type}.succeeded",
            organization_id=envelope.organization_id,
            brand_id=envelope.brand_id,
            command_id=envelope.command_id,
            correlation_id=envelope.correlation_id,
            aggregate_type=handler.aggregate_type,
            aggregate_id=handler.aggregate_id(envelope, payload),
            payload=payload,
        )
        self.event_outbox.append(event)
        return event

    def _reject(
        self,
        envelope: CommandEnvelope,
        validation_results: list[ValidationResult],
    ) -> CommandResult:
        result = CommandResult(
            command_id=envelope.command_id,
            status=CommandStatus.rejected,
            result_payload={},
            validation_results=validation_results,
        )
        receipt = new_audit_receipt(
            command_id=envelope.command_id,
            organization_id=envelope.organization_id,
            brand_id=envelope.brand_id,
            actor_id=envelope.actor.actor_id,
            action=envelope.command_type,
            status=result.status,
            policy_checks=validation_results,
            evidence_refs=["command_rejected_before_handler"],
        )
        try:
            self.audit_receipts.append(receipt)
            result.audit_receipt_id = receipt.receipt_id
        except RuntimeError as exc:
            result.result_payload["audit_receipt_error"] = str(exc)
        self.command_log.put(envelope, result)
        return result

    @staticmethod
    def _pass(code: str, message: str) -> ValidationResult:
        return ValidationResult(passed=True, code=code, message=message)


def create_in_memory_command_bus() -> CommandBus:
    bus = CommandBus(
        command_log=InMemoryCommandLogRepository(),
        event_outbox=InMemoryDomainEventOutbox(),
        audit_receipts=InMemoryAuditReceiptRepository(),
        idempotency=InMemoryIdempotencyRepository(),
        brands=InMemoryBrandRepository(),
    )
    bus.register_handler(ReferenceCommandHandler("SwitchActiveBrandCommand", "brand"))
    bus.register_handler(ReferenceCommandHandler("RecordConsentCommand", "consent"))
    bus.register_handler(ReferenceCommandHandler("SubmitCommand", "command"))
    return bus
