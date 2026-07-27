from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)


class ProgramStatus(str, Enum):
    DRAFT = "draft"
    COMPILED = "compiled"
    BLOCKING_PREVIEW_READY = "blocking_preview_ready"
    REVISION_REQUESTED = "revision_requested"
    FINAL_PREVIEW_READY = "final_preview_ready"
    APPROVED_FOR_RENDER = "approved_for_render"
    RENDERING = "rendering"
    RENDERED = "rendered"
    APPROVED_FOR_PUBLISH = "approved_for_publish"
    REJECTED = "rejected"


class AssetRef(StrictModel):
    uri: str
    sha256: str
    mime_type: Optional[str] = None
    size_bytes: Optional[int] = Field(default=None, ge=0)


class Timebase(StrictModel):
    ticks_per_second: int = Field(default=48000, gt=0)
    audio_sample_rate: int = Field(default=48000, gt=0)
    fps_numerator: int = Field(default=30, gt=0)
    fps_denominator: int = Field(default=1, gt=0)
    duration_ticks: int = Field(gt=0)

    def tick_to_frame(self, tick: int) -> int:
        return round(tick * self.fps_numerator / (self.ticks_per_second * self.fps_denominator))


class ContextRefs(StrictModel):
    brand_id: str
    brand_context_version_id: str
    interview_brief_id: str
    interview_asset_contract_id: str
    complete_expression_session_id: str
    transcript_beat_map_id: str
    expression_moment_ids: List[str]
    voice_dna_version_id: str
    visual_dna_version_id: str
    primitive_eval_bundle_id: str
    doctrine_bundle_id: str
    asset_package_spec_id: str
    scene_template_id: str
    format_target: str


class CharacterRefs(StrictModel):
    identity_pack_id: str
    character_art_version_id: str
    layered_asset_version_id: str
    rig_version_id: str
    performance_library_version_id: str
    acting_library_version_id: str
    costume_skin: str
    micro_semiotic_anchor_skins: List[str] = Field(default_factory=list)


class CoordinateSystem(StrictModel):
    origin: str = "character_root"
    x_axis: Literal["right", "left"] = "right"
    y_axis: Literal["up", "down"] = "up"
    units: str = "pixels_at_design_resolution"


class SidecarRef(StrictModel):
    uri: str
    sha256: str
    format: Optional[str] = None


class AttachmentPoint(StrictModel):
    id: str
    bone_id: str
    local_position: List[float] = Field(min_length=2, max_length=2)
    local_rotation: float = 0.0


class LayerNode(StrictModel):
    layer_id: str
    semantic_type: str
    side: Optional[Literal["left", "right", "center"]] = None
    source_name: str
    parent_id: Optional[str] = None
    draw_order: int
    canvas_rect: List[int] = Field(min_length=4, max_length=4)
    pivot_hint: Optional[List[float]] = Field(default=None, min_length=2, max_length=2)
    texture_ref: AssetRef
    mask_ids: List[str] = Field(default_factory=list)
    material_id: str
    visible: bool = True


class BoneNode(StrictModel):
    bone_id: str
    parent_id: Optional[str] = None
    x: float = 0.0
    y: float = 0.0
    rotation_deg: float = 0.0
    scale_x: float = 1.0
    scale_y: float = 1.0
    shear_x_deg: float = 0.0
    shear_y_deg: float = 0.0
    rotation_min_deg: Optional[float] = None
    rotation_max_deg: Optional[float] = None
    bend_direction: Optional[Literal["positive", "negative", "either"]] = None


class ConstraintSpec(StrictModel):
    constraint_id: str
    type: Literal["one_bone_ik", "two_bone_ik", "transform", "path", "gaze"]
    bones: List[str]
    target: str
    mix: float = Field(default=1.0, ge=0.0, le=1.0)
    softness: float = 0.0
    bend_direction: Optional[Literal["positive", "negative"]] = None


class RigManifest(StrictModel):
    rig_id: str
    coordinate_system: CoordinateSystem = Field(default_factory=CoordinateSystem)
    setup_pose_id: str
    layers: List[LayerNode]
    bones: List[BoneNode]
    mesh_bundle_ref: SidecarRef
    shape_key_bundle_ref: SidecarRef
    masks_ref: SidecarRef
    constraints: List[ConstraintSpec] = Field(default_factory=list)
    attachment_points: List[AttachmentPoint] = Field(default_factory=list)
    material_profile_id: str
    runtime_export_refs: List[AssetRef] = Field(default_factory=list)


