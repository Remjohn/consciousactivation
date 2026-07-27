from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ActivationDomain(str, Enum):
    SOURCE = "source"
    RELATIONSHIP = "relationship"
    AUDIENCE = "audience"


class EpistemicState(str, Enum):
    PLANNED = "planned"
    OBSERVED = "observed"
    INFERRED = "inferred"
    OPERATOR_CONFIRMED = "operator_confirmed"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class LifecycleState(str, Enum):
    CONTEXT_LOCKED = "context_locked"
    HYPOTHESES_COMPILED = "hypotheses_compiled"
    PLANNED = "planned"
    ARMED = "armed"
    LIVE = "live"
    OBSERVED = "observed"
    RESOLVED = "resolved"
    SOURCE_PACKAGED = "source_packaged"
    TRANSFERRED = "transferred"
    PRODUCED = "produced"
    PUBLISHED = "published"
    EVALUATED = "evaluated"
    LEARNED = "learned"
    SUPERSEDED = "superseded"
    CANCELLED = "cancelled"


class AdmissionMode(str, Enum):
    BRIEF_LED = "brief_led"
    IMPORTED_SOURCE = "imported_source"


class NarrativeState(str, Enum):
    CINEMATIC = "cinematic"
    VULNERABILITY = "vulnerability"
    AUTHORITY = "authority"
    TEACHING = "teaching"
    INVITATION = "invitation"


class ActivationDirection(str, Enum):
    MIRROR = "mirror"
    TARGET = "target"
    TRIBE = "tribe"
    MORAL = "moral"
    ASPIRATION = "aspiration"
    FUTURE_LOSS = "future_loss"
    GRIEF = "grief"
    NOSTALGIA = "nostalgia"
    CONTRADICTION = "contradiction"
    CURIOSITY = "curiosity"


class ReactionOutcome(str, Enum):
    ANCHOR_HIT = "anchor_hit"
    PARTIAL_ANCHOR_HIT = "partial_anchor_hit"
    UNEXPECTED_EDGE = "unexpected_edge"
    STATE_TRANSITION = "state_transition"
    COMPLETE_LANDING = "complete_landing"
    FLAT_ANSWER = "flat_answer"
    TOPIC_ESCAPE = "topic_escape"
    DEFENSIVE_REACTION = "defensive_reaction"
    COUNTERACTIVATION = "counteractivation"
    ACTIVATION_NULL = "activation_null"
    OBSERVATION_FAILURE = "observation_failure"
    OPERATOR_INTERRUPTION = "operator_interruption"


class ExpressionMomentState(str, Enum):
    PROPOSED = "proposed"
    VALIDATED = "validated"
    APPROVED = "approved"
    BORDERLINE = "borderline"
    REJECTED = "rejected"
    SUPERSEDED = "superseded"


class ImmutableRef(StrictModel):
    object_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")

    @property
    def uri(self) -> str:
        return f"{self.object_id}@{self.version}#sha256:{self.sha256}"


class EvidenceRef(StrictModel):
    ref: ImmutableRef
    description: str = Field(min_length=1)
    source_span: str | None = None


class ApplicabilityEnvelope(StrictModel):
    coach_ids: tuple[str, ...] = ()
    audience_segments: tuple[str, ...] = ()
    platforms: tuple[str, ...] = ()
    relationship_stages: tuple[str, ...] = ()
    formats: tuple[str, ...] = ()
    pressure_domains: tuple[str, ...] = ()
    exclusions: tuple[str, ...] = ()


class IdentityDNACandidateObservation(StrictModel):
    observation_id: str
    coach_id: str
    proposed_dimension: Literal[
        "identity_role", "stance", "edge", "emotional_range",
        "visual_world", "negative_space", "lived_proof"
    ]
    proposed_value: str
    epistemic_state: EpistemicState
    evidence_refs: tuple[ImmutableRef, ...]
    recurrence_count: int = Field(ge=1)
    contradictions: tuple[str, ...] = ()
    coach_fit: float = Field(ge=0, le=1)
    audience_fit: float = Field(ge=0, le=1)
    applicability: ApplicabilityEnvelope
    profile_resolution_status: Literal["pending", "approved", "rejected", "superseded"] = "pending"


