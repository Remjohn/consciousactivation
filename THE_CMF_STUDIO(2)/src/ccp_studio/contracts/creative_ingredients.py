"""Creative ingredient contracts.

Creative ingredients are the bridge between source references, visual research,
style routes, frame profiles, composition roles, and provider jobs.
"""

from __future__ import annotations

import hashlib
import json
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.frame_profiles import FrameProfileCode
from ccp_studio.contracts.style_routes import SourceReferenceMode, StyleRoute


class SourceReferenceKind(str, Enum):
    interview_frame = "interview_frame"
    transcript_quote = "transcript_quote"
    client_upload = "client_upload"
    proof_document = "proof_document"
    screenshot = "screenshot"
    memory_object = "memory_object"
    location_reference = "location_reference"
    composition_reference = "composition_reference"
    style_reference = "style_reference"
    source_language = "source_language"


class CreativeIngredientClass(str, Enum):
    real_life_artifact = "real_life_artifact"
    memory_object = "memory_object"
    proof_object = "proof_object"
    micro_semiotic_anchor = "micro_semiotic_anchor"
    cinematic_broll_reference = "cinematic_broll_reference"
    gmg_graphic_element = "gmg_graphic_element"
    paper_cut_prop = "paper_cut_prop"
    avatar_attachment = "avatar_attachment"
    composition_reference = "composition_reference"
    style_reference = "style_reference"
    ui_reaction_object = "ui_reaction_object"


class CompositionRole(str, Enum):
    hero_plate = "hero_plate"
    background_plate = "background_plate"
    proof_insert = "proof_insert"
    memory_insert = "memory_insert"
    foreground_artifact = "foreground_artifact"
    avatar_scene = "avatar_scene"
    diagram_panel = "diagram_panel"
    reaction_ui_object = "reaction_ui_object"
    transition_card = "transition_card"
    micro_semiotic_detail = "micro_semiotic_detail"


class SourceReference(BaseModel):
    schema_version: Literal["cmf.source_reference.v1"] = "cmf.source_reference.v1"
    source_reference_id: UUID = Field(default_factory=uuid4)
    kind: SourceReferenceKind
    source_ref: str = Field(min_length=1)
    provenance_ref: str | None = None
    rights_status: Literal["client_owned", "licensed", "direct_use_allowed", "edit_allowed", "reference_only", "unknown", "blocked"] = "unknown"
    timestamp_ref: str | None = None
    description: str = Field(min_length=1)


class CreativeIngredient(BaseModel):
    schema_version: Literal["cmf.creative_ingredient.v1"] = "cmf.creative_ingredient.v1"
    creative_ingredient_id: UUID = Field(default_factory=uuid4)
    brand_id: UUID
    brand_context_version_ref: str = Field(min_length=1)
    source_references: list[SourceReference] = Field(min_length=1)
    ingredient_class: CreativeIngredientClass
    ingredient_role: str = Field(min_length=1)
    allowed_frame_profiles: list[FrameProfileCode] = Field(min_length=1)
    composition_roles: list[CompositionRole] = Field(min_length=1)
    primitive_binding_refs: list[str] = Field(default_factory=list)
    style_route_codes_allowed: list[str] = Field(default_factory=list)
    preferred_style_route_code: str | None = None
    approval_status: Literal["candidate", "approved_reference_only", "approved_direct_use", "approved_editable", "blocked"] = "candidate"
    eval_refs: list[str] = Field(default_factory=list)
    usage_refs: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def source_references_required_for_real_life(self):
        if self.ingredient_class in {
            CreativeIngredientClass.real_life_artifact,
            CreativeIngredientClass.memory_object,
            CreativeIngredientClass.proof_object,
            CreativeIngredientClass.micro_semiotic_anchor,
            CreativeIngredientClass.cinematic_broll_reference,
        }:
            if not self.source_references:
                raise ValueError("real-life grounded ingredients require source references")
        if self.preferred_style_route_code and self.style_route_codes_allowed and self.preferred_style_route_code not in self.style_route_codes_allowed:
            raise ValueError("preferred_style_route_code must be listed in style_route_codes_allowed")
        return self


