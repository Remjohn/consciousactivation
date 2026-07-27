import pytest

from ccp_studio.contracts.local_render_worker import (
    CapabilityStatus,
    HealthStatus,
    LocalRenderWorker,
    LocalRenderWorkerCapability,
    LocalRuntimeName,
    RenderJob,
    RenderJobHeartbeat,
    RenderJobResult,
    RenderJobStatus,
    RenderJobType,
    RenderResultStatus,
    WorkerStatus,
)
from ccp_studio.services.local_render_worker_orchestrator_service import LocalRenderWorkerOrchestratorService
from ccp_studio.services.local_render_worker_service import LocalRenderWorkerService
from ccp_studio.services.render_job_queue_service import RenderJobQueueService
from ccp_studio.services.render_job_lease_service import RenderJobLeaseService
from ccp_studio.services.render_job_result_service import RenderJobResultService
from ccp_studio.services.render_worker_health_service import RenderWorkerHealthService


def test_worker_registration_requires_worker_and_machine_id():
    with pytest.raises(Exception):
        LocalRenderWorker(worker_id="", machine_id="machine", display_name="Worker")
    with pytest.raises(Exception):
        LocalRenderWorker(worker_id="worker", machine_id="", display_name="Worker")


def test_capability_available_requires_enabled_and_tested():
    with pytest.raises(Exception):
        LocalRenderWorkerCapability(
            capability_id="runtime:render:remotion",
            display_name="Remotion",
            runtime_name=LocalRuntimeName.REMOTION,
            enabled=True,
            tested=False,
            status=CapabilityStatus.AVAILABLE,
        )


def test_fake_python_capability_supports_all_job_types():
    capability = LocalRenderWorkerService().compile_fake_python_capability()
    assert capability.available
    assert set(capability.supports_job_types) == set(RenderJobType)


def test_render_job_blocks_provider_calls_and_external_runtime_calls():
    with pytest.raises(Exception):
        RenderJob(
            job_type=RenderJobType.PROXY_VIDEO_RENDER,
            job_name="Proxy",
            provider_calls_allowed=True,
        )
    with pytest.raises(Exception):
        RenderJob(
            job_type=RenderJobType.PROXY_VIDEO_RENDER,
            job_name="Proxy",
            external_runtime_calls_allowed=True,
        )


def test_final_video_render_requires_final_timeline_locked():
    with pytest.raises(Exception):
        RenderJob(
            job_type=RenderJobType.FINAL_VIDEO_RENDER,
            job_name="Final",
            payload={"final_timeline_locked": False},
        )


def test_final_video_render_job_compiles_when_timeline_locked():
    job = RenderJob(
        job_type=RenderJobType.FINAL_VIDEO_RENDER,
        job_name="Final",
        payload={"final_timeline_locked": True},
    )
    assert job.job_type == RenderJobType.FINAL_VIDEO_RENDER


def test_queue_enqueue_sets_queued_status():
    service = RenderJobQueueService()
    queue = service.create_queue()
    job = service.create_job(job_type=RenderJobType.TEMPLATE_PREVIEW_RENDER, job_name="Template preview")
    queue = service.enqueue(queue, job)
    assert queue.jobs[0].status == RenderJobStatus.QUEUED
    assert service.next_queued_job(queue).render_job_id == job.render_job_id


def test_lease_requires_healthy_worker():
    job_service = RenderJobQueueService()
    job = job_service.create_job(job_type=RenderJobType.TEMPLATE_PREVIEW_RENDER, job_name="Template preview")
    worker = LocalRenderWorkerService().register_worker(worker_id="worker_1", machine_id="machine_1", display_name="Worker")
    worker.status = WorkerStatus.OFFLINE
    with pytest.raises(Exception):
        RenderJobLeaseService().lease_job(job=job, worker=worker)


def test_lease_requires_worker_supports_job_type():
    job = RenderJobQueueService().create_job(job_type=RenderJobType.PROXY_VIDEO_RENDER, job_name="Proxy")
    capability = LocalRenderWorkerCapability(
        capability_id="runtime:python_fake",
        display_name="Fake",
        runtime_name=LocalRuntimeName.PYTHON_FAKE,
        enabled=True,
        tested=True,
        status=CapabilityStatus.AVAILABLE,
        supports_job_types=[RenderJobType.TEMPLATE_PREVIEW_RENDER],
    )
    worker = LocalRenderWorkerService().register_worker(worker_id="worker_1", machine_id="machine_1", display_name="Worker", capabilities=[capability])
    with pytest.raises(Exception):
        RenderJobLeaseService().lease_job(job=job, worker=worker)


