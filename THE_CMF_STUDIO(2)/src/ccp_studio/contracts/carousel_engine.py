from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()

def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"

def reject_16_9(frame_profile: str) -> None:
    if frame_profile and frame_profile.startswith("16:9"):
        raise ValueError("16:9 is source-only and cannot be Carousel delivery")

class CarouselProjectStatus(str, Enum):
    DRAFT="draft"; ACTIVE="active"; APPROVED="approved"; EXPORTED="exported"; ARCHIVED="archived"; FAILED="failed"

class CarouselVariantStatus(str, Enum):
    DRAFT="draft"; SOURCE_READY="source_ready"; SEQUENCE_READY="sequence_ready"; SLIDES_PLANNED="slides_planned"; VISUAL_SYSTEM_LOCKED="visual_system_locked"; COMPOSITIONS_LOCKED="compositions_locked"; LAYERS_READY="layers_ready"; RENDER_READY="render_ready"; RENDERED="rendered"; EVALUATED="evaluated"; APPROVAL_READY="approval_ready"; APPROVED="approved"; EXPORTED="exported"; REVISION_REQUIRED="revision_required"; FAILED="failed"

class SlideRole(str, Enum):
    COVER_HOOK="cover_hook"; CONTEXT_SETUP="context_setup"; PROBLEM_FRAME="problem_frame"; STAKES_SLIDE="stakes_slide"; REFRAME_SLIDE="reframe_slide"; PROOF_SLIDE="proof_slide"; MECHANISM_SLIDE="mechanism_slide"; FRAMEWORK_SLIDE="framework_slide"; EXAMPLE_SLIDE="example_slide"; OBJECTION_SLIDE="objection_slide"; SUMMARY_SLIDE="summary_slide"; SAVE_CARD="save_card"; CTA_SLIDE="cta_slide"

class ViewerState(str, Enum):
    PERCEPTUAL_ENTRY="perceptual_entry"; RELEVANT_OPEN_QUESTION="relevant_open_question"; ACTIVE_PREDICTION="active_prediction"; TRUTHFUL_PAYOFF="truthful_payoff"; HUMAN_AFFINITY="human_affinity"; EXPECTED_FUTURE_VALUE="expected_future_value"

class ClaimType(str, Enum):
    FACTUAL="factual"; INTERPRETIVE="interpretive"; QUOTE="quote"; CTA="cta"; NON_CLAIM="non_claim"

class MatMode(str, Enum):
    DETERMINISTIC="deterministic"; PROVIDER_MATERIALIZED="provider_materialized"

class PassStatus(str, Enum):
    PASS="pass"; PASS_WITH_RISKS="pass_with_risks"; FAIL="fail"

class RevisionCommandType(str, Enum):
    CHANGE_SLIDE_HEADLINE="change_slide_headline"; SWAP_SLIDE_ROLE="swap_slide_role"; REPLACE_PROOF_OBJECT="replace_proof_object"; INCREASE_NEGATIVE_SPACE="increase_negative_space"; CHANGE_STYLE_ROUTE="change_style_route"; SPLIT_DENSE_SLIDE="split_dense_slide"; REMOVE_UNSUPPORTED_CLAIM="remove_unsupported_claim"; MAKE_MORE_EDITORIAL="make_more_editorial"

class SourceRef(BaseModel):
    source_ref_id: str = Field(default_factory=lambda: new_id("source_ref"))
    source_kind: str
    source_id: str | None = None
    quote: str | None = None
    description: str | None = None

class CarouselProject(BaseModel):
    carousel_project_id: str = Field(default_factory=lambda: new_id("carousel_project"))
    brand_id: str
    brand_context_version_id: str
    source_context_refs: list[str]
    primitive_coalition_contract_id: str | None = None
    status: CarouselProjectStatus = CarouselProjectStatus.DRAFT
    variant_ids: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)
    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_id: raise ValueError("CarouselProject.brand_id is required")
        if not self.brand_context_version_id: raise ValueError("CarouselProject.brand_context_version_id is required")
        if not self.source_context_refs: raise ValueError("CarouselProject.source_context_refs are required")

