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


def validate_relative_asset_path(value: str, field_name: str = "asset_path") -> str:
    if not value:
        raise ValueError(f"{field_name} is required")
    normalized = value.replace("\\", "/")
    if normalized.startswith("/") or "://" in normalized:
        # URI refs are allowed because they are pointers, not local paths.
        return value
    pure = PurePosixPath(normalized)
    if pure.is_absolute() or ".." in pure.parts or any(part in {"", "."} for part in pure.parts):
        raise ValueError(f"{field_name} cannot contain path traversal or absolute/current path")
    return str(pure)


class PassStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class MouthAnimationMode(str, Enum):
    DISABLED = "disabled"


class FacePlateMode(str, Enum):
    EXPRESSION_PLATE = "expression_plate"
    PAPERIZED_REALISTIC_EXPRESSION_PLATE = "paperized_realistic_expression_plate"
    STORYBOOK_ANIME_EXPRESSION_PLATE = "storybook_anime_expression_plate"


class BodyMode(str, Enum):
    PAPER_CUT_RIGGED_BODY = "paper_cut_rigged_body"


class ExpressionPlateName(str, Enum):
    NEUTRAL_WARM = "neutral_warm"
    GENTLE_SMILE = "gentle_smile"
    SKEPTICAL_BROW = "skeptical_brow"
    CURIOUS_THINKING = "curious_thinking"
    SERIOUS_TRUTH = "serious_truth"
    PLAYFUL_WARNING = "playful_warning"
    COMPASSIONATE_CONCERN = "compassionate_concern"
    ENCOURAGING_CLOSE = "encouraging_close"


class CanonicalBodyLayerName(str, Enum):
    HEAD_ANCHOR = "head_anchor"
    TORSO = "torso"
    LEFT_ARM = "left_arm"
    RIGHT_ARM = "right_arm"
    LEFT_HAND = "left_hand"
    RIGHT_HAND = "right_hand"
    CLOTHES = "clothes"
    PAPER_EDGE = "paper_edge"
    SHADOW = "shadow"


class RuntimeExportTarget(str, Enum):
    STRETCHY_STUDIO = "stretchy_studio"
    SPINE = "spine"
    DRAGONBONES = "dragonbones"
    REMOTION = "remotion"


class MeshCandidateKind(str, Enum):
    LIMB_BEND = "limb_bend"
    CLOTH_DEFORM = "cloth_deform"
    HAIR_OR_HEADWRAP_FLOW = "hair_or_headwrap_flow"
    PAPER_WOBBLE = "paper_wobble"
    SUBTLE_BREATH = "subtle_breath"


class ShapeKeyKind(str, Enum):
    BLINK = "blink"
    BROW_RAISE = "brow_raise"
    SOFT_SMILE = "soft_smile"
    PAPER_SETTLE = "paper_settle"


class PropSocketName(str, Enum):
    LEFT_HAND = "left_hand"
    RIGHT_HAND = "right_hand"
    ABOVE_HEAD = "above_head"
    CARD_SURFACE = "card_surface"
    DIAGRAM_NODE = "diagram_node"
    TABLE_ANCHOR = "table_anchor"


class ActionClipName(str, Enum):
    RAISE_FINGER = "raise_finger"
    OPEN_PALM_REVEAL = "open_palm_reveal"
    POINT_TO_CARD = "point_to_card"
    THINKING_TILT = "thinking_tilt"
    SOFT_SHRUG = "soft_shrug"
    HOLD_MUG = "hold_mug"
    STAMP_TRUTH = "stamp_truth"
    PRESENT_DIAGRAM = "present_diagram"


class AvatarCharacterSpec(BaseModel):
    avatar_character_spec_id: str = Field(default_factory=lambda: new_id("avatar_character"))
    avatar_id: str
    brand_id: str
    brand_context_version_id: str
    character_name: str
    style_name: str = "CCP Paper-Cut Anime Editorial"
    face_plate_mode: FacePlateMode = FacePlateMode.STORYBOOK_ANIME_EXPRESSION_PLATE
    body_mode: BodyMode = BodyMode.PAPER_CUT_RIGGED_BODY
    mouth_animation: MouthAnimationMode = MouthAnimationMode.DISABLED
    lip_sync_enabled: bool = False
    identity_anchor_refs: list[str] = Field(default_factory=list)
    paper_material_profile_ref: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")
        if self.lip_sync_enabled:
            raise ValueError("AvatarCharacterSpec forbids lip_sync_enabled=True")
        if self.mouth_animation != MouthAnimationMode.DISABLED:
            raise ValueError("Mouth animation must be disabled")
        if not self.identity_anchor_refs:
            raise ValueError("AvatarCharacterSpec requires identity_anchor_refs")


