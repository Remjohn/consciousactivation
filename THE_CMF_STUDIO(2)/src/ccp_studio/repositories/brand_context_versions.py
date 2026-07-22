"""Brand Context version repositories for TS-CMF-021."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.brand_context import (
    BrandContextForkRequest,
    BrandContextLineageRef,
    BrandContextReceipt,
    BrandContextStatus,
    BrandContextVersion,
    GenesisClearanceCertificate,
)


@dataclass
class InMemoryBrandContextRepository:
    versions: dict[UUID, BrandContextVersion] = field(default_factory=dict)
    certificates: dict[UUID, GenesisClearanceCertificate] = field(default_factory=dict)
    fork_requests: dict[UUID, BrandContextForkRequest] = field(default_factory=dict)
    lineage_refs: dict[UUID, BrandContextLineageRef] = field(default_factory=dict)
    receipts: dict[UUID, BrandContextReceipt] = field(default_factory=dict)

    def put_version(self, version: BrandContextVersion) -> BrandContextVersion:
        existing = self.versions.get(version.brand_context_version_id)
        if existing and existing.status in {BrandContextStatus.locked, BrandContextStatus.superseded} and existing != version:
            if not self._is_allowed_supersession(existing, version):
                raise ValueError("locked brand context version is immutable")
        self.versions[version.brand_context_version_id] = version
        return version

    def put_certificate(self, certificate: GenesisClearanceCertificate) -> GenesisClearanceCertificate:
        self.certificates[certificate.genesis_clearance_certificate_id] = certificate
        return certificate

    def put_fork_request(self, request: BrandContextForkRequest) -> BrandContextForkRequest:
        self.fork_requests[request.brand_context_fork_request_id] = request
        return request

    def put_lineage_ref(self, lineage_ref: BrandContextLineageRef) -> BrandContextLineageRef:
        self.lineage_refs[lineage_ref.lineage_ref_id] = lineage_ref
        return lineage_ref

    def put_receipt(self, receipt: BrandContextReceipt) -> BrandContextReceipt:
        self.receipts[receipt.brand_context_receipt_id] = receipt
        return receipt

    def active_locked_for_brand(self, organization_id: UUID, brand_id: UUID) -> BrandContextVersion | None:
        locked = [
            version
            for version in self.versions.values()
            if version.organization_id == organization_id
            and version.brand_id == brand_id
            and version.status == BrandContextStatus.locked
        ]
        if not locked:
            return None
        return max(locked, key=lambda item: item.locked_at or item.created_at)

    @staticmethod
    def _is_allowed_supersession(existing: BrandContextVersion, proposed: BrandContextVersion) -> bool:
        return (
            existing.status == BrandContextStatus.locked
            and proposed.status == BrandContextStatus.superseded
            and existing.version_hash == proposed.version_hash
            and existing.asset_bundle == proposed.asset_bundle
            and existing.clearance_certificate_id == proposed.clearance_certificate_id
            and proposed.superseded_by_brand_context_version_id is not None
        )
