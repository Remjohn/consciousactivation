from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from pathlib import PurePosixPath
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


def validate_workspace_relative_path(value: str, field_name: str = "path") -> str:
    if not value:
        raise ValueError(f"{field_name} is required")
    normalized = value.replace("\\", "/")
    pure = PurePosixPath(normalized)
    if pure.is_absolute():
        raise ValueError(f"{field_name} cannot be absolute")
    if ".." in pure.parts or any(part in {"", "."} for part in pure.parts):
        raise ValueError(f"{field_name} cannot contain path traversal/current/empty parts")
    return str(pure)


class PassStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class RenderExecutionMode(str, Enum):
    DRY_RUN = "dry_run"
    REAL_LOCAL = "real_local"


class RenderJobStatus(str, Enum):
    PLANNED = "planned"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED = "blocked"


class RemotionCodec(str, Enum):
    H264 = "h264"
    H265 = "h265"
    PRORES = "prores"


class FFmpegCodec(str, Enum):
    H264 = "libx264"
    H265 = "libx265"
    PRORES = "prores_ks"


class RenderLayerName(str, Enum):
    BACKGROUND = "background"
    PROOF_OBJECT = "proof_object"
    REAL_LIFE_CUTOUT = "real_life_cutout"
    AVATAR = "avatar"
    TEXT = "text"
    ANNOTATION = "annotation"
    FOREGROUND_FX = "foreground_fx"


class VideoFormatId(str, Enum):
    FORMAT_01 = "format_01_cinematic_story"
    FORMAT_02 = "format_02_avatar_papercut_explainer"
    FORMAT_03 = "format_03_living_commentary_reactions"
    FORMAT_04 = "format_04_conscious_reactions_editing"


class MotionCueName(str, Enum):
    SLOW_PUSH = "slow_push"
    PAPER_SLIDE_IN = "paper_slide_in"
    SETTLE = "settle"
    SUBTLE_PARALLAX = "subtle_parallax"
    TEXT_REVEAL = "text_reveal"
    AVATAR_GESTURE = "avatar_gesture"
    PROXY_BOUNCE = "proxy_bounce"
    ROUGH_NOTATION_DRAW = "rough_notation_draw"
    SNAP_ZOOM = "snap_zoom"
    AI_LIQUID_MORPH = "ai_liquid_morph"
    OBJECT_WARP = "object_warp"
    UNMOTIVATED_SHAKE = "unmotivated_shake"


class RenderCommandPlan(BaseModel):
    render_command_plan_id: str = Field(default_factory=lambda: new_id("command_plan"))
    executable: str
    args: list[str]
    cwd: str | None = None
    environment_keys: list[str] = Field(default_factory=list)
    safe_for_execution: bool = False
    command_preview: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.executable:
            raise ValueError("RenderCommandPlan requires executable")
        for arg in self.args:
            if "\n" in arg or "\r" in arg:
                raise ValueError("Command args cannot contain newlines")
        self.command_preview = self.command_preview or " ".join([self.executable] + self.args)


class CompleteEditingSessionRenderStateWrapper(BaseModel):
    complete_editing_session_render_state_wrapper_id: str = Field(default_factory=lambda: new_id("ces_render_state"))
    complete_editing_session_ref: str
    brand_context_version_id: str
    research_snapshot_refs: list[str] = Field(default_factory=list)
    asset_manifest_refs: list[str]
    scene_spec_refs: list[str]
    composition_job_refs: list[str]
    provider_job_receipt_refs: list[str] = Field(default_factory=list)
    evaluation_receipt_refs: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.complete_editing_session_ref:
            raise ValueError("CompleteEditingSessionRenderStateWrapper requires complete_editing_session_ref")
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")
        if not self.asset_manifest_refs:
            raise ValueError("asset_manifest_refs are required")
        if not self.scene_spec_refs:
            raise ValueError("scene_spec_refs are required")
        if not self.composition_job_refs:
            raise ValueError("composition_job_refs are required")


class SevenLayerCompositionPayload(BaseModel):
    seven_layer_composition_payload_id: str = Field(default_factory=lambda: new_id("seven_layers"))
    layer_refs: dict[RenderLayerName, list[str]]

    def __init__(self, **data: Any):
        super().__init__(**data)
        required = set(RenderLayerName)
        if set(self.layer_refs.keys()) != required:
            raise ValueError("SevenLayerCompositionPayload requires exactly the seven canonical layers")
        if not self.layer_refs[RenderLayerName.BACKGROUND]:
            raise ValueError("background layer is required")
        if not self.layer_refs[RenderLayerName.TEXT]:
            raise ValueError("text layer is required")


