from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field

from api.schemas.interviews import RefModel  # {object_id, version, sha256}, reused unchanged


class AirAuthorityRefModel(BaseModel):
    """Deliberately not imported from api/schemas/campaigns.py -- see Governing
    Decisions §3 (wave-ordering)."""
    authority_id: str
    authority_version: str
    authority_sha256: str
    authority_state: Literal["current", "candidate_not_current"]


HypothesisGateName = Literal[
    "SOURCE_FIDELITY", "EPISTEMIC_LEGALITY", "IDENTITY_FIT", "DOMAIN_FIT",
    "OPERATOR_CONSTRAINTS", "FATAL_PRIMITIVE_CONFLICT", "WRONG_READING_LOCKS",
    "LINEAGE_COMPLETE", "CURRENT_VERSION", "SEMANTIC_DUPLICATE",
]
EvaluationDimension = Literal[
    "source_fidelity", "role_tension_integrity", "primitive_coalition_fitness",
    "archetype_fit", "edge_integrity", "anti_centroid_distinctiveness",
    "execution_feasibility",
]
PortfolioState = Literal["OPEN", "GATED", "COMPARED", "STOPPED", "PROMOTED", "CANCELLED", "SUPERSEDED"]
CandidateState = Literal["PROPOSED", "GATE_REJECTED", "ELIGIBLE", "REPAIRED", "SUPERSEDED", "SELECTED", "PROMOTED"]


class SearchBudgetModel(BaseModel):
    maximum_candidate_count: int
    maximum_round_count: int
    maximum_model_tokens: int
    maximum_provider_cost_micros: int
    consumed_candidate_count: int
    consumed_round_count: int
    consumed_model_tokens: int
    consumed_provider_cost_micros: int


class DiversitySignatureModel(BaseModel):
    axes: dict[str, str]
    proof_sha256: str


# ---- GET /api/air/hypotheses/{portfolio_id} ----

class GateCheckModel(BaseModel):
    gate: HypothesisGateName
    applicability: Literal["APPLIES", "NOT_APPLICABLE"]
    verdict: Literal["PASS", "FAIL"]
    reason: str


class CandidateGateResultModel(BaseModel):
    receipt_ref: RefModel
    overall: Literal["ELIGIBLE", "INELIGIBLE"]
    checks: list[GateCheckModel]


class CandidateScoreModel(BaseModel):
    dimension_scores_micros: dict[str, int]
    total_micros: int
    eligible: bool


class HypothesisCandidateSummary(BaseModel):
    hypothesis_ref: RefModel
    psychological_role: str
    tension: str
    activation_directions: list[str]
    pressure_path: str
    stance: str
    stakes: list[str]
    pressure_dose: int
    participation_design: str
    smallest_useful_commitment: str
    diversity_signature: DiversitySignatureModel
    state: CandidateState
    gate_result: CandidateGateResultModel | None
    comparative_score: CandidateScoreModel | None


class HypothesisPortfolioDetail(BaseModel):
    portfolio_ref: RefModel
    portfolio_state: PortfolioState
    search_policy_ref: RefModel
    search_budget: SearchBudgetModel
    upstream_snapshot_refs: list[RefModel]
    candidates: list[HypothesisCandidateSummary]
    gate_result_refs: list[RefModel]
    comparative_evaluation_refs: list[RefModel]
    stopping_receipt_ref: RefModel | None
    selected_hypothesis_ref: RefModel | None
    promotion_ref: RefModel | None


# ---- POST /api/air/hypotheses/{portfolio_id}/select ----

class CandidateJudgment(BaseModel):
    hypothesis_id: str
    producer_actor_id: str
    gate_outcomes: dict[HypothesisGateName, bool]
    dimension_scores_micros: dict[EvaluationDimension, int] = Field(
        description="Each value must be an integer in [0, 1_000_000] (micros)."
    )


class HypothesisSelectionRequest(BaseModel):
    idempotency_key: str
    authority: AirAuthorityRefModel
    selected_hypothesis_id: str
    evaluator_actor_id: str
    candidate_judgments: list[CandidateJudgment]
    gate_profile_ref: RefModel
    evaluation_profile_ref: RefModel
    evidence_refs: list[RefModel]
    matrix_of_edging_ref: RefModel
    role_tension_ref: RefModel
    source_refs: list[RefModel]
    authority_decision_ref: RefModel
    decisive_margin_micros: int = 100_000
    diversity_exhausted: bool = False
    remaining_budget: SearchBudgetModel | None = None


class HypothesisSelectionResponse(BaseModel):
    portfolio: HypothesisPortfolioDetail
    decision: Literal["DECISIVE_WINNER"]
    stop_reason: Literal["DECISIVE_ELIGIBLE_WINNER"]
    selected_hypothesis_ref: RefModel
    comparison_ref: RefModel
    stopping_receipt_ref: RefModel
    planned_pack_ref: RefModel
    promotion_ref: RefModel


# ---- GET /api/air/scripts/{script_id} ----