class AvatarPSDLayerRequirement(BaseModel):
    avatar_psd_layer_requirement_id: str = Field(default_factory=lambda: new_id("psd_layer_req"))
    layer_name: str
    canonical_layer: CanonicalBodyLayerName
    source_path: str
    required: bool = True
    z_index: int
    pivot_hint: tuple[float, float] = (0.5, 0.5)
    mesh_candidate: bool = True
    notes: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.layer_name:
            raise ValueError("PSD layer requirement requires layer_name")
        self.source_path = validate_relative_asset_path(self.source_path, "PSD layer source_path")


class AvatarFacePlateAsset(BaseModel):
    avatar_face_plate_asset_id: str = Field(default_factory=lambda: new_id("face_plate_asset"))
    expression_name: ExpressionPlateName
    asset_ref: str
    approved: bool = False
    sha256: str | None = None
    phoneme_key: str | None = None
    viseme_key: str | None = None
    mouth_animation: MouthAnimationMode = MouthAnimationMode.DISABLED

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.asset_ref = validate_relative_asset_path(self.asset_ref, "face plate asset_ref")
        if self.phoneme_key or self.viseme_key:
            raise ValueError("Face plate assets cannot carry phoneme or viseme keys")
        if self.mouth_animation != MouthAnimationMode.DISABLED:
            raise ValueError("Face plate asset mouth animation must be disabled")


class AvatarFacePlateApprovalSet(BaseModel):
    avatar_face_plate_approval_set_id: str = Field(default_factory=lambda: new_id("face_plate_approval"))
    avatar_id: str
    face_plates: list[AvatarFacePlateAsset]
    approved_by: str | None = None
    strict_eight: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        names = [plate.expression_name for plate in self.face_plates]
        if len(names) != len(set(names)):
            raise ValueError("Face plate approval set cannot contain duplicate expressions")
        if self.strict_eight and set(names) != set(ExpressionPlateName):
            raise ValueError("Face plate approval set requires the 8 canonical expressions")
        if not all(plate.approved for plate in self.face_plates):
            raise ValueError("All face plates must be approved in approval set")
        if not self.approved_by:
            raise ValueError("Face plate approval set requires approved_by")


class AvatarPaperBodyLayer(BaseModel):
    avatar_paper_body_layer_id: str = Field(default_factory=lambda: new_id("body_layer"))
    canonical_layer: CanonicalBodyLayerName
    asset_ref: str
    z_index: int
    pivot_hint: tuple[float, float] = (0.5, 0.5)
    riggable: bool = True
    mesh_candidate: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.asset_ref = validate_relative_asset_path(self.asset_ref, "body layer asset_ref")
        if self.riggable is False and self.canonical_layer in {
            CanonicalBodyLayerName.LEFT_ARM,
            CanonicalBodyLayerName.RIGHT_ARM,
            CanonicalBodyLayerName.LEFT_HAND,
            CanonicalBodyLayerName.RIGHT_HAND,
            CanonicalBodyLayerName.TORSO,
        }:
            raise ValueError("Core body layers must be riggable")


class AvatarPaperBodyLayerSet(BaseModel):
    avatar_paper_body_layer_set_id: str = Field(default_factory=lambda: new_id("body_layer_set"))
    avatar_id: str
    layers: list[AvatarPaperBodyLayer]
    strict_canonical: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        names = [layer.canonical_layer for layer in self.layers]
        if len(names) != len(set(names)):
            raise ValueError("Body layer set cannot contain duplicate canonical layers")
        if self.strict_canonical and set(names) != set(CanonicalBodyLayerName):
            raise ValueError("Body layer set requires canonical paper body layers")


class AvatarRigBoneHint(BaseModel):
    bone_name: str
    parent_bone_name: str | None = None
    target_layer: CanonicalBodyLayerName
    pivot_hint: tuple[float, float] = (0.5, 0.5)


class AvatarPropSocketSpec(BaseModel):
    avatar_prop_socket_spec_id: str = Field(default_factory=lambda: new_id("prop_socket"))
    socket_name: PropSocketName
    target_bone_name: str
    target_layer: CanonicalBodyLayerName
    offset_hint: tuple[float, float] = (0.0, 0.0)


class AvatarMeshCandidate(BaseModel):
    avatar_mesh_candidate_id: str = Field(default_factory=lambda: new_id("mesh_candidate"))
    kind: MeshCandidateKind
    target_layer: CanonicalBodyLayerName
    reason: str


