"""Legacy orchestration intent contracts for TS-CMF-017."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from ccp_studio.contracts.orchestration import utc_now


class OrganismLayer(str, Enum):
    dna_truth = "dna_truth"
    rna_contextual_transcription = "rna_contextual_transcription"
    force = "force"
    delivery = "delivery"
    variation = "variation"
    phenotype = "phenotype"
    evaluation = "evaluation"
    outer_learning = "outer_learning"


class OrchestrationPacketRef(BaseModel):
    schema_version: Literal["cmf.orchestration_packet_ref.v1"]
    packet_name: str
    packet_contract: str
    required: bool = True


class GateRef(BaseModel):
    schema_version: Literal["cmf.gate_ref.v1"]
    gate_name: str
    gate_contract: str
    required: bool = True


class LegacyOrchestrationIntentRecord(BaseModel):
    schema_version: Literal["cmf.legacy_orchestration_intent_record.v1"]
    legacy_orchestration_intent_record_id: UUID
    migration_ledger_entry_id: UUID
    product_purpose: str
    organism_layer: OrganismLayer
    upstream_inputs: list[OrchestrationPacketRef] = Field(min_length=1)
    emitted_packets: list[OrchestrationPacketRef] = Field(min_length=1)
    downstream_consumers: list[str] = Field(min_length=1)
    required_gates: list[GateRef] = Field(min_length=1)
    failure_modes: list[str] = Field(min_length=1)
    proof_obligations: list[str] = Field(min_length=1)
    source_document_refs: list[str] = Field(min_length=1)
    typed_contract_or_registry_target: str
    reviewer_actor_id: UUID
    approved_at: datetime | None = None


class AuthorityOverlapReview(BaseModel):
    schema_version: Literal["cmf.authority_overlap_review.v1"]
    authority_overlap_review_id: UUID
    intent_record_ids: list[UUID] = Field(min_length=2)
    resolved_layer_assignments: dict[str, OrganismLayer]
    reviewer_actor_id: UUID
    decision: str
    decided_at: datetime


class OrchestrationIntentReceipt(BaseModel):
    schema_version: Literal["cmf.orchestration_intent_receipt.v1"]
    orchestration_intent_receipt_id: UUID
    legacy_orchestration_intent_record_id: UUID
    migration_ledger_entry_id: UUID
    decision_code: str
    evidence_refs: list[str] = Field(default_factory=list)
    reviewer_actor_id: UUID
    written_at: datetime


class InheritedOrchestrationGates(BaseModel):
    schema_version: Literal["cmf.inherited_orchestration_gates.v1"]
    downstream_ref: str
    legacy_orchestration_intent_record_id: UUID
    inherited_gate_names: list[str] = Field(min_length=1)
    proof_obligations: list[str] = Field(min_length=1)


def packet_ref(packet_name: str, packet_contract: str, required: bool = True) -> OrchestrationPacketRef:
    return OrchestrationPacketRef(
        schema_version="cmf.orchestration_packet_ref.v1",
        packet_name=packet_name,
        packet_contract=packet_contract,
        required=required,
    )


def gate_ref(gate_name: str, gate_contract: str, required: bool = True) -> GateRef:
    return GateRef(
        schema_version="cmf.gate_ref.v1",
        gate_name=gate_name,
        gate_contract=gate_contract,
        required=required,
    )


def new_orchestration_intent_receipt(
    *,
    record: LegacyOrchestrationIntentRecord,
    decision_code: str,
    evidence_refs: list[str],
) -> OrchestrationIntentReceipt:
    return OrchestrationIntentReceipt(
        schema_version="cmf.orchestration_intent_receipt.v1",
        orchestration_intent_receipt_id=uuid4(),
        legacy_orchestration_intent_record_id=record.legacy_orchestration_intent_record_id,
        migration_ledger_entry_id=record.migration_ledger_entry_id,
        decision_code=decision_code,
        evidence_refs=evidence_refs,
        reviewer_actor_id=record.reviewer_actor_id,
        written_at=utc_now(),
    )
