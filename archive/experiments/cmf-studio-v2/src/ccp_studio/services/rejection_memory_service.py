"""Rejected candidate and coalition-fatality memory service for TS-CMF-035."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.consent import ConsentRecordVersion, ConsentVersionStatus
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.rejection_memory import (
    CoalitionFatalityRecord,
    MemoryAdmissionCandidate,
    MemoryAdmissionCandidateStatus,
    NegativeEvidenceKind,
    NegativeEvidenceRef,
    RejectedExpressionCandidate,
    RejectedRouteAttempt,
    RejectionCategory,
    RejectionReceipt,
    new_rejection_receipt,
)
from ccp_studio.repositories.consent_record_versions import InMemoryConsentRepository
from ccp_studio.repositories.rejection_memory import InMemoryRejectionMemoryRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.extraction_service import ExtractionService
from ccp_studio.services.routing_service import RoutingService


class RejectionMemoryServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class RejectionMemoryService:
    extraction_service: ExtractionService
    routing_service: RoutingService
    consent_repository: InMemoryConsentRepository | None = None
    repository: InMemoryRejectionMemoryRepository = field(default_factory=InMemoryRejectionMemoryRepository)

    def record_rejected_expression_candidate(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        candidate_id: UUID,
        category: RejectionCategory,
        reason: str,
        reviewer_id: UUID,
        route_attempt_receipt_id: UUID | None = None,
        consent_record_version_id: UUID | None = None,
        sensitive_material: bool = False,
    ) -> RejectionReceipt:
        candidate = self.extraction_service.repository.candidates.get(candidate_id)
        if candidate is None:
            raise RejectionMemoryServiceError("EXPRESSION_MOMENT_CANDIDATE_REQUIRED", "Candidate is required.")
        source_refs = [
            f"candidate:{candidate.candidate_id}",
            f"source_artifact:{candidate.source_artifact_id}",
            f"transcript_revision:{candidate.transcript_revision_id}",
            *[f"transcript_segment:{item}" for item in candidate.transcript_segment_ids],
        ]
        consent_compatible = self._consent_compatible(consent_record_version_id, sensitive_material=sensitive_material)
        quarantined = sensitive_material or not consent_compatible
        usable = consent_compatible and not quarantined
        record = self.repository.put_rejected_candidate(
            RejectedExpressionCandidate(
                schema_version="cmf.rejected_expression_candidate.v1",
                rejected_candidate_id=uuid4(),
                candidate_id=candidate.candidate_id,
                expression_session_id=candidate.expression_session_id,
                category=category,
                reason=reason,
                source_reference_ids=source_refs,
                route_attempt_receipt_id=route_attempt_receipt_id,
                reviewer_id=reviewer_id,
                consent_record_version_id=consent_record_version_id,
                consent_compatible=consent_compatible,
                quarantined=quarantined,
                usable_as_negative_evidence=usable,
                created_at=utc_now(),
            )
        )
        return self._write_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            category=category,
            source_refs=source_refs,
            reviewer_id=reviewer_id,
            rejected_candidate_id=record.rejected_candidate_id,
            consent_record_version_id=consent_record_version_id,
            consent_compatible=consent_compatible,
            quarantined=quarantined,
            negative_evidence_eligible=usable,
            decision_code="REJECTED_CANDIDATE_QUARANTINED" if quarantined else "REJECTED_CANDIDATE_RECORDED",
            evidence_refs=[*source_refs, f"reason:{reason}"],
        )

    def record_rejected_route_attempt(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        asset_route_receipt_id: UUID,
        category: RejectionCategory,
        reviewer_id: UUID,
        consent_record_version_id: UUID | None = None,
        sensitive_material: bool = False,
    ) -> RejectionReceipt:
        receipt = self.routing_service.repository.receipts.get(asset_route_receipt_id)
        if receipt is None:
            raise RejectionMemoryServiceError("ASSET_ROUTE_RECEIPT_REQUIRED", "Route receipt is required.")
        consent_compatible = self._consent_compatible(consent_record_version_id, sensitive_material=sensitive_material)
        quarantined = sensitive_material or not consent_compatible
        usable = consent_compatible and not quarantined and bool(receipt.rejected_route_ids or receipt.unsupported_format_rejection_ids)
        record = self.repository.put_rejected_route(
            RejectedRouteAttempt(
                schema_version="cmf.rejected_route_attempt.v1",
                rejected_route_attempt_id=uuid4(),
                asset_route_receipt_id=asset_route_receipt_id,
                expression_moment_id=receipt.expression_moment_id,
                route_refs=receipt.registry_entry_refs,
                category=category,
                source_gap=receipt.route_rationale,
                route_fit_score=receipt.route_fit_score,
                consent_record_version_id=consent_record_version_id,
                consent_compatible=consent_compatible,
                quarantined=quarantined,
                usable_as_negative_evidence=usable,
                created_at=utc_now(),
            )
        )
        return self._write_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            category=category,
            source_refs=[f"asset_route_receipt:{asset_route_receipt_id}", *receipt.source_support_evidence],
            reviewer_id=reviewer_id,
            rejected_route_attempt_id=record.rejected_route_attempt_id,
            consent_record_version_id=consent_record_version_id,
            consent_compatible=consent_compatible,
            quarantined=quarantined,
            negative_evidence_eligible=usable,
            decision_code="REJECTED_ROUTE_QUARANTINED" if quarantined else "REJECTED_ROUTE_RECORDED",
            evidence_refs=[f"asset_route_receipt:{asset_route_receipt_id}", f"decision:{receipt.decision_code}"],
        )

    def record_coalition_fatality(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        rejection_receipt_id: UUID,
        reviewer_id: UUID,
        failure_observation: str,
        downstream_stage: str,
        primitive_candidate_ids: list[UUID] | None = None,
        matrix_brief_id: UUID | None = None,
        edge_product_id: UUID | None = None,
    ) -> RejectionReceipt:
        prior_receipt = self._receipt(rejection_receipt_id)
        usable = prior_receipt.negative_evidence_eligible and not prior_receipt.quarantined
        record = self.repository.put_coalition_fatality(
            CoalitionFatalityRecord(
                schema_version="cmf.coalition_fatality_record.v1",
                coalition_fatality_id=uuid4(),
                matrix_brief_id=matrix_brief_id,
                primitive_candidate_ids=primitive_candidate_ids or [],
                edge_product_id=edge_product_id,
                failure_observation=failure_observation,
                downstream_stage=downstream_stage,
                rejection_receipt_id=rejection_receipt_id,
                usable_as_negative_evidence=usable,
                created_at=utc_now(),
            )
        )
        return self._write_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            category=RejectionCategory.coalition_fatality,
            source_refs=[f"rejection_receipt:{rejection_receipt_id}"],
            reviewer_id=reviewer_id,
            coalition_fatality_id=record.coalition_fatality_id,
            consent_record_version_id=prior_receipt.consent_record_version_id,
            consent_compatible=prior_receipt.consent_compatible,
            quarantined=prior_receipt.quarantined,
            negative_evidence_eligible=usable,
            decision_code="COALITION_FATALITY_RECORDED",
            evidence_refs=[f"coalition_fatality:{record.coalition_fatality_id}", f"observation:{failure_observation}"],
        )

    def quarantine_rejected_material(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        rejection_receipt_id: UUID,
        reviewer_id: UUID,
        reason: str,
    ) -> RejectionReceipt:
        prior = self._receipt(rejection_receipt_id)
        if prior.rejected_candidate_id and prior.rejected_candidate_id in self.repository.rejected_candidates:
            candidate = self.repository.rejected_candidates[prior.rejected_candidate_id]
            self.repository.put_rejected_candidate(
                candidate.model_copy(update={"quarantined": True, "usable_as_negative_evidence": False})
            )
        if prior.rejected_route_attempt_id and prior.rejected_route_attempt_id in self.repository.rejected_routes:
            route = self.repository.rejected_routes[prior.rejected_route_attempt_id]
            self.repository.put_rejected_route(
                route.model_copy(update={"quarantined": True, "usable_as_negative_evidence": False})
            )
        return self._write_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            category=prior.category,
            source_refs=prior.source_refs,
            reviewer_id=reviewer_id,
            rejected_candidate_id=prior.rejected_candidate_id,
            rejected_route_attempt_id=prior.rejected_route_attempt_id,
            coalition_fatality_id=prior.coalition_fatality_id,
            consent_record_version_id=prior.consent_record_version_id,
            consent_compatible=prior.consent_compatible,
            quarantined=True,
            negative_evidence_eligible=False,
            decision_code="REJECTED_MATERIAL_QUARANTINED",
            evidence_refs=[f"prior_rejection_receipt:{rejection_receipt_id}", f"reason:{reason}"],
        )

    def reference_negative_evidence(
        self,
        *,
        rejection_receipt_id: UUID,
        compiler_or_evaluator: str,
        usage_purpose: str,
    ) -> NegativeEvidenceRef:
        receipt = self._receipt(rejection_receipt_id)
        if not receipt.negative_evidence_eligible or receipt.quarantined:
            raise RejectionMemoryServiceError("NEGATIVE_EVIDENCE_NOT_ELIGIBLE", "Rejected material is quarantined or ineligible.")
        kind, source_record_id = self._source_record_for_receipt(receipt)
        return self.repository.put_negative_evidence_ref(
            NegativeEvidenceRef(
                schema_version="cmf.negative_evidence_ref.v1",
                negative_evidence_ref_id=uuid4(),
                evidence_kind=kind,
                source_record_id=source_record_id,
                rejection_receipt_id=rejection_receipt_id,
                compiler_or_evaluator=compiler_or_evaluator,
                usage_purpose=usage_purpose,
                evidence_refs=receipt.evidence_refs,
                truth_admission_blocked=True,
                cited_at=utc_now(),
            )
        )

    def propose_memory_admission_from_rejection(
        self,
        *,
        rejection_receipt_id: UUID,
        proposed_memory_scope: str,
        reason: str,
    ) -> MemoryAdmissionCandidate:
        receipt = self._receipt(rejection_receipt_id)
        if receipt.quarantined:
            raise RejectionMemoryServiceError("MEMORY_PROPOSAL_QUARANTINED", "Quarantined material cannot propose memory admission.")
        _kind, source_record_id = self._source_record_for_receipt(receipt)
        return self.repository.put_memory_admission_candidate(
            MemoryAdmissionCandidate(
                schema_version="cmf.memory_admission_candidate.v1",
                memory_admission_candidate_id=uuid4(),
                source_record_id=source_record_id,
                rejection_receipt_id=rejection_receipt_id,
                proposed_memory_scope=proposed_memory_scope,
                reason=reason,
                evidence_refs=receipt.evidence_refs,
                status=MemoryAdmissionCandidateStatus.proposed_requires_memory_gate,
                explicit_memory_gate_required=True,
                auto_admitted_to_memory=False,
                proposed_at=utc_now(),
            )
        )

    def export_failure_corpus_refs(self) -> list[NegativeEvidenceRef]:
        return [
            ref
            for ref in self.repository.negative_evidence_refs.values()
            if self.repository.receipts[ref.rejection_receipt_id].negative_evidence_eligible
            and not self.repository.receipts[ref.rejection_receipt_id].quarantined
        ]

    def _write_receipt(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        category: RejectionCategory,
        source_refs: list[str],
        consent_compatible: bool,
        quarantined: bool,
        negative_evidence_eligible: bool,
        decision_code: str,
        evidence_refs: list[str],
        reviewer_id: UUID | None = None,
        rejected_candidate_id: UUID | None = None,
        rejected_route_attempt_id: UUID | None = None,
        coalition_fatality_id: UUID | None = None,
        consent_record_version_id: UUID | None = None,
    ) -> RejectionReceipt:
        return self.repository.put_receipt(
            new_rejection_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                category=category,
                source_refs=source_refs,
                reviewer_id=reviewer_id,
                rejected_candidate_id=rejected_candidate_id,
                rejected_route_attempt_id=rejected_route_attempt_id,
                coalition_fatality_id=coalition_fatality_id,
                consent_record_version_id=consent_record_version_id,
                consent_compatible=consent_compatible,
                quarantined=quarantined,
                negative_evidence_eligible=negative_evidence_eligible,
                decision_code=decision_code,
                evidence_refs=evidence_refs,
            )
        )

    def _consent_compatible(self, consent_record_version_id: UUID | None, *, sensitive_material: bool) -> bool:
        if consent_record_version_id is None:
            return not sensitive_material
        if self.consent_repository is None:
            return False
        version: ConsentRecordVersion | None = self.consent_repository.versions.get(consent_record_version_id)
        if version is None or version.status != ConsentVersionStatus.active:
            return False
        return bool(version.scope.source_storage_allowed and version.scope.reuse_allowed and version.scope.retention_allowed)

    def _receipt(self, rejection_receipt_id: UUID) -> RejectionReceipt:
        receipt = self.repository.receipts.get(rejection_receipt_id)
        if receipt is None:
            raise RejectionMemoryServiceError("REJECTION_RECEIPT_REQUIRED", "Rejection receipt is required.")
        return receipt

    @staticmethod
    def _source_record_for_receipt(receipt: RejectionReceipt) -> tuple[NegativeEvidenceKind, UUID]:
        if receipt.rejected_candidate_id is not None:
            return NegativeEvidenceKind.rejected_candidate, receipt.rejected_candidate_id
        if receipt.rejected_route_attempt_id is not None:
            return NegativeEvidenceKind.rejected_route, receipt.rejected_route_attempt_id
        if receipt.coalition_fatality_id is not None:
            return NegativeEvidenceKind.coalition_fatality, receipt.coalition_fatality_id
        raise RejectionMemoryServiceError("REJECTION_SOURCE_RECORD_REQUIRED", "Receipt lacks a source rejection record.")


@dataclass
class RejectionMemoryCommandHandler:
    command_type: str
    service: RejectionMemoryService
    aggregate_type: str = "rejection_memory"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "reviewer"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "RecordRejectedExpressionCandidateCommand":
            return self.service.record_rejected_expression_candidate(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                candidate_id=UUID(payload["candidate_id"]),
                category=RejectionCategory(payload["category"]),
                reason=payload["reason"],
                reviewer_id=envelope.actor.actor_id,
                route_attempt_receipt_id=UUID(payload["route_attempt_receipt_id"]) if payload.get("route_attempt_receipt_id") else None,
                consent_record_version_id=UUID(payload["consent_record_version_id"]) if payload.get("consent_record_version_id") else None,
                sensitive_material=payload.get("sensitive_material", False),
            ).model_dump(mode="json")
        if self.command_type == "RecordRejectedRouteAttemptCommand":
            return self.service.record_rejected_route_attempt(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                asset_route_receipt_id=UUID(payload["asset_route_receipt_id"]),
                category=RejectionCategory(payload["category"]),
                reviewer_id=envelope.actor.actor_id,
                consent_record_version_id=UUID(payload["consent_record_version_id"]) if payload.get("consent_record_version_id") else None,
                sensitive_material=payload.get("sensitive_material", False),
            ).model_dump(mode="json")
        if self.command_type == "RecordCoalitionFatalityCommand":
            return self.service.record_coalition_fatality(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                rejection_receipt_id=UUID(payload["rejection_receipt_id"]),
                reviewer_id=envelope.actor.actor_id,
                failure_observation=payload["failure_observation"],
                downstream_stage=payload["downstream_stage"],
                primitive_candidate_ids=[UUID(item) for item in payload.get("primitive_candidate_ids", [])],
                matrix_brief_id=UUID(payload["matrix_brief_id"]) if payload.get("matrix_brief_id") else None,
                edge_product_id=UUID(payload["edge_product_id"]) if payload.get("edge_product_id") else None,
            ).model_dump(mode="json")
        if self.command_type == "QuarantineRejectedMaterialCommand":
            return self.service.quarantine_rejected_material(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                rejection_receipt_id=UUID(payload["rejection_receipt_id"]),
                reviewer_id=envelope.actor.actor_id,
                reason=payload["reason"],
            ).model_dump(mode="json")
        if self.command_type == "ReferenceNegativeEvidenceCommand":
            return self.service.reference_negative_evidence(
                rejection_receipt_id=UUID(payload["rejection_receipt_id"]),
                compiler_or_evaluator=payload["compiler_or_evaluator"],
                usage_purpose=payload["usage_purpose"],
            ).model_dump(mode="json")
        if self.command_type == "ProposeMemoryAdmissionFromRejectionCommand":
            return self.service.propose_memory_admission_from_rejection(
                rejection_receipt_id=UUID(payload["rejection_receipt_id"]),
                proposed_memory_scope=payload["proposed_memory_scope"],
                reason=payload["reason"],
            ).model_dump(mode="json")
        raise RejectionMemoryServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("candidate_id") or payload.get("asset_route_receipt_id") or payload.get("rejection_receipt_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_rejection_memory_command_handlers(bus: CommandBus, service: RejectionMemoryService) -> None:
    for command_type in [
        "RecordRejectedExpressionCandidateCommand",
        "RecordRejectedRouteAttemptCommand",
        "RecordCoalitionFatalityCommand",
        "QuarantineRejectedMaterialCommand",
        "ReferenceNegativeEvidenceCommand",
        "ProposeMemoryAdmissionFromRejectionCommand",
    ]:
        bus.register_handler(RejectionMemoryCommandHandler(command_type=command_type, service=service))
