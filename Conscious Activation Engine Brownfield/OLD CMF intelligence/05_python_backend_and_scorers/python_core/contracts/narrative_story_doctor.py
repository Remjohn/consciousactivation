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


class ExtractionMode(str, Enum):
    RAW_TRANSCRIPT = "raw_transcript"
    INTERVIEW_BRIEF_BOUND = "interview_brief_bound"
    COMPLETE_EXPRESSION_SESSION = "complete_expression_session"


class EvidenceStatus(str, Enum):
    PRESENT = "present"
    PARTIAL = "partial"
    MISSING = "missing"


class PassStatus(str, Enum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class CoverageStatus(str, Enum):
    STRONG_HIT = "strong_hit"
    PARTIAL_HIT = "partial_hit"
    MISS = "miss"
    UNEXPECTED_WIN = "unexpected_win"
    OVERRIDE_RECOMMENDED = "override_recommended"


class ExtractionTarget(str, Enum):
    FORMAT_01_CINEMATIC_STORY = "format_01_cinematic_story"
    FORMAT_02_AVATAR_PAPERCUT_EXPLAINER = "format_02_avatar_papercut_explainer"
    FORMAT_03_LIVING_COMMENTARY_REACTIONS = "format_03_living_commentary_reactions"
    FORMAT_04_CONSCIOUS_REACTIONS_EDITING = "format_04_conscious_reactions_editing"
    SUPERVISUAL_SINGLE_IMAGE = "supervisual_single_image"
    CAROUSEL_SEQUENCE = "carousel_sequence"
    VIDEO_SCENE = "video_scene"
    MEME_VISUAL = "meme_visual"
    POLL_VISUAL = "poll_visual"
    REACTION_SEED = "reaction_seed"


class IngredientType(str, Enum):
    SOURCE_QUOTE = "source_quote"
    BEFORE_AFTER_CHANGE = "before_after_change"
    EMOTIONAL_PAUSE = "emotional_pause"
    MEMORY_OBJECT = "memory_object"
    PROOF_OBJECT = "proof_object"
    VISUAL_SPR = "visual_spr"
    BROLL_ACTION = "broll_action"
    CONTRAST_PAIR = "contrast_pair"
    TEACHABLE_MECHANISM = "teachable_mechanism"
    CONCEPT_NOUN = "concept_noun"
    DIAGRAM_SEQUENCE = "diagram_sequence"
    AVATAR_GESTURE = "avatar_gesture"
    REACTION_TRIGGER = "reaction_trigger"
    PROOF_SURFACE = "proof_surface"
    DEBATE_TENSION = "debate_tension"
    RANKABLE_OPTIONS = "rankable_options"
    MEME_MECHANISM = "meme_mechanism"
    POLL_TENSION = "poll_tension"
    POWER_PHRASE = "power_phrase"
    SONIC_PAUSE = "sonic_pause"
    MICRO_SEMIOTIC_ANCHOR = "micro_semiotic_anchor"


class ExpressionMomentType(str, Enum):
    PAUSE = "pause"
    BREATH = "breath"
    VOICE_CRACK = "voice_crack"
    LAUGH = "laugh"
    SMILE = "smile"
    HAND_GESTURE = "hand_gesture"
    OBJECT_TOUCH = "object_touch"
    GAZE_SHIFT = "gaze_shift"
    SILENCE = "silence"
    HESITATION = "hesitation"
    EMPHASIS = "emphasis"


class ViewerStateFunction(str, Enum):
    PERCEPTUAL_ENTRY = "perceptual_entry"
    RELEVANT_OPEN_QUESTION = "relevant_open_question"
    ACTIVE_PREDICTION = "active_prediction"
    TRUTHFUL_PAYOFF = "truthful_payoff"
    HUMAN_AFFINITY = "human_affinity"
    EXPECTED_FUTURE_VALUE = "expected_future_value"
    OPEN_LOOP = "open_loop"
    CLOSURE_CONTRACT = "closure_contract"


class LayerAwareExtractionContext(BaseModel):
    context_id: str = Field(default_factory=lambda: new_id("layer_context"))
    brand_id: str
    brand_context_version_id: str
    doctrine_refs: list[str] = Field(default_factory=list)
    brand_genesis_session_id: str | None = None
    voice_dna_id: str | None = None
    visual_dna_id: str | None = None
    identity_pack_id: str | None = None
    guest_dossier_id: str | None = None
    audience_reality_brief_id: str | None = None
    interview_brief_id: str | None = None
    complete_expression_session_id: str | None = None
    target_output_families: list[str] = Field(default_factory=list)
    target_formats: list[ExtractionTarget] = Field(default_factory=list)
    target_frame_profiles: list[str] = Field(default_factory=list)
    primitive_taxonomy_version: str = "v1"
    extraction_mode: ExtractionMode = ExtractionMode.RAW_TRANSCRIPT
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_id:
            raise ValueError("brand_id is required")
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")


class QuestionProductionContract(BaseModel):
    question_contract_id: str = Field(default_factory=lambda: new_id("question_contract"))
    question_id: str
    question_text: str
    target_archetypes: list[str]
    target_expression_state: str
    first_line_anchor: str | None = None
    depth_anchor: str | None = None
    expected_primitives: list[str] = Field(default_factory=list)
    expected_ingredients: list[IngredientType]
    target_asset_routes: list[ExtractionTarget] = Field(default_factory=list)
    asset_routes: list[str] = Field(default_factory=list)
    evaluation_logic: dict[str, bool] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.question_text:
            raise ValueError("question_text is required")
        if not self.target_archetypes:
            raise ValueError("target_archetypes are required")
        if not self.target_expression_state:
            raise ValueError("target_expression_state is required")
        if not self.expected_ingredients:
            raise ValueError("expected_ingredients are required")


class InterviewBriefBinding(BaseModel):
    interview_brief_binding_id: str = Field(default_factory=lambda: new_id("brief_binding"))
    interview_brief_id: str
    brand_id: str
    brand_context_version_id: str
    interview_objective: str
    target_archetypes: list[str]
    target_primitives: list[str] = Field(default_factory=list)
    target_expression_states: list[str] = Field(default_factory=list)
    target_output_families: list[str] = Field(default_factory=list)
    target_content_formats: list[ExtractionTarget] = Field(default_factory=list)
    question_contracts: list[QuestionProductionContract]
    expected_ingredient_graph_id: str | None = None
    bias_strength: float = Field(default=0.65, ge=0.0, le=1.0)
    source_fidelity_policy: str = "brief_is_prior_not_evidence"

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("brand_context_version_id is required")
        if not self.question_contracts:
            raise ValueError("question_contracts are required")


class ExpectedIngredientNode(BaseModel):
    node_id: str = Field(default_factory=lambda: new_id("expected_node"))
    question_id: str
    ingredient_type: IngredientType
    target_archetype: str | None = None
    target_format: ExtractionTarget | None = None
    required: bool = True


class ExpectedIngredientEdge(BaseModel):
    edge_id: str = Field(default_factory=lambda: new_id("expected_edge"))
    from_node_id: str
    to_node_id: str
    relation: str


class ExpectedIngredientGraph(BaseModel):
    expected_ingredient_graph_id: str = Field(default_factory=lambda: new_id("expected_graph"))
    interview_brief_id: str
    brand_context_version_id: str
    nodes: list[ExpectedIngredientNode]
    edges: list[ExpectedIngredientEdge] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.nodes:
            raise ValueError("ExpectedIngredientGraph requires nodes")


class SourceReference(BaseModel):
    source_ref_id: str = Field(default_factory=lambda: new_id("source_ref"))
    source_kind: str
    source_id: str | None = None
    start_ms: int | None = None
    end_ms: int | None = None
    description: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.start_ms is not None and self.end_ms is not None and self.end_ms <= self.start_ms:
            raise ValueError("source reference end_ms must be greater than start_ms")


class VerbatimSpan(BaseModel):
    span_id: str = Field(default_factory=lambda: new_id("span"))
    text: str
    speaker: str
    source_ref_id: str
    question_id: str | None = None
    start_ms: int | None = None
    end_ms: int | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.text.strip():
            raise ValueError("verbatim span text is required")
        if not self.speaker:
            raise ValueError("speaker is required")
        if not self.source_ref_id:
            raise ValueError("source_ref_id is required")
        if self.start_ms is not None and self.end_ms is not None and self.end_ms <= self.start_ms:
            raise ValueError("span end_ms must be greater than start_ms")


class ExtractionSourcePacket(BaseModel):
    extraction_source_packet_id: str = Field(default_factory=lambda: new_id("source_packet"))
    mode: ExtractionMode
    transcript_text: str
    source_references: list[SourceReference]
    spans: list[VerbatimSpan] = Field(default_factory=list)
    timing_confidence: str = "medium"
    speaker_confidence: str = "medium"
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.transcript_text.strip():
            raise ValueError("transcript_text is required")
        if not self.source_references:
            raise ValueError("source_references are required")


class TranscriptBeat(BaseModel):
    beat_id: str = Field(default_factory=lambda: new_id("beat"))
    speaker: str
    start_ms: int | None = None
    end_ms: int | None = None
    verbatim_text: str
    source_ref_id: str
    source_span_ids: list[str] = Field(default_factory=list)
    semantic_function: str = "unknown"
    emotional_function: str = "unknown"
    viewer_state_function: ViewerStateFunction | None = None
    expression_signal: str | None = None
    visual_signal: str | None = None
    asset_signal: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.verbatim_text.strip():
            raise ValueError("TranscriptBeat requires verbatim_text")
        if self.start_ms is not None and self.end_ms is not None and self.end_ms <= self.start_ms:
            raise ValueError("beat end_ms must be greater than start_ms")


class TranscriptBeatMap(BaseModel):
    transcript_beat_map_id: str = Field(default_factory=lambda: new_id("beat_map"))
    extraction_source_packet_id: str
    beats: list[TranscriptBeat]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.beats:
            raise ValueError("TranscriptBeatMap requires beats")


class ExpressionMomentCandidate(BaseModel):
    expression_moment_id: str = Field(default_factory=lambda: new_id("expression"))
    expression_type: ExpressionMomentType
    description: str
    source_span_id: str | None = None
    beat_id: str | None = None
    timestamp_ms: int | None = None
    confidence: float = Field(default=0.65, ge=0.0, le=1.0)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not (self.source_span_id or self.beat_id or self.timestamp_ms is not None):
            raise ValueError("ExpressionMomentCandidate requires source_span_id, beat_id, or timestamp_ms")


class ExpressionIngredientInventory(BaseModel):
    expression_inventory_id: str = Field(default_factory=lambda: new_id("expression_inventory"))
    expression_moments: list[ExpressionMomentCandidate]
    coverage_notes: list[str] = Field(default_factory=list)


class NarrativeCluster(BaseModel):
    cluster_id: str = Field(default_factory=lambda: new_id("cluster"))
    source_span_ids: list[str]
    beat_ids: list[str] = Field(default_factory=list)
    verbatim_anchor: str
    emotional_movement: str
    object_signals: list[str] = Field(default_factory=list)
    expression_signals: list[str] = Field(default_factory=list)
    visual_signals: list[str] = Field(default_factory=list)
    possible_output_targets: list[ExtractionTarget] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.source_span_ids:
            raise ValueError("NarrativeCluster requires source_span_ids")
        if not self.verbatim_anchor:
            raise ValueError("NarrativeCluster requires verbatim_anchor")


class ClusterMeaningGraph(BaseModel):
    cluster_meaning_graph_id: str = Field(default_factory=lambda: new_id("cluster_graph"))
    clusters: list[NarrativeCluster]
    edges: list[dict[str, str]] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.clusters:
            raise ValueError("ClusterMeaningGraph requires clusters")


class MeaningPlaneCandidate(BaseModel):
    meaning_plane_candidate_id: str = Field(default_factory=lambda: new_id("meaning"))
    cluster_id: str
    meaning_family: str
    statement: str
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)


