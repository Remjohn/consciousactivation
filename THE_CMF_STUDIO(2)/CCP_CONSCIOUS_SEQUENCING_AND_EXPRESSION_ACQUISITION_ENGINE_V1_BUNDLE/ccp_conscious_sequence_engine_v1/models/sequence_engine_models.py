from __future__ import annotations

from enum import Enum
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class IngredientClass(str, Enum):
    HUMAN_EXPRESSION = "human_expression"
    RESEARCH_EVIDENCE = "research_evidence"
    AUDIENCE_REALITY = "audience_reality"
    VISUAL = "visual"
    BRAND_CONTINUITY = "brand_continuity"


class RequirementStatus(str, Enum):
    PLANNED = "planned"
    TARGETED = "targeted"
    PARTIAL = "partial"
    CAPTURED = "captured"
    QUALITY_PASSED = "quality_passed"
    SUBSTITUTED = "substituted"
    MISSING = "missing"
    PICKUP_REQUESTED = "pickup_requested"
    WAIVED = "waived"


class ViewerState(str, Enum):
    PERCEPTUAL_ENTRY = "perceptual_entry"
    RELEVANT_OPEN_QUESTION = "relevant_open_question"
    ACTIVE_PREDICTION = "active_prediction"
    TRUTHFUL_PAYOFF = "truthful_payoff"
    HUMAN_AFFINITY = "human_affinity"
    EXPECTED_FUTURE_VALUE = "expected_future_value"


class InterviewState(str, Enum):
    RAPPORT = "rapport"
    SAFETY = "safety"
    AUTHORITY = "authority"
    CINEMATIC = "cinematic"
    VULNERABILITY = "vulnerability"
    REFLECTION = "reflection"
    TEACHING = "teaching"
    HUMOR = "humor"
    INVITATION = "invitation"
    EDGE_PRESSURE = "edge_pressure"


class SourceType(str, Enum):
    GUEST_EXPRESSION = "guest_expression"
    GUEST_STORY = "guest_story"
    GUEST_TEACHING = "guest_teaching"
    GUEST_AUTHORITY = "guest_authority"
    LIVE_REACTION = "live_reaction"
    AUDIENCE_RESEARCH = "audience_research"
    GUEST_DOSSIER = "guest_dossier"
    EXTERNAL_RESEARCH = "external_research"
    BRAND_MEMORY = "brand_memory"
    VISUAL_ARCHIVE = "visual_archive"
    PICKUP = "pickup"


class SequenceScope(str, Enum):
    SINGLE_ASSET = "single_asset"
    ASSET_PACKAGE = "asset_package"
    SERIES = "series"


class ProgramStatus(str, Enum):
    DRAFT = "draft"
    SOURCE_VALIDATED = "source_validated"
    DOCTRINE_VALIDATED = "doctrine_validated"
    FORMAT_ADAPTED = "format_adapted"
    AWAITING_REVIEW = "awaiting_review"
    APPROVED = "approved"
    FROZEN = "frozen"
    RENDERED = "rendered"
    EVALUATED = "evaluated"
    PUBLISHED = "published"


class QualityMinimums(StrictModel):
    specificity: float = Field(default=0.0, ge=0, le=1)
    audience_relevance: float = Field(default=0.0, ge=0, le=1)
    emotional_density: float = Field(default=0.0, ge=0, le=1)
    explanatory_completeness: float = Field(default=0.0, ge=0, le=1)
    source_integrity: float = Field(default=1.0, ge=0, le=1)


class ResearchContextRefs(StrictModel):
    guest_dossier_id: str
    audience_reality_brief_id: str
    interviewer_resonance_context_id: str
    context_premise_ids: List[str]
    matrix_of_edging_brief_id: str
    doctrine_bundle_id: str


class AssetPortfolioIntent(StrictModel):
    target_outputs: List[str]
    required_output_count: Optional[int] = Field(default=None, ge=1)
    exploratory_routes_allowed: bool = True


class IngredientRequirement(StrictModel):
    ingredient_requirement_id: str
    ingredient_role: str
    ingredient_class: IngredientClass
    required: bool = True
    preferred_source: SourceType
    acquisition_instrument_ids: List[str] = Field(default_factory=list)
    sequence_hypothesis_ids: List[str] = Field(default_factory=list)
    compatible_asset_routes: List[str] = Field(default_factory=list)
    acceptable_substitute_roles: List[str] = Field(default_factory=list)
    fallback_sources: List[SourceType] = Field(default_factory=list)
    minimum_quality: QualityMinimums = Field(default_factory=QualityMinimums)
    status: RequirementStatus = RequirementStatus.PLANNED


