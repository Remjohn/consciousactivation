from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.approval_gate import (  # noqa: E402
    ApprovalBlockerSeverity,
    ApprovalGateBlocker,
    ApprovalGateDecision,
    ApprovalPolicyReport,
    ContentFormatValidation,
    new_approval_blocker_receipt,
)
from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.comfy_gpu_worker import CloudProvider, GpuCostReport, GpuTier, GpuWorkerJob, GpuWorkerStatus  # noqa: E402
from ccp_studio.contracts.operations_board import BlockerSummary  # noqa: E402
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.provider_jobs import ProviderJob, ProviderJobStatus, ProviderReceipt  # noqa: E402
from ccp_studio.contracts.provider_recovery import (  # noqa: E402
    OperationalIncident,
    OperationalIncidentType,
    ProviderJobCheckpoint,
    ProviderRecoveryAction,
    RecoveryActionStatus,
    RecoveryActionType,
    new_recovery_receipt,
)
from ccp_studio.repositories.approval_gate import InMemoryApprovalGateRepository  # noqa: E402
from ccp_studio.repositories.comfy_gpu_worker import InMemoryComfyGpuWorkerRepository  # noqa: E402
from ccp_studio.repositories.provider_jobs import InMemoryProviderOperationsRepository  # noqa: E402
from ccp_studio.repositories.provider_recovery import InMemoryProviderRecoveryRepository  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.operations_board_service import OperationsBoardService, register_operations_board_command_handlers  # noqa: E402
from ccp_studio.services.projection_service import ProjectionService  # noqa: E402
from ccp_studio.workflows.operations import OperationsWorkflow  # noqa: E402


def _provider_fixture(org_id, brand_id, actor_id):
    repo = InMemoryProviderOperationsRepository()
    request_id = uuid4()
    job = ProviderJob(
        schema_version="cmf.provider_job.v1",
        provider_job_id=uuid4(),
        provider_request_id=request_id,
        provider_capability_id="flux2.klein9b.image",
        provider_name="self_hosted_comfyui",
        capability_name="image_render",
        model_or_workflow_version="flux2-klein-9b",
        status=ProviderJobStatus.failed,
        provider_correlation_id="provider:job:001",
        retry_count=1,
        cost_policy_id="gpu-guardrail",
        retry_policy_id="safe-retry",
        evaluation_requirement_ids=["render_quality"],
        request_hash="sha256-request",
        submitted_at=utc_now(),
        updated_at=utc_now(),
    )
    receipt = ProviderReceipt(
        schema_version="cmf.provider_receipt.v2",
        provider_receipt_id=uuid4(),
        provider_job_id=job.provider_job_id,
        provider_request_id=request_id,
        provider_capability_id=job.provider_capability_id,
        provider_name=job.provider_name,
        capability_name=job.capability_name,
        model_or_workflow_version=job.model_or_workflow_version,
        status=ProviderJobStatus.failed,
        output_artifact_hashes=["sha256-partial-render"],
        cost_amount=4.25,
        retry_count=1,
        failure_code="GPU_WORKER_TIMEOUT",
        request_hash=job.request_hash,
        response_hash="sha256-response",
        provider_correlation_id="provider:job:001",
        created_domain_event_type="ProviderJobFailed",
        created_at=utc_now(),
    )
    repo.put_job(job)
    repo.put_receipt(receipt)
    return repo, job, receipt


def _gpu_fixture(provider_job_id, org_id, brand_id, actor_id):
    repo = InMemoryComfyGpuWorkerRepository()
    job = GpuWorkerJob(
        schema_version="cmf.gpu_worker_job.v1",
        gpu_worker_job_id=uuid4(),
        provider_job_id=provider_job_id,
        organization_id=org_id,
        brand_id=brand_id,
        actor_id=actor_id,
        cloud_provider=CloudProvider.aws,
        gpu_tier=GpuTier.vram_24gb,
        docker_image_digest="sha256:comfyui-worker",
        workflow_asset_id=uuid4(),
        workflow_hash="sha256-workflow",
        input_artifact_hashes=["sha256-input"],
        typed_parameters={"steps": 28},
        queue_position=1,
        expected_output_count=1,
        status=GpuWorkerStatus.draining,
        queued_at=utc_now(),
        updated_at=utc_now(),
    )
    cost = GpuCostReport(
        schema_version="cmf.gpu_cost_report.v1",
        gpu_cost_report_id=uuid4(),
        gpu_worker_job_id=job.gpu_worker_job_id,
        cloud_provider=CloudProvider.aws,
        gpu_tier=GpuTier.vram_24gb,
        instance_seconds=3600,
        cost_amount=9.5,
        queue_depth_at_start=3,
        shutdown_at=utc_now(),
    )
    repo.put_job(job)
    repo.put_cost_report(cost)
    return repo, job, cost


