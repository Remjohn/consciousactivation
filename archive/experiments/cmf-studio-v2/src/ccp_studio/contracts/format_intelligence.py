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


class FormatId(str, Enum):
    FORMAT_01_CINEMATIC_STORY = "format_01_cinematic_story"
    FORMAT_02_AVATAR_PAPERCUT_EXPLAINER = "format_02_avatar_papercut_explainer"
    FORMAT_03_LIVING_COMMENTARY_REACTIONS = "format_03_living_commentary_reactions"
    FORMAT_04_CONSCIOUS_REACTIONS_EDITING = "format_04_conscious_reactions_editing"
    SUPERVISUAL = "supervisual"
    CAROUSEL = "carousel"
    MEME_VISUAL = "meme_visual"
    POLL_VISUAL = "poll_visual"
    REACTION_SEED = "reaction_seed"


class EngineTarget(str, Enum):
    SUPERVISUAL_ENGINE = "supervisual_engine"
    CAROUSEL_ENGINE = "carousel_engine"
    VIDEO_EDITING_ENGINE = "video_editing_engine"
    TWO_D_CHARACTER_ANIMATION_ENGINE = "2d_character_animation_engine"
    MEME_VISUAL_ENGINE = "meme_visual_engine"
    POLL_VISUAL_ENGINE = "poll_visual_engine"
    REACTION_ENGINE = "reaction_engine"


class FormatProgramStatus(str, Enum):
    DRAFT = "draft"
    COMPILED = "compiled"
    BLOCKED = "blocked"
    AUTHORIZED = "authorized"
    ADAPTED = "adapted"


class IngredientStatus(str, Enum):
    PRESENT = "present"
    PARTIAL = "partial"
    MISSING = "missing"


class FormatIngredientType(str, Enum):
    AROLL_STORY_SPINE = "a_roll_story_spine"
    EMOTIONAL_CHANGE_MAP = "emotional_change_map"
    CUT_QUESTION_CHAIN = "cut_question_chain"
    MEMORY_OBJECT = "memory_object"
    PROOF_OBJECT = "proof_object"
    BROLL_FORESHADOWING_PAIR = "broll_foreshadowing_pair"
    POWER_PHRASE_PLAN = "power_phrase_plan"
    SONIC_STORY_ARC_SEED = "sonic_story_arc_seed"
    TEACHABLE_MECHANISM = "teachable_mechanism"
    CONCEPT_NODES = "concept_nodes"
    DIAGRAM_SEQUENCE = "diagram_sequence"
    AVATAR_PERFORMANCE_REQUIREMENTS = "avatar_performance_requirements"
    PROOF_OR_QUOTE_SURFACE = "proof_or_quote_surface"
    COACH_REACTION_ANGLE = "coach_reaction_angle"
    ROUGH_NOTATION_TARGETS = "rough_notation_targets"
    DEBATE_TENSION = "debate_tension"
    REACTION_UI_SURFACE = "reaction_ui_surface"
    SCORE_STATE_SEED = "score_state_seed"
    MEME_MECHANISM = "meme_mechanism"
    SINGLE_SOURCE_TRUTH = "single_source_truth"
    VISUAL_HOOK = "visual_hook"
    EDGE_PRODUCT = "edge_product"
    CAROUSEL_THESIS = "carousel_thesis"
    VIEWER_STATE_SEQUENCE = "viewer_state_sequence"
    CLOSURE_CONTRACT = "closure_contract"
    POLL_OPTIONS = "poll_options"
    REACTION_QUESTION = "reaction_question"


class StyleRoute(str, Enum):
    CAC = "CAC"
    CAC_ANALYST = "CAC_ANALYST"
    CAC_COMPOSER = "CAC_COMPOSER"
    DOCUMENTARY_PROOF = "Documentary Proof"
    PAPER_CUT_EDITORIAL = "Paper-Cut Editorial"
    PAPER_CUT_ARTIFACT = "Paper-Cut Artifact"
    UI_REACTION_SURFACE = "UI Reaction Surface"
    AVATAR_PERFORMANCE_LAYER = "Avatar Performance Layer"
    GMG_COMPOSER = "GMG Composer"
    GMG_ANALYST = "GMG Analyst"
    GMG_EXPERT_01 = "GMG Expert 01"
    GMG_EXPERT_02 = "GMG Expert 02"
    GMG_EXPERT_03 = "GMG Expert 03"
    GMG_EXPERT_04 = "GMG Expert 04"
    GMG_EXPERT_05 = "GMG Expert 05"
    GMG_EXPERT_06 = "GMG Expert 06"
    MOTION_CANVAS = "Motion Canvas"
    MANIM = "Manim"
    ROUGH_NOTATION = "Rough Notation"


