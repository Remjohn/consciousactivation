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


class TargetComponent(str, Enum):
    SUPERVISUAL = "supervisual"
    CAROUSEL = "carousel"
    VIDEO = "video"
    CAC = "cac"
    GMG = "gmg"
    PAPER_CUT = "paper_cut"
    DOCUMENTARY_PROOF = "documentary_proof"
    UI_REACTION_SURFACE = "ui_reaction_surface"
    CHARACTER = "character"


class PreproductionDepth(str, Enum):
    LITE = "lite"
    STANDARD = "standard"
    FULL_BATCH = "full_batch"


class PacketStatus(str, Enum):
    DRAFT = "draft"
    SCHEMA_COMPILED = "schema_compiled"
    INGREDIENTS_COMPILED = "ingredients_compiled"
    BEATS_PLANNED = "beats_planned"
    VALIDATED = "validated"
    REPAIR_REQUIRED = "repair_required"
    AUTHORIZED = "authorized"
    FROZEN = "frozen"
    DEPRECATED = "deprecated"


class PassStatus(str, Enum):
    PASS = "pass"
    PASS_WITH_RISKS = "pass_with_risks"
    FAIL = "fail"


class AuthorizationStatus(str, Enum):
    AUTHORIZED = "authorized"
    AUTHORIZED_WITH_RISKS = "authorized_with_risks"
    REPAIR_REQUIRED = "repair_required"
    REJECTED = "rejected"


class SourceAuthorityLevel(str, Enum):
    DIRECT_SOURCE = "direct_source"
    BRAND_APPROVED = "brand_approved"
    RESEARCH_SUPPORTED = "research_supported"
    INFERRED = "inferred"
    UNSUPPORTED = "unsupported"


class FamiliarityElementId(str, Enum):
    UNIVERSAL_EXPERIENCES = "universal_experiences"
    RECOGNIZABLE_EMOTIONS = "recognizable_emotions"
    FAMILIAR_BODY_TYPES = "familiar_body_types"
    DECISIVE_MOMENTS = "decisive_moments"
    CONTEXTUAL_CLUES = "contextual_clues"
    HUMAN_SCALE_SPACES = "human_scale_spaces"
    LIMINAL_SPACES = "liminal_spaces"
    CULTURAL_SYMBOLS = "cultural_symbols"
    ARCHETYPAL_COMPOSITIONS = "archetypal_compositions"
    NATURAL_FRAMING = "natural_framing"
    FOCAL_POINT_RULE = "focal_point_rule"
    LIGHTING_CONTEXTS = "lighting_contexts"
    COLOR_PALETTE = "color_palette"
    NOSTALGIC_AESTHETIC = "nostalgic_aesthetic"
    LIGHT_QUALITY = "light_quality"
    VISUAL_TROPES_USE_AVOID = "visual_tropes_use_avoid"


REQUIRED_FAMILIARITY_ELEMENTS = {item.value for item in FamiliarityElementId}


class ShotType(str, Enum):
    EXTREME_CLOSE_UP = "extreme_close_up"
    CLOSE_UP = "close_up"
    MEDIUM_CLOSE_UP = "medium_close_up"
    MEDIUM_SHOT = "medium_shot"
    WIDE_SHOT = "wide_shot"
    OVER_THE_SHOULDER = "over_the_shoulder"
    TOP_DOWN = "top_down"
    INSERT = "insert"
    MACRO_DETAIL = "macro_detail"
    SPLIT_SCREEN = "split_screen"
    STATIC_PROOF_CARD = "static_proof_card"
    UI_CAPTURE = "ui_capture"
    DIAGRAM_FRAME = "diagram_frame"


class TCode(str, Enum):
    T_SOURCE_PROOF = "T_SOURCE_PROOF"
    T_MEMORY_SCENE = "T_MEMORY_SCENE"
    T_IDENTITY_ANCHOR = "T_IDENTITY_ANCHOR"
    T_EXPLANATORY_MODEL = "T_EXPLANATORY_MODEL"
    T_CONTRADICTION = "T_CONTRADICTION"
    T_REVELATION = "T_REVELATION"
    T_TRANSITION = "T_TRANSITION"
    T_EMOTIONAL_TURN = "T_EMOTIONAL_TURN"


