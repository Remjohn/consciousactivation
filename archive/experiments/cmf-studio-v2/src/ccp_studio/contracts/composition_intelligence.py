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


class CompositionStatus(str, Enum):
    DRAFT = "draft"
    LOCKED = "locked"
    BLOCKED = "blocked"


class FrameFormatProfile(str, Enum):
    NINE_SIXTEEN_VERTICAL = "9:16_FULL_VERTICAL"
    NINE_SIXTEEN_PAPERCUT_EXPLAINER = "9:16_PAPERCUT_EXPLAINER"
    ONE_ONE_SOFT_ROUNDED = "1:1_SOFT_ROUNDED_EDITORIAL"
    FOUR_FIVE_CAROUSEL = "4:5_CAROUSEL_SLIDE"


class CompositionRole(str, Enum):
    HERO_OBJECT = "hero_object"
    SUPPORT_OBJECT = "support_object"
    PROOF_OBJECT = "proof_object"
    MEMORY_OBJECT = "memory_object"
    DIAGRAM_OBJECT = "diagram_object"
    AVATAR = "avatar"
    AUDIENCE_PROXY = "audience_proxy"
    TEXT_ANCHOR = "text_anchor"
    BACKGROUND = "background"
    MOTION_ACCENT = "motion_accent"


class AudienceProxyPersona(str, Enum):
    CONFUSED_SEEKER = "confused_seeker"
    OVERWHELMED_DOER = "overwhelmed_doer"
    SKEPTICAL_PROTECTOR = "skeptical_protector"
    GENTLE_BUILDER = "gentle_builder"


class ProviderRole(str, Enum):
    COMPOSITION_PLATE_GENERATOR = "composition_plate_generator"
    REFERENCE_BASED_OBJECT_EDITOR = "reference_based_object_editor"


class ProviderName(str, Enum):
    IDEOGRAM = "ideogram"
    FLUX = "flux"
    NONE = "none"


class CompositionIntelligenceContext(BaseModel):
    composition_context_id: str = Field(default_factory=lambda: new_id("composition_context"))
    brand_id: str
    brand_context_version_id: str
    format_program_id: str | None = None
    format_id: str
    sub_format_id: str | None = None
    frame_profile: FrameFormatProfile = FrameFormatProfile.NINE_SIXTEEN_PAPERCUT_EXPLAINER
    source_span_refs: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_id:
            raise ValueError("brand_id is required")
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")
        if not self.source_span_refs:
            raise ValueError("Composition context requires source_span_refs")


class CompositionTemplate(BaseModel):
    composition_template_id: str = Field(default_factory=lambda: new_id("composition_template"))
    template_name: str
    format_id: str
    frame_profile: FrameFormatProfile
    required_roles: list[CompositionRole]
    minimum_negative_space_ratio: float = Field(default=0.30, ge=0.0, le=1.0)


class SceneTemplate(BaseModel):
    scene_template_id: str = Field(default_factory=lambda: new_id("scene_template"))
    scene_role: str
    template_name: str
    allowed_composition_templates: list[str]
    default_attention_path: list[str]


class CognitiveLoadBudget(BaseModel):
    cognitive_load_budget_id: str = Field(default_factory=lambda: new_id("cognitive_budget"))
    max_visible_words: int = Field(default=14, ge=0)
    max_headline_words: int = Field(default=7, ge=0)
    max_support_labels: int = Field(default=4, ge=0)
    max_audience_proxies: int = Field(default=1, ge=0)
    max_hero_real_life_objects: int = Field(default=1, ge=0)
    max_support_real_life_objects: int = Field(default=2, ge=0)
    max_diagram_nodes: int = Field(default=4, ge=0)
    max_simultaneous_motion_events: int = Field(default=2, ge=0)
    minimum_negative_space_ratio: float = Field(default=0.30, ge=0.0, le=1.0)


class CognitiveLoadReport(BaseModel):
    cognitive_load_report_id: str = Field(default_factory=lambda: new_id("cognitive_report"))
    budget_id: str
    visible_words: int
    headline_words: int
    support_labels: int
    audience_proxies: int
    hero_real_life_objects: int
    support_real_life_objects: int
    diagram_nodes: int
    simultaneous_motion_events: int
    negative_space_ratio: float
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)


class AttentionPathStep(BaseModel):
    order: int
    target_role: CompositionRole
    target_ref: str
    reason: str


class AttentionPathPlan(BaseModel):
    attention_path_plan_id: str = Field(default_factory=lambda: new_id("attention_path"))
    steps: list[AttentionPathStep]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.steps:
            raise ValueError("AttentionPathPlan requires at least one step")
        orders = [step.order for step in self.steps]
        if orders != list(range(1, len(orders) + 1)):
            raise ValueError("AttentionPathPlan steps must be continuous starting at 1")


