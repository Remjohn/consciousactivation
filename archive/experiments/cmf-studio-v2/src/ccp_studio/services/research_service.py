"""Research field and evidence service for TS-CMF-023."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.research import (
    EvidenceCitation,
    ResearchEvidence,
    ResearchEvidenceReceipt,
    ResearchEvidenceStatus,
    ResearchField,
    ResearchSnapshot,
    SourceRole,
    TemporalSensitivity,
    new_research_evidence_receipt,
)
from ccp_studio.repositories.research import InMemoryResearchRepository
from ccp_studio.services.command_bus import CommandBus


class ResearchServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ResearchService:
    repository: InMemoryResearchRepository = field(default_factory=InMemoryResearchRepository)

    def create_field(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        objective: str,
        source_scope: list[str],
        created_by_actor_id: UUID,
        guest_id: UUID | None = None,
    ) -> ResearchField:
        now = utc_now()
        field_record = ResearchField(
            schema_version="cmf.research_field.v1",
            research_field_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            guest_id=guest_id,
            objective=objective,
            source_scope=source_scope,
            created_by_actor_id=created_by_actor_id,
            created_at=now,
            updated_at=now,
        )
        return self.repository.put_field(field_record)

    def attach_evidence(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        research_field_id: UUID,
        claim: str,
        source_role: SourceRole,
        citations: list[EvidenceCitation],
        confidence: float,
        temporal_sensitivity: TemporalSensitivity,
        provenance_summary: str,
        created_by_actor_id: UUID,
        freshness_due_at=None,
        contradiction_notes: list[str] | None = None,
        research_gap: bool = False,
        primitive_family_hints: list[str] | None = None,
    ) -> ResearchEvidence:
        field_record = self._field_for_brand(organization_id, brand_id, research_field_id)
        evidence = ResearchEvidence(
            schema_version="cmf.research_evidence.v1",
            evidence_id=uuid4(),
            research_field_id=field_record.research_field_id,
            organization_id=organization_id,
            brand_id=brand_id,
            claim=claim,
            source_role=source_role,
            citations=citations,
            confidence=confidence,
            temporal_sensitivity=temporal_sensitivity,
            freshness_due_at=freshness_due_at,
            provenance_summary=provenance_summary,
            contradiction_notes=contradiction_notes or [],
            research_gap=research_gap,
            primitive_family_hints=primitive_family_hints or [],
            status=ResearchEvidenceStatus.draft,
            created_by_actor_id=created_by_actor_id,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        self.repository.put_evidence(evidence)
        field_record = field_record.model_copy(
            update={"evidence_ids": [*field_record.evidence_ids, evidence.evidence_id], "updated_at": utc_now()}
        )
        self.repository.put_field(field_record)
        return evidence

    def validate_evidence_provenance(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        evidence_id: UUID,
        validator_actor_id: UUID,
    ) -> ResearchEvidence:
        evidence = self._evidence_for_brand(organization_id, brand_id, evidence_id)
        blockers = self._provenance_blockers(evidence)
        if blockers:
            self._write_receipt(evidence, validator_actor_id, blockers[0])
            return self.repository.put_evidence(
                evidence.model_copy(update={"status": ResearchEvidenceStatus.draft, "updated_at": utc_now()})
            )
        ready = evidence.model_copy(update={"status": ResearchEvidenceStatus.provenance_ready, "updated_at": utc_now()})
        self.repository.put_evidence(ready)
        self._write_receipt(ready, validator_actor_id, "RESEARCH_EVIDENCE_PROVENANCE_READY")
        return ready

    def approve_evidence(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        evidence_id: UUID,
        validator_actor_id: UUID,
    ) -> ResearchEvidence:
        evidence = self._evidence_for_brand(organization_id, brand_id, evidence_id)
        if evidence.status != ResearchEvidenceStatus.provenance_ready:
            raise ResearchServiceError("RESEARCH_EVIDENCE_PROVENANCE_REQUIRED", "Evidence must pass provenance validation before approval.")
        if self._is_stale(evidence):
            stale = evidence.model_copy(update={"status": ResearchEvidenceStatus.stale_review_required, "updated_at": utc_now()})
            self.repository.put_evidence(stale)
            raise ResearchServiceError("RESEARCH_EVIDENCE_FRESHNESS_REVIEW_REQUIRED", "Evidence requires freshness review.")
        approved = evidence.model_copy(update={"status": ResearchEvidenceStatus.approved_for_use, "updated_at": utc_now()})
        self.repository.put_evidence(approved)
        field_record = self.repository.fields[approved.research_field_id]
        if approved.evidence_id not in field_record.approved_evidence_ids:
            self.repository.put_field(
                field_record.model_copy(
                    update={
                        "approved_evidence_ids": [*field_record.approved_evidence_ids, approved.evidence_id],
                        "updated_at": utc_now(),
                    }
                )
            )
        self._write_receipt(approved, validator_actor_id, "RESEARCH_EVIDENCE_APPROVED")
        return approved

    def mark_evidence_stale(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        evidence_id: UUID,
        actor_id: UUID,
        reason: str,
    ) -> ResearchEvidence:
        evidence = self._evidence_for_brand(organization_id, brand_id, evidence_id)
        stale = evidence.model_copy(update={"status": ResearchEvidenceStatus.stale_review_required, "updated_at": utc_now()})
        self.repository.put_evidence(stale)
        self._write_receipt(stale, actor_id, f"RESEARCH_EVIDENCE_STALE:{reason}")
        return stale

    def prepare_downstream_evidence_inputs(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        evidence_ids: list[UUID],
    ) -> list[ResearchEvidence]:
        approved: list[ResearchEvidence] = []
        for evidence_id in evidence_ids:
            evidence = self._evidence_for_brand(organization_id, brand_id, evidence_id)
            if evidence.status != ResearchEvidenceStatus.approved_for_use:
                raise ResearchServiceError("RESEARCH_EVIDENCE_NOT_APPROVED", "Only approved evidence can support downstream compilers.")
            if self._is_stale(evidence):
                self.repository.put_evidence(
                    evidence.model_copy(update={"status": ResearchEvidenceStatus.stale_review_required, "updated_at": utc_now()})
                )
                raise ResearchServiceError("RESEARCH_EVIDENCE_FRESHNESS_REVIEW_REQUIRED", "Evidence requires freshness review before reuse.")
            approved.append(evidence)
        return approved

    def freeze_research_snapshot(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        research_field_id: UUID,
        evidence_ids: list[UUID],
        frozen_by_actor_id: UUID,
    ) -> ResearchSnapshot:
        field_record = self._field_for_brand(organization_id, brand_id, research_field_id)
        evidence = self.prepare_downstream_evidence_inputs(
            organization_id=organization_id,
            brand_id=brand_id,
            evidence_ids=evidence_ids,
        )
        if not evidence:
            raise ResearchServiceError("RESEARCH_EVIDENCE_REQUIRED", "At least one approved evidence item is required.")
        receipt_ids = [
            receipt.research_evidence_receipt_id
            for receipt in self.repository.receipts.values()
            if any(item in receipt.evidence_ids for item in evidence_ids)
        ]
        snapshot = ResearchSnapshot(
            schema_version="cmf.research_snapshot.v1",
            research_snapshot_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            research_field_id=research_field_id,
            approved_evidence_ids=evidence_ids,
            research_evidence_receipt_ids=receipt_ids,
            saturation_quality=self._saturation_quality(evidence),
            frozen_by_actor_id=frozen_by_actor_id,
            frozen_at=utc_now(),
        )
        self.repository.put_snapshot(snapshot)
        self.repository.put_field(
            field_record.model_copy(
                update={"frozen_snapshot_ids": [*field_record.frozen_snapshot_ids, snapshot.research_snapshot_id], "updated_at": utc_now()}
            )
        )
        return snapshot

    def _field_for_brand(self, organization_id: UUID, brand_id: UUID, research_field_id: UUID) -> ResearchField:
        field_record = self.repository.fields.get(research_field_id)
        if field_record is None:
            raise ResearchServiceError("RESEARCH_FIELD_REQUIRED", "Research field is required.")
        if field_record.organization_id != organization_id or field_record.brand_id != brand_id:
            raise ResearchServiceError("BRAND_SCOPE_VIOLATION", "Research field is outside the active brand scope.")
        return field_record

    def _evidence_for_brand(self, organization_id: UUID, brand_id: UUID, evidence_id: UUID) -> ResearchEvidence:
        evidence = self.repository.evidence.get(evidence_id)
        if evidence is None:
            raise ResearchServiceError("RESEARCH_EVIDENCE_REQUIRED", "Research evidence is required.")
        if evidence.organization_id != organization_id or evidence.brand_id != brand_id:
            raise ResearchServiceError("BRAND_SCOPE_VIOLATION", "Research evidence is outside the active brand scope.")
        return evidence

    def _provenance_blockers(self, evidence: ResearchEvidence) -> list[str]:
        blockers: list[str] = []
        if not evidence.citations:
            blockers.append("RESEARCH_CITATION_REQUIRED")
        if not evidence.provenance_summary.strip():
            blockers.append("RESEARCH_PROVENANCE_REQUIRED")
        if evidence.source_role == SourceRole.inference and not evidence.contradiction_notes:
            blockers.append("INFERENCE_CONTRADICTION_NOTES_REQUIRED")
        if evidence.temporal_sensitivity in {TemporalSensitivity.medium, TemporalSensitivity.high} and evidence.freshness_due_at is None:
            blockers.append("FRESHNESS_POLICY_REQUIRED")
        if evidence.confidence < 0.45 and not evidence.research_gap:
            blockers.append("LOW_CONFIDENCE_RESEARCH_GAP_REQUIRED")
        return blockers

    @staticmethod
    def _is_stale(evidence: ResearchEvidence) -> bool:
        return evidence.freshness_due_at is not None and evidence.freshness_due_at <= utc_now()

    @staticmethod
    def _saturation_quality(evidence: list[ResearchEvidence]) -> str:
        has_collision = any(item.contradiction_notes for item in evidence)
        has_cral = any(item.source_role == SourceRole.cral_signal for item in evidence)
        has_primary = any(item.source_role == SourceRole.primary_source for item in evidence)
        return "rscs_saturated" if has_collision and (has_cral or has_primary) else "basic_provenance"

    def _write_receipt(self, evidence: ResearchEvidence, validator_actor_id: UUID, decision_code: str) -> ResearchEvidenceReceipt:
        receipt = new_research_evidence_receipt(
            organization_id=evidence.organization_id,
            brand_id=evidence.brand_id,
            research_field_id=evidence.research_field_id,
            evidence_ids=[evidence.evidence_id],
            citations=evidence.citations,
            freshness_policy=evidence.temporal_sensitivity.value,
            validator_actor_id=validator_actor_id,
            decision_code=decision_code,
        )
        return self.repository.put_receipt(receipt)


@dataclass
class ResearchCommandHandler:
    command_type: str
    service: ResearchService
    aggregate_type: str = "research"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "CreateResearchFieldCommand":
            return self.service.create_field(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                objective=payload["objective"],
                source_scope=payload["source_scope"],
                guest_id=UUID(payload["guest_id"]) if payload.get("guest_id") else None,
                created_by_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "AttachResearchEvidenceCommand":
            return self.service.attach_evidence(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                research_field_id=UUID(payload["research_field_id"]),
                claim=payload["claim"],
                source_role=SourceRole(payload["source_role"]),
                citations=[EvidenceCitation(**item) for item in payload.get("citations", [])],
                confidence=payload["confidence"],
                temporal_sensitivity=TemporalSensitivity(payload["temporal_sensitivity"]),
                freshness_due_at=payload.get("freshness_due_at"),
                provenance_summary=payload.get("provenance_summary", ""),
                contradiction_notes=payload.get("contradiction_notes", []),
                research_gap=payload.get("research_gap", False),
                primitive_family_hints=payload.get("primitive_family_hints", []),
                created_by_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "ValidateEvidenceProvenanceCommand":
            return self.service.validate_evidence_provenance(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                evidence_id=UUID(payload["evidence_id"]),
                validator_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "ApproveResearchEvidenceCommand":
            return self.service.approve_evidence(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                evidence_id=UUID(payload["evidence_id"]),
                validator_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        if self.command_type == "MarkEvidenceStaleCommand":
            return self.service.mark_evidence_stale(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                evidence_id=UUID(payload["evidence_id"]),
                actor_id=envelope.actor.actor_id,
                reason=payload["reason"],
            ).model_dump(mode="json")
        if self.command_type == "FreezeResearchSnapshotCommand":
            return self.service.freeze_research_snapshot(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                research_field_id=UUID(payload["research_field_id"]),
                evidence_ids=[UUID(item) for item in payload["evidence_ids"]],
                frozen_by_actor_id=envelope.actor.actor_id,
            ).model_dump(mode="json")
        raise ResearchServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("research_field_id") or payload.get("evidence_id")
        if isinstance(raw, str):
            return UUID(raw)
        return envelope.brand_id


def register_research_command_handlers(bus: CommandBus, service: ResearchService) -> None:
    for command_type in [
        "CreateResearchFieldCommand",
        "AttachResearchEvidenceCommand",
        "ValidateEvidenceProvenanceCommand",
        "ApproveResearchEvidenceCommand",
        "MarkEvidenceStaleCommand",
        "FreezeResearchSnapshotCommand",
    ]:
        bus.register_handler(ResearchCommandHandler(command_type=command_type, service=service))