class VCode(str, Enum):
    V_HUMAN_SCALE = "V_HUMAN_SCALE"
    V_OBJECT_ANCHOR = "V_OBJECT_ANCHOR"
    V_DOCUMENTARY_PROOF = "V_DOCUMENTARY_PROOF"
    V_PAPER_CUT_ARTIFACT = "V_PAPER_CUT_ARTIFACT"
    V_CAC_REALISM = "V_CAC_REALISM"
    V_GMG_SYSTEM = "V_GMG_SYSTEM"
    V_EDITORIAL_CARD = "V_EDITORIAL_CARD"
    V_UI_SURFACE = "V_UI_SURFACE"


class KineticVerb(str, Enum):
    REVEAL = "reveal"
    FOLD = "fold"
    DRIFT = "drift"
    SNAP = "snap"
    TRACE = "trace"
    PULL = "pull"
    PUSH = "push"
    STACK = "stack"
    CUT = "cut"
    HOVER = "hover"
    PIN = "pin"
    TEAR = "tear"
    UNFURL = "unfurl"
    LOCK = "lock"
    BREATHE = "breathe"


class LightingPreset(str, Enum):
    MORNING_WINDOW = "morning_window"
    OVERCAST_SOFTBOX = "overcast_softbox"
    PRACTICAL_LAMP = "practical_lamp"
    DESK_LAMP = "desk_lamp"
    PHONE_SCREEN_GLOW = "phone_screen_glow"
    GOLDEN_HOUR_EDGE = "golden_hour_edge"
    DOCUMENTARY_FLAT = "documentary_flat"
    HIGH_CONTRAST_NOIR = "high_contrast_noir"
    PAPER_TABLETOP = "paper_tabletop"
    BLACK_VOID = "black_void"
    WHITE_PAPER = "white_paper"
    UI_NEUTRAL = "ui_neutral"


class CameraMoralStance(str, Enum):
    WITNESS = "witness"
    CONFESSIONAL = "confessional"
    INVESTIGATOR = "investigator"
    COMPANION = "companion"
    ARCHIVIST = "archivist"
    TEACHER = "teacher"
    OBSERVER = "observer"
    INTERROGATOR = "interrogator"


class SourceRef(BaseModel):
    source_ref_id: str = Field(default_factory=lambda: new_id("source_ref"))
    source_kind: str
    source_id: str | None = None
    description: str | None = None
    authority_level: SourceAuthorityLevel = SourceAuthorityLevel.RESEARCH_SUPPORTED


class VisualPreproductionRequest(BaseModel):
    visual_preproduction_request_id: str = Field(default_factory=lambda: new_id("vp_request"))
    brand_id: str
    brand_context_version_id: str
    target_component: TargetComponent
    preproduction_depth: PreproductionDepth
    source_context_refs: list[SourceRef] = Field(default_factory=list)
    primitive_coalition_contract_id: str | None = None
    strategy_brief_ref: str | None = None
    brand_avatar_ref: str | None = None
    target_output_ref: str | None = None
    operator_notes: str | None = None
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("VisualPreproductionRequest.brand_context_version_id is required")


class VisualFamiliarityElementAssessment(BaseModel):
    element_id: FamiliarityElementId
    finding: str | None = None
    source_evidence_refs: list[str] = Field(default_factory=list)
    score: float | None = Field(default=None, ge=0.0, le=1.0)
    not_applicable: bool = False
    not_applicable_reason: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.not_applicable and not self.not_applicable_reason:
            raise ValueError("not_applicable_reason is required when not_applicable is true")
        if not self.not_applicable and not self.finding:
            raise ValueError("finding is required unless element is not_applicable")


class VisualSchema(BaseModel):
    visual_schema_id: str = Field(default_factory=lambda: new_id("visual_schema"))
    brand_id: str
    brand_context_version_id: str
    source_context_refs: list[SourceRef] = Field(default_factory=list)
    primitive_coalition_contract_id: str | None = None
    strategy_brief_ref: str | None = None
    brand_avatar_ref: str | None = None
    target_component: TargetComponent
    preproduction_depth: PreproductionDepth
    visual_familiarity_elements: list[VisualFamiliarityElementAssessment]
    subjective_distortions: list[str] = Field(default_factory=list)
    environment_logic: str
    human_context: str | None = None
    object_logic: str | None = None
    lighting_context: str | None = None
    color_context: str | None = None
    composition_archetypes: list[str] = Field(default_factory=list)
    visual_tropes_to_use: list[str] = Field(default_factory=list)
    visual_tropes_to_avoid: list[str] = Field(default_factory=list)
    source_authority_map: dict[str, SourceAuthorityLevel] = Field(default_factory=dict)
    negative_space_risks: list[str] = Field(default_factory=list)
    style_route_constraints: list[str] = Field(default_factory=list)
    asset_intelligence_requirements: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("VisualSchema.brand_context_version_id is required")
        provided = {item.element_id.value for item in self.visual_familiarity_elements}
        missing = REQUIRED_FAMILIARITY_ELEMENTS - provided
        if missing:
            raise ValueError(f"VisualSchema missing familiarity elements: {sorted(missing)}")
        if not self.source_authority_map:
            raise ValueError("VisualSchema.source_authority_map is required")


