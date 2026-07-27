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


class PassStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class AvatarFormatUse(str, Enum):
    FORMAT_01 = "format_01_cinematic_story"
    FORMAT_02 = "format_02_avatar_papercut_explainer"
    FORMAT_03 = "format_03_living_commentary_reactions"
    FORMAT_04 = "format_04_conscious_reactions_editing"
    SUPERVISUAL = "supervisual"
    CAROUSEL = "carousel"


class FaceMode(str, Enum):
    STORYBOOK_EXPRESSION_PLATE = "storybook_expression_plate"
    REALISTIC_PAPERIZED_EXPRESSION_PLATE = "realistic_paperized_expression_plate"


class BodyMode(str, Enum):
    PAPER_CUT_RIGGED_BODY = "paper_cut_rigged_body"


class MouthAnimationMode(str, Enum):
    DISABLED = "disabled"


class FaceAnimationMode(str, Enum):
    EXPRESSION_SWAP_PLUS_MINOR_HEAD_MOTION = "expression_swap_plus_minor_head_motion"


class RuntimeTarget(str, Enum):
    STRETCHY_STUDIO_AUTHORING = "stretchy_studio_authoring"
    SPINE_RUNTIME = "spine_runtime"
    DRAGONBONES_RUNTIME = "dragonbones_runtime"
    REMOTION_LAYER = "remotion_layer"
    MOTION_CANVAS_LAYER = "motion_canvas_layer"


class ExpressionPlateName(str, Enum):
    NEUTRAL_WARM = "neutral_warm"
    GENTLE_SMILE = "gentle_smile"
    SKEPTICAL_BROW = "skeptical_brow"
    CURIOUS_THINKING = "curious_thinking"
    SERIOUS_TRUTH = "serious_truth"
    PLAYFUL_WARNING = "playful_warning"
    COMPASSIONATE_CONCERN = "compassionate_concern"
    ENCOURAGING_CLOSE = "encouraging_close"


class BodyPoseName(str, Enum):
    POINT_UP = "point_up"
    POINT_TO_CARD = "point_to_card"
    OPEN_PALM_REVEAL = "open_palm_reveal"
    THINKING_CHIN = "thinking_chin"
    STOP_HAND = "stop_hand"
    SOFT_SHRUG = "soft_shrug"
    HOLD_CUP = "hold_cup"
    PRESENT_DIAGRAM = "present_diagram"


class GestureClipType(str, Enum):
    RAISE_FINGER = "raise_finger"
    OPEN_PALM_REVEAL = "open_palm_reveal"
    POINT_TO_CARD = "point_to_card"
    THINKING_TILT = "thinking_tilt"
    SOFT_SHRUG = "soft_shrug"
    HOLD_MUG = "hold_mug"
    STAMP_TRUTH = "stamp_truth"
    PRESENT_DIAGRAM = "present_diagram"


class AudienceProxyPersona(str, Enum):
    CONFUSED_SEEKER = "confused_seeker"
    OVERWHELMED_DOER = "overwhelmed_doer"
    SKEPTICAL_PROTECTOR = "skeptical_protector"
    GENTLE_BUILDER = "gentle_builder"


class EdgeBand(str, Enum):
    GENTLE_RECOGNITION = "gentle_recognition"
    CLEAR_CONTRAST = "clear_contrast"
    UNCOMFORTABLE_TRUTH = "uncomfortable_truth"
    SHARP_CHALLENGE = "sharp_challenge"
    HIGH_AROUSAL_DEBATE = "high_arousal_debate"


class MockingRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AvatarIdentityProfile(BaseModel):
    avatar_identity_profile_id: str = Field(default_factory=lambda: new_id("avatar_identity"))
    brand_id: str
    brand_context_version_id: str
    avatar_id: str
    display_name: str
    identity_pack_ref: str | None = None
    visual_dna_ref: str | None = None
    face_plate_set_id: str | None = None
    body_rig_manifest_id: str | None = None
    style_name: str = "CCP Paper-Cut Anime Editorial"
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")
        if not self.avatar_id:
            raise ValueError("avatar_id is required")


