"""Brand Context versioning contracts for TS-CMF-021."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class BrandContextStatus(str, Enum):
    draft = "draft"
    locked = "locked"
    superseded = "superseded"
    archived = "archived"


class BrandContextAssetBundle(BaseModel):
    schema_version: Literal["cmf.brand_context_asset_bundle.v1"]
    acting_library_version_id: UUID
    rig_manifest_id: UUID
    micro_semiotic_anchor_ids: list[UUID] = Field(default_factory=list)
    motion_recipe_ids: list[UUID] = Field(default_factory=list)
    sfx_asset_ids: list[UUID] = Field(default_factory=list)
    composition_preference_ids: list[UUID] = Field(default_factory=list)
    platform_profile_ids: list[UUID] = Field(default_factory=list)
    creative_library_receipt_ids: list[UUID] = Field(default_factory=list)
    evaluation_receipt_ids: list[UUID] = Field(default_factory=list)


class BrandContextVersion(BaseModel):
    schema_version: Literal["cmf.brand_context_version.v1"]
    brand_context_version_id: UUID
    organization_id: UUID
    brand_id: UUID
    brand_genesis_session_id: UUID
    parent_brand_context_version_id: UUID | None = None
    superseded_by_brand_context_version_id: UUID | None = None
    status: BrandContextStatus
    version_hash: str
    asset_bundle: BrandContextAssetBundle
    clearance_certificate_id: UUID | None = None
    approved_change_reason: str | None = None
    created_by_actor_id: UUID
    locked_by_actor_id: UUID | None = None
    created_at: datetime
    updated_at: datetime
    locked_at: datetime | None = None


class GenesisClearanceCertificate(BaseModel):
    schema_version: Literal["cmf.genesis_clearance_certificate.v1"]
    genesis_clearance_certificate_id: UUID
    brand_context_version_id: UUID
    organization_id: UUID
    brand_id: UUID
    acting_library_version_id: UUID
    rig_manifest_id: UUID
    creative_library_receipt_ids: list[UUID] = Field(default_factory=list)
    evaluation_receipt_ids: list[UUID] = Field(default_factory=list)
    version_hash: str
    approved_by_actor_id: UUID
    issued_at: datetime


class BrandContextForkRequest(BaseModel):
    schema_version: Literal["cmf.brand_context_fork_request.v1"]
    brand_context_fork_request_id: UUID
    parent_brand_context_version_id: UUID
    child_brand_context_version_id: UUID | None = None
    organization_id: UUID
    brand_id: UUID
    approved_change_reason: str = Field(min_length=1)
    requested_by_actor_id: UUID
    approved_by_actor_id: UUID
    created_at: datetime


class BrandContextLineageRef(BaseModel):
    schema_version: Literal["cmf.brand_context_lineage_ref.v1"]
    lineage_ref_id: UUID
    organization_id: UUID
    brand_id: UUID
    downstream_object_id: UUID
    downstream_object_type: str = Field(min_length=1)
    brand_context_version_id: UUID
    brand_context_version_hash: str
    captured_at: datetime


class BrandContextReceipt(BaseModel):
    schema_version: Literal["cmf.brand_context_receipt.v1"]
    brand_context_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    brand_context_version_id: UUID
    action: str = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime


def brand_context_version_hash(parts: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_brand_context_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    brand_context_version_id: UUID,
    action: str,
    decision_code: str,
    evidence_refs: list[str],
) -> BrandContextReceipt:
    return BrandContextReceipt(
        schema_version="cmf.brand_context_receipt.v1",
        brand_context_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        brand_context_version_id=brand_context_version_id,
        action=action,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        written_at=utc_now(),
    )