class ExperiencePlaneCandidate(BaseModel):
    experience_plane_candidate_id: str = Field(default_factory=lambda: new_id("experience"))
    cluster_id: str
    experience_family: str
    felt_state: str
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)


class EdgeCandidate(BaseModel):
    edge_candidate_id: str = Field(default_factory=lambda: new_id("edge"))
    cluster_id: str
    edge_product: str
    misuse_risks: list[str] = Field(default_factory=list)


class ArchetypeFitScore(BaseModel):
    archetype: str
    score: float = Field(ge=0.0, le=1.0)
    rationale: str
    source_span_ids: list[str] = Field(default_factory=list)


class ArchetypeFitMatrix(BaseModel):
    archetype_fit_matrix_id: str = Field(default_factory=lambda: new_id("archetype_fit"))
    cluster_id: str
    scores: list[ArchetypeFitScore]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.scores:
            raise ValueError("ArchetypeFitMatrix requires scores")


class ArchetypeMeaningProgram(BaseModel):
    archetype_program_id: str = Field(default_factory=lambda: new_id("archetype_program"))
    primary_archetype: str
    secondary_archetypes: list[str] = Field(default_factory=list)
    required_modules: list[str]
    source_evidence_span_ids: list[str]
    format_affinity: dict[str, float] = Field(default_factory=dict)
    risk_flags: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.source_evidence_span_ids:
            raise ValueError("ArchetypeMeaningProgram requires source evidence")
        if not self.required_modules:
            raise ValueError("ArchetypeMeaningProgram requires required_modules")


