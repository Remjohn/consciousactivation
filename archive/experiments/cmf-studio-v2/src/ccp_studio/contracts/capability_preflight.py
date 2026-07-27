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


class CapabilityKind(str, Enum):
    PROVIDER = "provider"
    RUNTIME = "runtime"
    TOOL = "tool"
    STORAGE = "storage"
    WORKER = "worker"


class CapabilityState(str, Enum):
    AVAILABLE = "available"
    CONFIGURED = "configured"
    MISSING = "missing"
    DEGRADED = "degraded"
    BLOCKED = "blocked"
    UNAVAILABLE = "unavailable"


class PreflightPassStatus(str, Enum):
    PASS = "pass"
    DEGRADED = "degraded"
    BLOCKED = "blocked"


class ProviderName(str, Enum):
    IDEOGRAM = "ideogram"
    FLUX = "flux"
    OPENAI_IMAGE = "openai_image"
    RUNNINGHUB = "runninghub"
    COMFYUI = "comfyui"
    LOCAL_STUB = "local_stub"


class ProviderRole(str, Enum):
    COMPOSITION_PLATE_GENERATOR = "composition_plate_generator"
    REFERENCE_BASED_OBJECT_EDITOR = "reference_based_object_editor"
    IMAGE_PROVIDER = "image_provider"
    WORKFLOW_PROVIDER = "workflow_provider"
    FALLBACK_PROVIDER = "fallback_provider"


class RuntimeName(str, Enum):
    REMOTION = "remotion"
    FFMPEG = "ffmpeg"
    FFPROBE = "ffprobe"
    HYPERFRAMES = "hyperframes"
    MOTION_CANVAS = "motion_canvas"
    LOCAL_RENDER_WORKER = "local_render_worker"
    PYTHON = "python"


class PipelineId(str, Enum):
    FORMAT02_GOLDEN_PATH = "format02_golden_path"
    FORMAT02_PROVIDER_SCENE_BATCH = "format02_provider_scene_batch"
    AVATAR_64_STATE_LIBRARY_GENERATION = "avatar_64_state_library_generation"
    VIDEO_REAL_RENDER = "video_real_render"
    TEMPLATE_PREVIEW = "template_preview"


class CostEstimate(BaseModel):
    cost_estimate_id: str = Field(default_factory=lambda: new_id("cost_estimate"))
    min_usd: float = Field(default=0.0, ge=0.0)
    max_usd: float = Field(default=0.0, ge=0.0)
    unit: str = "run"
    notes: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.max_usd < self.min_usd:
            raise ValueError("max_usd cannot be less than min_usd")


class SetupOffer(BaseModel):
    setup_offer_id: str = Field(default_factory=lambda: new_id("setup_offer"))
    capability_id: str
    title: str
    steps: list[str]
    optional: bool = False
    estimated_minutes: int = Field(default=5, ge=0)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.capability_id:
            raise ValueError("SetupOffer requires capability_id")
        if not self.steps:
            raise ValueError("SetupOffer requires setup steps")


class MissingCapabilityBlocker(BaseModel):
    missing_capability_blocker_id: str = Field(default_factory=lambda: new_id("missing_capability"))
    capability_id: str
    reason: str
    blocks_pipeline: bool = True
    setup_offer_id: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.capability_id:
            raise ValueError("MissingCapabilityBlocker requires capability_id")
        if self.blocks_pipeline and not self.reason:
            raise ValueError("Blocking missing capability requires reason")


class ToolSupportEnvelope(BaseModel):
    tool_support_envelope_id: str = Field(default_factory=lambda: new_id("tool_support"))
    capability_id: str
    kind: CapabilityKind
    display_name: str
    configured: bool = False
    available: bool = False
    required: bool = False
    degraded: bool = False
    missing_reasons: list[str] = Field(default_factory=list)
    supports: list[str] = Field(default_factory=list)
    setup_offer_id: str | None = None
    provider_calls_executed: bool = False
    runtime_calls_executed: bool = False

    @property
    def state(self) -> CapabilityState:
        if self.required and not self.configured:
            return CapabilityState.MISSING
        if self.configured and not self.available:
            return CapabilityState.DEGRADED
        if self.degraded:
            return CapabilityState.DEGRADED
        if self.configured and self.available:
            return CapabilityState.AVAILABLE
        return CapabilityState.UNAVAILABLE

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.capability_id:
            raise ValueError("ToolSupportEnvelope requires capability_id")
        if self.available and not self.configured:
            raise ValueError("Tool cannot be available unless configured")
        if self.provider_calls_executed or self.runtime_calls_executed:
            raise ValueError("Capability preflight must not execute providers or runtimes")


class ProviderAvailabilityReport(BaseModel):
    provider_availability_report_id: str = Field(default_factory=lambda: new_id("provider_report"))
    provider_name: ProviderName
    provider_role: ProviderRole
    capability_id: str
    configured: bool
    available: bool
    missing_secrets: list[str] = Field(default_factory=list)
    degraded_reasons: list[str] = Field(default_factory=list)
    sample_required: bool = True
    sample_approved: bool = False
    batch_requested: bool = False
    estimated_cost: CostEstimate = Field(default_factory=CostEstimate)
    setup_offer_id: str | None = None
    provider_calls_executed: bool = False

    @property
    def status(self) -> CapabilityState:
        if self.missing_secrets:
            return CapabilityState.MISSING
        if self.configured and self.available and self.degraded_reasons:
            return CapabilityState.DEGRADED
        if self.configured and self.available:
            return CapabilityState.AVAILABLE
        if self.configured and not self.available:
            return CapabilityState.DEGRADED
        return CapabilityState.MISSING

    @property
    def batch_blocked(self) -> bool:
        return self.batch_requested and self.sample_required and not self.sample_approved

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.available and not self.configured:
            raise ValueError("Provider cannot be available unless configured")
        if self.missing_secrets and self.available:
            raise ValueError("Provider cannot be available with missing secrets")
        if self.provider_calls_executed:
            raise ValueError("Provider availability preflight must not execute provider calls")


