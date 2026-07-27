from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class PassStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class RenderQASeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKING = "blocking"


class MotionPromiseLevel(str, Enum):
    NONE = "none"
    SUBTLE = "subtle"
    STANDARD = "standard"
    HIGH = "high"


class ObservedMotionLevel(str, Enum):
    STATIC = "static"
    SUBTLE = "subtle"
    STANDARD = "standard"
    HIGH = "high"


class RenderQABlocker(BaseModel):
    render_qa_blocker_id: str = Field(default_factory=lambda: _id("render_qa_blocker"))
    code: str
    message: str
    severity: RenderQASeverity = RenderQASeverity.BLOCKING
    source_receipt_id: str | None = None
    recoverable: bool = True


class _Receipt(BaseModel):
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[RenderQABlocker] = Field(default_factory=list)

    def _finalize(self, blockers: list[RenderQABlocker], warn: bool = False):
        object.__setattr__(self, "blockers", blockers)
        if any(b.severity == RenderQASeverity.BLOCKING for b in blockers):
            object.__setattr__(self, "pass_status", PassStatus.FAIL)
        elif blockers or warn:
            object.__setattr__(self, "pass_status", PassStatus.WARN)
        else:
            object.__setattr__(self, "pass_status", PassStatus.PASS)


class FFprobeValidationReceipt(_Receipt):
    ffprobe_validation_receipt_id: str = Field(default_factory=lambda: _id("ffprobe"))
    file_ref: str
    playable: bool
    duration_ms: int = Field(gt=0)
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    fps: float = Field(gt=0)
    video_codec: str
    audio_codec: str | None = None
    has_video_stream: bool = True
    has_audio_stream: bool = True
    expected_width: int | None = None
    expected_height: int | None = None
    checked_at: str = Field(default_factory=_now)

    def __init__(self, **data: Any):
        super().__init__(**data)
        b = list(self.blockers)
        if not self.playable:
            b.append(RenderQABlocker(code="not_playable", message="Rendered file is not playable."))
        if not self.has_video_stream:
            b.append(RenderQABlocker(code="missing_video_stream", message="Rendered file has no video stream."))
        if not self.video_codec:
            b.append(RenderQABlocker(code="missing_video_codec", message="Rendered file has no video codec."))
        if self.expected_width and self.width != self.expected_width:
            b.append(RenderQABlocker(code="width_mismatch", message="Width does not match promise."))
        if self.expected_height and self.height != self.expected_height:
            b.append(RenderQABlocker(code="height_mismatch", message="Height does not match promise."))
        self._finalize(b)


class FrameSamplingReceipt(_Receipt):
    frame_sampling_receipt_id: str = Field(default_factory=lambda: _id("frame_sampling"))
    file_ref: str
    sampled_frame_count: int = Field(ge=0)
    expected_scene_count: int = Field(ge=1)
    black_frame_count: int = Field(default=0, ge=0)
    frozen_frame_count: int = Field(default=0, ge=0)
    first_frame_present: bool = True
    final_frame_present: bool = True
    broken_text_detected: bool = False
    visual_artifact_detected: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        b = list(self.blockers)
        checks = [
            (self.sampled_frame_count < self.expected_scene_count, "insufficient_frame_samples", "Frame sample count is below expected scene count."),
            (self.black_frame_count > 0, "black_frames_detected", "Black frames detected."),
            (self.frozen_frame_count > 0, "frozen_frames_detected", "Frozen frames detected."),
            (not self.first_frame_present, "missing_first_frame", "First frame missing."),
            (not self.final_frame_present, "missing_final_frame", "Final frame missing."),
            (self.broken_text_detected, "broken_text_detected", "Broken text detected."),
            (self.visual_artifact_detected, "visual_artifact_detected", "Visual artifact detected."),
        ]
        for fail, code, msg in checks:
            if fail:
                b.append(RenderQABlocker(code=code, message=msg))
        self._finalize(b)


