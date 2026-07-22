"""Cross-workflow consent guard service for TS-CMF-010."""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.consent_blockers import (
    AffectedPendingWork,
    ConsentGuardDecision,
    ConsentSensitiveCommand,
    new_affected_pending_work,
    new_consent_blocker_receipt,
)
from ccp_studio.domain.policies.consent_blocker_policy import ConsentBlockerPolicy
from ccp_studio.repositories.consent_blocker_receipts import InMemoryConsentBlockerRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.consent_service import ConsentService


@dataclass
class ConsentGuardService:
    consent_service: ConsentService
    repository: InMemoryConsentBlockerRepository = field(default_factory=InMemoryConsentBlockerRepository)
    policy: ConsentBlockerPolicy = field(default_factory=ConsentBlockerPolicy)

    def __post_init__(self) -> None:
        for command in self.policy.registry.values():
            self.repository.put_sensitive_command(command)

    def register_sensitive_command(self, command: ConsentSensitiveCommand) -> ConsentSensitiveCommand:
        self.policy.register(command)
        return self.repository.put_sensitive_command(command)

    def evaluate_command(self, envelope: CommandEnvelope) -> ConsentGuardDecision:
        guest_or_client_id = self._optional_uuid(envelope.payload.get("guest_or_client_id"))
        current = (
            self.consent_service.repository.current_version(
                envelope.organization_id,
                envelope.brand_id,
                guest_or_client_id,
            )
            if guest_or_client_id is not None
            else None
        )
        decision = self.policy.evaluate(
            command_type=envelope.command_type,
            version=current,
            require_mapping=bool(envelope.payload.get("requires_consent_policy")),
        )
        if decision.allowed:
            return decision
        object_type = str(envelope.payload.get("object_type") or "command")
        object_id = self._optional_uuid(envelope.payload.get("object_id")) or envelope.brand_id
        receipt = new_consent_blocker_receipt(
            organization_id=envelope.organization_id,
            brand_id=envelope.brand_id,
            command_id=envelope.command_id,
            object_type=object_type,
            object_id=object_id,
            consent_record_version_id=decision.consent_record_version_id,
            blocked_scope=decision.blocked_scope or "active_consent",
            decision_code=decision.decision_code,
            repair_actions=decision.repair_actions,
            evidence_refs=decision.evidence_refs,
        )
        self.repository.put_blocker_receipt(receipt)
        affected = self.flag_affected_pending_work(
            organization_id=envelope.organization_id,
            brand_id=envelope.brand_id,
            guest_or_client_id=guest_or_client_id,
            command_id=envelope.command_id,
            object_type=object_type,
            object_id=object_id,
            reason_code=decision.decision_code,
        )
        return decision.model_copy(
            update={
                "blocker_receipt_id": receipt.consent_blocker_receipt_id,
                "affected_pending_work_ids": affected.pending_work_ids if affected else [],
            }
        )

    def evaluate_workflow_boundary(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        guest_or_client_id: UUID,
        command_type: str,
        object_type: str,
        object_id: UUID,
        command_id: UUID | None = None,
        require_mapping: bool = False,
    ) -> ConsentGuardDecision:
        current = self.consent_service.repository.current_version(
            organization_id,
            brand_id,
            guest_or_client_id,
        )
        decision = self.policy.evaluate(
            command_type=command_type,
            version=current,
            require_mapping=require_mapping,
        )
        if decision.allowed:
            return decision
        resolved_command_id = command_id or uuid4()
        receipt = new_consent_blocker_receipt(
            organization_id=organization_id,
            brand_id=brand_id,
            command_id=resolved_command_id,
            object_type=object_type,
            object_id=object_id,
            consent_record_version_id=decision.consent_record_version_id,
            blocked_scope=decision.blocked_scope or "active_consent",
            decision_code=decision.decision_code,
            repair_actions=decision.repair_actions,
            evidence_refs=decision.evidence_refs,
        )
        self.repository.put_blocker_receipt(receipt)
        affected = self.flag_affected_pending_work(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_or_client_id=guest_or_client_id,
            command_id=resolved_command_id,
            object_type=object_type,
            object_id=object_id,
            reason_code=decision.decision_code,
        )
        return decision.model_copy(
            update={
                "blocker_receipt_id": receipt.consent_blocker_receipt_id,
                "affected_pending_work_ids": affected.pending_work_ids if affected else [],
            }
        )

    def flag_affected_pending_work(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        guest_or_client_id: UUID | None,
        command_id: UUID,
        object_type: str,
        object_id: UUID,
        reason_code: str,
    ) -> AffectedPendingWork | None:
        if guest_or_client_id is None:
            return None
        pending = self.consent_service.repository.pending_for_subject(
            organization_id,
            brand_id,
            guest_or_client_id,
        )
        if not pending:
            return None
        for item in pending:
            item.status = "quarantined"
            self.consent_service.repository.put_pending_work(item)
        affected = new_affected_pending_work(
            organization_id=organization_id,
            brand_id=brand_id,
            guest_or_client_id=guest_or_client_id,
            command_id=command_id,
            object_type=object_type,
            object_id=object_id,
            pending_work_ids=[item.pending_work_id for item in pending],
            reason_code=reason_code,
        )
        return self.repository.put_affected_pending_work(affected)

    @staticmethod
    def _optional_uuid(value: object) -> UUID | None:
        if isinstance(value, UUID):
            return value
        if isinstance(value, str) and value:
            return UUID(value)
        return None


def register_consent_guard(bus: CommandBus, guard: ConsentGuardService) -> None:
    bus.consent_policy = guard