class AvatarShapeKeyCandidate(BaseModel):
    avatar_shape_key_candidate_id: str = Field(default_factory=lambda: new_id("shape_key"))
    kind: ShapeKeyKind
    target_layer: CanonicalBodyLayerName
    reason: str


class AvatarAssetProductionPlan(BaseModel):
    avatar_asset_production_plan_id: str = Field(default_factory=lambda: new_id("asset_plan"))
    avatar_character_spec: AvatarCharacterSpec
    psd_layer_requirements: list[AvatarPSDLayerRequirement]
    face_plate_approval_set_id: str | None = None
    body_layer_set_id: str | None = None
    target_exports: list[RuntimeExportTarget] = Field(default_factory=lambda: [RuntimeExportTarget.STRETCHY_STUDIO, RuntimeExportTarget.REMOTION])
    sample_required_before_batch: bool = True
    sample_approved: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.psd_layer_requirements:
            raise ValueError("AvatarAssetProductionPlan requires PSD layer requirements")
        required_layers = {req.canonical_layer for req in self.psd_layer_requirements if req.required}
        missing = set(CanonicalBodyLayerName) - required_layers
        if missing:
            raise ValueError(f"AvatarAssetProductionPlan missing required PSD layers: {sorted(m.value for m in missing)}")


class StretchyStudioImportManifest(BaseModel):
    stretchy_studio_import_manifest_id: str = Field(default_factory=lambda: new_id("stretchy_manifest"))
    avatar_id: str
    source_psd_ref: str
    layer_requirements: list[AvatarPSDLayerRequirement]
    skeleton_hints: list[AvatarRigBoneHint]
    mesh_candidates: list[AvatarMeshCandidate]
    shape_key_candidates: list[AvatarShapeKeyCandidate] = Field(default_factory=list)
    prop_sockets: list[AvatarPropSocketSpec]
    action_timeline_ref: str | None = None
    see_through_source: bool = False
    notes: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.source_psd_ref = validate_relative_asset_path(self.source_psd_ref, "source_psd_ref")
        if not self.layer_requirements:
            raise ValueError("StretchyStudioImportManifest requires layer_requirements")
        if not self.skeleton_hints:
            raise ValueError("StretchyStudioImportManifest requires skeleton_hints")
        if not self.mesh_candidates:
            raise ValueError("StretchyStudioImportManifest requires mesh_candidates")
        if not self.prop_sockets:
            raise ValueError("StretchyStudioImportManifest requires prop_sockets")


class SpineExportManifest(BaseModel):
    spine_export_manifest_id: str = Field(default_factory=lambda: new_id("spine_export"))
    avatar_id: str
    source_stretchy_manifest_id: str
    output_json_ref: str
    output_atlas_ref: str | None = None
    spine_version: str = "4.0"
    license_confirmed: bool = False
    animation_clip_refs: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.output_json_ref = validate_relative_asset_path(self.output_json_ref, "spine output_json_ref")
        if self.output_atlas_ref:
            self.output_atlas_ref = validate_relative_asset_path(self.output_atlas_ref, "spine output_atlas_ref")
        if not self.license_confirmed:
            raise ValueError("Spine export requires license confirmation")


class DragonBonesExportManifest(BaseModel):
    dragonbones_export_manifest_id: str = Field(default_factory=lambda: new_id("dragonbones_export"))
    avatar_id: str
    source_stretchy_manifest_id: str
    output_json_ref: str
    output_texture_atlas_ref: str | None = None
    js_runtime_compatible: bool = False
    animation_clip_refs: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.output_json_ref = validate_relative_asset_path(self.output_json_ref, "dragonbones output_json_ref")
        if self.output_texture_atlas_ref:
            self.output_texture_atlas_ref = validate_relative_asset_path(self.output_texture_atlas_ref, "dragonbones output_texture_atlas_ref")
        if not self.js_runtime_compatible:
            raise ValueError("DragonBones export requires JS runtime compatibility declaration")


class AvatarRigExportManifest(BaseModel):
    avatar_rig_export_manifest_id: str = Field(default_factory=lambda: new_id("rig_export"))
    avatar_id: str
    stretchy_studio_import_manifest_id: str
    spine_export_manifest_id: str | None = None
    dragonbones_export_manifest_id: str | None = None
    remotion_layer_payload_id: str | None = None
    export_targets: list[RuntimeExportTarget]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.export_targets:
            raise ValueError("AvatarRigExportManifest requires export_targets")
        if RuntimeExportTarget.SPINE in self.export_targets and not self.spine_export_manifest_id:
            raise ValueError("Spine target requires spine_export_manifest_id")
        if RuntimeExportTarget.DRAGONBONES in self.export_targets and not self.dragonbones_export_manifest_id:
            raise ValueError("DragonBones target requires dragonbones_export_manifest_id")


