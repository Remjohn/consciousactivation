"""Asset package repositories for TS-CMF-034."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from ccp_studio.contracts.asset_package import (
    AssetPackageSpec,
    CompleteEditingSessionRequestCandidate,
    PackageGap,
    PackageSpecReceipt,
    ReactionSeed,
)


@dataclass
class InMemoryAssetPackageRepository:
    specs: dict[UUID, AssetPackageSpec] = field(default_factory=dict)
    gaps: dict[UUID, PackageGap] = field(default_factory=dict)
    reaction_seeds: dict[UUID, ReactionSeed] = field(default_factory=dict)
    receipts: dict[UUID, PackageSpecReceipt] = field(default_factory=dict)
    editing_session_requests: dict[UUID, CompleteEditingSessionRequestCandidate] = field(default_factory=dict)

    def put_spec(self, spec: AssetPackageSpec) -> AssetPackageSpec:
        self.specs[spec.asset_package_spec_id] = spec
        return spec

    def put_gap(self, gap: PackageGap) -> PackageGap:
        self.gaps[gap.package_gap_id] = gap
        return gap

    def put_reaction_seed(self, seed: ReactionSeed) -> ReactionSeed:
        self.reaction_seeds[seed.reaction_seed_id] = seed
        return seed

    def put_receipt(self, receipt: PackageSpecReceipt) -> PackageSpecReceipt:
        self.receipts[receipt.package_spec_receipt_id] = receipt
        return receipt

    def put_editing_session_request(
        self,
        request: CompleteEditingSessionRequestCandidate,
    ) -> CompleteEditingSessionRequestCandidate:
        self.editing_session_requests[request.complete_editing_session_request_id] = request
        return request