class AssetRequirement(BaseModel):
    asset_requirement_id: str = Field(default_factory=lambda: new_id("asset_req"))
    ingredient_kind: str
    semantic_need: str
    required: bool = True
    acceptable_use_modes: list[str] = Field(default_factory=lambda: ["direct_use", "reference_only"])
    required_asset_roles: list[str] = Field(default_factory=list)
    style_route_constraints: list[str] = Field(default_factory=list)
    frame_profile_constraints: list[str] = Field(default_factory=list)
    source_authority_required: SourceAuthorityLevel = SourceAuthorityLevel.RESEARCH_SUPPORTED


class StoryboardIngredientSet(BaseModel):
    storyboard_ingredient_set_id: str = Field(default_factory=lambda: new_id("storyboard_ingredients"))
    visual_schema_id: str
    brand_id: str
    brand_context_version_id: str
    target_component: TargetComponent
    beat_refs: list[str] = Field(default_factory=list)
    required_visual_ingredients: list[str] = Field(default_factory=list)
    optional_visual_ingredients: list[str] = Field(default_factory=list)
    character_anchor: str | None = None
    environment_anchor: str | None = None
    object_anchors: list[str] = Field(default_factory=list)
    proof_objects: list[str] = Field(default_factory=list)
    memory_objects: list[str] = Field(default_factory=list)
    micro_semiotic_anchors: list[str] = Field(default_factory=list)
    style_references: list[str] = Field(default_factory=list)
    composition_references: list[str] = Field(default_factory=list)
    lighting_requirements: list[str] = Field(default_factory=list)
    shot_requirements: list[ShotType] = Field(default_factory=list)
    motion_requirements: list[KineticVerb] = Field(default_factory=list)
    source_authority_requirements: dict[str, SourceAuthorityLevel] = Field(default_factory=dict)
    asset_requirements: list[AssetRequirement] = Field(default_factory=list)
    missing_ingredient_gaps: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("StoryboardIngredientSet.brand_context_version_id is required")


class VisualBeatPlan(BaseModel):
    visual_beat_plan_id: str = Field(default_factory=lambda: new_id("visual_beat"))
    visual_schema_id: str
    source_beat_ref: str | None = None
    beat_index: int = 0
    beat_role: str = "single_visual"
    viewer_state_target: str | None = None
    primitive_obligation: str | None = None
    visual_question: str | None = None
    visual_payoff: str | None = None
    shot_type: ShotType
    t_code: TCode
    v_code: VCode
    kinetic_verb: KineticVerb
    camera_moral_stance: CameraMoralStance
    environment_directive: str
    subject_directive: str | None = None
    object_directive: str | None = None
    lighting_preset: LightingPreset
    asset_requirements: list[AssetRequirement] = Field(default_factory=list)
    style_route_constraints: list[str] = Field(default_factory=list)
    forbidden_visuals: list[str] = Field(default_factory=list)


class PRIMALAnalysis(BaseModel):
    primal_analysis_id: str = Field(default_factory=lambda: new_id("primal"))
    visual_beat_plan_id: str
    feeling: str
    body_truth: str
    environment: str
    timestamp_or_temporal_context: str
    uniqueness: str
    extension_fields: dict[str, Any] = Field(default_factory=dict)
    source_evidence_refs: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    pass_status: PassStatus = PassStatus.PASS

    def __init__(self, **data: Any):
        super().__init__(**data)
        for field_name in ["feeling", "body_truth", "environment"]:
            if not getattr(self, field_name):
                raise ValueError(f"PRIMALAnalysis.{field_name} is required")


class VAEDecoderReport(BaseModel):
    vae_decoder_report_id: str = Field(default_factory=lambda: new_id("vae"))
    visual_beat_plan_id: str
    semantic_check: str
    shadow_filter: str
    anti_cliche_gate: str
    forbidden_interpretations: list[str] = Field(default_factory=list)
    generic_visual_risks: list[str] = Field(default_factory=list)
    primitive_drift_risks: list[str] = Field(default_factory=list)
    source_drift_risks: list[str] = Field(default_factory=list)
    recommended_repairs: list[str] = Field(default_factory=list)
    pass_status: PassStatus = PassStatus.PASS

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.generic_visual_risks and self.pass_status == PassStatus.PASS:
            raise ValueError("generic_visual_risks require pass_status to be pass_with_risks or fail")