class AudioLevelAnalysisReceipt(_Receipt):
    audio_level_analysis_receipt_id: str = Field(default_factory=lambda: _id("audio"))
    file_ref: str
    has_audio_stream: bool = True
    integrated_lufs: float | None = None
    true_peak_db: float | None = None
    target_lufs: float = -14.0
    tolerance_lufs: float = 3.0
    max_true_peak_db: float = -1.0
    silence_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    clipping_detected: bool = False
    dialogue_intelligibility_pass: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        b = list(self.blockers)
        if not self.has_audio_stream:
            b.append(RenderQABlocker(code="missing_audio_stream", message="Audio stream missing."))
        if self.has_audio_stream and self.integrated_lufs is None:
            b.append(RenderQABlocker(code="missing_lufs_measurement", message="LUFS measurement missing."))
        if self.has_audio_stream and self.true_peak_db is None:
            b.append(RenderQABlocker(code="missing_true_peak_measurement", message="True peak missing."))
        if self.integrated_lufs is not None and abs(self.integrated_lufs - self.target_lufs) > self.tolerance_lufs:
            b.append(RenderQABlocker(code="integrated_lufs_out_of_tolerance", message="Integrated loudness out of tolerance."))
        if self.true_peak_db is not None and self.true_peak_db > self.max_true_peak_db:
            b.append(RenderQABlocker(code="true_peak_exceeds_limit", message="True peak exceeds limit."))
        if self.silence_ratio > 0.30:
            b.append(RenderQABlocker(code="excessive_silence", message="Silence ratio too high."))
        if self.clipping_detected:
            b.append(RenderQABlocker(code="audio_clipping_detected", message="Audio clipping detected."))
        if not self.dialogue_intelligibility_pass:
            b.append(RenderQABlocker(code="dialogue_intelligibility_failed", message="Dialogue intelligibility failed."))
        self._finalize(b)


class CaptionBurnCheckReceipt(_Receipt):
    caption_burn_check_receipt_id: str = Field(default_factory=lambda: _id("caption"))
    file_ref: str
    captions_required: bool
    captions_detected: bool
    caption_track_detected: bool = False
    burned_caption_detected: bool = False
    safe_area_pass: bool = True
    legibility_pass: bool = True
    timing_alignment_pass: bool = True
    max_caption_line_count: int = Field(default=2, ge=1)
    observed_max_line_count: int = Field(default=1, ge=0)

    def __init__(self, **data: Any):
        super().__init__(**data)
        b = list(self.blockers)
        if self.captions_required and not self.captions_detected:
            b.append(RenderQABlocker(code="captions_required_but_missing", message="Captions required but missing."))
        if self.captions_required and not (self.caption_track_detected or self.burned_caption_detected):
            b.append(RenderQABlocker(code="caption_delivery_missing", message="No caption track or burned captions detected."))
        if not self.safe_area_pass:
            b.append(RenderQABlocker(code="caption_safe_area_failed", message="Caption safe area failed."))
        if not self.legibility_pass:
            b.append(RenderQABlocker(code="caption_legibility_failed", message="Caption legibility failed."))
        if not self.timing_alignment_pass:
            b.append(RenderQABlocker(code="caption_timing_alignment_failed", message="Caption timing failed."))
        if self.observed_max_line_count > self.max_caption_line_count:
            b.append(RenderQABlocker(code="caption_line_count_exceeded", message="Caption line count exceeded."))
        self._finalize(b)


class VisualRegressionScreenshotReceipt(_Receipt):
    visual_regression_screenshot_receipt_id: str = Field(default_factory=lambda: _id("visual_regression"))
    file_ref: str
    screenshot_refs: list[str]
    baseline_refs: list[str]
    max_allowed_drift: float = Field(default=0.10, ge=0.0, le=1.0)
    observed_max_drift: float = Field(default=0.0, ge=0.0, le=1.0)
    missing_screenshot_count: int = Field(default=0, ge=0)
    layout_shift_detected: bool = False
    style_drift_detected: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        b = list(self.blockers)
        if not self.screenshot_refs:
            b.append(RenderQABlocker(code="missing_screenshot_refs", message="Screenshot refs missing."))
        if not self.baseline_refs:
            b.append(RenderQABlocker(code="missing_baseline_refs", message="Baseline refs missing."))
        if self.missing_screenshot_count:
            b.append(RenderQABlocker(code="missing_screenshots", message="Expected screenshots missing."))
        if self.observed_max_drift > self.max_allowed_drift:
            b.append(RenderQABlocker(code="visual_drift_exceeds_threshold", message="Screenshot drift exceeds threshold."))
        if self.layout_shift_detected:
            b.append(RenderQABlocker(code="layout_shift_detected", message="Layout shift detected."))
        if self.style_drift_detected:
            b.append(RenderQABlocker(code="style_drift_detected", message="Style drift detected."))
        self._finalize(b)


