from __future__ import annotations

from datetime import datetime, timezone

from ccp_studio.contracts.local_render_worker import (
    HealthStatus,
    LocalRenderWorker,
    RenderWorkerHealthReceipt,
    WorkerStatus,
)


class RenderWorkerHealthService:
    def evaluate_health(
        self,
        *,
        worker: LocalRenderWorker,
        required_capability_ids: list[str] | None = None,
        max_heartbeat_age_seconds: int = 300,
    ) -> RenderWorkerHealthReceipt:
        required = required_capability_ids or []
        available = [cap.capability_id for cap in worker.capabilities if cap.available]
        missing = [cap_id for cap_id in required if cap_id not in available]
        stale = False
        if worker.last_heartbeat_at:
            age = datetime.now(timezone.utc) - datetime.fromisoformat(worker.last_heartbeat_at)
            stale = age.total_seconds() > max_heartbeat_age_seconds
        elif worker.status in {WorkerStatus.ONLINE, WorkerStatus.BUSY}:
            stale = True
        blockers = []
        if missing:
            blockers.append("missing_required_capabilities")
        if stale:
            blockers.append("stale_heartbeat")
        if worker.status in {WorkerStatus.OFFLINE, WorkerStatus.UNHEALTHY}:
            blockers.append("worker_offline_or_unhealthy")
        if blockers:
            status = HealthStatus.FAIL
        elif worker.status == WorkerStatus.DEGRADED:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.PASS
        return RenderWorkerHealthReceipt(
            worker_id=worker.worker_id,
            health_status=status,
            required_capability_ids=required,
            available_capability_ids=available,
            missing_capability_ids=missing,
            stale_heartbeat=stale,
            worker_status=worker.status,
            blockers=blockers,
        )