class ActivationHypothesis(StrictModel):
    hypothesis_id: str
    domain: ActivationDomain
    hidden_pressure: str
    edge: str
    directions: tuple[ActivationDirection, ...]
    roles: tuple[str, ...] = Field(min_length=1)
    stance: str
    identity_urges: tuple[str, ...]
    stakes: tuple[str, ...]
    pressure_dose: int = Field(ge=0, le=5)
    participation_design: str
    intended_reaction: str
    smallest_useful_commitment: str
    expected_signals: tuple[str, ...] = ()
    counteractivation_hypotheses: tuple[str, ...] = ()
    wrong_reading_locks: tuple[str, ...] = Field(min_length=1)
    evidence_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    freshness_score: float = Field(ge=0, le=1)
    confidence: float = Field(ge=0, le=1)


class ActivationHypothesisPortfolio(StrictModel):
    portfolio_id: str
    candidates: tuple[ActivationHypothesis, ...] = Field(min_length=2)
    selected_hypothesis_id: str | None = None
    rejected_hypothesis_ids: tuple[str, ...] = ()
    diversity_axes: tuple[str, ...] = Field(min_length=1)
    stopping_reason: str | None = None

    @model_validator(mode="after")
    def validate_ids(self) -> "ActivationHypothesisPortfolio":
        ids = [c.hypothesis_id for c in self.candidates]
        if len(ids) != len(set(ids)):
            raise ValueError("candidate hypothesis IDs must be unique")
        if self.selected_hypothesis_id and self.selected_hypothesis_id not in ids:
            raise ValueError("selected hypothesis must exist in candidates")
        unknown = set(self.rejected_hypothesis_ids) - set(ids)
        if unknown:
            raise ValueError(f"rejected hypothesis IDs are unknown: {sorted(unknown)}")
        return self


class PlannedActivativeIntelligencePack(StrictModel):
    pack_id: str
    version: str
    lifecycle_state: Literal[LifecycleState.PLANNED] = LifecycleState.PLANNED
    epistemic_state: Literal[EpistemicState.PLANNED] = EpistemicState.PLANNED
    domain: ActivationDomain
    source_premise_ref: ImmutableRef
    coach_identity_dna_ref: ImmutableRef
    audience_context_premise_ref: ImmutableRef
    resonance_map_ref: ImmutableRef
    matrix_of_edging_ref: ImmutableRef
    interviewer_resonance_ref: ImmutableRef | None = None
    relationship_state_ref: ImmutableRef | None = None
    candidate_portfolio: ActivationHypothesisPortfolio
    selected_hypothesis_id: str
    target_narrative_state: NarrativeState | None = None
    evaluation_contract_ref: ImmutableRef
    registry_refs: tuple[ImmutableRef, ...]
    research_requests: tuple[str, ...] = ()
    semantic_runtime_executed: bool = False

    @model_validator(mode="after")
    def selected_matches_portfolio(self) -> "PlannedActivativeIntelligencePack":
        if self.selected_hypothesis_id not in {
            h.hypothesis_id for h in self.candidate_portfolio.candidates
        }:
            raise ValueError("selected_hypothesis_id must exist in candidate_portfolio")
        return self


class FollowUpBranch(StrictModel):
    branch_id: str
    condition: str
    question: str
    target_state: NarrativeState | None = None
    pressure_delta: int = Field(ge=-2, le=2)
    stop_after: bool = False


class InterviewAssetContract(StrictModel):
    contract_id: str
    planned_pack_ref: ImmutableRef
    hypothesis_id: str
    target_state: NarrativeState
    current_state_hypothesis: NarrativeState | None = None
    first_line_anchor: str
    depth_anchor: str
    main_question: str
    follow_up_branches: tuple[FollowUpBranch, ...]
    expected_material: tuple[str, ...]
    anticipated_signals: tuple[str, ...]
    pressure_dose: int = Field(ge=0, le=5)
    pressure_ceiling: int = Field(ge=0, le=5)
    affinity_resets: tuple[str, ...] = ()
    landing_criteria: tuple[str, ...]
    clip_start_hypotheses: tuple[str, ...] = ()
    clip_end_hypotheses: tuple[str, ...] = ()
    eligible_routes: tuple[str, ...] = ()
    hard_negatives: tuple[str, ...] = ()
    wrong_reading_locks: tuple[str, ...] = Field(min_length=1)
    evaluation_contract_ref: ImmutableRef

    @model_validator(mode="after")
    def dose_ceiling(self) -> "InterviewAssetContract":
        if self.pressure_dose > self.pressure_ceiling:
            raise ValueError("pressure_dose cannot exceed pressure_ceiling")
        return self


