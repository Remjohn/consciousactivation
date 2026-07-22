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


class AssetKind(str, Enum):
    SOURCE_PHOTO = "source_photo"
    SOURCE_VIDEO = "source_video"
    SOURCE_AUDIO = "source_audio"
    SOURCE_DOCUMENT = "source_document"
    SCREENSHOT = "screenshot"
    TRANSCRIPT_SPAN = "transcript_span"
    PROOF_OBJECT = "proof_object"
    MEMORY_OBJECT = "memory_object"
    MICRO_SEMIOTIC_ANCHOR = "micro_semiotic_anchor"
    BRAND_IDENTITY_ASSET = "brand_identity_asset"
    AVATAR_ASSET = "avatar_asset"
    ACTING_REFERENCE = "acting_reference"
    PAPER_CUT_ARTIFACT = "paper_cut_artifact"
    PAPER_TEXTURE = "paper_texture"
    COMPOSITION_REFERENCE = "composition_reference"
    STYLE_REFERENCE = "style_reference"
    VISUAL_REFERENCE = "visual_reference"
    BROLL_REFERENCE = "broll_reference"
    SFX_ASSET = "sfx_asset"
    MOTION_RECIPE = "motion_recipe"
    PROVIDER_GENERATED_IMAGE = "provider_generated_image"
    PROVIDER_GENERATED_LAYER = "provider_generated_layer"
    MASK = "mask"
    CUTOUT = "cutout"
    RENDER_OUTPUT = "render_output"
    CAROUSEL_SLIDE_OUTPUT = "carousel_slide_output"
    VIDEO_INSERT_OUTPUT = "video_insert_output"


class AssetOrigin(str, Enum):
    BRAND_UPLOADED = "brand_uploaded"
    GUEST_UPLOADED = "guest_uploaded"
    INTERVIEW_CAPTURED = "interview_captured"
    TRANSCRIPT_DERIVED = "transcript_derived"
    VISUAL_RESEARCH_CANDIDATE = "visual_research_candidate"
    CREATIVE_LIBRARY_ITEM = "creative_library_item"
    ACTING_LIBRARY_ITEM = "acting_library_item"
    PROVIDER_GENERATED = "provider_generated"
    PROVIDER_EDITED = "provider_edited"
    PROVIDER_SEGMENTED = "provider_segmented"
    DETERMINISTIC_RENDER = "deterministic_render"
    OPERATOR_IMPORTED = "operator_imported"
    LEGACY_IMPORTED = "legacy_imported"
    PUBLIC_REFERENCE = "public_reference"
    STOCK_REFERENCE = "stock_reference"


class AssetStatus(str, Enum):
    INGESTED = "ingested"
    FINGERPRINTED = "fingerprinted"
    NEEDS_RIGHTS_REVIEW = "needs_rights_review"
    RIGHTS_BLOCKED = "rights_blocked"
    NEEDS_CLASSIFICATION = "needs_classification"
    NEEDS_EVALUATION = "needs_evaluation"
    CANDIDATE = "candidate"
    APPROVED = "approved"
    LOCKED = "locked"
    REFERENCE_ONLY = "reference_only"
    ACTIVE = "active"
    FATIGUED = "fatigued"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    BLOCKED = "blocked"


class AssetUseMode(str, Enum):
    DIRECT_USE = "direct_use"
    REFERENCE_ONLY = "reference_only"
    COMPOSITION_REFERENCE_ONLY = "composition_reference_only"
    STYLE_REFERENCE_ONLY = "style_reference_only"
    PROVIDER_INPUT_ONLY = "provider_input_only"
    OPERATOR_REVIEW_REQUIRED = "operator_review_required"
    BLOCKED = "blocked"


class RightsTier(str, Enum):
    OWNED = "owned"
    BRAND_PROVIDED = "brand_provided"
    GUEST_PROVIDED = "guest_provided"
    PUBLIC_DOMAIN = "public_domain"
    ROYALTY_FREE = "royalty_free"
    EDITORIAL_REVIEW = "editorial_review"
    REFERENCE_ONLY = "reference_only"
    UNKNOWN = "unknown"
    RESTRICTED = "restricted"
    BLOCKED = "blocked"


class ReviewStatus(str, Enum):
    PENDING = "pending"
    PROVENANCE_READY = "provenance_ready"
    NEEDS_OPERATOR_REVIEW = "needs_operator_review"
    BLOCKED = "blocked"