class MotionVocabularyPolicyReceipt(BaseModel):
    motion_vocabulary_policy_receipt_id: str = Field(default_factory=lambda: new_id("motion_vocab"))
    requested_motion_cues: list[MotionCueName]
    allowed_motion_cues: list[MotionCueName] = Field(default_factory=lambda: [
        MotionCueName.SLOW_PUSH,
        MotionCueName.PAPER_SLIDE_IN,
        MotionCueName.SETTLE,
        MotionCueName.SUBTLE_PARALLAX,
        MotionCueName.TEXT_REVEAL,
        MotionCueName.AVATAR_GESTURE,
        MotionCueName.PROXY_BOUNCE,
        MotionCueName.ROUGH_NOTATION_DRAW,
        MotionCueName.SNAP_ZOOM,
    ])
    banned_motion_cues: list[MotionCueName] = Field(default_factory=lambda: [
        MotionCueName.AI_LIQUID_MORPH,
        MotionCueName.OBJECT_WARP,
        MotionCueName.UNMOTIVATED_SHAKE,
    ])
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        blockers = list(self.blockers)
        requested = set(self.requested_motion_cues)
        banned = requested.intersection(set(self.banned_motion_cues))
        not_allowed = requested.difference(set(self.allowed_motion_cues)).difference(set(self.banned_motion_cues))
        if banned:
            blockers.append("banned_motion_cues_requested")
        if not_allowed:
            blockers.append("unregistered_motion_cues_requested")
        self.blockers = sorted(set(blockers))
        self.pass_status = PassStatus.FAIL if self.blockers else PassStatus.PASS


class MemeticSoundCueModerationReceipt(BaseModel):
    memetic_sound_cue_moderation_receipt_id: str = Field(default_factory=lambda: new_id("memetic_sound"))
    format_id: VideoFormatId
    cue_times_ms: list[int] = Field(default_factory=list)
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        spacing = 10000 if self.format_id == VideoFormatId.FORMAT_04 else 30000
        times = sorted(self.cue_times_ms)
        blockers = list(self.blockers)
        for a, b in zip(times, times[1:]):
            if b - a < spacing:
                blockers.append("memetic_sound_cue_spacing_violation")
                break
        self.blockers = sorted(set(blockers))
        self.pass_status = PassStatus.FAIL if self.blockers else PassStatus.PASS


class RenderRuntimeGateReceipt(BaseModel):
    render_runtime_gate_receipt_id: str = Field(default_factory=lambda: new_id("runtime_gate"))
    runtime_name: str
    capability_id: str
    runtime_capability_tested: bool
    local_worker_lease_id: str | None = None
    execution_mode: RenderExecutionMode
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        blockers = list(self.blockers)
        if self.execution_mode == RenderExecutionMode.REAL_LOCAL:
            if not self.runtime_capability_tested:
                blockers.append("runtime_capability_not_tested")
            if not self.local_worker_lease_id:
                blockers.append("missing_local_worker_lease")
        self.blockers = sorted(set(blockers))
        self.pass_status = PassStatus.FAIL if self.blockers else PassStatus.PASS


