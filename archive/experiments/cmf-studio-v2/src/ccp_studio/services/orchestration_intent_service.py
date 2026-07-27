"""Legacy orchestration intent service for TS-CMF-017."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ccp_studio.contracts.legacy_orchestration import (
    AuthorityOverlapReview,
    GateRef,
    InheritedOrchestrationGates,
    LegacyOrchestrationIntentRecord,
    OrchestrationPacketRef,
    OrganismLayer,
    new_orchestration_intent_receipt,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.legacy_orchestration_intent_records import (
    InMemoryLegacyOrchestrationIntentRepository,
)


class OrchestrationIntentError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


STYLE_ONLY_TERMS = ["style advice", "vibe", "better storytelling", "prompt snippet", "visual mood"]


@dataclass
class OrchestrationIntentService:
    repository: InMemoryLegacyOrchestrationIntentRepository = field(default_factory=InMemoryLegacyOrchestrationIntentRepository)

    def create_intent_record(
        self,
        *,
        migration_ledger_entry_id: UUID,
        product_purpose: str,
        organism_layer: OrganismLayer,
        upstream_inputs: list[OrchestrationPacketRef],
        emitted_packets: list[OrchestrationPacketRef],
        downstream_consumers: list[str],
        required_gates: list[GateRef],
        failure_modes: list[str],
        proof_obligations: list[str],
        source_document_refs: list[str],
        typed_contract_or_registry_target: str,
        reviewer_actor_id: UUID,
    ) -> LegacyOrchestrationIntentRecord:
        self._validate_intent(
            product_purpose=product_purpose,
            upstream_inputs=upstream_inputs,
            emitted_packets=emitted_packets,
            downstream_consumers=downstream_consumers,
            required_gates=required_gates,
            failure_modes=failure_modes,
            proof_obligations=proof_obligations,
            source_document_refs=source_document_refs,
            typed_contract_or_registry_target=typed_contract_or_registry_target,
        )
        record = LegacyOrchestrationIntentRecord(
            schema_version="cmf.legacy_orchestration_intent_record.v1",
            legacy_orchestration_intent_record_id=uuid4(),
            migration_ledger_entry_id=migration_ledger_entry_id,
            product_purpose=product_purpose,
            organism_layer=organism_layer,
            upstream_inputs=upstream_inputs,
            emitted_packets=emitted_packets,
            downstream_consumers=downstream_consumers,
            required_gates=required_gates,
            failure_modes=failure_modes,
            proof_obligations=proof_obligations,
            source_document_refs=source_document_refs,
            typed_contract_or_registry_target=typed_contract_or_registry_target,
            reviewer_actor_id=reviewer_actor_id,
        )
        self.repository.put_record(record)
        self.repository.put_receipt(
            new_orchestration_intent_receipt(
                record=record,
                decision_code="ORCHESTRATION_INTENT_CREATED",
                evidence_refs=source_document_refs,
            )
        )
        return record

    def approve_intent_record(self, *, intent_record_id: UUID) -> LegacyOrchestrationIntentRecord:
        record = self._record(intent_record_id)
        approved = record.model_copy(update={"approved_at": utc_now()})
        self.repository.put_record(approved)
        self.repository.put_receipt(
            new_orchestration_intent_receipt(
                record=approved,
                decision_code="ORCHESTRATION_INTENT_APPROVED",
                evidence_refs=[approved.typed_contract_or_registry_target],
            )
        )
        return approved

    def resolve_authority_overlap(
        self,
        *,
        intent_record_ids: list[UUID],
        resolved_layer_assignments: dict[str, OrganismLayer],
        reviewer_actor_id: UUID,
        decision: str,
    ) -> AuthorityOverlapReview:
        for record_id in intent_record_ids:
            self._record(record_id)
        review = AuthorityOverlapReview(
            schema_version="cmf.authority_overlap_review.v1",
            authority_overlap_review_id=uuid4(),
            intent_record_ids=intent_record_ids,
            resolved_layer_assignments=resolved_layer_assignments,
            reviewer_actor_id=reviewer_actor_id,
            decision=decision,
            decided_at=utc_now(),
        )
        return self.repository.put_overlap_review(review)

    def inherit_gates_for_downstream(self, *, intent_record_id: UUID, downstream_ref: str) -> InheritedOrchestrationGates:
        record = self._record(intent_record_id)
        if record.approved_at is None:
            raise OrchestrationIntentError("ORCHESTRATION_INTENT_APPROVAL_REQUIRED", "Intent record must be approved before inheritance.")
        inherited = InheritedOrchestrationGates(
            schema_version="cmf.inherited_orchestration_gates.v1",
            downstream_ref=downstream_ref,
            legacy_orchestration_intent_record_id=record.legacy_orchestration_intent_record_id,
            inherited_gate_names=[gate.gate_name for gate in record.required_gates],
            proof_obligations=record.proof_obligations,
        )
        return self.repository.put_inherited_gates(inherited)

    def validate_downstream_reference(self, *, intent_record_id: UUID | None) -> LegacyOrchestrationIntentRecord:
        if intent_record_id is None or intent_record_id not in self.repository.records:
            raise OrchestrationIntentError(
                "ORCHESTRATION_INTENT_RECORD_REQUIRED",
                "Downstream specs cannot cite an orchestration-bearing module without an intent record.",
            )
        return self._record(intent_record_id)

    @staticmethod
    def _validate_intent(
        *,
        product_purpose: str,
        upstream_inputs: list[OrchestrationPacketRef],
        emitted_packets: list[OrchestrationPacketRef],
        downstream_consumers: list[str],
        required_gates: list[GateRef],
        failure_modes: list[str],
        proof_obligations: list[str],
        source_document_refs: list[str],
        typed_contract_or_registry_target: str,
    ) -> None:
        lowered = product_purpose.lower()
        if any(term in lowered for term in STYLE_ONLY_TERMS):
            raise OrchestrationIntentError("ORCHESTRATION_INTENT_FLATTENED", "Style-only summaries are not orchestration intent.")
        if not product_purpose:
            raise OrchestrationIntentError("ORCHESTRATION_PURPOSE_REQUIRED", "Product purpose is required.")
        if not upstream_inputs or not emitted_packets:
            raise OrchestrationIntentError("ORCHESTRATION_PACKETS_REQUIRED", "Input and emitted packet refs are required.")
        if not downstream_consumers or not required_gates or not failure_modes or not proof_obligations:
            raise OrchestrationIntentError("ORCHESTRATION_PROOF_REQUIRED", "Consumers, gates, failures, and proof obligations are required.")
        if not source_document_refs:
            raise OrchestrationIntentError("SOURCE_DOCUMENT_REQUIRED", "Source document refs are required.")
        if not typed_contract_or_registry_target:
            raise OrchestrationIntentError("ORCHESTRATION_TYPED_TARGET_REQUIRED", "Typed target is required.")

    def _record(self, intent_record_id: UUID) -> LegacyOrchestrationIntentRecord:
        record = self.repository.records.get(intent_record_id)
        if record is None:
            raise OrchestrationIntentError("ORCHESTRATION_INTENT_RECORD_REQUIRED", "Intent record is required.")
        return record