class FrameProfile(str, Enum):
    NINE_SIXTEEN_VERTICAL = "9:16_FULL_VERTICAL"
    NINE_SIXTEEN_PAPERCUT = "9:16_PAPERCUT_EXPLAINER"
    NINE_SIXTEEN_SPLIT_REACTION = "9:16_SPLIT_REACTION"
    NINE_SIXTEEN_CONSCIOUS_REACTION = "9:16_CONSCIOUS_REACTION"
    ONE_ONE_SOFT_ROUNDED = "1:1_SOFT_ROUNDED_EDITORIAL"
    ONE_ONE_PROOF_CARD = "1:1_PROOF_CARD"
    FOUR_FIVE_CAROUSEL = "4:5_CAROUSEL_SLIDE"
    FOUR_FIVE_FEED_VIDEO = "4:5_FEED_VIDEO"


def _reject_16_9(frame_profile: str) -> None:
    if frame_profile and frame_profile.startswith("16:9"):
        raise ValueError("16:9 is source-only and cannot be a delivery frame profile")


class FormatIntelligenceContext(BaseModel):
    format_intelligence_context_id: str = Field(default_factory=lambda: new_id("format_context"))
    brand_id: str
    brand_context_version_id: str
    source_extraction_run_id: str | None = None
    archetype_program_id: str | None = None
    primitive_coalition_candidate_id: str | None = None
    delivery_recipe_program_id: str | None = None
    target_formats: list[FormatId] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_id:
            raise ValueError("brand_id is required")
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")


class GenericExtractionPacketRef(BaseModel):
    extraction_packet_id: str
    target_format: FormatId
    sub_format_hint: str | None = None
    source_span_refs: list[str]
    payload: dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.extraction_packet_id:
            raise ValueError("extraction_packet_id is required")
        if not self.source_span_refs:
            raise ValueError("GenericExtractionPacketRef requires source_span_refs")


class FormatActivationDecision(BaseModel):
    format_activation_decision_id: str = Field(default_factory=lambda: new_id("format_activation"))
    format_id: FormatId
    activated: bool
    activation_reason: str
    evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)


class FormatSubFormatRoute(BaseModel):
    format_sub_format_route_id: str = Field(default_factory=lambda: new_id("sub_format_route"))
    format_id: FormatId
    sub_format_id: str
    rationale: str
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)


class FormatIngredientRequirement(BaseModel):
    requirement_id: str = Field(default_factory=lambda: new_id("ingredient_req"))
    ingredient_type: FormatIngredientType
    required: bool = True
    source_key: str | None = None
    reason: str | None = None


class FormatIngredientCheck(BaseModel):
    ingredient_type: FormatIngredientType
    status: IngredientStatus
    evidence: str | None = None
    missing_reason: str | None = None


class FormatIngredientChecklist(BaseModel):
    checklist_id: str = Field(default_factory=lambda: new_id("ingredient_checklist"))
    format_id: FormatId
    checks: list[FormatIngredientCheck]

    @property
    def missing_required(self) -> list[FormatIngredientCheck]:
        return [check for check in self.checks if check.status == IngredientStatus.MISSING]


class FormatCompositionGrammar(BaseModel):
    composition_grammar_id: str = Field(default_factory=lambda: new_id("composition_grammar"))
    format_id: FormatId
    sub_format_id: str
    grammar_name: str
    rules: list[str]
    attention_path: list[str] = Field(default_factory=list)
    negative_space_policy: str = "intentional"
    text_policy: str = "source_faithful"
    source_preservation_policy: str = "strict"


class FormatLayerRequirement(BaseModel):
    layer_role: str
    required: bool = True
    z_index: int
    description: str


