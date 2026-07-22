"""Ideogram 4 CompositionJob lineage contracts for TS-CMF-038."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class CompositionUsageState(str, Enum):
    approved_composition_plate = "approved_composition_plate"
    background_only = "background_only"
    repair_required = "repair_required"
    rejected = "rejected"


class CompositionConstraints(BaseModel):
    schema_version: Literal["cmf.composition_constraints.v1"]
    aspect_ratio: str = Field(min_length=1)
    subject_position: str = Field(min_length=1)
    text_area: str = Field(min_length=1)
    visual_flow: str = Field(min_length=1)
    style: str = Field(min_length=1)
    identity_boundary: str = Field(min_length=1)
    final_text_policy: str = Field(min_length=1)
    micro_semiotic_anchor_ids: list[UUID] = Field(default_factory=list)


class CompositionOutputRequirements(BaseModel):
    schema_version: Literal["cmf.composition_output_requirements.v1"]
    storage_prefix: str = Field(min_length=1)
    plate_format: str = Field(min_length=1)
    layerability_required: bool = True
    composition_analysis_required: bool = True
    final_text_must_be_downstream: bool = True
    identity_must_be_rebuilt_downstream: bool = True


class FinalTextPlan(BaseModel):
    schema_version: Literal["cmf.final_text_plan.v1"]
    final_text_plan_id: UUID
    composition_job_id: UUID
    text_content_ref: str = Field(min_length=1)
    text_layer_strategy: str = Field(min_length=1)
    renderer_route: str = Field(min_length=1)
    editable_text_required: bool = True
    approved_for_downstream_render: bool = False


class CompositionJob(BaseModel):
    schema_version: Literal["cmf.composition_job.v1"]
    composition_job_id: UUID
    complete_editing_session_id: UUID
    scene_spec_id: UUID
    provider: Literal["ideogram_4"] = "ideogram_4"
    purpose: Literal["composition_plate"] = "composition_plate"
    compiled_prompt: str = Field(min_length=1)
    prompt_hash: str = Field(min_length=1)
    constraints: CompositionConstraints
    output_requirements: CompositionOutputRequirements
    provider_metadata: dict[str, Any] = Field(default_factory=dict)
    provider_correlation_id: str | None = None
    selected_brand_layer_refs: list[str] = Field(default_factory=list)
    final_text_plan_id: UUID | None = None
    job_json_hash: str = Field(min_length=1)
    created_at: datetime


class IdeogramProviderReceipt(BaseModel):
    schema_version: Literal["cmf.ideogram_provider_receipt.v1"]
    provider_receipt_id: UUID
    composition_job_id: UUID
    provider: Literal["ideogram_4"] = "ideogram_4"
    operation: str = Field(min_length=1)
    provider_correlation_id: str = Field(min_length=1)
    model_version: str = Field(min_length=1)
    request_hash: str = Field(min_length=1)
    response_metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


class CompositionAnalysis(BaseModel):
    schema_version: Literal["cmf.composition_analysis.v1"]
    composition_analysis_id: UUID
    composition_job_id: UUID
    text_space_score: float = Field(ge=0, le=1)
    identity_drift_score: float = Field(ge=0, le=1)
    baked_final_text_detected: bool
    layerability_score: float = Field(ge=0, le=1)
    style_fit_score: float = Field(ge=0, le=1)
    visual_flow_score: float = Field(ge=0, le=1)
    boundary_notes: list[str] = Field(default_factory=list)
    created_at: datetime


class CompositionPlate(BaseModel):
    schema_version: Literal["cmf.composition_plate.v1"]
    composition_plate_id: UUID
    composition_job_id: UUID
    plate_uri: str = Field(min_length=1)
    plate_hash: str = Field(min_length=1)
    provider_receipt_id: UUID
    composition_analysis_id: UUID
    usage_state: CompositionUsageState
    usage_reason: str = Field(min_length=1)
    created_at: datetime


class DownstreamCompositionEdit(BaseModel):
    schema_version: Literal["cmf.downstream_composition_edit.v1"]
    downstream_composition_edit_id: UUID
    composition_job_id: UUID
    composition_plate_id: UUID
    downstream_object_id: UUID
    downstream_object_type: str = Field(min_length=1)
    edit_type: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    created_at: datetime


class CompositionLineageAudit(BaseModel):
    schema_version: Literal["cmf.composition_lineage_audit.v1"]
    composition_job: CompositionJob
    composition_plate: CompositionPlate | None = None
    composition_analysis: CompositionAnalysis | None = None
    downstream_edits: list[DownstreamCompositionEdit] = Field(default_factory=list)
    final_text_plan: FinalTextPlan | None = None


class IdeogramCompositionProviderResponse(BaseModel):
    schema_version: Literal["cmf.ideogram_composition_provider_response.v1"]
    provider_correlation_id: str
    plate_uri: str
    plate_hash: str
    model_version: str = "ideogram_4"
    response_metadata: dict[str, Any] = Field(default_factory=dict)
    analysis: dict[str, Any] = Field(default_factory=dict)


class CompositionReceipt(BaseModel):
    schema_version: Literal["cmf.composition_receipt.v1"]
    composition_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    complete_editing_session_id: UUID | None = None
    scene_spec_id: UUID | None = None
    composition_job_id: UUID | None = None
    composition_job_json_hash: str | None = None
    prompt_hash: str | None = None
    composition_plate_id: UUID | None = None
    plate_uri: str | None = None
    plate_hash: str | None = None
    provider_receipt_id: UUID | None = None
    composition_analysis_id: UUID | None = None
    usage_state: CompositionUsageState | None = None
    downstream_edit_ids: list[UUID] = Field(default_factory=list)
    final_text_plan_id: UUID | None = None
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    actor_id: UUID
    command_id: UUID | None = None
    written_at: datetime


def stable_hash(parts: Any) -> str:
    payload = json.dumps(parts, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def new_composition_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    actor_id: UUID,
    decision_code: str,
    evidence_refs: list[str],
    complete_editing_session_id: UUID | None = None,
    scene_spec_id: UUID | None = None,
    composition_job_id: UUID | None = None,
    composition_job_json_hash: str | None = None,
    prompt_hash: str | None = None,
    composition_plate_id: UUID | None = None,
    plate_uri: str | None = None,
    plate_hash: str | None = None,
    provider_receipt_id: UUID | None = None,
    composition_analysis_id: UUID | None = None,
    usage_state: CompositionUsageState | None = None,
    downstream_edit_ids: list[UUID] | None = None,
    final_text_plan_id: UUID | None = None,
    command_id: UUID | None = None,
) -> CompositionReceipt:
    return CompositionReceipt(
        schema_version="cmf.composition_receipt.v1",
        composition_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        complete_editing_session_id=complete_editing_session_id,
        scene_spec_id=scene_spec_id,
        composition_job_id=composition_job_id,
        composition_job_json_hash=composition_job_json_hash,
        prompt_hash=prompt_hash,
        composition_plate_id=composition_plate_id,
        plate_uri=plate_uri,
        plate_hash=plate_hash,
        provider_receipt_id=provider_receipt_id,
        composition_analysis_id=composition_analysis_id,
        usage_state=usage_state,
        downstream_edit_ids=downstream_edit_ids or [],
        final_text_plan_id=final_text_plan_id,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        actor_id=actor_id,
        command_id=command_id,
        written_at=utc_now(),
    )
