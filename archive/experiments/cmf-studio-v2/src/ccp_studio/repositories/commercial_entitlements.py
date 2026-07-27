"""Commercial repositories for TS-CMF-006."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.commercial import (
    CommercialEntitlement,
    CostPolicy,
    CostReceipt,
    QuotaPolicy,
    UsageLedgerEntry,
)


@dataclass
class InMemoryCommercialRepository:
    entitlements: dict[UUID, CommercialEntitlement] = field(default_factory=dict)
    entitlement_by_scope: dict[tuple[UUID, UUID], UUID] = field(default_factory=dict)
    quota_policies: dict[UUID, QuotaPolicy] = field(default_factory=dict)
    cost_policies: dict[UUID, CostPolicy] = field(default_factory=dict)
    usage_entries: dict[UUID, UsageLedgerEntry] = field(default_factory=dict)
    cost_receipts: dict[UUID, CostReceipt] = field(default_factory=dict)

    def put_entitlement(self, entitlement: CommercialEntitlement) -> CommercialEntitlement:
        self.entitlements[entitlement.commercial_entitlement_id] = entitlement
        self.entitlement_by_scope[(entitlement.organization_id, entitlement.brand_id)] = (
            entitlement.commercial_entitlement_id
        )
        return entitlement

    def get_entitlement(self, organization_id: UUID, brand_id: UUID) -> CommercialEntitlement | None:
        entitlement_id = self.entitlement_by_scope.get((organization_id, brand_id))
        if entitlement_id is None:
            return None
        return self.entitlements.get(entitlement_id)

    def put_quota_policy(self, policy: QuotaPolicy) -> QuotaPolicy:
        self.quota_policies[policy.entitlement_id] = policy
        return policy

    def get_quota_policy(self, entitlement_id: UUID) -> QuotaPolicy | None:
        return self.quota_policies.get(entitlement_id)

    def put_cost_policy(self, policy: CostPolicy) -> CostPolicy:
        self.cost_policies[policy.entitlement_id] = policy
        return policy

    def get_cost_policy(self, entitlement_id: UUID) -> CostPolicy | None:
        return self.cost_policies.get(entitlement_id)

    def put_usage_entry(self, entry: UsageLedgerEntry) -> UsageLedgerEntry:
        self.usage_entries[entry.usage_ledger_entry_id] = entry
        return entry

    def count_usage(self, entitlement_id: UUID, usage_type: str) -> int:
        return sum(
            entry.quantity
            for entry in self.usage_entries.values()
            if entry.entitlement_id == entitlement_id and entry.usage_type == usage_type
        )

    def put_cost_receipt(self, receipt: CostReceipt) -> CostReceipt:
        self.cost_receipts[receipt.cost_receipt_id] = receipt
        return receipt