class ConstraintViolation(BaseModel):
    violation_id: str = Field(default_factory=lambda: new_id("constraint_violation"))
    check_id: str
    severity: str = "blocking"
    message: str
    repair_action: str | None = None


class ConstraintGateCReport(BaseModel):
    constraint_gate_c_report_id: str = Field(default_factory=lambda: new_id("gate_c"))
    target_ref: str
    checks: dict[str, bool] = Field(default_factory=dict)
    violations: list[ConstraintViolation] = Field(default_factory=list)
    accepted_risks: list[str] = Field(default_factory=list)
    repair_actions: list[str] = Field(default_factory=list)
    pass_status: PassStatus = PassStatus.PASS

    @property
    def blocking_violations(self) -> list[ConstraintViolation]:
        return [v for v in self.violations if v.severity == "blocking"]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blocking_violations and self.pass_status != PassStatus.FAIL:
            raise ValueError("blocking violations require pass_status='fail'")


class VisualAnalystReport(BaseModel):
    visual_analyst_report_id: str = Field(default_factory=lambda: new_id("visual_analyst"))
    visual_preproduction_packet_id: str | None = None
    target_component: TargetComponent
    checked_directives: list[str] = Field(default_factory=list)
    passed_checks: list[str] = Field(default_factory=list)
    failed_checks: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    repair_required: bool = False
    pass_status: PassStatus = PassStatus.PASS
    analyst_notes: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.failed_checks and self.pass_status == PassStatus.PASS:
            raise ValueError("failed_checks require pass_status to be pass_with_risks or fail")


class StoryboardCommanderVerdict(BaseModel):
    storyboard_commander_verdict_id: str = Field(default_factory=lambda: new_id("commander"))
    visual_preproduction_packet_id: str | None = None
    batch_ref: str | None = None
    project_code_lock_status: str = "not_applicable"
    visual_anchor_block_status: str = "not_checked"
    camera_moral_stance_status: str = "not_checked"
    atomic_task_list_status: str = "not_checked"
    montage_logic_status: str = "not_checked"
    tone_palette_avatar_status: str = "not_checked"
    authorization_status: AuthorizationStatus = AuthorizationStatus.REPAIR_REQUIRED
    required_repairs: list[str] = Field(default_factory=list)
    approved_for_downstream: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.approved_for_downstream and self.authorization_status not in {
            AuthorizationStatus.AUTHORIZED,
            AuthorizationStatus.AUTHORIZED_WITH_RISKS,
        }:
            raise ValueError("approved_for_downstream requires authorized status")


class VisualPreproductionPacket(BaseModel):
    visual_preproduction_packet_id: str = Field(default_factory=lambda: new_id("vp_packet"))
    brand_id: str
    brand_context_version_id: str
    target_component: TargetComponent
    preproduction_depth: PreproductionDepth
    source_context_refs: list[SourceRef] = Field(default_factory=list)
    primitive_coalition_contract_id: str | None = None
    visual_schema_id: str
    storyboard_ingredient_set_id: str | None = None
    visual_beat_plan_ids: list[str] = Field(default_factory=list)
    primal_analysis_ids: list[str] = Field(default_factory=list)
    vae_report_ids: list[str] = Field(default_factory=list)
    constraint_gate_c_report_id: str | None = None
    visual_analyst_report_id: str | None = None
    storyboard_commander_verdict_id: str | None = None
    asset_requirement_refs: list[str] = Field(default_factory=list)
    style_route_constraints: list[str] = Field(default_factory=list)
    frame_profile_constraints: list[str] = Field(default_factory=list)
    provider_preconditions: list[str] = Field(default_factory=list)
    approved_downstream_actions: list[str] = Field(default_factory=list)
    packet_status: PacketStatus = PacketStatus.DRAFT
    created_at: str = Field(default_factory=_now_iso)
    frozen_at: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("VisualPreproductionPacket.brand_context_version_id is required")
        if self.packet_status == PacketStatus.FROZEN and not self.frozen_at:
            raise ValueError("frozen_at is required when packet_status is frozen")
        if self.preproduction_depth == PreproductionDepth.FULL_BATCH and not self.storyboard_commander_verdict_id and self.packet_status == PacketStatus.FROZEN:
            raise ValueError("full_batch packet freeze requires StoryboardCommanderVerdict")
