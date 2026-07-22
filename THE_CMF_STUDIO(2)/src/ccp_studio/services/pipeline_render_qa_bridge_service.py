from __future__ import annotations

from ccp_studio.contracts.render_qa import PassStatus, RenderQACompositeReport
from ccp_studio.contracts.studio_pipeline_recipe_harness import (
    PipelineArtifactRef,
    PipelineArtifactRole,
    PipelineRunBlocker,
)
from ccp_studio.services.pipeline_artifact_ref_service import PipelineArtifactRefService


class PipelineRenderQABridgeService:
    """Project Render QA V1 reports into pipeline recipe read/control objects."""

    provider_calls_executed = False
    renderer_calls_executed = False
    local_worker_jobs_executed = False

    def __init__(self, artifact_service: PipelineArtifactRefService | None = None):
        self.artifact_service = artifact_service or PipelineArtifactRefService()

    def report_artifact_ref(
        self,
        report: RenderQACompositeReport,
        *,
        workspace_id: str | None = None,
        run_id: str | None = None,
    ) -> PipelineArtifactRef:
        return self.artifact_service.pointer(
            role=PipelineArtifactRole.QA_RECEIPT,
            uri=f"render_qa://composite/{report.render_qa_composite_report_id}",
            source_ref_ids=[report.file_ref],
            workspace_id=workspace_id,
            run_id=run_id,
        )

    def blockers_from_report(
        self,
        report: RenderQACompositeReport,
        *,
        step_id: str = "render_qa",
    ) -> list[PipelineRunBlocker]:
        if report.pass_status != PassStatus.FAIL:
            return []
        return [
            PipelineRunBlocker(
                code=blocker.code,
                message=blocker.message,
                step_id=step_id,
                recoverable=blocker.recoverable,
            )
            for blocker in report.blockers
        ]