def _recovery_fixture(provider_job_id, actor_id):
    repo = InMemoryProviderRecoveryRepository()
    checkpoint = ProviderJobCheckpoint(
        schema_version="cmf.provider_job_checkpoint.v1",
        provider_job_checkpoint_id=uuid4(),
        provider_job_id=provider_job_id,
        work_id="render-step-18",
        output_artifact_uri="object://partial/render.png",
        output_artifact_hash="sha256-partial-render",
        completed=True,
        cost_amount=3.5,
        provider_receipt_id=uuid4(),
        recorded_at=utc_now(),
    )
    incident = OperationalIncident(
        schema_version="cmf.operational_incident.v1",
        operational_incident_id=uuid4(),
        provider_job_id=provider_job_id,
        incident_type=OperationalIncidentType.provider_timeout,
        severity="high",
        summary="ComfyUI worker timed out after partial artifact upload.",
        resolved=True,
        evidence_refs=["provider_receipt:timeout"],
        recorded_at=utc_now(),
    )
    action = ProviderRecoveryAction(
        schema_version="cmf.provider_recovery_action.v1",
        provider_recovery_action_id=uuid4(),
        provider_job_id=provider_job_id,
        action_type=RecoveryActionType.retry,
        status=RecoveryActionStatus.applied,
        idempotency_key="recovery:retry:001",
        reason="Retry from completed checkpoint.",
        duplicate_cost_risk=False,
        manual_review_required=False,
        preserved_output_hashes=["sha256-partial-render"],
        requeued_work_ids=["render-step-19"],
        created_at=utc_now(),
    )
    receipt = new_recovery_receipt(
        provider_job_id=provider_job_id,
        action=action,
        decision_code="RECOVERY_RETRY_APPLIED",
        actor_id=actor_id,
        evidence_refs=["provider_job_checkpoint:render-step-18"],
    )
    repo.put_checkpoint(checkpoint)
    repo.put_incident(incident)
    repo.put_action(action)
    repo.put_receipt(receipt)
    return repo, incident, receipt


def _approval_fixture(org_id, brand_id):
    repo = InMemoryApprovalGateRepository()
    blocker = ApprovalGateBlocker(
        blocker_id=uuid4(),
        code="CONSENT_RECORD_REQUIRED",
        severity=ApprovalBlockerSeverity.hard,
        source_object_ref="render_output:blocked",
        evidence_refs=["consent:missing"],
        message="Consent record is required before approval.",
        repair_hint="record_consent",
    )
    validation = ContentFormatValidation(
        schema_version="cmf.content_format_validation.v1",
        platform_variant_id="instagram-reel",
        format_key="guest_asset_pack.clip.reel",
        valid_content_format=True,
        registry_version_id="formats:v1",
    )
    report = ApprovalPolicyReport(
        schema_version="cmf.approval_policy_report.v1",
        approval_policy_report_id=uuid4(),
        approval_request_id=uuid4(),
        organization_id=org_id,
        brand_id=brand_id,
        object_type="render_output",
        object_id=uuid4(),
        object_version_hash="sha256-render",
        lineage_complete=True,
        consent_compatible=False,
        source_truth_passed=True,
        identity_passed=True,
        evaluation_passed=True,
        platform_format_passed=True,
        content_format_passed=True,
        content_format_validation=validation,
        blockers=[blocker],
        decision=ApprovalGateDecision.blocked,
        policy_version="approval-policy:v1",
        created_at=utc_now(),
    )
    repo.put_report(report)
    repo.put_receipt(new_approval_blocker_receipt(report=report))
    return repo


def _service_fixture():
    org_id = uuid4()
    brand_id = uuid4()
    actor_id = uuid4()
    provider_repo, provider_job, provider_receipt = _provider_fixture(org_id, brand_id, actor_id)
    gpu_repo, gpu_job, gpu_cost = _gpu_fixture(provider_job.provider_job_id, org_id, brand_id, actor_id)
    recovery_repo, incident, recovery_receipt = _recovery_fixture(provider_job.provider_job_id, actor_id)
    approval_repo = _approval_fixture(org_id, brand_id)
    projection_service = ProjectionService()
    projection_service.mark_projection_unhealthy(reason="Projection count conflict.", conflict_count=1)
    service = OperationsBoardService(
        provider_repository=provider_repo,
        gpu_worker_repository=gpu_repo,
        recovery_repository=recovery_repo,
        approval_gate_repository=approval_repo,
        projection_repository=projection_service.repository,
    )
    return service, org_id, brand_id, actor_id, provider_job, provider_receipt, gpu_job, gpu_cost, incident, recovery_receipt


