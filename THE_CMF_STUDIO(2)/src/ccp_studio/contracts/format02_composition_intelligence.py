from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.composition_intelligence import (
    AudienceProxyPersona,
    CognitiveLoadBudget,
    CompositionRole,
    CompositionSceneProgram,
    PassStatus,
)


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


class Format02SceneRole(str, Enum):
    MYTH_SETUP = "myth_setup"
    TRUTH_DEFINE = "truth_define"
    PROOF_CONTRAST = "proof_contrast"
    BETTER_FRAME = "better_frame"
    DOSE_CONTRAST = "dose_contrast"
    PROCESS_STEP = "process_step"
    REFRAME = "reframe"
    TAKEAWAY = "takeaway"


class Format02VisualActionType(str, Enum):
    PAPER_STRIP_DROP = "paper_strip_drop"
    CARD_SLIDE_IN = "card_slide_in"
    PROOF_CARD_STAMP = "proof_card_stamp"
    COMPASS_NEEDLE_ROTATE = "compass_needle_rotate"
    RAIN_SUN_CONTRAST = "rain_sun_contrast"
    CHECKLIST_STAMP = "checklist_stamp"
    SEEDLING_GROW = "seedling_grow"
    SOFT_PUSH_IN = "soft_push_in"
    AVATAR_POINT = "avatar_point"
    AVATAR_OPEN_PALM = "avatar_open_palm"
    AVATAR_THINKING = "avatar_thinking"
    AVATAR_SOFT_SHRUG = "avatar_soft_shrug"


class Format02ConceptUnit(BaseModel):
    concept_unit_id: str = Field(default_factory=lambda: new_id("format02_concept"))
    concept_statement: str
    source_span_refs: list[str]
    one_concept_only: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.concept_statement:
            raise ValueError("Format02ConceptUnit requires concept_statement")
        if not self.source_span_refs:
            raise ValueError("Format02ConceptUnit requires source_span_refs")
        if not self.one_concept_only:
            raise ValueError("Format 02 requires one concept per scene")


class Format02VisualAction(BaseModel):
    visual_action_id: str = Field(default_factory=lambda: new_id("format02_visual_action"))
    action_type: Format02VisualActionType
    concept_unit_id: str
    sfl_function: str
    primitive_function: str
    is_primary_action: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.sfl_function:
            raise ValueError("Format02VisualAction requires SFL function")
        if not self.primitive_function:
            raise ValueError("Format02VisualAction requires primitive function")


class Format02ConceptMotionBudget(BaseModel):
    concept_motion_budget_id: str = Field(default_factory=lambda: new_id("format02_motion_budget"))
    concept_unit_id: str
    primary_visual_actions: list[str]
    max_primary_actions: int = 1
    max_simultaneous_motion_events: int = 2

    def __init__(self, **data: Any):
        super().__init__(**data)
        if len(self.primary_visual_actions) > self.max_primary_actions:
            raise ValueError("Format 02 requires one primary visual action per concept")


class Format02AvatarActionRequirement(BaseModel):
    avatar_action_requirement_id: str = Field(default_factory=lambda: new_id("format02_avatar_req"))
    required: bool = True
    action_ref: str
    pose_hint: str
    expression_hint: str
    action_serves_concept: bool = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.required and not self.action_ref:
            raise ValueError("Avatar action requirement needs action_ref")
        if not self.action_serves_concept:
            raise ValueError("Avatar action must serve concept")


class Format02AudienceProxyRequirement(BaseModel):
    audience_proxy_requirement_id: str = Field(default_factory=lambda: new_id("format02_proxy_req"))
    persona: AudienceProxyPersona
    sfl_function: str
    primitive_function: str
    scene_role: Format02SceneRole


class Format02RealLifeCutoutRequirement(BaseModel):
    real_life_cutout_requirement_id: str = Field(default_factory=lambda: new_id("format02_cutout_req"))
    required: bool = True
    object_type: str
    composition_role: CompositionRole
    source_ref_required: bool = True
    hero_object: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.required and not self.object_type:
            raise ValueError("Real-life cutout requirement needs object_type")
        if self.composition_role == CompositionRole.BACKGROUND:
            raise ValueError("Real-life cutout must have meaningful role")


class Format02PaperCardLayout(BaseModel):
    paper_card_layout_id: str = Field(default_factory=lambda: new_id("format02_card_layout"))
    headline_card_position: str
    avatar_position: str
    object_position: str | None = None
    proxy_position: str | None = None
    negative_space_ratio: float = Field(default=0.30, ge=0.0, le=1.0)


class Format02CognitiveLoadReceipt(BaseModel):
    format02_cognitive_load_receipt_id: str = Field(default_factory=lambda: new_id("format02_cognitive_receipt"))
    scene_id: str
    pass_status: PassStatus
    visible_word_count: int
    blocker_codes: list[str] = Field(default_factory=list)


class Format02SceneProgram(BaseModel):
    format02_scene_program_id: str = Field(default_factory=lambda: new_id("format02_scene"))
    scene_id: str
    scene_role: Format02SceneRole
    concept_unit: Format02ConceptUnit
    visual_action: Format02VisualAction
    motion_budget: Format02ConceptMotionBudget
    avatar_requirement: Format02AvatarActionRequirement | None = None
    audience_proxy_requirement: Format02AudienceProxyRequirement | None = None
    real_life_cutout_requirements: list[Format02RealLifeCutoutRequirement] = Field(default_factory=list)
    paper_card_layout: Format02PaperCardLayout
    composition_scene_program: CompositionSceneProgram | None = None
    cognitive_load_budget: CognitiveLoadBudget = Field(default_factory=CognitiveLoadBudget)

    def __init__(self, **data: Any):
        super().__init__(**data)
        hero_count = sum(1 for req in self.real_life_cutout_requirements if req.hero_object)
        if hero_count > self.cognitive_load_budget.max_hero_real_life_objects:
            raise ValueError("Format 02 allows only one hero real-life object per scene by default")
