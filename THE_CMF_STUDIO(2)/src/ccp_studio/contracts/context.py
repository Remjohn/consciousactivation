"""Context compilation contracts for TS-CMF-024."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class ContextOutputStatus(str, Enum):
    draft = "draft"
    evidence_review_required = "evidence_review_required"
    approved = "approved"
    rejected = "rejected"


class ContextArtifactKind(str, Enum):
    guest_dossier = "guest_dossier"
    audience_reality_brief = "audience_reality_brief"
    audience_deep_trigger_map = "audience_deep_trigger_map"
    context_premise = "context_premise"
    interviewer_resonance_context = "interviewer_resonance_context"


class TriggerDepthMode(str, Enum):
    shallow = "shallow"
    saturated = "saturated"


class EvidenceBackedInference(BaseModel):
    schema_version: Literal["cmf.evidence_backed_inference.v1"]
    inference_id: UUID
    statement: str = Field(min_length=1)
    evidence_ids: list[UUID] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    limitation: str | None = None


class ContextCompilerInputPacket(BaseModel):
    schema_version: Literal["cmf.context_compiler_input_packet.v1"]
    organization_id: UUID
    brand_id: UUID
    research_field_id: UUID
    approved_evidence_ids: list[UUID] = Field(min_length=1)
    research_snapshot_id: UUID | None = None
    guest_id: UUID | None = None
    audience_scope: str = Field(min_length=1)
    operator_id: UUID
    guest_profile_hints: list[str] = Field(default_factory=list)
    operator_notes: list[str] = Field(default_factory=list)
    brand_context_version_id: UUID | None = None

    def stable_hash(self) -> str:
        payload = self.model_dump(mode="json")
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


class GuestDossier(BaseModel):
    schema_version: Literal["cmf.guest_dossier.v1"]
    guest_dossier_id: UUID
    organization_id: UUID
    brand_id: UUID
    guest_id: UUID | None = None
    research_field_id: UUID
    identity_facts: list[EvidenceBackedInference] = Field(default_factory=list)
    biography_and_work: list[EvidenceBackedInference] = Field(default_factory=list)
    recurring_themes: list[EvidenceBackedInference] = Field(default_factory=list)
    strongest_scenes: list[EvidenceBackedInference] = Field(default_factory=list)
    public_language: list[EvidenceBackedInference] = Field(default_factory=list)
    prior_interview_patterns: list[EvidenceBackedInference] = Field(default_factory=list)
    contradictions: list[EvidenceBackedInference] = Field(default_factory=list)
    emotional_territory: list[EvidenceBackedInference] = Field(default_factory=list)
    likely_expression_states: list[EvidenceBackedInference] = Field(default_factory=list)
    risks_and_boundaries: list[EvidenceBackedInference] = Field(default_factory=list)
    audience_overlap: list[EvidenceBackedInference] = Field(default_factory=list)
    research_gaps: list[str] = Field(default_factory=list)
    status: ContextOutputStatus
    created_at: datetime
    updated_at: datetime


class AudienceRealityBrief(BaseModel):
    schema_version: Literal["cmf.audience_reality_brief.v1"]
    audience_reality_brief_id: UUID
    organization_id: UUID
    brand_id: UUID
    research_field_id: UUID
    audience_scope: str = Field(min_length=1)
    current_anxieties: list[EvidenceBackedInference] = Field(default_factory=list)
    recurring_comments: list[EvidenceBackedInference] = Field(default_factory=list)
    social_debates: list[EvidenceBackedInference] = Field(default_factory=list)
    search_questions: list[EvidenceBackedInference] = Field(default_factory=list)
    objections: list[EvidenceBackedInference] = Field(default_factory=list)
    cultural_language: list[EvidenceBackedInference] = Field(default_factory=list)
    identity_tensions: list[EvidenceBackedInference] = Field(default_factory=list)
    ordinary_objects_and_rituals: list[EvidenceBackedInference] = Field(default_factory=list)
    micro_semiotic_anchor_candidates: list[EvidenceBackedInference] = Field(default_factory=list)
    temporal_relevance: str = Field(default="evergreen_or_reviewed")
    status: ContextOutputStatus
    created_at: datetime
    updated_at: datetime


class AudienceDeepTriggerMap(BaseModel):
    schema_version: Literal["cmf.audience_deep_trigger_map.v1"]
    trigger_map_id: UUID
    organization_id: UUID
    brand_id: UUID
    research_field_id: UUID
    depth_mode: TriggerDepthMode
    hermeneutical_gaps: list[EvidenceBackedInference] = Field(default_factory=list)
    moral_emotional_vectors: list[EvidenceBackedInference] = Field(default_factory=list)
    coping_trajectory: list[EvidenceBackedInference] = Field(default_factory=list)
    audience_guest_matches: list[EvidenceBackedInference] = Field(default_factory=list)
    audience_coach_matches: list[EvidenceBackedInference] = Field(default_factory=list)
    regulatory_focus: str | None = None
    confidence: float = Field(default=0.5, ge=0, le=1)
    gaps: list[str] = Field(default_factory=list)
    status: ContextOutputStatus
    created_at: datetime
    updated_at: datetime


class ContextPremise(BaseModel):
    schema_version: Literal["cmf.context_premise.v1"]
    context_premise_id: UUID
    organization_id: UUID
    brand_id: UUID
    research_field_id: UUID
    guest_dossier_id: UUID
    audience_reality_brief_id: UUID
    trigger_map_id: UUID
    statement: str = Field(min_length=1)
    evidence_ids: list[UUID] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    valid_for: Literal["interview_preparation"] = "interview_preparation"
    expires_at: datetime | None = None
    guest_implication: str = Field(min_length=1)
    audience_implication: str = Field(min_length=1)
    question_implications: list[str] = Field(min_length=1)
    audience_conversation_refs: list[str] = Field(default_factory=list)
    trigger_match_summary: str | None = None
    risk_if_wrong: str = Field(min_length=1)
    unsupported_inference_flags: list[str] = Field(default_factory=list)
    stored_as_fact: Literal[False] = False
    status: ContextOutputStatus
    created_at: datetime
    updated_at: datetime


class InterviewerResonanceContext(BaseModel):
    schema_version: Literal["cmf.interviewer_resonance_context.v1"]
    resonance_context_id: UUID
    organization_id: UUID
    brand_id: UUID
    research_field_id: UUID
    operator_id: UUID
    authentic_curiosity: list[str] = Field(min_length=1)
    emotional_bridges: list[str] = Field(min_length=1)
    questions_to_avoid: list[str] = Field(min_length=1)
    opening_state: str = Field(min_length=1)
    small_reflection_zones: list[str] = Field(default_factory=list)
    refusal_to_fake: list[str] = Field(default_factory=list)
    evidence_ids: list[UUID] = Field(min_length=1)
    status: ContextOutputStatus
    created_at: datetime
    updated_at: datetime


class ContextCompilationReceipt(BaseModel):
    schema_version: Literal["cmf.context_compilation_receipt.v1"]
    context_compilation_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    research_field_id: UUID
    compiler_version: str = Field(min_length=1)
    input_evidence_ids: list[UUID] = Field(min_length=1)
    input_packet_hash: str = Field(min_length=1)
    source_hashes: list[str] = Field(default_factory=list)
    output_ids: dict[ContextArtifactKind, UUID] = Field(default_factory=dict)
    evaluator_results: list[str] = Field(default_factory=list)
    reviewer_state: str = Field(min_length=1)
    decision_code: str = Field(min_length=1)
    reviewer_actor_id: UUID | None = None
    written_at: datetime


class ContextArtifactSaturationPacket(BaseModel):
    schema_version: Literal["cmf.context_artifact_saturation_packet.v1"]
    organization_id: UUID
    brand_id: UUID
    guest_dossier_id: UUID
    audience_reality_brief_id: UUID
    context_premise_id: UUID
    trigger_map_id: UUID | None = None
    interviewer_resonance_context_id: UUID | None = None
    evidence_ids: list[UUID] = Field(min_length=1)
    context_compilation_receipt_ids: list[UUID] = Field(default_factory=list)


def new_inference(
    *,
    statement: str,
    evidence_ids: list[UUID],
    confidence: float,
    limitation: str | None = None,
) -> EvidenceBackedInference:
    return EvidenceBackedInference(
        schema_version="cmf.evidence_backed_inference.v1",
        inference_id=uuid4(),
        statement=statement,
        evidence_ids=evidence_ids,
        confidence=confidence,
        limitation=limitation,
    )


def new_context_compilation_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    research_field_id: UUID,
    compiler_version: str,
    input_evidence_ids: list[UUID],
    input_packet_hash: str,
    source_hashes: list[str],
    output_ids: dict[ContextArtifactKind, UUID],
    evaluator_results: list[str],
    reviewer_state: str,
    decision_code: str,
    reviewer_actor_id: UUID | None = None,
) -> ContextCompilationReceipt:
    return ContextCompilationReceipt(
        schema_version="cmf.context_compilation_receipt.v1",
        context_compilation_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        research_field_id=research_field_id,
        compiler_version=compiler_version,
        input_evidence_ids=input_evidence_ids,
        input_packet_hash=input_packet_hash,
        source_hashes=source_hashes,
        output_ids=output_ids,
        evaluator_results=evaluator_results,
        reviewer_state=reviewer_state,
        decision_code=decision_code,
        reviewer_actor_id=reviewer_actor_id,
        written_at=utc_now(),
    )
