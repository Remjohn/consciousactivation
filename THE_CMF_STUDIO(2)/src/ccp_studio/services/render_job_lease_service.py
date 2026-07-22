from __future__ import annotations

from datetime import datetime, timezone, timedelta

from ccp_studio.contracts.local_render_worker import (
    LocalRenderWorker,
    RenderJob,
    RenderJobLease,
    RenderJobStatus,
)
from ccp_studio.repositories.local_render_worker import InMemoryLocalRenderWorkerRepository


class RenderJobLeaseService:
    def __init__(self, repository: InMemoryLocalRenderWorkerRepository | None = None):
        self.repository = repository or InMemoryLocalRenderWorkerRepository()

    def lease_job(self, *, job: RenderJob, worker: LocalRenderWorker, lease_seconds: int = 300) -> RenderJobLease:
        if not worker.healthy_for_leasing:
            raise ValueError("Cannot lease job to offline/unhealthy/busy worker")
        if not worker.supports_job_type(job.job_type):
            raise ValueError("Worker does not support job type")
        missing = [cap_id for cap_id in job.required_capability_ids if cap_id not in [cap.capability_id for cap in worker.capabilities if cap.available]]
        if missing:
            raise ValueError(f"Worker missing required capabilities: {missing}")
        now = datetime.now(timezone.utc)
        lease = RenderJobLease(
            render_job_id=job.render_job_id,
            worker_id=worker.worker_id,
            leased_at=now.isoformat(),
            expires_at=(now + timedelta(seconds=lease_seconds)).isoformat(),
        )
        job.status = RenderJobStatus.LEASED
        worker.current_job_ids.append(job.render_job_id)
        self.repository.upsert("leases", lease.render_job_lease_id, lease)
        self.repository.upsert("jobs", job.render_job_id, job)
        self.repository.upsert("workers", worker.worker_id, worker)
        return lease
