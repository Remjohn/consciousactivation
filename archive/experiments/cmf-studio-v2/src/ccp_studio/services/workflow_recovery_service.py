"""Workflow recovery service for TS-CMF-060."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.workflow_recovery import (
    RecoveryValidationReport,
    WorkflowOperationalIncident,
    WorkflowRecoveryAction,
    WorkflowRecoveryActionType,
    WorkflowRecoveryDomainEvent,
    WorkflowRecoveryReceipt,
    WorkflowRecoveryStatus,
    new_workflow_recovery_receipt,
)
from ccp_studio.repositories.workflow_recovery import InMemoryWorkflowRecoveryRepository
from ccp_studio.services.command_bus import CommandBus


WORKFLOW_RECOVERY_ROLES = {"owner", "admin", "operator", "production_steward"}


class WorkflowRecoveryError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class WorkflowRecoveryService:
    repository: InMemoryWorkflowRecoveryRepository = field(default_factory=InMemoryWorkflowRecoveryRepository)

    def build_recovery_validation_report(
        self,
        *,
        workflow_id: str,
        failed_object_ref: str,
        completed_artifact_refs: list[str],
        receipt_refs: list[str],
        consent_compatible: bool,
        publishing_side_effect_risk: bool = False,
        memory_side_effect_risk: bool = False,
        provider_cost_risk: bool = False,
        severity: str = "medium",
        summary: str | None = None,
    ) -> RecoveryValidationReport:
        duplicate_risks: list[str] = []
        if publishing_side_effect_risk:
            duplicate_risks.append("public_schedule_side_effect")
        if memory_side_effect_risk:
            duplicate_risks.append("memory_side_effect")
        if provider_cost_risk:
            duplicate_risks.append("provider_billing_side_effect")
        safe_actions = [WorkflowRecoveryActionType.quarantine]
        blocked_actions: list[str] = []
        if consent_compatible and not duplicate_risks:
            safe_actions.extend([WorkflowRecoveryActionType.retry, WorkflowRecoveryActionType.resume])
        else:
            blocked_actions.extend(["retry", "resume"])
        safe_actions.extend([WorkflowRecoveryActionType.cancel, WorkflowRecoveryActionType.compensate])
        report = self.repository.put_report(
            RecoveryValidationReport(
                schema_version="cmf.workflow_recovery_validation_report.v1",
                report_id=uuid4(),
                workflow_id=workflow_id,
                failed_object_ref=failed_object_ref,
                safe_actions=safe_actions,
                blocked_actions=blocked_actions,
                completed_artifact_refs=completed_artifact_refs,
                receipt_refs=receipt_refs,
                duplicate_side_effect_risks=duplicate_risks,
                consent_compatible=consent_compatible,
                provider_cost_risk=provider_cost_risk,
                publishing_side_effect_risk=publishing_side_effect_risk,
                memory_side_effect_risk=memory_side_effect_risk,
                checked_at=utc_now(),
            )
        )
        incident = self.repository.put_incident(
            WorkflowOperationalIncident(
                schema_version="cmf.workflow_operational_incident.v1",
                incident_id=uuid4(),
                workflow_id=workflow_id,
                failed_object_ref=failed_object_ref,
                severity=severity,
                summary=summary or f"Recovery validation required for {failed_object_ref}",
                resolved=False,
                validation_report_id=report.report_id,
                evidence_refs=receipt_refs,
                recorded_at=utc_now(),
            )
        )
        self._event("RecoveryValidationReportBuilt", incident.incident_id, None, {"report_id": str(report.report_id)})
        return report

    def apply_recovery_action(
        self,
        *,
        incident_id: UUID,
        action_type: WorkflowRecoveryActionType | str,
        requested_by_user_id: UUID,
        role_ids: list[str],
        reason: str,
        idempotency_key: str,
    ) -> WorkflowRecoveryReceipt:
        action_type = WorkflowRecoveryActionType(action_type)
        prior = self.repository.receipt_for_idempotency(incident_id, action_type, idempotency_key)
        if prior:
            return prior
        self._assert_role(role_ids)
        incident = self._incident(incident_id)
        if incident.validation_report_id is None:
            raise WorkflowRecoveryError("RECOVERY_VALIDATION_REPORT_REQUIRED", "Recovery validation report is required.")
        report = self._report(incident.validation_report_id)
        if action_type not in report.safe_actions:
            receipt = self.repository.put_receipt(
                new_workflow_recovery_receipt(
                    report=report,
                    incident_id=incident.incident_id,
                    action_type=action_type,
                    status=WorkflowRecoveryStatus.blocked,
                    idempotency_key=idempotency_key,
                    actor_id=requested_by_user_id,
                    decision_code="RECOVERY_ACTION_BLOCKED",
                    blocked_actions=[action_type.value, *report.blocked_actions],
                )
            )
            self._event("RecoveryReceiptRecorded", incident.incident_id, None, {"receipt_id": str(receipt.receipt_id), "status": "blocked"})
            return receipt
        action = self.repository.put_action(
            WorkflowRecoveryAction(
                schema_version="cmf.workflow_recovery_action.v1",
                recovery_action_id=uuid4(),
                incident_id=incident.incident_id,
                action_type=action_type,
                idempotency_key=idempotency_key,
                validation_report_id=report.report_id,
                requested_by_user_id=requested_by_user_id,
                reason=reason,
                created_at=utc_now(),
            )
        )
        preserved = report.completed_artifact_refs
        requeued = []
        quarantined = []
        terminal_state = None
        decision_code = f"WORKFLOW_{action_type.value.upper()}_APPLIED"
        event_type = {
            WorkflowRecoveryActionType.retry: "WorkflowRetried",
            WorkflowRecoveryActionType.resume: "WorkflowResumed",
            WorkflowRecoveryActionType.cancel: "WorkflowCancelled",
            WorkflowRecoveryActionType.compensate: "WorkflowCompensated",
            WorkflowRecoveryActionType.quarantine: "WorkflowArtifactsQuarantined",
        }[action_type]
        if action_type == WorkflowRecoveryActionType.retry:
            requeued = [f"{report.workflow_id}:incomplete_work"]
        elif action_type == WorkflowRecoveryActionType.resume:
            requeued = [f"{report.workflow_id}:resume_from_checkpoint"]
        elif action_type == WorkflowRecoveryActionType.cancel:
            terminal_state = "cancelled"
        elif action_type == WorkflowRecoveryActionType.compensate:
            terminal_state = "compensated"
        elif action_type == WorkflowRecoveryActionType.quarantine:
            quarantined = [report.failed_object_ref, *report.completed_artifact_refs]
            terminal_state = "quarantined"
        receipt = self.repository.put_receipt(
            new_workflow_recovery_receipt(
                report=report,
                incident_id=incident.incident_id,
                action_type=action_type,
                status=WorkflowRecoveryStatus.applied,
                idempotency_key=idempotency_key,
                actor_id=requested_by_user_id,
                decision_code=decision_code,
                recovery_action_id=action.recovery_action_id,
                preserved_artifact_refs=preserved,
                requeued_work_refs=requeued,
                quarantined_refs=quarantined,
                terminal_state=terminal_state,
            )
        )
        self.repository.put_incident(incident.model_copy(update={"resolved": action_type != WorkflowRecoveryActionType.quarantine}))
        self._event(event_type, incident.incident_id, action.recovery_action_id, {"receipt_id": str(receipt.receipt_id)})
        self._event("RecoveryReceiptRecorded", incident.incident_id, action.recovery_action_id, {"receipt_id": str(receipt.receipt_id)})
        return receipt

    def retry_workflow(self, **kwargs: Any) -> WorkflowRecoveryReceipt:
        return self.apply_recovery_action(action_type=WorkflowRecoveryActionType.retry, **kwargs)

    def resume_workflow(self, **kwargs: Any) -> WorkflowRecoveryReceipt:
        return self.apply_recovery_action(action_type=WorkflowRecoveryActionType.resume, **kwargs)

    def cancel_workflow(self, **kwargs: Any) -> WorkflowRecoveryReceipt:
        return self.apply_recovery_action(action_type=WorkflowRecoveryActionType.cancel, **kwargs)

    def compensate_workflow(self, **kwargs: Any) -> WorkflowRecoveryReceipt:
        return self.apply_recovery_action(action_type=WorkflowRecoveryActionType.compensate, **kwargs)

    def quarantine_workflow_artifacts(self, **kwargs: Any) -> WorkflowRecoveryReceipt:
        return self.apply_recovery_action(action_type=WorkflowRecoveryActionType.quarantine, **kwargs)

    def recover_failed_workflow(self, *, action_type: WorkflowRecoveryActionType | str, **kwargs: Any) -> WorkflowRecoveryReceipt:
        return self.apply_recovery_action(action_type=action_type, **kwargs)

    @staticmethod
    def _assert_role(role_ids: list[str]) -> None:
        if not set(role_ids).intersection(WORKFLOW_RECOVERY_ROLES):
            raise WorkflowRecoveryError("ROLE_PERMISSION_DENIED", "Actor lacks a workflow recovery role.")

    def _incident(self, incident_id: UUID) -> WorkflowOperationalIncident:
        incident = self.repository.incidents.get(UUID(str(incident_id)))
        if incident is None:
            raise WorkflowRecoveryError("OPERATIONAL_INCIDENT_REQUIRED", "Operational incident is required.")
        return incident

    def _report(self, report_id: UUID) -> RecoveryValidationReport:
        report = self.repository.validation_reports.get(UUID(str(report_id)))
        if report is None:
            raise WorkflowRecoveryError("RECOVERY_VALIDATION_REPORT_REQUIRED", "Recovery validation report is required.")
        return report

    def _event(self, event_type: str, incident_id: UUID | None, recovery_action_id: UUID | None, payload: dict[str, Any]) -> WorkflowRecoveryDomainEvent:
        return self.repository.append_event(
            WorkflowRecoveryDomainEvent(
                schema_version="cmf.workflow_recovery_domain_event.v1",
                workflow_recovery_event_id=uuid4(),
                event_type=event_type,
                incident_id=incident_id,
                recovery_action_id=recovery_action_id,
                payload=payload,
                created_at=utc_now(),
            )
        )


@dataclass
class WorkflowRecoveryCommandHandler:
    command_type: str
    service: WorkflowRecoveryService
    aggregate_type: str = "workflow_recovery"
    allowed_roles: set[str] = field(default_factory=lambda: WORKFLOW_RECOVERY_ROLES)
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "BuildRecoveryValidationReportCommand":
            return self.service.build_recovery_validation_report(**payload).model_dump(mode="json")
        common = {
            "incident_id": UUID(payload["incident_id"]),
            "requested_by_user_id": envelope.actor.actor_id,
            "role_ids": envelope.actor.role_ids,
            "reason": payload["reason"],
            "idempotency_key": envelope.idempotency_key,
        }
        if self.command_type == "RetryWorkflowCommand":
            return self.service.retry_workflow(**common).model_dump(mode="json")
        if self.command_type == "ResumeWorkflowCommand":
            return self.service.resume_workflow(**common).model_dump(mode="json")
        if self.command_type == "CancelWorkflowCommand":
            return self.service.cancel_workflow(**common).model_dump(mode="json")
        if self.command_type == "CompensateWorkflowCommand":
            return self.service.compensate_workflow(**common).model_dump(mode="json")
        if self.command_type == "QuarantineWorkflowArtifactsCommand":
            return self.service.quarantine_workflow_artifacts(**common).model_dump(mode="json")
        if self.command_type == "RecordRecoveryReceiptCommand":
            receipt = self.service.repository.receipts.get(UUID(payload["receipt_id"]))
            if receipt is None:
                raise WorkflowRecoveryError("RECOVERY_RECEIPT_REQUIRED", "Recovery receipt is required.")
            return receipt.model_dump(mode="json")
        raise WorkflowRecoveryError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        if payload.get("incident_id"):
            return UUID(payload["incident_id"])
        return envelope.brand_id


def register_workflow_recovery_command_handlers(bus: CommandBus, service: WorkflowRecoveryService) -> None:
    for command_type in [
        "BuildRecoveryValidationReportCommand",
        "RetryWorkflowCommand",
        "ResumeWorkflowCommand",
        "CancelWorkflowCommand",
        "CompensateWorkflowCommand",
        "QuarantineWorkflowArtifactsCommand",
        "RecordRecoveryReceiptCommand",
    ]:
        bus.register_handler(WorkflowRecoveryCommandHandler(command_type=command_type, service=service))
