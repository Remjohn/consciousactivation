from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4
import hashlib
from pydantic import BaseModel, Field


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class ProviderName(str, Enum):
    IDEOGRAM = "ideogram"
    FLUX = "flux"


class ProviderRole(str, Enum):
    COMPOSITION_PLATE_GENERATOR = "composition_plate_generator"
    REFERENCE_BASED_OBJECT_EDITOR = "reference_based_object_editor"


class ProviderCapabilityStatus(str, Enum):
    AVAILABLE = "available"
    CONFIGURED = "configured"
    UNTESTED = "untested"
    MISSING = "missing"
    DEGRADED = "degraded"


class ProviderJobKind(str, Enum):
    SCENE_SAMPLE = "scene_sample"
    FACE_PLATE_SAMPLE = "face_plate_sample"
    TEMPLATE_PREVIEW_SAMPLE = "template_preview_sample"
    COMPOSITION_PLATE_BATCH = "composition_plate_batch"
    REFERENCE_EDIT_BATCH = "reference_edit_batch"
    SINGLE_COMPOSITION_PLATE = "single_composition_plate"
    SINGLE_REFERENCE_EDIT = "single_reference_edit"


class ProviderJobStatus(str, Enum):
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED = "blocked"


class ProviderExecutionMode(str, Enum):
    FAKE = "fake"
    REAL_PROVIDER = "real_provider"


class ProviderOutputAssetRole(str, Enum):
    COMPOSITION_PLATE = "composition_plate"
    REFERENCE_EDIT = "reference_edit"
    FACE_PLATE = "face_plate"
    TEMPLATE_PREVIEW = "template_preview"
    REAL_LIFE_CUTOUT = "real_life_cutout"
    PROOF_OBJECT = "proof_object"


class PassStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class ProviderCostEstimate(BaseModel):
    provider_cost_estimate_id: str = Field(default_factory=lambda: new_id("provider_cost"))
    provider_name: ProviderName
    job_kind: ProviderJobKind
    unit_count: int = Field(default=1, ge=1)
    min_usd: float = Field(default=0.0, ge=0.0)
    max_usd: float = Field(default=0.0, ge=0.0)
    currency: str = "USD"
    notes: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.max_usd < self.min_usd:
            raise ValueError("ProviderCostEstimate max_usd cannot be less than min_usd")


class ProviderCapabilityProfile(BaseModel):
    provider_capability_profile_id: str = Field(default_factory=lambda: new_id("provider_capability"))
    provider_name: ProviderName
    provider_role: ProviderRole
    capability_id: str
    configured: bool = False
    tested: bool = False
    available: bool = False
    supported_job_kinds: list[ProviderJobKind]
    model_family: str | None = None
    provider_calls_executed: bool = False

    @property
    def status(self) -> ProviderCapabilityStatus:
        if self.available:
            return ProviderCapabilityStatus.AVAILABLE
        if self.configured and not self.tested:
            return ProviderCapabilityStatus.UNTESTED
        if self.configured:
            return ProviderCapabilityStatus.CONFIGURED
        return ProviderCapabilityStatus.MISSING

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.capability_id:
            raise ValueError("ProviderCapabilityProfile requires capability_id")
        if self.available and (not self.configured or not self.tested):
            raise ValueError("Provider capability cannot be available unless configured and tested")
        if self.provider_calls_executed:
            raise ValueError("Provider capability profile must not execute provider calls")


class ProviderRetryPolicy(BaseModel):
    provider_retry_policy_id: str = Field(default_factory=lambda: new_id("provider_retry"))
    max_attempts: int = Field(default=2, ge=1, le=5)
    retry_backoff_seconds: int = Field(default=30, ge=0)
    retry_on_transient_failure: bool = True
    retry_on_policy_failure: bool = False
    retry_on_sample_rejection: bool = False

    def can_attempt(self, attempt_number: int) -> bool:
        return 1 <= attempt_number <= self.max_attempts