class SafeZonePlan(BaseModel):
    safe_zone_plan_id: str = Field(default_factory=lambda: new_id("safe_zone"))
    frame_profile: FrameFormatProfile
    top_margin_pct: float = 0.08
    bottom_margin_pct: float = 0.10
    side_margin_pct: float = 0.07
    face_safe_zone: dict[str, float] = Field(default_factory=dict)
    text_safe_zone: dict[str, float] = Field(default_factory=dict)


class TextPlacementPlan(BaseModel):
    text_placement_plan_id: str = Field(default_factory=lambda: new_id("text_placement"))
    headline_text: str
    support_labels: list[str] = Field(default_factory=list)
    placement: str = "upper_card"
    max_visible_words: int = 14
    avoid_face: bool = True
    avoid_proof_object: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        visible_words = len(self.headline_text.split()) + sum(len(label.split()) for label in self.support_labels)
        if visible_words > self.max_visible_words:
            raise ValueError(f"TextPlacementPlan exceeds visible word budget: {visible_words} > {self.max_visible_words}")


class TextRevealPolicy(BaseModel):
    text_reveal_policy_id: str = Field(default_factory=lambda: new_id("text_reveal"))
    reveal_style: str = "card_slide_then_rest"
    reveal_order: list[str]
    dim_previous_labels: bool = True
    paragraphs_forbidden: bool = True


class AvatarPlacementPlan(BaseModel):
    avatar_placement_plan_id: str = Field(default_factory=lambda: new_id("avatar_place"))
    avatar_ref: str
    placement: str
    action_ref: str
    action_serves_concept: bool
    max_actions: int = 1

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.action_serves_concept:
            raise ValueError("Avatar action must serve the concept")
        if self.max_actions != 1:
            raise ValueError("Format 02 default requires one avatar action per scene")


class AudienceProxyPlacementPlan(BaseModel):
    audience_proxy_placement_plan_id: str = Field(default_factory=lambda: new_id("proxy_place"))
    persona: AudienceProxyPersona
    placement: str
    sfl_function: str
    primitive_function: str | None = None
    mocking_risk: str = "low"

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.sfl_function:
            raise ValueError("Audience proxy requires SFL function")
        if self.mocking_risk == "high":
            raise ValueError("Audience proxy mocking risk cannot be high")


class RealLifeCutoutPlacementPlan(BaseModel):
    real_life_cutout_placement_plan_id: str = Field(default_factory=lambda: new_id("cutout_place"))
    asset_id: str
    source_ref: str
    role: CompositionRole
    placement: str
    reference_mode: str = "real_life_cutout"
    allowed_motion: list[str] = Field(default_factory=lambda: ["slide_in", "settle", "subtle_parallax"])
    forbidden_motion: list[str] = Field(default_factory=lambda: ["morph", "warp", "deform", "ai_liquid_motion"])

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.asset_id or not self.source_ref:
            raise ValueError("Real-life cutout requires asset_id and source_ref")
        if self.role == CompositionRole.BACKGROUND:
            raise ValueError("Real-life cutout requires a meaningful composition role")


class ObjectCompositionRoleSpec(BaseModel):
    object_composition_role_spec_id: str = Field(default_factory=lambda: new_id("object_role"))
    role: CompositionRole
    primitive_function: str
    sfl_function: str
    source_fidelity_boundary: str


class LayerSpec(BaseModel):
    layer_id: str = Field(default_factory=lambda: new_id("layer"))
    layer_role: CompositionRole
    z_index: int
    ref_id: str
    locked: bool = True


class LayerPlan(BaseModel):
    layer_plan_id: str = Field(default_factory=lambda: new_id("layer_plan"))
    layers: list[LayerSpec]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.layers:
            raise ValueError("LayerPlan requires layers")
        z_values = [layer.z_index for layer in self.layers]
        if len(z_values) != len(set(z_values)):
            raise ValueError("LayerPlan z_index values must be unique")


class LayerManifest(BaseModel):
    layer_manifest_id: str = Field(default_factory=lambda: new_id("layer_manifest"))
    layer_plan_id: str
    locked_layer_ids: list[str]
    editable_layer_ids: list[str] = Field(default_factory=list)


class LockedCompositionElements(BaseModel):
    locked_composition_elements_id: str = Field(default_factory=lambda: new_id("locked_elements"))
    locked_text: list[str] = Field(default_factory=list)
    locked_layout_refs: list[str] = Field(default_factory=list)
    locked_avatar_refs: list[str] = Field(default_factory=list)
    locked_source_refs: list[str] = Field(default_factory=list)
    locked_negative_space: bool = True


