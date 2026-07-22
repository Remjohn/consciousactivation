from __future__ import annotations

from datetime import datetime, timezone

from ccp_studio.contracts.pipeline_run_monitor import (
    GoldenPathRunDetailReadModel,
    PipelineApprovalReadModel,
    PipelineArtifactReadModel,
    PipelineBlockerReadModel,
    PipelineRunMonitorReadModel,
    PipelineRunStatusReadModel,
    PipelineSceneOutputLinkReadModel,
    PipelineStageReceiptReadModel,
)
from ccp_studio.contracts.studio_pipeline_recipe_harness import (
    PassStatus,
    PipelineApprovalStatus,
    PipelineArtifactRole,
    PipelineBlockerSeverity,
    PipelineRecipeId,
    PipelineRunBlocker,
    PipelineRunStatus,
    PipelineStepStatus,
)
from ccp_studio.services.pipeline_artifact_ref_service import PipelineArtifactRefService
from ccp_studio.services.pipeline_recipe_catalog_service import PipelineRecipeCatalogService
from ccp_studio.services.pipeline_run_service import PipelineRunService
from ccp_studio.services.pipeline_run_summary_service import PipelineRunSummaryService


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _enum_value(value) -> str:
    return getattr(value, "value", value)


def _dump_model(model):
    return model.model_dump() if hasattr(model, "model_dump") else model.dict()


