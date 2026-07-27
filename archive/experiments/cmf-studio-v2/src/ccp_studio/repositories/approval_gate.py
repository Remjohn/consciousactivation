"""Approval gate repositories for TS-CMF-053."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.approval_gate import (
    ApprovalBlockerReceipt,
    ApprovalGateDomainEvent,
    ApprovalPolicyReport,
)


@dataclass
class InMemoryApprovalGateRepository:
    reports: dict[UUID, ApprovalPolicyReport] = field(default_factory=dict)
    receipts: dict[UUID, ApprovalBlockerReceipt] = field(default_factory=dict)
    events: list[ApprovalGateDomainEvent] = field(default_factory=list)

    def put_report(self, report: ApprovalPolicyReport) -> ApprovalPolicyReport:
        self.reports[report.approval_policy_report_id] = report
        return report

    def put_receipt(self, receipt: ApprovalBlockerReceipt) -> ApprovalBlockerReceipt:
        self.receipts[receipt.approval_blocker_receipt_id] = receipt
        return receipt

    def append_event(self, event: ApprovalGateDomainEvent) -> ApprovalGateDomainEvent:
        self.events.append(event)
        return event