class PrimitiveCandidateSet(BaseModel):
    primitive_candidate_set_id: str = Field(default_factory=lambda: new_id("primitive_candidates"))
    cluster_id: str
    meaning_plane_family: str
    experience_plane_family: str
    primitive_family: str
    primitive_binding_candidate: str
    coalition_signature_candidate: str
    edge_product_candidate: str
    misuse_risk_candidates: list[str] = Field(default_factory=list)


class PrimitiveCoalitionCandidate(BaseModel):
    primitive_coalition_candidate_id: str = Field(default_factory=lambda: new_id("coalition_candidate"))
    primitive_candidate_set_id: str
    coalition_signature: str
    governing_primitives: list[str]
    misuse_risks: list[str] = Field(default_factory=list)


class DeliveryRecipeProgram(BaseModel):
    delivery_recipe_program_id: str = Field(default_factory=lambda: new_id("delivery_recipe"))
    archetype_program_id: str
    module_sequence: list[str]
    emotional_temperature: str
    first_frame_tension: float = Field(default=0.5, ge=0.0, le=1.0)
    text_interruption_budget: int = Field(default=3, ge=0)
    motion_intensity_hint: str = "medium"
    sound_doctrine_hint: str = "voice_first"


class FormatFitScore(BaseModel):
    target: ExtractionTarget
    score: float = Field(ge=0.0, le=1.0)
    rationale: str


