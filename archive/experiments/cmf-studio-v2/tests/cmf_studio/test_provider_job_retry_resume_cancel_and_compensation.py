from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.provider_jobs import ProviderJobStatus, ProviderWebhookEnvelope  # noqa: E402
from ccp_studio.contracts.provider_recovery import OperationalIncidentType, RecoveryActionType  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.provider_operations_service import ProviderOperationsService  # noqa: E402
from ccp_studio.services.provider_recovery_service import (  # noqa: E402
    ProviderRecoveryService,
    register_provider_recovery_command_handlers,
)
from ccp_studio.workflows.provider_job_workflow import ProviderJobWorkflow  # noqa: E402


def _provider_ops() -> ProviderOperationsService:
    service = ProviderOperationsService()
    service.seed_current_cmf_capabilities()
    return service


def _request_kwargs(service: ProviderOperationsService, idempotency_key: str = "provider-job:recovery"):
    capability = service.repository.capabilities["ideogram_4.composition_plate.v1"]
    return {
        "provider_capability_id": capability.provider_capability_id,
        "organization_id": uuid4(),
        "brand_id": uuid4(),
        "requested_by_actor_id": uuid4(),
        "complete_editing_session_id": uuid4(),
        "scene_spec_id": uuid4(),
        "input_artifact_hashes": ["sha256-source", "sha256-render-contract"],
        "input_types": capability.allowed_input_types[:1],
        "prompt_hash": "sha256-prompt",
        "parameters": {"estimated_cost_amount": 1.25, "compiled_prompt": "source-backed scene prompt"},
        "idempotency_key": idempotency_key,
    }


def _failed_job(service: ProviderOperationsService):
    kwargs = _request_kwargs(service)
    job = service.submit_provider_job(**kwargs)
    receipt = service.normalize_provider_response(
        provider_job_id=job.provider_job_id,
        status=ProviderJobStatus.failed,
        output_artifact_hashes=[],
        cost_amount=1.25,
        failure_code="TIMEOUT",
        response_metadata={"retry_count": 0},
        provider_correlation_id=job.provider_correlation_id,
    )
    return kwargs, service.repository.jobs[job.provider_job_id], receipt


def test_timeout_retry_only_requeues_incomplete_work_and_preserves_prior_receipts():
    provider_ops = _provider_ops()
    kwargs, job, failed_receipt = _failed_job(provider_ops)
    recovery = ProviderRecoveryService(provider_ops)
    recovery.record_provider_job_checkpoint(
        provider_job_id=job.provider_job_id,
        work_id="asset-roll-1",
        completed=True,
        output_artifact_uri="object://provider/asset-roll-1.png",
        output_artifact_hash="sha256-asset-roll-1",
        actor_id=kwargs["requested_by_actor_id"],
        provider_receipt_id=failed_receipt.provider_receipt_id,
    )
    recovery.record_provider_job_checkpoint(
        provider_job_id=job.provider_job_id,
        work_id="asset-roll-2",
        completed=False,
        actor_id=kwargs["requested_by_actor_id"],
    )

    receipt = recovery.retry_provider_job(
        provider_job_id=job.provider_job_id,
        actor_id=kwargs["requested_by_actor_id"],
        idempotency_key="recovery:retry:timeout",
        reason="Provider timeout after first asset-roll checkpoint.",
        requeued_work_ids=["asset-roll-2"],
    )
    replay = recovery.retry_provider_job(
        provider_job_id=job.provider_job_id,
        actor_id=kwargs["requested_by_actor_id"],
        idempotency_key="recovery:retry:timeout",
        reason="Provider timeout after first asset-roll checkpoint.",
        requeued_work_ids=["asset-roll-2"],
    )

    updated = provider_ops.repository.jobs[job.provider_job_id]
    assert receipt.decision_code == "PROVIDER_JOB_RETRY_SCHEDULED"
    assert receipt.preserved_output_hashes == ["sha256-asset-roll-1"]
    assert receipt.requeued_work_ids == ["asset-roll-2"]
    assert replay.recovery_receipt_id == receipt.recovery_receipt_id
    assert updated.retry_count == 1
    assert failed_receipt.provider_receipt_id in provider_ops.repository.receipts


