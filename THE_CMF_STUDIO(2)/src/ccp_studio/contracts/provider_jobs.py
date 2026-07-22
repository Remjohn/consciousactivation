"""Provider capability and receipt contracts for TS-CMF-042."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.orchestration import utc_now


class ProviderJobStatus(str, Enum):
    requested = "requested"
    submitted = "submitted"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"
    cancelled = "cancelled"


class ProviderCostPolicy(BaseModel):
    schema_version: Literal["cmf.provider_cost_policy.v1"]
    cost_policy_id: str = Field(min_length=1)
    max_cost_amount: float = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3)
    requires_estimate: bool = True


class ProviderRetryPolicy(BaseModel):
    schema_version: Literal["cmf.provider_retry_policy.v1"]
    retry_policy_id: str = Field(min_length=1)
    max_retries: int = Field(ge=0)
    retryable_failure_codes: list[str] = Field(default_factory=list)


class ProviderCapabilityRecord(BaseModel):
    schema_version: Literal["cmf.provider_capability_record.v1"]
    provider_capability_id: str = Field(min_length=1)
    provider_name: str = Field(min_length=1)
    capability_name: str = Field(min_length=1)
    model_or_workflow_version: str = Field(min_length=1)
    allowed_input_types: list[str] = Field(min_length=1)
    output_contract: str = Field(min_length=1)
    cost_policy_id: str = Field(min_length=1)
    retry_policy_id: str = Field(min_length=1)
    evaluation_requirement_ids: list[str] = Field(min_length=1)
    execution_environment: str = Field(min_length=1)
    governance_notes: list[str] = Field(default_factory=list)
    active: bool
    activated_at: datetime


class ProviderRequest(BaseModel):
    schema_version: Literal["cmf.provider_request.v1"]
    provider_request_id: UUID
    provider_capability_id: str = Field(min_length=1)
    organization_id: UUID
    brand_id: UUID
    requested_by_actor_id: UUID
    complete_editing_session_id: UUID | None = None
    scene_spec_id: UUID | None = None
    input_artifact_hashes: list[str] = Field(min_length=1)
    input_types: list[str] = Field(min_length=1)
    prompt_hash: str | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)
    idempotency_key: str = Field(min_length=1)
    correlation_id: UUID
    requested_at: datetime

    @model_validator(mode="after")
    def prompt_hash_required_when_prompt_is_present(self):
        if any(key in self.parameters for key in {"prompt", "compiled_prompt", "prompt_ref"}) and not self.prompt_hash:
            raise ValueError("prompt_hash is required when prompt parameters are submitted")
        return self


class ProviderJob(BaseModel):
    schema_version: Literal["cmf.provider_job.v1"]
    provider_job_id: UUID
    provider_request_id: UUID
    provider_capability_id: str = Field(min_length=1)
    provider_name: str = Field(min_length=1)
    capability_name: str = Field(min_length=1)
    model_or_workflow_version: str = Field(min_length=1)
    status: ProviderJobStatus
    provider_correlation_id: str | None = None
    retry_count: int = Field(ge=0)
    cost_policy_id: str = Field(min_length=1)
    retry_policy_id: str = Field(min_length=1)
    evaluation_requirement_ids: list[str] = Field(min_length=1)
    request_hash: str = Field(min_length=1)
    submitted_at: datetime
    updated_at: datetime


class ProviderResponse(BaseModel):
    schema_version: Literal["cmf.provider_response.v1"]
    provider_response_id: UUID
    provider_job_id: UUID
    provider_correlation_id: str = Field(min_length=1)
    status: ProviderJobStatus
    output_artifact_hashes: list[str] = Field(default_factory=list)
    cost_amount: float | None = Field(default=None, ge=0)
    failure_code: str | None = None
    response_metadata: dict[str, Any] = Field(default_factory=dict)
    received_at: datetime


class ProviderReceipt(BaseModel):
    schema_version: Literal["cmf.provider_receipt.v2"]
    provider_receipt_id: UUID
    provider_job_id: UUID
    provider_request_id: UUID
    provider_capability_id: str = Field(min_length=1)
    provider_name: str = Field(min_length=1)
    capability_name: str = Field(min_length=1)
    model_or_workflow_version: str = Field(min_length=1)
    status: ProviderJobStatus
    output_artifact_hashes: list[str] = Field(default_factory=list)
    cost_amount: float | None = Field(default=None, ge=0)
    retry_count: int = Field(ge=0)
    failure_code: str | None = None
    request_hash: str = Field(min_length=1)
    response_hash: str = Field(min_length=1)
    provider_correlation_id: str = Field(min_length=1)
    created_domain_event_type: str = Field(min_length=1)
    created_at: datetime

    @model_validator(mode="after")
    def receipt_must_prove_terminal_state(self):
        if self.status == ProviderJobStatus.succeeded and not self.output_artifact_hashes:
            raise ValueError("successful provider receipts require output artifact hashes")
        if self.status == ProviderJobStatus.failed and not self.failure_code:
            raise ValueError("failed provider receipts require a failure_code")
        return self


class ProviderWebhookEnvelope(BaseModel):
    schema_version: Literal["cmf.provider_webhook_envelope.v1"]
    provider_webhook_id: UUID
    provider_name: str = Field(min_length=1)
    provider_correlation_id: str = Field(min_length=1)
    payload: dict[str, Any]
    idempotency_key: str = Field(min_length=1)
    received_at: datetime


class ProviderDomainEvent(BaseModel):
    schema_version: Literal["cmf.provider_domain_event.v1"]
    provider_event_id: UUID
    event_type: str = Field(min_length=1)
    provider_job_id: UUID
    provider_receipt_id: UUID | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime


def provider_hash(parts: Any) -> str:
    payload = json.dumps(parts, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def new_provider_request(
    *,
    provider_capability_id: str,
    organization_id: UUID,
    brand_id: UUID,
    requested_by_actor_id: UUID,
    input_artifact_hashes: list[str],
    input_types: list[str],
    idempotency_key: str,
    correlation_id: UUID,
    complete_editing_session_id: UUID | None = None,
    scene_spec_id: UUID | None = None,
    prompt_hash: str | None = None,
    parameters: dict[str, Any] | None = None,
) -> ProviderRequest:
    return ProviderRequest(
        schema_version="cmf.provider_request.v1",
        provider_request_id=uuid4(),
        provider_capability_id=provider_capability_id,
        organization_id=organization_id,
        brand_id=brand_id,
        requested_by_actor_id=requested_by_actor_id,
        complete_editing_session_id=complete_editing_session_id,
        scene_spec_id=scene_spec_id,
        input_artifact_hashes=input_artifact_hashes,
        input_types=input_types,
        prompt_hash=prompt_hash,
        parameters=parameters or {},
        idempotency_key=idempotency_key,
        correlation_id=correlation_id,
        requested_at=utc_now(),
    )