class CharacterQAReport(_Receipt):
    character_qa_report_id: str = Field(default_factory=lambda: _id("character_qa"))
    file_ref: str
    character_id: str
    identity_consistency_score: float = Field(ge=0.0, le=1.0)
    face_plate_consistency_score: float = Field(ge=0.0, le=1.0)
    body_layer_consistency_score: float = Field(ge=0.0, le=1.0)
    style_consistency_score: float = Field(ge=0.0, le=1.0)
    min_identity_score: float = 0.85
    min_style_score: float = 0.80
    character_drift_detected: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        b = list(self.blockers)
        checks = [
            (self.identity_consistency_score < self.min_identity_score, "identity_consistency_failed"),
            (self.face_plate_consistency_score < self.min_identity_score, "face_plate_consistency_failed"),
            (self.body_layer_consistency_score < self.min_identity_score, "body_layer_consistency_failed"),
            (self.style_consistency_score < self.min_style_score, "character_style_consistency_failed"),
            (self.character_drift_detected, "character_drift_detected"),
        ]
        for fail, code in checks:
            if fail:
                b.append(RenderQABlocker(code=code, message=code.replace("_", " ")))
        self._finalize(b)


class MotionDowngradeBlocker(_Receipt):
    motion_downgrade_blocker_id: str = Field(default_factory=lambda: _id("motion_downgrade"))
    file_ref: str
    promised_motion_level: MotionPromiseLevel
    observed_motion_level: ObservedMotionLevel
    motion_required: bool = True
    operator_downgrade_approved: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        order = {"none": 0, "static": 0, "subtle": 1, "standard": 2, "high": 3}
        b = list(self.blockers)
        if self.motion_required and self.promised_motion_level != MotionPromiseLevel.NONE and self.observed_motion_level == ObservedMotionLevel.STATIC:
            b.append(RenderQABlocker(code="motion_missing", message="Motion promised but output appears static."))
        elif order[self.observed_motion_level.value] < order[self.promised_motion_level.value]:
            b.append(RenderQABlocker(code="motion_downgraded", message="Observed motion below promised motion."))
        if b and self.operator_downgrade_approved:
            b = [RenderQABlocker(code="motion_downgrade_operator_approved", message="Motion downgrade explicitly approved.", severity=RenderQASeverity.WARNING)]
            self._finalize(b, warn=True)
        else:
            self._finalize(b)


class RenderQAPromiseProfile(BaseModel):
    render_qa_promise_profile_id: str = Field(default_factory=lambda: _id("promise"))
    delivery_id: str
    expected_width: int = Field(gt=0)
    expected_height: int = Field(gt=0)
    expected_duration_ms: int = Field(gt=0)
    duration_tolerance_ms: int = Field(default=500, ge=0)
    captions_required: bool = True
    motion_required: bool = True
    promised_motion_level: MotionPromiseLevel = MotionPromiseLevel.STANDARD
    min_negative_space_ratio: float = Field(default=0.30, ge=0.0, le=1.0)
    min_identity_consistency: float = Field(default=0.85, ge=0.0, le=1.0)
    min_composition_quality: float = Field(default=0.80, ge=0.0, le=1.0)
    min_style_consistency: float = Field(default=0.80, ge=0.0, le=1.0)
    min_emotional_accuracy: float = Field(default=0.75, ge=0.0, le=1.0)
    min_platform_fit: float = Field(default=0.80, ge=0.0, le=1.0)
    min_hook_strength: float = Field(default=0.70, ge=0.0, le=1.0)
    min_shareability: float = Field(default=0.65, ge=0.0, le=1.0)
    min_routeability: float = Field(default=0.80, ge=0.0, le=1.0)