class CarouselVariant(BaseModel):
    carousel_variant_id: str = Field(default_factory=lambda: new_id("carousel_variant"))
    carousel_project_id: str
    brand_id: str
    brand_context_version_id: str
    slide_count: int = 0
    frame_profile: str = "4:5_CAROUSEL_SLIDE"
    sequence_strategy_id: str | None = None
    slide_program_ids: list[str] = Field(default_factory=list)
    render_batch_contract_id: str | None = None
    evaluation_receipt_id: str | None = None
    approval_status: str = "draft"
    export_pack_id: str | None = None
    status: CarouselVariantStatus = CarouselVariantStatus.DRAFT
    created_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)
    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id: raise ValueError("CarouselVariant.brand_context_version_id is required")
        reject_16_9(self.frame_profile)

class CarouselSourceClaim(BaseModel):
    source_claim_id: str = Field(default_factory=lambda: new_id("carousel_claim"))
    claim_text: str
    claim_type: ClaimType = ClaimType.FACTUAL
    source_refs: list[SourceRef] = Field(default_factory=list)
    approved_strategy_ref: str | None = None
    risk_level: str = "normal"
    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.claim_type in {ClaimType.FACTUAL, ClaimType.QUOTE} and not (self.source_refs or self.approved_strategy_ref):
            raise ValueError("Factual/quote carousel claims require source_refs or approved_strategy_ref")

class CarouselSourcePacket(BaseModel):
    carousel_source_packet_id: str = Field(default_factory=lambda: new_id("carousel_source"))
    brand_id: str
    brand_context_version_id: str
    source_context_refs: list[str]
    candidate_claims: list[CarouselSourceClaim]
    proof_points: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    objections: list[str] = Field(default_factory=list)
    frameworks: list[str] = Field(default_factory=list)
    emotional_moments: list[str] = Field(default_factory=list)

class CarouselSequenceStrategy(BaseModel):
    sequence_strategy_id: str = Field(default_factory=lambda: new_id("carousel_strategy"))
    brand_id: str
    brand_context_version_id: str
    source_packet_id: str
    primitive_coalition_contract_id: str | None = None
    carousel_objective: str
    audience_state_before: str
    audience_state_after: str
    viewer_state_sequence: list[ViewerState]
    narrative_arc: str
    slide_count_range: tuple[int, int]
    claim_policy: str
    visual_rhythm_policy: str
    saveability_strategy: str
    cta_strategy: str
    complexity: str = "standard"
    preproduction_depth: str = "standard"
    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.audience_state_before or not self.audience_state_after:
            raise ValueError("CarouselSequenceStrategy requires audience state transition")
        mn, mx = self.slide_count_range
        if mn < 1 or mx < mn or mx > 12: raise ValueError("Invalid Carousel V1 slide_count_range")
        if self.complexity == "complex" and self.preproduction_depth != "full_batch":
            raise ValueError("Complex carousels require full_batch visual preproduction")

class CarouselViewerStateSequence(BaseModel):
    viewer_state_sequence_id: str = Field(default_factory=lambda: new_id("viewer_state_sequence"))
    sequence_strategy_id: str
    states: list[ViewerState]
    slide_state_map: dict[int, ViewerState]
    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.slide_state_map: raise ValueError("Each slide must advance viewer state or earn its place")

class CarouselSlideCountDecision(BaseModel):
    slide_count_decision_id: str = Field(default_factory=lambda: new_id("slide_count"))
    sequence_strategy_id: str
    slide_count: int
    rationale: str
    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.slide_count < 5 or self.slide_count > 12: raise ValueError("Carousel V1 slide count must be 5-12")

class CarouselSlideRoleSpec(BaseModel):
    slide_index: int
    slide_role: SlideRole
    viewer_state_target: ViewerState
    source_claim_requirement: str | None = None
    visual_function: str
    copy_function: str
    asset_requirement: str | None = None
    style_route_constraints: list[str] = Field(default_factory=list)
    repeat_reason: str | None = None