class SequenceHypothesis(StrictModel):
    sequence_hypothesis_id: str
    target_archetype: str
    asset_derivative: Optional[str] = None
    target_asset_route: str
    format_target: str
    sequence_pattern_id: str
    central_viewer_question: str
    promised_payoff: str
    anticipated_wrong_model: Optional[str] = None
    closure_type: str
    affinity_opportunity: Optional[str] = None
    future_value_key: Optional[str] = None
    ingredient_requirement_ids: List[str]
    confidence: float = Field(default=0.5, ge=0, le=1)


class InterviewStateStep(StrictModel):
    order: int = Field(ge=0)
    state: InterviewState
    purpose: str
    transition_condition: Optional[str] = None


class LiveCoveragePolicy(StrictModel):
    track_ingredient_coverage: bool = True
    prompt_when_required_ingredient_missing: bool = True
    do_not_interrupt_emotional_peak: bool = True
    allow_unexpected_ingredient_substitution: bool = True
    require_interviewer_confirmation_for_sensitive_followup: bool = True


class ExpressionAcquisitionPlan(StrictModel):
    plan_id: str
    ingredient_requirements: List[IngredientRequirement]
    shared_requirement_groups: Dict[str, List[str]] = Field(default_factory=dict)
    visual_asset_request_ids: List[str] = Field(default_factory=list)
    research_task_ids: List[str] = Field(default_factory=list)
    pickup_policy: str = "request_pickup_before_synthetic_repair"


class InterviewBriefV2(StrictModel):
    schema_version: str = "1.0.0"
    interview_brief_id: str
    brand_id: str
    brand_context_version_id: str
    guest_id: str
    interviewer_id: str
    research_context: ResearchContextRefs
    asset_portfolio_intent: AssetPortfolioIntent
    sequence_hypotheses: List[SequenceHypothesis]
    expression_acquisition_plan: ExpressionAcquisitionPlan
    interview_state_sequence: List[InterviewStateStep]
    live_coverage_policy: LiveCoveragePolicy
    status: Literal[
        "draft", "research_complete", "sequence_hypotheses_compiled",
        "acquisition_plan_ready", "operator_review", "approved",
        "active_session", "superseded"
    ] = "draft"


class FirstLineAnchors(StrictModel):
    cinematic: Optional[str] = None
    emotional: Optional[str] = None
    reels_hook: Optional[str] = None
    authority: Optional[str] = None
    teaching: Optional[str] = None
    invitation: Optional[str] = None


class RepairFollowups(StrictModel):
    too_historical: Optional[str] = None
    too_abstract: Optional[str] = None
    too_flat: Optional[str] = None
    not_clip_ready: Optional[str] = None
    missing_cost: Optional[str] = None
    missing_mechanism: Optional[str] = None
    missing_action: Optional[str] = None


class IngredientTarget(StrictModel):
    ingredient_role: str
    required_for: List[str]
    mandatory: bool = True


class CoverageSuccessRule(StrictModel):
    minimum_required_ingredients: int = Field(ge=0)
    mandatory_roles: List[str] = Field(default_factory=list)


class InterviewAssetContractV2(StrictModel):
    schema_version: str = "1.0.0"
    contract_id: str
    guest_id: str
    interviewer_id: str
    target_archetype: str
    asset_derivatives: List[str] = Field(default_factory=list)
    target_expression_states: List[InterviewState]
    edge_product: str
    sequence_hypothesis_ids: List[str]
    main_question: str
    first_line_anchors: FirstLineAnchors
    depth_anchor: Optional[str] = None
    narrative_instrumental_followups: List[str] = Field(default_factory=list)
    expected_source_material: List[str] = Field(default_factory=list)
    ingredient_targets: List[IngredientTarget]
    clip_start_rule: str
    depth_eval_rule: str
    landing_eval_targets: List[str]
    repair_followups: RepairFollowups = Field(default_factory=RepairFollowups)
    coverage_success_rule: CoverageSuccessRule
    safety_constraints: List[str] = Field(default_factory=list)


class CoverageItem(StrictModel):
    ingredient_requirement_id: str
    ingredient_role: str
    status: RequirementStatus
    provisional_quality: Optional[float] = Field(default=None, ge=0, le=1)
    source_segment_hint: Optional[str] = None
    notes: List[str] = Field(default_factory=list)


