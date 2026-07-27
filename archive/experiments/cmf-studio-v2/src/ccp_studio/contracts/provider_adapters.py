from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class ProviderId(str, Enum):
    FAKE_IMAGE = "fake_image"
    OPENAI_IMAGE = "openai_image"
    IDEOGRAM = "ideogram"
    BFL_FLUX = "bfl_flux"
    QWEN_IMAGE = "qwen_image"
    SEGMENT_ANYTHING = "segment_anything"


class ProviderCapabilityId(str, Enum):
    IMAGE_GENERATE = "image.generate"
    IMAGE_EDIT = "image.edit"
    IMAGE_INPAINT = "image.inpaint"
    IMAGE_REFERENCE_EDIT = "image.reference_edit"
    IMAGE_REMIX = "image.remix"
    IMAGE_DESCRIBE = "image.describe"
    IMAGE_UPSCALE = "image.upscale"
    BACKGROUND_REMOVE = "background.remove"
    OBJECT_SEGMENT = "object.segment"
    MASK_GENERATE = "mask.generate"
    LAYER_DECOMPOSE = "layer.decompose"
    IMAGE_REPAIR = "image.repair"
    IMAGE_OUTPAINT = "image.outpaint"
    SKIA_RENDER = "skia.render"


class ProviderTransportMode(str, Enum):
    DISABLED = "disabled"
    HTTP = "http"
    SDK = "sdk"
    SELF_HOSTED_HTTP = "self_hosted_http"
    RUNNINGHUB_WORKFLOW = "runninghub_workflow"
    COMFYUI_WORKFLOW = "comfyui_workflow"
    LOCAL = "local"
    FAKE = "fake"


class ProviderExecutionStatus(str, Enum):
    CREATED = "created"
    PREFLIGHT_FAILED = "preflight_failed"
    SUBMITTED = "submitted"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProviderOutputType(str, Enum):
    IMAGE = "image"
    IMAGE_LAYER = "image_layer"
    MASK = "mask"
    CUTOUT = "cutout"
    METADATA = "metadata"
    TEXT = "text"


class ProviderErrorCode(str, Enum):
    AUTH_FAILED = "auth_failed"
    RATE_LIMITED = "rate_limited"
    QUOTA_EXCEEDED = "quota_exceeded"
    TIMEOUT = "timeout"
    SERVER_ERROR = "server_error"
    BAD_REQUEST = "bad_request"
    UNSUPPORTED_FRAME_PROFILE = "unsupported_frame_profile"
    UNSUPPORTED_INPUT_ASSET = "unsupported_input_asset"
    MODERATION_BLOCKED = "moderation_blocked"
    PROVIDER_SAFETY_BLOCKED = "provider_safety_blocked"
    DOWNLOAD_FAILED = "download_failed"
    INVALID_OUTPUT = "invalid_output"
    STORAGE_FAILED = "storage_failed"
    PROVIDER_DISABLED = "provider_disabled"
    MISSING_CREDENTIALS = "missing_credentials"
    UNKNOWN = "unknown"


class RetryDecision(str, Enum):
    RETRY = "retry"
    DO_NOT_RETRY = "do_not_retry"
    REPAIR_THEN_RETRY = "repair_then_retry"


class ProviderCredentialRef(BaseModel):
    credential_ref_id: str = Field(default_factory=lambda: new_id("credential_ref"))
    provider_id: ProviderId
    env_var_name: str
    secret_manager_ref: str | None = None


class ProviderAdapterConfig(BaseModel):
    provider_id: ProviderId
    enabled: bool = False
    transport_mode: ProviderTransportMode = ProviderTransportMode.DISABLED
    base_url: str | None = None
    model_name: str | None = None
    credential_ref: ProviderCredentialRef | None = None
    timeout_seconds: int = 120
    max_reference_images: int = 4
    default_headers: dict[str, str] = Field(default_factory=dict)
    extra: dict[str, Any] = Field(default_factory=dict)


