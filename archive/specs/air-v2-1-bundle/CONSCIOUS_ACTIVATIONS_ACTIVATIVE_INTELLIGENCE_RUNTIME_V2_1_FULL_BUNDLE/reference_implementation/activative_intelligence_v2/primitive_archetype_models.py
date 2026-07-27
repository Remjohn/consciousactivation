from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import Field, model_validator

from .models import ApplicabilityEnvelope, EpistemicState, ImmutableRef, StrictModel


class PrimitivePlane(str, Enum):
    MEANING = "meaning_plane"
    EXPERIENCE = "experience_plane"


class PrimitiveBinding(StrictModel):
    binding_id: str = Field(min_length=1)
    primitive_id: str = Field(min_length=1)
    primitive_version: str = Field(min_length=1)
    primitive_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    plane: PrimitivePlane
    family: str = Field(min_length=1)
    core_move: str = Field(min_length=1)
    local_function: str = Field(min_length=1)
    activation_evidence_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    suppression_conditions: tuple[str, ...] = ()
    conflicts_with: tuple[str, ...] = ()
    misuse_modes: tuple[str, ...] = ()
    epistemic_state: EpistemicState


class PrimitiveMisuseRisk(StrictModel):
    risk_id: str
    primitive_id: str
    misuse_mode: str
    trigger_condition: str
    probable_wrong_reading: str
    severity: Literal["low", "moderate", "high", "fatal"]
    prevention_gate: str
    evidence_refs: tuple[ImmutableRef, ...] = ()


class CoalitionSignature(StrictModel):
    signature_id: str
    dominant_pressure_path: str
    recognition_move: str
    tension_release_pattern: str
    psychological_role_transition: str
    participation_threshold: str
    visual_attention_logic: str | None = None
    experiential_progression: str | None = None
    canonical_fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")


class EdgeProduct(StrictModel):
    edge_product_id: str
    broad_signal_ref: ImmutableRef
    matrix_of_edging_ref: ImmutableRef
    hidden_pressure: str
    surviving_edge: str
    stance: str
    psychological_role: str
    tension: str
    consequence: str
    counteractivation_risks: tuple[str, ...] = ()
    evidence_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    epistemic_state: EpistemicState


class PrimitiveCoalitionContract(StrictModel):
    coalition_id: str
    version: str
    source_context_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    primitive_bindings: tuple[PrimitiveBinding, ...] = Field(min_length=2)
    execution_order: tuple[str, ...] = Field(min_length=2)
    compatibility_explanation: str = Field(min_length=1)
    conflict_resolutions: tuple[str, ...] = ()
    suppressed_bindings: tuple[str, ...] = ()
    signature: CoalitionSignature
    edge_product: EdgeProduct
    misuse_risks: tuple[PrimitiveMisuseRisk, ...] = ()
    evaluation_contract_ref: ImmutableRef
    lifecycle_state: Literal["proposed", "validated", "approved", "superseded"]

    @model_validator(mode="after")
    def check_order(self) -> "PrimitiveCoalitionContract":
        ids = {b.binding_id for b in self.primitive_bindings}
        if set(self.execution_order) != ids:
            raise ValueError("execution_order must contain each binding exactly once")
        if len(ids) != len(self.primitive_bindings):
            raise ValueError("primitive binding IDs must be unique")
        return self


class PrimitiveEvaluationReceipt(StrictModel):
    receipt_id: str
    coalition_ref: ImmutableRef
    binding_results: dict[str, Literal["pass", "fail", "not_applicable"]]
    conflict_gate_passed: bool
    misuse_gate_passed: bool
    coalition_signature_preserved: bool
    edge_product_preserved: bool
    evidence_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    verdict: Literal["pass", "fail", "insufficient_evidence"]

    @model_validator(mode="after")
    def gates_control_verdict(self) -> "PrimitiveEvaluationReceipt":
        hard_pass = (
            all(v in {"pass", "not_applicable"} for v in self.binding_results.values())
            and self.conflict_gate_passed and self.misuse_gate_passed
            and self.coalition_signature_preserved and self.edge_product_preserved
        )
        if self.verdict == "pass" and not hard_pass:
            raise ValueError("failed Primitive gate cannot receive pass verdict")
        return self


