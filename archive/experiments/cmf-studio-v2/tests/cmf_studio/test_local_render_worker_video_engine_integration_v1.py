from ccp_studio.contracts.local_render_worker import RenderJobType
from ccp_studio.contracts.video_editing_engine import ProxyRenderContract
from ccp_studio.services.local_render_worker_service import LocalRenderWorkerService
from ccp_studio.services.render_job_lease_service import RenderJobLeaseService
from ccp_studio.services.render_job_queue_service import RenderJobQueueService
from ccp_studio.services.render_job_result_service import RenderJobResultService


def test_proxy_render_contract_can_queue_lease_and_complete_fake_worker_result():
    proxy_contract = ProxyRenderContract(
        timeline_program_id="timeline_format02_001",
        remotion_input_props_id="remotion_props_format02_001",
    )

    queue_service = RenderJobQueueService()
    job = queue_service.create_job(
        job_type=RenderJobType.PROXY_VIDEO_RENDER,
        job_name="Format 02 proxy render",
        payload={
            "proxy_render_contract_id": proxy_contract.proxy_render_contract_id,
            "timeline_program_id": proxy_contract.timeline_program_id,
            "remotion_input_props_id": proxy_contract.remotion_input_props_id,
        },
    )
    queue = queue_service.enqueue(queue_service.create_queue(), job)
    worker = LocalRenderWorkerService().register_worker(
        worker_id="worker_proxy_demo",
        machine_id="machine_proxy_demo",
        display_name="Proxy Demo Worker",
    )

    lease = RenderJobLeaseService().lease_job(job=queue.queued_jobs[0], worker=worker)
    result = RenderJobResultService().complete_fake_result(job=job, worker=worker, lease=lease)

    assert result.output_uri.startswith("fake://local-render-worker/proxy_video_render/")
    assert result.output_sha256
    assert result.provider_calls_executed is False
    assert result.external_runtime_calls_executed is False
