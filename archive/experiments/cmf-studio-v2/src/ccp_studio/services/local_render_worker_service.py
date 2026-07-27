from __future__ import annotations

from ccp_studio.contracts.local_render_worker import (
    CapabilityStatus,
    LocalRenderWorker,
    LocalRenderWorkerCapability,
    LocalRuntimeName,
    RenderJobType,
    WorkerStatus,
)
from ccp_studio.repositories.local_render_worker import InMemoryLocalRenderWorkerRepository


class LocalRenderWorkerService:
    def __init__(self, repository: InMemoryLocalRenderWorkerRepository | None = None):
        self.repository = repository or InMemoryLocalRenderWorkerRepository()

    def compile_fake_python_capability(self) -> LocalRenderWorkerCapability:
        return LocalRenderWorkerCapability(
            capability_id="runtime:python_fake",
            display_name="Python Fake Renderer",
            runtime_name=LocalRuntimeName.PYTHON_FAKE,
            enabled=True,
            tested=True,
            status=CapabilityStatus.AVAILABLE,
            supports_job_types=list(RenderJobType),
            version="v1",
            notes="Fake deterministic local worker capability. No external runtime calls.",
        )

    def compile_disabled_remotion_capability(self) -> LocalRenderWorkerCapability:
        return LocalRenderWorkerCapability(
            capability_id="runtime:render:remotion",
            display_name="Remotion",
            runtime_name=LocalRuntimeName.REMOTION,
            enabled=False,
            tested=False,
            status=CapabilityStatus.DISABLED,
            supports_job_types=[RenderJobType.PROXY_VIDEO_RENDER, RenderJobType.FINAL_VIDEO_RENDER, RenderJobType.TEMPLATE_PREVIEW_RENDER],
        )

    def register_worker(
        self,
        *,
        worker_id: str,
        machine_id: str,
        display_name: str,
        workspace_root: str | None = None,
        capabilities: list[LocalRenderWorkerCapability] | None = None,
        max_concurrent_jobs: int = 1,
    ) -> LocalRenderWorker:
        worker = LocalRenderWorker(
            worker_id=worker_id,
            machine_id=machine_id,
            display_name=display_name,
            workspace_root=workspace_root,
            capabilities=capabilities or [self.compile_fake_python_capability()],
            max_concurrent_jobs=max_concurrent_jobs,
            status=WorkerStatus.ONLINE,
        )
        self.repository.upsert("workers", worker.worker_id, worker)
        return worker

    def set_worker_status(self, worker: LocalRenderWorker, status: WorkerStatus) -> LocalRenderWorker:
        worker.status = status
        self.repository.upsert("workers", worker.worker_id, worker)
        return worker