class AssetClass(str, Enum):
    PERSON = "person"
    FACE = "face"
    BODY = "body"
    GESTURE = "gesture"
    OBJECT = "object"
    DOCUMENT = "document"
    ROOM = "room"
    LANDSCAPE = "landscape"
    SCREEN = "screen"
    DEVICE = "device"
    VEHICLE = "vehicle"
    FOOD = "food"
    CLOTHING = "clothing"
    TEXTURE = "texture"
    TYPOGRAPHY = "typography"
    DIAGRAM = "diagram"
    SCREENSHOT = "screenshot"
    AUDIO = "audio"
    MOTION = "motion"
    RENDER = "render"


class AssetRole(str, Enum):
    HERO_VISUAL = "hero_visual"
    PROOF_OBJECT = "proof_object"
    MEMORY_ANCHOR = "memory_anchor"
    IDENTITY_ANCHOR = "identity_anchor"
    MICRO_SEMIOTIC_ANCHOR = "micro_semiotic_anchor"
    STYLE_REFERENCE = "style_reference"
    COMPOSITION_REFERENCE = "composition_reference"
    BACKGROUND = "background"
    FOREGROUND_OBJECT = "foreground_object"
    PAPER_CUT_OBJECT = "paper_cut_object"
    BROLL_REFERENCE = "broll_reference"
    AVATAR_REFERENCE = "avatar_reference"
    REACTION_SURFACE = "reaction_surface"
    UI_SURFACE = "ui_surface"
    TEXTURE_LAYER = "texture_layer"
    CAPTION_BACKGROUND = "caption_background"


class ProductionRole(str, Enum):
    SOURCE_EVIDENCE = "source_evidence"
    DIRECT_VISUAL = "direct_visual"
    REFERENCE_VISUAL = "reference_visual"
    PROVIDER_INPUT = "provider_input"
    CUTOUT_SOURCE = "cutout_source"
    MASK_SOURCE = "mask_source"
    LAYER_SOURCE = "layer_source"
    RENDER_OUTPUT = "render_output"
    TRAINING_REFERENCE = "training_reference"
    OPERATOR_REFERENCE = "operator_reference"


class RequestingComponent(str, Enum):
    SUPERVISUAL = "supervisual"
    CAROUSEL = "carousel"
    VIDEO = "video"
    VISUAL_PREPRODUCTION = "visual_preproduction"
    STYLE_ROUTE = "style_route"
    PAPER_CUT = "paper_cut"
    CHARACTER = "character"
    PROVIDER_ORCHESTRATION = "provider_orchestration"


class EvaluationScope(str, Enum):
    INTRINSIC = "intrinsic"
    CONTEXTUAL = "contextual"


class SourceRef(BaseModel):
    source_ref_id: str = Field(default_factory=lambda: new_id("source_ref"))
    source_kind: str
    source_id: str | None = None
    description: str | None = None


class AssetSource(BaseModel):
    asset_source_id: str = Field(default_factory=lambda: new_id("asset_source"))
    origin: AssetOrigin
    source_refs: list[SourceRef] = Field(default_factory=list)
    notes: str | None = None


class RightsProvenanceProfile(BaseModel):
    rights_profile_id: str = Field(default_factory=lambda: new_id("rights"))
    asset_id: str
    rights_tier: RightsTier = RightsTier.UNKNOWN
    direct_use_allowed: bool = False
    reference_use_allowed: bool = True
    composition_reference_allowed: bool = True
    style_reference_allowed: bool = True
    provider_input_allowed: bool = False
    attribution_required: bool = False
    commercial_use_allowed: bool = False
    identity_sensitive: bool = False
    known_person_sensitive: bool = False
    minor_sensitive: bool = False
    restricted_terms: list[str] = Field(default_factory=list)
    provenance_summary: str | None = None
    reviewer_actor_id: str | None = None
    review_status: ReviewStatus = ReviewStatus.PENDING
    evidence_refs: list[str] = Field(default_factory=list)
    decided_at: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.rights_tier in {RightsTier.UNKNOWN, RightsTier.RESTRICTED, RightsTier.BLOCKED, RightsTier.REFERENCE_ONLY} and self.direct_use_allowed:
            raise ValueError(f"{self.rights_tier.value} assets cannot be marked direct_use_allowed")
        if self.rights_tier == RightsTier.BLOCKED and self.review_status != ReviewStatus.BLOCKED:
            raise ValueError("blocked rights tier must use blocked review_status")

    def allows(self, use_mode: AssetUseMode) -> bool:
        if self.rights_tier in {RightsTier.RESTRICTED, RightsTier.BLOCKED} or self.review_status == ReviewStatus.BLOCKED:
            return False
        if use_mode == AssetUseMode.DIRECT_USE:
            return self.direct_use_allowed and self.review_status == ReviewStatus.PROVENANCE_READY
        if use_mode == AssetUseMode.REFERENCE_ONLY:
            return self.reference_use_allowed
        if use_mode == AssetUseMode.COMPOSITION_REFERENCE_ONLY:
            return self.composition_reference_allowed
        if use_mode == AssetUseMode.STYLE_REFERENCE_ONLY:
            return self.style_reference_allowed
        if use_mode == AssetUseMode.PROVIDER_INPUT_ONLY:
            return self.provider_input_allowed
        if use_mode == AssetUseMode.OPERATOR_REVIEW_REQUIRED:
            return True
        return False


