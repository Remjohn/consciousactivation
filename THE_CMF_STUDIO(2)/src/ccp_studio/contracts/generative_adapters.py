"""Generative provider adapter contracts for TS-CMF-044."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


class GenerativeEvaluationState(str, Enum):
    pending_evaluation = "pending_evaluation"
    passed = "passed"
    failed = "failed"
    promotion_blocked = "promotion_blocked"
    promoted = "promoted"


class ProviderMetadata(BaseModel):
    schema_version: Literal["cmf.provider_metadata.v1"]
    provider_name: str = Field(min_length=1)
    model_or_workflow_version: str = Field(min_length=1)
    seed: str | None = None
    config_values: dict[str, Any] = Field(default_factory=dict)
    provider_response_id: str | None = None


class GenerativeProviderRequest(BaseModel):
    schema_version: Literal["cmf.generative_provider_request.v1"]
    generative_provider_request_id: UUID
    provider_capability_id: str = Field(min_length=1)
    organization_id: UUID
    brand_id: UUID
    actor_id: UUID
    purpose: str = Field(min_length=1)
    input_artifact_hashes: list[str] = Field(min_length=1)
    input_types: list[str] = Field(min_length=1)
    prompt_hash: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)
    consent_record_version_ids: list[UUID] = Field(default_factory=list)
    requires_consent_compatibility: bool = False
    evaluation_target_id: UUID | None = None
    idempotency_key: str = Field(min_length=1)
    created_at: datetime

    @model_validator(mode="after")
    def consent_refs_required_for_source_inputs(self):
        if self.requires_consent_compatibility and not self.consent_record_version_ids:
            raise ValueError("consent_record_version_ids are required for source-compatible provider inputs")
        return self


class GenerativeProviderOutput(BaseModel):
    schema_version: Literal["cmf.generative_provider_output.v1"]
    provider_output_id: UUID
    generative_provider_request_id: UUID
    provider_job_id: UUID
    provider_receipt_id: UUID
    raw_output_uri: str = Field(min_length=1)
    output_hash: str = Field(min_length=1)
    metadata: ProviderMetadata
    evaluation_state: GenerativeEvaluationState
    consent_record_version_ids: list[UUID] = Field(default_factory=list)
    promoted_asset_id: UUID | None = None
    created_at: datetime

    @model_validator(mode="after")
    def promotion_requires_passed_state(self):
        if self.promoted_asset_id and self.evaluation_state != GenerativeEvaluationState.promoted:
            raise ValueError("promoted_asset_id requires promoted evaluation state")
        return self


class GenerativeAdapterReceipt(BaseModel):
    schema_version: Literal["cmf.generative_adapter_receipt.v1"]
    generative_adapter_receipt_id: UUID
    generative_provider_request_id: UUID | None = None
    provider_output_id: UUID | None = None
    provider_receipt_id: UUID | None = None
    decision_code: str = Field(min_length=1)
    evaluation_state: GenerativeEvaluationState | None = None
    promoted_asset_id: UUID | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    actor_id: UUID
    command_id: UUID | None = None
    written_at: datetime


def new_generative_adapter_receipt(
    *,
    actor_id: UUID,
    decision_code: str,
    evidence_refs: list[str],
    generative_provider_request_id: UUID | None = None,
    provider_output_id: UUID | None = None,
    provider_receipt_id: UUID | None = None,
    evaluation_state: GenerativeEvaluationState | None = None,
    promoted_asset_id: UUID | None = None,
    command_id: UUID | None = None,
) -> GenerativeAdapterReceipt:
    return GenerativeAdapterReceipt(
        schema_version="cmf.generative_adapter_receipt.v1",
        generative_adapter_receipt_id=uuid4(),
        generative_provider_request_id=generative_provider_request_id,
        provider_output_id=provider_output_id,
        provider_receipt_id=provider_receipt_id,
        decision_code=decision_code,
        evaluation_state=evaluation_state,
        promoted_asset_id=promoted_asset_id,
        evidence_refs=evidence_refs,
        actor_id=actor_id,
        command_id=command_id,
        written_at=utc_now(),
    )


class GPTImage2Parameters(BaseModel):
    schema_version: Literal["cmf.gpt_image_2_parameters.v1"]
    prompt_hash: str = Field(min_length=1)
    aspect_ratio: str = Field(min_length=1)
    seed: str | None = None
    config_values: dict[str, Any] = Field(default_factory=dict)


class Flux2Klein9BParameters(BaseModel):
    schema_version: Literal["cmf.flux_2_klein_9b_parameters.v1"]
    prompt_hash: str = Field(min_length=1)
    edit_mode: str = Field(min_length=1)
    seed: str | None = None
    config_values: dict[str, Any] = Field(default_factory=dict)


class QwenImageLayeredParameters(BaseModel):
    schema_version: Literal["cmf.qwen_image_layered_parameters.v1"]
    layer_strategy: str = Field(min_length=1)
    seed: str | None = None
    config_values: dict[str, Any] = Field(default_factory=dict)


class SAM3Parameters(BaseModel):
    schema_version: Literal["cmf.sam3_parameters.v1"]
    segmentation_target: str = Field(min_length=1)
    tracking_required: bool = False
    config_values: dict[str, Any] = Field(default_factory=dict)


class LavaSRParameters(BaseModel):
    schema_version: Literal["cmf.lavasr_parameters.v1"]
    audio_repair_intent: str = Field(min_length=1)
    config_values: dict[str, Any] = Field(default_factory=dict)


class MossTTSParameters(BaseModel):
    schema_version: Literal["cmf.moss_tts_parameters.v1"]
    bridge_text_hash: str = Field(min_length=1)
    voice_profile_ref: str = Field(min_length=1)
    config_values: dict[str, Any] = Field(default_factory=dict)