class LiveCue(StrictModel):
    cue_id: str
    cue_type: str
    text: str
    ingredient_role: Optional[str] = None
    proposed_at_tick: int = Field(ge=0)
    suppressed: bool = False
    suppression_reason: Optional[str] = None
    accepted_by_interviewer: Optional[bool] = None


class LiveIngredientCoverageState(StrictModel):
    schema_version: str = "1.0.0"
    expression_session_id: str
    interview_brief_id: str
    active_contract_id: Optional[str] = None
    current_interview_state: InterviewState
    emotional_peak_active: bool = False
    coverage_items: List[CoverageItem]
    cues: List[LiveCue] = Field(default_factory=list)
    last_updated_tick: int = Field(ge=0)


class SourceSegment(StrictModel):
    expression_session_id: str
    recording_artifact_id: str
    speaker_id: str
    start_tick: int = Field(ge=0)
    end_tick: int = Field(gt=0)
    transcript_text: str

    @model_validator(mode="after")
    def validate_order(self):
        if self.end_tick <= self.start_tick:
            raise ValueError("end_tick must be greater than start_tick")
        return self


class IngredientQualityScores(StrictModel):
    specificity: float = Field(ge=0, le=1)
    emotional_density: float = Field(ge=0, le=1)
    truth_density: float = Field(ge=0, le=1)
    audience_relevance: float = Field(ge=0, le=1)
    clipability: float = Field(ge=0, le=1)
    explanatory_completeness: float = Field(ge=0, le=1)
    evidence_strength: float = Field(ge=0, le=1)
    visual_routeability: float = Field(ge=0, le=1)
    source_integrity: float = Field(ge=0, le=1)
    brand_fit: float = Field(ge=0, le=1)


class ExpressionIngredient(StrictModel):
    ingredient_id: str
    ingredient_role: str
    ingredient_class: IngredientClass
    source_type: SourceType
    source_segment: Optional[SourceSegment] = None
    external_source_ref: Optional[str] = None
    expression_state: Optional[InterviewState] = None
    primitive_tags: List[str] = Field(default_factory=list)
    edge_product_ids: List[str] = Field(default_factory=list)
    archetype_compatibility: List[str] = Field(default_factory=list)
    asset_compatibility: List[str] = Field(default_factory=list)
    quality_scores: IngredientQualityScores
    planned_requirement_ids: List[str] = Field(default_factory=list)
    approval_status: Literal["extracted", "auto_evaluated", "human_reviewed", "approved", "rejected", "needs_repair"] = "extracted"
    sha256: str

    @model_validator(mode="after")
    def require_source(self):
        if not self.source_segment and not self.external_source_ref:
            raise ValueError("An expression ingredient requires source_segment or external_source_ref")
        return self


class IngredientRelation(StrictModel):
    source_ingredient_id: str
    target_ingredient_id: str
    relation_type: Literal[
        "opens_question", "adds_stake", "provides_clue", "complicates",
        "contradicts", "reframes", "answers", "provides_proof",
        "humanizes", "creates_future_value", "transitions"
    ]
    confidence: float = Field(ge=0, le=1)


class IngredientGap(StrictModel):
    ingredient_role: str
    requirement_ids: List[str]
    gap_type: Literal["missing", "weak", "source_integrity", "visual_missing", "research_missing"]
    recommended_action: Literal["pickup", "research", "visual_request", "substitute", "waive", "abandon_sequence"]
    notes: str


class ExpressionIngredientInventory(StrictModel):
    schema_version: str = "1.0.0"
    ingredient_inventory_id: str
    expression_session_id: str
    interview_brief_id: str
    ingredients: List[ExpressionIngredient]
    relations: List[IngredientRelation] = Field(default_factory=list)
    gaps: List[IngredientGap] = Field(default_factory=list)
    unexpected_high_value_ingredient_ids: List[str] = Field(default_factory=list)
    frozen: bool = False
    inventory_sha256: Optional[str] = None


class SequenceLoop(StrictModel):
    loop_id: str
    question: str
    opened_at_beat_id: str
    closed_at_beat_id: Optional[str] = None
    closure_required: bool = True
    policy: Literal["must_close", "discussion_open", "series_deferred"] = "must_close"


class ViewerJourney(StrictModel):
    entry_state: str
    target_exit_state: str
    central_question: str
    promised_payoff: str
    future_value_key: Optional[str] = None


