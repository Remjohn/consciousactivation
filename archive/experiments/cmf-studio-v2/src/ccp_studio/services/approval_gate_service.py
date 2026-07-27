"""Approval gate policy service for TS-CMF-053."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.approval_gate import (
    ApprovalBlockerReceipt,
    ApprovalBlockerSeverity,
    ApprovalGateBlocker,
    ApprovalGateDecision,
    ApprovalGateDomainEvent,
    ApprovalGateInput,
    ApprovalPolicyReport,
    ContentFormatValidation,
    new_approval_blocker_receipt,
)
from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.approval_gate import InMemoryApprovalGateRepository
from ccp_studio.services.command_bus import CommandBus


class ApprovalGateError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ApprovalGateService:
    repository: InMemoryApprovalGateRepository = field(default_factory=InMemoryApprovalGateRepository)
    policy_version: str = "cmf.approval_gate_policy.v1"

    def evaluate_approval_gate(self, gate_input: ApprovalGateInput | dict[str, Any]) -> ApprovalPolicyReport:
        parsed = gate_input if isinstance(gate_input, ApprovalGateInput) else ApprovalGateInput.model_validate(gate_input)
        content_format = self.validate_content_format(
            platform_variant_id=parsed.platform_variant_id,
            format_key=parsed.content_format_key,
            registry_version_id=parsed.content_format_registry_version_id,
            valid_content_formats=parsed.valid_content_formats,
        )
        blockers = self._blockers(parsed, content_format)
        hard = [blocker for blocker in blockers if blocker.severity == ApprovalBlockerSeverity.hard]
        escalations = [blocker for blocker in blockers if blocker.severity == ApprovalBlockerSeverity.escalate]
        decision = (
            ApprovalGateDecision.blocked
            if hard
            else ApprovalGateDecision.escalate
            if escalations
            else ApprovalGateDecision.approved_allowed
        )
        report = ApprovalPolicyReport(
            schema_version="cmf.approval_policy_report.v1",
            approval_policy_report_id=uuid4(),
            approval_request_id=parsed.approval_request_id,
            organization_id=parsed.organization_id,
            brand_id=parsed.brand_id,
            object_type=parsed.object_type,
            object_id=parsed.object_id,
            object_version_hash=parsed.object_version_hash,
            lineage_complete=self._lineage_complete(parsed),
            consent_compatible=parsed.consent_compatible,
            source_truth_passed=parsed.source_truth_passed and not parsed.disputed_source_refs,
            identity_passed=parsed.identity_passed and not parsed.identity_failure_refs,
            evaluation_passed=parsed.evaluation_passed and not parsed.evaluation_hard_failure_codes,
            platform_format_passed=parsed.platform_format_passed and not parsed.platform_blocker_codes,
            content_format_passed=content_format.valid_content_format,
            content_format_validation=content_format,
            blockers=blockers,
            decision=decision,
            policy_version=self.policy_version,
            created_at=utc_now(),
        )
        self.repository.put_report(report)
        receipt = self.repository.put_receipt(new_approval_blocker_receipt(report=report))
        self._event(
            "ApprovalGateEvaluated",
            report,
            {"decision": report.decision.value, "blocker_codes": receipt.blocker_codes},
        )
        if blockers:
            self._event("ApprovalBlocked", report, {"blocker_codes": receipt.blocker_codes})
        self._event("ApprovalBlockerReceiptRecorded", report, {"approval_blocker_receipt_id": str(receipt.approval_blocker_receipt_id)})
        return report

    def validate_content_format(
        self,
        *,
        platform_variant_id: str,
        format_key: str,
        registry_version_id: str,
        valid_content_formats: list[str],
    ) -> ContentFormatValidation:
        validation = ContentFormatValidation(
            schema_version="cmf.content_format_validation.v1",
            platform_variant_id=platform_variant_id,
            format_key=format_key,
            valid_content_format=format_key in valid_content_formats,
            registry_version_id=registry_version_id,
            blocker_code=None if format_key in valid_content_formats else "CONTENT_FORMAT_UNSUPPORTED",
        )
        self.repository.append_event(
            ApprovalGateDomainEvent(
                schema_version="cmf.approval_gate_domain_event.v1",
                approval_gate_event_id=uuid4(),
                event_type="ContentFormatValidated",
                approval_request_id=uuid4(),
                object_type="content_format",
                object_id=uuid4(),
                payload=validation.model_dump(mode="json"),
                created_at=utc_now(),
            )
        )
        return validation

    def clear_approval_blocker(
        self,
        *,
        approval_blocker_receipt_id: UUID,
        blocker_id: UUID,
        actor_id: UUID,
        evidence_refs: list[str],
    ) -> ApprovalBlockerReceipt:
        receipt = self.repository.receipts.get(approval_blocker_receipt_id)
        if receipt is None:
            raise ApprovalGateError("APPROVAL_BLOCKER_RECEIPT_REQUIRED", "Approval blocker receipt is required.")
        if blocker_id not in receipt.blocker_ids:
            raise ApprovalGateError("APPROVAL_BLOCKER_REQUIRED", "Approval blocker is not present on this receipt.")
        updated = receipt.model_copy(update={"cleared_blocker_ids": sorted(set([*receipt.cleared_blocker_ids, blocker_id]), key=str)})
        self.repository.put_receipt(updated)
        self.repository.append_event(
            ApprovalGateDomainEvent(
                schema_version="cmf.approval_gate_domain_event.v1",
                approval_gate_event_id=uuid4(),
                event_type="ApprovalBlockerCleared",
                approval_request_id=receipt.approval_request_id,
                object_type=receipt.object_type,
                object_id=receipt.object_id,
                payload={"blocker_id": str(blocker_id), "actor_id": str(actor_id), "evidence_refs": evidence_refs},
                created_at=utc_now(),
            )
        )
        return updated

    def stage13_approval_gate(self, gate_input: ApprovalGateInput | dict[str, Any]) -> ApprovalPolicyReport:
        return self.evaluate_approval_gate(gate_input)

    def _blockers(self, gate_input: ApprovalGateInput, content_format: ContentFormatValidation) -> list[ApprovalGateBlocker]:
        blockers: list[ApprovalGateBlocker] = []
        missing_lineage = [key for key in gate_input.required_lineage_keys if not gate_input.lineage_refs.get(key)]
        if missing_lineage:
            blockers.append(
                self._blocker(
                    "LINEAGE_INCOMPLETE",
                    "lineage",
                    [f"missing:{key}" for key in missing_lineage],
                    f"Lineage is incomplete: {', '.join(missing_lineage)}.",
                    "repair_lineage_before_approval",
                )
            )
        if not gate_input.consent_compatible or gate_input.consent_blocker_codes:
            blockers.append(
                self._blocker(
                    gate_input.consent_blocker_codes[0] if gate_input.consent_blocker_codes else "CONSENT_SCOPE_BLOCKED",
                    "consent",
                    gate_input.evidence_refs or ["consent"],
                    "Consent is incompatible with final approval.",
                    "repair_or_refresh_consent",
                )
            )
        if not gate_input.source_truth_passed or gate_input.disputed_source_refs:
            blockers.append(
                self._blocker(
                    "SOURCE_TRUTH_BLOCKED",
                    "source_truth",
                    gate_input.disputed_source_refs or gate_input.evidence_refs or ["source_truth"],
                    "Source truth is missing or disputed.",
                    "revise_or_remove_unsupported_claim",
                )
            )
        if not gate_input.identity_passed or gate_input.identity_failure_refs:
            blockers.append(
                self._blocker(
                    "IDENTITY_OR_LIKENESS_FAILED",
                    "identity",
                    gate_input.identity_failure_refs or gate_input.evidence_refs or ["identity"],
                    "Identity or likeness evaluation failed.",
                    "request_revision_or_reject_asset",
                )
            )
        if not gate_input.evaluation_passed or gate_input.evaluation_hard_failure_codes:
            blockers.append(
                self._blocker(
                    gate_input.evaluation_hard_failure_codes[0] if gate_input.evaluation_hard_failure_codes else "EVALUATION_HARD_FAIL",
                    "evaluation",
                    [str(item) for item in gate_input.evaluation_receipt_ids] or gate_input.evidence_refs or ["evaluation"],
                    "Evaluation hard failure is unresolved.",
                    "rerun_evaluation_after_revision",
                )
            )
        if not gate_input.platform_format_passed or gate_input.platform_blocker_codes:
            blockers.append(
                self._blocker(
                    gate_input.platform_blocker_codes[0] if gate_input.platform_blocker_codes else "PLATFORM_FORMAT_BLOCKED",
                    "platform_format",
                    gate_input.evidence_refs or [gate_input.platform_variant_id],
                    "Platform format is invalid for approval.",
                    "repair_platform_variant_or_manifest",
                )
            )
        if not content_format.valid_content_format:
            blockers.append(
                self._blocker(
                    "CONTENT_FORMAT_UNSUPPORTED",
                    "content_format_registry",
                    [content_format.registry_version_id, content_format.format_key],
                    "Content format is not represented in the valid content-format registry.",
                    "select_documented_content_format",
                )
            )
        return blockers

    def _lineage_complete(self, gate_input: ApprovalGateInput) -> bool:
        return all(gate_input.lineage_refs.get(key) for key in gate_input.required_lineage_keys)

    @staticmethod
    def _blocker(
        code: str,
        source_object_ref: str,
        evidence_refs: list[str],
        message: str,
        repair_hint: str,
        severity: ApprovalBlockerSeverity = ApprovalBlockerSeverity.hard,
    ) -> ApprovalGateBlocker:
        return ApprovalGateBlocker(
            blocker_id=uuid4(),
            code=code,
            severity=severity,
            source_object_ref=source_object_ref,
            evidence_refs=evidence_refs,
            message=message,
            repair_hint=repair_hint,
        )

    def _event(self, event_type: str, report: ApprovalPolicyReport, payload: dict[str, Any]) -> ApprovalGateDomainEvent:
        return self.repository.append_event(
            ApprovalGateDomainEvent(
                schema_version="cmf.approval_gate_domain_event.v1",
                approval_gate_event_id=uuid4(),
                event_type=event_type,
                approval_request_id=report.approval_request_id,
                object_type=report.object_type,
                object_id=report.object_id,
                payload=payload,
                created_at=utc_now(),
            )
        )


@dataclass
class ApprovalGateCommandHandler:
    command_type: str
    service: ApprovalGateService
    aggregate_type: str = "approval_gate"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "reviewer", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type in {"EvaluateApprovalGateCommand", "BlockApprovalCommand"}:
            gate_input = payload["gate_input"] | {
                "organization_id": str(envelope.organization_id),
                "brand_id": str(envelope.brand_id),
            }
            return self.service.evaluate_approval_gate(gate_input).model_dump(mode="json")
        if self.command_type == "ValidateContentFormatCommand":
            return self.service.validate_content_format(
                platform_variant_id=payload["platform_variant_id"],
                format_key=payload["format_key"],
                registry_version_id=payload["registry_version_id"],
                valid_content_formats=payload.get("valid_content_formats", []),
            ).model_dump(mode="json")
        if self.command_type == "ClearApprovalBlockerCommand":
            return self.service.clear_approval_blocker(
                approval_blocker_receipt_id=UUID(payload["approval_blocker_receipt_id"]),
                blocker_id=UUID(payload["blocker_id"]),
                actor_id=envelope.actor.actor_id,
                evidence_refs=payload.get("evidence_refs", []),
            ).model_dump(mode="json")
        if self.command_type == "RecordApprovalBlockerReceiptCommand":
            receipt = self.service.repository.receipts.get(UUID(payload["approval_blocker_receipt_id"]))
            if receipt is None:
                raise ApprovalGateError("APPROVAL_BLOCKER_RECEIPT_REQUIRED", "Approval blocker receipt is required.")
            return receipt.model_dump(mode="json")
        raise ApprovalGateError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("approval_blocker_receipt_id") or payload.get("approval_policy_report_id")
        gate_input = payload.get("gate_input", {})
        raw = raw or gate_input.get("approval_request_id") or gate_input.get("object_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_approval_gate_command_handlers(bus: CommandBus, service: ApprovalGateService) -> None:
    for command_type in [
        "EvaluateApprovalGateCommand",
        "BlockApprovalCommand",
        "ClearApprovalBlockerCommand",
        "ValidateContentFormatCommand",
        "RecordApprovalBlockerReceiptCommand",
    ]:
        bus.register_handler(ApprovalGateCommandHandler(command_type=command_type, service=service))

