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


class RequestingComponent(str, Enum):
    SUPERVISUAL = "supervisual"
    CAROUSEL = "carousel"
    VIDEO = "video"
    VISUAL_PREPRODUCTION = "visual_preproduction"
    STYLE_ROUTE = "style_route"
    PAPER_CUT = "paper_cut"
    CHARACTER = "character"


class StyleRouteId(str, Enum):
    CAC_CONSCIOUS_AMBIENT_CINEMA = "CAC_CONSCIOUS_AMBIENT_CINEMA"
    GMG_EXPERT_01_NEO_SCHEMATIC_ARCHITECT = "GMG_EXPERT_01_NEO_SCHEMATIC_ARCHITECT"
    GMG_EXPERT_02_MONO_KINETIC_PROTAGONIST = "GMG_EXPERT_02_MONO_KINETIC_PROTAGONIST"
    GMG_EXPERT_03_EMOTIONAL_ANIMATOR = "GMG_EXPERT_03_EMOTIONAL_ANIMATOR"
    GMG_EXPERT_04_PAPER_ARCHITECT = "GMG_EXPERT_04_PAPER_ARCHITECT"
    GMG_EXPERT_05_EDITORIAL_SCRIBE = "GMG_EXPERT_05_EDITORIAL_SCRIBE"
    GMG_EXPERT_06_VISUAL_SYNTHESIZER = "GMG_EXPERT_06_VISUAL_SYNTHESIZER"
    PAPER_CUT_EDITORIAL = "PAPER_CUT_EDITORIAL"
    PAPER_CUT_ARTIFACT = "PAPER_CUT_ARTIFACT"
    DOCUMENTARY_PROOF = "DOCUMENTARY_PROOF"
    UI_REACTION_SURFACE = "UI_REACTION_SURFACE"
    AVATAR_PERFORMANCE_LAYER = "AVATAR_PERFORMANCE_LAYER"
    DETERMINISTIC_SKIA_CARD = "DETERMINISTIC_SKIA_CARD"


class StyleRouteFamily(str, Enum):
    REAL_CINEMATIC = "real_cinematic"
    GMG = "gmg"
    PAPER_CUT = "paper_cut"
    EVIDENCE_INTERFACE_AVATAR = "evidence_interface_avatar"
    DETERMINISTIC = "deterministic"


class SourceGroundingMode(str, Enum):
    DIRECT_REAL_REFERENCE = "direct_real_reference"
    COMPOSITE_REAL_REFERENCES = "composite_real_references"
    STYLE_REFERENCE_ONLY = "style_reference_only"
    SOURCE_LANGUAGE_REFERENCE = "source_language_reference"
    ABSTRACT_SYMBOLIC_EXCEPTION = "abstract_symbolic_exception"
    DETERMINISTIC_ASSET_ONLY = "deterministic_asset_only"


class TargetOutputType(str, Enum):
    STILL_IMAGE = "still_image"
    IMAGE_LAYER = "image_layer"
    MOTION_INSERT = "motion_insert"
    BROLL_CLIP = "broll_clip"
    PROVIDER_BLUEPRINT = "provider_blueprint"
    SKIA_RENDER = "skia_render"
    SOURCE_REFERENCE = "source_reference"


class ProviderCapability(str, Enum):
    IDEOGRAM_4 = "ideogram_4"
    GPT_IMAGE = "gpt_image"
    FLUX = "flux"
    QWEN_IMAGE_LAYERED = "qwen_image_layered"
    SAM3 = "sam3"
    SKIA = "skia"
    REMOTION = "remotion"
    MOTION_CANVAS = "motion_canvas"
    FAKE_PROVIDER = "fake_provider"


class RouteStatus(str, Enum):
    DRAFT = "draft"
    PRECONDITIONS_FAILED = "preconditions_failed"
    SELECTED = "selected"
    PRODUCTION_SPEC_COMPILED = "production_spec_compiled"
    PROVIDER_BLUEPRINT_COMPILED = "provider_blueprint_compiled"
    EVALUATED = "evaluated"
    REPAIR_REQUIRED = "repair_required"
    APPROVED = "approved"
    BLOCKED = "blocked"


class PassStatus(str, Enum):
    PASS = "pass"
    PASS_WITH_RISKS = "pass_with_risks"
    FAIL = "fail"


class CompositionRole(str, Enum):
    BACKGROUND_PLATE = "background_plate"
    HERO_VISUAL = "hero_visual"
    PROOF_OBJECT = "proof_object"
    MEMORY_ANCHOR = "memory_anchor"
    PAPER_CUT_OBJECT = "paper_cut_object"
    FOREGROUND_INSERT = "foreground_insert"
    DIAGRAM_LAYER = "diagram_layer"
    AVATAR_LAYER = "avatar_layer"
    UI_SURFACE = "ui_surface"
    TEXTURE_LAYER = "texture_layer"
    TYPOGRAPHY_LAYER = "typography_layer"