def test_lease_job_to_worker_sets_status_and_current_job():
    job = RenderJobQueueService().create_job(job_type=RenderJobType.PROXY_VIDEO_RENDER, job_name="Proxy")
    worker = LocalRenderWorkerService().register_worker(worker_id="worker_1", machine_id="machine_1", display_name="Worker")
    lease = RenderJobLeaseService().lease_job(job=job, worker=worker)
    assert lease.worker_id == worker.worker_id
    assert job.status == RenderJobStatus.LEASED
    assert job.render_job_id in worker.current_job_ids


def test_heartbeat_rejects_offline_active_jobs():
    with pytest.raises(Exception):
        RenderJobHeartbeat(
            worker_id="worker_1",
            status=WorkerStatus.OFFLINE,
            active_job_ids=["job_1"],
        )


def test_fake_result_requires_matching_lease_worker():
    job = RenderJobQueueService().create_job(job_type=RenderJobType.THUMBNAIL_RENDER, job_name="Thumb")
    worker = LocalRenderWorkerService().register_worker(worker_id="worker_1", machine_id="machine_1", display_name="Worker")
    lease = RenderJobLeaseService().lease_job(job=job, worker=worker)
    other = LocalRenderWorkerService().register_worker(worker_id="worker_2", machine_id="machine_2", display_name="Worker 2")
    with pytest.raises(Exception):
        RenderJobResultService().complete_fake_result(job=job, worker=other, lease=lease)


def test_fake_result_completes_job_and_emits_hash():
    job = RenderJobQueueService().create_job(job_type=RenderJobType.CAROUSEL_PREVIEW_RENDER, job_name="Carousel preview")
    worker = LocalRenderWorkerService().register_worker(worker_id="worker_1", machine_id="machine_1", display_name="Worker")
    lease = RenderJobLeaseService().lease_job(job=job, worker=worker)
    result = RenderJobResultService().complete_fake_result(job=job, worker=worker, lease=lease)
    assert result.result_status == RenderResultStatus.SUCCEEDED
    assert result.output_sha256
    assert result.output_uri.startswith("fake://")
    assert not result.provider_calls_executed
    assert not result.external_runtime_calls_executed
    assert job.status == RenderJobStatus.COMPLETED


def test_render_job_result_blocks_external_runtime_execution_flag():
    with pytest.raises(Exception):
        RenderJobResult(
            render_job_id="job_1",
            worker_id="worker_1",
            lease_id="lease_1",
            result_status=RenderResultStatus.SUCCEEDED,
            output_uri="fake://out",
            output_sha256="hash",
            external_runtime_calls_executed=True,
        )


def test_worker_health_fails_missing_required_capability():
    worker = LocalRenderWorkerService().register_worker(worker_id="worker_1", machine_id="machine_1", display_name="Worker")
    receipt = RenderWorkerHealthService().evaluate_health(worker=worker, required_capability_ids=["runtime:render:remotion"])
    assert receipt.health_status == HealthStatus.FAIL
    assert "runtime:render:remotion" in receipt.missing_capability_ids


def test_worker_health_fails_offline_worker():
    worker = LocalRenderWorkerService().register_worker(worker_id="worker_1", machine_id="machine_1", display_name="Worker")
    worker.status = WorkerStatus.OFFLINE
    receipt = RenderWorkerHealthService().evaluate_health(worker=worker)
    assert receipt.health_status == HealthStatus.FAIL
    assert "worker_offline_or_unhealthy" in receipt.blockers


def test_orchestrator_full_fake_worker_path():
    orchestrator = LocalRenderWorkerOrchestratorService()
    worker = orchestrator.workers.register_worker(worker_id="worker_1", machine_id="machine_1", display_name="Local Worker")
    orchestrator.heartbeats.record_heartbeat(worker=worker, status=WorkerStatus.ONLINE, active_job_ids=[])
    queue = orchestrator.queue.create_queue()
    job = orchestrator.queue.create_job(job_type=RenderJobType.SUPERVISUAL_PREVIEW_RENDER, job_name="SuperVisual preview")
    queue = orchestrator.queue.enqueue(queue, job)
    lease = orchestrator.leases.lease_job(job=job, worker=worker)
    result = orchestrator.results.complete_fake_result(job=job, worker=worker, lease=lease)
    assert result.output_sha256
    assert job.status == RenderJobStatus.COMPLETED
    assert not worker.current_job_ids


def test_all_supported_job_types_can_be_created():
    service = RenderJobQueueService()
    for job_type in RenderJobType:
        payload = {"final_timeline_locked": True} if job_type == RenderJobType.FINAL_VIDEO_RENDER else {}
        job = service.create_job(job_type=job_type, job_name=job_type.value, payload=payload)
        assert job.job_type == job_type
        assert job.fake_execution_only
