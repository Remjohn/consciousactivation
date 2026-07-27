"""Versioned consent service for TS-CMF-008."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.consent import (
    ConsentChangeImpact,
    ConsentCompatibilityResult,
    ConsentReceipt,
    ConsentRecordVersion,
    ConsentReviewView,
    ConsentScope,
    ConsentVersionStatus,
    PendingWorkItem,
    new_consent_version,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.domain.policies.consent_policy import COMMAND_REQUIRED_SCOPES, ConsentPolicy
from ccp_studio.repositories.consent_record_versions import InMemoryConsentRepository
from ccp_studio.services.command_bus import CommandBus


class ConsentServiceError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ConsentService:
    repository: InMemoryConsentRepository = field(default_factory=InMemoryConsentRepository)
    policy: ConsentPolicy = field(default_factory=ConsentPolicy)

    def grant_consent(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        guest_or_client_id: UUID,
        scope: ConsentScope,
        actor_id: UUID,
        evidence_refs: list[str],
        command_id: UUID | None = None,
    ) -> ConsentRecordVersion:
        return self._append_version(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_or_client_id=guest_or_client_id,
            scope=scope,
            actor_id=actor_id,
            evidence_refs=evidence_refs,
            status=ConsentVersionStatus.active,
            action="GrantConsentCommand",
            command_id=command_id,
        )

    def narrow_consent(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        guest_or_client_id: UUID,
        scope: ConsentScope,
        actor_id: UUID,
        evidence_refs: list[str],
        command_id: UUID | None = None,
    ) -> ConsentRecordVersion:
        current = self.repository.current_version(organization_id, brand_id, guest_or_client_id)
        version = self._append_version(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_or_client_id=guest_or_client_id,
            scope=scope,
            actor_id=actor_id,
            evidence_refs=evidence_refs,
            status=ConsentVersionStatus.active,
            action="NarrowConsentCommand",
            command_id=command_id,
            replaces_version_id=current.consent_record_version_id if current else None,
        )
        self.mark_pending_work_for_review(version)
        return version

    def expire_consent(self, *, organization_id: UUID, brand_id: UUID, guest_or_client_id: UUID, actor_id: UUID, command_id: UUID | None = None) -> ConsentRecordVersion:
        current = self._require_current(organization_id, brand_id, guest_or_client_id)
        version = self._append_version(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_or_client_id=guest_or_client_id,
            scope=current.scope,
            actor_id=actor_id,
            evidence_refs=current.evidence_refs,
            status=ConsentVersionStatus.expired,
            action="ExpireConsentCommand",
            command_id=command_id,
            replaces_version_id=current.consent_record_version_id,
        )
        self.mark_pending_work_for_review(version)
        return version

    def revoke_consent(self, *, organization_id: UUID, brand_id: UUID, guest_or_client_id: UUID, actor_id: UUID, command_id: UUID | None = None) -> ConsentRecordVersion:
        current = self._require_current(organization_id, brand_id, guest_or_client_id)
        version = self._append_version(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_or_client_id=guest_or_client_id,
            scope=current.scope,
            actor_id=actor_id,
            evidence_refs=current.evidence_refs,
            status=ConsentVersionStatus.revoked,
            action="RevokeConsentCommand",
            command_id=command_id,
            replaces_version_id=current.consent_record_version_id,
        )
        self.mark_pending_work_for_review(version)
        return version

    def evaluate_command(self, envelope: CommandEnvelope) -> ConsentCompatibilityResult:
        if envelope.command_type not in COMMAND_REQUIRED_SCOPES:
            return ConsentCompatibilityResult(
                schema_version="cmf.consent_compatibility_result.v1",
                command_type=envelope.command_type,
                allowed=True,
                decision_code="CONSENT_NOT_APPLICABLE",
            )
        raw_subject = envelope.payload.get("guest_or_client_id")
        if not raw_subject:
            return ConsentCompatibilityResult(
                schema_version="cmf.consent_compatibility_result.v1",
                command_type=envelope.command_type,
                allowed=False,
                decision_code="CONSENT_RECORD_REQUIRED",
            )
        subject_id = UUID(raw_subject)
        current = self.repository.current_version(envelope.organization_id, envelope.brand_id, subject_id)
        result = self.policy.evaluate(command_type=envelope.command_type, version=current)
        if current is not None:
            self._write_receipt(
                version=current,
                actor_id=envelope.actor.actor_id,
                action="EvaluateConsentCompatibilityCommand",
                decision_code=result.decision_code,
                command_id=envelope.command_id,
                evidence_refs=result.evidence_refs,
            )
        return result

    def add_pending_work(self, *, organization_id: UUID, brand_id: UUID, guest_or_client_id: UUID, work_type: str, source_ref: str) -> PendingWorkItem:
        item = PendingWorkItem(
            pending_work_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            guest_or_client_id=guest_or_client_id,
            work_type=work_type,
            status="queued",
            source_ref=source_ref,
        )
        return self.repository.put_pending_work(item)

    def mark_pending_work_for_review(self, version: ConsentRecordVersion) -> ConsentChangeImpact:
        affected = self.repository.pending_for_subject(
            version.organization_id,
            version.brand_id,
            version.guest_or_client_id,
        )
        for item in affected:
            item.status = "quarantined"
            self.repository.put_pending_work(item)
        impact = ConsentChangeImpact(
            schema_version="cmf.consent_change_impact.v1",
            impact_id=uuid4(),
            consent_record_version_id=version.consent_record_version_id,
            affected_pending_work_ids=[item.pending_work_id for item in affected],
            quarantine_required=bool(affected),
            review_required=bool(affected),
            created_at=utc_now(),
        )
        return self.repository.put_impact(impact)

    def review_view(self, *, organization_id: UUID, brand_id: UUID, guest_or_client_id: UUID, command_type: str) -> ConsentReviewView:
        current = self._require_current(organization_id, brand_id, guest_or_client_id)
        compatibility = self.policy.evaluate(command_type=command_type, version=current)
        risk = "revoked" if current.status == ConsentVersionStatus.revoked else "none"
        return ConsentReviewView(
            schema_version="cmf.consent_review_view.v1",
            active_version=current,
            compatibility=compatibility,
            source_evidence_refs=current.evidence_refs,
            revocation_risk=risk,
        )

    def _append_version(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        guest_or_client_id: UUID,
        scope: ConsentScope,
        actor_id: UUID,
        evidence_refs: list[str],
        status: ConsentVersionStatus,
        action: str,
        command_id: UUID | None,
        replaces_version_id: UUID | None = None,
    ) -> ConsentRecordVersion:
        versions = self.repository.versions_for_subject(organization_id, brand_id, guest_or_client_id)
        version = new_consent_version(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_or_client_id=guest_or_client_id,
            version_number=len(versions) + 1,
            status=status,
            scope=scope,
            created_by_actor_id=actor_id,
            evidence_refs=evidence_refs,
            replaces_version_id=replaces_version_id,
        )
        self.repository.put_version(version)
        self._write_receipt(
            version=version,
            actor_id=actor_id,
            action=action,
            decision_code=status.value,
            command_id=command_id,
            evidence_refs=evidence_refs,
        )
        return version

    def _write_receipt(self, *, version: ConsentRecordVersion, actor_id: UUID, action: str, decision_code: str, command_id: UUID | None, evidence_refs: list[str]) -> ConsentReceipt:
        receipt = ConsentReceipt(
            schema_version="cmf.consent_receipt.v1",
            consent_receipt_id=uuid4(),
            organization_id=version.organization_id,
            brand_id=version.brand_id,
            guest_or_client_id=version.guest_or_client_id,
            consent_record_version_id=version.consent_record_version_id,
            action=action,
            decision_code=decision_code,
            command_id=command_id,
            evidence_refs=evidence_refs,
            storage_path=f"brands/{version.brand_id}/receipts/consent/{version.consent_record_version_id}.json",
            written_at=utc_now(),
        )
        return self.repository.put_receipt(receipt)

    def _require_current(self, organization_id: UUID, brand_id: UUID, guest_or_client_id: UUID) -> ConsentRecordVersion:
        current = self.repository.current_version(organization_id, brand_id, guest_or_client_id)
        if current is None:
            raise ConsentServiceError("CONSENT_RECORD_REQUIRED", "Consent record is required.")
        return current


@dataclass
class ConsentCommandHandler:
    command_type: str
    service: ConsentService
    aggregate_type: str = "consent"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        subject_id = UUID(payload["guest_or_client_id"])
        if self.command_type == "GrantConsentCommand":
            version = self.service.grant_consent(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                guest_or_client_id=subject_id,
                scope=ConsentScope(**payload["scope"]),
                actor_id=envelope.actor.actor_id,
                evidence_refs=payload.get("evidence_refs", []),
                command_id=envelope.command_id,
            )
            return version.model_dump(mode="json")
        if self.command_type == "NarrowConsentCommand":
            version = self.service.narrow_consent(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                guest_or_client_id=subject_id,
                scope=ConsentScope(**payload["scope"]),
                actor_id=envelope.actor.actor_id,
                evidence_refs=payload.get("evidence_refs", []),
                command_id=envelope.command_id,
            )
            return version.model_dump(mode="json")
        if self.command_type == "ExpireConsentCommand":
            return self.service.expire_consent(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                guest_or_client_id=subject_id,
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "RevokeConsentCommand":
            return self.service.revoke_consent(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                guest_or_client_id=subject_id,
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "InspectConsentCommand":
            view = self.service.review_view(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                guest_or_client_id=subject_id,
                command_type=payload["target_command_type"],
            )
            return view.model_dump(mode="json")
        if self.command_type == "EvaluateConsentCompatibilityCommand":
            result = self.service.evaluate_command(envelope)
            return result.model_dump(mode="json")
        raise ConsentServiceError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("consent_record_version_id")
        if isinstance(raw, str):
            return UUID(raw)
        return envelope.brand_id


def register_consent_command_handlers(bus: CommandBus, service: ConsentService) -> None:
    bus.consent_policy = service
    for command_type in [
        "GrantConsentCommand",
        "NarrowConsentCommand",
        "ExpireConsentCommand",
        "RevokeConsentCommand",
        "InspectConsentCommand",
        "EvaluateConsentCompatibilityCommand",
    ]:
        bus.register_handler(ConsentCommandHandler(command_type=command_type, service=service))