class ScriptSegmentModel(BaseModel):
    # CORRECTED against services/air/src/cmf_activative_intelligence/
    # production_domain.py::_validate_script_segment, read directly rather
    # than trusting the spec's own Section 6 text:
    #   - transformation_class's real enum is {VERBATIM, CONDENSATION, BRIDGE,
    #     VOICE_DNA_REWRITE}. The spec's literal model instead listed
    #     TransformationRuleModel's enum (REWRITE/REORDER/VISUAL_TRANSLATION/
    #     AUDIO_REUSE/ANIMATION_TRANSLATION) -- a different object type's
    #     field, copy-pasted into the wrong model. Any real segment with
    #     transformation_class="BRIDGE" or "VOICE_DNA_REWRITE" (both of which
    #     production_demo.py actually produces) would fail response
    #     validation under the spec's literal schema.
    #   - claim_state, epistemic_state, and sequence_role are required fields
    #     on every real script_segment payload and were missing entirely.
    order: int
    segment_id: str
    transformation_class: Literal["VERBATIM", "CONDENSATION", "BRIDGE", "VOICE_DNA_REWRITE"]
    source_text: str | None
    final_text: str
    transformation_operations: list[str]
    source_span_refs: list[RefModel]
    voice_dna_applied: bool | None
    claim_state: str
    epistemic_state: str
    sequence_role: str


class BatchCompilationRefs(BaseModel):
    """Exactly the field names services/pipeline/src/cmf_pipeline/batch/service.py
    ::_compile_job reads off each `routes[]` entry -- ready to paste in unchanged.
    Route-authoring fields (route_id, derivative_type, source_spans, priority,
    animation_scene_package_ref, not_applicable_reason) are NOT AIR's concern
    and are not included here -- see Section 2, Out of scope."""
    final_script_ref: RefModel
    semantic_program_ref: RefModel
    archetype_coalition_ref: RefModel
    primitive_coalition_ref: RefModel
    activation_transfer_contract_ref: RefModel


class BatchCompilationRefsUnavailable(BaseModel):
    reason: Literal["SCRIPT_NOT_APPROVED", "NO_TRANSFER_CONTRACT_YET"]


class FinalScriptDetail(BaseModel):
    script_ref: RefModel
    lifecycle_state: str
    epistemic_state: str
    operator_approved: bool
    composition_eligible: bool
    program_ref: RefModel
    proposal_ref: RefModel
    segments: list[ScriptSegmentModel]
    script_sha256: str
    evaluation_receipt_refs: list[RefModel]
    source_lineage_refs: list[RefModel]
    role_tension_ref: RefModel
    primitive_coalition_ref: RefModel
    archetype_coalition_ref: RefModel
    brand_context_ref: RefModel
    voice_dna_ref: RefModel
    distillation_receipt_refs: list[RefModel]
    ccv_axes: dict[str, str]
    wrong_reading_lock_refs: list[RefModel]
    maximum_claim: str
    approval_receipt_ref: RefModel | None
    limitations: list[str]
    batch_compilation_refs: BatchCompilationRefs | BatchCompilationRefsUnavailable


# ---- POST /api/air/scripts/{script_id}/approve ----

class ScriptApprovalRequest(BaseModel):
    idempotency_key: str
    operator_id: str
    operator_decision_ref: RefModel
    rationale: str
    evaluation_refs: list[RefModel] | None = Field(
        default=None,
        description="Defaults to the candidate script's own evaluation_receipt_refs if omitted."
    )


class ScriptApprovalResponse(BaseModel):
    approval_ref: RefModel
    decision: Literal["APPROVE"]
    script: FinalScriptDetail


# ---- POST /api/air/scripts/{script_id}/transfer-contract ----

class MustSurvivePropertyModel(BaseModel):
    property_id: str
    property_kind: Literal["SOURCE_MEANING", "ROLE_TENSION", "EDGE_PRODUCT", "VOICE", "VISUAL", "WRONG_READING_LOCK", "IDENTITY_CONTINUITY", "SEQUENCE_FUNCTION"]
    statement: str
    evidence_refs: list[RefModel]
    hard_gate: bool


class TransformationRuleModel(BaseModel):
    operation_class: Literal["VERBATIM", "CONDENSATION", "REWRITE", "REORDER", "VISUAL_TRANSLATION", "AUDIO_REUSE", "ANIMATION_TRANSLATION"]
    allowed: bool
    constraints: list[str]


class RequiredChangeModel(BaseModel):
    change_id: str
    reason: str
    target_property_ids: list[str]
    required_operations: list[str]


class TransferContractRequest(BaseModel):
    idempotency_key: str
    authority: AirAuthorityRefModel
    source_expression_refs: list[RefModel]
    source_package_refs: list[RefModel]
    expression_moment_refs: list[RefModel]
    reaction_receipt_refs: list[RefModel]
    selected_hypothesis_ref: RefModel
    must_survive_properties: list[MustSurvivePropertyModel]
    transformation_rules: list[TransformationRuleModel]
    required_changes: list[RequiredChangeModel]
    evaluation_profile_ref: RefModel
    limitations: list[str]


class TransferContractResponse(BaseModel):
    contract_ref: RefModel
    final_script_ref: RefModel
