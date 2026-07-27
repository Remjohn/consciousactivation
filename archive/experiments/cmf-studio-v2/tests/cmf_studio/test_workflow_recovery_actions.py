from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.workflow_recovery import WorkflowRecoveryActionType, WorkflowRecoveryStatus  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.operations_board_service import OperationsBoardService  # noqa: E402
from ccp_studio.services.workflow_recovery_service import (  # noqa: E402
    WorkflowRecoveryService,
    register_workflow_recovery_command_handlers,
)
from ccp_studio.workflows.operations import OperationsWorkflow  # noqa: E402


def _service() -> WorkflowRecoveryService:
    return WorkflowRecoveryService()


def _report(service: WorkflowRecoveryService, **overrides):
    payload = {
        "workflow_id": "workflow-1",
        "failed_object_ref": "provider_job:job-001",
        "completed_artifact_refs": ["artifact:render:001"],
        "receipt_refs": ["provider_receipt:001"],
        "consent_compatible": True,
        "summary": "Workflow failed after a completed render artifact.",
    }
    payload.update(overrides)
    return service.build_recovery_validation_report(**payload)


def _incident_id(service: WorkflowRecoveryService):
    return next(iter(service.repository.incidents))


def test_validation_report_derives_safe_actions_from_state_completed_artifacts_receipts_and_consent():
    service = _service()

    report = _report(service)

    assert {
        WorkflowRecoveryActionType.retry,
        WorkflowRecoveryActionType.resume,
        WorkflowRecoveryActionType.cancel,
        WorkflowRecoveryActionType.compensate,
        WorkflowRecoveryActionType.quarantine,
    } <= set(report.safe_actions)
    assert report.completed_artifact_refs == ["artifact:render:001"]
    assert report.receipt_refs == ["provider_receipt:001"]
    assert report.duplicate_side_effect_risks == []
    assert any(event.event_type == "RecoveryValidationReportBuilt" for event in service.repository.events)


def test_safe_retry_preserves_completed_artifacts_and_requeues_incomplete_work_only():
    service = _service()
    _report(service)
    actor_id = uuid4()

    receipt = service.retry_workflow(
        incident_id=_incident_id(service),
        requested_by_user_id=actor_id,
        role_ids=["operator"],
        reason="Retry only incomplete work after preserving completed artifact.",
        idempotency_key="workflow:retry:one",
    )

    assert receipt.status == WorkflowRecoveryStatus.applied
    assert receipt.decision_code == "WORKFLOW_RETRY_APPLIED"
    assert receipt.preserved_artifact_refs == ["artifact:render:001"]
    assert receipt.requeued_work_refs == ["workflow-1:incomplete_work"]
    assert receipt.quarantined_refs == []


def test_cancel_records_terminal_state_with_receipt():
    service = _service()
    _report(service)
    actor_id = uuid4()

    receipt = service.cancel_workflow(
        incident_id=_incident_id(service),
        requested_by_user_id=actor_id,
        role_ids=["operator"],
        reason="Cancel stale workflow before more provider jobs are queued.",
        idempotency_key="workflow:cancel:one",
    )

    assert receipt.status == WorkflowRecoveryStatus.applied
    assert receipt.terminal_state == "cancelled"
    assert receipt.receipt_id in service.repository.receipts
    assert service.repository.incidents[receipt.incident_id].resolved is True


def test_quarantine_blocks_affected_assets_memory_provider_jobs_or_publishing_intents():
    service = _service()
    _report(
        service,
        failed_object_ref="provider_job:job-001",
        completed_artifact_refs=[
            "asset:render:001",
            "memory:guest_claim:001",
            "publishing_intent:publer:001",
        ],
    )
    actor_id = uuid4()

    receipt = service.quarantine_workflow_artifacts(
        incident_id=_incident_id(service),
        requested_by_user_id=actor_id,
        role_ids=["production_steward"],
        reason="Quarantine affected outputs until the incident is reviewed.",
        idempotency_key="workflow:quarantine:one",
    )

    assert receipt.terminal_state == "quarantined"
    assert set(receipt.quarantined_refs) == {
        "provider_job:job-001",
        "asset:render:001",
        "memory:guest_claim:001",
        "publishing_intent:publer:001",
    }
    assert set(receipt.quarantined_refs) <= service.repository.quarantined_refs