class RuntimeAvailabilityReport(BaseModel):
    runtime_availability_report_id: str = Field(default_factory=lambda: new_id("runtime_report"))
    runtime_name: RuntimeName
    capability_id: str
    configured: bool
    available: bool
    version: str | None = None
    executable_path: str | None = None
    local: bool = True
    degraded_reasons: list[str] = Field(default_factory=list)
    supports: list[str] = Field(default_factory=list)
    setup_offer_id: str | None = None
    runtime_calls_executed: bool = False

    @property
    def status(self) -> CapabilityState:
        if self.configured and self.available and self.degraded_reasons:
            return CapabilityState.DEGRADED
        if self.configured and self.available:
            return CapabilityState.AVAILABLE
        if self.configured and not self.available:
            return CapabilityState.DEGRADED
        return CapabilityState.MISSING

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.available and not self.configured:
            raise ValueError("Runtime cannot be available unless configured")
        if self.runtime_calls_executed:
            raise ValueError("Runtime preflight must not execute runtime calls")


class ProviderMenuSummary(BaseModel):
    provider_menu_summary_id: str = Field(default_factory=lambda: new_id("provider_menu"))
    provider_reports: list[ProviderAvailabilityReport]
    configured_count: int = 0
    missing_count: int = 0
    degraded_count: int = 0
    available_count: int = 0
    blocked_count: int = 0
    estimated_cost_min_usd: float = 0.0
    estimated_cost_max_usd: float = 0.0
    sample_required: bool = False
    sample_approved: bool = False
    recommended_provider_ids: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        reports = self.provider_reports
        self.configured_count = sum(1 for report in reports if report.configured)
        self.available_count = sum(1 for report in reports if report.status == CapabilityState.AVAILABLE)
        self.missing_count = sum(1 for report in reports if report.status == CapabilityState.MISSING)
        self.degraded_count = sum(1 for report in reports if report.status == CapabilityState.DEGRADED)
        self.blocked_count = sum(1 for report in reports if report.batch_blocked)
        self.estimated_cost_min_usd = sum(report.estimated_cost.min_usd for report in reports)
        self.estimated_cost_max_usd = sum(report.estimated_cost.max_usd for report in reports)
        self.sample_required = any(report.sample_required for report in reports)
        self.sample_approved = all((not report.sample_required) or report.sample_approved for report in reports)
        if not self.recommended_provider_ids:
            self.recommended_provider_ids = [
                report.capability_id for report in reports if report.status == CapabilityState.AVAILABLE
            ]


class PipelineCapabilityStatus(BaseModel):
    pipeline_capability_status_id: str = Field(default_factory=lambda: new_id("pipeline_status"))
    pipeline_id: PipelineId
    pass_status: PreflightPassStatus
    required_capability_ids: list[str]
    available_required_capability_ids: list[str] = Field(default_factory=list)
    missing_required_capability_ids: list[str] = Field(default_factory=list)
    degraded_required_capability_ids: list[str] = Field(default_factory=list)
    optional_missing_capability_ids: list[str] = Field(default_factory=list)
    batch_blocked: bool = False
    sample_required: bool = False
    sample_approved: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.missing_required_capability_ids and self.pass_status != PreflightPassStatus.BLOCKED:
            raise ValueError("Missing required capabilities must block pipeline")
        if self.batch_blocked and self.pass_status != PreflightPassStatus.BLOCKED:
            raise ValueError("Batch blocked requires blocked preflight status")


class CapabilityPreflightReport(BaseModel):
    capability_preflight_report_id: str = Field(default_factory=lambda: new_id("preflight_report"))
    pipeline_id: PipelineId
    pipeline_status: PipelineCapabilityStatus
    provider_menu_summary: ProviderMenuSummary
    runtime_reports: list[RuntimeAvailabilityReport] = Field(default_factory=list)
    tool_support: list[ToolSupportEnvelope] = Field(default_factory=list)
    setup_offers: list[SetupOffer] = Field(default_factory=list)
    missing_blockers: list[MissingCapabilityBlocker] = Field(default_factory=list)
    total_estimated_cost: CostEstimate = Field(default_factory=CostEstimate)
    sample_required: bool = False
    sample_approved: bool = False
    provider_calls_executed: bool = False
    runtime_calls_executed: bool = False
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.provider_calls_executed or self.runtime_calls_executed:
            raise ValueError("CapabilityPreflightReport cannot execute providers or runtimes")
        if self.missing_blockers and self.pipeline_status.pass_status != PreflightPassStatus.BLOCKED:
            raise ValueError("Missing blockers require blocked pipeline status")
        self.total_estimated_cost = CostEstimate(
            min_usd=self.provider_menu_summary.estimated_cost_min_usd,
            max_usd=self.provider_menu_summary.estimated_cost_max_usd,
            unit="preflight",
            notes="Sum of configured provider estimates in menu summary",
        )
        self.sample_required = self.provider_menu_summary.sample_required
        self.sample_approved = self.provider_menu_summary.sample_approved
