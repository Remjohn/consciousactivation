from __future__ import annotations

from ccp_studio.contracts.local_render_worker import LocalRenderWorker, RenderJobHeartbeat, WorkerStatus
from ccp_studio.repositories.local_render_worker import InMemoryLocalRenderWorkerRepository


class RenderJobHeartbeatService:
    def __init__(self, repository: InMemoryLocalRenderWorkerRepository | None = None):
        self.repository = repository or InMemoryLocalRenderWorkerRepository()

    def record_heartbeat(
        self,
        *,
        worker: LocalRenderWorker,
        status: WorkerStatus | None = None,
        active_job_ids: list[str] | None = None,
        free_disk_mb: int | None = None,
        free_memory_mb: int | None = None,
    ) -> RenderJobHeartbeat:
        heartbeat = RenderJobHeartbeat(
            worker_id=worker.worker_id,
            status=status or worker.status,
            active_job_ids=active_job_ids if active_job_ids is not None else list(worker.current_job_ids),
            observed_capability_ids=[cap.capability_id for cap in worker.capabilities if cap.available],
            free_disk_mb=free_disk_mb,
            free_memory_mb=free_memory_mb,
        )
        worker.status = heartbeat.status
        worker.current_job_ids = list(heartbeat.active_job_ids)
        worker.last_heartbeat_at = heartbeat.created_at
        self.repository.upsert("heartbeats", heartbeat.render_job_heartbeat_id, heartbeat)
        self.repository.upsert("workers", worker.worker_id, worker)
        return heartbeat
