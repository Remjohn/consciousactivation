"""Evaluation receipt repositories for TS-CMF-050."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.evaluation_receipts import (
    EvaluationApprovalBlocker,
    EvaluationDomainEvent,
    EvaluationObjectType,
    EvaluationReceipt,
    EvaluationThresholdProfile,
)


@dataclass
class InMemoryEvaluationReceiptRepository:
    threshold_profiles: dict[str, EvaluationThresholdProfile] = field(default_factory=dict)
    receipts: dict[UUID, EvaluationReceipt] = field(default_factory=dict)
    approval_blockers: dict[UUID, EvaluationApprovalBlocker] = field(default_factory=dict)
    events: list[EvaluationDomainEvent] = field(default_factory=list)

    def put_threshold_profile(self, profile: EvaluationThresholdProfile) -> EvaluationThresholdProfile:
        self.threshold_profiles[profile.threshold_profile_id] = profile
        return profile

    def put_receipt(self, receipt: EvaluationReceipt) -> EvaluationReceipt:
        if receipt.evaluation_receipt_id in self.receipts:
            raise ValueError("evaluation receipts are immutable")
        self.receipts[receipt.evaluation_receipt_id] = receipt
        return receipt

    def put_approval_blocker(self, blocker: EvaluationApprovalBlocker) -> EvaluationApprovalBlocker:
        self.approval_blockers[blocker.evaluation_approval_blocker_id] = blocker
        return blocker

    def append_event(self, event: EvaluationDomainEvent) -> EvaluationDomainEvent:
        self.events.append(event)
        return event

    def receipts_for_object(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        object_type: EvaluationObjectType | str,
        object_id: UUID,
    ) -> list[EvaluationReceipt]:
        normalized = EvaluationObjectType(object_type)
        receipts = [
            receipt
            for receipt in self.receipts.values()
            if receipt.organization_id == organization_id
            and receipt.brand_id == brand_id
            and receipt.object_type == normalized
            and receipt.object_id == object_id
        ]
        return sorted(receipts, key=lambda item: item.created_at)

    def latest_for_object(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        object_type: EvaluationObjectType | str,
        object_id: UUID,
    ) -> EvaluationReceipt | None:
        receipts = self.receipts_for_object(
            organization_id=organization_id,
            brand_id=brand_id,
            object_type=object_type,
            object_id=object_id,
        )
        return receipts[-1] if receipts else None

    def blockers_for_receipt(self, evaluation_receipt_id: UUID) -> list[EvaluationApprovalBlocker]:
        blockers = [
            blocker
            for blocker in self.approval_blockers.values()
            if blocker.evaluation_receipt_id == evaluation_receipt_id
        ]
        return sorted(blockers, key=lambda item: item.created_at)

