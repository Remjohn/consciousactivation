from __future__ import annotations

from ccp_studio.contracts.local_render_worker import RenderJob, RenderJobQueue, RenderJobStatus, RenderJobType
from ccp_studio.repositories.local_render_worker import InMemoryLocalRenderWorkerRepository


class RenderJobQueueService:
    def __init__(self, repository: InMemoryLocalRenderWorkerRepository | None = None):
        self.repository = repository or InMemoryLocalRenderWorkerRepository()

    def create_queue(self, queue_name: str = "local_render_queue") -> RenderJobQueue:
        queue = RenderJobQueue(queue_name=queue_name)
        self.repository.upsert("queues", queue.render_job_queue_id, queue)
        return queue

    def create_job(
        self,
        *,
        job_type: RenderJobType,
        job_name: str,
        payload: dict | None = None,
        requested_by: str = "system",
        required_capability_ids: list[str] | None = None,
        priority: int = 100,
    ) -> RenderJob:
        job = RenderJob(
            job_type=job_type,
            job_name=job_name,
            requested_by=requested_by,
            payload=payload or {},
            required_capability_ids=required_capability_ids or ["runtime:python_fake"],
            priority=priority,
            status=RenderJobStatus.CREATED,
        )
        self.repository.upsert("jobs", job.render_job_id, job)
        return job

    def enqueue(self, queue: RenderJobQueue, job: RenderJob) -> RenderJobQueue:
        job.status = RenderJobStatus.QUEUED
        queue.jobs.append(job)
        queue.jobs = sorted(queue.jobs, key=lambda j: (j.priority, j.created_at))
        self.repository.upsert("jobs", job.render_job_id, job)
        self.repository.upsert("queues", queue.render_job_queue_id, queue)
        return queue

    def next_queued_job(self, queue: RenderJobQueue) -> RenderJob | None:
        queued = [job for job in queue.jobs if job.status == RenderJobStatus.QUEUED]
        return queued[0] if queued else None
