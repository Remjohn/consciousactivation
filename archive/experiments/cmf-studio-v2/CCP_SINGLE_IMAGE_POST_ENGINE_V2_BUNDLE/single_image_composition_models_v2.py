from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, model_validator


class AspectRatio(str, Enum):
    square = "1:1"
    portrait = "4:5"
    story = "9:16"
    landscape = "16:9"


class ReviewStatus(str, Enum):
    draft = "draft"
    routed = "routed"
    assets_pending = "assets_pending"
    rendering = "rendering"
    auto_evaluated = "auto_evaluated"
    awaiting_operator_review = "awaiting_operator_review"
    approved = "approved"
    needs_revision = "needs_revision"
    rejected = "rejected"
    published = "published"


class Bounds(BaseModel):
    x: float = Field(ge=0, le=1)
    y: float = Field(ge=0, le=1)
    w: float = Field(gt=0, le=1)
    h: float = Field(gt=0, le=1)

    @model_validator(mode="after")
    def within_canvas(self) -> "Bounds":
        if self.x + self.w > 1.0001 or self.y + self.h > 1.0001:
            raise ValueError("Bounds extend beyond normalized canvas")
        return self


class CompositionZone(BaseModel):
    id: str
    role: str
    bounds: Bounds
    z_index: int
    required: bool = True
    content_type: str
    alignment: str = "center"


class TextBudget(BaseModel):
    headline_words_max: Optional[int] = None
    support_words_max: Optional[int] = None
    body_words_max: Optional[int] = None
    option_words_max: Optional[int] = None
    caption_words_per_panel: Optional[int] = None
    bullet_lines_per_side: Optional[int] = None
    stat_chips_max: Optional[int] = None
    metadata_lines_max: Optional[int] = None


class RoughNotationContract(BaseModel):
    allowed: List[str] = Field(default_factory=list)
    max_annotations: int = Field(default=0, ge=0, le=4)


class MicroSemioticAnchorSlot(BaseModel):
    slot: str
    prominence: Literal["subtle", "visible_but_secondary", "visible"]


class CanonicalSingleImageCompositionV2(BaseModel):
    schema_id: str
    composition_id: str
    version: str
    family: str
    semantic_intent: str
    layout_template_id: str
    compatible_archetypes: List[str]
    compatible_derivatives: List[str]
    compatible_meme_mechanisms: List[str] = Field(default_factory=list)
    compatible_reaction_archetypes: List[str] = Field(default_factory=list)
    content_shapes: List[str]
    format_support: List[AspectRatio]
    text_budget: TextBudget
    provider_mode: str
    micro_semiotic_anchor_slots: List[MicroSemioticAnchorSlot] = Field(default_factory=list)
    rough_notation_contract: RoughNotationContract
    evaluation_profile_id: str
    visual_energy: str
    visual_density: str
    zones: List[CompositionZone]
    notes: List[str] = Field(default_factory=list)


class SingleImageEngineInput(BaseModel):
    organization_id: str
    brand_id: str
    brand_context_version_id: str
    registry_bundle_version: str
    source_expression_session_id: Optional[str] = None
    source_expression_moment_id: Optional[str] = None
    interview_asset_contract_id: Optional[str] = None
    content_archetype_id: str
    asset_derivative_id: str
    meme_mechanism_id: Optional[str] = None
    reaction_archetype_id: Optional[str] = None
    expression_state: Optional[str] = None
    primitive_evaluations: Dict[str, float] = Field(default_factory=dict)
    doctrines: List[str] = Field(default_factory=list)
    target_platform: str
    target_aspect_ratio: AspectRatio
    content_shape: str
    headline: str
    support_text: Optional[str] = None
    body_text: Optional[str] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    panel_captions: List[str] = Field(default_factory=list)
    verified_quotes: List[str] = Field(default_factory=list)
    verified_stats: List[Dict[str, Any]] = Field(default_factory=list)
    approved_asset_ids: List[str] = Field(default_factory=list)
    micro_semiotic_anchor_candidates: List[str] = Field(default_factory=list)


class CompositionCandidateScore(BaseModel):
    composition_id: str
    total_score: float = Field(ge=0, le=1)
    component_scores: Dict[str, float]
    penalties: Dict[str, float] = Field(default_factory=dict)
    hard_constraint_failures: List[str] = Field(default_factory=list)
    explanation: str


class CompositionRouterDecision(BaseModel):
    request_id: str
    selected_composition_id: str
    candidates: List[CompositionCandidateScore]
    operator_override: bool = False
    override_reason: Optional[str] = None


class TextElement(BaseModel):
    id: str
    zone_id: str
    role: str
    text: str
    font_token: str
    color_token: str
    max_lines: int
    alignment: str
    emphasis_spans: List[Dict[str, Any]] = Field(default_factory=list)


class VisualAssetPlacement(BaseModel):
    id: str
    zone_id: str
    asset_id: str
    asset_role: str
    fit: str = "cover"
    focal_point: Optional[Dict[str, float]] = None
    mask_asset_id: Optional[str] = None
    layer_manifest_id: Optional[str] = None


class AnnotationSpec(BaseModel):
    id: str
    target_element_id: str
    annotation_type: str
    color_token: str
    roughness: float = Field(default=1.0, ge=0, le=3)
    seed: int


class MicroSemioticAnchorPlacement(BaseModel):
    anchor_asset_id: str
    slot: str
    zone_id: str
    prominence: str
    purpose: str
    legal_status: str = "approved"


class ProviderJobSpec(BaseModel):
    provider: str
    task_type: str
    input_contract: Dict[str, Any]
    model_version: str
    seed: Optional[int] = None
    output_asset_roles: List[str]
    approval_required: bool = True


class SingleImageSceneSpecV2(BaseModel):
    scene_spec_id: str
    input_context_hash: str
    brand_context_version_id: str
    registry_bundle_version: str
    composition_id: str
    aspect_ratio: AspectRatio
    canvas_width: int
    canvas_height: int
    background_token: str
    text_elements: List[TextElement]
    visual_assets: List[VisualAssetPlacement]
    annotations: List[AnnotationSpec] = Field(default_factory=list)
    micro_semiotic_anchors: List[MicroSemioticAnchorPlacement] = Field(default_factory=list)
    provider_jobs: List[ProviderJobSpec] = Field(default_factory=list)
    evaluation_profile_id: str


class SkiaRenderReceipt(BaseModel):
    render_id: str
    scene_spec_id: str
    renderer_version: str
    font_manifest_hash: str
    asset_hashes: Dict[str, str]
    scene_spec_hash: str
    output_uri: str
    output_sha256: str
    duration_ms: int


class SingleImageEvaluationReceiptV2(BaseModel):
    receipt_id: str
    render_id: str
    composition_id: str
    dimension_scores: Dict[str, float]
    hard_failures: List[str] = Field(default_factory=list)
    overall_score: float = Field(ge=0, le=1)
    suggested_repairs: List[Dict[str, Any]] = Field(default_factory=list)
    operator_status: Literal["approved", "needs_revision", "rejected"]
    operator_notes: Optional[str] = None


class SingleImageProductionRecord(BaseModel):
    input: SingleImageEngineInput
    router_decision: CompositionRouterDecision
    scene_spec: SingleImageSceneSpecV2
    render_receipt: Optional[SkiaRenderReceipt] = None
    evaluation_receipt: Optional[SingleImageEvaluationReceiptV2] = None
    status: ReviewStatus = ReviewStatus.draft