class PsychologicalRoleTensionContract(StrictModel):
    contract_id: str
    activation_domain: Literal["source", "relationship", "audience", "campaign", "derivative"]
    psychological_role: str = Field(min_length=1)
    tension: str = Field(min_length=1)
    recognition_path: str = Field(min_length=1)
    stance: str = Field(min_length=1)
    participation_threshold: str = Field(min_length=1)
    counteractivation_roles: tuple[str, ...] = ()
    transfer_invariants: tuple[str, ...] = Field(min_length=1)
    evidence_refs: tuple[ImmutableRef, ...] = Field(min_length=1)


class ArchetypeBinding(StrictModel):
    binding_id: str
    archetype_id: str
    evidence_prompt_ref: ImmutableRef | None = None
    local_function: str
    source_fit: str
    category_geometry: str
    primitive_binding_ids: tuple[str, ...] = Field(min_length=1)
    rejection_conditions: tuple[str, ...] = ()


class ArchetypeCoalitionProgram(StrictModel):
    program_id: str
    version: str
    role_tension_contract: PsychologicalRoleTensionContract
    primitive_coalition_ref: ImmutableRef
    primary_archetype: ArchetypeBinding
    supporting_archetypes: tuple[ArchetypeBinding, ...] = ()
    source_expression_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    category_target: str
    sequence_or_reading_logic: str
    anti_centroid_locks: tuple[str, ...] = Field(min_length=1)
    wrong_reading_locks: tuple[str, ...] = Field(min_length=1)
    rejected_alternatives: tuple[str, ...] = ()
    lifecycle_state: Literal["proposed", "validated", "approved", "superseded"]


class BrandContextVersion(StrictModel):
    brand_context_id: str
    version: str
    brand_genesis_session_ref: ImmutableRef
    identity_truths: tuple[str, ...] = Field(min_length=1)
    audience_relationship: str
    positioning_tension: str
    source_references: tuple[ImmutableRef, ...] = Field(min_length=1)
    supersedes_ref: ImmutableRef | None = None


class VoiceDNA(StrictModel):
    voice_dna_id: str
    version: str
    brand_context_ref: ImmutableRef
    vocabulary_patterns: tuple[str, ...]
    rhythm_patterns: tuple[str, ...]
    sentence_pressure_patterns: tuple[str, ...]
    stance_patterns: tuple[str, ...]
    specificity_patterns: tuple[str, ...]
    metaphor_range: tuple[str, ...]
    emotional_distance: str
    prohibited_centroid_patterns: tuple[str, ...] = ()
    source_evidence_refs: tuple[ImmutableRef, ...] = Field(min_length=1)


class VisualDNA(StrictModel):
    visual_dna_id: str
    version: str
    brand_context_ref: ImmutableRef
    real_life_reference_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    subject_treatment: tuple[str, ...]
    visual_temperature: tuple[str, ...]
    materiality: tuple[str, ...]
    composition_tendencies: tuple[str, ...]
    negative_space_functions: tuple[str, ...]
    edge_behaviors: tuple[str, ...]
    typographic_posture: tuple[str, ...]
    motion_character: tuple[str, ...] = ()
    prohibited_centroid_defaults: tuple[str, ...] = ()


class DistillationLayer(str, Enum):
    SATURATION = "saturation"
    COLLISION = "collision"
    COMPRESSION = "compression"
    EVALUATION = "evaluation"
    RECURSION = "recursion"


class DistillationLayerReceipt(StrictModel):
    receipt_id: str
    layer: DistillationLayer
    input_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    output_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    decisions: tuple[str, ...] = Field(min_length=1)
    edge_product_preserved: bool
    role_tension_preserved: bool
    voice_dna_preserved: bool | None = None
    visual_dna_preserved: bool | None = None
    rejection_refs: tuple[ImmutableRef, ...] = ()


