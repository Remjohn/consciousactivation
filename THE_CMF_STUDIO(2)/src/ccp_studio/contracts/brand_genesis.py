"""Brand Genesis intake and session contracts for TS-CMF-018."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class BrandGenesisSessionStatus(str, Enum):
    draft = "draft"
    ready = "ready"
    blocked = "blocked"
    running = "running"
    completed = "completed"


class VoiceDnaReferenceKind(str, Enum):
    migrated_registry_entry = "migrated_registry_entry"
    approved_calibration = "approved_calibration"
    raw_legacy_reference = "raw_legacy_reference"


class BrandSourceInput(BaseModel):
    schema_version: Literal["cmf.brand_source_input.v1"]
    source_artifact_ids: list[UUID] = Field(min_length=1)
    consent_record_version_id: UUID
    source_quality_receipt_ids: list[UUID] = Field(default_factory=list)
    source_notes: str | None = None


class VoiceDnaReference(BaseModel):
    schema_version: Literal["cmf.voice_dna_reference.v1"]
    voice_dna_reference_id: UUID
    reference_kind: VoiceDnaReferenceKind
    label: str = Field(min_length=1)
    approved: bool
    migration_ledger_entry_id: UUID | None = None
    registry_entry_id: UUID | None = None
    evidence_refs: list[str] = Field(default_factory=list)


class VisualConstitutionInput(BaseModel):
    schema_version: Literal["cmf.visual_constitution_input.v1"]
    visual_preferences: list[str] = Field(min_length=1)
    paper_cut_direction: str = Field(min_length=1)
    composition_preferences: list[str] = Field(min_length=1)
    style_constraints: list[str] = Field(default_factory=list)


class NegativeSpaceInput(BaseModel):
    schema_version: Literal["cmf.negative_space_input.v1"]
    forbidden_tone: list[str] = Field(min_length=1)
    forbidden_visual_motifs: list[str] = Field(default_factory=list)
    avoided_claims: list[str] = Field(default_factory=list)
    style_boundaries: list[str] = Field(default_factory=list)


class BrandGenesisMissingEvidenceReport(BaseModel):
    schema_version: Literal["cmf.brand_genesis_missing_evidence_report.v1"]
    brand_genesis_session_id: UUID
    organization_id: UUID
    brand_id: UUID
    missing_fields: list[str] = Field(default_factory=list)
    blocker_codes: list[str] = Field(default_factory=list)
    fabricated_defaults_used: bool = False
    created_at: datetime

    @property
    def complete(self) -> bool:
        return not self.missing_fields and not self.blocker_codes


class BrandGenesisSession(BaseModel):
    schema_version: Literal["cmf.brand_genesis_session.v1"]
    brand_genesis_session_id: UUID
    organization_id: UUID
    brand_id: UUID
    status: BrandGenesisSessionStatus
    brand_notes: str
    audience_summary: str
    offer_summary: str
    forbidden_tone: list[str]
    visual_preferences: list[str]
    voice_dna_references: list[VoiceDnaReference] = Field(default_factory=list)
    source_inputs: list[BrandSourceInput]
    visual_constitution_input: VisualConstitutionInput | None = None
    negative_space_input: NegativeSpaceInput | None = None
    storage_prefix: str
    output_brand_context_version_id: UUID | None = None
    last_missing_evidence_report_id: UUID | None = None
    created_by_actor_id: UUID
    created_at: datetime
    updated_at: datetime


class GenesisStartReceipt(BaseModel):
    schema_version: Literal["cmf.genesis_start_receipt.v1"]
    genesis_start_receipt_id: UUID
    brand_genesis_session_id: UUID
    organization_id: UUID
    brand_id: UUID
    actor_id: UUID
    decision_code: str
    consent_record_version_ids: list[UUID] = Field(default_factory=list)
    source_artifact_ids: list[UUID] = Field(default_factory=list)
    voice_dna_reference_ids: list[UUID] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    storage_path: str
    written_at: datetime


class BrandGenesisWorkflowRun(BaseModel):
    schema_version: Literal["cmf.brand_genesis_workflow_run.v1"]
    workflow_run_id: UUID
    brand_genesis_session_id: UUID
    organization_id: UUID
    brand_id: UUID
    start_receipt_id: UUID
    status: Literal["started"]
    started_at: datetime


class CreateBrandGenesisSessionCommand(BaseModel):
    brand_notes: str
    audience_summary: str
    offer_summary: str
    forbidden_tone: list[str]
    visual_preferences: list[str]
    voice_dna_references: list[VoiceDnaReference]
    source_inputs: list[BrandSourceInput]
    visual_constitution_input: VisualConstitutionInput | None = None
    negative_space_input: NegativeSpaceInput | None = None


class ValidateBrandGenesisIntakeCommand(BaseModel):
    brand_genesis_session_id: UUID


class StartBrandGenesisWorkflowCommand(BaseModel):
    brand_genesis_session_id: UUID


class BlockBrandGenesisForConsentCommand(BaseModel):
    brand_genesis_session_id: UUID
    decision_code: str
    blocked_scope: str | None = None


def brand_genesis_storage_prefix(brand_id: UUID, brand_genesis_session_id: UUID) -> str:
    return f"brands/{brand_id}/brand-genesis/{brand_genesis_session_id}"


def new_brand_genesis_session(
    *,
    organization_id: UUID,
    brand_id: UUID,
    brand_notes: str,
    audience_summary: str,
    offer_summary: str,
    forbidden_tone: list[str],
    visual_preferences: list[str],
    voice_dna_references: list[VoiceDnaReference],
    source_inputs: list[BrandSourceInput],
    visual_constitution_input: VisualConstitutionInput | None,
    negative_space_input: NegativeSpaceInput | None,
    created_by_actor_id: UUID,
) -> BrandGenesisSession:
    now = utc_now()
    session_id = uuid4()
    return BrandGenesisSession(
        schema_version="cmf.brand_genesis_session.v1",
        brand_genesis_session_id=session_id,
        organization_id=organization_id,
        brand_id=brand_id,
        status=BrandGenesisSessionStatus.draft,
        brand_notes=brand_notes,
        audience_summary=audience_summary,
        offer_summary=offer_summary,
        forbidden_tone=forbidden_tone,
        visual_preferences=visual_preferences,
        voice_dna_references=voice_dna_references,
        source_inputs=source_inputs,
        visual_constitution_input=visual_constitution_input,
        negative_space_input=negative_space_input,
        storage_prefix=brand_genesis_storage_prefix(brand_id, session_id),
        created_by_actor_id=created_by_actor_id,
        created_at=now,
        updated_at=now,
    )


def new_genesis_start_receipt(
    *,
    session: BrandGenesisSession,
    actor_id: UUID,
    decision_code: str,
    evidence_refs: list[str],
) -> GenesisStartReceipt:
    return GenesisStartReceipt(
        schema_version="cmf.genesis_start_receipt.v1",
        genesis_start_receipt_id=uuid4(),
        brand_genesis_session_id=session.brand_genesis_session_id,
        organization_id=session.organization_id,
        brand_id=session.brand_id,
        actor_id=actor_id,
        decision_code=decision_code,
        consent_record_version_ids=[
            source_input.consent_record_version_id for source_input in session.source_inputs
        ],
        source_artifact_ids=[
            artifact_id
            for source_input in session.source_inputs
            for artifact_id in source_input.source_artifact_ids
        ],
        voice_dna_reference_ids=[
            reference.voice_dna_reference_id for reference in session.voice_dna_references
        ],
        evidence_refs=evidence_refs,
        storage_path=f"{session.storage_prefix}/receipts/genesis-start.json",
        written_at=utc_now(),
    )
