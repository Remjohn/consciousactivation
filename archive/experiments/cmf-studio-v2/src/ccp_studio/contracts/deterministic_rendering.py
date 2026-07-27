"""Deterministic Remotion and Motion Canvas rendering contracts for TS-CMF-043."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


class DeterministicRenderer(str, Enum):
    remotion = "remotion"
    motion_canvas = "motion_canvas"


class DeterministicRenderStatus(str, Enum):
    props_built = "props_built"
    validated = "validated"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"
    replayed = "replayed"


class RendererRouteDecision(BaseModel):
    schema_version: Literal["cmf.renderer_route_decision.v1"]
    renderer_route_decision_id: UUID
    render_contract_id: UUID
    renderer: DeterministicRenderer
    decision_reason: str = Field(min_length=1)
    input_manifest_ids: list[UUID] = Field(min_length=1)
    created_at: datetime


class RendererPropsBundle(BaseModel):
    schema_version: Literal["cmf.renderer_props_bundle.v1"]
    renderer_props_bundle_id: UUID
    render_contract_id: UUID
    assembly_plan_id: UUID
    renderer: DeterministicRenderer
    layer_manifest_id: UUID
    animation_plan_id: UUID
    timeline_manifest_id: UUID
    caption_manifest_id: UUID | None = None
    audio_mix_manifest_id: UUID | None = None
    final_text_plan_id: UUID
    brand_context_version_id: UUID
    rig_manifest_id: UUID
    selected_brand_layer_ids: list[UUID] = Field(default_factory=list)
    motion_recipe_ids: list[UUID] = Field(default_factory=list)
    sfx_asset_ids: list[UUID] = Field(default_factory=list)
    platform_variant_ids: list[UUID] = Field(min_length=1)
    props_payload: dict[str, Any]
    props_hash: str = Field(min_length=1)
    generated_typescript_contract_ref: str = Field(min_length=1)
    generated_typescript_contract_hash: str = Field(min_length=1)
    built_at: datetime


class DeterministicRenderJob(BaseModel):
    schema_version: Literal["cmf.deterministic_render_job.v1"]
    deterministic_render_job_id: UUID
    renderer_props_bundle_id: UUID
    render_contract_id: UUID
    renderer: DeterministicRenderer
    status: DeterministicRenderStatus
    idempotency_key: str = Field(min_length=1)
    retry_count: int = Field(ge=0)
    provider_job_id: UUID | None = None
    started_at: datetime
    completed_at: datetime | None = None


class RenderOutput(BaseModel):
    schema_version: Literal["cmf.render_output.v1"]
    render_output_id: UUID
    deterministic_render_job_id: UUID
    render_contract_id: UUID
    renderer: DeterministicRenderer
    preview_uri: str | None = None
    final_uri: str = Field(min_length=1)
    output_hash: str = Field(min_length=1)
    renderer_version: str = Field(min_length=1)
    manifest_hashes: list[str] = Field(min_length=1)
    final_text_plan_id: UUID
    platform_variant_ids: list[UUID] = Field(min_length=1)
    provider_receipt_id: UUID | None = None
    completed_at: datetime


class RenderReceipt(BaseModel):
    schema_version: Literal["cmf.render_receipt.v1"]
    render_receipt_id: UUID
    render_contract_id: UUID | None = None
    renderer_props_bundle_id: UUID | None = None
    deterministic_render_job_id: UUID | None = None
    render_output_id: UUID | None = None
    provider_receipt_id: UUID | None = None
    renderer: DeterministicRenderer | None = None
    props_hash: str | None = None
    input_manifest_hashes: list[str] = Field(default_factory=list)
    renderer_version: str | None = None
    output_hashes: list[str] = Field(default_factory=list)
    final_text_plan_id: UUID | None = None
    duration_seconds: float | None = None
    cost_amount: float | None = Field(default=None, ge=0)
    retry_count: int = Field(ge=0)
    decision_code: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    actor_id: UUID
    command_id: UUID | None = None
    written_at: datetime

    @model_validator(mode="after")
    def successful_receipts_need_output_hashes(self):
        if self.decision_code == "DETERMINISTIC_RENDER_OUTPUT_RECORDED" and not self.output_hashes:
            raise ValueError("successful render receipts require output hashes")
        return self


def deterministic_render_hash(parts: Any) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def deterministic_renderer_typescript_contract() -> str:
    return "\n".join(
        [
            "export type DeterministicRenderer = \"remotion\" | \"motion_canvas\";",
            "",
            "export interface RendererPropsBundleV1 {",
            "  schema_version: \"cmf.renderer_props_bundle.v1\";",
            "  renderer_props_bundle_id: string;",
            "  render_contract_id: string;",
            "  assembly_plan_id: string;",
            "  renderer: DeterministicRenderer;",
            "  layer_manifest_id: string;",
            "  animation_plan_id: string;",
            "  timeline_manifest_id: string;",
            "  caption_manifest_id?: string | null;",
            "  audio_mix_manifest_id?: string | null;",
            "  final_text_plan_id: string;",
            "  brand_context_version_id: string;",
            "  rig_manifest_id: string;",
            "  selected_brand_layer_ids: string[];",
            "  motion_recipe_ids: string[];",
            "  sfx_asset_ids: string[];",
            "  platform_variant_ids: string[];",
            "  props_payload: Record<string, unknown>;",
            "  props_hash: string;",
            "}",
        ]
    )


def new_render_receipt(
    *,
    actor_id: UUID,
    decision_code: str,
    retry_count: int = 0,
    evidence_refs: list[str] | None = None,
    render_contract_id: UUID | None = None,
    renderer_props_bundle_id: UUID | None = None,
    deterministic_render_job_id: UUID | None = None,
    render_output_id: UUID | None = None,
    provider_receipt_id: UUID | None = None,
    renderer: DeterministicRenderer | None = None,
    props_hash: str | None = None,
    input_manifest_hashes: list[str] | None = None,
    renderer_version: str | None = None,
    output_hashes: list[str] | None = None,
    final_text_plan_id: UUID | None = None,
    duration_seconds: float | None = None,
    cost_amount: float | None = None,
    command_id: UUID | None = None,
) -> RenderReceipt:
    return RenderReceipt(
        schema_version="cmf.render_receipt.v1",
        render_receipt_id=uuid4(),
        render_contract_id=render_contract_id,
        renderer_props_bundle_id=renderer_props_bundle_id,
        deterministic_render_job_id=deterministic_render_job_id,
        render_output_id=render_output_id,
        provider_receipt_id=provider_receipt_id,
        renderer=renderer,
        props_hash=props_hash,
        input_manifest_hashes=input_manifest_hashes or [],
        renderer_version=renderer_version,
        output_hashes=output_hashes or [],
        final_text_plan_id=final_text_plan_id,
        duration_seconds=duration_seconds,
        cost_amount=cost_amount,
        retry_count=retry_count,
        decision_code=decision_code,
        evidence_refs=evidence_refs or [],
        actor_id=actor_id,
        command_id=command_id,
        written_at=utc_now(),
    )
