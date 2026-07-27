"""Commercial entitlement and cost policy service for TS-CMF-006."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.commercial import (
    PUBLIC_OFFER_COPY,
    CommercialEntitlement,
    CommercialPolicyDecision,
    CostPolicy,
    CostReceipt,
    EntitlementStatus,
    PublicContentOffer,
    QuotaPolicy,
    UsageLedgerEntry,
    new_commercial_entitlement,
)
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.repositories.commercial_entitlements import InMemoryCommercialRepository
from ccp_studio.services.command_bus import CommandBus


PRODUCTION_COMMANDS = {
    "StartProductionCommand",
    "QueueRenderCommand",
    "SubmitProviderJobCommand",
    "GenerateAssetPackageSpecCommand",
    "PublishIntentCommand",
}

FORBIDDEN_PUBLIC_LABELS = {
    "newsletter",
    "newsletters",
    "credit bundle",
    "credits",
    "lite plan",
    "pro plan",
    "enterprise tier",
}


class CommercialPolicyError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class CommercialPolicyService:
    repository: InMemoryCommercialRepository = field(default_factory=InMemoryCommercialRepository)

    def render_public_offer_copy(self, public_offer: PublicContentOffer | str) -> str:
        try:
            offer = PublicContentOffer(public_offer)
        except ValueError as exc:
            raise CommercialPolicyError(
                "PUBLIC_OFFER_NOT_ALLOWED",
                "Only trial Guest Asset Pack or Monthly Asset Engine may render publicly.",
            ) from exc
        return PUBLIC_OFFER_COPY[offer]

    def validate_public_copy(self, copy: str) -> None:
        lowered = copy.lower()
        if any(label in lowered for label in FORBIDDEN_PUBLIC_LABELS):
            raise CommercialPolicyError(
                "PUBLIC_OFFER_DRIFT_BLOCKED",
                "Public copy contains unsupported offer drift.",
            )

    def create_entitlement(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        public_offer: PublicContentOffer,
        provider_budget_cents_per_period: int | None = None,
        manual_override_above_cents: int | None = None,
        max_provider_jobs_per_period: int | None = None,
    ) -> CommercialEntitlement:
        entitlement = new_commercial_entitlement(
            organization_id=organization_id,
            brand_id=brand_id,
            public_offer=public_offer,
        )
        self.repository.put_entitlement(entitlement)
        self.repository.put_quota_policy(
            QuotaPolicy(
                schema_version="cmf.quota_policy.v1",
                quota_policy_id=uuid4(),
                entitlement_id=entitlement.commercial_entitlement_id,
                max_provider_jobs_per_period=max_provider_jobs_per_period,
            )
        )
        self.repository.put_cost_policy(
            CostPolicy(
                schema_version="cmf.cost_policy.v1",
                cost_policy_id=uuid4(),
                entitlement_id=entitlement.commercial_entitlement_id,
                provider_budget_cents_per_period=provider_budget_cents_per_period,
                requires_manual_override_above_cents=manual_override_above_cents,
            )
        )
        return entitlement

    def update_entitlement_status(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        status: EntitlementStatus,
    ) -> CommercialEntitlement:
        entitlement = self._require_entitlement(organization_id, brand_id)
        entitlement.status = status
        self.repository.put_entitlement(entitlement)
        return entitlement

    def record_usage(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        usage_type: str,
        quantity: int,
        command_id: UUID | None = None,
    ) -> UsageLedgerEntry:
        entitlement = self._require_entitlement(organization_id, brand_id)
        entry = UsageLedgerEntry(
            schema_version="cmf.usage_ledger_entry.v1",
            usage_ledger_entry_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            entitlement_id=entitlement.commercial_entitlement_id,
            usage_type=usage_type,
            quantity=quantity,
            command_id=command_id,
            recorded_at=utc_now(),
        )
        return self.repository.put_usage_entry(entry)

    def evaluate_command(self, envelope: CommandEnvelope) -> CommercialPolicyDecision:
        if envelope.command_type not in PRODUCTION_COMMANDS:
            return self._decision(envelope, True, "COMMERCIAL_POLICY_NOT_APPLICABLE", None)
        entitlement = self.repository.get_entitlement(envelope.organization_id, envelope.brand_id)
        if entitlement is None:
            return self._blocked(envelope, "COMMERCIAL_ENTITLEMENT_REQUIRED", None)
        if entitlement.status == EntitlementStatus.expired:
            return self._blocked(envelope, "COMMERCIAL_ENTITLEMENT_EXPIRED", entitlement)
        if entitlement.status == EntitlementStatus.suspended:
            return self._blocked(envelope, "COMMERCIAL_ENTITLEMENT_SUSPENDED", entitlement)
        if entitlement.status == EntitlementStatus.cancelled:
            return self._blocked(envelope, "COMMERCIAL_ENTITLEMENT_CANCELLED", entitlement)

        requirements_missing = [
            key
            for key in [
                "source_lineage_ref",
                "consent_receipt_id",
                "evaluation_receipt_required",
                "human_approval_required",
                "valid_format_key",
            ]
            if not envelope.payload.get(key)
        ]
        if requirements_missing:
            return self._blocked(
                envelope,
                "PRODUCTION_REQUIREMENTS_INCOMPLETE",
                entitlement,
                evidence_refs=requirements_missing,
            )

        quota = self.repository.get_quota_policy(entitlement.commercial_entitlement_id)
        if quota and quota.max_provider_jobs_per_period is not None:
            used = self.repository.count_usage(entitlement.commercial_entitlement_id, "provider_job")
            requested = int(envelope.payload.get("provider_job_count", 0))
            if used + requested > quota.max_provider_jobs_per_period:
                return self._blocked(envelope, "QUOTA_EXCEEDED", entitlement)

        cost_policy = self.repository.get_cost_policy(entitlement.commercial_entitlement_id)
        estimated_cost = envelope.payload.get("estimated_cost_cents")
        if cost_policy and estimated_cost is not None:
            threshold = cost_policy.requires_manual_override_above_cents
            if threshold is not None and estimated_cost > threshold and not envelope.payload.get("manual_override_approved"):
                return self._blocked(envelope, "MANUAL_OVERRIDE_REQUIRED", entitlement, estimated_cost)

        decision = self._decision(envelope, True, "COMMERCIAL_POLICY_ALLOWED", entitlement, estimated_cost)
        self._write_cost_receipt(envelope, entitlement, decision.decision_code, estimated_cost)
        return decision

    def _blocked(
        self,
        envelope: CommandEnvelope,
        decision_code: str,
        entitlement: CommercialEntitlement | None,
        estimated_cost_cents: int | None = None,
        evidence_refs: list[str] | None = None,
    ) -> CommercialPolicyDecision:
        decision = self._decision(envelope, False, decision_code, entitlement, estimated_cost_cents)
        if entitlement is not None:
            self._write_cost_receipt(
                envelope,
                entitlement,
                decision_code,
                estimated_cost_cents,
                evidence_refs=evidence_refs,
            )
        return decision

    def _decision(
        self,
        envelope: CommandEnvelope,
        allowed: bool,
        decision_code: str,
        entitlement: CommercialEntitlement | None,
        estimated_cost_cents: int | None = None,
    ) -> CommercialPolicyDecision:
        return CommercialPolicyDecision(
            schema_version="cmf.commercial_policy_decision.v1",
            organization_id=envelope.organization_id,
            brand_id=envelope.brand_id,
            command_type=envelope.command_type,
            allowed=allowed,
            decision_code=decision_code,
            entitlement_id=entitlement.commercial_entitlement_id if entitlement else None,
            estimated_cost_cents=estimated_cost_cents,
            decided_at=utc_now(),
        )

    def _write_cost_receipt(
        self,
        envelope: CommandEnvelope,
        entitlement: CommercialEntitlement,
        decision_code: str,
        estimated_cost_cents: int | None,
        evidence_refs: list[str] | None = None,
    ) -> CostReceipt:
        receipt = CostReceipt(
            schema_version="cmf.cost_receipt.v1",
            cost_receipt_id=uuid4(),
            organization_id=envelope.organization_id,
            brand_id=envelope.brand_id,
            command_id=envelope.command_id,
            entitlement_id=entitlement.commercial_entitlement_id,
            policy_decision=decision_code,
            estimated_cost_cents=estimated_cost_cents,
            evidence_refs=evidence_refs or [],
            written_at=utc_now(),
        )
        return self.repository.put_cost_receipt(receipt)

    def _require_entitlement(self, organization_id: UUID, brand_id: UUID) -> CommercialEntitlement:
        entitlement = self.repository.get_entitlement(organization_id, brand_id)
        if entitlement is None:
            raise CommercialPolicyError("COMMERCIAL_ENTITLEMENT_REQUIRED", "Entitlement not found.")
        return entitlement


@dataclass
class CommercialCommandHandler:
    command_type: str
    service: CommercialPolicyService
    aggregate_type: str = "commercial_entitlement"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "commercial_administrator"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "CreateCommercialEntitlementCommand":
            entitlement = self.service.create_entitlement(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                public_offer=PublicContentOffer(payload["public_offer"]),
                provider_budget_cents_per_period=payload.get("provider_budget_cents_per_period"),
                manual_override_above_cents=payload.get("manual_override_above_cents"),
                max_provider_jobs_per_period=payload.get("max_provider_jobs_per_period"),
            )
            return entitlement.model_dump(mode="json")
        if self.command_type == "UpdateCommercialEntitlementCommand":
            entitlement = self.service.update_entitlement_status(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                status=EntitlementStatus(payload["status"]),
            )
            return entitlement.model_dump(mode="json")
        if self.command_type == "EvaluateCommercialPolicyCommand":
            decision = self.service.evaluate_command(envelope)
            return decision.model_dump(mode="json")
        if self.command_type == "RecordUsageCommand":
            entry = self.service.record_usage(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                usage_type=payload["usage_type"],
                quantity=int(payload["quantity"]),
                command_id=envelope.command_id,
            )
            return entry.model_dump(mode="json")
        raise CommercialPolicyError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("commercial_entitlement_id")
        if isinstance(raw, str):
            return UUID(raw)
        return envelope.brand_id


def register_commercial_command_handlers(bus: CommandBus, service: CommercialPolicyService) -> None:
    bus.commercial_policy = service
    for command_type in [
        "CreateCommercialEntitlementCommand",
        "UpdateCommercialEntitlementCommand",
        "EvaluateCommercialPolicyCommand",
        "RecordUsageCommand",
    ]:
        bus.register_handler(CommercialCommandHandler(command_type=command_type, service=service))