class ProviderEditBoundary(BaseModel):
    provider_edit_boundary_id: str = Field(default_factory=lambda: new_id("provider_boundary"))
    provider_name: ProviderName
    provider_role: ProviderRole
    allowed_edits: list[str]
    forbidden_edits: list[str]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if "rewrite_text" in self.allowed_edits:
            raise ValueError("Providers cannot be allowed to rewrite locked text")
        if "change_layout" in self.allowed_edits:
            raise ValueError("Providers cannot be allowed to change locked layout")


class ProviderCompositionPlateContract(BaseModel):
    provider_composition_plate_contract_id: str = Field(default_factory=lambda: new_id("composition_plate"))
    provider_name: ProviderName = ProviderName.IDEOGRAM
    provider_role: ProviderRole = ProviderRole.COMPOSITION_PLATE_GENERATOR
    composition_scene_program_id: str
    locked_elements: LockedCompositionElements
    edit_boundary: ProviderEditBoundary
    placeholder_object_slots: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.provider_role != ProviderRole.COMPOSITION_PLATE_GENERATOR:
            raise ValueError("ProviderCompositionPlateContract requires composition_plate_generator role")
        if self.provider_name != ProviderName.IDEOGRAM:
            raise ValueError("Ideogram is the expected composition plate provider in V1")


class ReferenceEditContract(BaseModel):
    reference_edit_contract_id: str = Field(default_factory=lambda: new_id("reference_edit"))
    provider_name: ProviderName = ProviderName.FLUX
    provider_role: ProviderRole = ProviderRole.REFERENCE_BASED_OBJECT_EDITOR
    composition_plate_ref: str
    reference_inputs: list[RealLifeCutoutPlacementPlan]
    locked_elements: LockedCompositionElements
    edit_boundary: ProviderEditBoundary

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.provider_role != ProviderRole.REFERENCE_BASED_OBJECT_EDITOR:
            raise ValueError("ReferenceEditContract requires reference_based_object_editor role")
        if self.provider_name != ProviderName.FLUX:
            raise ValueError("Flux is the expected reference edit provider in V1")
        if not self.reference_inputs:
            raise ValueError("ReferenceEditContract requires reference inputs")
        forbidden = set(self.edit_boundary.forbidden_edits)
        required_forbidden = {"rewrite_text", "move_avatar", "change_layout", "invent_claims", "add_extra_objects"}
        if not required_forbidden.issubset(forbidden):
            raise ValueError("ReferenceEditContract must forbid text/layout/avatar/claim/object drift")


class CompositionSceneProgram(BaseModel):
    composition_scene_program_id: str = Field(default_factory=lambda: new_id("composition_scene"))
    context_id: str
    scene_id: str
    scene_role: str
    concept_statement: str
    composition_template_id: str
    cognitive_load_budget: CognitiveLoadBudget
    attention_path_plan: AttentionPathPlan
    safe_zone_plan: SafeZonePlan
    text_placement_plan: TextPlacementPlan
    text_reveal_policy: TextRevealPolicy
    avatar_placement_plan: AvatarPlacementPlan | None = None
    audience_proxy_placement_plan: AudienceProxyPlacementPlan | None = None
    real_life_cutout_plans: list[RealLifeCutoutPlacementPlan] = Field(default_factory=list)
    layer_plan: LayerPlan
    layer_manifest: LayerManifest
    status: CompositionStatus = CompositionStatus.DRAFT

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.concept_statement:
            raise ValueError("CompositionSceneProgram requires concept_statement")


class CompositionDecisionReceipt(BaseModel):
    composition_decision_receipt_id: str = Field(default_factory=lambda: new_id("composition_receipt"))
    composition_scene_program_id: str
    pass_status: PassStatus
    cognitive_load_report_id: str
    locked: bool = False
    blockers: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blockers and self.pass_status == PassStatus.PASS:
            raise ValueError("Composition decision with blockers cannot pass")
        if self.locked and self.pass_status != PassStatus.PASS:
            raise ValueError("Only passing compositions can be locked")


class CompositionCommanderVerdict(BaseModel):
    composition_commander_verdict_id: str = Field(default_factory=lambda: new_id("composition_verdict"))
    authorized: bool
    pass_status: PassStatus
    blockers: list[str] = Field(default_factory=list)
    repair_recommendations: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blockers and self.authorized:
            raise ValueError("Composition cannot be authorized with blockers")
