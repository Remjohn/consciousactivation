from __future__ import annotations

from datetime import datetime, timezone

from ccp_studio.contracts.golden_path_orchestrator import GoldenPathRun, GoldenPathStatus
from ccp_studio.contracts.studio_pipeline_recipe_harness import (
    PipelineArtifactRole,
    PipelineRun,
    PipelineRunBlocker,
    PipelineRunStatus,
    PipelineStepStatus,
)
from ccp_studio.services.golden_path_orchestration_spine_adapter_service import (
    GoldenPathOrchestrationSpineAdapterService,
)
from ccp_studio.services.pipeline_artifact_ref_service import PipelineArtifactRefService
from ccp_studio.services.pipeline_recipe_catalog_service import PipelineRecipeCatalogService
from ccp_studio.services.pipeline_run_service import PipelineRunService
from ccp_studio.services.pipeline_run_summary_service import PipelineRunSummaryService
from ccp_studio.contracts.studio_pipeline_recipe_harness import PipelineRecipeId


class Format02GoldenPathRecipeAdapterService:
    """Project an existing GoldenPathRun into the recipe harness read model.

    This adapter does not run the golden path, call providers, call renderers,
    or call the Local Render Worker. It maps already-created golden path
    outputs into pointer-only PipelineArtifactRef records and PipelineRun
    summary state.
    """

    provider_calls_executed = False
    renderer_calls_executed = False
    local_worker_calls_executed = False

    def __init__(
        self,
        *,
        catalog_service: PipelineRecipeCatalogService | None = None,
        run_service: PipelineRunService | None = None,
        summary_service: PipelineRunSummaryService | None = None,
        artifact_service: PipelineArtifactRefService | None = None,
        spine_adapter: GoldenPathOrchestrationSpineAdapterService | None = None,
    ):
        self.catalog_service = catalog_service or PipelineRecipeCatalogService()
        self.run_service = run_service or PipelineRunService()
        self.summary_service = summary_service or PipelineRunSummaryService()
        self.artifact_service = artifact_service or PipelineArtifactRefService()
        self.spine_adapter = spine_adapter or GoldenPathOrchestrationSpineAdapterService()

    def to_pipeline_run(self, golden_run: GoldenPathRun, *, workspace_id: str | None = None) -> PipelineRun:
        recipe = self.catalog_service.get_recipe(PipelineRecipeId.FORMAT02_GOLDEN_PATH)
        orchestration_run = self.spine_adapter.map_to_orchestration_run(golden_run)
        artifacts = self.compile_artifact_refs(golden_run, workspace_id=workspace_id)
        pipeline_run = self.run_service.create_run(
            recipe=recipe,
            brand_context_version_id=golden_run.input.brand_context_version_id,
            workspace_id=workspace_id,
            orchestration_run_id=str(orchestration_run.orchestration_run_id),
            input_artifacts=artifacts,
        )
        if golden_run.status == GoldenPathStatus.PASS:
            pipeline_run.status = PipelineRunStatus.SUCCEEDED
            self._mark_steps_succeeded(pipeline_run)
        elif golden_run.status == GoldenPathStatus.FAIL:
            pipeline_run.status = PipelineRunStatus.FAILED
            pipeline_run.blockers = [
                PipelineRunBlocker(
                    code=blocker.code,
                    message=blocker.message,
                    step_id=blocker.stage_name.value,
                )
                for blocker in (golden_run.receipt.blockers if golden_run.receipt else [])
            ]
        return pipeline_run

    def summarize(self, golden_run: GoldenPathRun, *, workspace_id: str | None = None):
        return self.summary_service.summarize(
            self.to_pipeline_run(golden_run, workspace_id=workspace_id)
        )

    def compile_artifact_refs(
        self, golden_run: GoldenPathRun, *, workspace_id: str | None = None
    ):
        source_refs = list(golden_run.input.source_span_refs)
        artifacts = [
            self.artifact_service.pointer(
                role=PipelineArtifactRole.SOURCE_REF,
                uri=f"golden_path://source_span/{source_ref}",
                source_ref_ids=[source_ref],
                workspace_id=workspace_id,
            )
            for source_ref in source_refs
        ]
        if golden_run.output is None:
            return artifacts

        output = golden_run.output
        pointer_specs = [
            (PipelineArtifactRole.INTERMEDIATE, "format_program", output.format_program_id),
            (PipelineArtifactRole.INTERMEDIATE, "video_timeline", output.video_timeline_program_id),
            (PipelineArtifactRole.RENDER_OUTPUT, "proxy_render", output.proxy_render_receipt_id),
            (PipelineArtifactRole.RENDER_OUTPUT, "final_render", output.final_render_receipt_id),
            (PipelineArtifactRole.QA_RECEIPT, "evaluation", output.evaluation_receipt_id),
            (PipelineArtifactRole.APPROVAL_RECEIPT, "approval", output.approval_packet_id),
            (PipelineArtifactRole.EXPORT, "export_pack", output.export_pack_id),
        ]
        for role, name, ref in pointer_specs:
            artifacts.append(
                self.artifact_service.pointer(
                    role=role,
                    uri=f"golden_path://{name}/{ref}",
                    source_ref_ids=source_refs,
                    workspace_id=workspace_id,
                )
            )

        for scene_id in output.scene_program_ids:
            artifacts.append(
                self.artifact_service.pointer(
                    role=PipelineArtifactRole.INTERMEDIATE,
                    uri=f"golden_path://scene_program/{scene_id}",
                    source_ref_ids=source_refs,
                    workspace_id=workspace_id,
                )
            )
        for receipt_id in output.composition_decision_receipt_ids:
            artifacts.append(
                self.artifact_service.pointer(
                    role=PipelineArtifactRole.QA_RECEIPT,
                    uri=f"golden_path://composition_receipt/{receipt_id}",
                    source_ref_ids=source_refs,
                    workspace_id=workspace_id,
                )
            )
        return artifacts

    def to_read_model(self, golden_run: GoldenPathRun, *, workspace_id: str | None = None):
        pipeline_run = self.to_pipeline_run(golden_run, workspace_id=workspace_id)
        return {
            "pipeline_run": pipeline_run,
            "summary": self.summary_service.summarize(pipeline_run),
            "orchestration_run_id": pipeline_run.orchestration_run_id,
            "provider_calls_executed": self.provider_calls_executed,
            "renderer_calls_executed": self.renderer_calls_executed,
            "local_worker_calls_executed": self.local_worker_calls_executed,
        }

    def _mark_steps_succeeded(self, pipeline_run: PipelineRun) -> None:
        completed_at = datetime.now(timezone.utc).isoformat()
        artifact_ids = [artifact.pipeline_artifact_ref_id for artifact in pipeline_run.input_artifacts]
        for step in pipeline_run.step_runs:
            step.status = PipelineStepStatus.SUCCEEDED
            step.completed_at = completed_at
            step.output_artifact_ids = artifact_ids