class ReactionObservation(StrictModel):
    observation_id: str
    modality: Literal["lexical", "vocal", "visual", "temporal", "interactional", "technical"]
    source_ref: ImmutableRef
    time_start_ms: int | None = Field(default=None, ge=0)
    time_end_ms: int | None = Field(default=None, ge=0)
    observed_value: str
    observation_confidence: float = Field(ge=0, le=1)
    inferred_interpretations: tuple[str, ...] = ()

    @model_validator(mode="after")
    def valid_times(self) -> "ReactionObservation":
        if self.time_start_ms is not None and self.time_end_ms is not None:
            if self.time_end_ms < self.time_start_ms:
                raise ValueError("time_end_ms must be >= time_start_ms")
        return self


class ReactionReceipt(StrictModel):
    receipt_id: str
    contract_ref: ImmutableRef
    call_id: str
    pre_state: NarrativeState | None
    observations: tuple[ReactionObservation, ...]
    outcome: ReactionOutcome
    post_state: NarrativeState | None
    anchor_status: Literal["none", "partial", "hit", "unexpected"]
    epistemic_state: EpistemicState
    interpretation: str | None = None
    operator_resolution_ref: ImmutableRef | None = None
    next_action_recommendation: str
    evidence_refs: tuple[ImmutableRef, ...]
    created_at: datetime


class ExpressionMoment(StrictModel):
    moment_id: str
    source_package_ref: ImmutableRef
    source_span_ref: ImmutableRef
    speaker_id: str
    start_ms: int = Field(ge=0)
    end_ms: int = Field(gt=0)
    quote_or_summary: str
    context_window: str
    reaction_receipt_refs: tuple[ImmutableRef, ...] = ()
    qualities: tuple[str, ...]
    role_potential: tuple[str, ...]
    eligible_routes: tuple[str, ...]
    state: ExpressionMomentState
    epistemic_state: EpistemicState
    approval_ref: ImmutableRef | None = None
    rejection_reason: str | None = None
    wrong_reading_risks: tuple[str, ...] = ()

    @model_validator(mode="after")
    def moment_rules(self) -> "ExpressionMoment":
        if self.end_ms <= self.start_ms:
            raise ValueError("end_ms must be greater than start_ms")
        if self.state is ExpressionMomentState.APPROVED and self.approval_ref is None:
            raise ValueError("approved Expression Moments require approval_ref")
        if self.state is ExpressionMomentState.REJECTED and not self.rejection_reason:
            raise ValueError("rejected Expression Moments require rejection_reason")
        return self


class CanonicalInterviewSourcePackage(StrictModel):
    source_package_id: str
    version: str
    admission_mode: AdmissionMode
    original_media_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    transcript_ref: ImmutableRef
    speaker_map_ref: ImmutableRef
    phrase_pack_ref: ImmutableRef
    shot_map_ref: ImmutableRef | None = None
    keyframe_set_ref: ImmutableRef | None = None
    brief_ref: ImmutableRef | None = None
    planned_pack_ref: ImmutableRef | None = None
    absent_planning_declaration: bool = False
    tag_refs: tuple[ImmutableRef, ...] = ()
    reaction_receipt_refs: tuple[ImmutableRef, ...] = ()
    expression_moment_refs: tuple[ImmutableRef, ...] = ()
    operator_source_authority_ref: ImmutableRef
    provenance_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    lifecycle_state: Literal[LifecycleState.SOURCE_PACKAGED] = LifecycleState.SOURCE_PACKAGED

    @model_validator(mode="after")
    def admission_rules(self) -> "CanonicalInterviewSourcePackage":
        if self.admission_mode is AdmissionMode.BRIEF_LED:
            if self.brief_ref is None or self.planned_pack_ref is None:
                raise ValueError("brief-led admission requires brief_ref and planned_pack_ref")
        if self.admission_mode is AdmissionMode.IMPORTED_SOURCE:
            if not self.absent_planning_declaration:
                raise ValueError("imported source requires absent_planning_declaration=true")
        return self


class PlannedObservedDelta(StrictModel):
    activated_hypothesis_ids: tuple[str, ...] = ()
    unmet_hypothesis_ids: tuple[str, ...] = ()
    unexpected_edges: tuple[str, ...] = ()
    rejected_assumptions: tuple[str, ...] = ()
    unresolved_inferences: tuple[str, ...] = ()