class VisualIngredientRequirement(BaseModel):
    schema_version: Literal["cmf.visual_ingredient_requirement.v1"] = "cmf.visual_ingredient_requirement.v1"
    visual_ingredient_requirement_id: UUID = Field(default_factory=uuid4)
    brand_id: UUID
    primitive_coalition_contract_ref: str = Field(min_length=1)
    content_archetype: str = Field(min_length=1)
    target_format: str = Field(min_length=1)
    required_ingredient_class: CreativeIngredientClass
    semantic_need: str = Field(min_length=1)
    required: bool = True
    acceptable_source_kinds: list[SourceReferenceKind] = Field(default_factory=list)
    eval_targets: dict[str, float] = Field(default_factory=dict)


class VisualIngredientProgram(BaseModel):
    schema_version: Literal["cmf.visual_ingredient_program.v1"] = "cmf.visual_ingredient_program.v1"
    visual_ingredient_program_id: UUID = Field(default_factory=uuid4)
    creative_ingredient_id: UUID
    brand_id: UUID | None = None
    brand_context_version_id: str | None = None
    primitive_coalition_contract_id: str | None = None
    source_reference: SourceReference | None = None
    visual_schema_ref: str | None = None
    storyboard_ingredient_ref: str | None = None
    source_reference_mode: SourceReferenceMode
    style_route: StyleRoute
    frame_profile: FrameProfileCode
    composition_role: CompositionRole
    prompt_sections: dict[str, str] = Field(default_factory=dict)
    evaluation_requirements: dict[str, float] = Field(default_factory=dict)
    eval_requirements: dict[str, float] = Field(default_factory=dict)
    program_hash: str = Field(min_length=1)

    @model_validator(mode="after")
    def provider_jobs_require_source_or_exception(self):
        if not self.evaluation_requirements and self.eval_requirements:
            self.evaluation_requirements = dict(self.eval_requirements)
        if self.evaluation_requirements and not self.eval_requirements:
            self.eval_requirements = dict(self.evaluation_requirements)
        if self.style_route.requires_real_reference and self.source_reference_mode not in {
            SourceReferenceMode.direct_real_reference,
            SourceReferenceMode.composite_real_references,
        }:
            raise ValueError("style route requires real-life reference mode")
        payload = self.model_dump(mode="json", exclude={"program_hash", "visual_ingredient_program_id", "schema_version"}, exclude_none=True)
        expected = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        if self.program_hash != expected:
            raise ValueError("program_hash must equal sha256 of VisualIngredientProgram payload")
        return self


class CreativeIngredientVariant(BaseModel):
    schema_version: Literal["cmf.creative_ingredient_variant.v1"] = "cmf.creative_ingredient_variant.v1"
    creative_ingredient_variant_id: UUID = Field(default_factory=uuid4)
    creative_ingredient_id: UUID
    style_route_code: str = Field(min_length=1)
    frame_profile: FrameProfileCode
    file_ref: str = Field(min_length=1)
    alpha_ref: str | None = None
    mask_ref: str | None = None
    layer_manifest_ref: str | None = None
    provider_job_ref: str | None = None
    transformation_receipt_ref: str = Field(min_length=1)
    recognizability_score: float = Field(ge=0, le=1)
    style_fit_score: float = Field(ge=0, le=1)
    status: Literal["draft", "needs_review", "approved", "blocked"] = "draft"


def _json_safe(value):
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    return value


def visual_ingredient_program_hash(program: VisualIngredientProgram | dict) -> str:
    if isinstance(program, VisualIngredientProgram):
        payload = program.model_dump(mode="json", exclude={"program_hash", "visual_ingredient_program_id", "schema_version"}, exclude_none=True)
    else:
        payload = {k: _json_safe(v) for k, v in program.items() if k not in {"program_hash", "visual_ingredient_program_id", "schema_version"} and v is not None}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
