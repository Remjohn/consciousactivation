"""Acting library repositories for TS-CMF-019."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.acting_library import (
    ActingLibraryReceipt,
    ActingLibraryVersion,
    ActingProviderReceipt,
    ActingReference,
    ActingReferenceEvaluation,
    ActingReferenceStatus,
)


@dataclass
class InMemoryActingLibraryRepository:
    versions: dict[UUID, ActingLibraryVersion] = field(default_factory=dict)
    references: dict[UUID, ActingReference] = field(default_factory=dict)
    evaluations: dict[UUID, ActingReferenceEvaluation] = field(default_factory=dict)
    provider_receipts: dict[UUID, ActingProviderReceipt] = field(default_factory=dict)
    receipts: dict[UUID, ActingLibraryReceipt] = field(default_factory=dict)

    def put_version(self, version: ActingLibraryVersion) -> ActingLibraryVersion:
        existing = self.versions.get(version.acting_library_version_id)
        if existing and existing.locked and existing != version:
            raise ValueError("locked acting library version is immutable")
        self.versions[version.acting_library_version_id] = version
        return version

    def put_reference(self, reference: ActingReference) -> ActingReference:
        existing = self.references.get(reference.acting_reference_id)
        if existing and existing.status == ActingReferenceStatus.locked and existing != reference:
            raise ValueError("locked acting reference is immutable")
        self.references[reference.acting_reference_id] = reference
        return reference

    def put_evaluation(self, evaluation: ActingReferenceEvaluation) -> ActingReferenceEvaluation:
        self.evaluations[evaluation.evaluation_receipt_id] = evaluation
        return evaluation

    def put_provider_receipt(self, receipt: ActingProviderReceipt) -> ActingProviderReceipt:
        self.provider_receipts[receipt.provider_receipt_id] = receipt
        return receipt

    def put_receipt(self, receipt: ActingLibraryReceipt) -> ActingLibraryReceipt:
        self.receipts[receipt.acting_library_receipt_id] = receipt
        return receipt

    def references_for_version(self, acting_library_version_id: UUID) -> list[ActingReference]:
        return [
            reference
            for reference in self.references.values()
            if reference.acting_library_version_id == acting_library_version_id
        ]

    def references_for_brand(self, organization_id: UUID, brand_id: UUID) -> list[ActingReference]:
        return [
            reference
            for reference in self.references.values()
            if reference.organization_id == organization_id and reference.brand_id == brand_id
        ]