class FormatLayerStackSpec(BaseModel):
    layer_stack_spec_id: str = Field(default_factory=lambda: new_id("layer_stack"))
    format_id: FormatId
    layers: list[FormatLayerRequirement]
    min_layers: int = 1

    def __init__(self, **data: Any):
        super().__init__(**data)
        if len(self.layers) < self.min_layers:
            raise ValueError("Layer stack does not meet min_layers")


class FormatMotionDoctrine(BaseModel):
    motion_doctrine_id: str = Field(default_factory=lambda: new_id("motion_doctrine"))
    format_id: FormatId
    allowed_motion: list[str]
    banned_motion: list[str]
    max_motion_events_per_15s: int = Field(default=4, ge=0)
    voice_first: bool = True


class FormatMemeticCuePolicy(BaseModel):
    memetic_cue_policy_id: str = Field(default_factory=lambda: new_id("memetic_policy"))
    format_id: FormatId
    max_cues: int = Field(default=1, ge=0)
    per_seconds: int = Field(default=30, ge=1)
    exceptions: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.format_id in {FormatId.FORMAT_01_CINEMATIC_STORY, FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER, FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS} and self.per_seconds < 30:
            raise ValueError("Formats 01-03 require memetic cue spacing of at least 30 seconds")
        if self.format_id == FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING and self.per_seconds < 10:
            raise ValueError("Format 04 requires memetic cue spacing of at least 10 seconds")


class FormatSoundDoctrine(BaseModel):
    sound_doctrine_id: str = Field(default_factory=lambda: new_id("sound_doctrine"))
    format_id: FormatId
    voice_master: bool = True
    sonic_profile: str
    allowed_cues: list[str] = Field(default_factory=list)
    memetic_policy: FormatMemeticCuePolicy


class FormatStyleRoutePolicy(BaseModel):
    style_route_policy_id: str = Field(default_factory=lambda: new_id("style_route_policy"))
    format_id: FormatId
    primary_routes: list[StyleRoute]
    secondary_routes: list[StyleRoute] = Field(default_factory=list)
    forbidden_routes: list[StyleRoute] = Field(default_factory=list)

    def validate_selected_routes(self, selected_routes: list[StyleRoute]) -> None:
        forbidden = set(selected_routes).intersection(set(self.forbidden_routes))
        if forbidden:
            raise ValueError(f"Selected style routes include forbidden routes: {sorted(route.value for route in forbidden)}")


class FormatFirstFramePolicy(BaseModel):
    first_frame_policy_id: str = Field(default_factory=lambda: new_id("first_frame_policy"))
    format_id: FormatId
    required: bool = True
    iris_required: bool = True
    face_presence_policy: str = "format_specific"
    text_hook_policy: str = "source_faithful"


class FormatSubtitlePolicy(BaseModel):
    subtitle_policy_id: str = Field(default_factory=lambda: new_id("subtitle_policy"))
    format_id: FormatId
    max_lines: int = Field(default=2, ge=0)
    collision_policy: str = "avoid_face_and_proof_object"
    emotional_pause_policy: str = "do_not_flatten_pause"


class FormatBrollPolicy(BaseModel):
    broll_policy_id: str = Field(default_factory=lambda: new_id("broll_policy"))
    required: bool = False
    broll_function: str = "support"
    forbid_filler: bool = True
    real_life_reference_required: bool = True


class FormatProofPolicy(BaseModel):
    proof_policy_id: str = Field(default_factory=lambda: new_id("proof_policy"))
    proof_required: bool = False
    proof_surface_required: bool = False
    legibility_required: bool = True
    source_grounding_required: bool = True


class FormatMemoryObjectPolicy(BaseModel):
    memory_object_policy_id: str = Field(default_factory=lambda: new_id("memory_policy"))
    memory_object_required: bool = False
    source_grounding_required: bool = True
    allow_derivative_if_private: bool = True


class FormatAvatarPerformancePolicy(BaseModel):
    avatar_performance_policy_id: str = Field(default_factory=lambda: new_id("avatar_policy"))
    avatar_required: bool = False
    allowed_clip_types: list[str] = Field(default_factory=list)
    lip_sync_policy: str = "optional"
    decorative_avatar_forbidden: bool = True