class SequenceBeat(StrictModel):
    beat_id: str
    order: int = Field(ge=0)
    viewer_state: ViewerState
    semantic_role: str
    ingredient_ids: List[str]
    information_state: str
    primitive_coalition: List[str] = Field(default_factory=list)
    composition_function: str
    emotional_state: Optional[str] = None
    duration_ms: Optional[int] = Field(default=None, ge=0)
    slide_index: Optional[int] = Field(default=None, ge=1)
    attention_order: Optional[int] = Field(default=None, ge=0)


class DoctrineConstraints(StrictModel):
    no_false_open_loop: bool = True
    no_fabricated_conflict: bool = True
    no_trauma_sensationalization: bool = True
    payoff_must_be_source_grounded: bool = True
    guest_meaning_may_not_be_distorted: bool = True
    no_synthetic_guest_claim: bool = True


class AffinityContract(StrictModel):
    authentic_human_presence_required: bool = True
    preferred_cues: List[str] = Field(default_factory=list)
    forbidden_cues: List[str] = Field(default_factory=list)


class FutureValueContract(StrictModel):
    scope: Literal["asset_signal", "package", "series"]
    category_promise: str
    continuity_keys: List[str] = Field(default_factory=list)


class ContentSequenceProgram(StrictModel):
    schema_version: str = "1.0.0"
    sequence_program_id: str
    version: int = Field(ge=1)
    status: ProgramStatus
    scope: SequenceScope = SequenceScope.SINGLE_ASSET
    brand_id: str
    brand_context_version_id: str
    doctrine_bundle_id: str
    interview_brief_id: str
    expression_session_id: str
    ingredient_inventory_id: str
    target_archetype: str
    asset_derivative: Optional[str] = None
    format_target: str
    sequence_pattern_id: str
    viewer_journey: ViewerJourney
    loops: List[SequenceLoop]
    beats: List[SequenceBeat]
    affinity_contract: AffinityContract
    future_value_contract: FutureValueContract
    doctrine_constraints: DoctrineConstraints = Field(default_factory=DoctrineConstraints)
    evaluation_requirement_ids: List[str] = Field(default_factory=list)
    operator_approval_status: Literal["not_reviewed", "needs_revision", "approved", "rejected"] = "not_reviewed"
    program_sha256: Optional[str] = None

    @model_validator(mode="after")
    def check_order_and_loops(self):
        orders = [b.order for b in self.beats]
        if orders != sorted(orders) or len(set(orders)) != len(orders):
            raise ValueError("Beat order values must be unique and sorted")
        beat_ids = {b.beat_id for b in self.beats}
        for loop in self.loops:
            if loop.opened_at_beat_id not in beat_ids:
                raise ValueError(f"Unknown opening beat {loop.opened_at_beat_id}")
            if loop.closure_required and loop.policy == "must_close" and not loop.closed_at_beat_id:
                raise ValueError(f"Loop {loop.loop_id} must close")
            if loop.closed_at_beat_id and loop.closed_at_beat_id not in beat_ids:
                raise ValueError(f"Unknown closing beat {loop.closed_at_beat_id}")
        return self


class PackageAssetRef(StrictModel):
    asset_id: str
    sequence_program_id: str
    format_target: str
    relationship_role: str
    order: int = Field(ge=1)


class PackageSequenceProgram(StrictModel):
    schema_version: str = "1.0.0"
    package_sequence_program_id: str
    brand_id: str
    brand_context_version_id: str
    package_type: str
    category_promise: str
    assets: List[PackageAssetRef]
    diversity_requirements: Dict[str, int] = Field(default_factory=dict)
    status: Literal["draft", "evaluated", "approved", "scheduled", "completed"] = "draft"


class SequenceStageScore(StrictModel):
    stage: ViewerState
    score: float = Field(ge=0, le=1)
    dimensions: Dict[str, float]
    notes: List[str] = Field(default_factory=list)


class SequenceEvaluationReceipt(StrictModel):
    schema_version: str = "1.0.0"
    receipt_id: str
    sequence_program_id: str
    sequence_program_sha256: str
    stage_scores: List[SequenceStageScore]
    loop_closure_score: float = Field(ge=0, le=1)
    source_grounding_score: float = Field(ge=0, le=1)
    voice_dna_score: float = Field(ge=0, le=1)
    negative_space_score: float = Field(ge=0, le=1)
    doctrine_alignment_score: float = Field(ge=0, le=1)
    confusion_penalty: float = Field(ge=0, le=1)
    manipulation_risk: float = Field(ge=0, le=1)
    overall_score: float = Field(ge=0, le=1)
    hard_failures: List[str] = Field(default_factory=list)
    operator_status: Literal["approved", "needs_revision", "rejected"]