class AssetVersion(BaseModel):
    asset_version_id: str = Field(default_factory=lambda: new_id("asset_version"))
    asset_id: str
    sha256: str
    uri: str | None = None
    mime_type: str | None = None
    width: int | None = None
    height: int | None = None
    duration_seconds: float | None = None
    byte_size: int | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.sha256 or not self.sha256.strip():
            raise ValueError("AssetVersion.sha256 is required")


class AssetClassification(BaseModel):
    classification_id: str = Field(default_factory=lambda: new_id("asset_classification"))
    asset_id: str
    asset_classes: list[AssetClass] = Field(default_factory=list)
    asset_roles: list[AssetRole] = Field(default_factory=list)
    production_roles: list[ProductionRole] = Field(default_factory=list)
    ingredient_kinds: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.75, ge=0.0, le=1.0)
    classifier: str = "asset_intelligence_v1"


class AssetSemanticProfile(BaseModel):
    semantic_profile_id: str = Field(default_factory=lambda: new_id("asset_semantic"))
    asset_id: str
    literal_description: str
    recognizable_objects: list[str] = Field(default_factory=list)
    human_context: str | None = None
    setting_context: str | None = None
    cultural_context: str | None = None
    time_period_signal: str | None = None
    emotional_signal: list[str] = Field(default_factory=list)
    status_signal: str | None = None
    familiarity_signal: str | None = None
    proof_signal: str | None = None
    memory_signal: str | None = None
    visual_density: float = Field(default=0.5, ge=0.0, le=1.0)
    attention_gravity: float = Field(default=0.5, ge=0.0, le=1.0)
    primitive_affinities: list[str] = Field(default_factory=list)
    negative_space_risks: list[str] = Field(default_factory=list)
    forbidden_interpretations: list[str] = Field(default_factory=list)
    best_use_cases: list[str] = Field(default_factory=list)
    bad_use_cases: list[str] = Field(default_factory=list)


class AssetRecord(BaseModel):
    asset_id: str = Field(default_factory=lambda: new_id("asset"))
    organization_id: str | None = None
    brand_id: str
    brand_context_version_id: str | None = None
    asset_kind: AssetKind
    asset_origin: AssetOrigin
    asset_status: AssetStatus = AssetStatus.INGESTED
    display_name: str
    description: str | None = None
    source_refs: list[SourceRef] = Field(default_factory=list)
    rights_profile_id: str | None = None
    current_version_id: str | None = None
    classification_id: str | None = None
    semantic_profile_id: str | None = None
    primitive_binding_refs: list[str] = Field(default_factory=list)
    style_route_affinities: list[str] = Field(default_factory=list)
    frame_profile_affinities: list[str] = Field(default_factory=list)
    composition_role_affinities: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)
    updated_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_id:
            raise ValueError("AssetRecord.brand_id is required")