class CarouselSlideRolePlan(BaseModel):
    slide_role_plan_id: str = Field(default_factory=lambda: new_id("slide_role_plan"))
    sequence_strategy_id: str
    slide_roles: list[CarouselSlideRoleSpec]
    def __init__(self, **data: Any):
        super().__init__(**data)
        indexes = [r.slide_index for r in self.slide_roles]
        if indexes != list(range(1, len(indexes)+1)): raise ValueError("Carousel slide indexes must be continuous starting at 1")
        seen = set()
        for role in self.slide_roles:
            if role.slide_role in seen and not role.repeat_reason: raise ValueError("Repeated slide roles require repeat_reason")
            seen.add(role.slide_role)

class CarouselNarrativeArcReport(BaseModel):
    narrative_arc_report_id: str = Field(default_factory=lambda: new_id("narrative_arc"))
    slide_role_plan_id: str
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)

class CarouselClaimMapEntry(BaseModel):
    slide_index: int
    claim: str
    claim_type: ClaimType = ClaimType.FACTUAL
    source_ref_ids: list[str] = Field(default_factory=list)
    supporting_quote: str | None = None
    risk_level: str = "normal"
    allowed_copy_strength: str = "source_faithful"
    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.claim_type == ClaimType.FACTUAL and not self.source_ref_ids:
            raise ValueError("Unsupported factual claim in CarouselClaimMap")

class CarouselClaimMap(BaseModel):
    claim_map_id: str = Field(default_factory=lambda: new_id("claim_map"))
    source_packet_id: str
    entries: list[CarouselClaimMapEntry]

class CarouselCopySystem(BaseModel):
    copy_system_id: str = Field(default_factory=lambda: new_id("copy_system"))
    brand_id: str
    brand_context_version_id: str
    frame_profile: str
    headline_char_budget: int = 70
    support_char_budget: int = 110
    headline_style: str = "sharp_editorial"
    def __init__(self, **data: Any):
        super().__init__(**data)
        reject_16_9(self.frame_profile)

class CarouselSlideBrief(BaseModel):
    slide_brief_id: str = Field(default_factory=lambda: new_id("slide_brief"))
    slide_index: int
    slide_role: SlideRole
    headline_intent: str
    source_claim_refs: list[str] = Field(default_factory=list)
    non_claim_function: bool = False
    visual_directive: str
    asset_needs: list[str] = Field(default_factory=list)
    style_route_constraints: list[str] = Field(default_factory=list)
    composition_density_target: str = "medium"
    reader_action: str | None = None
    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.source_claim_refs and not self.non_claim_function:
            raise ValueError("Every slide brief must reference source claim or declare non_claim_function")

class CarouselSlideCopyPacket(BaseModel):
    slide_copy_packet_id: str = Field(default_factory=lambda: new_id("slide_copy"))
    slide_index: int
    headline: str
    support_line: str | None = None
    headline_char_budget: int = 70
    support_char_budget: int = 110
    def __init__(self, **data: Any):
        super().__init__(**data)
        if len(self.headline) > self.headline_char_budget: raise ValueError("Slide headline exceeds frame profile text budget")
        if self.support_line and len(self.support_line) > self.support_char_budget: raise ValueError("Slide support copy exceeds frame profile text budget")

class CarouselAssetRequirement(BaseModel):
    asset_requirement_id: str = Field(default_factory=lambda: new_id("carousel_asset_req"))
    slide_index: int | None = None
    role: str
    semantic_need: str
    required: bool = True

class CarouselAssetRequirementPlan(BaseModel):
    asset_requirement_plan_id: str = Field(default_factory=lambda: new_id("asset_req_plan"))
    carousel_variant_id: str
    requirements: list[CarouselAssetRequirement]
    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.requirements: raise ValueError("Asset requirements must be explicit before retrieval")

class CarouselAssetCandidateBinding(BaseModel):
    slide_index: int
    asset_id: str
    use_mode: str = "reference_only"
    rights_status: str = "provenance_ready"
    blocked: bool = False
    sequence_reason: str | None = None
    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blocked: raise ValueError("Blocked assets cannot be allocated to carousel slides")
        if self.use_mode == "direct_use" and self.rights_status not in {"provenance_ready", "owned", "brand_provided"}:
            raise ValueError("Unknown-rights assets cannot be direct-use")