class PipelineRunMonitorService:
    """Compile read models for operator pipeline monitoring.

    The service is intentionally read-model only. It does not run recipes,
    providers, renderers, Local Render Worker jobs, or Golden Path stages.
    """

    provider_calls_executed = False
    renderer_calls_executed = False
    local_worker_jobs_executed = False

    def __init__(
        self,
        *,
        catalog_service: PipelineRecipeCatalogService | None = None,
        run_service: PipelineRunService | None = None,
        summary_service: PipelineRunSummaryService | None = None,
        artifact_service: PipelineArtifactRefService | None = None,
    ):
        self.catalog_service = catalog_service or PipelineRecipeCatalogService()
        self.run_service = run_service or PipelineRunService()
        self.summary_service = summary_service or PipelineRunSummaryService()
        self.artifact_service = artifact_service or PipelineArtifactRefService()
        self._monitors: dict[str, PipelineRunMonitorReadModel] = {}
        self._golden_path_details: dict[str, GoldenPathRunDetailReadModel] = {}
        self._seed_demo_state()

    def list_runs(self) -> list[PipelineRunStatusReadModel]:
        return [monitor.run_status for monitor in self._monitors.values()]

    def get_run_monitor(self, pipeline_run_id: str) -> PipelineRunMonitorReadModel:
        try:
            return self._monitors[pipeline_run_id]
        except KeyError as exc:
            raise KeyError(f"pipeline_run_id not found: {pipeline_run_id}") from exc

    def get_pipeline_scene_outputs(self, pipeline_run_id: str) -> list[PipelineSceneOutputLinkReadModel]:
        return self.get_run_monitor(pipeline_run_id).scene_output_links

    def get_golden_path_detail(self, golden_path_run_id: str) -> GoldenPathRunDetailReadModel:
        try:
            return self._golden_path_details[golden_path_run_id]
        except KeyError as exc:
            raise KeyError(f"golden_path_run_id not found: {golden_path_run_id}") from exc

    def build_scene_output_links(self, artifacts: list[PipelineArtifactReadModel]) -> list[PipelineSceneOutputLinkReadModel]:
        template_artifacts = [artifact for artifact in artifacts if artifact.linked_preview_type == "template_preview"]
        video_artifacts = [artifact for artifact in artifacts if artifact.linked_preview_type == "video_preview"]
        template_url = template_artifacts[0].linked_preview_url if template_artifacts else None
        video_url = video_artifacts[0].linked_preview_url if video_artifacts else None
        artifact_refs = [
            artifact.pipeline_artifact_ref_id or artifact.artifact_ref_id or artifact.artifact_id
            for artifact in [*template_artifacts, *video_artifacts]
        ]
        return [
            PipelineSceneOutputLinkReadModel(
                scene_id="format02_scene_01",
                step_id="format02_composition",
                template_preview_url=template_url,
                video_preview_url=video_url,
                artifact_refs=artifact_refs,
                status="preview_available" if template_url or video_url else "preview_unavailable",
            )
        ]

    def _seed_demo_state(self) -> None:
        recipe = self.catalog_service.get_recipe(PipelineRecipeId.FORMAT02_GOLDEN_PATH)
        run = self.run_service.create_run(
            recipe=recipe,
            brand_context_version_id="bcv_health_myth_demo_v1",
            workspace_id="workspace_health_myth_demo",
            orchestration_run_id="orch_format02_pipeline_monitor_demo",
            input_artifacts=[],
        )
        run.pipeline_run_id = "pipeline_run_format02_health_myth_demo"
        run.status = PipelineRunStatus.BLOCKED

        blocker = PipelineRunBlocker(
            code="approval_gate_not_approved",
            message="Provider batch is blocked until scene, face plate, and template preview samples are approved.",
            severity=PipelineBlockerSeverity.BLOCKING,
            step_id="provider_samples",
            recoverable=True,
        )
        run.blockers = [blocker]

        completed_step_ids = {
            "source_intake",
            "narrative_story_doctor",
            "format_intelligence",
            "format02_composition",
            "avatar_assets",
        }
        artifact_refs = self._demo_artifacts()
        artifact_ids = [artifact.pipeline_artifact_ref_id for artifact in artifact_refs]
        now = _now_iso()
        for step in run.step_runs:
            if step.step_id in completed_step_ids:
                step.status = PipelineStepStatus.SUCCEEDED
                step.started_at = now
                step.completed_at = now
                step.output_artifact_ids = artifact_ids
            elif step.step_id == "provider_samples":
                step.status = PipelineStepStatus.BLOCKED
                step.started_at = now
            else:
                step.status = PipelineStepStatus.PLANNED

        for gate in run.approval_gates:
            if gate.gate_id == "provider_sample_first":
                gate.approved_sample_types = ["scene_sample"]
                gate.blockers = [blocker]
            if gate.gate_id == "operator_final_approval":
                gate.status = PipelineApprovalStatus.PENDING

        summary = self.summary_service.summarize(run)
        artifacts = self._artifact_read_models(artifact_refs)
        blockers = [self._blocker_read_model(blocker)]
        approvals = [self._approval_read_model(gate) for gate in run.approval_gates]
        scene_links = self.build_scene_output_links(artifacts)
        monitor = PipelineRunMonitorReadModel(
            run_status=PipelineRunStatusReadModel(
                pipeline_run_id=run.pipeline_run_id,
                orchestration_run_id=run.orchestration_run_id,
                golden_path_run_id="golden_path_health_myth_demo",
                recipe_id=_enum_value(run.recipe_id),
                recipe_version=run.recipe_version,
                brand_context_version_id=run.brand_context_version_id,
                workspace_id=run.workspace_id,
                status=_enum_value(run.status),
                started_at=run.created_at,
                current_step_id=summary.next_step_id,
                progress_percent=round((summary.succeeded_steps / max(summary.total_steps, 1)) * 100),
                source_mode="synthetic",
                blocker_count=len(blockers),
                pending_approval_count=summary.pending_approval_count,
            ),
            stage_receipts=self._stage_receipts(recipe, run, blocker),
            artifacts=artifacts,
            blockers=blockers,
            approvals=approvals,
            scene_output_links=scene_links,
            summary=_dump_model(summary),
            provider_calls_executed=self.provider_calls_executed,
            renderer_calls_executed=self.renderer_calls_executed,
            local_worker_jobs_executed=self.local_worker_jobs_executed,
        )
        self._monitors[run.pipeline_run_id] = monitor
        self._golden_path_details["golden_path_health_myth_demo"] = self._golden_path_detail(monitor)

    def _demo_artifacts(self):
        source_refs = ["span_health_myth_1"]
        specs = [
            (PipelineArtifactRole.SOURCE_REF, "golden_path://source_span/span_health_myth_1"),
            (PipelineArtifactRole.INTERMEDIATE, "golden_path://scene_program/format02_scene_01"),
            (PipelineArtifactRole.TEMPLATE_PREVIEW, "template-preview://format02_scene_01"),
            (PipelineArtifactRole.RENDER_OUTPUT, "video-timeline://timeline_health_myth_demo"),
            (PipelineArtifactRole.QA_RECEIPT, "golden_path://evaluation/eval_health_myth_demo"),
            (PipelineArtifactRole.APPROVAL_RECEIPT, "golden_path://approval/approval_health_myth_demo"),
            (PipelineArtifactRole.EXPORT, "golden_path://export_pack/export_health_myth_demo"),
        ]
        return [
            self.artifact_service.pointer(role=role, uri=uri, source_ref_ids=source_refs, workspace_id="workspace_health_myth_demo")
            for role, uri in specs
        ]

    def _artifact_read_models(self, artifact_refs) -> list[PipelineArtifactReadModel]:
        read_models = []
        for artifact in artifact_refs:
            role = _enum_value(artifact.role)
            preview_type = "none"
            preview_url = None
            if role == PipelineArtifactRole.TEMPLATE_PREVIEW.value:
                preview_type = "template_preview"
                preview_url = "/template-preview/format02_scene_01"
            if role == PipelineArtifactRole.RENDER_OUTPUT.value and artifact.uri.startswith("video-timeline://"):
                preview_type = "video_preview"
                preview_url = "/timeline?program_id=timeline_health_myth_demo"
            read_models.append(
                PipelineArtifactReadModel(
                    artifact_id=artifact.pipeline_artifact_ref_id,
                    artifact_ref_id=artifact.artifact_ref_id,
                    pipeline_artifact_ref_id=artifact.pipeline_artifact_ref_id,
                    role=role,
                    uri=artifact.uri,
                    storage_state=_enum_value(artifact.storage_state),
                    sha256=artifact.sha256,
                    source_ref_ids=list(artifact.source_ref_ids),
                    linked_preview_type=preview_type,
                    linked_preview_url=preview_url,
                    raw_bytes_included=False,
                )
            )
        return read_models

    def _stage_receipts(self, recipe, run, blocker) -> list[PipelineStageReceiptReadModel]:
        step_names = {step.step_id: step.display_name for step in recipe.steps}
        receipts = []
        for step in run.step_runs:
            step_blockers = [self._blocker_read_model(blocker)] if step.step_id == blocker.step_id else []
            pass_status = PassStatus.PASS if step.status == PipelineStepStatus.SUCCEEDED else PassStatus.WARN
            if step_blockers:
                pass_status = PassStatus.FAIL
            receipts.append(
                PipelineStageReceiptReadModel(
                    step_id=step.step_id,
                    step_name=step_names.get(step.step_id, step.step_id),
                    step_kind=_enum_value(step.step_kind),
                    status=_enum_value(step.status),
                    pass_status=_enum_value(pass_status),
                    receipt_id=f"pipeline_step_receipt_{step.step_id}",
                    orchestration_stage_execution_id=step.orchestration_stage_execution_id,
                    started_at=step.started_at,
                    completed_at=step.completed_at,
                    message=self._stage_message(step.step_id, step.status),
                    blockers=step_blockers,
                )
            )
        return receipts

    def _stage_message(self, step_id: str, status) -> str:
        if status == PipelineStepStatus.SUCCEEDED:
            return f"{step_id} receipt passed in read-model demo state."
        if status == PipelineStepStatus.BLOCKED:
            return "Step is waiting on operator-visible approval gates."
        return "Step has not executed in this read-model view."

    def _blocker_read_model(self, blocker: PipelineRunBlocker) -> PipelineBlockerReadModel:
        return PipelineBlockerReadModel(
            blocker_id=blocker.pipeline_run_blocker_id,
            code=blocker.code,
            message=blocker.message,
            severity=_enum_value(blocker.severity),
            step_id=blocker.step_id,
            recoverable=blocker.recoverable,
        )

    def _approval_read_model(self, gate) -> PipelineApprovalReadModel:
        pending_reason = None
        if gate.status == PipelineApprovalStatus.PENDING:
            pending_reason = "Awaiting operator approval."
            if gate.gate_type.value == "sample_first":
                missing = sorted(set(gate.required_sample_types) - set(gate.approved_sample_types))
                pending_reason = f"Missing sample approvals: {', '.join(missing)}" if missing else pending_reason
        return PipelineApprovalReadModel(
            gate_id=gate.gate_id,
            gate_type=_enum_value(gate.gate_type),
            required=gate.required,
            status=_enum_value(gate.status),
            approved_by=gate.approved_by,
            pending_reason=pending_reason,
            blockers=[self._blocker_read_model(blocker) for blocker in gate.blockers],
            required_sample_types=list(gate.required_sample_types),
            approved_sample_types=list(gate.approved_sample_types),
        )

    def _golden_path_detail(self, monitor: PipelineRunMonitorReadModel) -> GoldenPathRunDetailReadModel:
        return GoldenPathRunDetailReadModel(
            golden_path_run_id=monitor.run_status.golden_path_run_id or "golden_path_health_myth_demo",
            pipeline_run_id=monitor.run_status.pipeline_run_id,
            orchestration_run_id=monitor.run_status.orchestration_run_id,
            brand_context_version_id=monitor.run_status.brand_context_version_id,
            input_fixture_refs=["fixtures/golden_path/health_myth_interview_brief.json"],
            narrative_outputs=[
                {"ref": "golden_path://extraction/extraction_health_myth_demo", "status": "ready"}
            ],
            format_outputs=[
                {"ref": "golden_path://format_program/format02_health_myth_demo", "status": "ready"}
            ],
            composition_scene_outputs=[
                {"scene_id": "format02_scene_01", "ref": "golden_path://scene_program/format02_scene_01", "status": "locked"}
            ],
            avatar_outputs=[
                {"ref": "golden_path://avatar_plan/avatar_health_myth_demo", "no_lip_sync": True}
            ],
            timeline_outputs=[
                {"ref": "video-timeline://timeline_health_myth_demo", "timeline_program_id": "timeline_health_myth_demo"}
            ],
            render_outputs=[
                {"ref": "golden_path://proxy_render/proxy_health_myth_demo", "fake_or_dry_run": True}
            ],
            approval_outputs=[
                {"ref": "golden_path://approval/approval_health_myth_demo", "status": "pending"}
            ],
            scene_output_links=monitor.scene_output_links,
            receipts=[
                {"receipt_id": receipt.receipt_id, "step_id": receipt.step_id, "pass_status": receipt.pass_status}
                for receipt in monitor.stage_receipts
            ],
            blockers=monitor.blockers,
            approvals=monitor.approvals,
            source_mode="synthetic",
            provider_calls_executed=self.provider_calls_executed,
            renderer_calls_executed=self.renderer_calls_executed,
            local_worker_jobs_executed=self.local_worker_jobs_executed,
        )
