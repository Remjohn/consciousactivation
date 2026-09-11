from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class RefModel(BaseModel):
    object_id: str
    version: str
    sha256: str


ContextClass = Literal[
    "IDENTITY_DNA",
    "CONTEXT_PREMISE",
    "RESONANCE_REFERENCE",
    "BRAND_VOICE",
    "EVIDENCE_SOURCE",
    "INTERVIEW_RECORDING",
    "CAPTION_TRACK",
]


class UploadedDocumentSummary(BaseModel):
    asset_id: str
    sha256: str
    bytes: int
    media_type: str
    original_filename: str
    context_class: str = "EVIDENCE_SOURCE"
    caption_for: str | None = None
    brand_ref: RefModel | None = None


class GuestResearchPackageResponse(BaseModel):
    research_package_id: str
    revision: int
    guest_name: str
    source_urls: list[str]
    uploaded_documents: list[UploadedDocumentSummary]
    idempotent_replay: bool


class MatrixOfEdgingSeed(BaseModel):
    psychological_role: str
    tension: str
    activation_direction_set: list[str]
    pressure_path: str
    stance: str
    counteractivation_strategy: str
    smallest_commitment: str


class PlannedQuestion(BaseModel):
    question_text: str
    activation_direction: str
    psychological_role: str


class HypothesisPipelineStatus(BaseModel):
    status: Literal["BLOCKED_PENDING_GAP_007"]
    iac_ref: RefModel | None
    planned_aip_ref: RefModel | None
    arm_receipt_ref: RefModel | None
    blocked_reason: str


class PlanningLineageTemplate(BaseModel):
    brief_ref: RefModel
    planned_aip_ref: RefModel | None
    iac_ref: RefModel | None
    arm_receipt_ref: RefModel | None
    planned_object_digests: dict[str, str] | None


class ComposeBriefRequest(BaseModel):
    research_package_id: str
    brand_context_ref: RefModel | None = None
    voice_dna_ref: RefModel | None = None
    guest_name: str
    tension_hypothesis: str
    matrix_of_edging_seed: MatrixOfEdgingSeed
    planned_questions: list[PlannedQuestion]
    expression_targets: list[str]
    operator_id: str
    authority_scope: str
    assertion_id: str


class ActivativeInterviewBriefResponse(BaseModel):
    brief_id: str
    revision: int
    research_package_ref: RefModel
    brand_context_ref: RefModel | None
    voice_dna_ref: RefModel | None
    guest_name: str
    content_origin: Literal["operator_supplied"]
    tension_hypothesis: str
    matrix_of_edging_seed: MatrixOfEdgingSeed
    planned_questions: list[PlannedQuestion]
    expression_targets: list[str]
    hypothesis_pipeline_status: HypothesisPipelineStatus
    planning_lineage_template: PlanningLineageTemplate
    idempotent_replay: bool


class ComposeSessionRequest(BaseModel):
    brief_id: str
    recording_date: str | None = None
    operator_id: str
    authority_scope: str
    assertion_id: str


class ComposerSessionResponse(BaseModel):
    session_id: str
    revision: int
    brief_ref: RefModel
    relationship_state_ref: RefModel
    progression_ref: RefModel
    stage: str
    recording_date: str | None
    idempotent_replay: bool