class FormatReactionSurfacePolicy(BaseModel):
    reaction_surface_policy_id: str = Field(default_factory=lambda: new_id("reaction_surface_policy"))
    reaction_surface_required: bool = False
    upper_surface_role: str | None = None
    lower_surface_role: str | None = None
    timing_policy: str = "reaction_after_stimulus"


class FormatAntiSlopRule(BaseModel):
    rule_id: str = Field(default_factory=lambda: new_id("anti_slop"))
    code: str
    description: str
    blocking: bool = True


class FormatEvalGateSet(BaseModel):
    eval_gate_set_id: str = Field(default_factory=lambda: new_id("eval_gate_set"))
    format_id: FormatId
    gates: list[str]
    anti_slop_rules: list[FormatAntiSlopRule]


class FormatRenderRequirement(BaseModel):
    render_requirement_id: str = Field(default_factory=lambda: new_id("render_req"))
    format_id: FormatId
    frame_profile: FrameProfile
    engine_target: EngineTarget
    deterministic_render_required: bool = True
    provider_calls_allowed_during_final_render: bool = False
    output_requirements: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        _reject_16_9(self.frame_profile.value)
        if self.provider_calls_allowed_during_final_render:
            raise ValueError("Provider calls are not allowed during final render")


class FormatRepairCommand(BaseModel):
    repair_command_id: str = Field(default_factory=lambda: new_id("format_repair"))
    command_type: str
    reason: str
    payload: dict[str, Any] = Field(default_factory=dict)


class FormatCommanderVerdict(BaseModel):
    commander_verdict_id: str = Field(default_factory=lambda: new_id("format_verdict"))
    authorized: bool
    pass_status: PassStatus
    blockers: list[str] = Field(default_factory=list)
    repair_commands: list[FormatRepairCommand] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blockers and self.authorized:
            raise ValueError("Cannot authorize format program with blockers")


class FormatIntelligenceProgram(BaseModel):
    format_intelligence_program_id: str = Field(default_factory=lambda: new_id("format_program"))
    brand_id: str
    brand_context_version_id: str
    source_extraction_packet_id: str
    source_span_refs: list[str]
    archetype_program_id: str | None = None
    primitive_coalition_candidate_id: str | None = None
    delivery_recipe_program_id: str | None = None
    format_id: FormatId
    sub_format_id: str
    activation_reason: str
    ingredient_checklist: FormatIngredientChecklist
    composition_grammar: FormatCompositionGrammar
    layer_stack_spec: FormatLayerStackSpec
    motion_doctrine: FormatMotionDoctrine | None = None
    sound_doctrine: FormatSoundDoctrine | None = None
    style_route_policy: FormatStyleRoutePolicy
    first_frame_policy: FormatFirstFramePolicy
    subtitle_policy: FormatSubtitlePolicy | None = None
    broll_policy: FormatBrollPolicy | None = None
    proof_policy: FormatProofPolicy | None = None
    memory_object_policy: FormatMemoryObjectPolicy | None = None
    avatar_performance_policy: FormatAvatarPerformancePolicy | None = None
    reaction_surface_policy: FormatReactionSurfacePolicy | None = None
    eval_gate_set: FormatEvalGateSet
    render_requirement: FormatRenderRequirement
    commander_verdict: FormatCommanderVerdict | None = None
    status: FormatProgramStatus = FormatProgramStatus.COMPILED
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")
        if not self.source_extraction_packet_id:
            raise ValueError("source_extraction_packet_id is required")
        if not self.source_span_refs:
            raise ValueError("FormatIntelligenceProgram requires source_span_refs")


class Format01CinematicStoryProgram(FormatIntelligenceProgram):
    aroll_story_spine_ref: str
    emotional_change_map_ref: str
    cut_question_chain_refs: list[str]
    broll_foreshadowing_pair_refs: list[str] = Field(default_factory=list)
    sonic_story_arc_seed_ref: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.format_id != FormatId.FORMAT_01_CINEMATIC_STORY:
            raise ValueError("Format01CinematicStoryProgram requires format_01_cinematic_story")
        if not self.aroll_story_spine_ref or not self.cut_question_chain_refs:
            raise ValueError("Format 01 requires A-roll story spine and cut-question chain")