class AvatarActionClipSpec(BaseModel):
    avatar_action_clip_spec_id: str = Field(default_factory=lambda: new_id("action_clip"))
    clip_name: ActionClipName
    start_ms: int = Field(ge=0)
    end_ms: int = Field(gt=0)
    primitive_function: str
    sfl_function: str
    target_runtime: RuntimeExportTarget = RuntimeExportTarget.STRETCHY_STUDIO
    lip_sync_enabled: bool = False
    mouth_flap: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.end_ms <= self.start_ms:
            raise ValueError("AvatarActionClipSpec requires positive duration")
        if self.lip_sync_enabled or self.mouth_flap:
            raise ValueError("AvatarActionClipSpec forbids lip sync and mouth flap")
        if not self.primitive_function or not self.sfl_function:
            raise ValueError("AvatarActionClipSpec requires primitive and SFL function")


class AvatarActionTimeline(BaseModel):
    avatar_action_timeline_id: str = Field(default_factory=lambda: new_id("action_timeline"))
    avatar_id: str
    clips: list[AvatarActionClipSpec]
    total_duration_ms: int = Field(gt=0)
    lip_sync_enabled: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.lip_sync_enabled:
            raise ValueError("AvatarActionTimeline forbids lip_sync_enabled=True")
        if not self.clips:
            raise ValueError("AvatarActionTimeline requires clips")
        if max(clip.end_ms for clip in self.clips) > self.total_duration_ms:
            raise ValueError("AvatarActionTimeline total_duration_ms must cover clips")


class AvatarRemotionLayerPayload(BaseModel):
    avatar_remotion_layer_payload_id: str = Field(default_factory=lambda: new_id("remotion_avatar"))
    avatar_id: str
    layer_refs: list[str]
    action_timeline_ref: str
    rig_export_manifest_ref: str
    runtime_props: dict[str, Any] = Field(default_factory=dict)
    final_render: bool = False
    renderer_calls_executed: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.layer_refs:
            raise ValueError("AvatarRemotionLayerPayload requires layer_refs")
        if self.final_render or self.renderer_calls_executed:
            raise ValueError("AvatarRemotionLayerPayload is not final render and cannot execute renderer")


class AvatarCharacterQAReport(BaseModel):
    avatar_character_qa_report_id: str = Field(default_factory=lambda: new_id("avatar_qa"))
    avatar_id: str
    face_plate_count: int
    body_layer_count: int
    required_bones_present: bool
    prop_sockets_present: bool
    no_lipsync_policy_pass: bool
    path_safety_pass: bool
    export_manifests_valid: bool
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        blockers = list(self.blockers)
        if self.face_plate_count != 8:
            blockers.append("face_plate_count_not_8")
        if self.body_layer_count < len(CanonicalBodyLayerName):
            blockers.append("missing_canonical_body_layers")
        if not self.required_bones_present:
            blockers.append("required_bones_missing")
        if not self.prop_sockets_present:
            blockers.append("prop_sockets_missing")
        if not self.no_lipsync_policy_pass:
            blockers.append("no_lipsync_policy_failed")
        if not self.path_safety_pass:
            blockers.append("path_safety_failed")
        if not self.export_manifests_valid:
            blockers.append("export_manifests_invalid")
        self.blockers = sorted(set(blockers))
        self.pass_status = PassStatus.FAIL if self.blockers else PassStatus.PASS


class AvatarRigContinuityReceipt(BaseModel):
    avatar_rig_continuity_receipt_id: str = Field(default_factory=lambda: new_id("rig_continuity"))
    avatar_id: str
    identity_anchors_preserved: bool
    face_plate_set_stable: bool
    body_layer_set_stable: bool
    rig_version_stable: bool
    paper_material_profile_stable: bool
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        blockers = list(self.blockers)
        if not self.identity_anchors_preserved:
            blockers.append("identity_anchors_drift")
        if not self.face_plate_set_stable:
            blockers.append("face_plate_set_drift")
        if not self.body_layer_set_stable:
            blockers.append("body_layer_set_drift")
        if not self.rig_version_stable:
            blockers.append("rig_version_drift")
        if not self.paper_material_profile_stable:
            blockers.append("paper_material_profile_drift")
        self.blockers = sorted(set(blockers))
        self.pass_status = PassStatus.FAIL if self.blockers else PassStatus.PASS
