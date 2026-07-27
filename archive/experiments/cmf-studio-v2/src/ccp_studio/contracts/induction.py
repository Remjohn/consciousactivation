"""CRAL, DNA, and root-down induction rationale contracts for TS-CMF-028."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.research import SourceRole


class CRALMoment(str, Enum):
    relevant = "relevant"
    believable = "believable"
    undeniable = "undeniable"
    resonant = "resonant"
    surprising = "surprising"
    irrefutable = "irrefutable"
    relatable = "relatable"


class RationaleMode(str, Enum):
    full_depth = "full_depth"
    partial = "partial"
    shallow_supported = "shallow_supported"
    blocked_unsupported = "blocked_unsupported"


class InductionArtifactStatus(str, Enum):
    draft = "draft"
    compiled = "compiled"
    partial = "partial"
    blocked = "blocked"
    superseded = "superseded"


class SupportedPsychologyClaim(BaseModel):
    schema_version: Literal["cmf.supported_psychology_claim.v1"]
    claim_id: UUID
    statement: str = Field(min_length=1)
    claim_type: str = Field(min_length=1)
    evidence_ids: list[UUID] = Field(default_factory=list)
    source_roles: list[SourceRole] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    limitation: str = Field(min_length=1)
    rationale_mode: RationaleMode


class CRALFinding(BaseModel):
    schema_version: Literal["cmf.cral_finding.v1"]
    cral_finding_id: UUID
    organization_id: UUID
    brand_id: UUID
    research_field_id: UUID
    moment: CRALMoment
    signal: str = Field(min_length=1)
    source_role: SourceRole
    evidence_ids: list[UUID] = Field(min_length=1)
    confidence: float = Field(ge=0, le=1)
    contradiction_notes: list[str] = Field(default_factory=list)
    status: InductionArtifactStatus
    created_at: datetime


class EmotionalDNAProfile(BaseModel):
    schema_version: Literal["cmf.emotional_dna_profile.v1"]
    emotional_dna_profile_id: UUID
    organization_id: UUID
    brand_id: UUID
    guest_id: UUID | None = None
    research_field_id: UUID
    belief_content: list[SupportedPsychologyClaim] = Field(default_factory=list)
    emotional_path: list[SupportedPsychologyClaim] = Field(default_factory=list)
    suppression_markers: list[SupportedPsychologyClaim] = Field(default_factory=list)
    escalation_triggers: list[SupportedPsychologyClaim] = Field(default_factory=list)
    evidence_ids: list[UUID] = Field(default_factory=list)
    limitation: str | None = None
    status: InductionArtifactStatus
    created_at: datetime
    updated_at: datetime


class VoiceDNAProfile(BaseModel):
    schema_version: Literal["cmf.voice_dna_profile.v1"]
    voice_dna_profile_id: UUID
    organization_id: UUID
    brand_id: UUID
    guest_id: UUID | None = None
    research_field_id: UUID
    construction_mechanics: list[SupportedPsychologyClaim] = Field(default_factory=list)
    negative_space: list[SupportedPsychologyClaim] = Field(default_factory=list)
    normative_expression_targets: list[SupportedPsychologyClaim] = Field(default_factory=list)
    calibration_receipt_ids: list[UUID] = Field(default_factory=list)
    emotional_dna_profile_id: UUID | None = None
    evidence_ids: list[UUID] = Field(default_factory=list)
    limitation: str | None = None
    status: InductionArtifactStatus
    created_at: datetime
    updated_at: datetime


class InductionRationale(BaseModel):
    schema_version: Literal["cmf.induction_rationale.v1"]
    rationale_id: UUID
    organization_id: UUID
    brand_id: UUID
    planned_move_id: UUID
    pre_induction_plan_id: UUID
    interview_contract_id: UUID | None = None
    cral_finding_ids: list[UUID] = Field(default_factory=list)
    context_premise_id: UUID
    trigger_map_id: UUID
    emotional_dna_profile_id: UUID | None = None
    voice_dna_profile_id: UUID | None = None
    matrix_brief_id: UUID
    matrix_edge_product_id: UUID | None = None
    target_expression_state: list[str] = Field(min_length=1)
    intended_extraction_outcome: list[str] = Field(min_length=1)
    supported_claims: list[SupportedPsychologyClaim] = Field(default_factory=list)
    evidence_ids: list[UUID] = Field(default_factory=list)
    rationale_mode: RationaleMode
    support_limitations: list[str] = Field(default_factory=list)
    status: InductionArtifactStatus
    created_at: datetime
    updated_at: datetime


class InductionRationaleInspection(BaseModel):
    schema_version: Literal["cmf.induction_rationale_inspection.v1"]
    rationale_id: UUID
    planned_move_id: UUID
    cral_signals: list[str] = Field(default_factory=list)
    context_premise_id: UUID
    trigger_map_id: UUID
    emotional_dna_profile_id: UUID | None = None
    voice_dna_profile_id: UUID | None = None
    matrix_edge_product_id: UUID | None = None
    target_expression_state: list[str] = Field(default_factory=list)
    intended_extraction_outcome: list[str] = Field(default_factory=list)
    rationale_mode: RationaleMode
    support_limitations: list[str] = Field(default_factory=list)


class InductionRationaleReceipt(BaseModel):
    schema_version: Literal["cmf.induction_rationale_receipt.v1"]
    induction_rationale_receipt_id: UUID
    organization_id: UUID
    brand_id: UUID
    pre_induction_plan_id: UUID | None = None
    matrix_brief_id: UUID | None = None
    rationale_ids: list[UUID] = Field(default_factory=list)
    cral_finding_ids: list[UUID] = Field(default_factory=list)
    emotional_dna_profile_id: UUID | None = None
    voice_dna_profile_id: UUID | None = None
    rationale_mode: RationaleMode
    evidence_ids: list[UUID] = Field(default_factory=list)
    compiler_versions: dict[str, str] = Field(default_factory=dict)
    blocked_claims: list[str] = Field(default_factory=list)
    downstream_bindings: dict[str, list[UUID]] = Field(default_factory=dict)
    decision_code: str = Field(min_length=1)
    reviewer_actor_id: UUID | None = None
    written_at: datetime


def new_supported_claim(
    *,
    statement: str,
    claim_type: str,
    evidence_ids: list[UUID],
    source_roles: list[SourceRole],
    confidence: float,
    limitation: str,
    rationale_mode: RationaleMode,
) -> SupportedPsychologyClaim:
    return SupportedPsychologyClaim(
        schema_version="cmf.supported_psychology_claim.v1",
        claim_id=uuid4(),
        statement=statement,
        claim_type=claim_type,
        evidence_ids=evidence_ids,
        source_roles=source_roles,
        confidence=confidence,
        limitation=limitation,
        rationale_mode=rationale_mode,
    )


def new_induction_rationale_receipt(
    *,
    organization_id: UUID,
    brand_id: UUID,
    rationale_mode: RationaleMode,
    decision_code: str,
    pre_induction_plan_id: UUID | None = None,
    matrix_brief_id: UUID | None = None,
    rationale_ids: list[UUID] | None = None,
    cral_finding_ids: list[UUID] | None = None,
    emotional_dna_profile_id: UUID | None = None,
    voice_dna_profile_id: UUID | None = None,
    evidence_ids: list[UUID] | None = None,
    compiler_versions: dict[str, str] | None = None,
    blocked_claims: list[str] | None = None,
    downstream_bindings: dict[str, list[UUID]] | None = None,
    reviewer_actor_id: UUID | None = None,
) -> InductionRationaleReceipt:
    return InductionRationaleReceipt(
        schema_version="cmf.induction_rationale_receipt.v1",
        induction_rationale_receipt_id=uuid4(),
        organization_id=organization_id,
        brand_id=brand_id,
        pre_induction_plan_id=pre_induction_plan_id,
        matrix_brief_id=matrix_brief_id,
        rationale_ids=rationale_ids or [],
        cral_finding_ids=cral_finding_ids or [],
        emotional_dna_profile_id=emotional_dna_profile_id,
        voice_dna_profile_id=voice_dna_profile_id,
        rationale_mode=rationale_mode,
        evidence_ids=evidence_ids or [],
        compiler_versions=compiler_versions or {},
        blocked_claims=blocked_claims or [],
        downstream_bindings=downstream_bindings or {},
        decision_code=decision_code,
        reviewer_actor_id=reviewer_actor_id,
        written_at=utc_now(),
    )