class ProviderSampleApprovalGate(BaseModel):
    provider_sample_approval_gate_id: str = Field(default_factory=lambda: new_id("sample_gate"))
    scene_sample_approved: bool = False
    face_plate_sample_approved: bool = False
    template_preview_sample_approved: bool = False
    approved_by: str | None = None
    blockers: list[str] = Field(default_factory=list)
    notes: str | None = None

    @property
    def batch_approved(self) -> bool:
        return (
            self.scene_sample_approved
            and self.face_plate_sample_approved
            and self.template_preview_sample_approved
            and not self.blockers
            and bool(self.approved_by)
        )

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blockers and self.scene_sample_approved and self.face_plate_sample_approved and self.template_preview_sample_approved:
            raise ValueError("Sample approval gate cannot approve all samples with blockers")


class ProviderDecisionLog(BaseModel):
    provider_decision_log_id: str = Field(default_factory=lambda: new_id("provider_decision"))
    provider_name: ProviderName
    provider_role: ProviderRole
    job_kind: ProviderJobKind
    decision_reason: str
    alternatives_considered: list[str] = Field(default_factory=list)
    sample_or_batch: str
    operator_approved: bool = False
    cost_estimate: ProviderCostEstimate
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.decision_reason:
            raise ValueError("ProviderDecisionLog requires decision_reason")
        if self.sample_or_batch not in {"sample", "batch", "single"}:
            raise ValueError("sample_or_batch must be sample, batch, or single")
        if self.cost_estimate.provider_name != self.provider_name:
            raise ValueError("Decision log cost estimate provider mismatch")


class ProviderJobInput(BaseModel):
    provider_job_input_id: str = Field(default_factory=lambda: new_id("provider_input"))
    provider_name: ProviderName
    provider_role: ProviderRole
    job_kind: ProviderJobKind
    input_payload: dict[str, Any]
    source_refs: list[str]
    reference_asset_refs: list[str] = Field(default_factory=list)
    template_preview_refs: list[str] = Field(default_factory=list)
    composition_scene_refs: list[str] = Field(default_factory=list)
    avatar_asset_refs: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.input_payload:
            raise ValueError("ProviderJobInput requires input_payload")
        if not self.source_refs:
            raise ValueError("ProviderJobInput requires source_refs")
        if self.provider_name == ProviderName.IDEOGRAM and self.provider_role != ProviderRole.COMPOSITION_PLATE_GENERATOR:
            raise ValueError("Ideogram role must be composition_plate_generator")
        if self.provider_name == ProviderName.FLUX and self.provider_role != ProviderRole.REFERENCE_BASED_OBJECT_EDITOR:
            raise ValueError("Flux role must be reference_based_object_editor")


class ProviderJob(BaseModel):
    provider_job_id: str = Field(default_factory=lambda: new_id("provider_job"))
    provider_name: ProviderName
    provider_role: ProviderRole
    job_kind: ProviderJobKind
    job_input: ProviderJobInput
    capability_profile_id: str
    decision_log: ProviderDecisionLog
    retry_policy: ProviderRetryPolicy = Field(default_factory=ProviderRetryPolicy)
    sample_approval_gate: ProviderSampleApprovalGate | None = None
    status: ProviderJobStatus = ProviderJobStatus.CREATED
    execution_mode: ProviderExecutionMode = ProviderExecutionMode.FAKE
    provider_calls_allowed: bool = False
    batch_requested: bool = False
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.provider_calls_allowed:
            raise ValueError("Provider Runtime V1 cannot allow provider calls")
        if self.execution_mode != ProviderExecutionMode.FAKE:
            raise ValueError("Provider Runtime V1 supports fake execution only")
        if self.job_input.provider_name != self.provider_name or self.job_input.provider_role != self.provider_role:
            raise ValueError("ProviderJob input mismatch")
        if self.decision_log.provider_name != self.provider_name:
            raise ValueError("ProviderJob decision log provider mismatch")
        if self.batch_requested or self.job_kind in {ProviderJobKind.COMPOSITION_PLATE_BATCH, ProviderJobKind.REFERENCE_EDIT_BATCH}:
            if not self.sample_approval_gate or not self.sample_approval_gate.batch_approved:
                raise ValueError("Batch provider job requires approved scene, face plate, and template preview samples")


