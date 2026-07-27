from __future__ import annotations

try:
    from fastapi import APIRouter, HTTPException
except Exception:  # pragma: no cover
    APIRouter = None  # type: ignore
    HTTPException = Exception  # type: ignore

from ccp_studio.services.pipeline_run_monitor_service import PipelineRunMonitorService


def create_pipeline_run_monitor_router(service: PipelineRunMonitorService | None = None):
    if APIRouter is None:
        raise RuntimeError("FastAPI is required to create the Pipeline Run Monitor router")

    monitor_service = service or PipelineRunMonitorService()
    router = APIRouter(prefix="/api/v1", tags=["pipeline-run-monitor"])

    def handle(fn):
        try:
            return fn()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    @router.get("/pipeline-runs")
    def list_pipeline_runs():
        return handle(monitor_service.list_runs)

    @router.get("/pipeline-runs/{pipeline_run_id}")
    def get_pipeline_run_monitor(pipeline_run_id: str):
        return handle(lambda: monitor_service.get_run_monitor(pipeline_run_id))

    @router.get("/pipeline-runs/{pipeline_run_id}/scene-outputs")
    def get_pipeline_scene_outputs(pipeline_run_id: str):
        return handle(lambda: monitor_service.get_pipeline_scene_outputs(pipeline_run_id))

    @router.get("/golden-path-runs/{golden_path_run_id}")
    def get_golden_path_detail(golden_path_run_id: str):
        return handle(lambda: monitor_service.get_golden_path_detail(golden_path_run_id))

    return router


router = create_pipeline_run_monitor_router() if APIRouter is not None else None
