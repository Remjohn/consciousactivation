"""Doctrine test harness repositories for TS-CMF-077."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.doctrine_tests import (
    DoctrineInvariant,
    DoctrineTestRunReceipt,
)


@dataclass
class InMemoryDoctrineTestRepository:
    invariants: dict[str, DoctrineInvariant] = field(default_factory=dict)
    receipts: dict[UUID, DoctrineTestRunReceipt] = field(default_factory=dict)

    def put_invariant(self, invariant: DoctrineInvariant) -> DoctrineInvariant:
        self.invariants[invariant.invariant_id] = invariant
        return invariant

    def list_invariants_for_target_type(self, target_type: str) -> list[DoctrineInvariant]:
        return [
            invariant
            for invariant in self.invariants.values()
            if "*" in invariant.applies_to_target_types
            or target_type in invariant.applies_to_target_types
        ]

    def put_receipt(self, receipt: DoctrineTestRunReceipt) -> DoctrineTestRunReceipt:
        if receipt.doctrine_test_run_receipt_id in self.receipts:
            raise ValueError("doctrine test run receipts are immutable")
        self.receipts[receipt.doctrine_test_run_receipt_id] = receipt
        return receipt

    def receipts_for_target(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        target_id: UUID,
    ) -> list[DoctrineTestRunReceipt]:
        receipts = [
            receipt
            for receipt in self.receipts.values()
            if receipt.organization_id == organization_id
            and receipt.brand_id == brand_id
            and receipt.target.target_id == target_id
        ]
        return sorted(receipts, key=lambda item: item.created_at)