class ProviderJobAttempt(BaseModel):
    provider_job_attempt_id: str = Field(default_factory=lambda: new_id("provider_attempt"))
    provider_job_id: str
    attempt_number: int = Field(ge=1)
    retry_policy: ProviderRetryPolicy
    status: ProviderJobStatus
    error_message: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.retry_policy.can_attempt(self.attempt_number):
            raise ValueError("Provider job attempt exceeds retry policy")


class ProviderJobOutput(BaseModel):
    provider_job_output_id: str = Field(default_factory=lambda: new_id("provider_output"))
    provider_job_id: str
    provider_name: ProviderName
    job_kind: ProviderJobKind
    output_uri: str
    output_sha256: str
    output_payload: dict[str, Any] = Field(default_factory=dict)
    fake_output: bool = True
    provider_calls_executed: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.output_uri or not self.output_sha256:
            raise ValueError("ProviderJobOutput requires output_uri and output_sha256")
        if self.provider_calls_executed:
            raise ValueError("ProviderJobOutput cannot execute provider calls in V1")
        if not self.fake_output:
            raise ValueError("Provider Runtime V1 outputs are fake only")


class ProviderJobReceipt(BaseModel):
    provider_job_receipt_id: str = Field(default_factory=lambda: new_id("provider_receipt"))
    provider_job_id: str
    provider_job_output_id: str | None = None
    provider_name: ProviderName
    job_kind: ProviderJobKind
    status: ProviderJobStatus
    pass_status: PassStatus
    cost_estimate: ProviderCostEstimate
    decision_log_id: str
    fake_execution: bool = True
    provider_calls_executed: bool = False
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.provider_calls_executed:
            raise ValueError("ProviderJobReceipt cannot execute provider calls in V1")
        if not self.fake_execution:
            raise ValueError("Provider Runtime V1 receipts are fake_execution=True")
        if self.blockers and self.pass_status == PassStatus.PASS:
            raise ValueError("ProviderJobReceipt cannot pass with blockers")
        if self.status == ProviderJobStatus.SUCCEEDED and not self.provider_job_output_id:
            raise ValueError("Succeeded provider receipt requires output id")


class ProviderOutputAssetRef(BaseModel):
    provider_output_asset_ref_id: str = Field(default_factory=lambda: new_id("provider_asset"))
    provider_job_id: str
    provider_job_receipt_id: str
    provider_job_output_id: str
    provider_name: ProviderName
    asset_role: ProviderOutputAssetRole
    asset_uri: str
    sha256: str
    source_refs: list[str]
    workspace_artifact_ref_id: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.provider_job_receipt_id:
            raise ValueError("ProviderOutputAssetRef requires provider_job_receipt_id")
        if not self.sha256:
            raise ValueError("ProviderOutputAssetRef requires sha256")
        if not self.source_refs:
            raise ValueError("ProviderOutputAssetRef requires source_refs")


class ProviderBatchPolicyReceipt(BaseModel):
    provider_batch_policy_receipt_id: str = Field(default_factory=lambda: new_id("batch_policy"))
    sample_gate: ProviderSampleApprovalGate
    batch_requested: bool
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        blockers = list(self.blockers)
        if self.batch_requested and not self.sample_gate.batch_approved:
            blockers.append("batch_requires_scene_face_plate_and_template_sample_approval")
        self.blockers = sorted(set(blockers))
        self.pass_status = PassStatus.FAIL if self.blockers else PassStatus.PASS


class ProviderRuntimePlan(BaseModel):
    provider_runtime_plan_id: str = Field(default_factory=lambda: new_id("provider_runtime_plan"))
    provider_jobs: list[ProviderJob]
    sample_approval_gate: ProviderSampleApprovalGate
    batch_policy_receipt: ProviderBatchPolicyReceipt
    estimated_total_cost: ProviderCostEstimate

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.provider_jobs:
            raise ValueError("ProviderRuntimePlan requires provider_jobs")
        if self.batch_policy_receipt.pass_status == PassStatus.FAIL:
            raise ValueError("ProviderRuntimePlan cannot compile with failed batch policy")