class RemotionRenderJob(BaseModel):
    remotion_render_job_id: str = Field(default_factory=lambda: new_id("remotion_job"))
    timeline_program_id: str
    composition_id: str
    entry_point: str
    output_path: str
    input_props_ref: str
    complete_editing_session_state: CompleteEditingSessionRenderStateWrapper
    seven_layer_payload: SevenLayerCompositionPayload
    motion_vocabulary_receipt: MotionVocabularyPolicyReceipt
    memetic_sound_receipt: MemeticSoundCueModerationReceipt
    codec: RemotionCodec = RemotionCodec.H264
    fps: int = Field(default=30, gt=0)
    width: int = Field(default=1080, gt=0)
    height: int = Field(default=1920, gt=0)
    duration_in_frames: int = Field(gt=0)
    execution_mode: RenderExecutionMode = RenderExecutionMode.DRY_RUN
    runtime_capability_tested: bool = False
    local_worker_lease_id: str | None = None
    provider_calls_allowed: bool = False
    allow_subprocess_execution: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.entry_point = validate_workspace_relative_path(self.entry_point, "entry_point")
        self.output_path = validate_workspace_relative_path(self.output_path, "output_path")
        if self.provider_calls_allowed:
            raise ValueError("Remotion render job cannot allow provider calls")
        if self.motion_vocabulary_receipt.pass_status == PassStatus.FAIL:
            raise ValueError("Remotion render job cannot compile with failed motion vocabulary receipt")
        if self.memetic_sound_receipt.pass_status == PassStatus.FAIL:
            raise ValueError("Remotion render job cannot compile with failed memetic sound receipt")
        gate = RenderRuntimeGateReceipt(
            runtime_name="remotion",
            capability_id="runtime:render:remotion",
            runtime_capability_tested=self.runtime_capability_tested,
            local_worker_lease_id=self.local_worker_lease_id,
            execution_mode=self.execution_mode,
        )
        if gate.pass_status == PassStatus.FAIL:
            raise ValueError(f"Remotion runtime gate failed: {gate.blockers}")
        if self.allow_subprocess_execution and self.execution_mode != RenderExecutionMode.REAL_LOCAL:
            raise ValueError("allow_subprocess_execution requires execution_mode=real_local")


class RemotionRenderResult(BaseModel):
    remotion_render_result_id: str = Field(default_factory=lambda: new_id("remotion_result"))
    remotion_render_job_id: str
    status: RenderJobStatus
    output_uri: str | None = None
    output_sha256: str | None = None
    command_plan: RenderCommandPlan | None = None
    dry_run: bool = True
    provider_calls_executed: bool = False
    external_runtime_calls_executed: bool = False
    logs: list[str] = Field(default_factory=list)
    error_message: str | None = None
    completed_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.provider_calls_executed:
            raise ValueError("Remotion result cannot execute provider calls")
        if self.dry_run and self.external_runtime_calls_executed:
            raise ValueError("Dry-run Remotion result cannot execute external runtime")
        if self.status == RenderJobStatus.SUCCEEDED and (not self.output_uri or not self.output_sha256):
            raise ValueError("Succeeded Remotion result requires output_uri and output_sha256")


class FFmpegFinishJob(BaseModel):
    ffmpeg_finish_job_id: str = Field(default_factory=lambda: new_id("ffmpeg_job"))
    input_path: str
    output_path: str
    codec: FFmpegCodec = FFmpegCodec.H264
    filters: list[str] = Field(default_factory=lambda: ["scale=1080:1920", "loudnorm=I=-14:TP=-1:LRA=11"])
    execution_mode: RenderExecutionMode = RenderExecutionMode.DRY_RUN
    runtime_capability_tested: bool = False
    local_worker_lease_id: str | None = None
    provider_calls_allowed: bool = False
    allow_subprocess_execution: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.input_path = validate_workspace_relative_path(self.input_path, "input_path")
        self.output_path = validate_workspace_relative_path(self.output_path, "output_path")
        if self.provider_calls_allowed:
            raise ValueError("FFmpeg finish job cannot allow provider calls")
        if not self.filters:
            raise ValueError("FFmpeg finish job requires filters")
        gate = RenderRuntimeGateReceipt(
            runtime_name="ffmpeg",
            capability_id="runtime:finish:ffmpeg",
            runtime_capability_tested=self.runtime_capability_tested,
            local_worker_lease_id=self.local_worker_lease_id,
            execution_mode=self.execution_mode,
        )
        if gate.pass_status == PassStatus.FAIL:
            raise ValueError(f"FFmpeg runtime gate failed: {gate.blockers}")
        if self.allow_subprocess_execution and self.execution_mode != RenderExecutionMode.REAL_LOCAL:
            raise ValueError("allow_subprocess_execution requires execution_mode=real_local")


class FFmpegFinishResult(BaseModel):
    ffmpeg_finish_result_id: str = Field(default_factory=lambda: new_id("ffmpeg_result"))
    ffmpeg_finish_job_id: str
    status: RenderJobStatus
    output_uri: str | None = None
    output_sha256: str | None = None
    command_plan: RenderCommandPlan | None = None
    dry_run: bool = True
    provider_calls_executed: bool = False
    external_runtime_calls_executed: bool = False
    logs: list[str] = Field(default_factory=list)
    error_message: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.provider_calls_executed:
            raise ValueError("FFmpeg finish result cannot execute provider calls")
        if self.dry_run and self.external_runtime_calls_executed:
            raise ValueError("Dry-run FFmpeg result cannot execute external runtime")
        if self.status == RenderJobStatus.SUCCEEDED and (not self.output_uri or not self.output_sha256):
            raise ValueError("Succeeded FFmpeg result requires output_uri and output_sha256")


