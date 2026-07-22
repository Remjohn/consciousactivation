"""Publishing Intent and Publer adapter service for TS-CMF-054."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.publishing import (
    PublerJob,
    PublerJobStatus,
    PublerWebhookEnvelope,
    PublishingDomainEvent,
    PublishingIntent,
    PublishingIntentStatus,
    PublishingOutcome,
    PublishingPlatformVariant,
    PublishingReceipt,
    PublishingSchedule,
    new_publishing_receipt,
)
from ccp_studio.providers.publer import PublerAdapter
from ccp_studio.repositories.publishing import InMemoryPublishingRepository
from ccp_studio.services.command_bus import CommandBus


ACTIVE_PUBLISHING_STATUSES = {
    PublishingIntentStatus.draft,
    PublishingIntentStatus.validated,
    PublishingIntentStatus.confirmed,
    PublishingIntentStatus.submitted,
    PublishingIntentStatus.succeeded,
}


class PublishingError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class PublishingService:
    repository: InMemoryPublishingRepository = field(default_factory=InMemoryPublishingRepository)
    publer_adapter: PublerAdapter = field(default_factory=PublerAdapter)

    def draft_publishing_intent(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        approved_asset_id: UUID,
        approval_event_id: UUID | None,
        consent_record_version_id: UUID | None,
        approver_user_id: UUID,
        platform_variants: list[PublishingPlatformVariant | dict[str, Any]],
        schedule: PublishingSchedule | dict[str, Any],
        idempotency_key: str,
        compliance_notes: list[str] | None = None,
        command_id: UUID | None = None,
    ) -> PublishingIntent:
        variants = [item if isinstance(item, PublishingPlatformVariant) else PublishingPlatformVariant.model_validate(item) for item in platform_variants]
        parsed_schedule = schedule if isinstance(schedule, PublishingSchedule) else PublishingSchedule.model_validate(schedule)
        blockers = self._draft_blockers(approval_event_id, consent_record_version_id, variants)
        duplicate = self._duplicate_intent(approved_asset_id, variants, parsed_schedule)
        if duplicate:
            blockers.append("DUPLICATE_PUBLISHING_INTENT")
        if blockers:
            self._blocked_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                approved_asset_id=approved_asset_id,
                decision_code="PUBLISHING_INTENT_DRAFT_BLOCKED",
                blocker_codes=blockers,
                idempotency_key=idempotency_key,
                command_id=command_id,
            )
            raise PublishingError(blockers[0], "Publishing Intent draft is blocked.")
        now = utc_now()
        intent = PublishingIntent(
            schema_version="cmf.publishing_intent.v1",
            publishing_intent_id=uuid4(),
            organization_id=organization_id,
            brand_id=brand_id,
            approved_asset_id=approved_asset_id,
            approval_event_id=approval_event_id,
            consent_record_version_id=consent_record_version_id,
            approver_user_id=approver_user_id,
            platform_variants=variants,
            schedule=parsed_schedule,
            status=PublishingIntentStatus.draft,
            idempotency_key=idempotency_key,
            compliance_notes=compliance_notes or [],
            created_at=now,
            updated_at=now,
        )
        self.repository.put_intent(intent)
        self._receipt(intent, "PUBLISHING_INTENT_DRAFTED", command_id=command_id)
        self._event("PublishingIntentDrafted", intent, {})
        return intent

    def validate_publishing_intent(self, publishing_intent_id: UUID, *, command_id: UUID | None = None) -> PublishingIntent:
        intent = self._intent(publishing_intent_id)
        blockers = self._draft_blockers(intent.approval_event_id, intent.consent_record_version_id, intent.platform_variants)
        if blockers:
            self._receipt(intent, "PUBLISHING_INTENT_VALIDATION_BLOCKED", blocker_codes=blockers, command_id=command_id)
            raise PublishingError(blockers[0], "Publishing Intent validation is blocked.")
        updated = intent.model_copy(update={"status": PublishingIntentStatus.validated, "updated_at": utc_now()})
        self.repository.put_intent(updated)
        self._receipt(updated, "PUBLISHING_INTENT_VALIDATED", command_id=command_id)
        self._event("PublishingIntentValidated", updated, {})
        return updated

    def confirm_publishing_intent(
        self,
        publishing_intent_id: UUID,
        *,
        confirmed_by_user_id: UUID,
        human_confirmation: bool,
        command_id: UUID | None = None,
    ) -> PublishingIntent:
        intent = self._intent(publishing_intent_id)
        if intent.status not in {PublishingIntentStatus.validated, PublishingIntentStatus.confirmed}:
            self._receipt(intent, "PUBLISHING_INTENT_CONFIRMATION_BLOCKED", blocker_codes=["PUBLISHING_INTENT_VALIDATION_REQUIRED"], command_id=command_id)
            raise PublishingError("PUBLISHING_INTENT_VALIDATION_REQUIRED", "Publishing Intent must be validated before confirmation.")
        if not human_confirmation:
            self._receipt(intent, "PUBLISHING_INTENT_CONFIRMATION_BLOCKED", blocker_codes=["HUMAN_CONFIRMATION_REQUIRED"], command_id=command_id)
            raise PublishingError("HUMAN_CONFIRMATION_REQUIRED", "Human confirmation is required before Publer submission.")
        updated = intent.model_copy(
            update={
                "confirmed_by_user_id": confirmed_by_user_id,
                "status": PublishingIntentStatus.confirmed,
                "updated_at": utc_now(),
            }
        )
        self.repository.put_intent(updated)
        self._receipt(updated, "PUBLISHING_INTENT_CONFIRMED", command_id=command_id)
        self._event("PublishingIntentConfirmed", updated, {"confirmed_by_user_id": str(confirmed_by_user_id)})
        return updated

    def submit_publishing_intent_to_publer(
        self,
        publishing_intent_id: UUID,
        *,
        idempotency_key: str,
        command_id: UUID | None = None,
    ) -> PublerJob:
        intent = self._intent(publishing_intent_id)
        if intent.status != PublishingIntentStatus.confirmed:
            self._receipt(intent, "PUBLER_SUBMISSION_BLOCKED", blocker_codes=["PUBLISHING_INTENT_CONFIRMATION_REQUIRED"], command_id=command_id)
            raise PublishingError("PUBLISHING_INTENT_CONFIRMATION_REQUIRED", "Only confirmed Publishing Intents can be submitted to Publer.")
        prior_id = self.repository.submit_idempotency_index.get(idempotency_key)
        if prior_id:
            return self.repository.publer_jobs[prior_id]
        duplicate = self._duplicate_intent(intent.approved_asset_id, intent.platform_variants, intent.schedule, exclude_intent_id=intent.publishing_intent_id)
        if duplicate:
            self._receipt(intent, "DUPLICATE_PUBLISHING_BLOCKED", blocker_codes=["DUPLICATE_PUBLISHING_INTENT"], idempotency_key=idempotency_key, command_id=command_id)
            self._event("DuplicatePublishingBlocked", intent, {"duplicate_intent_id": str(duplicate.publishing_intent_id)})
            raise PublishingError("DUPLICATE_PUBLISHING_INTENT", "Duplicate scheduling attempt is blocked.")
        adapter_result = self.publer_adapter.submit_confirmed_intent(intent, idempotency_key=idempotency_key)
        job = PublerJob(
            schema_version="cmf.publer_job.v1",
            publer_job_id=uuid4(),
            publishing_intent_id=intent.publishing_intent_id,
            external_job_id=adapter_result["external_job_id"],
            request_receipt_id=uuid4(),
            status=PublerJobStatus(adapter_result["status"]),
            idempotency_key=idempotency_key,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        self.repository.put_publer_job(job)
        updated = intent.model_copy(update={"status": PublishingIntentStatus.submitted, "updated_at": utc_now()})
        self.repository.put_intent(updated)
        self._receipt(updated, "PUBLISHING_INTENT_SUBMITTED_TO_PUBLER", publer_job=job, idempotency_key=idempotency_key, command_id=command_id)
        self._event("PublishingIntentSubmittedToPubler", updated, {"publer_job_id": str(job.publer_job_id), "external_job_id": job.external_job_id})
        return job

    def reconcile_publer_status(
        self,
        envelope: PublerWebhookEnvelope,
        *,
        source: str = "webhook",
        command_id: UUID | None = None,
    ) -> PublishingOutcome:
        prior_id = self.repository.webhook_idempotency_index.get(envelope.idempotency_key)
        if prior_id:
            return self.repository.outcomes[prior_id]
        intent = self._intent(envelope.publishing_intent_id)
        job = self._job_for_external(envelope.external_job_id)
        outcome = PublishingOutcome(
            schema_version="cmf.publishing_outcome.v1",
            publishing_outcome_id=uuid4(),
            publishing_intent_id=intent.publishing_intent_id,
            publer_job_id=job.publer_job_id if job else None,
            external_status=envelope.external_status,
            external_url=envelope.external_url,
            failure_reason=envelope.failure_reason,
            source=source,  # type: ignore[arg-type]
            received_at=envelope.received_at,
        )
        self.repository.put_outcome(outcome, webhook_idempotency_key=envelope.idempotency_key)
        if job:
            self.repository.put_publer_job(job.model_copy(update={"status": envelope.external_status, "updated_at": utc_now()}))
        updated_status = self._intent_status_for_outcome(envelope.external_status)
        updated = intent.model_copy(update={"status": updated_status, "updated_at": utc_now()})
        self.repository.put_intent(updated)
        self.repository.memory_admission_proposals.append(outcome.publishing_outcome_id)
        self._receipt(updated, "PUBLER_STATUS_RECONCILED", publer_job=job, outcome=outcome, command_id=command_id)
        self._event("PublerStatusReconciled", updated, {"external_status": envelope.external_status.value, "outcome_id": str(outcome.publishing_outcome_id)})
        return outcome

    def cancel_publishing_intent(self, publishing_intent_id: UUID, *, actor_id: UUID, command_id: UUID | None = None) -> PublishingIntent:
        intent = self._intent(publishing_intent_id)
        updated = intent.model_copy(update={"status": PublishingIntentStatus.cancelled, "updated_at": utc_now()})
        self.repository.put_intent(updated)
        self._receipt(updated, "PUBLISHING_INTENT_CANCELLED", evidence_refs=[f"actor:{actor_id}"], command_id=command_id)
        self._event("PublishingIntentCancelled", updated, {"actor_id": str(actor_id)})
        return updated

    def stage14_publish_intent(self, publishing_intent_id: UUID, *, idempotency_key: str) -> PublerJob:
        return self.submit_publishing_intent_to_publer(publishing_intent_id, idempotency_key=idempotency_key)

    @staticmethod
    def _intent_status_for_outcome(status: PublerJobStatus) -> PublishingIntentStatus:
        if status == PublerJobStatus.published:
            return PublishingIntentStatus.succeeded
        if status == PublerJobStatus.failed:
            return PublishingIntentStatus.failed
        if status == PublerJobStatus.cancelled:
            return PublishingIntentStatus.cancelled
        return PublishingIntentStatus.submitted

    @staticmethod
    def _draft_blockers(
        approval_event_id: UUID | None,
        consent_record_version_id: UUID | None,
        variants: list[PublishingPlatformVariant],
    ) -> list[str]:
        blockers: list[str] = []
        if approval_event_id is None:
            blockers.append("APPROVAL_EVENT_REQUIRED")
        if consent_record_version_id is None:
            blockers.append("CONSENT_RECORD_VERSION_REQUIRED")
        if not variants:
            blockers.append("PUBLISHING_PLATFORM_VARIANT_REQUIRED")
        for variant in variants:
            if not variant.asset_uri or not variant.caption_manifest_id or not variant.account_mapping_id or not variant.platform_format_key:
                blockers.append("PUBLISHING_PLATFORM_VARIANT_INCOMPLETE")
        return blockers

    def _duplicate_intent(
        self,
        approved_asset_id: UUID,
        variants: list[PublishingPlatformVariant],
        schedule: PublishingSchedule,
        *,
        exclude_intent_id: UUID | None = None,
    ) -> PublishingIntent | None:
        requested = {
            (variant.platform_variant_id, variant.account_mapping_id, schedule.schedule_at.isoformat())
            for variant in variants
        }
        for intent in self.repository.intents.values():
            if exclude_intent_id and intent.publishing_intent_id == exclude_intent_id:
                continue
            if intent.approved_asset_id != approved_asset_id or intent.status not in ACTIVE_PUBLISHING_STATUSES:
                continue
            existing = {
                (variant.platform_variant_id, variant.account_mapping_id, intent.schedule.schedule_at.isoformat())
                for variant in intent.platform_variants
            }
            if requested.intersection(existing):
                return intent
        return None

    def _receipt(
        self,
        intent: PublishingIntent,
        decision_code: str,
        *,
        publer_job: PublerJob | None = None,
        outcome: PublishingOutcome | None = None,
        blocker_codes: list[str] | None = None,
        evidence_refs: list[str] | None = None,
        idempotency_key: str | None = None,
        command_id: UUID | None = None,
    ) -> PublishingReceipt:
        return self.repository.put_receipt(
            new_publishing_receipt(
                organization_id=intent.organization_id,
                brand_id=intent.brand_id,
                publishing_intent=intent,
                publer_job=publer_job,
                outcome=outcome,
                decision_code=decision_code,
                blocker_codes=blocker_codes,
                evidence_refs=evidence_refs or [str(intent.approval_event_id), str(intent.consent_record_version_id)],
                idempotency_key=idempotency_key,
            )
        )

    def _blocked_receipt(
        self,
        *,
        organization_id: UUID,
        brand_id: UUID,
        approved_asset_id: UUID,
        decision_code: str,
        blocker_codes: list[str],
        idempotency_key: str,
        command_id: UUID | None = None,
    ) -> PublishingReceipt:
        return self.repository.put_receipt(
            new_publishing_receipt(
                organization_id=organization_id,
                brand_id=brand_id,
                decision_code=decision_code,
                blocker_codes=blocker_codes,
                evidence_refs=[str(approved_asset_id)],
                idempotency_key=idempotency_key,
            )
        )

    def _intent(self, publishing_intent_id: UUID) -> PublishingIntent:
        intent = self.repository.intents.get(publishing_intent_id)
        if intent is None:
            raise PublishingError("PUBLISHING_INTENT_REQUIRED", "Publishing Intent is required.")
        return intent

    def _job_for_external(self, external_job_id: str) -> PublerJob | None:
        return next((job for job in self.repository.publer_jobs.values() if job.external_job_id == external_job_id), None)

    def _event(self, event_type: str, intent: PublishingIntent, payload: dict[str, Any]) -> PublishingDomainEvent:
        return self.repository.append_event(
            PublishingDomainEvent(
                schema_version="cmf.publishing_domain_event.v1",
                publishing_event_id=uuid4(),
                event_type=event_type,
                publishing_intent_id=intent.publishing_intent_id,
                payload=payload,
                created_at=utc_now(),
            )
        )


@dataclass
class PublishingCommandHandler:
    command_type: str
    service: PublishingService
    aggregate_type: str = "publishing"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "publishing_approver", "production_steward"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        if self.command_type == "DraftPublishingIntentCommand":
            return self.service.draft_publishing_intent(
                organization_id=envelope.organization_id,
                brand_id=envelope.brand_id,
                approved_asset_id=UUID(payload["approved_asset_id"]),
                approval_event_id=UUID(payload["approval_event_id"]) if payload.get("approval_event_id") else None,
                consent_record_version_id=UUID(payload["consent_record_version_id"]) if payload.get("consent_record_version_id") else None,
                approver_user_id=envelope.actor.actor_id,
                platform_variants=payload["platform_variants"],
                schedule=payload["schedule"],
                idempotency_key=payload.get("publishing_idempotency_key", envelope.idempotency_key),
                compliance_notes=payload.get("compliance_notes", []),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "ValidatePublishingIntentCommand":
            return self.service.validate_publishing_intent(UUID(payload["publishing_intent_id"]), command_id=envelope.command_id).model_dump(mode="json")
        if self.command_type == "ConfirmPublishingIntentCommand":
            return self.service.confirm_publishing_intent(
                UUID(payload["publishing_intent_id"]),
                confirmed_by_user_id=envelope.actor.actor_id,
                human_confirmation=bool(payload.get("human_confirmation", False)),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "SubmitPublishingIntentToPublerCommand":
            return self.service.submit_publishing_intent_to_publer(
                UUID(payload["publishing_intent_id"]),
                idempotency_key=payload.get("publer_idempotency_key", envelope.idempotency_key),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "ReconcilePublerStatusCommand":
            return self.service.reconcile_publer_status(
                PublerWebhookEnvelope.model_validate(payload["webhook"]),
                source=payload.get("source", "webhook"),
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        if self.command_type == "BlockDuplicatePublishingCommand":
            intent = self.service._intent(UUID(payload["publishing_intent_id"]))
            duplicate = self.service._duplicate_intent(
                intent.approved_asset_id,
                intent.platform_variants,
                intent.schedule,
                exclude_intent_id=intent.publishing_intent_id,
            )
            if duplicate:
                self.service._receipt(intent, "DUPLICATE_PUBLISHING_BLOCKED", blocker_codes=["DUPLICATE_PUBLISHING_INTENT"], command_id=envelope.command_id)
                return {"blocked": True, "duplicate_intent_id": str(duplicate.publishing_intent_id)}
            return {"blocked": False}
        if self.command_type == "CancelPublishingIntentCommand":
            return self.service.cancel_publishing_intent(
                UUID(payload["publishing_intent_id"]),
                actor_id=envelope.actor.actor_id,
                command_id=envelope.command_id,
            ).model_dump(mode="json")
        raise PublishingError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("publishing_intent_id") or payload.get("approved_asset_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_publishing_command_handlers(bus: CommandBus, service: PublishingService) -> None:
    for command_type in [
        "DraftPublishingIntentCommand",
        "ValidatePublishingIntentCommand",
        "ConfirmPublishingIntentCommand",
        "SubmitPublishingIntentToPublerCommand",
        "ReconcilePublerStatusCommand",
        "BlockDuplicatePublishingCommand",
        "CancelPublishingIntentCommand",
    ]:
        bus.register_handler(PublishingCommandHandler(command_type=command_type, service=service))