def test_partial_output_compensation_preserves_completed_artifacts_and_isolates_missing_work():
    provider_ops = _provider_ops()
    kwargs, job, _failed_receipt = _failed_job(provider_ops)
    recovery = ProviderRecoveryService(provider_ops)
    recovery.record_provider_job_checkpoint(
        provider_job_id=job.provider_job_id,
        work_id="caption-render",
        completed=True,
        output_artifact_uri="object://provider/caption-render.mov",
        output_artifact_hash="sha256-caption-render",
        actor_id=kwargs["requested_by_actor_id"],
    )

    receipt = recovery.compensate_provider_job(
        provider_job_id=job.provider_job_id,
        actor_id=kwargs["requested_by_actor_id"],
        idempotency_key="recovery:compensate:partial",
        reason="Partial output exists but final render failed.",
        missing_work_ids=["final-mix-render"],
    )

    assert receipt.decision_code == "PROVIDER_JOB_COMPENSATION_RECORDED"
    assert receipt.preserved_output_hashes == ["sha256-caption-render"]
    assert receipt.requeued_work_ids == ["final-mix-render"]
    assert receipt.terminal_state == "compensation_pending"
    assert any(event.event_type == "ProviderJobCompensated" for event in provider_ops.repository.domain_events)


def test_cancel_reconciles_provider_and_canonical_state_by_recovery_receipt():
    provider_ops = _provider_ops()
    kwargs = _request_kwargs(provider_ops, "provider-job:cancel")
    job = provider_ops.submit_provider_job(**kwargs)
    recovery = ProviderRecoveryService(provider_ops)

    receipt = recovery.cancel_provider_job(
        provider_job_id=job.provider_job_id,
        actor_id=kwargs["requested_by_actor_id"],
        idempotency_key="recovery:cancel:one",
        reason="Operator cancelled stale provider job.",
    )

    assert provider_ops.repository.jobs[job.provider_job_id].status == ProviderJobStatus.cancelled
    assert receipt.decision_code == "PROVIDER_JOB_CANCELLED_RECONCILED"
    assert receipt.terminal_state == ProviderJobStatus.cancelled.value
    assert {"provider_state_cancelled", "canonical_state_cancelled"} <= set(receipt.evidence_refs)


def test_duplicate_provider_webhook_creates_no_duplicate_completion_event_and_records_incident():
    provider_ops = _provider_ops()
    kwargs = _request_kwargs(provider_ops, "provider-job:webhook")
    job = provider_ops.submit_provider_job(**kwargs)
    recovery = ProviderRecoveryService(provider_ops)
    envelope = ProviderWebhookEnvelope(
        schema_version="cmf.provider_webhook_envelope.v1",
        provider_webhook_id=uuid4(),
        provider_name=job.provider_name,
        provider_correlation_id=job.provider_correlation_id,
        payload={
            "status": "succeeded",
            "output_artifact_hashes": ["sha256-webhook-final"],
            "cost_amount": 1.25,
            "response_metadata": {"retry_count": 0},
        },
        idempotency_key="webhook:duplicate-safe",
        received_at=utc_now(),
    )

    first = recovery.process_provider_webhook_with_recovery_guard(envelope, actor_id=kwargs["requested_by_actor_id"])
    second = recovery.process_provider_webhook_with_recovery_guard(envelope, actor_id=kwargs["requested_by_actor_id"])

    assert second.provider_receipt_id == first.provider_receipt_id
    assert len([event for event in provider_ops.repository.domain_events if event.event_type == "ProviderJobCompleted"]) == 1
    incident = next(iter(recovery.repository.incidents.values()))
    assert incident.incident_type == OperationalIncidentType.duplicate_webhook
    assert incident.duplicate_webhook_count == 1


