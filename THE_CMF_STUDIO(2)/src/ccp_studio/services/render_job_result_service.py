from __future__ import annotations

from ccp_studio.contracts.local_render_worker import (
    LocalRenderWorker,
    RenderJob,
    RenderJobLease,
    RenderJobResult,
    RenderJobStatus,
    RenderResultStatus,
    stable_hash,
)
from ccp_studio.repositories.local_render_worker import InMemoryLocalRenderWorkerRepository


class RenderJobResultService:
    def __init__(self, repository: InMemoryLocalRenderWorkerRepository | None = None):
        self.repository = repository or InMemoryLocalRenderWorkerRepository()

    def complete_fake_result(self, *, job: RenderJob, worker: LocalRenderWorker, lease: RenderJobLease) -> RenderJobResult:
        if lease.worker_id != worker.worker_id:
            raise ValueError("Lease worker_id must match completing worker")
        if lease.render_job_id != job.render_job_id:
            raise ValueError("Lease render_job_id must match job")
        digest = stable_hash(f"{job.render_job_id}:{worker.worker_id}:{lease.render_job_lease_id}:{job.job_type.value}")
        result = RenderJobResult(
            render_job_id=job.render_job_id,
            worker_id=worker.worker_id,
            lease_id=lease.render_job_lease_id,
            result_status=RenderResultStatus.SUCCEEDED,
            output_uri=f"fake://local-render-worker/{job.job_type.value}/{digest}.json",
            output_sha256=digest,
            fake_result=True,
        )
        job.status = RenderJobStatus.COMPLETED
        lease.active = False
        worker.current_job_ids = [jid for jid in worker.current_job_ids if jid != job.render_job_id]
        self.repository.upsert("results", result.render_job_result_id, result)
        self.repository.upsert("jobs", job.render_job_id, job)
        self.repository.upsert("leases", lease.render_job_lease_id, lease)
        self.repository.upsert("workers", worker.worker_id, worker)
        return result

    def fail_result(self, *, job: RenderJob, worker: LocalRenderWorker, lease: RenderJobLease, error_message: str) -> RenderJobResult:
        if lease.worker_id != worker.worker_id:
            raise ValueError("Lease worker_id must match completing worker")
        result = RenderJobResult(
            render_job_id=job.render_job_id,
            worker_id=worker.worker_id,
            lease_id=lease.render_job_lease_id,
            result_status=RenderResultStatus.FAILED,
            error_message=error_message,
            fake_result=True,
        )
        job.status = RenderJobStatus.FAILED
        lease.active = False
        worker.current_job_ids = [jid for jid in worker.current_job_ids if jid != job.render_job_id]
        self.repository.upsert("results", result.render_job_result_id, result)
        return result
