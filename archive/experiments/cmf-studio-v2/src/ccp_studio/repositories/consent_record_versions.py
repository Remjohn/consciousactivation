"""Consent repositories for TS-CMF-008."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.consent import (
    ConsentChangeImpact,
    ConsentReceipt,
    ConsentRecordVersion,
    PendingWorkItem,
)


@dataclass
class InMemoryConsentRepository:
    versions: dict[UUID, ConsentRecordVersion] = field(default_factory=dict)
    receipts: dict[UUID, ConsentReceipt] = field(default_factory=dict)
    pending_work: dict[UUID, PendingWorkItem] = field(default_factory=dict)
    impacts: dict[UUID, ConsentChangeImpact] = field(default_factory=dict)

    def put_version(self, version: ConsentRecordVersion) -> ConsentRecordVersion:
        self.versions[version.consent_record_version_id] = version
        return version

    def versions_for_subject(self, organization_id: UUID, brand_id: UUID, guest_or_client_id: UUID) -> list[ConsentRecordVersion]:
        return sorted(
            [
                version
                for version in self.versions.values()
                if version.organization_id == organization_id
                and version.brand_id == brand_id
                and version.guest_or_client_id == guest_or_client_id
            ],
            key=lambda item: item.version_number,
        )

    def current_version(self, organization_id: UUID, brand_id: UUID, guest_or_client_id: UUID) -> ConsentRecordVersion | None:
        versions = self.versions_for_subject(organization_id, brand_id, guest_or_client_id)
        if not versions:
            return None
        return versions[-1]

    def put_receipt(self, receipt: ConsentReceipt) -> ConsentReceipt:
        self.receipts[receipt.consent_receipt_id] = receipt
        return receipt

    def put_pending_work(self, item: PendingWorkItem) -> PendingWorkItem:
        self.pending_work[item.pending_work_id] = item
        return item

    def pending_for_subject(self, organization_id: UUID, brand_id: UUID, guest_or_client_id: UUID) -> list[PendingWorkItem]:
        return [
            item
            for item in self.pending_work.values()
            if item.organization_id == organization_id
            and item.brand_id == brand_id
            and item.guest_or_client_id == guest_or_client_id
            and item.status == "queued"
        ]

    def put_impact(self, impact: ConsentChangeImpact) -> ConsentChangeImpact:
        self.impacts[impact.impact_id] = impact
        return impact