class CreativeIngredient(BaseModel):
    creative_ingredient_id: str = Field(default_factory=lambda: new_id("ingredient"))
    brand_id: str
    brand_context_version_id: str | None = None
    ingredient_kind: str
    display_name: str
    source_asset_ids: list[str] = Field(default_factory=list)
    source_refs: list[SourceRef] = Field(default_factory=list)
    semantic_need: str | None = None
    primitive_binding_refs: list[str] = Field(default_factory=list)
    compatible_style_routes: list[str] = Field(default_factory=list)
    compatible_frame_profiles: list[str] = Field(default_factory=list)
    composition_role_affinities: list[str] = Field(default_factory=list)
    use_modes: list[AssetUseMode] = Field(default_factory=lambda: [AssetUseMode.REFERENCE_ONLY])
    status: str = "candidate"


class CreativeIngredientVariant(BaseModel):
    variant_id: str = Field(default_factory=lambda: new_id("ingredient_variant"))
    creative_ingredient_id: str
    asset_id: str
    source_asset_version_id: str | None = None
    variant_asset_version_id: str
    variant_kind: str
    provider_job_receipt_id: str | None = None
    render_receipt_id: str | None = None
    transformation_summary: str | None = None
    created_at: str = Field(default_factory=_now_iso)


class VisualIngredientRequirement(BaseModel):
    visual_ingredient_requirement_id: str = Field(default_factory=lambda: new_id("visual_req"))
    requesting_component: RequestingComponent
    brand_id: str
    brand_context_version_id: str
    ingredient_kind: str
    semantic_need: str
    required_asset_roles: list[AssetRole] = Field(default_factory=list)
    acceptable_use_modes: list[AssetUseMode] = Field(default_factory=lambda: [AssetUseMode.DIRECT_USE, AssetUseMode.REFERENCE_ONLY])
    style_route: str | None = None
    frame_profile: str | None = None
    composition_role: str | None = None
    primitive_coalition_contract_id: str | None = None
    source_truth_refs: list[str] = Field(default_factory=list)
    is_required: bool = True


class AssetRetrievalQuery(BaseModel):
    retrieval_query_id: str = Field(default_factory=lambda: new_id("asset_query"))
    brand_id: str
    brand_context_version_id: str
    requesting_component: RequestingComponent
    visual_ingredient_requirement_id: str | None = None
    desired_asset_roles: list[AssetRole] = Field(default_factory=list)
    required_use_mode: AssetUseMode = AssetUseMode.REFERENCE_ONLY
    allowed_asset_kinds: list[AssetKind] = Field(default_factory=list)
    style_route: str | None = None
    frame_profile: str | None = None
    composition_role: str | None = None
    primitive_coalition_contract_id: str | None = None
    visual_schema_id: str | None = None
    source_truth_refs: list[str] = Field(default_factory=list)
    avoid_asset_ids: list[str] = Field(default_factory=list)
    include_reference_only: bool = True
    max_candidates: int = 12


class AssetCandidateMatch(BaseModel):
    candidate_match_id: str = Field(default_factory=lambda: new_id("asset_match"))
    asset_id: str
    asset_version_id: str | None = None
    creative_ingredient_id: str | None = None
    use_mode: AssetUseMode
    rights_status: ReviewStatus
    semantic_match_score: float = Field(default=0.5, ge=0.0, le=1.0)
    primitive_fit_score: float = Field(default=0.5, ge=0.0, le=1.0)
    visual_schema_fit_score: float = Field(default=0.5, ge=0.0, le=1.0)
    style_route_fit_score: float = Field(default=0.5, ge=0.0, le=1.0)
    frame_profile_fit_score: float = Field(default=0.5, ge=0.0, le=1.0)
    composition_role_fit_score: float = Field(default=0.5, ge=0.0, le=1.0)
    freshness_score: float = Field(default=0.5, ge=0.0, le=1.0)
    fatigue_risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    total_score: float = Field(default=0.5, ge=0.0, le=1.0)
    blocker_codes: list[str] = Field(default_factory=list)
    rationale: str | None = None


class MissingIngredientGap(BaseModel):
    gap_id: str = Field(default_factory=lambda: new_id("asset_gap"))
    required_role: AssetRole | None = None
    ingredient_kind: str | None = None
    semantic_need: str
    severity: str = "blocking"
    recommendation: str | None = None


class VisualReferenceBoard(BaseModel):
    reference_board_id: str = Field(default_factory=lambda: new_id("ref_board"))
    brand_id: str
    brand_context_version_id: str
    requesting_component: RequestingComponent
    query_id: str | None = None
    candidate_matches: list[AssetCandidateMatch] = Field(default_factory=list)
    grouped_asset_ids: dict[str, list[str]] = Field(default_factory=dict)
    missing_gaps: list[MissingIngredientGap] = Field(default_factory=list)
    operator_notes: str | None = None
    created_at: str = Field(default_factory=_now_iso)