class ObservedActivativeIntelligencePack(StrictModel):
    pack_id: str
    version: str
    planned_pack_ref: ImmutableRef
    source_package_ref: ImmutableRef
    lifecycle_state: Literal[LifecycleState.RESOLVED] = LifecycleState.RESOLVED
    epistemic_state: Literal[EpistemicState.OBSERVED, EpistemicState.OPERATOR_CONFIRMED]
    reaction_receipt_refs: tuple[ImmutableRef, ...]
    expression_moment_refs: tuple[ImmutableRef, ...]
    confirmed_roles: tuple[str, ...]
    confirmed_stances: tuple[str, ...]
    confirmed_stakes: tuple[str, ...]
    unresolved_inferences: tuple[str, ...] = ()
    identity_dna_candidate_observations: tuple[IdentityDNACandidateObservation, ...] = ()
    planned_observed_delta: PlannedObservedDelta
    transfer_requirements: tuple[str, ...]
    campaign_opportunities: tuple[str, ...] = ()
    wrong_reading_updates: tuple[str, ...] = ()


class ActivationTransferContract(StrictModel):
    transfer_id: str
    observed_pack_ref: ImmutableRef
    source_package_ref: ImmutableRef
    expression_moment_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    original_activation_generator: tuple[str, ...] = Field(min_length=1)
    source_role: str
    target_audience_roles: tuple[str, ...] = Field(min_length=1)
    must_remain_true: tuple[str, ...] = Field(min_length=1)
    required_changes: tuple[str, ...] = ()
    creative_degrees_of_freedom: tuple[str, ...] = ()
    permitted_compression: tuple[str, ...] = ()
    prohibited_collapses: tuple[str, ...] = Field(min_length=1)
    wrong_reading_locks: tuple[str, ...] = Field(min_length=1)
    target_format: str
    audience_segment: str
    evaluation_contract_ref: ImmutableRef


class DerivativeActivationProgram(StrictModel):
    program_id: str
    domain: Literal[ActivationDomain.AUDIENCE] = ActivationDomain.AUDIENCE
    transfer_contract_ref: ImmutableRef
    source_package_ref: ImmutableRef
    audience_segment: str
    format_harness: str
    directions: tuple[ActivationDirection, ...]
    roles: tuple[str, ...]
    stance: str
    emotional_load: str
    pattern_match: str
    pattern_interrupt: str
    attention_sequence: tuple[str, ...]
    participation_path: str
    freshness_profile_ref: ImmutableRef | None = None
    wrong_reading_locks: tuple[str, ...]


class CampaignAssetPlan(StrictModel):
    asset_id: str
    derivative_program_ref: ImmutableRef
    sequence_index: int = Field(ge=0)
    primary_role: str
    primary_direction: ActivationDirection
    edge: str
    format_harness: str


class CampaignActivationProgram(StrictModel):
    campaign_id: str
    source_package_ref: ImmutableRef
    audience_segments: tuple[str, ...] = Field(min_length=1)
    assets: tuple[CampaignAssetPlan, ...] = Field(min_length=1)
    role_diversity_minimum: int = Field(ge=1)
    direction_diversity_minimum: int = Field(ge=1)
    repeated_structure_limit: int = Field(ge=1)
    fatigue_budget: float = Field(ge=0, le=1)
    affinity_reset_indices: tuple[int, ...] = ()
    publication_order_locked: bool = True
    evaluation_contract_ref: ImmutableRef

    @model_validator(mode="after")
    def diversity_rules(self) -> "CampaignActivationProgram":
        if len({a.primary_role for a in self.assets}) < self.role_diversity_minimum:
            raise ValueError("campaign role diversity minimum not met")
        if len({a.primary_direction for a in self.assets}) < self.direction_diversity_minimum:
            raise ValueError("campaign direction diversity minimum not met")
        return self


class HumanResolutionEpisode(StrictModel):
    episode_id: str
    before_ref: ImmutableRef
    operator_action: str
    exact_reason: str
    wrong_reading: str | None = None
    implicated_layer: str
    accepted_replacement_ref: ImmutableRef | None = None
    invalidated_descendant_refs: tuple[ImmutableRef, ...] = ()
    applicability: ApplicabilityEnvelope
    evidence_refs: tuple[ImmutableRef, ...]
    learning_recommendation: Literal["none", "capture_only", "steering_candidate", "constitutional_candidate"]
    created_at: datetime