class FormatFitMatrix(BaseModel):
    format_fit_matrix_id: str = Field(default_factory=lambda: new_id("format_fit"))
    cluster_id: str
    scores: list[FormatFitScore]


class FormatExpressionProgram(BaseModel):
    format_expression_program_id: str = Field(default_factory=lambda: new_id("format_expression"))
    target: ExtractionTarget
    cluster_id: str
    required_ingredients: list[IngredientType]
    preserve: list[str] = Field(default_factory=list)
    forbid: list[str] = Field(default_factory=list)
    emit_packet_type: str


class ExpectedActualIngredientDiff(BaseModel):
    diff_id: str = Field(default_factory=lambda: new_id("ingredient_diff"))
    question_id: str
    expected_ingredients: list[IngredientType]
    actual_ingredients: list[IngredientType]
    hits: list[IngredientType] = Field(default_factory=list)
    misses: list[IngredientType] = Field(default_factory=list)
    unexpected_wins: list[IngredientType] = Field(default_factory=list)
    route_change: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        overlap = set(self.hits).intersection(set(self.misses))
        if overlap:
            raise ValueError(f"Ingredients cannot be both hit and missing: {overlap}")


class QuestionCoverageReceipt(BaseModel):
    question_coverage_receipt_id: str = Field(default_factory=lambda: new_id("question_coverage"))
    question_id: str
    coverage_status: CoverageStatus
    answer_span_refs: list[str]
    expected_ingredients_hit: list[IngredientType] = Field(default_factory=list)
    expected_ingredients_missing: list[IngredientType] = Field(default_factory=list)
    unexpected_high_value_ingredients: list[IngredientType] = Field(default_factory=list)
    best_output_routes: list[ExtractionTarget] = Field(default_factory=list)
    follow_up_needed: bool = False
    follow_up_question: str | None = None


class BriefAlignmentReport(BaseModel):
    brief_alignment_report_id: str = Field(default_factory=lambda: new_id("brief_alignment"))
    interview_brief_id: str
    question_receipt_ids: list[str]
    overall_alignment: float = Field(default=0.0, ge=0.0, le=1.0)
    missed_depth_paths: list[str] = Field(default_factory=list)
    unexpected_wins: list[str] = Field(default_factory=list)


class FollowUpQuestion(BaseModel):
    follow_up_question_id: str = Field(default_factory=lambda: new_id("followup"))
    question_text: str
    missing_ingredient: IngredientType
    target_archetype: str | None = None
    reason: str


