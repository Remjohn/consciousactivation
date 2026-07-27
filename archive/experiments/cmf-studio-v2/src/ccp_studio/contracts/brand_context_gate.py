"""Production gate contracts for locked Brand Context in TS-CMF-022."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class BrandContextGateStatus(str, Enum):
    allowed = "allowed"
    blocked = "blocked"
    decision_required = "decision_required"


class SupersededContextAction(str, Enum):
    preserve_original = "preserve_original"
    fork_to_new_context = "fork_to_new_context"


class SelectedBrandAssetRef(BaseModel):
    schema_version: Literal["cmf.selected_brand_asset_ref.v1"]
    asset_type: str = Field(min_length=1)
    asset_id: UUID
    asset_hash: str = Field(min_length=1)
    brand_context_version_id: UUID


class BrandContextGateResult(BaseModel):
    schema_version: Literal["cmf.brand_context_gate_result.v1"]
    brand_context_gate_result_id: UUID
    organization_id: UUID
    brand_id: UUID
    requested_brand_context_version_id: UUID | None = None
    requested_brand_context_version_hash: str | None = None
    status: BrandContextGateStatus
    decision_code: str
    selected_asset_refs: list[SelectedBrandAssetRef] = Field(default_factory=list)
    created_at: datetime


class SceneSpecBrandContextBinding(BaseModel):
    schema_version: Literal["cmf.scene_spec_brand_context_binding.v1"]
    scene_spec_id: UUID
    organization_id: UUID
    brand_id: UUID
    brand_context_version_id: UUID
    brand_context_version_hash: str
    selected_asset_refs: list[SelectedBrandAssetRef]
    bound_at: datetime


class SupersededContextDecision(BaseModel):
    schema_version: Literal["cmf.superseded_context_decision.v1"]
    superseded_context_decision_id: UUID
    organization_id: UUID
    brand_id: UUID
    superseded_brand_context_version_id: UUID
    action: SupersededContextAction
    replacement_brand_context_version_id: UUID | None = None
    decided_by_actor_id: UUID
    rationale: str = Field(min_length=1)
    decided_at: datetime


class ProviderBrandContextReceipt(BaseModel):
    schema_version: Literal["cmf.provider_brand_context_receipt.v1"]
    provider_brand_context_receipt_id: UUID
    provider_job_id: UUID
    organization_id: UUID
    brand_id: UUID
    scene_spec_id: UUID
    brand_context_version_id: UUID
    brand_context_version_hash: str
    selected_asset_hashes: list[str] = Field(min_length=1)
    written_at: datetime


class BrandContextLineageView(BaseModel):
    schema_version: Literal["cmf.brand_context_lineage_view.v1"]
    brand_context_lineage_view_id: UUID
    organization_id: UUID
    brand_id: UUID
    downstream_object_id: UUID
    downstream_object_type: str
    brand_context_version_id: UUID
    brand_context_version_hash: str
    selected_asset_refs: list[SelectedBrandAssetRef]
    opened_at: datetime


class BrandContextGateReceipt(BaseModel):
    schema_version: Literal["cmf.brand_context_gate_receipt.v1"]
    brand_context_gate_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    brand_context_gate_result_id: UUID
    decision_code: str
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime


def new_brand_context_gate_receipt(
    *,
    result: BrandContextGateResult,
    evidence_refs: list[str],
) -> BrandContextGateReceipt:
    return BrandContextGateReceipt(
        schema_version="cmf.brand_context_gate_receipt.v1",
        brand_context_gate_receipt_id=uuid4(),
        organization_id=result.organization_id,
        brand_id=result.brand_id,
        brand_context_gate_result_id=result.brand_context_gate_result_id,
        decision_code=result.decision_code,
        evidence_refs=evidence_refs,
        written_at=utc_now(),
    )
