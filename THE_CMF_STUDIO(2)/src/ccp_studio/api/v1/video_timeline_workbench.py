from __future__ import annotations

try:
    from fastapi import APIRouter, HTTPException
except Exception:  # pragma: no cover
    APIRouter = None  # type: ignore
    HTTPException = Exception  # type: ignore

from ccp_studio.contracts.video_timeline_workbench import (
    OTIOExportRequest,
    ProxyRenderRequest,
    VideoTimelineEditProposal,
    VideoTimelineEditSubmission,
)
from ccp_studio.services.video_timeline_workbench_service import VideoTimelineWorkbenchService


def create_video_timeline_workbench_router(service: VideoTimelineWorkbenchService | None = None):
    if APIRouter is None:
        raise RuntimeError("FastAPI is required to create the Video Timeline Workbench router")

    workbench = service or VideoTimelineWorkbenchService()
    router = APIRouter(prefix="/api/v1/video-edit-programs", tags=["video-timeline-workbench"])

    def handle(fn):
        try:
            return fn()
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    @router.get("/current/timeline-workbench")
    def get_current_timeline_workbench(format: str | None = None):
        return handle(lambda: workbench.get_current_workbench(format=format))

    @router.get("/{program_id}/timeline-workbench")
    def get_timeline_workbench(program_id: str):
        return handle(lambda: workbench.get_workbench(program_id))

    @router.post("/{program_id}/timeline-edits/propose")
    def propose_timeline_edit(program_id: str, request: VideoTimelineEditProposal):
        return handle(lambda: workbench.propose_timeline_edit(program_id, request))

    @router.post("/{program_id}/timeline-edits/submit")
    def submit_timeline_edit(program_id: str, request: VideoTimelineEditSubmission):
        return handle(lambda: workbench.submit_timeline_edit(program_id, request))

    @router.post("/{program_id}/proxy-renders")
    def create_proxy_render(program_id: str, request: ProxyRenderRequest | None = None):
        return handle(lambda: workbench.create_proxy_render(program_id, request or ProxyRenderRequest()))

    @router.get("/{program_id}/render-jobs/{render_job_id}")
    def get_render_job_state(program_id: str, render_job_id: str):
        return handle(lambda: workbench.get_render_job_state(program_id, render_job_id))

    @router.post("/{program_id}/otio-exports")
    def export_otio(program_id: str, request: OTIOExportRequest | None = None):
        return handle(lambda: workbench.export_otio(program_id, request or OTIOExportRequest()))

    return router


router = create_video_timeline_workbench_router() if APIRouter is not None else None