class FollowUpQuestionSet(BaseModel):
    follow_up_question_set_id: str = Field(default_factory=lambda: new_id("followup_set"))
    questions: list[FollowUpQuestion]


class BriefOverrideRecommendation(BaseModel):
    brief_override_recommendation_id: str = Field(default_factory=lambda: new_id("brief_override"))
    original_target: str
    recommended_target: str
    reason: str
    source_span_ids: list[str]


class SuperVisualExtractionPacket(BaseModel):
    supervisual_extraction_packet_id: str = Field(default_factory=lambda: new_id("supervisual_packet"))
    single_source_truth: str
    visual_hook_candidate: str
    edge_product: str
    source_span_refs: list[str]
    proof_object_candidate: str | None = None
    memory_object_candidate: str | None = None
    micro_semiotic_anchor_candidate: str | None = None
    visual_spr_candidate: str | None = None
    frame_profile_hint: str = "1:1_SOFT_ROUNDED_EDITORIAL"
    style_route_hint: str | None = None
    composition_role_hint: str = "hero_visual"
    negative_space_requirement: str = "intentional_negative_space"
    text_overlay_candidate: str | None = None
    source_fidelity_risk: str = "normal"

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.source_span_refs:
            raise ValueError("SuperVisualExtractionPacket requires source_span_refs")
        if not self.single_source_truth:
            raise ValueError("SuperVisualExtractionPacket requires a single source truth")


class CarouselSlideSeed(BaseModel):
    slide_index: int
    role: str
    slide_copy: str
    source_ref: str | None = None


class CarouselExtractionPacket(BaseModel):
    carousel_extraction_packet_id: str = Field(default_factory=lambda: new_id("carousel_packet"))
    carousel_thesis: str
    source_span_refs: list[str]
    viewer_state_sequence: list[ViewerStateFunction]
    slides: list[CarouselSlideSeed]
    open_loop: str
    closure_contract: str
    slide_count_hint: int = Field(default=7, ge=3, le=12)
    visual_system_seed: str | None = None
    asset_requirement_seed: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.source_span_refs:
            raise ValueError("CarouselExtractionPacket requires source_span_refs")
        indexes = [slide.slide_index for slide in self.slides]
        if indexes != list(range(1, len(indexes) + 1)):
            raise ValueError("Carousel slide seeds must be continuous")
        if not self.closure_contract:
            raise ValueError("CarouselExtractionPacket requires closure_contract")


class ArollStorySpine(BaseModel):
    aroll_story_spine_id: str = Field(default_factory=lambda: new_id("aroll_spine"))
    source_span_refs: list[str]
    spine_lines: list[str]

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.source_span_refs or not self.spine_lines:
            raise ValueError("ArollStorySpine requires source refs and spine lines")


class CutQuestionContract(BaseModel):
    cut_question_contract_id: str = Field(default_factory=lambda: new_id("cut_question"))
    cut_index: int
    raises: str
    answers: str
    feeling: str
    tempo: str
    source_span_refs: list[str] = Field(default_factory=list)


class EmotionalChangeMap(BaseModel):
    emotional_change_map_id: str = Field(default_factory=lambda: new_id("emotional_change"))
    before_state: str
    pressure_state: str | None = None
    truthful_payoff: str
    after_state: str


class BrollForeshadowingPair(BaseModel):
    broll_foreshadowing_pair_id: str = Field(default_factory=lambda: new_id("broll_pair"))
    before_visual: str
    after_visual: str
    change_function: str
    source_signal: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.before_visual or not self.after_visual or not self.change_function:
            raise ValueError("BrollForeshadowingPair requires before_visual, after_visual, and change_function")


class RhythmPriorityMap(BaseModel):
    rhythm_priority_map_id: str = Field(default_factory=lambda: new_id("rhythm_priority"))
    priorities_by_scene: dict[str, str]


class PowerPhrasePlan(BaseModel):
    power_phrase_plan_id: str = Field(default_factory=lambda: new_id("power_phrase"))
    phrases: list[str]


class SonicStoryArcSeed(BaseModel):
    sonic_story_arc_seed_id: str = Field(default_factory=lambda: new_id("sonic_seed"))
    voice_master: bool = True
    room_tone: str = "natural"
    sound_cues: list[str] = Field(default_factory=list)
    memetic_cue_limit: str = "1_per_30s"