class FFprobeValidationReceipt(BaseModel):
    ffprobe_validation_receipt_id: str = Field(default_factory=lambda: new_id("ffprobe_receipt"))
    file_ref: str
    duration_ms: int = Field(gt=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    fps: float = Field(gt=0)
    video_codec: str
    audio_codec: str | None = None
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        blockers = list(self.blockers)
        if self.width <= 0 or self.height <= 0:
            blockers.append("invalid_dimensions")
        if self.duration_ms <= 0:
            blockers.append("invalid_duration")
        if not self.video_codec:
            blockers.append("missing_video_codec")
        self.blockers = sorted(set(blockers))
        self.pass_status = PassStatus.FAIL if self.blockers else self.pass_status
        if self.blockers and self.pass_status == PassStatus.PASS:
            raise ValueError("FFprobeValidationReceipt cannot pass with blockers")


class FrameSamplingReceipt(BaseModel):
    frame_sampling_receipt_id: str = Field(default_factory=lambda: new_id("frame_sampling"))
    file_ref: str
    sampled_frame_count: int = Field(ge=0)
    expected_scene_count: int = Field(ge=1)
    black_frame_count: int = Field(default=0, ge=0)
    broken_text_detected: bool = False
    character_drift_detected: bool = False
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        blockers = list(self.blockers)
        if self.sampled_frame_count < self.expected_scene_count:
            blockers.append("insufficient_frame_samples")
        if self.black_frame_count > 0:
            blockers.append("black_frames_detected")
        if self.broken_text_detected:
            blockers.append("broken_text_detected")
        if self.character_drift_detected:
            blockers.append("character_drift_detected")
        self.blockers = sorted(set(blockers))
        self.pass_status = PassStatus.FAIL if self.blockers else self.pass_status


class AudioLevelAnalysisReceipt(BaseModel):
    audio_level_analysis_receipt_id: str = Field(default_factory=lambda: new_id("audio_receipt"))
    file_ref: str
    integrated_lufs: float
    true_peak_db: float
    target_lufs: float = -14.0
    tolerance_lufs: float = 3.0
    max_true_peak_db: float = -1.0
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        blockers = list(self.blockers)
        if abs(self.integrated_lufs - self.target_lufs) > self.tolerance_lufs:
            blockers.append("integrated_lufs_out_of_tolerance")
        if self.true_peak_db > self.max_true_peak_db:
            blockers.append("true_peak_exceeds_limit")
        self.blockers = sorted(set(blockers))
        self.pass_status = PassStatus.FAIL if self.blockers else self.pass_status


class DurationToleranceReceipt(BaseModel):
    duration_tolerance_receipt_id: str = Field(default_factory=lambda: new_id("duration_receipt"))
    expected_duration_ms: int = Field(gt=0)
    actual_duration_ms: int = Field(gt=0)
    tolerance_ms: int = Field(default=500, ge=0)
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        blockers = list(self.blockers)
        if abs(self.actual_duration_ms - self.expected_duration_ms) > self.tolerance_ms:
            blockers.append("duration_out_of_tolerance")
        self.blockers = sorted(set(blockers))
        self.pass_status = PassStatus.FAIL if self.blockers else self.pass_status


class RenderQAReport(BaseModel):
    render_qa_report_id: str = Field(default_factory=lambda: new_id("render_qa"))
    file_ref: str
    ffprobe_validation: FFprobeValidationReceipt
    frame_sampling: FrameSamplingReceipt
    audio_level_analysis: AudioLevelAnalysisReceipt
    duration_tolerance: DurationToleranceReceipt
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        blockers = list(self.blockers)
        for receipt in [self.ffprobe_validation, self.frame_sampling, self.audio_level_analysis, self.duration_tolerance]:
            if receipt.pass_status == PassStatus.FAIL:
                blockers.extend(receipt.blockers)
        self.blockers = sorted(set(blockers))
        self.pass_status = PassStatus.FAIL if self.blockers else self.pass_status
        if self.blockers and self.pass_status == PassStatus.PASS:
            raise ValueError("RenderQAReport cannot pass with blockers")