class AvatarHybridDesignSpec(BaseModel):
    avatar_hybrid_design_spec_id: str = Field(default_factory=lambda: new_id("hybrid_design"))
    avatar_id: str
    face_mode: FaceMode = FaceMode.STORYBOOK_EXPRESSION_PLATE
    body_mode: BodyMode = BodyMode.PAPER_CUT_RIGGED_BODY
    mouth_animation: MouthAnimationMode = MouthAnimationMode.DISABLED
    face_animation: FaceAnimationMode = FaceAnimationMode.EXPRESSION_SWAP_PLUS_MINOR_HEAD_MOTION
    material_unification: list[str] = Field(default_factory=lambda: ["paper_texture_overlay", "cutout_border", "coherent_shadow"])
    lip_sync_enabled: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.lip_sync_enabled:
            raise ValueError("Avatar Performance Layer V1 forbids lip sync")
        if self.mouth_animation != MouthAnimationMode.DISABLED:
            raise ValueError("Mouth animation must be disabled")
        if self.face_animation != FaceAnimationMode.EXPRESSION_SWAP_PLUS_MINOR_HEAD_MOTION:
            raise ValueError("Face animation must be expression swap plus minor head motion only")
        required = {"paper_texture_overlay", "cutout_border", "coherent_shadow"}
        if not required.issubset(set(self.material_unification)):
            raise ValueError("Hybrid avatar requires paper texture, cutout border, and coherent shadow")


class AvatarFacePlate(BaseModel):
    avatar_face_plate_id: str = Field(default_factory=lambda: new_id("face_plate"))
    avatar_id: str
    expression_name: ExpressionPlateName
    image_ref: str
    mouth_animation: MouthAnimationMode = MouthAnimationMode.DISABLED
    phoneme_key: str | None = None
    viseme_key: str | None = None
    allows_minor_head_motion: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.mouth_animation != MouthAnimationMode.DISABLED:
            raise ValueError("Face plates cannot carry mouth animation")
        if self.phoneme_key or self.viseme_key:
            raise ValueError("Face plates cannot carry phoneme or viseme keys")


class AvatarFacePlateSet(BaseModel):
    avatar_face_plate_set_id: str = Field(default_factory=lambda: new_id("face_plate_set"))
    avatar_id: str
    plates: list[AvatarFacePlate]
    strict_eight: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        names = [plate.expression_name for plate in self.plates]
        if len(names) != len(set(names)):
            raise ValueError("Face plate set cannot contain duplicate expressions")
        if self.strict_eight and set(names) != set(ExpressionPlateName):
            raise ValueError("Face plate set must contain the 8 canonical expression plates")


class AvatarLayer(BaseModel):
    avatar_layer_id: str = Field(default_factory=lambda: new_id("avatar_layer"))
    layer_name: str
    layer_role: str
    source_ref: str
    z_index: int


class AvatarLayerGraph(BaseModel):
    avatar_layer_graph_id: str = Field(default_factory=lambda: new_id("layer_graph"))
    avatar_id: str
    layers: list[AvatarLayer]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.layers:
            raise ValueError("AvatarLayerGraph requires layers")
        z_values = [layer.z_index for layer in self.layers]
        if len(z_values) != len(set(z_values)):
            raise ValueError("Avatar layers need unique z_index values")


class AvatarRigBone(BaseModel):
    bone_id: str = Field(default_factory=lambda: new_id("bone"))
    bone_name: str
    parent_bone_name: str | None = None
    pivot_x: float = 0.0
    pivot_y: float = 0.0


class AvatarPivotMap(BaseModel):
    avatar_pivot_map_id: str = Field(default_factory=lambda: new_id("pivot_map"))
    pivot_by_layer: dict[str, tuple[float, float]]


class AvatarBodyRigManifest(BaseModel):
    avatar_body_rig_manifest_id: str = Field(default_factory=lambda: new_id("body_rig"))
    avatar_id: str
    layer_graph_id: str
    bones: list[AvatarRigBone]
    pivot_map: AvatarPivotMap
    runtime_targets: list[RuntimeTarget] = Field(default_factory=lambda: [RuntimeTarget.REMOTION_LAYER])
    supports_mesh_deformation: bool = True
    supports_prop_sockets: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        bone_names = {bone.bone_name for bone in self.bones}
        required = {"torso", "neck", "head_anchor", "left_arm", "right_arm", "left_hand", "right_hand"}
        if not required.issubset(bone_names):
            raise ValueError("Body rig manifest missing required paper-cut body bones")
        if not self.supports_prop_sockets:
            raise ValueError("Avatar body rig must support prop sockets")


class AvatarBodyPose(BaseModel):
    avatar_body_pose_id: str = Field(default_factory=lambda: new_id("body_pose"))
    pose_name: BodyPoseName
    primitive_function: str
    sfl_function: str
    required_bones: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.primitive_function or not self.sfl_function:
            raise ValueError("Body pose requires primitive and SFL function")