class FinalScriptSegment(StrictModel):
    segment_id: str
    text: str = Field(min_length=1)
    transformation_kind: Literal["verbatim", "condensed", "adapted", "newly_authored"]
    source_span_refs: tuple[ImmutableRef, ...] = ()
    local_archetype_function: str
    local_primitive_binding_ids: tuple[str, ...] = Field(min_length=1)
    voice_dna_check: Literal["pass", "fail", "not_applicable"]


class FinalScriptPackage(StrictModel):
    final_script_id: str
    version: str
    source_package_ref: ImmutableRef
    expression_moment_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    role_tension_contract_ref: ImmutableRef
    primitive_coalition_ref: ImmutableRef
    archetype_coalition_ref: ImmutableRef
    edge_product_ref: ImmutableRef
    brand_context_ref: ImmutableRef
    voice_dna_ref: ImmutableRef
    visual_dna_ref: ImmutableRef
    rscs_receipt_refs: tuple[ImmutableRef, ...] = Field(min_length=5)
    segments: tuple[FinalScriptSegment, ...] = Field(min_length=1)
    category_target: str
    wrong_reading_locks: tuple[str, ...] = Field(min_length=1)
    anti_centroid_locks: tuple[str, ...] = Field(min_length=1)
    operator_approval_ref: ImmutableRef
    lifecycle_state: Literal["draft", "validated", "approved", "superseded"]


class AnimationSceneSpec(StrictModel):
    scene_id: str
    source_ref: ImmutableRef
    script_segment_ids: tuple[str, ...] = Field(min_length=1)
    function: Literal["b_roll", "explanation", "quote_visualization", "concept_demonstration", "carousel_element", "supervisual_element", "full_animation"]
    character_or_avatar_refs: tuple[ImmutableRef, ...] = ()
    source_audio_ref: ImmutableRef | None = None
    pose_expression_intent: str
    environment_and_prop_refs: tuple[ImmutableRef, ...] = ()
    composition_intent: str
    transparency_required: bool = False
    render_requirement: Literal["composition_ready", "preview_required", "full_render_required"]


class AnimationScenePackage(StrictModel):
    package_id: str
    final_script_ref: ImmutableRef
    scenes: tuple[AnimationSceneSpec, ...] = Field(min_length=1)
    reusable_across_derivatives: bool = True
    runtime_capability_requirements: tuple[str, ...] = ()
    format02_activated: Literal[False] = False
    evaluation_contract_ref: ImmutableRef


class ProgrammedModelArtifact(StrictModel):
    artifact_id: str
    base_model: str
    tokenizer_ref: ImmutableRef
    checkpoint_or_adapter_ref: ImmutableRef
    runtime_ref: ImmutableRef
    training_corpus_ref: ImmutableRef
    supported_contract_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    exact_hashes: dict[str, str]


class LearnedCapabilityClaim(StrictModel):
    claim_id: str
    capability_id: str
    artifact_ref: ImmutableRef
    applicability: ApplicabilityEnvelope
    advantage_profile: dict[str, float]
    hard_gate_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    fallback_binding_ref: ImmutableRef
    lifecycle_state: Literal["proposed", "experimental", "validated", "shadow", "limited_production", "production", "deprecated", "retired", "revoked"]


class ModelProgramBinding(StrictModel):
    binding_id: str
    claim_ref: ImmutableRef
    workflow_node_type: str
    canonical_skill_refs: tuple[ImmutableRef, ...] = Field(min_length=1)
    primitive_contract_refs: tuple[ImmutableRef, ...] = ()
    allowed_tool_ids: tuple[str, ...]
    context_capsule_ref: ImmutableRef
    deterministic_validator_refs: tuple[ImmutableRef, ...]
    independent_evaluator_ref: ImmutableRef
    fallback_ref: ImmutableRef
    budget_class: str


class ProductHandoffReceipt(StrictModel):
    receipt_id: str
    producer_product: str
    consumer_product: str
    object_ref: ImmutableRef
    schema_ref: ImmutableRef
    producer_verdict: Literal["pass", "blocked", "superseded"]
    consumer_verdict: Literal["accepted", "rejected", "adapter_required"]
    limitations: tuple[str, ...] = ()
    next_admissible_action: str | None = None