class Format01StoryExtractionPacket(BaseModel):
    format01_packet_id: str = Field(default_factory=lambda: new_id("format01_packet"))
    sub_format: str
    aroll_story_spine: ArollStorySpine
    emotional_change_map: EmotionalChangeMap
    cut_question_chain: list[CutQuestionContract]
    broll_foreshadowing_pairs: list[BrollForeshadowingPair] = Field(default_factory=list)
    rhythm_priority_map: RhythmPriorityMap
    power_phrase_plan: PowerPhrasePlan
    sonic_story_arc_seed: SonicStoryArcSeed
    memory_object_candidates: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.cut_question_chain:
            raise ValueError("Format01StoryExtractionPacket requires cut_question_chain")


class Format02ExplainerExtractionPacket(BaseModel):
    format02_packet_id: str = Field(default_factory=lambda: new_id("format02_packet"))
    sub_format: str
    teachable_mechanism: str
    source_span_refs: list[str]
    concept_nodes: list[str]
    diagram_sequence: list[str]
    avatar_performance_requirements: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.teachable_mechanism:
            raise ValueError("Format02 requires teachable_mechanism")
        if not self.source_span_refs:
            raise ValueError("Format02 requires source_span_refs")


class Format03ReactionExtractionPacket(BaseModel):
    format03_packet_id: str = Field(default_factory=lambda: new_id("format03_packet"))
    sub_format: str
    proof_or_quote_surface: str
    source_span_refs: list[str]
    coach_reaction_angle: str
    rough_notation_targets: list[str] = Field(default_factory=list)
    reaction_question: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.proof_or_quote_surface:
            raise ValueError("Format03 requires proof_or_quote_surface")
        if not self.source_span_refs:
            raise ValueError("Format03 requires source_span_refs")


class Format04ConsciousReactionExtractionPacket(BaseModel):
    format04_packet_id: str = Field(default_factory=lambda: new_id("format04_packet"))
    sub_format: str
    debate_tension: str
    source_span_refs: list[str]
    reaction_ui_surface: str
    score_state_seed: str | None = None
    meme_mechanism: str | None = None
    memetic_cue_limit: str = "1_per_10s"

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.debate_tension:
            raise ValueError("Format04 requires debate_tension")
        if not self.reaction_ui_surface:
            raise ValueError("Format04 requires reaction_ui_surface")
        if not self.source_span_refs:
            raise ValueError("Format04 requires source_span_refs")


class VideoExtractionPacket(BaseModel):
    video_extraction_packet_id: str = Field(default_factory=lambda: new_id("video_packet"))
    selected_beat_refs: list[str]
    aroll_spine_candidates: list[str] = Field(default_factory=list)
    expression_moment_refs: list[str] = Field(default_factory=list)
    scene_candidate_map: dict[str, str] = Field(default_factory=dict)
    broll_requirements: list[str] = Field(default_factory=list)
    sonic_story_requirements: list[str] = Field(default_factory=list)
    subtitle_power_phrases: list[str] = Field(default_factory=list)
    cut_question_chain_refs: list[str] = Field(default_factory=list)
    timeline_duration_hint_seconds: int = 60


class MemeVisualExtractionPacket(BaseModel):
    meme_visual_packet_id: str = Field(default_factory=lambda: new_id("meme_packet"))
    sub_format: str
    source_truth: str
    compressed_paradox: str
    meme_mechanism: str
    source_span_refs: list[str]
    risk: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.meme_mechanism:
            raise ValueError("MemeVisualExtractionPacket requires meme_mechanism")


class PollVisualExtractionPacket(BaseModel):
    poll_visual_packet_id: str = Field(default_factory=lambda: new_id("poll_packet"))
    sub_format: str
    question: str
    options: list[str]
    source_span_refs: list[str]
    discussion_value: str = "medium"

    def __init__(self, **data: Any):
        super().__init__(**data)
        if len(self.options) < 2:
            raise ValueError("PollVisualExtractionPacket requires at least two options")
        if not self.source_span_refs:
            raise ValueError("PollVisualExtractionPacket requires source_span_refs")


class ReactionSeedPacket(BaseModel):
    reaction_seed_id: str = Field(default_factory=lambda: new_id("reaction_seed"))
    source_expression_moment_id: str | None = None
    source_quote: str
    source_span_refs: list[str]
    reaction_question: str
    compatible_reaction_formats: list[str]
    status: str = "stored_for_future_use"

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.source_span_refs:
            raise ValueError("ReactionSeedPacket requires source_span_refs")