class AvatarBodyPoseLibrary(BaseModel):
    avatar_body_pose_library_id: str = Field(default_factory=lambda: new_id("pose_library"))
    avatar_id: str
    poses: list[AvatarBodyPose]
    strict_eight: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        names = [pose.pose_name for pose in self.poses]
        if len(names) != len(set(names)):
            raise ValueError("Body pose library cannot contain duplicate poses")
        if self.strict_eight and set(names) != set(BodyPoseName):
            raise ValueError("Body pose library must contain the 8 canonical body poses")


class AvatarGestureClip(BaseModel):
    avatar_gesture_clip_id: str = Field(default_factory=lambda: new_id("gesture_clip"))
    clip_type: GestureClipType
    body_pose_name: BodyPoseName
    duration_ms: int = Field(default=900, gt=0)
    primitive_function: str
    sfl_function: str
    loopable: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.primitive_function or not self.sfl_function:
            raise ValueError("Gesture clip requires primitive and SFL function")


class AvatarGestureClipLibrary(BaseModel):
    avatar_gesture_clip_library_id: str = Field(default_factory=lambda: new_id("gesture_library"))
    avatar_id: str
    clips: list[AvatarGestureClip]


class AvatarActingState(BaseModel):
    avatar_acting_state_id: str = Field(default_factory=lambda: new_id("acting_state"))
    expression_name: ExpressionPlateName
    body_pose_name: BodyPoseName
    primitive_function: str
    sfl_function: str
    best_formats: list[AvatarFormatUse] = Field(default_factory=list)
    edge_band: EdgeBand = EdgeBand.GENTLE_RECOGNITION


class Avatar64StateActingLibrary(BaseModel):
    avatar_64_state_acting_library_id: str = Field(default_factory=lambda: new_id("acting64"))
    avatar_id: str
    states: list[AvatarActingState]
    strict_64: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        pairs = {(state.expression_name, state.body_pose_name) for state in self.states}
        if len(pairs) != len(self.states):
            raise ValueError("Acting state library cannot contain duplicate expression/pose pairs")
        if self.strict_64 and len(self.states) != 64:
            raise ValueError("64-state acting library must contain exactly 64 states")
        if self.strict_64:
            expected = {(expr, pose) for expr in ExpressionPlateName for pose in BodyPoseName}
            if pairs != expected:
                raise ValueError("64-state acting library must contain all expression×pose combinations")


class AudienceProxyPersonaSpec(BaseModel):
    audience_proxy_persona_spec_id: str = Field(default_factory=lambda: new_id("proxy_persona"))
    persona: AudienceProxyPersona
    visual_description: str
    inner_line: str
    primitive_function: str
    default_sfl_function: str
    allowed_formats: list[AvatarFormatUse]
    forbidden_uses: list[str] = Field(default_factory=list)


class AudienceProxyState(BaseModel):
    audience_proxy_state_id: str = Field(default_factory=lambda: new_id("proxy_state"))
    persona: AudienceProxyPersona
    state_name: str
    primitive_function: str
    sfl_function: str
    edge_band: EdgeBand
    mocking_risk: MockingRisk = MockingRisk.LOW

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.sfl_function:
            raise ValueError("AudienceProxyState requires SFL function")
        if self.mocking_risk == MockingRisk.HIGH:
            raise ValueError("Audience proxy mocking risk cannot be high")


class SDABoundary(BaseModel):
    sda_boundary_id: str = Field(default_factory=lambda: new_id("sda_boundary"))
    source_claim: str
    symbolic_proxy: str
    allowed_interpretation: str
    forbidden_interpretation: str


class CCVVariantGroup(BaseModel):
    ccv_variant_group_id: str = Field(default_factory=lambda: new_id("ccv_group"))
    base_identity_ref: str
    allowed_variations: list[str]
    never_vary: list[str]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.never_vary:
            raise ValueError("CCVVariantGroup requires never_vary anchors")


class PropAttachmentSocket(BaseModel):
    prop_attachment_socket_id: str = Field(default_factory=lambda: new_id("prop_socket"))
    socket_name: str
    bone_name: str
    offset_x: float = 0.0
    offset_y: float = 0.0
    rotation_degrees: float = 0.0


class AvatarPropAttachmentSpec(BaseModel):
    avatar_prop_attachment_spec_id: str = Field(default_factory=lambda: new_id("prop_attach"))
    prop_ref: str
    socket: PropAttachmentSocket
    purpose: str
    sfl_function: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.prop_ref:
            raise ValueError("Prop attachment requires prop_ref")
        if not self.sfl_function:
            raise ValueError("Prop attachment requires SFL function")


