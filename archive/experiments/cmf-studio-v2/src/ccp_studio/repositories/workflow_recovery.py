"""Workflow recovery repository for TS-CMF-060."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.workflow_recovery import (
    RecoveryValidationReport,
    WorkflowOperationalIncident,
    WorkflowRecoveryAction,
    WorkflowRecoveryActionType,
    WorkflowRecoveryDomainEvent,
    WorkflowRecoveryReceipt,
)


@dataclass
class InMemoryWorkflowRecoveryRepository:
    validation_reports: dict[UUID, RecoveryValidationReport] = field(default_factory=dict)
    incidents: dict[UUID, WorkflowOperationalIncident] = field(default_factory=dict)
    actions: dict[UUID, WorkflowRecoveryAction] = field(default_factory=dict)
    receipts: dict[UUID, WorkflowRecoveryReceipt] = field(default_factory=dict)
    quarantined_refs: set[str] = field(default_factory=set)
    events: list[WorkflowRecoveryDomainEvent] = field(default_factory=list)
    idempotency_index: dict[tuple[UUID, WorkflowRecoveryActionType, str], UUID] = field(default_factory=dict)

    def put_report(self, report: RecoveryValidationReport) -> RecoveryValidationReport:
        self.validation_reports[report.report_id] = report
        return report

    def put_incident(self, incident: WorkflowOperationalIncident) -> WorkflowOperationalIncident:
        self.incidents[incident.incident_id] = incident
        return incident

    def put_action(self, action: WorkflowRecoveryAction) -> WorkflowRecoveryAction:
        self.actions[action.recovery_action_id] = action
        return action

    def put_receipt(self, receipt: WorkflowRecoveryReceipt) -> WorkflowRecoveryReceipt:
        self.receipts[receipt.receipt_id] = receipt
        self.idempotency_index[(receipt.incident_id, receipt.action_type, receipt.idempotency_key)] = receipt.receipt_id
        self.quarantined_refs.update(receipt.quarantined_refs)
        return receipt

    def receipt_for_idempotency(
        self,
        incident_id: UUID,
        action_type: WorkflowRecoveryActionType,
        idempotency_key: str,
    ) -> WorkflowRecoveryReceipt | None:
        receipt_id = self.idempotency_index.get((incident_id, action_type, idempotency_key))
        return self.receipts.get(receipt_id) if receipt_id else None

    def append_event(self, event: WorkflowRecoveryDomainEvent) -> WorkflowRecoveryDomainEvent:
        self.events.append(event)
        return event
