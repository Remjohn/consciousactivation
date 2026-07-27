from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4
from hashlib import sha256

from pydantic import BaseModel, Field


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


def stable_hash(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


class PassStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class VideoProjectStatus(str, Enum):
    CREATED = "created"
    SOURCE_LOADED = "source_loaded"
    FORMAT_PROGRAMS_ATTACHED = "format_programs_attached"
    COMPOSITION_ATTACHED = "composition_attached"
    SCENE_REALIZATION_COMPILED = "scene_realization_compiled"
    TIMELINE_COMPILED = "timeline_compiled"
    PROXY_RENDERED = "proxy_rendered"
    EVAL_PASSED = "eval_passed"
    REVISION_REQUIRED = "revision_required"
    FINAL_TIMELINE_LOCKED = "final_timeline_locked"
    FINAL_RENDERED = "final_rendered"
    APPROVED = "approved"
    EXPORTED = "exported"


class VideoFrameProfile(str, Enum):
    NINE_SIXTEEN_FULL_VERTICAL = "9:16_FULL_VERTICAL"
    NINE_SIXTEEN_PAPERCUT_EXPLAINER = "9:16_PAPERCUT_EXPLAINER"
    NINE_SIXTEEN_SPLIT_REACTION = "9:16_SPLIT_REACTION"
    NINE_SIXTEEN_CONSCIOUS_REACTION = "9:16_CONSCIOUS_REACTION"
    ONE_ONE_SOFT_ROUNDED_EDITORIAL = "1:1_SOFT_ROUNDED_EDITORIAL"
    ONE_ONE_PROOF_CARD = "1:1_PROOF_CARD"
    FOUR_FIVE_FEED_VIDEO = "4:5_FEED_VIDEO"


def reject_16_9_delivery(frame_profile: str) -> None:
    if frame_profile.startswith("16:9"):
        raise ValueError("16:9 is source-only and cannot be a delivery frame profile")


class VideoFormatId(str, Enum):
    FORMAT_01 = "format_01_cinematic_story"
    FORMAT_02 = "format_02_avatar_papercut_explainer"
    FORMAT_03 = "format_03_living_commentary_reactions"
    FORMAT_04 = "format_04_conscious_reactions_editing"


class VideoTrackType(str, Enum):
    SOURCE_VIDEO = "source_video"
    SOURCE_AUDIO = "source_audio"
    A_ROLL = "a_roll"
    BROLL = "broll"
    PROOF_OBJECT = "proof_object"
    MEMORY_OBJECT = "memory_object"
    REAL_LIFE_CUTOUT = "real_life_cutout"
    AVATAR = "avatar"
    AUDIENCE_PROXY = "audience_proxy"
    DIAGRAM = "diagram"
    ROUGH_NOTATION = "rough_notation"
    REACTION_UI = "reaction_ui"
    CAPTION = "caption"
    TEXT_REVEAL = "text_reveal"
    SOUND_CUE = "sound_cue"
    MUSIC = "music"
    ROOM_TONE = "room_tone"
    ATMOSPHERE = "atmosphere"


class VideoLayerRole(str, Enum):
    PRIMARY_SOURCE = "primary_source"
    SUPPORTING_BROLL = "supporting_broll"
    AVATAR_PERFORMANCE = "avatar_performance"
    AUDIENCE_PROXY_PERFORMANCE = "audience_proxy_performance"
    TEXT = "text"
    CAPTION = "caption"
    PROOF_SURFACE = "proof_surface"
    REACTION_SURFACE = "reaction_surface"
    SOUND = "sound"
    MOTION_ACCENT = "motion_accent"


class MotionCueType(str, Enum):
    SLOW_PUSH = "slow_push"
    PAPER_SLIDE_IN = "paper_slide_in"
    SETTLE = "settle"
    SUBTLE_PARALLAX = "subtle_parallax"
    TEXT_REVEAL = "text_reveal"
    AVATAR_GESTURE = "avatar_gesture"
    PROXY_BOUNCE = "proxy_bounce"
    ROUGH_NOTATION_DRAW = "rough_notation_draw"
    SNAP_ZOOM = "snap_zoom"
    SCORE_TICK = "score_tick"


class SoundCueType(str, Enum):
    ROOM_TONE = "room_tone"
    PAPER_RUSTLE = "paper_rustle"
    CHALK_SCRATCH = "chalk_scratch"
    SOFT_HIT = "soft_hit"
    SNAP = "snap"
    SCORE_TICK = "score_tick"
    REVEAL_HIT = "reveal_hit"


class CompleteEditingSessionRef(BaseModel):
    complete_editing_session_ref_id: str = Field(default_factory=lambda: new_id("ces_ref"))
    source_expression_session_id: str | None = None
    source_asset_set_id: str | None = None
    transcript_ref: str | None = None
    source_media_refs: list[str] = Field(default_factory=list)


class VideoEditingProject(BaseModel):
    video_project_id: str = Field(default_factory=lambda: new_id("video_project"))
    brand_id: str
    brand_context_version_id: str
    title: str
    complete_editing_session_ref: CompleteEditingSessionRef | None = None
    status: VideoProjectStatus = VideoProjectStatus.CREATED
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")


class VideoEditingVariant(BaseModel):
    video_variant_id: str = Field(default_factory=lambda: new_id("video_variant"))
    project_id: str
    frame_profile: VideoFrameProfile
    target_duration_ms: int = Field(gt=0)
    status: VideoProjectStatus = VideoProjectStatus.CREATED
    approved: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        reject_16_9_delivery(self.frame_profile.value)


class VideoSourceMedia(BaseModel):
    source_media_id: str = Field(default_factory=lambda: new_id("source_media"))
    source_ref: str
    media_type: str
    uri: str
    duration_ms: int = Field(gt=0)
    width: int | None = None
    height: int | None = None
    fps: int | None = None
    rights_profile_ref: str | None = None


class VideoSourceAssetSet(BaseModel):
    source_asset_set_id: str = Field(default_factory=lambda: new_id("source_asset_set"))
    source_media: list[VideoSourceMedia]
    source_span_refs: list[str]
    asset_hashes: dict[str, str] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.source_media:
            raise ValueError("VideoSourceAssetSet requires source_media")
        if not self.source_span_refs:
            raise ValueError("VideoSourceAssetSet requires source_span_refs")


class VideoMediaProbeReceipt(BaseModel):
    video_media_probe_receipt_id: str = Field(default_factory=lambda: new_id("media_probe"))
    source_media_id: str
    duration_ms: int
    width: int | None = None
    height: int | None = None
    fps: int | None = None
    pass_status: PassStatus = PassStatus.PASS


class VideoTranscriptTimingMap(BaseModel):
    transcript_timing_map_id: str = Field(default_factory=lambda: new_id("transcript_timing"))
    source_ref: str
    beat_timing: dict[str, tuple[int, int]]

    def __init__(self, **data: Any):
        super().__init__(**data)
        for beat, (start, end) in self.beat_timing.items():
            if end <= start:
                raise ValueError(f"Invalid timing for beat {beat}")


class VideoExpressionMomentMap(BaseModel):
    expression_moment_map_id: str = Field(default_factory=lambda: new_id("expression_map"))
    expression_timing: dict[str, tuple[int, int]] = Field(default_factory=dict)


class VideoFormatProgramRef(BaseModel):
    format_program_ref_id: str = Field(default_factory=lambda: new_id("format_prog_ref"))
    format_program_id: str
    format_id: VideoFormatId
    source_span_refs: list[str]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.source_span_refs:
            raise ValueError("VideoFormatProgramRef requires source_span_refs")


class VideoCompositionSceneRef(BaseModel):
    composition_scene_ref_id: str = Field(default_factory=lambda: new_id("composition_scene_ref"))
    composition_scene_id: str
    format_id: VideoFormatId
    locked: bool = True
    cognitive_load_receipt_ref: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.format_id == VideoFormatId.FORMAT_02 and not self.locked:
            raise ValueError("Format 02 requires locked composition scene")


class VideoAvatarPerformanceRef(BaseModel):
    avatar_performance_ref_id: str = Field(default_factory=lambda: new_id("avatar_perf_ref"))
    avatar_performance_plan_id: str
    lip_sync_enabled: bool = False
    source_scene_ref: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.lip_sync_enabled:
            raise ValueError("Video Engine rejects lip-sync avatar performance plans in V1")


class VideoAssetReceiptRef(BaseModel):
    asset_receipt_ref_id: str = Field(default_factory=lambda: new_id("asset_receipt_ref"))
    asset_id: str
    receipt_id: str
    asset_hash: str


class VideoMotionCue(BaseModel):
    motion_cue_id: str = Field(default_factory=lambda: new_id("motion_cue"))
    cue_type: MotionCueType
    start_ms: int = Field(ge=0)
    end_ms: int = Field(gt=0)
    reason: str
    argument_shift_ref: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.end_ms <= self.start_ms:
            raise ValueError("VideoMotionCue end_ms must be after start_ms")
        if self.cue_type == MotionCueType.SNAP_ZOOM and not self.argument_shift_ref:
            raise ValueError("Snap zoom requires argument_shift_ref")


class VideoTransitionCue(BaseModel):
    transition_cue_id: str = Field(default_factory=lambda: new_id("transition"))
    transition_type: str
    start_ms: int = Field(ge=0)
    duration_ms: int = Field(gt=0)
    reason: str


class VideoSceneBoundary(BaseModel):
    scene_id: str
    start_ms: int = Field(ge=0)
    end_ms: int = Field(gt=0)
    scene_role: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.end_ms <= self.start_ms:
            raise ValueError("VideoSceneBoundary end_ms must be after start_ms")


class VideoLayerProgram(BaseModel):
    layer_id: str = Field(default_factory=lambda: new_id("video_layer"))
    layer_role: VideoLayerRole
    source_ref: str | None = None
    asset_ref: str | None = None
    start_ms: int = Field(ge=0)
    end_ms: int = Field(gt=0)
    z_index: int = 1
    frame_profile: VideoFrameProfile
    position: dict[str, float] = Field(default_factory=dict)
    scale: float = 1.0
    crop: dict[str, float] = Field(default_factory=dict)
    opacity: float = Field(default=1.0, ge=0.0, le=1.0)
    motion_cues: list[VideoMotionCue] = Field(default_factory=list)
    composition_scene_ref: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        reject_16_9_delivery(self.frame_profile.value)
        if self.end_ms <= self.start_ms:
            raise ValueError("VideoLayerProgram requires positive duration")


class VideoTrackProgram(BaseModel):
    track_id: str = Field(default_factory=lambda: new_id("track"))
    track_type: VideoTrackType
    layers: list[VideoLayerProgram]

    def __init__(self, **data: Any):
        super().__init__(**data)
        for layer in self.layers:
            if layer.end_ms <= layer.start_ms:
                raise ValueError("Track layers must have positive duration")


class VideoSceneTimingPlan(BaseModel):
    scene_timing_plan_id: str = Field(default_factory=lambda: new_id("scene_timing"))
    scene_boundaries: list[VideoSceneBoundary]

    def __init__(self, **data: Any):
        super().__init__(**data)
        starts = [scene.start_ms for scene in self.scene_boundaries]
        if starts != sorted(starts):
            raise ValueError("Scene boundaries must be time-sorted")
        for prev, cur in zip(self.scene_boundaries, self.scene_boundaries[1:]):
            if cur.start_ms < prev.end_ms:
                raise ValueError("Scene boundaries cannot overlap")


class Format01SceneRealizationPlan(BaseModel):
    format01_scene_realization_plan_id: str = Field(default_factory=lambda: new_id("format01_realization"))
    aroll_story_spine_ref: str
    broll_story_functions: list[str]
    emotional_pause_refs: list[str] = Field(default_factory=list)
    power_phrase_refs: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.aroll_story_spine_ref:
            raise ValueError("Format 01 requires A-roll spine")
        if not self.broll_story_functions:
            raise ValueError("Format 01 B-roll requires story function")
        for fn in self.broll_story_functions:
            if fn not in {"foreshadow", "contrast", "clarify", "memory_object"}:
                raise ValueError("Format 01 B-roll must foreshadow, contrast, clarify, or act as memory object")


class Format02SceneRealizationPlan(BaseModel):
    format02_scene_realization_plan_id: str = Field(default_factory=lambda: new_id("format02_realization"))
    composition_scene_refs: list[VideoCompositionSceneRef]
    avatar_performance_refs: list[VideoAvatarPerformanceRef]
    cognitive_load_budget_preserved: bool = True
    real_life_cutout_motion_policy: list[str] = Field(default_factory=lambda: ["slide_in", "settle", "subtle_parallax"])

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.composition_scene_refs:
            raise ValueError("Format 02 requires locked composition scene refs")
        if not self.avatar_performance_refs:
            raise ValueError("Format 02 requires avatar performance refs")
        if not self.cognitive_load_budget_preserved:
            raise ValueError("Format 02 must preserve cognitive load budget")
        forbidden = {"morph", "warp", "deform", "ai_liquid_motion"}
        if forbidden.intersection(set(self.real_life_cutout_motion_policy)):
            raise ValueError("Format 02 real-life cutouts cannot morph/warp/deform")


class Format03SceneRealizationPlan(BaseModel):
    format03_scene_realization_plan_id: str = Field(default_factory=lambda: new_id("format03_realization"))
    proof_or_quote_surface_ref: str
    stimulus_time_ms: int = Field(ge=0)
    reaction_start_ms: int = Field(ge=0)
    rough_notation_speech_timing_refs: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.proof_or_quote_surface_ref:
            raise ValueError("Format 03 requires proof or quote surface")
        if self.reaction_start_ms < self.stimulus_time_ms:
            raise ValueError("Format 03 reaction timing must follow stimulus")
        if not self.rough_notation_speech_timing_refs:
            raise ValueError("Format 03 rough notation requires speech timing refs")


class SoundCueEvent(BaseModel):
    sound_cue_event_id: str = Field(default_factory=lambda: new_id("sound_event"))
    cue_type: SoundCueType
    start_ms: int = Field(ge=0)
    target_ref: str
    memetic: bool = False


class MemeticCueLedger(BaseModel):
    memetic_cue_ledger_id: str = Field(default_factory=lambda: new_id("memetic_ledger"))
    format_id: VideoFormatId
    cue_times_ms: list[int] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        min_spacing = 10000 if self.format_id == VideoFormatId.FORMAT_04 else 30000
        times = sorted(self.cue_times_ms)
        for a, b in zip(times, times[1:]):
            if b - a < min_spacing:
                raise ValueError(f"Memetic cue spacing too short for {self.format_id.value}")


class Format04SceneRealizationPlan(BaseModel):
    format04_scene_realization_plan_id: str = Field(default_factory=lambda: new_id("format04_realization"))
    debate_tension_ref: str
    reaction_ui_surface_ref: str
    zoom_motion_cues: list[VideoMotionCue] = Field(default_factory=list)
    memetic_cue_ledger: MemeticCueLedger

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.debate_tension_ref:
            raise ValueError("Format 04 requires debate tension")
        if not self.reaction_ui_surface_ref:
            raise ValueError("Format 04 requires reaction UI surface")


class VoicePresencePlan(BaseModel):
    voice_presence_plan_id: str = Field(default_factory=lambda: new_id("voice_presence"))
    authentic_recorded_voice_required: bool = True
    synthetic_primary_delivery_allowed: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.synthetic_primary_delivery_allowed:
            raise ValueError("Synthetic primary delivery is not allowed in V1")


class PausePreservationPlan(BaseModel):
    pause_preservation_plan_id: str = Field(default_factory=lambda: new_id("pause_plan"))
    preserved_pause_refs: list[str]
    override_receipt_ref: str | None = None


class SoundCueTimeline(BaseModel):
    sound_cue_timeline_id: str = Field(default_factory=lambda: new_id("sound_timeline"))
    format_id: VideoFormatId
    events: list[SoundCueEvent]
    memetic_cue_ledger: MemeticCueLedger


class AudioMixPlan(BaseModel):
    audio_mix_plan_id: str = Field(default_factory=lambda: new_id("audio_mix"))
    voice_presence_plan: VoicePresencePlan
    room_tone_required: bool = True
    ducking_policy: str = "voice_first"


class LoudnessFinishPlan(BaseModel):
    loudness_finish_plan_id: str = Field(default_factory=lambda: new_id("loudness"))
    target_integrated_lufs: float = -14.0
    true_peak_db: float = -1.0
    ffmpeg_filter: str = "loudnorm"


class TalkingHeadTrackingPlan(BaseModel):
    talking_head_tracking_plan_id: str = Field(default_factory=lambda: new_id("talking_head"))
    source_media_id: str
    face_box: dict[str, float]
    torso_box: dict[str, float] = Field(default_factory=dict)


class VerticalReframePlan(BaseModel):
    vertical_reframe_plan_id: str = Field(default_factory=lambda: new_id("vertical_reframe"))
    source_media_id: str
    target_frame_profile: VideoFrameProfile
    preserve_face: bool = True
    preserve_eyeline: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        reject_16_9_delivery(self.target_frame_profile.value)


class SquareSoftCardPlan(BaseModel):
    square_soft_card_plan_id: str = Field(default_factory=lambda: new_id("square_card"))
    source_media_id: str
    rounded_corners: bool = True
    preserve_face: bool = True


class FaceSafeZoneReceipt(BaseModel):
    face_safe_zone_receipt_id: str = Field(default_factory=lambda: new_id("face_safe"))
    pass_status: PassStatus
    eyes_cropped: bool = False
    mouth_cropped: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if (self.eyes_cropped or self.mouth_cropped) and self.pass_status == PassStatus.PASS:
            raise ValueError("Face safe zone cannot pass if eyes or mouth are cropped")


class CaptionCue(BaseModel):
    caption_cue_id: str = Field(default_factory=lambda: new_id("caption_cue"))
    text: str
    start_ms: int = Field(ge=0)
    end_ms: int = Field(gt=0)
    avoid_face: bool = True
    avoid_proof_object: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.end_ms <= self.start_ms:
            raise ValueError("CaptionCue requires positive duration")


class CaptionTrack(BaseModel):
    caption_track_id: str = Field(default_factory=lambda: new_id("caption_track"))
    cues: list[CaptionCue]
    mobile_readability_pass: bool = True
    collision_with_face: bool = False
    collision_with_proof_object: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.collision_with_face or self.collision_with_proof_object:
            raise ValueError("Caption track cannot collide with face or proof object")
        if not self.mobile_readability_pass:
            raise ValueError("Caption track must pass mobile readability")


class TextRevealTrack(BaseModel):
    text_reveal_track_id: str = Field(default_factory=lambda: new_id("text_reveal_track"))
    reveal_refs: list[str]
    reveal_order: list[str]


class VideoTimelineProgram(BaseModel):
    timeline_program_id: str = Field(default_factory=lambda: new_id("timeline"))
    brand_id: str
    brand_context_version_id: str
    project_id: str
    variant_id: str
    frame_profile: VideoFrameProfile
    fps: int = Field(default=30, gt=0)
    duration_ms: int = Field(gt=0)
    source_asset_set_id: str
    format_program_refs: list[VideoFormatProgramRef]
    composition_scene_refs: list[VideoCompositionSceneRef] = Field(default_factory=list)
    avatar_performance_plan_refs: list[VideoAvatarPerformanceRef] = Field(default_factory=list)
    tracks: list[VideoTrackProgram]
    scene_timing_plan: VideoSceneTimingPlan
    caption_track_id: str | None = None
    sound_cue_timeline_id: str | None = None
    status: VideoProjectStatus = VideoProjectStatus.TIMELINE_COMPILED
    final_locked: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")
        reject_16_9_delivery(self.frame_profile.value)
        if not self.source_asset_set_id:
            raise ValueError("VideoTimelineProgram requires source_asset_set_id")
        if not self.format_program_refs:
            raise ValueError("VideoTimelineProgram requires format_program_refs")
        has_format02 = any(ref.format_id == VideoFormatId.FORMAT_02 for ref in self.format_program_refs)
        if has_format02 and not self.composition_scene_refs:
            raise ValueError("Format 02 timeline requires composition_scene_refs")
        if not self.tracks:
            raise ValueError("VideoTimelineProgram requires tracks")


class OTIOAuditTimeline(BaseModel):
    otio_audit_timeline_id: str = Field(default_factory=lambda: new_id("otio_audit"))
    timeline_program_id: str
    tracks_summary: list[str]
    external_media_refs: list[str]


class RemotionCompositionBinding(BaseModel):
    remotion_composition_binding_id: str = Field(default_factory=lambda: new_id("remotion_binding"))
    composition_id: str
    fps: int
    width: int
    height: int
    duration_in_frames: int


class RemotionInputProps(BaseModel):
    remotion_input_props_id: str = Field(default_factory=lambda: new_id("remotion_props"))
    timeline_program_id: str
    input_props: dict[str, Any]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.input_props.get("timeline_program_id") != self.timeline_program_id:
            raise ValueError("Remotion props must include matching timeline_program_id")


class MotionCanvasProgramBinding(BaseModel):
    motion_canvas_program_binding_id: str = Field(default_factory=lambda: new_id("motion_canvas"))
    scene_id: str
    program_ref: str


class ProxyRenderContract(BaseModel):
    proxy_render_contract_id: str = Field(default_factory=lambda: new_id("proxy_render_contract"))
    timeline_program_id: str
    remotion_input_props_id: str
    output_profile: str = "proxy_720p"
    provider_calls_allowed: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.provider_calls_allowed:
            raise ValueError("Proxy render cannot call providers")


class FinalRenderContract(BaseModel):
    final_render_contract_id: str = Field(default_factory=lambda: new_id("final_render_contract"))
    timeline_program_id: str
    timeline_locked: bool
    asset_hashes: dict[str, str]
    provider_calls_allowed: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.timeline_locked:
            raise ValueError("Final render requires locked timeline")
        if self.provider_calls_allowed:
            raise ValueError("Final render cannot call providers")
        if not self.asset_hashes:
            raise ValueError("Final render requires asset hashes")


class ProxyRenderReceipt(BaseModel):
    proxy_render_receipt_id: str = Field(default_factory=lambda: new_id("proxy_receipt"))
    proxy_render_contract_id: str
    output_uri: str
    output_sha256: str
    fake_render: bool = True


class FinalRenderReceipt(BaseModel):
    final_render_receipt_id: str = Field(default_factory=lambda: new_id("final_receipt"))
    final_render_contract_id: str
    output_uri: str
    output_sha256: str
    fake_render: bool = True


class FFmpegFinishPlan(BaseModel):
    ffmpeg_finish_plan_id: str = Field(default_factory=lambda: new_id("ffmpeg_finish"))
    final_render_contract_id: str
    filters: list[str] = Field(default_factory=lambda: ["scale", "loudnorm"])
    codec: str = "h264"


class TimelineIntegrityReceipt(BaseModel):
    timeline_integrity_receipt_id: str = Field(default_factory=lambda: new_id("timeline_integrity"))
    pass_status: PassStatus
    blockers: list[str] = Field(default_factory=list)


class CaptionReadabilityReceipt(BaseModel):
    caption_readability_receipt_id: str = Field(default_factory=lambda: new_id("caption_readability"))
    pass_status: PassStatus
    blockers: list[str] = Field(default_factory=list)


class AudioQualityReceipt(BaseModel):
    audio_quality_receipt_id: str = Field(default_factory=lambda: new_id("audio_quality"))
    pass_status: PassStatus
    blockers: list[str] = Field(default_factory=list)


class MotionDoctrineReceipt(BaseModel):
    motion_doctrine_receipt_id: str = Field(default_factory=lambda: new_id("motion_doctrine_receipt"))
    pass_status: PassStatus
    blockers: list[str] = Field(default_factory=list)


class VideoEvaluationReceipt(BaseModel):
    video_evaluation_receipt_id: str = Field(default_factory=lambda: new_id("video_eval"))
    timeline_program_id: str
    pass_status: PassStatus
    timeline_integrity: TimelineIntegrityReceipt
    caption_readability: CaptionReadabilityReceipt | None = None
    audio_quality: AudioQualityReceipt | None = None
    motion_doctrine: MotionDoctrineReceipt | None = None
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        blockers = list(self.blockers)
        if self.timeline_integrity.pass_status == PassStatus.FAIL:
            blockers.extend(self.timeline_integrity.blockers or ["timeline_integrity_failed"])
        for receipt in [self.caption_readability, self.audio_quality, self.motion_doctrine]:
            if receipt and receipt.pass_status == PassStatus.FAIL:
                blockers.extend(receipt.blockers)
        self.blockers = blockers
        if blockers and self.pass_status == PassStatus.PASS:
            raise ValueError("Video evaluation with blockers cannot pass")


class OperatorVideoRevisionCommand(BaseModel):
    operator_video_revision_command_id: str = Field(default_factory=lambda: new_id("video_revision_cmd"))
    command_type: str
    target_ref: str
    reason: str
    payload: dict[str, Any] = Field(default_factory=dict)


class OperatorVideoRevisionReceipt(BaseModel):
    operator_video_revision_receipt_id: str = Field(default_factory=lambda: new_id("video_revision_receipt"))
    command_id: str
    applied: bool
    notes: str | None = None


class VideoExportPack(BaseModel):
    video_export_pack_id: str = Field(default_factory=lambda: new_id("video_export"))
    variant_id: str
    final_render_receipt_id: str
    approved_variant: bool
    output_files: list[str]
    platform_caption_seed: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.approved_variant:
            raise ValueError("Export requires approved variant")
        if not self.output_files:
            raise ValueError("Export pack requires output files")


class VideoApprovalPacket(BaseModel):
    video_approval_packet_id: str = Field(default_factory=lambda: new_id("video_approval"))
    variant_id: str
    evaluation_receipt_id: str
    final_render_receipt_id: str
    approved: bool


class VideoEditingStateReceipt(BaseModel):
    video_editing_state_receipt_id: str = Field(default_factory=lambda: new_id("video_state"))
    project_id: str
    variant_id: str
    status: VideoProjectStatus
    created_at: str = Field(default_factory=_now_iso)