class ProviderCapabilityProfile(BaseModel):
    provider_id: ProviderId
    capability_ids: list[ProviderCapabilityId]
    max_reference_images: int = 0
    supports_async: bool = False
    supports_masks: bool = False
    supports_text_rendering: bool = False
    notes: str | None = None


class ProviderAssetInput(BaseModel):
    provider_asset_input_id: str = Field(default_factory=lambda: new_id("provider_asset_input"))
    asset_id: str
    asset_version_id: str | None = None
    uri: str | None = None
    sha256: str | None = None
    mime_type: str | None = None
    use_role: str = "reference"


class ProviderPromptContract(BaseModel):
    prompt_contract_id: str = Field(default_factory=lambda: new_id("prompt_contract"))
    primary_prompt: str
    negative_prompt: str | None = None
    route_id: str
    frame_profile: str
    composition_role: str
    source_reference_ids: list[str] = Field(default_factory=list)
    forbidden_patterns: list[str] = Field(default_factory=list)


class ProviderOutputRequirement(BaseModel):
    output_requirement_id: str = Field(default_factory=lambda: new_id("output_req"))
    output_type: ProviderOutputType = ProviderOutputType.IMAGE
    required: bool = True
    width: int | None = None
    height: int | None = None
    transparent_background: bool = False
    notes: str | None = None


class ProviderExecutionRequest(BaseModel):
    provider_execution_request_id: str = Field(default_factory=lambda: new_id("provider_exec_req"))
    brand_id: str
    brand_context_version_id: str
    provider_id: ProviderId
    provider_capability_id: ProviderCapabilityId
    provider_job_blueprint_id: str
    route_production_spec_id: str
    primary_style_route_id: str
    source_references: list[str] = Field(default_factory=list)
    input_assets: list[ProviderAssetInput] = Field(default_factory=list)
    reference_assets: list[ProviderAssetInput] = Field(default_factory=list)
    frame_profile: str
    composition_role: str
    prompt_contract: ProviderPromptContract
    output_requirements: list[ProviderOutputRequirement] = Field(default_factory=list)
    idempotency_key: str
    budget_limit: float | None = None
    timeout_seconds: int = 120
    operator_approval_ref: str | None = None
    trusted_auto_approval_policy_id: str | None = None
    allow_fake_without_approval: bool = False
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        required = {
            "brand_context_version_id": self.brand_context_version_id,
            "provider_job_blueprint_id": self.provider_job_blueprint_id,
            "route_production_spec_id": self.route_production_spec_id,
            "primary_style_route_id": self.primary_style_route_id,
            "frame_profile": self.frame_profile,
            "composition_role": self.composition_role,
            "idempotency_key": self.idempotency_key,
        }
        missing = [key for key, value in required.items() if not value]
        if missing:
            raise ValueError(f"ProviderExecutionRequest missing required fields: {missing}")
        if not (self.source_references or self.input_assets or self.reference_assets):
            raise ValueError("ProviderExecutionRequest requires source/reference/input assets")
        approved = self.operator_approval_ref or self.trusted_auto_approval_policy_id
        if not approved and not (self.provider_id == ProviderId.FAKE_IMAGE and self.allow_fake_without_approval):
            raise ValueError("real provider calls require operator_approval_ref or trusted_auto_approval_policy_id")


class ProviderPreflightReport(BaseModel):
    provider_preflight_report_id: str = Field(default_factory=lambda: new_id("provider_preflight"))
    request_id: str
    provider_id: ProviderId
    capability_id: ProviderCapabilityId
    pass_status: bool
    missing_requirements: list[str] = Field(default_factory=list)
    blocker_codes: list[ProviderErrorCode] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ProviderCostEstimate(BaseModel):
    provider_cost_estimate_id: str = Field(default_factory=lambda: new_id("provider_cost"))
    request_id: str
    provider_id: ProviderId
    estimated_cost_usd: float | None = None
    estimated_units: int | None = None
    notes: str | None = None