class CarouselAssetAllocationPlan(BaseModel):
    asset_allocation_plan_id: str = Field(default_factory=lambda: new_id("asset_allocation"))
    carousel_variant_id: str
    bindings: list[CarouselAssetCandidateBinding]
    def __init__(self, **data: Any):
        super().__init__(**data)
        usage = {}
        for b in self.bindings: usage.setdefault(b.asset_id, []).append(b)
        for asset_id, bindings in usage.items():
            if len(bindings) > 1 and not any(b.sequence_reason for b in bindings):
                raise ValueError("Repeated hero asset requires sequence_reason")

class CarouselVisualSystem(BaseModel):
    visual_system_id: str = Field(default_factory=lambda: new_id("visual_system"))
    carousel_variant_id: str
    motif_system: str
    background_system: str
    type_scale: str
    color_policy: str
    slide_numbering_policy: str
    spacing_rhythm: str
    cross_slide_continuity: str
    locked: bool = True

class CarouselStyleRouteAssignment(BaseModel):
    slide_index: int
    primary_style_route: str
    allowed_route_family: str | None = None
    transition_reason: str | None = None
    def __init__(self, **data: Any):
        super().__init__(**data)
        if any(t in self.primary_style_route for t in ["+", ",", "/"]):
            raise ValueError("No route averaging inside a single provider job")

class CarouselStyleRoutePolicy(BaseModel):
    style_route_policy_id: str = Field(default_factory=lambda: new_id("style_route_policy"))
    carousel_variant_id: str
    assignments: list[CarouselStyleRouteAssignment]

class CarouselSlideCompositionHypothesis(BaseModel):
    composition_hypothesis_id: str = Field(default_factory=lambda: new_id("composition_hypothesis"))
    slide_index: int
    attention_path: str
    copy_placement: str
    asset_placement: str
    negative_space: str
    safe_zone_compliant: bool = True
    mobile_readability_risk: bool = False
    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.safe_zone_compliant: raise ValueError("Composition hypothesis must respect frame profile safe zones")

class CarouselSlideCompositionDecision(BaseModel):
    composition_decision_id: str = Field(default_factory=lambda: new_id("composition_decision"))
    slide_index: int
    selected_hypothesis_id: str
    locked: bool = True
    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.locked: raise ValueError("CarouselSlideCompositionDecision must be locked")

class CarouselSequenceCompositionAudit(BaseModel):
    sequence_composition_audit_id: str = Field(default_factory=lambda: new_id("sequence_audit"))
    carousel_variant_id: str
    pass_status: PassStatus = PassStatus.PASS
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.blockers and self.pass_status == PassStatus.PASS: raise ValueError("Blocking sequence composition failures require fail/pass_with_risks")

class CarouselLayerSpec(BaseModel):
    layer_id: str = Field(default_factory=lambda: new_id("carousel_layer"))
    slide_index: int
    layer_role: str
    materialization_mode: MatMode = MatMode.DETERMINISTIC
    asset_id: str | None = None
    asset_sha256: str | None = None
    text_ref: str | None = None
    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.materialization_mode == MatMode.PROVIDER_MATERIALIZED and not self.asset_sha256:
            raise ValueError("Provider-materialized carousel layers require asset_sha256")

class CarouselSlideLayerPlan(BaseModel):
    slide_layer_plan_id: str = Field(default_factory=lambda: new_id("slide_layer_plan"))
    slide_index: int
    composition_decision_id: str
    layers: list[CarouselLayerSpec]
    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.layers: raise ValueError("CarouselSlideLayerPlan requires layers")

class CarouselProviderJobBlueprint(BaseModel):
    provider_job_blueprint_id: str = Field(default_factory=lambda: new_id("carousel_provider_blueprint"))
    slide_index: int
    source_refs: list[str]
    primary_style_route: str
    frame_profile: str
    composition_role: str
    composition_decision_id: str
    prompt_contract: str
    def __init__(self, **data: Any):
        super().__init__(**data)
        reject_16_9(self.frame_profile)
        if not self.source_refs: raise ValueError("Provider blueprints require source/reference/input refs")
        if any(t in self.primary_style_route for t in ["+", ",", "/"]): raise ValueError("One provider blueprint gets one primary style route")