class AssetEvaluationReceipt(BaseModel):
    evaluation_receipt_id: str = Field(default_factory=lambda: new_id("asset_eval"))
    asset_id: str
    scope: EvaluationScope
    requesting_component: RequestingComponent | None = None
    context_ref: str | None = None
    technical_quality: float = Field(default=0.5, ge=0.0, le=1.0)
    source_quality: float = Field(default=0.5, ge=0.0, le=1.0)
    provenance_quality: float = Field(default=0.5, ge=0.0, le=1.0)
    recognition_clarity: float = Field(default=0.5, ge=0.0, le=1.0)
    semantic_strength: float = Field(default=0.5, ge=0.0, le=1.0)
    primitive_fit: float | None = Field(default=None, ge=0.0, le=1.0)
    visual_schema_fit: float | None = Field(default=None, ge=0.0, le=1.0)
    style_route_fit: float | None = Field(default=None, ge=0.0, le=1.0)
    frame_profile_fit: float | None = Field(default=None, ge=0.0, le=1.0)
    composition_role_fit: float | None = Field(default=None, ge=0.0, le=1.0)
    source_truth_fit: float | None = Field(default=None, ge=0.0, le=1.0)
    brand_context_fit: float | None = Field(default=None, ge=0.0, le=1.0)
    audience_recognition_fit: float | None = Field(default=None, ge=0.0, le=1.0)
    freshness_fit: float | None = Field(default=None, ge=0.0, le=1.0)
    fatigue_risk: float | None = Field(default=None, ge=0.0, le=1.0)
    pass_status: str = "pass"
    blocker_codes: list[str] = Field(default_factory=list)
    rationale: str | None = None
    created_at: str = Field(default_factory=_now_iso)


class AssetUsageReceipt(BaseModel):
    usage_receipt_id: str = Field(default_factory=lambda: new_id("asset_usage"))
    asset_id: str
    asset_version_id: str | None = None
    creative_ingredient_id: str | None = None
    brand_id: str
    brand_context_version_id: str
    requesting_component: RequestingComponent
    output_ref: str | None = None
    project_ref: str | None = None
    scene_ref: str | None = None
    beat_ref: str | None = None
    timeline_range: tuple[float, float] | None = None
    composition_role: str | None = None
    style_route: str | None = None
    frame_profile: str | None = None
    primitive_coalition_contract_id: str | None = None
    used_as: AssetUseMode = AssetUseMode.REFERENCE_ONLY
    created_at: str = Field(default_factory=_now_iso)


class AssetPerformanceMemory(BaseModel):
    performance_memory_id: str = Field(default_factory=lambda: new_id("asset_perf"))
    asset_id: str
    brand_id: str
    platform: str | None = None
    output_ref: str | None = None
    impressions: int | None = None
    views: int | None = None
    saves: int | None = None
    shares: int | None = None
    comments: int | None = None
    completion_rate: float | None = Field(default=None, ge=0.0, le=1.0)
    engagement_rate: float | None = Field(default=None, ge=0.0, le=1.0)
    qualitative_notes: str | None = None
    performance_score: float = Field(default=0.0, ge=0.0, le=1.0)
    created_at: str = Field(default_factory=_now_iso)


class AssetFatigueRecord(BaseModel):
    fatigue_record_id: str = Field(default_factory=lambda: new_id("asset_fatigue"))
    asset_id: str
    brand_id: str
    usage_count: int = 0
    recent_usage_count: int = 0
    fatigue_score: float = Field(default=0.0, ge=0.0, le=1.0)
    status_recommendation: AssetStatus = AssetStatus.ACTIVE
    rationale: str | None = None
    created_at: str = Field(default_factory=_now_iso)


class WinningAssetRecord(BaseModel):
    winning_asset_record_id: str = Field(default_factory=lambda: new_id("asset_winner"))
    asset_id: str
    brand_id: str
    promoted_by_actor_id: str | None = None
    evidence_receipt_ids: list[str] = Field(default_factory=list)
    performance_score: float = Field(default=0.0, ge=0.0, le=1.0)
    winning_pattern_summary: str | None = None
    approved: bool = False
    created_at: str = Field(default_factory=_now_iso)