def test_retry_that_would_duplicate_billing_or_publishing_is_blocked_for_manual_review():
    provider_ops = _provider_ops()
    kwargs = _request_kwargs(provider_ops, "provider-job:duplicate-cost")
    job = provider_ops.submit_provider_job(**kwargs)
    provider_ops.normalize_provider_response(
        provider_job_id=job.provider_job_id,
        status=ProviderJobStatus.succeeded,
        output_artifact_hashes=["sha256-final-output"],
        cost_amount=1.25,
        response_metadata={"retry_count": 0},
        provider_correlation_id=job.provider_correlation_id,
    )
    recovery = ProviderRecoveryService(provider_ops)

    receipt = recovery.retry_provider_job(
        provider_job_id=job.provider_job_id,
        actor_id=kwargs["requested_by_actor_id"],
        idempotency_key="recovery:retry:duplicate-cost",
        reason="Retry requested after final output already completed.",
        requeued_work_ids=[],
        side_effects=["publishing"],
    )

    assert receipt.decision_code == "DUPLICATE_COST_RECOVERY_BLOCKED"
    assert receipt.duplicate_cost_risk is True
    assert receipt.manual_review_required is True
    assert receipt.preserved_output_hashes == ["sha256-final-output"]
    assert provider_ops.repository.jobs[job.provider_job_id].retry_count == 0


def test_provider_job_workflow_stage11_12_recovery_can_pause_and_resume():
    provider_ops = _provider_ops()
    kwargs = _request_kwargs(provider_ops, "provider-job:workflow")
    job = provider_ops.submit_provider_job(**kwargs)
    recovery = ProviderRecoveryService(provider_ops)
    workflow = ProviderJobWorkflow(provider_ops, recovery_service=recovery)

    pause = workflow.stage11_12_recovery(
        provider_job_id=job.provider_job_id,
        action_type=RecoveryActionType.pause,
        actor_id=kwargs["requested_by_actor_id"],
        idempotency_key="recovery:workflow:pause",
        reason="Pause while provider health recovers.",
    )
    resume = workflow.stage11_12_recovery(
        provider_job_id=job.provider_job_id,
        action_type=RecoveryActionType.resume,
        actor_id=kwargs["requested_by_actor_id"],
        idempotency_key="recovery:workflow:resume",
        reason="Provider health recovered.",
    )

    assert pause.decision_code == "PROVIDER_JOB_PAUSED"
    assert resume.decision_code == "PROVIDER_JOB_RESUMED"
    assert provider_ops.repository.jobs[job.provider_job_id].status == ProviderJobStatus.running


def test_provider_recovery_command_bus_emits_recovery_receipt_event():
    provider_ops = _provider_ops()
    kwargs, job, _failed_receipt = _failed_job(provider_ops)
    recovery = ProviderRecoveryService(provider_ops)
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(kwargs["organization_id"], kwargs["brand_id"])
    register_provider_recovery_command_handlers(bus, recovery)
    actor = ActorContext(actor_id=kwargs["requested_by_actor_id"], actor_type=ActorType.human, role_ids=["production_steward"])
    envelope = new_command_envelope(
        command_type="RetryProviderJobCommand",
        organization_id=kwargs["organization_id"],
        brand_id=kwargs["brand_id"],
        actor=actor,
        payload={
            "provider_job_id": str(job.provider_job_id),
            "reason": "Retry only missing work after timeout.",
            "requeued_work_ids": ["asset-roll-2"],
            "recovery_idempotency_key": "recovery:command:retry",
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["decision_code"] == "PROVIDER_JOB_RETRY_SCHEDULED"
    assert result.result_payload["requeued_work_ids"] == ["asset-roll-2"]
    assert bus.event_outbox.events[-1].event_type == "RetryProviderJobCommand.succeeded"
