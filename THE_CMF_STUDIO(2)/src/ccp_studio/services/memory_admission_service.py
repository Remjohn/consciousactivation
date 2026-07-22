"""Evidence-backed memory admission service for TS-CMF-056."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.consent import ConsentVersionStatus
from ccp_studio.contracts.memory_admission import (
    MemoryAdmissionCandidate,
    MemoryAdmissionDomainEvent,
    MemoryAdmissionPolicyResult,
    MemoryAdmissionReceipt,
    MemoryClaimScope,
    MemoryEvent,
    MemoryEventStatus,
    MemoryEventType,
    MemoryEvidenceRef,
    MemoryPolicyDecision,
    MemoryScope,
    MemoryUsageCitation,
    new_memory_admission_receipt,
    new_memory_event,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.consent_record_versions import InMemoryConsentRepository
from ccp_studio.repositories.memory_admission import InMemoryMemoryAdmissionRepository
from ccp_studio.services.command_bus import CommandBus


MEMORY_REVIEW_ROLES = {"owner", "admin", "reviewer", "production_steward", "operator"}
GENERIC_MEMORY_PATTERNS = {
    "this brand likes bold claims",
    "make it more authentic",
    "the guest is inspiring",
    "use emotional storytelling",
}


class MemoryAdmissionError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class MemoryAdmissionService:
    consent_repository: InMemoryConsentRepository | None = None
    repository: InMemoryMemoryAdmissionRepository = field(default_factory=InMemoryMemoryAdmissionRepository)
    confidence_threshold: float = 0.6

    def propose_memory_admission(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        memory_type: MemoryEventType | str,
        proposed_from_event_id: str,
        proposed_statement: str,
        evidence_refs: list[MemoryEvidenceRef | dict[str, Any]],
        confidence: float,
        scope: MemoryScope | str,
        consent_record_version_id: UUID | None,
        consent_compatible: bool,
        provenance_summary: str,
        proposed_by_actor_id: UUID,
        originating_route_ref: str | None = None,
        downstream_usage_constraints: list[str] | None = None,
        idempotency_key: str | None = None,
    ) -> MemoryAdmissionCandidate:
        if idempotency_key:
            prior = self.repository.candidate_for_idempotency(organization_id, brand_id, idempotency_key)
            if prior:
                return prior
        refs = [self._evidence_ref(ref) for ref in evidence_refs]
        candidate = MemoryAdmissionCandidate(
            schema_version="cmf.memory_admission_candidate.v1",
            candidate_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            memory_type=MemoryEventType(memory_type),
            proposed_from_event_id=proposed_from_event_id,
            proposed_statement=proposed_statement,
            evidence_refs=refs,
            confidence=confidence,
            scope=MemoryScope(scope),
            consent_record_version_id=consent_record_version_id,
            consent_compatible=consent_compatible,
            originating_route_ref=originating_route_ref,
            provenance_summary=provenance_summary,
            proposed_by_actor_id=proposed_by_actor_id,
            downstream_usage_constraints=downstream_usage_constraints or ["must_cite_memory_event_and_evidence_refs"],
            created_at=utc_now(),
        )
        self.repository.put_candidate(candidate, idempotency_key=idempotency_key)
        self._event("MemoryAdmissionProposed", candidate, {"memory_type": candidate.memory_type.value, "scope": candidate.scope.value})
        return candidate

    def validate_memory_evidence(self, candidate_id: UUID) -> MemoryPolicyDecision:
        candidate = self._candidate(candidate_id)
        decision = self._policy(candidate)
        self._event("MemoryEvidenceValidated", candidate, {"evidence_valid": decision.evidence_valid, "blockers": decision.blockers})
        return decision

    def validate_memory_consent(self, candidate_id: UUID) -> MemoryPolicyDecision:
        candidate = self._candidate(candidate_id)
        decision = self._policy(candidate)
        self._event("MemoryConsentValidated", candidate, {"consent_valid": decision.consent_valid, "blockers": decision.blockers})
        return decision

    def approve_memory_admission(
        self,
        *,
        candidate_id: UUID,
        reviewer_id: UUID,
        role_ids: list[str],
        idempotency_key: str,
    ) -> MemoryAdmissionReceipt:
        prior = self.repository.receipt_for_idempotency(candidate_id, "approve", idempotency_key)
        if prior:
            return prior
        self._assert_memory_role(role_ids)
        candidate = self._candidate(candidate_id)
        decision = self._policy(candidate)
        if decision.result == MemoryAdmissionPolicyResult.approved:
            event = self.repository.put_memory_event(new_memory_event(candidate=candidate, status=MemoryEventStatus.approved, approved_by=reviewer_id))
            result = MemoryAdmissionPolicyResult.approved
            event_type = "MemoryAdmissionApproved"
        elif not decision.consent_valid:
            event = self.repository.put_memory_event(new_memory_event(candidate=candidate, status=MemoryEventStatus.quarantined, approved_by=None))
            result = MemoryAdmissionPolicyResult.quarantined
            event_type = "MemoryCandidateQuarantined"
        else:
            event = self.repository.put_memory_event(new_memory_event(candidate=candidate, status=MemoryEventStatus.rejected, approved_by=None))
            result = MemoryAdmissionPolicyResult.rejected
            event_type = "MemoryAdmissionRejected"
        receipt = self.repository.put_receipt(
            new_memory_admission_receipt(
                candidate=candidate,
                policy_result=result,
                memory_event_id=event.memory_event_id,
                reviewer_id=reviewer_id,
                blocker_codes=decision.blockers,
            ),
            action="approve",
            idempotency_key=idempotency_key,
        )
        self._event(event_type, candidate, {"memory_event_id": str(event.memory_event_id), "receipt_id": str(receipt.memory_admission_receipt_id)})
        return receipt

    def reject_memory_admission(
        self,
        *,
        candidate_id: UUID,
        reviewer_id: UUID,
        role_ids: list[str],
        reason: str,
        idempotency_key: str,
    ) -> MemoryAdmissionReceipt:
        prior = self.repository.receipt_for_idempotency(candidate_id, "reject", idempotency_key)
        if prior:
            return prior
        self._assert_memory_role(role_ids)
        candidate = self._candidate(candidate_id)
        event = self.repository.put_memory_event(new_memory_event(candidate=candidate, status=MemoryEventStatus.rejected, approved_by=None))
        receipt = self.repository.put_receipt(
            new_memory_admission_receipt(
                candidate=candidate,
                policy_result=MemoryAdmissionPolicyResult.rejected,
                memory_event_id=event.memory_event_id,
                reviewer_id=reviewer_id,
                blocker_codes=[f"operator_rejected:{reason}"],
            ),
            action="reject",
            idempotency_key=idempotency_key,
        )
        self._event("MemoryAdmissionRejected", candidate, {"reason": reason, "receipt_id": str(receipt.memory_admission_receipt_id)})
        return receipt

    def quarantine_memory_candidate(
        self,
        *,
        candidate_id: UUID,
        reviewer_id: UUID,
        role_ids: list[str],
        reason: str,
        idempotency_key: str,
    ) -> MemoryAdmissionReceipt:
        prior = self.repository.receipt_for_idempotency(candidate_id, "quarantine", idempotency_key)
        if prior:
            return prior
        self._assert_memory_role(role_ids)
        candidate = self._candidate(candidate_id)
        event = self.repository.put_memory_event(new_memory_event(candidate=candidate, status=MemoryEventStatus.quarantined, approved_by=None))
        receipt = self.repository.put_receipt(
            new_memory_admission_receipt(
                candidate=candidate,
                policy_result=MemoryAdmissionPolicyResult.quarantined,
                memory_event_id=event.memory_event_id,
                reviewer_id=reviewer_id,
                blocker_codes=[f"operator_quarantined:{reason}"],
            ),
            action="quarantine",
            idempotency_key=idempotency_key,
        )
        self._event("MemoryCandidateQuarantined", candidate, {"reason": reason, "receipt_id": str(receipt.memory_admission_receipt_id)})
        return receipt

    def record_memory_usage_citation(
        self,
        *,
        memory_event_id: UUID,
        compiler_or_agent: str,
        citing_object_ref: str,
        evidence_refs: list[MemoryEvidenceRef | dict[str, Any]],
        idempotency_key: str,
    ) -> MemoryUsageCitation:
        prior = self.repository.citation_for_idempotency(memory_event_id, compiler_or_agent, idempotency_key)
        if prior:
            return prior
        event = self._memory_event(memory_event_id)
        if event.status != MemoryEventStatus.approved:
            raise MemoryAdmissionError("MEMORY_EVENT_NOT_APPROVED", "Only approved memory may be cited by compilers.")
        refs = [self._evidence_ref(ref) for ref in evidence_refs]
        if not refs:
            raise MemoryAdmissionError("MEMORY_CITATION_EVIDENCE_REQUIRED", "Memory usage must cite evidence refs.")
        candidate_evidence = {(ref.source_type, ref.source_id, ref.receipt_id, ref.transcript_segment_id) for ref in event.evidence_refs}
        citation_evidence = {(ref.source_type, ref.source_id, ref.receipt_id, ref.transcript_segment_id) for ref in refs}
        if not candidate_evidence.intersection(citation_evidence):
            raise MemoryAdmissionError("MEMORY_CITATION_EVIDENCE_MISMATCH", "Compiler citation must reference admitted memory evidence.")
        citation = self.repository.put_usage_citation(
            MemoryUsageCitation(
                schema_version="cmf.memory_usage_citation.v1",
                memory_usage_citation_id=uuid4(),
                memory_event_id=event.memory_event_id,
                compiler_or_agent=compiler_or_agent,
                citing_object_ref=citing_object_ref,
                evidence_refs=refs,
                memory_statement=event.proposed_statement,
                cited_at=utc_now(),
            ),
            idempotency_key=idempotency_key,
        )
        self.repository.append_event(
            MemoryAdmissionDomainEvent(
                schema_version="cmf.memory_admission_domain_event.v1",
                memory_admission_event_id=uuid4(),
                event_type="MemoryUsageCited",
                candidate_id=event.candidate_id,
                memory_event_id=event.memory_event_id,
                payload={"compiler_or_agent": compiler_or_agent, "citation_id": str(citation.memory_usage_citation_id)},
                created_at=utc_now(),
            )
        )
        return citation

    def stage14_admit_evidence_memory(self, **kwargs: Any) -> MemoryAdmissionReceipt:
        proposal_kwargs = {
            key: value
            for key, value in kwargs.items()
            if key not in {"role_ids", "approval_idempotency_key"}
        }
        candidate = self.propose_memory_admission(**proposal_kwargs)
        return self.approve_memory_admission(
            candidate_id=candidate.candidate_id,
            reviewer_id=kwargs["proposed_by_actor_id"],
            role_ids=kwargs.get("role_ids", ["operator"]),
            idempotency_key=kwargs.get("approval_idempotency_key", f"memory:approve:{candidate.candidate_id}"),
        )

    def _policy(self, candidate: MemoryAdmissionCandidate) -> MemoryPolicyDecision:
        blockers: list[str] = []
        evidence_valid = bool(candidate.evidence_refs)
        if not evidence_valid:
            blockers.append("MEMORY_EVIDENCE_REQUIRED")
        if candidate.confidence < self.confidence_threshold:
            blockers.append("MEMORY_CONFIDENCE_BELOW_THRESHOLD")
        provenance_valid = bool(candidate.provenance_summary.strip()) and bool(candidate.proposed_from_event_id.strip())
        if not provenance_valid:
            blockers.append("MEMORY_PROVENANCE_REQUIRED")
        statement_specific = self._statement_specific(candidate.proposed_statement)
        if not statement_specific:
            blockers.append("MEMORY_STATEMENT_TOO_GENERIC")
        consent_valid = self._consent_valid(candidate)
        if not consent_valid:
            blockers.append("MEMORY_CONSENT_INCOMPATIBLE")
        if not consent_valid:
            result = MemoryAdmissionPolicyResult.quarantined
        elif blockers:
            result = MemoryAdmissionPolicyResult.rejected
        else:
            result = MemoryAdmissionPolicyResult.approved
        return MemoryPolicyDecision(
            schema_version="cmf.memory_policy_decision.v1",
            candidate_id=candidate.candidate_id,
            evidence_valid=evidence_valid,
            consent_valid=consent_valid,
            confidence_valid=candidate.confidence >= self.confidence_threshold,
            provenance_valid=provenance_valid,
            statement_specific=statement_specific,
            blockers=sorted(set(blockers)),
            result=result,
            checked_at=utc_now(),
        )

    def _consent_valid(self, candidate: MemoryAdmissionCandidate) -> bool:
        if not candidate.consent_compatible:
            return False
        if candidate.consent_record_version_id is None or self.consent_repository is None:
            return candidate.consent_compatible
        version = self.consent_repository.versions.get(candidate.consent_record_version_id)
        if version is None:
            return False
        if version.organization_id != candidate.organization_id or version.brand_id != candidate.brand_id:
            return False
        if version.status != ConsentVersionStatus.active:
            return False
        return bool(version.scope.source_storage_allowed and version.scope.reuse_allowed and version.scope.retention_allowed)

    @staticmethod
    def _statement_specific(statement: str) -> bool:
        normalized = " ".join(statement.strip().lower().split())
        if normalized in GENERIC_MEMORY_PATTERNS:
            return False
        return len(normalized) >= 24 and any(char.isdigit() or ":" in normalized or "because" in normalized or "when " in normalized for char in normalized)

    @staticmethod
    def _evidence_ref(ref: MemoryEvidenceRef | dict[str, Any]) -> MemoryEvidenceRef:
        if isinstance(ref, MemoryEvidenceRef):
            return ref
        return MemoryEvidenceRef(**ref)

    @staticmethod
    def _assert_memory_role(role_ids: list[str]) -> None:
        if not set(role_ids).intersection(MEMORY_REVIEW_ROLES):
            raise MemoryAdmissionError("ROLE_PERMISSION_DENIED", "Actor lacks a memory admission role.")

    def _candidate(self, candidate_id: UUID) -> MemoryAdmissionCandidate:
        candidate = self.repository.candidates.get(UUID(str(candidate_id)))
        if candidate is None:
            raise MemoryAdmissionError("MEMORY_CANDIDATE_REQUIRED", "Memory admission candidate is required.")
        return candidate

    def _memory_event(self, memory_event_id: UUID) -> MemoryEvent:
        event = self.repository.memory_events.get(UUID(str(memory_event_id)))
        if event is None:
            raise MemoryAdmissionError("MEMORY_EVENT_REQUIRED", "Memory event is required.")
        return event

    def _event(self, event_type: str, candidate: MemoryAdmissionCandidate, payload: dict[str, Any]) -> MemoryAdmissionDomainEvent:
        return self.repository.append_event(
            MemoryAdmissionDomainEvent(
                schema_version="cmf.memory_admission_domain_event.v1",
                memory_admission_event_id=uuid4(),
                event_type=event_type,
                candidate_id=candidate.candidate_id,
                payload=payload,
                created_at=utc_now(),
            )
        )


@dataclass
class MemoryAdmissionCommandHandler:
    command_type: str
    service: MemoryAdmissionService
    aggregate_type: str = "memory_admission"
    allowed_roles: set[str] = field(default_factory=lambda: MEMORY_REVIEW_ROLES)
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "ProposeMemoryAdmissionCommand":
            return self.service.propose_memory_admission(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                memory_type=payload["memory_type"],
                proposed_from_event_id=payload["proposed_from_event_id"],
                proposed_statement=payload["proposed_statement"],
                evidence_refs=payload.get("evidence_refs", []),
                confidence=float(payload["confidence"]),
                scope=payload["scope"],
                consent_record_version_id=UUID(payload["consent_record_version_id"]) if payload.get("consent_record_version_id") else None,
                consent_compatible=bool(payload.get("consent_compatible", False)),
                provenance_summary=payload["provenance_summary"],
                proposed_by_actor_id=envelope.actor.actor_id,
                originating_route_ref=payload.get("originating_route_ref"),
                downstream_usage_constraints=payload.get("downstream_usage_constraints"),
                idempotency_key=envelope.idempotency_key,
            ).model_dump(mode="json")
        if self.command_type == "ValidateMemoryEvidenceCommand":
            return self.service.validate_memory_evidence(UUID(payload["candidate_id"])).model_dump(mode="json")
        if self.command_type == "ValidateMemoryConsentCommand":
            return self.service.validate_memory_consent(UUID(payload["candidate_id"])).model_dump(mode="json")
        if self.command_type == "ApproveMemoryAdmissionCommand":
            return self.service.approve_memory_admission(
                candidate_id=UUID(payload["candidate_id"]),
                reviewer_id=envelope.actor.actor_id,
                role_ids=envelope.actor.role_ids,
                idempotency_key=envelope.idempotency_key,
            ).model_dump(mode="json")
        if self.command_type == "RejectMemoryAdmissionCommand":
            return self.service.reject_memory_admission(
                candidate_id=UUID(payload["candidate_id"]),
                reviewer_id=envelope.actor.actor_id,
                role_ids=envelope.actor.role_ids,
                reason=payload["reason"],
                idempotency_key=envelope.idempotency_key,
            ).model_dump(mode="json")
        if self.command_type == "QuarantineMemoryCandidateCommand":
            return self.service.quarantine_memory_candidate(
                candidate_id=UUID(payload["candidate_id"]),
                reviewer_id=envelope.actor.actor_id,
                role_ids=envelope.actor.role_ids,
                reason=payload["reason"],
                idempotency_key=envelope.idempotency_key,
            ).model_dump(mode="json")
        if self.command_type == "RecordMemoryUsageCitationCommand":
            return self.service.record_memory_usage_citation(
                memory_event_id=UUID(payload["memory_event_id"]),
                compiler_or_agent=payload["compiler_or_agent"],
                citing_object_ref=payload["citing_object_ref"],
                evidence_refs=payload.get("evidence_refs", []),
                idempotency_key=envelope.idempotency_key,
            ).model_dump(mode="json")
        raise MemoryAdmissionError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("candidate_id") or payload.get("memory_event_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_memory_admission_command_handlers(bus: CommandBus, service: MemoryAdmissionService) -> None:
    for command_type in [
        "ProposeMemoryAdmissionCommand",
        "ValidateMemoryEvidenceCommand",
        "ValidateMemoryConsentCommand",
        "ApproveMemoryAdmissionCommand",
        "RejectMemoryAdmissionCommand",
        "QuarantineMemoryCandidateCommand",
        "RecordMemoryUsageCitationCommand",
    ]:
        bus.register_handler(MemoryAdmissionCommandHandler(command_type=command_type, service=service))
