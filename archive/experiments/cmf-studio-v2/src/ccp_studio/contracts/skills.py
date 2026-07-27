"""JIT skill invocation contracts for TS-CMF-002."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.interview_contracts import (
    ContractRouteTarget,
    ExpressionState,
    FirstLineAnchorSet,
    RepairFollowups,
)
from ccp_studio.contracts.orchestration import utc_now


class SkillInvocationRecord(BaseModel):
    schema_version: Literal["cmf.skill_invocation_record.v1"]
    skill_invocation_id: UUID
    orchestration_run_id: UUID
    stage_execution_plan_id: UUID
    skill_key: str = Field(min_length=1)
    registry_snapshot_id: UUID
    compiler_fingerprint: str = Field(min_length=1)
    source_context_refs: list[str] = Field(min_length=1)
    contrastive_prompt_layer_refs: list[str] = Field(min_length=1)
    critic_result_ref: str = Field(min_length=1)
    synthesis_result_ref: str = Field(min_length=1)
    eval_state: str = Field(min_length=1)
    created_at: datetime


class SkillUseMode(str, Enum):
    live_guest_induction = "live_guest_induction"
    conscious_interview_brief = "conscious_interview_brief"
    interview_engineering = "interview_engineering"
    narrative_induction = "narrative_induction"
    transcript_extraction = "transcript_extraction"
    source_expression_contrast = "source_expression_contrast"
    routing_support = "routing_support"
    evaluation_support = "evaluation_support"
    voice_dna_support = "voice_dna_support"
    scene_prompt_support_after_route = "scene_prompt_support_after_route"


class SaturationContextBundle(BaseModel):
    schema_version: Literal["cmf.saturation_context_bundle.v1"]
    source_doc_refs: list[str] = Field(default_factory=list)
    transcript_segment_refs: list[str] = Field(default_factory=list)
    guest_dossier_id: UUID | None = None
    audience_reality_brief_id: UUID | None = None
    context_premise_id: UUID | None = None
    audience_deep_trigger_map_id: UUID | None = None
    interviewer_resonance_context_id: UUID | None = None
    matrix_brief_id: UUID | None = None
    brand_context_version_id: UUID | None = None
    cral_finding_refs: list[str] = Field(default_factory=list)
    audience_conversation_refs: list[str] = Field(default_factory=list)
    primitive_candidate_ids: list[UUID] = Field(default_factory=list)
    invariant_field_refs: list[str] = Field(default_factory=list)
    coalition_signature_refs: list[str] = Field(default_factory=list)
    edge_product_refs: list[str] = Field(default_factory=list)
    ccf_orchestration_refs: list[str] = Field(default_factory=list)
    prior_evaluation_receipt_ids: list[UUID] = Field(default_factory=list)
    failure_corpus_refs: list[str] = Field(default_factory=list)
    expression_moment_id: UUID | None = None
    route_receipt_id: UUID | None = None
    complete_editing_session_id: UUID | None = None

    def stable_hash(self) -> str:
        payload = self.model_dump(mode="json")
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


class DSPyProgramSpec(BaseModel):
    schema_version: Literal["cmf.dspy_program_spec.v1"]
    dspy_program_spec_id: UUID
    program_key: str
    input_model: str
    output_model: str
    version: str
    fixture_set_ids: list[UUID]
    evaluation_target_ids: list[UUID]
    eval_threshold: float | None = Field(default=None, ge=0, le=1)


class JITSkillCompiler(BaseModel):
    schema_version: Literal["cmf.jit_skill_compiler.v1"]
    skill_key: str
    allowed_use_modes: list[SkillUseMode] = Field(min_length=1)
    dspy_program_spec_id: UUID
    registry_snapshot_id: UUID
    output_schema: str
    compiler_fingerprint: str
    approved: bool


class ContrastivePromptLayer(BaseModel):
    schema_version: Literal["cmf.contrastive_prompt_layer.v1"]
    contrastive_prompt_layer_id: UUID
    positive_pressure: list[str] = Field(min_length=1)
    negative_space: list[str] = Field(min_length=1)
    anti_centroid_checks: list[str] = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)


class CompilerCandidate(BaseModel):
    schema_version: Literal["cmf.compiler_candidate.v1"]
    candidate_id: UUID
    text: str = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)


class CompilerCandidateSet(BaseModel):
    schema_version: Literal["cmf.compiler_candidate_set.v1"]
    compiler_candidate_set_id: UUID
    candidates: list[CompilerCandidate] = Field(min_length=1)
    contrast_candidates: list[CompilerCandidate] = Field(min_length=1)


class AntiDraftCalibrationReport(BaseModel):
    schema_version: Literal["cmf.anti_draft_calibration_report.v1"]
    anti_draft_calibration_report_id: UUID
    genericity_score: float = Field(ge=0, le=1)
    citation_coverage: float = Field(ge=0, le=1)
    passed: bool
    failure_code: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)


class SkillInvocationReceipt(BaseModel):
    schema_version: Literal["cmf.skill_invocation_receipt.v1"]
    skill_invocation_receipt_id: UUID
    skill_key: str
    use_mode: SkillUseMode
    dspy_program_spec_id: UUID
    dspy_program_version: str
    registry_snapshot_id: UUID
    input_hashes: list[str] = Field(min_length=1)
    output_schema: str
    evidence_refs: list[str] = Field(min_length=1)
    eval_score: float | None = None
    reviewer_state: str | None = None
    extraction_boundary: str
    decision_code: str
    created_at: datetime


class ConsciousInterviewBriefQuestion(BaseModel):
    schema_version: Literal["cmf.conscious_interview_brief_question.v1"]
    question_id: UUID
    main_question: str = Field(min_length=1)
    source_pressure_refs: list[str] = Field(min_length=1)
    context_premise_ref: UUID
    matrix_brief_ref: UUID
    primitive_candidate_ids: list[UUID] = Field(min_length=1)
    invariant_refs: list[str] = Field(default_factory=list)
    interviewer_resonance_context_ref: UUID
    target_expression_states: list[ExpressionState] = Field(min_length=1)
    route_target: ContractRouteTarget
    edge_product_refs: list[str] = Field(default_factory=list)
    first_line_anchors: FirstLineAnchorSet
    depth_anchor: str = Field(min_length=1)
    expected_source_material: list[str] = Field(min_length=1)
    clip_start_rule: Literal["start_at_selected_first_line_anchor"] = "start_at_selected_first_line_anchor"
    depth_eval_rule: Literal["answer_must_contain_specific_cost_or_tension"] = "answer_must_contain_specific_cost_or_tension"
    landing_eval_targets: list[str] = Field(min_length=1)
    repair_followups: RepairFollowups
    intended_guest_reaction: str = Field(min_length=1)
    intended_extraction_outcome: str = Field(min_length=1)
    anti_centroid_check: str = Field(min_length=1)


class ConsciousInterviewBriefSkillOutput(BaseModel):
    schema_version: Literal["cmf.conscious_interview_brief_skill_output.v1"]
    interview_brief_skill_output_id: UUID
    question_contracts: list[ConsciousInterviewBriefQuestion] = Field(min_length=1)
    ccf_reverse_engineering_chain: list[str] = Field(min_length=1)
    required_skill_invocation_receipt_id: UUID | None = None


def new_skill_invocation_record(
    *,
    orchestration_run_id: UUID,
    stage_execution_plan_id: UUID,
    skill_key: str,
    registry_snapshot_id: UUID,
    compiler_fingerprint: str,
    source_context_refs: list[str],
    contrastive_prompt_layer_refs: list[str],
    critic_result_ref: str,
    synthesis_result_ref: str,
    eval_state: str,
) -> SkillInvocationRecord:
    return SkillInvocationRecord(
        schema_version="cmf.skill_invocation_record.v1",
        skill_invocation_id=uuid4(),
        orchestration_run_id=orchestration_run_id,
        stage_execution_plan_id=stage_execution_plan_id,
        skill_key=skill_key,
        registry_snapshot_id=registry_snapshot_id,
        compiler_fingerprint=compiler_fingerprint,
        source_context_refs=source_context_refs,
        contrastive_prompt_layer_refs=contrastive_prompt_layer_refs,
        critic_result_ref=critic_result_ref,
        synthesis_result_ref=synthesis_result_ref,
        eval_state=eval_state,
        created_at=utc_now(),
    )


def new_compiler_candidate(*, text: str, evidence_refs: list[str], confidence: float) -> CompilerCandidate:
    return CompilerCandidate(
        schema_version="cmf.compiler_candidate.v1",
        candidate_id=uuid4(),
        text=text,
        evidence_refs=evidence_refs,
        confidence=confidence,
    )
