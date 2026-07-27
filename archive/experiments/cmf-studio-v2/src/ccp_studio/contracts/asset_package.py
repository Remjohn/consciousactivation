"""Guest Asset Pack spec contracts for TS-CMF-034."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.commercial import PublicContentOffer
from ccp_studio.contracts.orchestration import utc_now


class PackageItemType(str, Enum):
    short_video = "short_video"
    carousel = "carousel"
    meme_visual = "meme_visual"
    poll_visual = "poll_visual"
    reaction_seed = "reaction_seed"


class PackageItemStatus(str, Enum):
    ready_for_editing_session = "ready_for_editing_session"
    source_gap = "source_gap"
    review_required = "review_required"


class AssetPackageStatus(str, Enum):
    draft = "draft"
    approved = "approved"
    superseded = "superseded"


class AssetPackageItem(BaseModel):
    schema_version: Literal["cmf.asset_package_item.v1"]
    package_item_id: UUID
    item_type: PackageItemType
    expression_moment_id: UUID | None = None
    asset_route_receipt_id: UUID | None = None
    registry_refs: list[str] = Field(default_factory=list)
    brand_context_required: bool = True
    evaluation_state: str = Field(min_length=1)
    production_readiness: PackageItemStatus
    source_gap_id: UUID | None = None
    complete_editing_session_request_id: UUID | None = None


class PackageGap(BaseModel):
    schema_version: Literal["cmf.package_gap.v1"]
    package_gap_id: UUID
    target_item_type: PackageItemType
    reason: str = Field(min_length=1)
    missing_source_requirement: str = Field(min_length=1)
    route_attempt_receipt_ids: list[UUID] = Field(default_factory=list)


class ReactionSeed(BaseModel):
    schema_version: Literal["cmf.reaction_seed.v1"]
    reaction_seed_id: UUID
    asset_package_spec_id: UUID
    package_item_id: UUID
    expression_moment_id: UUID
    seed_text: str = Field(min_length=1)
    route_receipt_id: UUID
    stored_for_future_reactions: bool = True


class CompleteEditingSessionRequestCandidate(BaseModel):
    schema_version: Literal["cmf.complete_editing_session_request_candidate.v1"]
    complete_editing_session_request_id: UUID
    asset_package_spec_id: UUID
    package_item_id: UUID
    expression_moment_id: UUID
    asset_route_receipt_id: UUID
    registry_refs: list[str] = Field(min_length=1)
    brand_context_required: bool = True
    evaluation_state: str = Field(min_length=1)
    route_state: str = Field(min_length=1)
    source_lineage_refs: list[str] = Field(min_length=1)
    created_at: datetime


class PackageSpecReceipt(BaseModel):
    schema_version: Literal["cmf.package_spec_receipt.v1"]
    package_spec_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    asset_package_spec_id: UUID
    route_receipt_ids: list[UUID] = Field(default_factory=list)
    ready_item_counts: dict[PackageItemType, int] = Field(default_factory=dict)
    gap_counts: dict[PackageItemType, int] = Field(default_factory=dict)
    offer_code: PublicContentOffer
    customer_facing_price_label: str = Field(min_length=1)
    readiness_status: str = Field(min_length=1)
    reviewer_actor_id: UUID | None = None
    written_at: datetime


class AssetPackageSpec(BaseModel):
    schema_version: Literal["cmf.asset_package_spec.v1"]
    asset_package_spec_id: UUID
    organization_id: UUID
    brand_id: UUID
    expression_session_id: UUID
    offer_code: PublicContentOffer
    customer_facing_price_label: str = Field(min_length=1)
    target_item_counts: dict[PackageItemType, int]
    items: list[AssetPackageItem]
    gaps: list[PackageGap] = Field(default_factory=list)
    reaction_seeds: list[ReactionSeed] = Field(default_factory=list)
    package_spec_receipt_id: UUID
    status: AssetPackageStatus
    approved_at: datetime | None = None
    created_at: datetime


TARGET_TRIAL_GUEST_PACK_COUNTS: dict[PackageItemType, int] = {
    PackageItemType.short_video: 4,
    PackageItemType.carousel: 2,
    PackageItemType.meme_visual: 2,
    PackageItemType.poll_visual: 2,
    PackageItemType.reaction_seed: 3,
}


def new_asset_package_item(
    *,
    item_type: PackageItemType,
    production_readiness: PackageItemStatus,
    evaluation_state: str,
    expression_moment_id: UUID | None = None,
    asset_route_receipt_id: UUID | None = None,
    registry_refs: list[str] | None = None,
    source_gap_id: UUID | None = None,
) -> AssetPackageItem:
    return AssetPackageItem(
        schema_version="cmf.asset_package_item.v1",
        package_item_id=uuid4(),
        item_type=item_type,
        expression_moment_id=expression_moment_id,
        asset_route_receipt_id=asset_route_receipt_id,
        registry_refs=registry_refs or [],
        evaluation_state=evaluation_state,
        production_readiness=production_readiness,
        source_gap_id=source_gap_id,
    )


def new_package_gap(
    *,
    target_item_type: PackageItemType,
    reason: str,
    missing_source_requirement: str,
    route_attempt_receipt_ids: list[UUID] | None = None,
) -> PackageGap:
    return PackageGap(
        schema_version="cmf.package_gap.v1",
        package_gap_id=uuid4(),
        target_item_type=target_item_type,
        reason=reason,
        missing_source_requirement=missing_source_requirement,
        route_attempt_receipt_ids=route_attempt_receipt_ids or [],
    )


def new_package_spec_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    asset_package_spec_id: UUID,
    route_receipt_ids: list[UUID],
    ready_item_counts: dict[PackageItemType, int],
    gap_counts: dict[PackageItemType, int],
    offer_code: PublicContentOffer,
    customer_facing_price_label: str,
    readiness_status: str,
    reviewer_actor_id: UUID | None = None,
) -> PackageSpecReceipt:
    return PackageSpecReceipt(
        schema_version="cmf.package_spec_receipt.v1",
        package_spec_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        asset_package_spec_id=asset_package_spec_id,
        route_receipt_ids=route_receipt_ids,
        ready_item_counts=ready_item_counts,
        gap_counts=gap_counts,
        offer_code=offer_code,
        customer_facing_price_label=customer_facing_price_label,
        readiness_status=readiness_status,
        reviewer_actor_id=reviewer_actor_id,
        written_at=utc_now(),
    )