class ProviderSubmissionReceipt(BaseModel):
    provider_submission_receipt_id: str = Field(default_factory=lambda: new_id("provider_submit"))
    request_id: str
    provider_id: ProviderId
    provider_request_id: str
    request_payload_hash: str
    idempotency_key: str
    status: ProviderExecutionStatus = ProviderExecutionStatus.SUBMITTED
    submitted_at: str = Field(default_factory=_now_iso)
    raw_response_redacted: dict[str, Any] = Field(default_factory=dict)


class ProviderPollReceipt(BaseModel):
    provider_poll_receipt_id: str = Field(default_factory=lambda: new_id("provider_poll"))
    request_id: str
    provider_id: ProviderId
    provider_request_id: str
    status: ProviderExecutionStatus
    output_urls: list[str] = Field(default_factory=list)
    provider_output_refs: list[str] = Field(default_factory=list)
    raw_response_redacted: dict[str, Any] = Field(default_factory=dict)
    polled_at: str = Field(default_factory=_now_iso)


class ProviderOutputAsset(BaseModel):
    provider_output_asset_id: str = Field(default_factory=lambda: new_id("provider_output"))
    request_id: str
    provider_id: ProviderId
    output_type: ProviderOutputType
    uri: str
    sha256: str
    mime_type: str = "image/png"
    byte_size: int | None = None
    width: int | None = None
    height: int | None = None
    provider_model: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProviderDownloadReceipt(BaseModel):
    provider_download_receipt_id: str = Field(default_factory=lambda: new_id("provider_download"))
    request_id: str
    provider_id: ProviderId
    output_asset_ids: list[str]
    downloaded_at: str = Field(default_factory=_now_iso)


class ProviderJobReceipt(BaseModel):
    provider_job_receipt_id: str = Field(default_factory=lambda: new_id("provider_job_receipt"))
    request_id: str
    provider_id: ProviderId
    provider_capability_id: ProviderCapabilityId
    provider_request_id: str
    status: ProviderExecutionStatus
    output_assets: list[ProviderOutputAsset] = Field(default_factory=list)
    submission_receipt_id: str | None = None
    poll_receipt_id: str | None = None
    download_receipt_id: str | None = None
    error_receipt_id: str | None = None
    route_production_spec_id: str
    provider_job_blueprint_id: str
    primary_style_route_id: str
    frame_profile: str
    composition_role: str
    created_at: str = Field(default_factory=_now_iso)


class ProviderErrorReceipt(BaseModel):
    provider_error_receipt_id: str = Field(default_factory=lambda: new_id("provider_error"))
    provider_id: ProviderId
    provider_request_id: str | None = None
    provider_status_code: int | None = None
    provider_error_code: str | None = None
    normalized_error_code: ProviderErrorCode
    retry_decision: RetryDecision
    retryable: bool
    user_correctable: bool
    safe_to_retry: bool
    message: str
    request_id: str | None = None
    moderation_stage: str | None = None
    raw_error_redacted: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=_now_iso)


class ProviderRetryPolicy(BaseModel):
    provider_id: ProviderId
    max_attempts: int = 3
    initial_backoff_seconds: float = 1.0
    max_backoff_seconds: float = 30.0
    retryable_codes: list[ProviderErrorCode] = Field(default_factory=lambda: [
        ProviderErrorCode.RATE_LIMITED,
        ProviderErrorCode.TIMEOUT,
        ProviderErrorCode.SERVER_ERROR,
    ])


class ProviderModerationReceipt(BaseModel):
    provider_moderation_receipt_id: str = Field(default_factory=lambda: new_id("provider_moderation"))
    request_id: str
    provider_id: ProviderId
    blocked: bool
    reason: str | None = None
    stage: str = "pre_submit"
    created_at: str = Field(default_factory=_now_iso)


class ProviderAdapterHealth(BaseModel):
    provider_id: ProviderId
    enabled: bool
    configured: bool
    credential_present: bool
    last_checked_at: str = Field(default_factory=_now_iso)
    notes: str | None = None