class SourceReference(BaseModel):
    source_reference_id: str = Field(default_factory=lambda: new_id("style_source"))
    source_kind: str
    source_id: str | None = None
    description: str | None = None
    is_real_life_reference: bool = False


class AssetReference(BaseModel):
    asset_ref_id: str = Field(default_factory=lambda: new_id("style_asset_ref"))
    asset_id: str
    creative_ingredient_id: str | None = None
    use_mode: str = "reference_only"
    source_reference_ids: list[str] = Field(default_factory=list)
    asset_role: str | None = None
    direct_use_allowed: bool = False


class StyleRouteDecisionRequest(BaseModel):
    style_route_decision_request_id: str = Field(default_factory=lambda: new_id("style_route_request"))
    brand_id: str
    brand_context_version_id: str
    requesting_component: RequestingComponent
    visual_preproduction_packet_id: str | None = None
    visual_schema_id: str | None = None
    visual_beat_plan_id: str | None = None
    primitive_coalition_contract_id: str | None = None
    asset_candidate_refs: list[AssetReference] = Field(default_factory=list)
    reference_board_id: str | None = None
    frame_profile: str
    composition_role: CompositionRole
    target_output_type: TargetOutputType
    source_grounding_mode: SourceGroundingMode
    source_references: list[SourceReference] = Field(default_factory=list)
    operator_route_hint: StyleRouteId | None = None
    forbidden_routes: list[StyleRouteId] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("StyleRouteDecisionRequest.brand_context_version_id is required")


class StyleRoutePreconditionReport(BaseModel):
    style_route_precondition_report_id: str = Field(default_factory=lambda: new_id("style_precondition"))
    request_id: str
    route_id: StyleRouteId
    required_inputs: list[str] = Field(default_factory=list)
    present_inputs: list[str] = Field(default_factory=list)
    missing_inputs: list[str] = Field(default_factory=list)
    violations: list[str] = Field(default_factory=list)
    source_grounding_valid: bool = True
    provider_ready: bool = False
    pass_status: PassStatus = PassStatus.PASS

    def __init__(self, **data: Any):
        super().__init__(**data)
        if (self.missing_inputs or self.violations or not self.source_grounding_valid) and self.pass_status == PassStatus.PASS:
            raise ValueError("precondition failures require pass_status to be pass_with_risks or fail")
        if self.provider_ready and (self.missing_inputs or self.violations or self.pass_status == PassStatus.FAIL):
            raise ValueError("provider_ready cannot be true with missing inputs, violations, or failed status")


class StyleRouteDecision(BaseModel):
    style_route_decision_id: str = Field(default_factory=lambda: new_id("style_route_decision"))
    request_id: str
    selected_route_id: StyleRouteId
    route_family: StyleRouteFamily
    confidence: float = Field(default=0.75, ge=0.0, le=1.0)
    decision_rationale: str
    source_grounding_mode: SourceGroundingMode
    required_inputs: list[str] = Field(default_factory=list)
    missing_inputs: list[str] = Field(default_factory=list)
    compatible_provider_capabilities: list[ProviderCapability] = Field(default_factory=list)
    frame_profile_compatibility: bool = True
    composition_role_compatibility: bool = True
    precondition_report_id: str | None = None
    provider_ready: bool = False
    accepted_risks: list[str] = Field(default_factory=list)
    blocked_routes: list[StyleRouteId] = Field(default_factory=list)
    created_at: str = Field(default_factory=_now_iso)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.provider_ready and self.missing_inputs:
            raise ValueError("provider_ready decision cannot have missing_inputs")


class StyleRouteSourcePacket(BaseModel):
    style_route_source_packet_id: str = Field(default_factory=lambda: new_id("style_source_packet"))
    request_id: str
    source_grounding_mode: SourceGroundingMode
    source_references: list[SourceReference] = Field(default_factory=list)
    visual_nouns: list[str] = Field(default_factory=list)
    asset_refs: list[AssetReference] = Field(default_factory=list)
    is_source_grounded: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        source_grounded_modes = {
            SourceGroundingMode.DIRECT_REAL_REFERENCE,
            SourceGroundingMode.COMPOSITE_REAL_REFERENCES,
            SourceGroundingMode.DETERMINISTIC_ASSET_ONLY,
        }
        if self.source_grounding_mode in source_grounded_modes and not (self.source_references or self.asset_refs):
            raise ValueError("source references or asset refs are required for source-grounded mode")


