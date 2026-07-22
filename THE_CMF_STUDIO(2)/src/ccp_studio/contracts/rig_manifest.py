"""Paper-cut rig manifest contracts for TS-CMF-020."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.creative_libraries import CreativeItemStatus
from ccp_studio.contracts.orchestration import utc_now


class RigLayer(BaseModel):
    schema_version: Literal["cmf.rig_layer.v1"]
    layer_name: str = Field(min_length=1)
    asset_uri: str = Field(min_length=1)
    pivot_points: dict[str, tuple[float, float]] = Field(default_factory=dict)
    layer_hash: str = Field(min_length=1)
    z_index: int = Field(ge=0)
    parent_layer_name: str | None = None


class RigPreviewTest(BaseModel):
    schema_version: Literal["cmf.rig_preview_test.v1"]
    test_name: str = Field(min_length=1)
    passed: bool
    failure_category: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)


class RigManifest(BaseModel):
    schema_version: Literal["cmf.rig_manifest.v1"]
    rig_manifest_id: UUID
    organization_id: UUID
    brand_id: UUID
    brand_genesis_session_id: UUID
    acting_library_version_id: UUID
    layers: list[RigLayer] = Field(default_factory=list)
    mouth_shape_refs: list[str] = Field(default_factory=list)
    eye_brow_variant_refs: list[str] = Field(default_factory=list)
    gesture_variant_refs: list[str] = Field(default_factory=list)
    body_layer_refs: list[str] = Field(default_factory=list)
    preview_tests: list[RigPreviewTest] = Field(default_factory=list)
    version_hash: str
    status: CreativeItemStatus
    created_at: datetime
    updated_at: datetime
    locked_at: datetime | None = None


class RigValidationReport(BaseModel):
    schema_version: Literal["cmf.rig_validation_report.v1"]
    rig_manifest_id: UUID
    organization_id: UUID
    brand_id: UUID
    passed: bool
    blocker_codes: list[str] = Field(default_factory=list)
    failed_preview_tests: list[str] = Field(default_factory=list)
    created_at: datetime


class RigPreviewReceipt(BaseModel):
    schema_version: Literal["cmf.rig_preview_receipt.v1"]
    rig_preview_receipt_id: UUID
    rig_manifest_id: UUID
    organization_id: UUID
    brand_id: UUID
    decision_code: str
    blocker_codes: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    written_at: datetime


def rig_manifest_hash(manifest_parts: dict) -> str:
    return hashlib.sha256(json.dumps(manifest_parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def new_rig_preview_receipt(
    *,
    manifest: RigManifest,
    decision_code: str,
    blocker_codes: list[str],
    evidence_refs: list[str],
) -> RigPreviewReceipt:
    return RigPreviewReceipt(
        schema_version="cmf.rig_preview_receipt.v1",
        rig_preview_receipt_id=uuid4(),
        rig_manifest_id=manifest.rig_manifest_id,
        organization_id=manifest.organization_id,
        brand_id=manifest.brand_id,
        decision_code=decision_code,
        blocker_codes=blocker_codes,
        evidence_refs=evidence_refs,
        written_at=utc_now(),
    )