class AssetPackageCandidateSet(BaseModel):
    asset_package_candidate_set_id: str = Field(default_factory=lambda: new_id("asset_package_candidates"))
    source_expression_session_id: str | None = None
    video_packet_ids: list[str] = Field(default_factory=list)
    carousel_packet_ids: list[str] = Field(default_factory=list)
    supervisual_packet_ids: list[str] = Field(default_factory=list)
    meme_visual_packet_ids: list[str] = Field(default_factory=list)
    poll_visual_packet_ids: list[str] = Field(default_factory=list)
    reaction_seed_ids: list[str] = Field(default_factory=list)
    enforce_guest_asset_pack_counts: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.enforce_guest_asset_pack_counts:
            if len(self.video_packet_ids) < 4:
                raise ValueError("Guest Asset Pack requires at least 4 videos")
            if len(self.carousel_packet_ids) < 2:
                raise ValueError("Guest Asset Pack requires at least 2 carousels")
            if len(self.meme_visual_packet_ids) < 2:
                raise ValueError("Guest Asset Pack requires at least 2 meme visuals")
            if len(self.poll_visual_packet_ids) < 2:
                raise ValueError("Guest Asset Pack requires at least 2 poll visuals")
            if len(self.reaction_seed_ids) < 2:
                raise ValueError("Guest Asset Pack requires at least 2 reaction seeds")


class CompleteEditingSessionRequestCandidate(BaseModel):
    complete_editing_session_request_id: str = Field(default_factory=lambda: new_id("editing_session_req"))
    source_expression_session_id: str
    expression_moment_id: str | None = None
    asset_type: str
    archetype: str
    derivative: str
    cmf_route: str
    source_span_refs: list[str]
    evaluation_requirements: list[str] = Field(default_factory=list)


class ExtractionGapReport(BaseModel):
    extraction_gap_report_id: str = Field(default_factory=lambda: new_id("gap_report"))
    missing_ingredients: list[IngredientType] = Field(default_factory=list)
    missing_context: list[str] = Field(default_factory=list)
    missing_source_refs: list[str] = Field(default_factory=list)
    severity: str = "low"


class SourceFidelityReceipt(BaseModel):
    source_fidelity_receipt_id: str = Field(default_factory=lambda: new_id("source_fidelity"))
    pass_status: PassStatus
    invented_claims: list[str] = Field(default_factory=list)
    unsupported_interpretations: list[str] = Field(default_factory=list)
    checked_span_ids: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if (self.invented_claims or self.unsupported_interpretations) and self.pass_status == PassStatus.PASS:
            raise ValueError("SourceFidelityReceipt with invented/unsupported content cannot pass")


class ExtractionQualityReceipt(BaseModel):
    extraction_quality_receipt_id: str = Field(default_factory=lambda: new_id("extraction_quality"))
    source_fidelity: float = Field(ge=0.0, le=1.0)
    brief_alignment: float = Field(ge=0.0, le=1.0)
    archetype_fit: float = Field(ge=0.0, le=1.0)
    primitive_fit: float = Field(ge=0.0, le=1.0)
    expression_density: float = Field(ge=0.0, le=1.0)
    asset_yield: float = Field(ge=0.0, le=1.0)
    format_diversity: float = Field(ge=0.0, le=1.0)
    visual_routeability: float = Field(ge=0.0, le=1.0)
    gap_severity: str = "low"


class ExtractionCommanderVerdict(BaseModel):
    extraction_commander_verdict_id: str = Field(default_factory=lambda: new_id("extraction_verdict"))
    authorized: bool
    pass_status: PassStatus
    blockers: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blockers and self.authorized:
            raise ValueError("Extraction cannot be authorized with blockers")


class InterviewerLearningReceipt(BaseModel):
    interviewer_learning_receipt_id: str = Field(default_factory=lambda: new_id("interviewer_learning"))
    missed_depth_paths: list[str] = Field(default_factory=list)
    successful_activation_patterns: list[str] = Field(default_factory=list)
    recommended_followup_questions: list[str] = Field(default_factory=list)


class NarrativeStoryDoctorRun(BaseModel):
    narrative_story_doctor_run_id: str = Field(default_factory=lambda: new_id("nsd_run"))
    context: LayerAwareExtractionContext
    source_packet_id: str
    interview_brief_binding_id: str | None = None
    status: str = "created"
    created_at: str = Field(default_factory=_now_iso)