class FailureAttribution(StrictModel):
    failure_id: str
    failed_object_ref: ImmutableRef
    responsible_layer: str
    root_cause: str
    evidence_refs: tuple[ImmutableRef, ...]
    frozen_upstream_refs: tuple[ImmutableRef, ...]
    object_to_change_ref: ImmutableRef
    invalidated_descendant_refs: tuple[ImmutableRef, ...]
    rerun_nodes: tuple[str, ...]
    human_escalation_required: bool = False


class ActivationEvaluationReceipt(StrictModel):
    receipt_id: str
    evaluated_ref: ImmutableRef
    domain: ActivationDomain
    gate_results: dict[str, bool]
    dimension_scores: dict[str, float]
    verdict: Literal["pass", "concerns", "fail", "human_resolution_required"]
    wrong_readings: tuple[str, ...] = ()
    responsible_failure_layer: str | None = None
    evidence_refs: tuple[ImmutableRef, ...]
    created_at: datetime

    @model_validator(mode="after")
    def score_range(self) -> "ActivationEvaluationReceipt":
        for key, score in self.dimension_scores.items():
            if not 0 <= score <= 1:
                raise ValueError(f"dimension score {key} must be between 0 and 1")
        if not all(self.gate_results.values()) and self.verdict == "pass":
            raise ValueError("pass verdict cannot contain failed gates")
        return self


class RelationshipActivationState(StrictModel):
    state_id: str
    prospect_id: str
    stage: Literal[
        "unobserved", "observed", "publicly_recognized", "replied",
        "idea_elevated", "micro_committed", "reelcast_proposed",
        "scheduled", "recorded", "asset_delivered", "offer_revealed", "client"
    ]
    source_message_refs: tuple[ImmutableRef, ...] = ()
    last_call_ref: ImmutableRef | None = None
    last_reaction_ref: ImmutableRef | None = None
    next_allowed_transitions: tuple[str, ...]
    smallest_useful_commitment: str | None = None
    wrong_reading_locks: tuple[str, ...] = ()


class ActivativeCall(StrictModel):
    call_id: str
    domain: ActivationDomain
    relationship_state_ref: ImmutableRef | None = None
    interview_asset_contract_ref: ImmutableRef | None = None
    source_refs: tuple[ImmutableRef, ...]
    recognized_premise: str
    edge: str
    target_roles: tuple[str, ...]
    pressure_dose: int = Field(ge=0, le=5)
    call_text: str
    intended_reaction: str
    smallest_useful_commitment: str
    wrong_reading_locks: tuple[str, ...]


class LiveActivativeState(StrictModel):
    state_id: str
    session_id: str
    domain: Literal[ActivationDomain.SOURCE] = ActivationDomain.SOURCE
    active_contract_ref: ImmutableRef
    current_narrative_state: NarrativeState | None = None
    target_narrative_state: NarrativeState
    pressure_dose: int = Field(ge=0, le=5)
    anchor_status: Literal["none", "partial", "hit", "unexpected"]
    recent_call_refs: tuple[ImmutableRef, ...] = ()
    recent_reaction_receipt_refs: tuple[ImmutableRef, ...] = ()
    observed_signals: tuple[str, ...] = ()
    emerging_edges: tuple[str, ...] = ()
    counteractivation_risk: float = Field(ge=0, le=1)
    affinity_reserve: float = Field(ge=0, le=1)
    next_action_candidates: tuple[str, ...] = ()
    stop_conditions: tuple[str, ...] = ()


class AudienceReactionReceipt(StrictModel):
    receipt_id: str
    asset_ref: ImmutableRef
    audience_segment: str
    observed_reactions: tuple[str, ...]
    role_evidence: dict[str, tuple[str, ...]]
    intended_roles: tuple[str, ...]
    wrong_roles: tuple[str, ...] = ()
    counteractivation_evidence: tuple[str, ...] = ()
    quantitative_metrics: dict[str, float] = Field(default_factory=dict)
    epistemic_state: EpistemicState
    operator_resolution_ref: ImmutableRef | None = None
    created_at: datetime


class ActivationFreshnessProfile(StrictModel):
    profile_id: str
    audience_segment: str
    recent_linguistic_patterns: dict[str, int] = Field(default_factory=dict)
    recent_visual_operators: dict[str, int] = Field(default_factory=dict)
    recent_roles: dict[str, int] = Field(default_factory=dict)
    recent_directions: dict[str, int] = Field(default_factory=dict)
    qualitative_fatigue_signals: tuple[str, ...] = ()
    freshness_score: float = Field(ge=0, le=1)
    updated_at: datetime