class EmotionSpec(StrictModel):
    primary: str
    secondary: Optional[str] = None
    intensity: float = Field(default=0.5, ge=0.0, le=1.0)


class ActingState(StrictModel):
    state_id: str
    communicative_intent: str
    emotion: EmotionSpec
    base_clip: str
    gesture_clip: Optional[str] = None
    face_pose: str
    gaze_policy: str
    hand_pose_L: Optional[str] = None
    hand_pose_R: Optional[str] = None
    energy: float = Field(ge=0.0, le=1.0)
    minimum_hold_ticks: int = Field(ge=0)
    transition_in_ticks: int = Field(ge=0)
    transition_out_ticks: int = Field(ge=0)
    primitive_affinities: List[str] = Field(default_factory=list)
    forbidden_contexts: List[str] = Field(default_factory=list)


class TransitionRule(StrictModel):
    from_state: str
    to_state: str
    allowed: bool
    min_mix_ticks: int = Field(ge=0)
    max_mix_ticks: int = Field(ge=0)
    bridge_clip: Optional[str] = None


class PerformanceLibrary(StrictModel):
    library_id: str
    acting_states: List[ActingState]
    transition_rules: List[TransitionRule]
    viseme_map_id: str
    facial_pose_map_id: str
    gaze_map_id: str
    hand_pose_map_id: str
    prop_action_map_id: str


class CueAction(str, Enum):
    PLAY_CLIP = "play_clip"
    APPLY_ACTING_STATE = "apply_acting_state"
    SET_GAZE = "set_gaze"
    SET_SHAPE_KEY = "set_shape_key"
    ATTACH_PROP = "attach_prop"
    DETACH_PROP = "detach_prop"
    SET_ATTACHMENT = "set_attachment"
    SET_DRAW_ORDER = "set_draw_order"
    SET_PARAMETER = "set_parameter"


class PerformanceCue(StrictModel):
    cue_id: str
    start_tick: int = Field(ge=0)
    end_tick: Optional[int] = Field(default=None, ge=0)
    action: CueAction
    clip_id: Optional[str] = None
    state_id: Optional[str] = None
    target_id: Optional[str] = None
    value: Optional[Union[str, float, int, bool, Dict[str, Any], List[Any]]] = None
    loop: bool = False
    mix_in_ticks: int = Field(default=0, ge=0)
    mix_out_ticks: int = Field(default=0, ge=0)
    semantic_target: Optional[str] = None

    @model_validator(mode="after")
    def validate_range(self):
        if self.end_tick is not None and self.end_tick < self.start_tick:
            raise ValueError("end_tick must be >= start_tick")
        return self


class PerformanceTrack(StrictModel):
    track_id: str
    priority: int
    property_scope: List[str]
    cues: List[PerformanceCue] = Field(default_factory=list)
    cue_ref: Optional[SidecarRef] = None


class TranscriptAlignment(StrictModel):
    word_alignment_ref: SidecarRef
    phoneme_alignment_ref: Optional[SidecarRef] = None
    viseme_cues_ref: SidecarRef
    alignment_confidence: float = Field(ge=0.0, le=1.0)
    manual_repairs: List[Dict[str, Any]] = Field(default_factory=list)


class CharacterPosition(StrictModel):
    x: float
    y: float
    scale: float = Field(gt=0)
    rotation_deg: float = 0.0


class CameraCue(StrictModel):
    start_tick: int = Field(ge=0)
    end_tick: int = Field(gt=0)
    motion: str
    scale_from: float = 1.0
    scale_to: float = 1.0
    x_from: float = 0.0
    x_to: float = 0.0
    y_from: float = 0.0
    y_to: float = 0.0
    easing: str = "linear"


class SceneObjectCue(StrictModel):
    object_id: str
    start_tick: int = Field(ge=0)
    end_tick: Optional[int] = Field(default=None, ge=0)
    motion_path_id: str
    target_attachment: Optional[str] = None