class Format02AvatarPaperCutExplainerProgram(FormatIntelligenceProgram):
    teachable_mechanism_ref: str
    concept_node_refs: list[str]
    diagram_sequence_ref: str
    avatar_clip_requirements: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.format_id != FormatId.FORMAT_02_AVATAR_PAPERCUT_EXPLAINER:
            raise ValueError("Format02 program requires format_02_avatar_papercut_explainer")
        if not self.teachable_mechanism_ref or not self.concept_node_refs or not self.diagram_sequence_ref:
            raise ValueError("Format 02 requires mechanism, concept nodes, and diagram sequence")


class Format03LivingCommentaryReactionProgram(FormatIntelligenceProgram):
    proof_or_quote_surface_ref: str
    coach_reaction_angle_ref: str
    rough_notation_target_refs: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.format_id != FormatId.FORMAT_03_LIVING_COMMENTARY_REACTIONS:
            raise ValueError("Format03 program requires format_03_living_commentary_reactions")
        if not self.proof_or_quote_surface_ref or not self.coach_reaction_angle_ref:
            raise ValueError("Format 03 requires proof/quote surface and reaction angle")


class Format04ConsciousReactionEditingProgram(FormatIntelligenceProgram):
    debate_tension_ref: str
    reaction_ui_surface_ref: str
    score_state_seed_ref: str | None = None
    meme_mechanism_ref: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.format_id != FormatId.FORMAT_04_CONSCIOUS_REACTIONS_EDITING:
            raise ValueError("Format04 program requires format_04_conscious_reactions_editing")
        if not self.debate_tension_ref or not self.reaction_ui_surface_ref:
            raise ValueError("Format 04 requires debate tension and reaction UI surface")


class SuperVisualFormatProgram(FormatIntelligenceProgram):
    single_source_truth_ref: str
    visual_hook_ref: str
    edge_product_ref: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.format_id != FormatId.SUPERVISUAL:
            raise ValueError("SuperVisualFormatProgram requires supervisual format_id")
        if not self.single_source_truth_ref:
            raise ValueError("SuperVisual requires one single source truth")
        if not self.visual_hook_ref:
            raise ValueError("SuperVisual requires visual_hook_ref")
        if not self.edge_product_ref:
            raise ValueError("SuperVisual requires edge_product_ref")


class CarouselSequenceStep(BaseModel):
    step_index: int
    role: str
    viewer_state: str
    source_ref: str | None = None


class CarouselFormatProgram(FormatIntelligenceProgram):
    carousel_thesis_ref: str
    sequence_steps: list[CarouselSequenceStep]
    closure_contract_ref: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.format_id != FormatId.CAROUSEL:
            raise ValueError("CarouselFormatProgram requires carousel format_id")
        if not self.closure_contract_ref:
            raise ValueError("Carousel requires closure_contract")
        indexes = [step.step_index for step in self.sequence_steps]
        if indexes != list(range(1, len(indexes) + 1)):
            raise ValueError("Carousel sequence steps must be continuous")


class MemeVisualFormatProgram(FormatIntelligenceProgram):
    source_truth_ref: str
    compressed_paradox_ref: str
    meme_mechanism_ref: str
    risk_boundary: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.format_id != FormatId.MEME_VISUAL:
            raise ValueError("MemeVisualFormatProgram requires meme_visual format_id")
        if not self.meme_mechanism_ref:
            raise ValueError("Meme visual requires meme mechanism")


class PollVisualFormatProgram(FormatIntelligenceProgram):
    poll_question_ref: str
    option_refs: list[str]
    discussion_value: str = "medium"

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.format_id != FormatId.POLL_VISUAL:
            raise ValueError("PollVisualFormatProgram requires poll_visual format_id")
        if len(self.option_refs) < 2:
            raise ValueError("Poll visual requires at least two meaningful options")


class ReactionSeedFormatProgram(FormatIntelligenceProgram):
    source_quote_ref: str
    reaction_question_ref: str
    compatible_reaction_formats: list[str]
    store_only: bool = True


class EngineAdapterPayload(BaseModel):
    engine_adapter_payload_id: str = Field(default_factory=lambda: new_id("engine_payload"))
    format_program_id: str
    engine_target: EngineTarget
    payload_kind: str
    source_span_refs: list[str]
    payload: dict[str, Any]
    commander_verdict_id: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.source_span_refs:
            raise ValueError("EngineAdapterPayload requires source_span_refs")