class DeliveryPromiseValidationReceipt(_Receipt):
    delivery_promise_validation_receipt_id: str = Field(default_factory=lambda: _id("delivery"))
    file_ref: str
    promise_profile: RenderQAPromiseProfile
    actual_width: int = Field(gt=0)
    actual_height: int = Field(gt=0)
    actual_duration_ms: int = Field(gt=0)
    captions_pass: bool
    motion_pass: bool
    negative_space_ratio: float = Field(ge=0.0, le=1.0)
    identity_consistency: float = Field(ge=0.0, le=1.0)
    composition_quality: float = Field(ge=0.0, le=1.0)
    style_consistency: float = Field(ge=0.0, le=1.0)
    emotional_accuracy: float = Field(ge=0.0, le=1.0)
    platform_fit: float = Field(ge=0.0, le=1.0)
    hook_strength: float = Field(ge=0.0, le=1.0)
    shareability: float = Field(ge=0.0, le=1.0)
    routeability: float = Field(ge=0.0, le=1.0)

    def __init__(self, **data: Any):
        super().__init__(**data)
        p = self.promise_profile
        b = list(self.blockers)
        if (self.actual_width, self.actual_height) != (p.expected_width, p.expected_height):
            b.append(RenderQABlocker(code="delivery_dimensions_mismatch", message="Dimensions violate delivery promise."))
        if abs(self.actual_duration_ms - p.expected_duration_ms) > p.duration_tolerance_ms:
            b.append(RenderQABlocker(code="delivery_duration_out_of_tolerance", message="Duration violates delivery promise."))
        if p.captions_required and not self.captions_pass:
            b.append(RenderQABlocker(code="delivery_caption_promise_failed", message="Caption promise failed."))
        if p.motion_required and not self.motion_pass:
            b.append(RenderQABlocker(code="delivery_motion_promise_failed", message="Motion promise failed."))
        for code, actual, minimum in [
            ("negative_space_below_minimum", self.negative_space_ratio, p.min_negative_space_ratio),
            ("identity_consistency_below_minimum", self.identity_consistency, p.min_identity_consistency),
            ("composition_quality_below_minimum", self.composition_quality, p.min_composition_quality),
            ("style_consistency_below_minimum", self.style_consistency, p.min_style_consistency),
            ("emotional_accuracy_below_minimum", self.emotional_accuracy, p.min_emotional_accuracy),
            ("platform_fit_below_minimum", self.platform_fit, p.min_platform_fit),
            ("hook_strength_below_minimum", self.hook_strength, p.min_hook_strength),
            ("shareability_below_minimum", self.shareability, p.min_shareability),
            ("routeability_below_minimum", self.routeability, p.min_routeability),
        ]:
            if actual < minimum:
                b.append(RenderQABlocker(code=code, message=f"{code}: {actual} < {minimum}"))
        self._finalize(b)


class RenderedAssetEvaluationReceipt(BaseModel):
    rendered_asset_evaluation_receipt_id: str = Field(default_factory=lambda: _id("rendered_eval"))
    file_ref: str
    identity_consistency: float = Field(ge=0.0, le=1.0)
    composition_quality: float = Field(ge=0.0, le=1.0)
    style_consistency: float = Field(ge=0.0, le=1.0)
    emotional_accuracy: float = Field(ge=0.0, le=1.0)
    platform_fit: float = Field(ge=0.0, le=1.0)
    negative_space_compliance: float = Field(ge=0.0, le=1.0)
    hook_strength: float = Field(ge=0.0, le=1.0)
    shareability: float = Field(ge=0.0, le=1.0)
    routeability: float = Field(ge=0.0, le=1.0)


class RenderQACompositeReport(_Receipt):
    render_qa_composite_report_id: str = Field(default_factory=lambda: _id("render_qa_report"))
    file_ref: str
    ffprobe_validation: FFprobeValidationReceipt
    frame_sampling: FrameSamplingReceipt
    audio_level_analysis: AudioLevelAnalysisReceipt
    caption_burn_check: CaptionBurnCheckReceipt
    visual_regression: VisualRegressionScreenshotReceipt
    character_qa: CharacterQAReport | None = None
    motion_downgrade: MotionDowngradeBlocker
    delivery_promise: DeliveryPromiseValidationReceipt
    rendered_asset_evaluation: RenderedAssetEvaluationReceipt | None = None
    created_at: str = Field(default_factory=_now)

    def __init__(self, **data: Any):
        super().__init__(**data)
        receipts = [self.ffprobe_validation, self.frame_sampling, self.audio_level_analysis, self.caption_burn_check, self.visual_regression, self.motion_downgrade, self.delivery_promise]
        if self.character_qa:
            receipts.append(self.character_qa)
        b = []
        warn = False
        for r in receipts:
            b.extend(r.blockers)
            warn = warn or r.pass_status == PassStatus.WARN
        self._finalize(b, warn=warn)
