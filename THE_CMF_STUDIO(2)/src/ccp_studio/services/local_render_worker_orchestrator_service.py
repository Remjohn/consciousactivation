from __future__ import annotations

from ccp_studio.repositories.local_render_worker import InMemoryLocalRenderWorkerRepository
from ccp_studio.services.local_render_worker_service import LocalRenderWorkerService
from ccp_studio.services.render_job_queue_service import RenderJobQueueService
from ccp_studio.services.render_job_lease_service import RenderJobLeaseService
from ccp_studio.services.render_job_heartbeat_service import RenderJobHeartbeatService
from ccp_studio.services.render_job_result_service import RenderJobResultService
from ccp_studio.services.render_worker_health_service import RenderWorkerHealthService


class LocalRenderWorkerOrchestratorService:
    def __init__(self, repository: InMemoryLocalRenderWorkerRepository | None = None):
        self.repository = repository or InMemoryLocalRenderWorkerRepository()
        self.workers = LocalRenderWorkerService(self.repository)
        self.queue = RenderJobQueueService(self.repository)
        self.leases = RenderJobLeaseService(self.repository)
        self.heartbeats = RenderJobHeartbeatService(self.repository)
        self.results = RenderJobResultService(self.repository)
        self.health = RenderWorkerHealthService()