class MotionCanvasChoreography(StrictModel):
    template_id: str
    character_position: CharacterPosition
    camera_cues: List[CameraCue] = Field(default_factory=list)
    scene_object_cues: List[SceneObjectCue] = Field(default_factory=list)
    seed: str


class RemotionComposition(StrictModel):
    composition_id: str
    width: int = Field(gt=0)
    height: int = Field(gt=0)
    fps: int = Field(gt=0)
    duration_in_frames: int = Field(gt=0)
    character_render_mode: Literal["embedded_spine_runtime", "precomposed_rgba_plate", "native_runtime"]
    subtitle_profile_id: str
    background_scene_id: str
    safe_zone_profile_id: str
    audio_master_ref: str
    seed: str


class FFmpegFinishing(StrictModel):
    video_codec: str = "h264"
    pixel_format: str = "yuv420p"
    audio_codec: str = "aac"
    audio_bitrate: str = "192k"
    voice_loudness_target_lufs: float = -16.0
    true_peak_target_db: float = -1.5
    music_ducking_profile: str
    output_variants: List[str]


class EvalGateResult(StrictModel):
    gate_id: str
    score: float = Field(ge=0.0, le=1.0)
    threshold: float = Field(ge=0.0, le=1.0)
    passed: bool
    notes: List[str] = Field(default_factory=list)


class EvaluationSpec(StrictModel):
    required_gates: List[str]
    thresholds: Dict[str, float]
    results: List[EvalGateResult] = Field(default_factory=list)


class OperatorApproval(StrictModel):
    status: Literal["not_reviewed", "revision_requested", "approved", "rejected"]
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None
    approval_surface: Optional[str] = None
    revision_history_ids: List[str] = Field(default_factory=list)


class RenderReceipt(StrictModel):
    program_sha256: Optional[str] = None
    python_harness_image_digest: str
    motion_canvas_image_digest: str
    remotion_image_digest: str
    ffmpeg_version: str
    character_runtime_version: str
    font_hashes: List[str] = Field(default_factory=list)
    provider_output_hashes: List[str] = Field(default_factory=list)
    rendered_file_sha256: Optional[str] = None


class AssetBundle(StrictModel):
    psd: AssetRef
    spine_skeleton: Optional[AssetRef] = None
    atlas: Optional[AssetRef] = None
    textures: List[AssetRef]
    audio_master: AssetRef


class TwoDCharacterProgram(StrictModel):
    schema_version: str = "1.0.0"
    program_id: str
    status: ProgramStatus
    timebase: Timebase
    context_refs: ContextRefs
    character: CharacterRefs
    asset_bundle: AssetBundle
    rig_manifest: RigManifest
    performance_library: PerformanceLibrary
    transcript_alignment: TranscriptAlignment
    performance_tracks: List[PerformanceTrack]
    motion_canvas_choreography: MotionCanvasChoreography
    remotion_composition: RemotionComposition
    ffmpeg_finishing: FFmpegFinishing
    evaluation: EvaluationSpec
    operator_approval: OperatorApproval
    receipt: RenderReceipt

    @model_validator(mode="after")
    def validate_timing(self):
        max_tick = self.timebase.duration_ticks
        for track in self.performance_tracks:
            for cue in track.cues:
                if cue.start_tick > max_tick:
                    raise ValueError(f"cue {cue.cue_id} starts after program duration")
                if cue.end_tick is not None and cue.end_tick > max_tick:
                    raise ValueError(f"cue {cue.cue_id} ends after program duration")
        expected_frames = self.timebase.tick_to_frame(max_tick)
        if abs(expected_frames - self.remotion_composition.duration_in_frames) > 1:
            raise ValueError("Remotion duration does not match canonical timebase")
        return self


if __name__ == "__main__":
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    schema_dir = root / "schemas"
    schema_dir.mkdir(exist_ok=True)
    (schema_dir / "two_d_character_program.schema.json").write_text(
        json.dumps(TwoDCharacterProgram.model_json_schema(), indent=2), encoding="utf-8"
    )
    (schema_dir / "character_rig_manifest.schema.json").write_text(
        json.dumps(RigManifest.model_json_schema(), indent=2), encoding="utf-8"
    )
    (schema_dir / "performance_library.schema.json").write_text(
        json.dumps(PerformanceLibrary.model_json_schema(), indent=2), encoding="utf-8"
    )