def test_operations_board_shows_queues_workers_gpu_provider_checkpoints_retries_costs_and_blockers():
    service, org_id, brand_id, *_ = _service_fixture()

    state = service.build_operations_board_state(organization_id=org_id, brand_id=brand_id)

    assert any(queue.queue_name == "provider_jobs" and queue.failed_count == 1 for queue in state.queues)
    assert any(worker.status == "draining" and worker.gpu_tier == "24gb_vram" for worker in state.workers)
    assert state.provider_statuses[0].status == "outage"
    assert state.workflow_checkpoint_refs
    assert state.cost_snapshot.total_cost_usd >= 13.75
    assert any(blocker.blocker_type == "approval" for blocker in state.blockers)
    assert any(blocker.blocker_type == "projection" for blocker in state.blockers)
    assert state.recovery_recommendations


def test_provider_outage_view_shows_affected_jobs_artifacts_safe_retries_cost_blockers_and_action():
    service, org_id, brand_id, _actor_id, provider_job, _receipt, *_ = _service_fixture()

    state = service.build_operations_board_state(organization_id=org_id, brand_id=brand_id)
    provider = state.provider_statuses[0]

    assert provider.status == "outage"
    assert str(provider_job.provider_job_id) in provider.affected_job_ids
    assert "sha256-partial-render" in provider.completed_artifact_hashes
    assert provider.safe_retry_available is True
    assert provider.cost_estimate_usd == 4.25
    assert "GPU_WORKER_TIMEOUT" in provider.blocker_codes
    assert provider.recommended_action == "RetryProviderJobCommand"


def test_consent_or_approval_blocker_links_to_exact_object_and_decision():
    service, org_id, brand_id, *_ = _service_fixture()
    service.link_blocker_to_object(
        blocker_type="consent",
        blocker_code="CONSENT_REVOKED",
        object_ref="render_output:123",
        receipt_id="consent-receipt:123",
        required_action="record_new_consent_or_quarantine",
        allowed_command_type="RecordConsentCommand",
    )

    state = service.build_operations_board_state(organization_id=org_id, brand_id=brand_id)

    consent_blocker = next(blocker for blocker in state.blockers if blocker.blocker_type == "consent")
    assert consent_blocker.object_ref == "render_output:123"
    assert consent_blocker.receipt_id == "consent-receipt:123"
    assert consent_blocker.allowed_command_type == "RecordConsentCommand"


def test_draining_worker_shows_shutdown_status_and_final_cost():
    service, org_id, brand_id, *_rest = _service_fixture()

    state = service.build_operations_board_state(organization_id=org_id, brand_id=brand_id)
    worker = state.workers[0]

    assert worker.status == "draining"
    assert worker.shutdown_status == "draining_until_queue_empty"
    assert worker.current_cost_estimate_usd == 9.5


def test_resolved_incident_history_and_receipts_remain_visible():
    service, org_id, brand_id, _actor_id, _job, _provider_receipt, _gpu_job, _cost, incident, recovery_receipt = _service_fixture()

    state = service.build_operations_board_state(organization_id=org_id, brand_id=brand_id, include_resolved=True)
    summary = state.incidents[0]

    assert summary.incident_id == str(incident.operational_incident_id)
    assert summary.resolved is True
    assert str(recovery_receipt.recovery_receipt_id) in summary.receipt_ids


def test_operations_board_actions_route_to_commands_not_manual_database_edits():
    service, *_ = _service_fixture()

    decision = service.operations_action_boundary(
        requested_action="repair_provider_job",
        allowed_command_type="RetryProviderJobCommand",
        manual_database_edit_requested=True,
    )

    assert decision.manual_database_edit_allowed is False
    assert decision.allowed_command_type == "RetryProviderJobCommand"


def test_operations_workflow_and_command_bus_build_board_with_receipt():
    service, org_id, brand_id, actor_id, *_ = _service_fixture()
    workflow = OperationsWorkflow(service)
    state = workflow.overlay_board_state(organization_id=org_id, brand_id=brand_id)
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_operations_board_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["operator"])
    envelope = new_command_envelope(
        command_type="BuildOperationsBoardStateCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        idempotency_key="operations:board:one",
        payload={"include_resolved": True},
    )

    first = bus.submit(envelope)
    second = bus.submit(envelope)

    assert state.board_state_id in service.repository.board_states
    assert first.status == CommandStatus.succeeded
    assert second.status == CommandStatus.replayed
    assert first.result_payload["board_state_id"] == second.result_payload["board_state_id"]
    assert service.repository.receipts
    assert any(event.event_type == "OperationsBoardStateBuilt" for event in service.repository.events)