class CarouselRenderBatchContract(BaseModel):
    render_batch_contract_id: str = Field(default_factory=lambda: new_id("render_batch"))
    carousel_variant_id: str
    frame_profile: str
    slide_count: int
    slide_layer_plan_ids: list[str]
    required_asset_hashes: list[str]
    font_refs: list[str] = Field(default_factory=list)
    texture_refs: list[str] = Field(default_factory=list)
    render_seed: str = "carousel_v1_seed"
    def __init__(self, **data: Any):
        super().__init__(**data)
        reject_16_9(self.frame_profile)
        if self.slide_count != len(self.slide_layer_plan_ids): raise ValueError("Render batch slide count must match layer plans")
        if not self.required_asset_hashes: raise ValueError("Render batch contract requires asset hashes")

class CarouselSlideRenderReceipt(BaseModel):
    slide_render_receipt_id: str = Field(default_factory=lambda: new_id("slide_render_receipt"))
    slide_index: int
    render_batch_contract_id: str
    output_uri: str
    output_sha256: str
    pass_status: PassStatus = PassStatus.PASS

class CarouselPreviewPack(BaseModel):
    carousel_preview_pack_id: str = Field(default_factory=lambda: new_id("preview_pack"))
    carousel_variant_id: str
    slide_receipt_ids: list[str]

class CarouselSequenceEvaluationReceipt(BaseModel):
    sequence_evaluation_receipt_id: str = Field(default_factory=lambda: new_id("sequence_eval"))
    carousel_variant_id: str
    source_fidelity: float = Field(default=0.8, ge=0, le=1)
    claim_support: float = Field(default=0.8, ge=0, le=1)
    sequence_cohesion: float = Field(default=0.8, ge=0, le=1)
    mobile_readability: float = Field(default=0.8, ge=0, le=1)
    style_route_purity: float = Field(default=0.8, ge=0, le=1)
    blockers: list[str] = Field(default_factory=list)
    pass_status: PassStatus = PassStatus.PASS
    def __init__(self, **data: Any):
        super().__init__(**data)
        blockers = set(self.blockers)
        if self.claim_support < .5: blockers.add("unsupported_claim")
        if self.mobile_readability < .5: blockers.add("mobile_readability_failure")
        if self.style_route_purity < .5: blockers.add("style_route_failure")
        if blockers:
            self.blockers = sorted(blockers)
            self.pass_status = PassStatus.FAIL

class CarouselRevisionCommand(BaseModel):
    carousel_revision_command_id: str = Field(default_factory=lambda: new_id("carousel_revision_cmd"))
    command_type: RevisionCommandType
    slide_index: int | None = None
    payload: dict[str, Any] = Field(default_factory=dict)

class CarouselRevisionReceipt(BaseModel):
    carousel_revision_receipt_id: str = Field(default_factory=lambda: new_id("carousel_revision"))
    carousel_variant_id: str
    commands: list[CarouselRevisionCommand]
    requires_re_eval: bool = True

class CarouselVariantComparisonReport(BaseModel):
    carousel_variant_comparison_report_id: str = Field(default_factory=lambda: new_id("carousel_variant_compare"))
    baseline_variant_id: str
    candidate_variant_id: str
    preferred_variant_id: str | None = None
    source_fidelity_delta: float = 0.0
    sequence_cohesion_delta: float = 0.0
    mobile_readability_delta: float = 0.0
    style_route_purity_delta: float = 0.0
    rationale: str = "V1 deterministic comparison placeholder"

class CarouselExportPack(BaseModel):
    carousel_export_pack_id: str = Field(default_factory=lambda: new_id("carousel_export"))
    carousel_variant_id: str
    approval_status: str
    slide_image_uris: list[str]
    alt_text: list[str]
    posting_order: list[int]
    cover_slide_index: int = 1
    caption_seed: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.approval_status != "approved": raise ValueError("Only approved variants can export for publishing")
        if len(self.slide_image_uris) != len(self.posting_order): raise ValueError("Export slides must match posting order")

class CarouselApprovalPacket(BaseModel):
    carousel_approval_packet_id: str = Field(default_factory=lambda: new_id("carousel_approval"))
    carousel_variant_id: str
    evaluation_receipt_id: str
    export_pack_id: str | None = None
    approval_ready: bool = True
    summary: str
