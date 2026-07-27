from __future__ import annotations

from uuid import NAMESPACE_URL, UUID, uuid5

from ccp_studio.contracts.golden_path_orchestrator import (
    GoldenPathRun,
    GoldenPathStageResult,
    GoldenPathStatus,
)
from ccp_studio.contracts.orchestration import (
    ActiveObjectRef,
    OrchestrationRun,
    StageExecutionPlan,
    StageExecutionReceipt,
    StageRunStatus,
    ValidationContract,
    utc_now,
)


class GoldenPathOrchestrationSpineAdapterService:
    """Map Golden Path receipts into the existing orchestration spine.

    This adapter is intentionally projection-only: it does not run the golden
    path, mutate upstream compiler outputs, or create a second harness.
    """

    def map_to_orchestration_run(self, golden_run: GoldenPathRun) -> OrchestrationRun:
        now = utc_now()
        return OrchestrationRun(
            schema_version="cmf.orchestration_run.v1",
            orchestration_run_id=self._run_id(golden_run),
            organization_id=self._stable_uuid("organization", "cmf_studio"),
            brand_id=self._stable_uuid("brand", golden_run.input.brand_id),
            actor_id=self._stable_uuid("actor", "format02_golden_path_orchestrator"),
            active_object=self._active_object(golden_run),
            requested_outcome="format02_golden_path_source_to_fake_export",
            status=self._run_status(golden_run.status),
            correlation_id=self._stable_uuid("correlation", golden_run.golden_path_run_id),
            opened_at=now,
            updated_at=now,
        )

    def compile_stage_execution_plans(
        self, golden_run: GoldenPathRun
    ) -> list[StageExecutionPlan]:
        orchestration_run = self.map_to_orchestration_run(golden_run)
        stage_names = [stage.stage_name.value for stage in golden_run.stage_results]
        if not stage_names:
            stage_names = [stage.value for stage in golden_run.recipe.stage_names]

        plans: list[StageExecutionPlan] = []
        for index, stage_name in enumerate(stage_names):
            stage_ref = self._stage_ref(golden_run, stage_name, index)
            plans.append(
                StageExecutionPlan(
                    schema_version="cmf.stage_execution_plan.v1",
                    stage_execution_plan_id=self._stable_uuid(
                        "stage_execution_plan", stage_ref
                    ),
                    orchestration_run_id=orchestration_run.orchestration_run_id,
                    pipeline_stage=stage_name,
                    entry_object=orchestration_run.active_object,
                    expected_exit_object_type=f"golden_path.{stage_name}.output",
                    allowed_actor_or_service="Format02GoldenPathOrchestratorService",
                    required_inputs=self._required_inputs_for_stage(
                        golden_run, stage_name, index
                    ),
                    allowed_actions=["execute_stage", "record_receipt"],
                    blocked_actions=[
                        "skip_stage",
                        "call_provider",
                        "call_remotion",
                        "call_ffmpeg",
                        "create_second_harness",
                    ],
                    downstream_proof_obligation=(
                        f"Record GoldenPathStageResult for {stage_name} with "
                        "source, brand context, and output evidence refs."
                    ),
                    created_at=utc_now(),
                )
            )
        return plans

    def compile_validation_contracts(
        self, golden_run: GoldenPathRun
    ) -> list[ValidationContract]:
        plans = self.compile_stage_execution_plans(golden_run)
        stage_results_by_name = {
            stage.stage_name.value: stage for stage in golden_run.stage_results
        }
        return [
            ValidationContract(
                schema_version="cmf.validation_contract.v1",
                validation_contract_id=self._stable_uuid(
                    "validation_contract", str(plan.stage_execution_plan_id)
                ),
                stage_execution_plan_id=plan.stage_execution_plan_id,
                success_criteria=[
                    f"{plan.pipeline_stage} produces a passing GoldenPathStageResult",
                    "brand_context_version_id is preserved",
                    "source_span_refs are preserved where applicable",
                    "no providers, Remotion, or FFmpeg are called",
                ],
                failure_criteria=self._gate_codes_for_stage(plan.pipeline_stage),
                thresholds={},
                required_receipt_types=["golden_path_stage_result"],
                forbidden_skips=plan.blocked_actions,
                required_evidence_refs=self._stage_evidence_refs(
                    golden_run, stage_results_by_name.get(plan.pipeline_stage)
                ),
                created_at=utc_now(),
            )
            for plan in plans
        ]

    def compile_stage_execution_receipts(
        self, golden_run: GoldenPathRun
    ) -> list[StageExecutionReceipt]:
        orchestration_run = self.map_to_orchestration_run(golden_run)
        plans = self.compile_stage_execution_plans(golden_run)
        plans_by_stage = {plan.pipeline_stage: plan for plan in plans}
        receipts: list[StageExecutionReceipt] = []
        for stage_result in golden_run.stage_results:
            plan = plans_by_stage[stage_result.stage_name.value]
            receipts.append(
                StageExecutionReceipt(
                    schema_version="cmf.stage_execution_receipt.v1",
                    receipt_id=self._stable_uuid(
                        "stage_execution_receipt",
                        stage_result.golden_path_stage_result_id,
                    ),
                    orchestration_run_id=orchestration_run.orchestration_run_id,
                    stage_execution_plan_id=plan.stage_execution_plan_id,
                    receipt_type="golden_path_stage_result",
                    status=self._stage_status(stage_result.status),
                    decision=self._decision(stage_result),
                    evidence_refs=self._stage_evidence_refs(golden_run, stage_result),
                    correlation_id=orchestration_run.correlation_id,
                    output_object=ActiveObjectRef(
                        object_type=f"golden_path.{stage_result.stage_name.value}.output",
                        object_id=self._stable_uuid(
                            "golden_path_stage_result",
                            stage_result.golden_path_stage_result_id,
                        ),
                        version_id=self._stable_uuid(
                            "brand_context_version",
                            golden_run.input.brand_context_version_id,
                        ),
                    ),
                    created_event_id=None,
                    created_at=utc_now(),
                )
            )
        return receipts

    def map_to_spine_bundle(self, golden_run: GoldenPathRun) -> dict[str, object]:
        """Return a deterministic read model for docs/UI without new runtime."""

        return {
            "orchestration_run": self.map_to_orchestration_run(golden_run),
            "stage_execution_plans": self.compile_stage_execution_plans(golden_run),
            "validation_contracts": self.compile_validation_contracts(golden_run),
            "stage_execution_receipts": self.compile_stage_execution_receipts(
                golden_run
            ),
        }

    def _active_object(self, golden_run: GoldenPathRun) -> ActiveObjectRef:
        return ActiveObjectRef(
            object_type="golden_path_run",
            object_id=self._stable_uuid("golden_path_run", golden_run.golden_path_run_id),
            version_id=self._stable_uuid(
                "brand_context_version", golden_run.input.brand_context_version_id
            ),
        )

    def _required_inputs_for_stage(
        self, golden_run: GoldenPathRun, stage_name: str, index: int
    ) -> list[str]:
        required = [
            f"brand_context_version_id:{golden_run.input.brand_context_version_id}",
            *[f"source_span_ref:{ref}" for ref in golden_run.input.source_span_refs],
        ]
        if index > 0:
            required.append("previous_stage_receipt")
        if stage_name in {"composition_scenes_compile", "video_timeline_compile"}:
            required.append("authorized_format_program")
        if stage_name in {"avatar_plans_compile", "video_timeline_compile"}:
            required.append("locked_format02_composition")
        if stage_name in {"fake_render_compile", "export_compile"}:
            required.append("fake_render_only")
        return required

    def _stage_evidence_refs(
        self, golden_run: GoldenPathRun, stage_result: GoldenPathStageResult | None
    ) -> list[str]:
        refs = [
            f"brand_context_version_id:{golden_run.input.brand_context_version_id}",
            *[f"source_span_ref:{ref}" for ref in golden_run.input.source_span_refs],
        ]
        if stage_result is not None:
            refs.append(f"golden_stage_result:{stage_result.golden_path_stage_result_id}")
            refs.extend(f"output:{key}:{value}" for key, value in stage_result.output_refs.items())
            refs.extend(f"receipt:{key}:{value}" for key, value in stage_result.receipt_refs.items())
        if golden_run.output is not None:
            refs.extend(
                [
                    f"video_timeline:{golden_run.output.video_timeline_program_id}",
                    f"proxy_render:{golden_run.output.proxy_render_receipt_id}",
                    f"final_render:{golden_run.output.final_render_receipt_id}",
                    f"export_pack:{golden_run.output.export_pack_id}",
                ]
            )
        if golden_run.object_spine_map is not None:
            refs.append(f"object_spine_map:{golden_run.object_spine_map.golden_path_object_spine_map_id}")
        return refs

    def _gate_codes_for_stage(self, stage_name: str) -> list[str]:
        common = [
            "missing_brand_context_version_id",
            "missing_source_span_refs",
            "second_harness_created",
            "external_provider_called",
            "real_renderer_called",
        ]
        stage_specific = {
            "fixture_load": ["scene_count_not_8"],
            "composition_scenes_compile": ["composition_not_locked"],
            "avatar_plans_compile": [
                "avatar_lipsync_detected",
                "missing_proxy_sfl_function",
            ],
            "video_timeline_compile": ["timeline_compile_failed"],
            "fake_render_compile": ["fake_render_hash_missing"],
            "eval_run": ["eval_failed"],
            "export_compile": ["export_not_approved"],
        }
        return common + stage_specific.get(stage_name, [])

    def _decision(self, stage_result: GoldenPathStageResult) -> str:
        if stage_result.status == GoldenPathStatus.PASS:
            return f"{stage_result.stage_name.value}_passed"
        if stage_result.blockers:
            return "; ".join(stage_result.blockers)
        return f"{stage_result.stage_name.value}_{stage_result.status.value}"

    def _run_status(self, status: GoldenPathStatus) -> StageRunStatus:
        if status == GoldenPathStatus.PASS:
            return StageRunStatus.succeeded
        if status == GoldenPathStatus.FAIL:
            return StageRunStatus.failed
        if status == GoldenPathStatus.RUNNING:
            return StageRunStatus.executing
        return StageRunStatus.opened

    def _stage_status(self, status: GoldenPathStatus) -> StageRunStatus:
        return self._run_status(status)

    def _run_id(self, golden_run: GoldenPathRun) -> UUID:
        return self._stable_uuid("orchestration_run", golden_run.golden_path_run_id)

    def _stage_ref(self, golden_run: GoldenPathRun, stage_name: str, index: int) -> str:
        return f"{golden_run.golden_path_run_id}:{index}:{stage_name}"

    def _stable_uuid(self, namespace: str, value: str) -> UUID:
        return uuid5(NAMESPACE_URL, f"cmf:{namespace}:{value}")
