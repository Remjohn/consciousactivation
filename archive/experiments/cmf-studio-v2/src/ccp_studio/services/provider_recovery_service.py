"""Durable provider recovery service for TS-CMF-048."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

from ccp_studio.contracts.commands import CommandEnvelope
from ccp_studio.contracts.orchestration import utc_now
from ccp_studio.contracts.provider_jobs import (
    ProviderDomainEvent,
    ProviderJob,
    ProviderJobStatus,
    ProviderReceipt,
    ProviderWebhookEnvelope,
)
from ccp_studio.contracts.provider_recovery import (
    DuplicateCostRisk,
    OperationalIncident,
    OperationalIncidentType,
    ProviderJobCheckpoint,
    ProviderRecoveryAction,
    RecoveryActionStatus,
    RecoveryActionType,
    RecoveryReceipt,
    new_recovery_receipt,
)
from ccp_studio.repositories.provider_recovery import InMemoryProviderRecoveryRepository
from ccp_studio.services.command_bus import CommandBus
from ccp_studio.services.provider_operations_service import ProviderOperationsService


class ProviderRecoveryError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass
class ProviderRecoveryService:
    provider_operations: ProviderOperationsService
    repository: InMemoryProviderRecoveryRepository = field(default_factory=InMemoryProviderRecoveryRepository)

    def record_provider_job_checkpoint(
        self,
        *,
        provider_job_id: UUID,
        work_id: str,
        completed: bool,
        actor_id: UUID,
        output_artifact_uri: str | None = None,
        output_artifact_hash: str | None = None,
        cost_amount: float | None = None,
        provider_receipt_id: UUID | None = None,
    ) -> ProviderJobCheckpoint:
        self._job(provider_job_id)
        checkpoint = ProviderJobCheckpoint(
            schema_version="cmf.provider_job_checkpoint.v1",
            provider_job_checkpoint_id=uuid4(),
            provider_job_id=provider_job_id,
            work_id=work_id,
            output_artifact_uri=output_artifact_uri,
            output_artifact_hash=output_artifact_hash,
            completed=completed,
            cost_amount=cost_amount,
            provider_receipt_id=provider_receipt_id,
            recorded_at=utc_now(),
        )
        return self.repository.put_checkpoint(checkpoint)

    def pause_provider_job(
        self,
        *,
        provider_job_id: UUID,
        actor_id: UUID,
        idempotency_key: str,
        reason: str,
        command_id: UUID | None = None,
    ) -> RecoveryReceipt:
        prior = self._prior(provider_job_id, RecoveryActionType.pause, idempotency_key)
        if prior:
            return prior
        job = self._job(provider_job_id)
        if job.status in {ProviderJobStatus.succeeded, ProviderJobStatus.cancelled}:
            return self._blocked_receipt(
                job=job,
                action_type=RecoveryActionType.pause,
                idempotency_key=idempotency_key,
                reason=reason,
                actor_id=actor_id,
                decision_code="PROVIDER_JOB_PAUSE_BLOCKED_TERMINAL",
                terminal_state=job.status.value,
                command_id=command_id,
            )
        return self._receipt(
            job=job,
            action_type=RecoveryActionType.pause,
            status=RecoveryActionStatus.applied,
            idempotency_key=idempotency_key,
            reason=reason,
            actor_id=actor_id,
            decision_code="PROVIDER_JOB_PAUSED",
            terminal_state="paused",
            evidence_refs=["durable_workflow_pause_requested"],
            command_id=command_id,
        )

    def retry_provider_job(
        self,
        *,
        provider_job_id: UUID,
        actor_id: UUID,
        idempotency_key: str,
        reason: str,
        requeued_work_ids: list[str],
        allow_duplicate_cost: bool = False,
        side_effects: list[str] | None = None,
        command_id: UUID | None = None,
    ) -> RecoveryReceipt:
        prior = self._prior(provider_job_id, RecoveryActionType.retry, idempotency_key)
        if prior:
            return prior
        job = self._job(provider_job_id)
        latest = self._latest_provider_receipt(provider_job_id)
        risk = self._duplicate_cost_risk(
            job=job,
            action_type=RecoveryActionType.retry,
            requeued_work_ids=requeued_work_ids,
            side_effects=side_effects or [],
            allow_duplicate_cost=allow_duplicate_cost,
        )
        if risk.blocked:
            return self._blocked_receipt(
                job=job,
                action_type=RecoveryActionType.retry,
                idempotency_key=idempotency_key,
                reason=reason,
                actor_id=actor_id,
                decision_code="DUPLICATE_COST_RECOVERY_BLOCKED",
                duplicate_cost_risk=True,
                manual_review_required=risk.manual_review_required,
                evidence_refs=risk.risk_reasons,
                command_id=command_id,
            )
        self._assert_retry_allowed(job, latest)
        updated = job.model_copy(update={"status": ProviderJobStatus.submitted, "retry_count": job.retry_count + 1, "updated_at": utc_now()})
        self.provider_operations.repository.put_job(updated)
        self._append_provider_event("ProviderJobRetried", updated, {"requeued_work_ids": requeued_work_ids})
        return self._receipt(
            job=updated,
            action_type=RecoveryActionType.retry,
            status=RecoveryActionStatus.applied,
            idempotency_key=idempotency_key,
            reason=reason,
            actor_id=actor_id,
            decision_code="PROVIDER_JOB_RETRY_SCHEDULED",
            requeued_work_ids=requeued_work_ids,
            evidence_refs=["completed_outputs_preserved", *(latest.output_artifact_hashes if latest else [])],
            command_id=command_id,
        )

    def resume_provider_job(
        self,
        *,
        provider_job_id: UUID,
        actor_id: UUID,
        idempotency_key: str,
        reason: str,
        command_id: UUID | None = None,
    ) -> RecoveryReceipt:
        prior = self._prior(provider_job_id, RecoveryActionType.resume, idempotency_key)
        if prior:
            return prior
        job = self._job(provider_job_id)
        if job.status in {ProviderJobStatus.succeeded, ProviderJobStatus.cancelled}:
            return self._blocked_receipt(
                job=job,
                action_type=RecoveryActionType.resume,
                idempotency_key=idempotency_key,
                reason=reason,
                actor_id=actor_id,
                decision_code="PROVIDER_JOB_RESUME_BLOCKED_TERMINAL",
                terminal_state=job.status.value,
                command_id=command_id,
            )
        updated = job.model_copy(update={"status": ProviderJobStatus.running, "updated_at": utc_now()})
        self.provider_operations.repository.put_job(updated)
        self._append_provider_event("ProviderJobResumed", updated, {})
        return self._receipt(
            job=updated,
            action_type=RecoveryActionType.resume,
            status=RecoveryActionStatus.applied,
            idempotency_key=idempotency_key,
            reason=reason,
            actor_id=actor_id,
            decision_code="PROVIDER_JOB_RESUMED",
            terminal_state=ProviderJobStatus.running.value,
            evidence_refs=["durable_workflow_resume_requested"],
            command_id=command_id,
        )

    def cancel_provider_job(
        self,
        *,
        provider_job_id: UUID,
        actor_id: UUID,
        idempotency_key: str,
        reason: str,
        command_id: UUID | None = None,
    ) -> RecoveryReceipt:
        prior = self._prior(provider_job_id, RecoveryActionType.cancel, idempotency_key)
        if prior:
            return prior
        job = self._job(provider_job_id)
        if job.status == ProviderJobStatus.succeeded:
            return self._blocked_receipt(
                job=job,
                action_type=RecoveryActionType.cancel,
                idempotency_key=idempotency_key,
                reason=reason,
                actor_id=actor_id,
                decision_code="PROVIDER_JOB_CANCEL_BLOCKED_TERMINAL_SUCCESS",
                terminal_state=job.status.value,
                manual_review_required=True,
                command_id=command_id,
            )
        updated = job.model_copy(update={"status": ProviderJobStatus.cancelled, "updated_at": utc_now()})
        self.provider_operations.repository.put_job(updated)
        self._append_provider_event("ProviderJobCancelled", updated, {"reason": reason})
        return self._receipt(
            job=updated,
            action_type=RecoveryActionType.cancel,
            status=RecoveryActionStatus.applied,
            idempotency_key=idempotency_key,
            reason=reason,
            actor_id=actor_id,
            decision_code="PROVIDER_JOB_CANCELLED_RECONCILED",
            terminal_state=ProviderJobStatus.cancelled.value,
            evidence_refs=["provider_state_cancelled", "canonical_state_cancelled"],
            command_id=command_id,
        )

    def compensate_provider_job(
        self,
        *,
        provider_job_id: UUID,
        actor_id: UUID,
        idempotency_key: str,
        reason: str,
        missing_work_ids: list[str],
        command_id: UUID | None = None,
    ) -> RecoveryReceipt:
        prior = self._prior(provider_job_id, RecoveryActionType.compensate, idempotency_key)
        if prior:
            return prior
        job = self._job(provider_job_id)
        self._append_provider_event("ProviderJobCompensated", job, {"missing_work_ids": missing_work_ids})
        return self._receipt(
            job=job,
            action_type=RecoveryActionType.compensate,
            status=RecoveryActionStatus.applied,
            idempotency_key=idempotency_key,
            reason=reason,
            actor_id=actor_id,
            decision_code="PROVIDER_JOB_COMPENSATION_RECORDED",
            requeued_work_ids=missing_work_ids,
            terminal_state="compensation_pending",
            evidence_refs=["completed_outputs_preserved", "missing_work_isolated"],
            command_id=command_id,
        )

    def block_duplicate_cost_recovery(
        self,
        *,
        provider_job_id: UUID,
        actor_id: UUID,
        idempotency_key: str,
        reason: str,
        action_type: RecoveryActionType | str = RecoveryActionType.escalate,
        risk_reasons: list[str] | None = None,
        command_id: UUID | None = None,
    ) -> RecoveryReceipt:
        job = self._job(provider_job_id)
        return self._blocked_receipt(
            job=job,
            action_type=RecoveryActionType(action_type),
            idempotency_key=idempotency_key,
            reason=reason,
            actor_id=actor_id,
            decision_code="DUPLICATE_COST_RECOVERY_BLOCKED",
            duplicate_cost_risk=True,
            manual_review_required=True,
            evidence_refs=risk_reasons or ["duplicate_billing_or_publishing_risk"],
            command_id=command_id,
        )

    def record_operational_incident(
        self,
        *,
        provider_job_id: UUID,
        incident_type: OperationalIncidentType | str,
        severity: str,
        summary: str,
        actor_id: UUID,
        duplicate_webhook_count: int = 0,
        recovery_action_id: UUID | None = None,
        evidence_refs: list[str] | None = None,
    ) -> OperationalIncident:
        self._job(provider_job_id)
        incident = OperationalIncident(
            schema_version="cmf.operational_incident.v1",
            operational_incident_id=uuid4(),
            provider_job_id=provider_job_id,
            incident_type=OperationalIncidentType(incident_type),
            severity=severity,
            summary=summary,
            duplicate_webhook_count=duplicate_webhook_count,
            recovery_action_id=recovery_action_id,
            evidence_refs=evidence_refs or [],
            recorded_at=utc_now(),
        )
        return self.repository.put_incident(incident)

    def process_provider_webhook_with_recovery_guard(self, envelope: ProviderWebhookEnvelope, *, actor_id: UUID) -> ProviderReceipt:
        was_seen = envelope.idempotency_key in self.provider_operations.repository.webhook_idempotency_index
        before_completed = len([item for item in self.provider_operations.repository.domain_events if item.event_type == "ProviderJobCompleted"])
        receipt = self.provider_operations.process_provider_webhook(envelope)
        after_completed = len([item for item in self.provider_operations.repository.domain_events if item.event_type == "ProviderJobCompleted"])
        if was_seen:
            self.record_operational_incident(
                provider_job_id=receipt.provider_job_id,
                incident_type=OperationalIncidentType.duplicate_webhook,
                severity="low",
                summary="Duplicate provider webhook replayed idempotently without duplicate completion event.",
                actor_id=actor_id,
                duplicate_webhook_count=1,
                evidence_refs=[envelope.idempotency_key, f"completed_events_before:{before_completed}", f"completed_events_after:{after_completed}"],
            )
        return receipt

    def stage11_12_recovery(
        self,
        *,
        provider_job_id: UUID,
        action_type: RecoveryActionType | str,
        actor_id: UUID,
        idempotency_key: str,
        reason: str,
        requeued_work_ids: list[str] | None = None,
        missing_work_ids: list[str] | None = None,
        allow_duplicate_cost: bool = False,
        side_effects: list[str] | None = None,
    ) -> RecoveryReceipt:
        action = RecoveryActionType(action_type)
        if action == RecoveryActionType.retry:
            return self.retry_provider_job(
                provider_job_id=provider_job_id,
                actor_id=actor_id,
                idempotency_key=idempotency_key,
                reason=reason,
                requeued_work_ids=requeued_work_ids or [],
                allow_duplicate_cost=allow_duplicate_cost,
                side_effects=side_effects,
            )
        if action == RecoveryActionType.resume:
            return self.resume_provider_job(provider_job_id=provider_job_id, actor_id=actor_id, idempotency_key=idempotency_key, reason=reason)
        if action == RecoveryActionType.cancel:
            return self.cancel_provider_job(provider_job_id=provider_job_id, actor_id=actor_id, idempotency_key=idempotency_key, reason=reason)
        if action == RecoveryActionType.compensate:
            return self.compensate_provider_job(
                provider_job_id=provider_job_id,
                actor_id=actor_id,
                idempotency_key=idempotency_key,
                reason=reason,
                missing_work_ids=missing_work_ids or [],
            )
        if action == RecoveryActionType.pause:
            return self.pause_provider_job(provider_job_id=provider_job_id, actor_id=actor_id, idempotency_key=idempotency_key, reason=reason)
        return self.block_duplicate_cost_recovery(provider_job_id=provider_job_id, actor_id=actor_id, idempotency_key=idempotency_key, reason=reason)

    def _duplicate_cost_risk(
        self,
        *,
        job: ProviderJob,
        action_type: RecoveryActionType,
        requeued_work_ids: list[str],
        side_effects: list[str],
        allow_duplicate_cost: bool,
    ) -> DuplicateCostRisk:
        latest = self._latest_provider_receipt(job.provider_job_id)
        reasons: list[str] = []
        if latest and latest.status == ProviderJobStatus.succeeded and not requeued_work_ids:
            reasons.append("completed_paid_job_has_no_incomplete_work")
        if {"publishing", "final_approval"}.intersection(side_effects):
            reasons.append("public_or_approval_side_effect_may_repeat")
        risk = bool(reasons)
        duplicate = DuplicateCostRisk(
            schema_version="cmf.duplicate_cost_risk.v1",
            duplicate_cost_risk_id=uuid4(),
            provider_job_id=job.provider_job_id,
            action_type=action_type,
            risk_detected=risk,
            risk_reasons=reasons,
            manual_review_required=risk,
            blocked=risk and not allow_duplicate_cost,
            created_at=utc_now(),
        )
        return self.repository.put_duplicate_cost_risk(duplicate)

    def _assert_retry_allowed(self, job: ProviderJob, latest: ProviderReceipt | None) -> None:
        policy = self.provider_operations.retry_policies[job.retry_policy_id]
        if job.retry_count >= policy.max_retries:
            raise ProviderRecoveryError("RETRY_POLICY_EXHAUSTED", "Provider retry policy has been exhausted.")
        if latest and latest.status == ProviderJobStatus.failed and latest.failure_code not in policy.retryable_failure_codes:
            raise ProviderRecoveryError("PROVIDER_FAILURE_NOT_RETRYABLE", "Provider failure code is not retryable.")

    def _receipt(
        self,
        *,
        job: ProviderJob,
        action_type: RecoveryActionType,
        status: RecoveryActionStatus,
        idempotency_key: str,
        reason: str,
        actor_id: UUID,
        decision_code: str,
        requeued_work_ids: list[str] | None = None,
        terminal_state: str | None = None,
        evidence_refs: list[str] | None = None,
        command_id: UUID | None = None,
    ) -> RecoveryReceipt:
        preserved_hashes = self._preserved_output_hashes(job.provider_job_id)
        action = self.repository.put_action(
            ProviderRecoveryAction(
                schema_version="cmf.provider_recovery_action.v1",
                provider_recovery_action_id=uuid4(),
                provider_job_id=job.provider_job_id,
                action_type=action_type,
                status=status,
                idempotency_key=idempotency_key,
                reason=reason,
                duplicate_cost_risk=False,
                preserved_output_hashes=preserved_hashes,
                requeued_work_ids=requeued_work_ids or [],
                terminal_state=terminal_state,
                created_at=utc_now(),
            )
        )
        return self.repository.put_receipt(
            new_recovery_receipt(
                provider_job_id=job.provider_job_id,
                action=action,
                decision_code=decision_code,
                actor_id=actor_id,
                evidence_refs=evidence_refs or [],
                command_id=command_id,
            )
        )

    def _blocked_receipt(
        self,
        *,
        job: ProviderJob,
        action_type: RecoveryActionType,
        idempotency_key: str,
        reason: str,
        actor_id: UUID,
        decision_code: str,
        duplicate_cost_risk: bool = False,
        manual_review_required: bool = False,
        terminal_state: str | None = None,
        evidence_refs: list[str] | None = None,
        command_id: UUID | None = None,
    ) -> RecoveryReceipt:
        action = self.repository.put_action(
            ProviderRecoveryAction(
                schema_version="cmf.provider_recovery_action.v1",
                provider_recovery_action_id=uuid4(),
                provider_job_id=job.provider_job_id,
                action_type=action_type,
                status=RecoveryActionStatus.escalated if manual_review_required else RecoveryActionStatus.blocked,
                idempotency_key=idempotency_key,
                reason=reason,
                duplicate_cost_risk=duplicate_cost_risk,
                manual_review_required=manual_review_required,
                preserved_output_hashes=self._preserved_output_hashes(job.provider_job_id),
                terminal_state=terminal_state,
                created_at=utc_now(),
            )
        )
        return self.repository.put_receipt(
            new_recovery_receipt(
                provider_job_id=job.provider_job_id,
                action=action,
                decision_code=decision_code,
                actor_id=actor_id,
                evidence_refs=evidence_refs or [],
                command_id=command_id,
            )
        )

    def _preserved_output_hashes(self, provider_job_id: UUID) -> list[str]:
        checkpoint_hashes = [
            item.output_artifact_hash
            for item in self.repository.checkpoints_for_job(provider_job_id)
            if item.completed and item.output_artifact_hash
        ]
        receipt_hashes: list[str] = []
        latest = self._latest_provider_receipt(provider_job_id)
        if latest is not None:
            receipt_hashes = latest.output_artifact_hashes
        return sorted(set([*checkpoint_hashes, *receipt_hashes]))

    def _prior(self, provider_job_id: UUID, action_type: RecoveryActionType, idempotency_key: str) -> RecoveryReceipt | None:
        return self.repository.receipt_for_idempotency(provider_job_id, action_type, idempotency_key)

    def _latest_provider_receipt(self, provider_job_id: UUID) -> ProviderReceipt | None:
        receipts = [item for item in self.provider_operations.repository.receipts.values() if item.provider_job_id == provider_job_id]
        if not receipts:
            return None
        return sorted(receipts, key=lambda item: item.created_at)[-1]

    def _job(self, provider_job_id: UUID) -> ProviderJob:
        job = self.provider_operations.repository.jobs.get(provider_job_id)
        if job is None:
            raise ProviderRecoveryError("PROVIDER_JOB_REQUIRED", "Provider job is required for recovery.")
        return job

    def _append_provider_event(self, event_type: str, job: ProviderJob, payload: dict[str, Any]) -> ProviderDomainEvent:
        return self.provider_operations.repository.append_event(
            ProviderDomainEvent(
                schema_version="cmf.provider_domain_event.v1",
                provider_event_id=uuid4(),
                event_type=event_type,
                provider_job_id=job.provider_job_id,
                payload=payload,
                created_at=utc_now(),
            )
        )


@dataclass
class ProviderRecoveryCommandHandler:
    command_type: str
    service: ProviderRecoveryService
    aggregate_type: str = "provider_recovery"
    allowed_roles: set[str] = field(default_factory=lambda: {"owner", "admin", "operator", "production_steward", "provider_webhook"})
    requires_existing_brand_scope: bool = True

    def handle(self, envelope: CommandEnvelope) -> dict[str, Any]:
        payload = envelope.payload
        provider_job_id = UUID(payload["provider_job_id"])
        common = {
            "provider_job_id": provider_job_id,
            "actor_id": envelope.actor.actor_id,
            "idempotency_key": payload.get("recovery_idempotency_key", envelope.idempotency_key),
            "reason": payload.get("reason", envelope.command_type),
            "command_id": envelope.command_id,
        }
        if self.command_type == "PauseProviderJobCommand":
            return self.service.pause_provider_job(**common).model_dump(mode="json")
        if self.command_type == "RetryProviderJobCommand":
            return self.service.retry_provider_job(
                **common,
                requeued_work_ids=payload.get("requeued_work_ids", []),
                allow_duplicate_cost=bool(payload.get("allow_duplicate_cost", False)),
                side_effects=payload.get("side_effects", []),
            ).model_dump(mode="json")
        if self.command_type == "ResumeProviderJobCommand":
            return self.service.resume_provider_job(**common).model_dump(mode="json")
        if self.command_type == "CancelProviderJobCommand":
            return self.service.cancel_provider_job(**common).model_dump(mode="json")
        if self.command_type == "CompensateProviderJobCommand":
            return self.service.compensate_provider_job(
                **common,
                missing_work_ids=payload.get("missing_work_ids", []),
            ).model_dump(mode="json")
        if self.command_type == "BlockDuplicateCostRecoveryCommand":
            return self.service.block_duplicate_cost_recovery(
                **common,
                action_type=payload.get("action_type", RecoveryActionType.escalate.value),
                risk_reasons=payload.get("risk_reasons", []),
            ).model_dump(mode="json")
        if self.command_type == "RecordOperationalIncidentCommand":
            return self.service.record_operational_incident(
                provider_job_id=provider_job_id,
                incident_type=payload["incident_type"],
                severity=payload.get("severity", "medium"),
                summary=payload["summary"],
                actor_id=envelope.actor.actor_id,
                duplicate_webhook_count=int(payload.get("duplicate_webhook_count", 0)),
                recovery_action_id=UUID(payload["recovery_action_id"]) if payload.get("recovery_action_id") else None,
                evidence_refs=payload.get("evidence_refs", []),
            ).model_dump(mode="json")
        raise ProviderRecoveryError("COMMAND_HANDLER_NOT_REGISTERED", self.command_type)

    def aggregate_id(self, envelope: CommandEnvelope, payload: dict[str, Any]) -> UUID:
        raw = payload.get("recovery_receipt_id") or payload.get("operational_incident_id") or envelope.payload.get("provider_job_id")
        if isinstance(raw, str):
            return UUID(raw)
        if isinstance(raw, UUID):
            return raw
        return envelope.brand_id


def register_provider_recovery_command_handlers(bus: CommandBus, service: ProviderRecoveryService) -> None:
    for command_type in [
        "PauseProviderJobCommand",
        "RetryProviderJobCommand",
        "ResumeProviderJobCommand",
        "CancelProviderJobCommand",
        "CompensateProviderJobCommand",
        "BlockDuplicateCostRecoveryCommand",
        "RecordOperationalIncidentCommand",
    ]:
        bus.register_handler(ProviderRecoveryCommandHandler(command_type=command_type, service=service))