def test_duplicate_or_corrupting_action_is_blocked_by_validation_report():
    service = _service()
    _report(
        service,
        publishing_side_effect_risk=True,
        memory_side_effect_risk=True,
        provider_cost_risk=True,
    )
    actor_id = uuid4()

    receipt = service.retry_workflow(
        incident_id=_incident_id(service),
        requested_by_user_id=actor_id,
        role_ids=["operator"],
        reason="Unsafe retry requested after side effects were detected.",
        idempotency_key="workflow:retry:blocked",
    )

    assert receipt.status == WorkflowRecoveryStatus.blocked
    assert receipt.recovery_action_id is None
    assert receipt.decision_code == "RECOVERY_ACTION_BLOCKED"
    assert "retry" in receipt.blocked_actions
    assert set(receipt.duplicate_side_effect_risks) == {
        "public_schedule_side_effect",
        "memory_side_effect",
        "provider_billing_side_effect",
    }


def test_idempotency_replays_same_recovery_receipt_without_duplicate_action():
    service = _service()
    _report(service)
    actor_id = uuid4()
    kwargs = {
        "incident_id": _incident_id(service),
        "requested_by_user_id": actor_id,
        "role_ids": ["operator"],
        "reason": "Retry only once for the same operator request.",
        "idempotency_key": "workflow:retry:idempotent",
    }

    first = service.retry_workflow(**kwargs)
    second = service.retry_workflow(**kwargs)

    assert second.receipt_id == first.receipt_id
    assert len(service.repository.receipts) == 1
    assert len(service.repository.actions) == 1


def test_operations_workflow_and_command_bus_route_recovery_actions():
    service = _service()
    workflow = OperationsWorkflow(OperationsBoardService(), workflow_recovery_service=service)
    report = _report(service)
    incident_id = _incident_id(service)
    actor_id = uuid4()

    workflow_receipt = workflow.recover_failed_workflow(
        action_type=WorkflowRecoveryActionType.cancel,
        incident_id=incident_id,
        requested_by_user_id=actor_id,
        role_ids=["operator"],
        reason="Cancel through operations workflow.",
        idempotency_key="workflow:operations:cancel",
    )
    bus = create_in_memory_command_bus()
    org_id = uuid4()
    brand_id = uuid4()
    bus.brands.add_scope(org_id, brand_id)
    register_workflow_recovery_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["operator"])
    build = new_command_envelope(
        command_type="BuildRecoveryValidationReportCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        idempotency_key="workflow:validation:command",
        payload={
            "workflow_id": "workflow-command",
            "failed_object_ref": "asset:failed:command",
            "completed_artifact_refs": [],
            "receipt_refs": [f"recovery_receipt:{workflow_receipt.receipt_id}"],
            "consent_compatible": True,
        },
    )
    build_result = bus.submit(build)
    retry_incident_id = next(
        incident.incident_id
        for incident in service.repository.incidents.values()
        if incident.workflow_id == "workflow-command"
    )
    retry = new_command_envelope(
        command_type="RetryWorkflowCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        idempotency_key="workflow:retry:command",
        payload={
            "incident_id": str(retry_incident_id),
            "reason": "Retry missing command-routed work.",
        },
    )

    first = bus.submit(retry)
    second = bus.submit(retry)

    assert report.report_id in service.repository.validation_reports
    assert workflow_receipt.terminal_state == "cancelled"
    assert build_result.status == CommandStatus.succeeded
    assert first.status == CommandStatus.succeeded
    assert second.status == CommandStatus.replayed
    assert first.result_payload["decision_code"] == "WORKFLOW_RETRY_APPLIED"
    assert bus.event_outbox.events[-1].event_type == "RetryWorkflowCommand.succeeded"
