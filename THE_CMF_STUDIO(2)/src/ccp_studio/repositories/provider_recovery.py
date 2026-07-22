"""Provider recovery repositories for TS-CMF-048."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.provider_recovery import (
    DuplicateCostRisk,
    OperationalIncident,
    ProviderJobCheckpoint,
    ProviderRecoveryAction,
    RecoveryActionType,
    RecoveryReceipt,
)


@dataclass
class InMemoryProviderRecoveryRepository:
    checkpoints: dict[UUID, ProviderJobCheckpoint] = field(default_factory=dict)
    duplicate_cost_risks: dict[UUID, DuplicateCostRisk] = field(default_factory=dict)
    actions: dict[UUID, ProviderRecoveryAction] = field(default_factory=dict)
    incidents: dict[UUID, OperationalIncident] = field(default_factory=dict)
    receipts: dict[UUID, RecoveryReceipt] = field(default_factory=dict)
    idempotency_index: dict[tuple[UUID, RecoveryActionType, str], UUID] = field(default_factory=dict)

    def put_checkpoint(self, checkpoint: ProviderJobCheckpoint) -> ProviderJobCheckpoint:
        self.checkpoints[checkpoint.provider_job_checkpoint_id] = checkpoint
        return checkpoint

    def put_duplicate_cost_risk(self, risk: DuplicateCostRisk) -> DuplicateCostRisk:
        self.duplicate_cost_risks[risk.duplicate_cost_risk_id] = risk
        return risk

    def put_action(self, action: ProviderRecoveryAction) -> ProviderRecoveryAction:
        self.actions[action.provider_recovery_action_id] = action
        return action

    def put_incident(self, incident: OperationalIncident) -> OperationalIncident:
        self.incidents[incident.operational_incident_id] = incident
        return incident

    def put_receipt(self, receipt: RecoveryReceipt) -> RecoveryReceipt:
        self.receipts[receipt.recovery_receipt_id] = receipt
        self.idempotency_index[(receipt.provider_job_id, receipt.action_type, receipt.idempotency_key)] = receipt.recovery_receipt_id
        return receipt

    def receipt_for_idempotency(
        self,
        provider_job_id: UUID,
        action_type: RecoveryActionType,
        idempotency_key: str,
    ) -> RecoveryReceipt | None:
        receipt_id = self.idempotency_index.get((provider_job_id, action_type, idempotency_key))
        return self.receipts.get(receipt_id) if receipt_id else None

    def checkpoints_for_job(self, provider_job_id: UUID) -> list[ProviderJobCheckpoint]:
        return [item for item in self.checkpoints.values() if item.provider_job_id == provider_job_id]