class AvatarPerformanceState(BaseModel):
    avatar_performance_state_id: str = Field(default_factory=lambda: new_id("performance_state"))
    start_ms: int = Field(ge=0)
    end_ms: int = Field(gt=0)
    expression_name: ExpressionPlateName
    body_pose_name: BodyPoseName
    gesture_clip_id: str | None = None
    prop_attachment_ids: list[str] = Field(default_factory=list)
    look_target_ref: str | None = None
    primitive_function: str
    sfl_function: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.end_ms <= self.start_ms:
            raise ValueError("AvatarPerformanceState end_ms must be after start_ms")
        if not self.primitive_function or not self.sfl_function:
            raise ValueError("AvatarPerformanceState requires primitive and SFL function")


class AvatarPerformancePlan(BaseModel):
    avatar_performance_plan_id: str = Field(default_factory=lambda: new_id("performance_plan"))
    avatar_id: str
    format_use: AvatarFormatUse
    scene_id: str
    performance_states: list[AvatarPerformanceState]
    lip_sync_enabled: bool = False
    voice_master_ref: str | None = None
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.lip_sync_enabled:
            raise ValueError("AvatarPerformancePlan forbids lip_sync_enabled=True")
        if not self.performance_states:
            raise ValueError("AvatarPerformancePlan requires performance_states")
        starts = [state.start_ms for state in self.performance_states]
        if starts != sorted(starts):
            raise ValueError("AvatarPerformancePlan states must be sorted by start_ms")


class AudienceProxyPerformancePlan(BaseModel):
    audience_proxy_performance_plan_id: str = Field(default_factory=lambda: new_id("proxy_perf"))
    scene_id: str
    persona: AudienceProxyPersona
    state_name: str
    start_ms: int = Field(ge=0)
    end_ms: int = Field(gt=0)
    primitive_function: str
    sfl_function: str
    mocking_risk: MockingRisk = MockingRisk.LOW

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.end_ms <= self.start_ms:
            raise ValueError("AudienceProxyPerformancePlan end_ms must be after start_ms")
        if not self.sfl_function:
            raise ValueError("AudienceProxyPerformancePlan requires SFL function")
        if self.mocking_risk == MockingRisk.HIGH:
            raise ValueError("Audience proxy mocking risk cannot be high")


class AvatarRenderPayload(BaseModel):
    avatar_render_payload_id: str = Field(default_factory=lambda: new_id("avatar_payload"))
    avatar_performance_plan_id: str
    runtime_target: RuntimeTarget
    layer_refs: list[str]
    performance_state_refs: list[str]
    final_render: bool = False
    provider_calls_executed: bool = False
    render_executed: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.final_render:
            raise ValueError("AvatarRenderPayload is not a final render")
        if self.provider_calls_executed or self.render_executed:
            raise ValueError("AvatarRenderPayload must not execute providers or render")
        if not self.layer_refs:
            raise ValueError("AvatarRenderPayload requires layer_refs")


class AvatarPerformanceReceipt(BaseModel):
    avatar_performance_receipt_id: str = Field(default_factory=lambda: new_id("avatar_receipt"))
    avatar_performance_plan_id: str
    pass_status: PassStatus
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blockers and self.pass_status == PassStatus.PASS:
            raise ValueError("Receipt with blockers cannot pass")


class AvatarContinuityReceipt(BaseModel):
    avatar_continuity_receipt_id: str = Field(default_factory=lambda: new_id("continuity_receipt"))
    avatar_id: str
    identity_anchors_preserved: bool
    expression_plate_set_consistent: bool
    body_rig_consistent: bool
    pass_status: PassStatus


class AvatarUncannyRiskReceipt(BaseModel):
    avatar_uncanny_risk_receipt_id: str = Field(default_factory=lambda: new_id("uncanny_receipt"))
    avatar_id: str
    face_morphing_detected: bool = False
    lip_sync_detected: bool = False
    mouth_flap_detected: bool = False
    mismatched_lighting_detected: bool = False
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        auto_blockers = list(self.blockers)
        if self.face_morphing_detected:
            auto_blockers.append("face_morphing_detected")
        if self.lip_sync_detected:
            auto_blockers.append("lip_sync_detected")
        if self.mouth_flap_detected:
            auto_blockers.append("mouth_flap_detected")
        if auto_blockers:
            self.blockers = sorted(set(auto_blockers))
            self.pass_status = PassStatus.FAIL


class AvatarFormatFitReceipt(BaseModel):
    avatar_format_fit_receipt_id: str = Field(default_factory=lambda: new_id("format_fit_receipt"))
    format_use: AvatarFormatUse
    avatar_usage_role: str
    pass_status: PassStatus
    rationale: str
