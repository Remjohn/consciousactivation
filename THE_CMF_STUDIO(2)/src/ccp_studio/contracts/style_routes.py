"""Canonical visual style route contracts.

Style routes are production contracts, not vague aesthetic labels. A provider
job must pick one primary route unless a composition contract explicitly allows
multi-style assembly.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator

from ccp_studio.contracts.frame_profiles import FrameProfileCode


class StyleFamily(str, Enum):
    cac = "CAC"
    gmg = "GMG"
    paper_cut = "PAPER_CUT"
    documentary_proof = "DOCUMENTARY_PROOF"
    ui_reaction = "UI_REACTION"
    avatar_performance = "AVATAR_PERFORMANCE"


StyleRouteFamily = StyleFamily


class StyleExpertCode(str, Enum):
    cac_composer = "cac-composer"
    gmg_expert_01 = "gmg-expert-01-neo-schematic-architect"
    gmg_expert_02 = "gmg-expert-02-mono-kinetic-protagonist"
    gmg_expert_03 = "gmg-expert-03-emotional-animator"
    gmg_expert_04 = "gmg-expert-04-paper-architect"
    gmg_expert_05 = "gmg-expert-05-editorial-scribe"
    gmg_expert_06 = "gmg-expert-06-visual-synthesizer"
    paper_cut_editorial = "paper-cut-editorial"
    paper_cut_artifact = "paper-cut-artifact"
    documentary_proof = "documentary-proof"
    ui_reaction_surface = "ui-reaction-surface"
    avatar_performance_layer = "avatar-performance-layer"


class SourceReferenceMode(str, Enum):
    direct_real_reference = "direct_real_reference"
    composite_real_references = "composite_real_references"
    style_reference_only = "style_reference_only"
    abstract_symbolic_exception = "abstract_symbolic_exception"
    source_language_reference = "source_language_reference"


class StyleRoute(BaseModel):
    schema_version: Literal["cmf.style_route.v1"] = "cmf.style_route.v1"
    style_route_id: UUID = Field(default_factory=uuid4)
    route_code: str = Field(min_length=1)
    family: StyleFamily
    expert: StyleExpertCode | None = None
    display_name: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    requires_real_reference: bool = True
    allowed_reference_modes: list[SourceReferenceMode] = Field(min_length=1)
    required_inputs: list[str] = Field(default_factory=list)
    compatible_frame_profiles: list[FrameProfileCode] = Field(default_factory=list)
    compatible_content_formats: list[str] = Field(default_factory=list)
    primitive_affinities: list[str] = Field(default_factory=list)
    forbidden_patterns: list[str] = Field(default_factory=list)
    validation_agent: str | None = None

    @model_validator(mode="after")
    def hard_route_rules(self):
        real_modes = {SourceReferenceMode.direct_real_reference, SourceReferenceMode.composite_real_references}
        if self.requires_real_reference and not any(mode in self.allowed_reference_modes for mode in real_modes):
            raise ValueError("routes requiring real references must allow direct or composite real reference modes")
        if self.route_code in {"CAC_CONSCIOUS_AMBIENT_CINEMA", "PAPER_CUT_ARTIFACT", "DOCUMENTARY_PROOF"}:
            if not self.requires_real_reference:
                raise ValueError(f"{self.route_code} requires real-life/source reference")
        if self.route_code == "GMG_EXPERT_03_EMOTIONAL_ANIMATOR" and "photo_cutout_object" not in self.required_inputs:
            raise ValueError("GMG Expert 03 requires a photo_cutout_object")
        if self.route_code == "GMG_EXPERT_04_PAPER_ARCHITECT" and not any(
            marker in " ".join(self.required_inputs)
            for marker in ("documentary", "proof", "archive", "artifact")
        ):
            raise ValueError("GMG Expert 04 requires documentary/proof/archive/artifact input")
        if self.route_code == "GMG_EXPERT_06_VISUAL_SYNTHESIZER":
            if SourceReferenceMode.source_language_reference not in self.allowed_reference_modes:
                raise ValueError("GMG Expert 06 requires source-language/concept reference support")
            if "arbitrary_metaphor_without_source_language" not in self.forbidden_patterns:
                raise ValueError("GMG Expert 06 must not invent arbitrary metaphors")
        return self


DEFAULT_STYLE_ROUTES: list[StyleRoute] = [
    StyleRoute(
        route_code="CAC_CONSCIOUS_AMBIENT_CINEMA",
        family=StyleFamily.cac,
        expert=StyleExpertCode.cac_composer,
        display_name="CAC Conscious Ambient Cinema",
        purpose="Editorial cinematic realism and B-roll grounded in real-life reference.",
        requires_real_reference=True,
        allowed_reference_modes=[SourceReferenceMode.direct_real_reference, SourceReferenceMode.composite_real_references],
        required_inputs=["visual_schema", "brand_avatar", "transcript_beat", "real_life_reference"],
        compatible_frame_profiles=[FrameProfileCode.vertical_full, FrameProfileCode.square_soft_rounded_editorial],
        compatible_content_formats=["cinematic_story_commentary", "documentary_social_card"],
        primitive_affinities=["narrative_structure", "voice_intimacy", "trust_transfer"],
        forbidden_patterns=["generic_cinematic_sad_person", "unmotivated_light", "cgi_spectacle"],
        validation_agent="visual-analyst",
    ),
    StyleRoute(
        route_code="GMG_EXPERT_01_NEO_SCHEMATIC_ARCHITECT",
        family=StyleFamily.gmg,
        expert=StyleExpertCode.gmg_expert_01,
        display_name="GMG Expert 01 Neo Schematic Architect",
        purpose="Clean technical diagrams, architecture maps, and explainable systems.",
        requires_real_reference=False,
        allowed_reference_modes=[SourceReferenceMode.source_language_reference, SourceReferenceMode.abstract_symbolic_exception],
        required_inputs=["source_language_or_concept", "primitive_coalition", "diagram_scope"],
        compatible_frame_profiles=[FrameProfileCode.vertical_full, FrameProfileCode.vertical_papercut_explainer, FrameProfileCode.square_soft_rounded_editorial, FrameProfileCode.carousel_slide],
        compatible_content_formats=["educational_explainer", "carousel"],
        primitive_affinities=["reasoning_methodology", "visual_sonic_guidance", "friction_reduction"],
        forbidden_patterns=["arbitrary_metaphor", "decorative_diagram_without_source"],
        validation_agent="visual-analyst",
    ),
    StyleRoute(
        route_code="GMG_EXPERT_02_MONO_KINETIC_PROTAGONIST",
        family=StyleFamily.gmg,
        expert=StyleExpertCode.gmg_expert_02,
        display_name="GMG Expert 02 Mono Kinetic Protagonist",
        purpose="A single monochrome protagonist expressing a transcript-grounded action or pressure.",
        requires_real_reference=False,
        allowed_reference_modes=[SourceReferenceMode.source_language_reference, SourceReferenceMode.abstract_symbolic_exception],
        required_inputs=["transcript_beat", "kinetic_verb", "primitive_coalition"],
        compatible_frame_profiles=[FrameProfileCode.vertical_full, FrameProfileCode.square_soft_rounded_editorial, FrameProfileCode.feed_poster],
        compatible_content_formats=["educational_explainer", "supervisual"],
        primitive_affinities=["performance_delivery", "recognition", "visual_sonic_guidance"],
        forbidden_patterns=["crowded_scene", "unmotivated_pose"],
        validation_agent="visual-analyst",
    ),
    StyleRoute(
        route_code="GMG_EXPERT_03_EMOTIONAL_ANIMATOR",
        family=StyleFamily.gmg,
        expert=StyleExpertCode.gmg_expert_03,
        display_name="GMG Expert 03 Emotional Animator",
        purpose="Stick figure plus photorealistic object cutout for relatable emotional illustration.",
        requires_real_reference=True,
        allowed_reference_modes=[SourceReferenceMode.direct_real_reference, SourceReferenceMode.composite_real_references],
        required_inputs=["beat_cluster", "visual_schema", "photo_cutout_object"],
        compatible_frame_profiles=[FrameProfileCode.vertical_full, FrameProfileCode.square_soft_rounded_editorial, FrameProfileCode.feed_poster, FrameProfileCode.carousel_slide],
        compatible_content_formats=["supervisual", "carousel", "educational_explainer"],
        primitive_affinities=["recognition", "safe_recovery", "visual_sonic_guidance"],
        forbidden_patterns=["passive_floating_object", "no_photo_cutout"],
        validation_agent="visual-analyst",
    ),
    StyleRoute(
        route_code="GMG_EXPERT_04_PAPER_ARCHITECT",
        family=StyleFamily.gmg,
        expert=StyleExpertCode.gmg_expert_04,
        display_name="GMG Expert 04 Paper Architect",
        purpose="Documents, evidence, archives, ripped edges, tape, and tactile proof objects.",
        requires_real_reference=True,
        allowed_reference_modes=[SourceReferenceMode.direct_real_reference, SourceReferenceMode.composite_real_references, SourceReferenceMode.style_reference_only],
        required_inputs=["visual_schema", "documentary_or_proof_or_archive_or_artifact_input", "proof_or_memory_artifact"],
        compatible_frame_profiles=[FrameProfileCode.vertical_full, FrameProfileCode.square_proof_card, FrameProfileCode.square_soft_rounded_editorial, FrameProfileCode.carousel_slide],
        compatible_content_formats=["documentary_proof", "paper_cut_explainer", "supervisual"],
        primitive_affinities=["trust_transfer", "documentary_proof", "memory"],
        forbidden_patterns=["perfect_digital_edge", "unproven_fake_document"],
        validation_agent="visual-analyst",
    ),
    StyleRoute(
        route_code="GMG_EXPERT_05_EDITORIAL_SCRIBE",
        family=StyleFamily.gmg,
        expert=StyleExpertCode.gmg_expert_05,
        display_name="GMG Expert 05 Editorial Scribe",
        purpose="Text-led editorial cards with source-backed quote, claim, or proof hierarchy.",
        requires_real_reference=False,
        allowed_reference_modes=[SourceReferenceMode.source_language_reference, SourceReferenceMode.style_reference_only],
        required_inputs=["source_quote_or_claim", "copy_hierarchy", "primitive_coalition"],
        compatible_frame_profiles=[FrameProfileCode.square_soft_rounded_editorial, FrameProfileCode.square_proof_card, FrameProfileCode.feed_poster, FrameProfileCode.carousel_slide],
        compatible_content_formats=["quote_card", "supervisual", "carousel"],
        primitive_affinities=["voice_intimacy", "trust_transfer", "format_material"],
        forbidden_patterns=["fabricated_quote", "unreadable_text_stack"],
        validation_agent="visual-analyst",
    ),
    StyleRoute(
        route_code="GMG_EXPERT_06_VISUAL_SYNTHESIZER",
        family=StyleFamily.gmg,
        expert=StyleExpertCode.gmg_expert_06,
        display_name="GMG Expert 06 Visual Synthesizer",
        purpose="Pure black/white geometric truth for logic, mechanism, and abstract synthesis.",
        requires_real_reference=False,
        allowed_reference_modes=[SourceReferenceMode.source_language_reference, SourceReferenceMode.abstract_symbolic_exception],
        required_inputs=["primitive_coalition", "source_language_or_concept"],
        compatible_frame_profiles=[FrameProfileCode.vertical_full, FrameProfileCode.square_soft_rounded_editorial, FrameProfileCode.feed_poster, FrameProfileCode.carousel_slide],
        compatible_content_formats=["supervisual", "carousel", "explainer"],
        primitive_affinities=["structure", "visual_sonic_guidance", "friction_reduction"],
        forbidden_patterns=["gold_accent", "decorative_geometry", "arbitrary_metaphor_without_source_language"],
        validation_agent="visual-analyst",
    ),
    StyleRoute(
        route_code="PAPER_CUT_EDITORIAL",
        family=StyleFamily.paper_cut,
        expert=StyleExpertCode.paper_cut_editorial,
        display_name="Paper-Cut Editorial",
        purpose="Textured paper teaching scenes with labels, arrows, and concept panels.",
        requires_real_reference=False,
        allowed_reference_modes=[SourceReferenceMode.source_language_reference, SourceReferenceMode.style_reference_only],
        required_inputs=["teaching_concept", "paper_material_profile", "primitive_coalition"],
        compatible_frame_profiles=[FrameProfileCode.vertical_papercut_explainer, FrameProfileCode.feed_poster, FrameProfileCode.carousel_slide],
        compatible_content_formats=["paper_cut_explainer", "carousel", "supervisual"],
        primitive_affinities=["education", "format_material", "visual_sonic_guidance"],
        forbidden_patterns=["generic_scrapbook_clutter", "illegible_labels"],
        validation_agent="visual-analyst",
    ),
    StyleRoute(
        route_code="PAPER_CUT_ARTIFACT",
        family=StyleFamily.paper_cut,
        expert=StyleExpertCode.paper_cut_artifact,
        display_name="Paper-Cut Artifact",
        purpose="Transform recognizable real-life objects into tactile paper-cut scene ingredients.",
        requires_real_reference=True,
        allowed_reference_modes=[SourceReferenceMode.direct_real_reference, SourceReferenceMode.composite_real_references],
        required_inputs=["source_artifact", "composition_role", "paper_material_profile"],
        compatible_frame_profiles=[FrameProfileCode.vertical_full, FrameProfileCode.vertical_papercut_explainer, FrameProfileCode.square_soft_rounded_editorial, FrameProfileCode.feed_poster, FrameProfileCode.carousel_slide],
        compatible_content_formats=["paper_cut_explainer", "supervisual"],
        primitive_affinities=["recognition", "micro_semiotic_anchoring", "visual_sonic_guidance"],
        forbidden_patterns=["lost_object_recognizability", "generic_scrapbook_clutter"],
        validation_agent="visual-analyst",
    ),
    StyleRoute(
        route_code="DOCUMENTARY_PROOF",
        family=StyleFamily.documentary_proof,
        expert=StyleExpertCode.documentary_proof,
        display_name="Documentary Proof",
        purpose="Source-backed proof, archive, screenshot, receipt, or real-world evidence as the visual anchor.",
        requires_real_reference=True,
        allowed_reference_modes=[SourceReferenceMode.direct_real_reference, SourceReferenceMode.composite_real_references],
        required_inputs=["source_reference", "proof_or_archive_or_artifact_input", "composition_role"],
        compatible_frame_profiles=[FrameProfileCode.square_proof_card, FrameProfileCode.square_soft_rounded_editorial, FrameProfileCode.feed_poster, FrameProfileCode.carousel_slide],
        compatible_content_formats=["documentary_proof", "supervisual", "carousel"],
        primitive_affinities=["trust_transfer", "documentary_proof", "source_truth"],
        forbidden_patterns=["fabricated_evidence", "generic_stock_proof"],
        validation_agent="visual-analyst",
    ),
    StyleRoute(
        route_code="UI_REACTION_SURFACE",
        family=StyleFamily.ui_reaction,
        expert=StyleExpertCode.ui_reaction_surface,
        display_name="UI Reaction Surface",
        purpose="Polls, rankings, tier lists, this-vs-that cards, comments, and debate surfaces for reaction edits.",
        requires_real_reference=False,
        allowed_reference_modes=[SourceReferenceMode.source_language_reference, SourceReferenceMode.abstract_symbolic_exception],
        required_inputs=["reaction_prompt", "ui_state", "primitive_coalition"],
        compatible_frame_profiles=[FrameProfileCode.vertical_split_reaction, FrameProfileCode.feed_poster],
        compatible_content_formats=["conscious_reactions_editing", "visual_poll", "reaction_clip"],
        primitive_affinities=["feedback_loop", "experience_entry", "friction_management"],
        forbidden_patterns=["untracked_poll_state", "unsupported_claim"],
        validation_agent="visual-analyst",
    ),
    StyleRoute(
        route_code="AVATAR_PERFORMANCE_LAYER",
        family=StyleFamily.avatar_performance,
        expert=StyleExpertCode.avatar_performance_layer,
        display_name="Avatar Performance Layer",
        purpose="2D avatar or rigged character performance layer for educational and explainer sequences.",
        requires_real_reference=False,
        allowed_reference_modes=[SourceReferenceMode.source_language_reference, SourceReferenceMode.style_reference_only],
        required_inputs=["character_rig", "performance_state", "primitive_coalition"],
        compatible_frame_profiles=[FrameProfileCode.vertical_papercut_explainer, FrameProfileCode.vertical_full],
        compatible_content_formats=["animated_avatar_explainer", "paper_cut_explainer"],
        primitive_affinities=["performance_delivery", "education", "visual_sonic_guidance"],
        forbidden_patterns=["unrigged_random_avatar", "off-brand_character"],
        validation_agent="visual-analyst",
    ),
]
