"""Consent blocker repositories for TS-CMF-010."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.consent_blockers import (
    AffectedPendingWork,
    ConsentBlockerReceipt,
    ConsentSensitiveCommand,
)


@dataclass
class InMemoryConsentBlockerRepository:
    sensitive_commands: dict[str, ConsentSensitiveCommand] = field(default_factory=dict)
    blocker_receipts: dict[UUID, ConsentBlockerReceipt] = field(default_factory=dict)
    affected_pending_work: dict[UUID, AffectedPendingWork] = field(default_factory=dict)

    def put_sensitive_command(self, command: ConsentSensitiveCommand) -> ConsentSensitiveCommand:
        self.sensitive_commands[command.command_type] = command
        return command

    def get_sensitive_command(self, command_type: str) -> ConsentSensitiveCommand | None:
        return self.sensitive_commands.get(command_type)

    def put_blocker_receipt(self, receipt: ConsentBlockerReceipt) -> ConsentBlockerReceipt:
        self.blocker_receipts[receipt.consent_blocker_receipt_id] = receipt
        return receipt

    def receipts_for_command(self, command_id: UUID) -> list[ConsentBlockerReceipt]:
        return [
            receipt
            for receipt in self.blocker_receipts.values()
            if receipt.command_id == command_id
        ]

    def put_affected_pending_work(self, item: AffectedPendingWork) -> AffectedPendingWork:
        self.affected_pending_work[item.affected_pending_work_id] = item
        return item