class GMGVerbatimNounMap(BaseModel):
    gmg_verbatim_noun_map_id: str = Field(default_factory=lambda: new_id("gmg_noun_map"))
    source_terms: list[str]
    approved_nouns: list[str]
    rejected_nouns: list[str] = Field(default_factory=list)
    approved_asset_nouns: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        source_set = {term.lower() for term in self.source_terms + self.approved_asset_nouns}
        illegal = [noun for noun in self.approved_nouns if noun.lower() not in source_set]
        if illegal:
            raise ValueError(f"approved_nouns must be source terms or approved asset nouns: {illegal}")


class CACProductionSpec(BaseModel):
    cac_production_spec_id: str = Field(default_factory=lambda: new_id("cac_spec"))
    route_id: StyleRouteId = StyleRouteId.CAC_CONSCIOUS_AMBIENT_CINEMA
    source_packet_id: str
    source_grounding_mode: SourceGroundingMode
    real_reference_refs: list[str]
    mundane_anchor: str
    contact_point: str
    composition_logic: str
    atmosphere: str
    imperfection_cues: list[str]
    lens_language: str
    camera_distance: str
    lighting_motivation: str
    human_scale_space: str
    forbidden_cliches: list[str] = Field(default_factory=list)
    provider_constraints: list[str] = Field(default_factory=list)
    eval_targets: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.source_grounding_mode not in {SourceGroundingMode.DIRECT_REAL_REFERENCE, SourceGroundingMode.COMPOSITE_REAL_REFERENCES}:
            raise ValueError("CAC requires direct_real_reference or composite_real_references")
        if not self.real_reference_refs:
            raise ValueError("CAC requires real_reference_refs")
        required = [self.mundane_anchor, self.contact_point, self.composition_logic, self.atmosphere, self.lens_language, self.lighting_motivation, self.human_scale_space]
        if any(not value for value in required) or not self.imperfection_cues:
            raise ValueError("CAC requires Anchor, Contact, Composition, Atmosphere, Imperfection, and Lens")


class GMGExpertSelection(BaseModel):
    gmg_expert_selection_id: str = Field(default_factory=lambda: new_id("gmg_selection"))
    selected_expert_route_id: StyleRouteId
    visual_noun_map_id: str | None = None
    rationale: str
    confidence: float = Field(default=0.75, ge=0.0, le=1.0)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.selected_expert_route_id.value.startswith("GMG_EXPERT_"):
            raise ValueError("GMGExpertSelection must select exactly one GMG expert")


class GMGProductionSpec(BaseModel):
    gmg_production_spec_id: str = Field(default_factory=lambda: new_id("gmg_spec"))
    route_id: StyleRouteId
    expert_number: int
    source_packet_id: str
    verbatim_noun_map_id: str
    primary_visual_nouns: list[str]
    motion_language: str
    prompt_contract: str
    frame_profile: str
    composition_role: CompositionRole
    expert_input_requirements: list[str] = Field(default_factory=list)
    has_photo_cutout_object: bool = False
    has_document_archive_input: bool = False
    forbidden_patterns: list[str] = Field(default_factory=list)

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.route_id.value.startswith("GMG_EXPERT_"):
            raise ValueError("GMGProductionSpec route_id must be a GMG expert")
        if self.expert_number == 3 and not self.has_photo_cutout_object:
            raise ValueError("GMG Expert 03 requires a photo cutout object")
        if self.expert_number == 4 and not self.has_document_archive_input:
            raise ValueError("GMG Expert 04 requires document/evidence/archive input")
        if not self.primary_visual_nouns:
            raise ValueError("GMGProductionSpec requires primary_visual_nouns")


class PaperCutArtifactSpec(BaseModel):
    paper_cut_artifact_spec_id: str = Field(default_factory=lambda: new_id("paper_artifact_spec"))
    route_id: StyleRouteId = StyleRouteId.PAPER_CUT_ARTIFACT
    source_object_refs: list[str]
    cutout_requirements: list[str]
    mask_requirements: list[str] = Field(default_factory=list)
    layer_depth: int = Field(default=3, ge=1)
    paper_edge_treatment: str
    shadow_treatment: str
    attachment_treatment: str | None = None
    semantic_role: str
    composition_role: CompositionRole

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.source_object_refs:
            raise ValueError("Paper-Cut Artifact requires source_object_refs")
        if not self.cutout_requirements:
            raise ValueError("Paper-Cut Artifact requires cutout_requirements")


