"""Commercial entitlement contracts for TS-CMF-006."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class PublicContentOffer(str, Enum):
    trial_guest_asset_pack = "trial_guest_asset_pack"
    monthly_asset_engine = "monthly_asset_engine"


PUBLIC_OFFER_COPY = {
    PublicContentOffer.trial_guest_asset_pack: "$29/week trial Guest Asset Pack",
    PublicContentOffer.monthly_asset_engine: "$99/month Monthly Asset Engine",
}


class EntitlementStatus(str, Enum):
    active = "active"
    expired = "expired"
    suspended = "suspended"
    cancelled = "cancelled"


class CommercialEntitlement(BaseModel):
    schema_version: Literal["cmf.commercial_entitlement.v1"]
    commercial_entitlement_id: UUID
    organization_id: UUID
    brand_id: UUID
    public_offer: PublicContentOffer
    status: EntitlementStatus
    starts_at: datetime
    ends_at: datetime | None = None


class QuotaPolicy(BaseModel):
    schema_version: Literal["cmf.quota_policy.v1"]
    quota_policy_id: UUID
    entitlement_id: UUID
    max_provider_jobs_per_period: int | None = None
    max_render_minutes_per_period: int | None = None
    max_storage_gb: int | None = None


class CostPolicy(BaseModel):
    schema_version: Literal["cmf.cost_policy.v1"]
    cost_policy_id: UUID
    entitlement_id: UUID
    provider_budget_cents_per_period: int | None = None
    requires_manual_override_above_cents: int | None = None


class UsageLedgerEntry(BaseModel):
    schema_version: Literal["cmf.usage_ledger_entry.v1"]
    usage_ledger_entry_id: UUID
    organization_id: UUID
    brand_id: UUID
    entitlement_id: UUID
    usage_type: str = Field(min_length=1)
    quantity: int = Field(ge=1)
    command_id: UUID | None = None
    recorded_at: datetime


class CommercialPolicyDecision(BaseModel):
    schema_version: Literal["cmf.commercial_policy_decision.v1"]
    organization_id: UUID
    brand_id: UUID
    command_type: str
    allowed: bool
    decision_code: str = Field(min_length=1)
    entitlement_id: UUID | None = None
    estimated_cost_cents: int | None = None
    decided_at: datetime


class CostReceipt(BaseModel):
    schema_version: Literal["cmf.cost_receipt.v1"]
    cost_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    command_id: UUID
    entitlement_id: UUID
    policy_decision: str = Field(min_length=1)
    estimated_cost_cents: int | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime


def new_commercial_entitlement(
    *,
    organization_id: UUID,
    brand_id: UUID,
    public_offer: PublicContentOffer,
    status: EntitlementStatus = EntitlementStatus.active,
    ends_at: datetime | None = None,
) -> CommercialEntitlement:
    return CommercialEntitlement(
        schema_version="cmf.commercial_entitlement.v1",
        commercial_entitlement_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        public_offer=public_offer,
        status=status,
        starts_at=utc_now(),
        ends_at=ends_at,
    )