class CounteractivationProfile(StrictModel):
    profile_id: str
    target_id: str
    desired_roles: tuple[str, ...]
    probable_defense_roles: tuple[str, ...]
    triggers: tuple[str, ...]
    maximum_pressure_dose: int = Field(ge=0, le=5)
    affinity_resets: tuple[str, ...]
    recovery_routes: tuple[str, ...]
    stop_conditions: tuple[str, ...]


class SteeringRecipeCandidate(StrictModel):
    recipe_id: str
    title: str
    implicated_layer: str
    guidance: str
    source_episode_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    counterexample_refs: tuple[ImmutableRef, ...] = ()
    applicability: ApplicabilityEnvelope
    lifecycle_state: Literal[
        "captured", "candidate", "locally_useful", "repeated_evidence",
        "promoted", "deprecated", "superseded"
    ]
    evidence_count: int = Field(ge=1)
    promotion_ref: ImmutableRef | None = None


class JITContextCapsule(StrictModel):
    capsule_id: str
    role: Literal[
        "hunter", "analyst", "composer", "commander",
        "live_assistant", "profile_resolver", "learning_curator"
    ]
    task: str
    object_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    rendered_context: dict[str, Any]
    allowed_actions: tuple[str, ...]
    forbidden_actions: tuple[str, ...]
    output_schema_ref: ImmutableRef
    evaluation_contract_ref: ImmutableRef
    expires_at: datetime | None = None


class VisualSemanticCandidate(StrictModel):
    candidate_id: str
    recognition_intent: str
    recognition_carrier: str
    audience_semiotic_evidence: tuple[ImmutableRef, ...]
    role_activation_map: dict[str, str]
    wrong_reading_locks: tuple[str, ...]
    zero_second_score: float = Field(ge=0, le=1)
    anti_cliche_score: float = Field(ge=0, le=1)
    coach_identity_fit: float = Field(ge=0, le=1)
    audience_fit: float = Field(ge=0, le=1)


class VisualNarrativeBeat(StrictModel):
    beat_id: str
    attention_state: Literal[
        "stimulation", "captivation", "prediction", "payoff",
        "affinity", "anticipation"
    ]
    visual_job: str
    operator_ids: tuple[str, ...]
    recognition_carrier: str
    viewer_action: str
    feature_contract_refs: tuple[ImmutableRef, ...] = ()


class VisualNarrativeProgram(StrictModel):
    program_id: str
    transfer_contract_ref: ImmutableRef
    format_harness: str
    activation_directions: tuple[ActivationDirection, ...]
    viewer_roles: tuple[str, ...]
    pattern_match: str
    pattern_interrupt: str
    beats: tuple[VisualNarrativeBeat, ...] = Field(min_length=1)
    payoff: str
    affinity_mechanism: str | None = None
    anticipation_gap: str | None = None
    wrong_reading_locks: tuple[str, ...]
    no_text_required: bool = False


class FeatureContract(StrictModel):
    contract_id: str
    feature_type: Literal[
        "gaze", "hands", "posture", "witness", "object_punctum",
        "distance", "crop", "light", "negative_space", "contact"
    ]
    subject: str
    execution: str
    activation_job: str
    must_not: tuple[str, ...] = ()
    wrong_reading_blocked: str | None = None


class BBoxIntent(StrictModel):
    component_id: str
    role: str
    first_seen_priority: int = Field(ge=0)
    spatial_requirement: str
    why: str


class CompositionAssetPack(StrictModel):
    pack_id: str
    visual_narrative_program_ref: ImmutableRef
    semantic_candidate_ref: ImmutableRef
    feature_contract_refs: tuple[ImmutableRef, ...]
    tv_route_request: dict[str, Any]
    bbox_intents: tuple[BBoxIntent, ...]
    format_constraints: dict[str, Any]
    text_policy: Literal["none", "minimal", "format_defined"]
    wrong_reading_locks: tuple[str, ...]
    evaluation_contract_ref: ImmutableRef


class RepairProgram(StrictModel):
    repair_id: str
    failure_attribution_ref: ImmutableRef
    frozen_upstream_refs: tuple[ImmutableRef, ...]
    object_to_change_ref: ImmutableRef
    required_change: str
    invalidated_descendant_refs: tuple[ImmutableRef, ...]
    rerun_nodes: tuple[str, ...]
    evaluation_contract_ref: ImmutableRef
    stop_condition: str