class PaperCutEditorialSpec(BaseModel):
    paper_cut_editorial_spec_id: str = Field(default_factory=lambda: new_id("paper_editorial_spec"))
    route_id: StyleRouteId = StyleRouteId.PAPER_CUT_EDITORIAL
    visual_hierarchy: list[str]
    paper_surface: str
    layer_system: list[str]
    object_anchors: list[str] = Field(default_factory=list)
    type_label_treatment: str
    mobile_readability_notes: str
    frame_profile: str

    def __init__(self, **data: Any):
        super().__init__(**data)
        if len(self.layer_system) < 2:
            raise ValueError("Paper-Cut Editorial requires a layer hierarchy")
        if not self.visual_hierarchy:
            raise ValueError("Paper-Cut Editorial requires visual_hierarchy")


class RouteProductionSpec(BaseModel):
    route_production_spec_id: str = Field(default_factory=lambda: new_id("route_spec"))
    style_route_decision_id: str
    route_id: StyleRouteId
    brand_id: str
    brand_context_version_id: str
    visual_preproduction_packet_id: str | None = None
    visual_beat_plan_id: str | None = None
    frame_profile: str
    composition_role: CompositionRole
    source_packet_id: str | None = None
    route_specific_spec_type: str
    route_specific_spec_id: str
    forbidden_patterns: list[str] = Field(default_factory=list)
    provider_constraints: list[str] = Field(default_factory=list)
    expected_output_type: TargetOutputType
    eval_targets: list[str] = Field(default_factory=list)
    status: RouteStatus = RouteStatus.PRODUCTION_SPEC_COMPILED

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.brand_context_version_id:
            raise ValueError("RouteProductionSpec.brand_context_version_id is required")


class ProviderJobBlueprint(BaseModel):
    provider_job_blueprint_id: str = Field(default_factory=lambda: new_id("provider_blueprint"))
    route_production_spec_id: str
    primary_style_route_id: StyleRouteId
    secondary_style_route_ids: list[StyleRouteId] = Field(default_factory=list)
    recommended_provider_capability: ProviderCapability
    input_asset_refs: list[str] = Field(default_factory=list)
    reference_asset_refs: list[str] = Field(default_factory=list)
    source_references: list[str] = Field(default_factory=list)
    frame_profile: str
    composition_role: CompositionRole
    prompt_contract: str
    negative_prompt_contract: str | None = None
    output_requirements: list[str] = Field(default_factory=list)
    idempotency_key_seed: str
    required_receipts: list[str] = Field(default_factory=list)
    blocked_until: list[str] = Field(default_factory=list)
    execution_state: str = "blueprint_only"

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.secondary_style_route_ids:
            raise ValueError("One provider job cannot average multiple primary style routes")
        if not self.source_references and not self.input_asset_refs and not self.reference_asset_refs:
            raise ValueError("ProviderJobBlueprint requires source/reference/input asset refs")
        if self.execution_state != "blueprint_only":
            raise ValueError("Style Route Engine must not execute provider jobs")


class StyleRouteEvaluationReceipt(BaseModel):
    style_route_evaluation_receipt_id: str = Field(default_factory=lambda: new_id("style_eval"))
    route_id: StyleRouteId
    route_production_spec_id: str | None = None
    source_grounding_score: float = Field(default=0.75, ge=0.0, le=1.0)
    primitive_fit_score: float = Field(default=0.75, ge=0.0, le=1.0)
    visual_preproduction_fit_score: float = Field(default=0.75, ge=0.0, le=1.0)
    frame_profile_fit_score: float = Field(default=0.75, ge=0.0, le=1.0)
    composition_role_fit_score: float = Field(default=0.75, ge=0.0, le=1.0)
    forbidden_patterns_detected: list[str] = Field(default_factory=list)
    pass_status: PassStatus = PassStatus.PASS
    rationale: str | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.forbidden_patterns_detected and self.pass_status == PassStatus.PASS:
            raise ValueError("forbidden patterns require pass_status to be fail or pass_with_risks")


class StyleRouteRepairInstruction(BaseModel):
    style_route_repair_instruction_id: str = Field(default_factory=lambda: new_id("style_repair"))
    route_id: StyleRouteId
    target_ref: str
    issue: str
    repair_action: str
    requires_new_preproduction_packet: bool = False
    requires_new_asset_reference: bool = False
    requires_new_provider_blueprint: bool = True


class StyleRouteUsageReceipt(BaseModel):
    style_route_usage_receipt_id: str = Field(default_factory=lambda: new_id("style_usage"))
    route_id: StyleRouteId
    brand_id: str
    brand_context_version_id: str
    requesting_component: RequestingComponent
    route_production_spec_id: str | None = None
    provider_job_blueprint_id: str | None = None
    output_ref: str | None = None
    frame_profile: str | None = None
    composition_role: CompositionRole | None = None
    created_at: str = Field(default_factory=_now_iso)
