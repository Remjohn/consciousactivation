from __future__ import annotations

from uuid import NAMESPACE_URL, UUID, uuid5

from ccp_studio.contracts.orchestration import (
    ActiveObjectRef,
    StageExecutionPlan,
    StageExecutionReceipt,
    StageRunStatus,
    ValidationContract,
    utc_now,
)
from ccp_studio.contracts.studio_pipeline_recipe_harness import (
    PassStatus,
    PipelineOrchestrationSpineBinding,
    PipelineRecipe,
    PipelineRun,
    PipelineStepReceipt,
    PipelineStepStatus,
)


class PipelineOrchestrationSpineAdapterService:
    """Projection adapter from recipe read models into the existing spine.

    The adapter does not run recipes and does not create a second workflow
    engine. It only compiles deterministic mappings and, where possible, real
    `StageExecutionPlan`, `ValidationContract`, and `StageExecutionReceipt`
    objects from the existing orchestration contracts.
    """

    def spine_available(self) -> bool:
        try:
            import ccp_studio.contracts.orchestration  # noqa: F401

            return True
        except Exception:
            return False

    def compile_binding(self, recipe: PipelineRecipe, orchestration_run_id: str | UUID):
        orchestration_run_id = str(self._orchestration_uuid(orchestration_run_id))
        return PipelineOrchestrationSpineBinding(
            orchestration_run_id=orchestration_run_id,
            stage_plan_refs={
                step.step_id: str(self._stage_plan_uuid(orchestration_run_id, step.step_id))
                for step in recipe.steps
            },
            validation_contract_refs={
                step.step_id: str(self._validation_uuid(orchestration_run_id, step.step_id))
                for step in recipe.steps
            },
            spine_available=self.spine_available(),
        )

    def compile_stage_execution_plans(
        self,
        recipe: PipelineRecipe,
        orchestration_run_id: str | UUID,
        *,
        active_object: ActiveObjectRef | None = None,
    ) -> list[StageExecutionPlan]:
        run_id = self._orchestration_uuid(orchestration_run_id)
        entry_object = active_object or self._active_object(recipe)
        plans: list[StageExecutionPlan] = []
        for step in recipe.steps:
            plans.append(
                StageExecutionPlan(
                    schema_version="cmf.stage_execution_plan.v1",
                    stage_execution_plan_id=self._stage_plan_uuid(run_id, step.step_id),
                    orchestration_run_id=run_id,
                    pipeline_stage=step.orchestration_stage_ref or step.step_id,
                    entry_object=entry_object,
                    expected_exit_object_type=f"pipeline_recipe.{recipe.recipe_id.value}.{step.step_id}.output",
                    allowed_actor_or_service="StudioPipelineRecipeHarness",
                    required_inputs=[
                        f"brand_context_version_id required by active PipelineRun",
                        *[f"dependency_step:{dep}" for dep in step.depends_on],
                        *[f"existing_service:{service_ref}" for service_ref in step.existing_service_refs],
                    ],
                    allowed_actions=[
                        "compile_stage_plan",
                        "record_stage_receipt",
                        "handoff_to_existing_service",
                    ],
                    blocked_actions=[
                        "create_parallel_harness",
                        "replace_orchestration_spine",
                        "call_provider",
                        "call_renderer",
                        "call_local_render_worker",
                        "execute_real_pipeline_stage",
                    ],
                    downstream_proof_obligation=(
                        f"Record PipelineStepReceipt for {step.step_id}; preserve recipe_id, "
                        "brand_context_version_id, orchestration_run_id, artifacts, and approvals."
                    ),
                    created_at=utc_now(),
                )
            )
        return plans

    def compile_validation_contracts(
        self,
        recipe: PipelineRecipe,
        orchestration_run_id: str | UUID,
    ) -> list[ValidationContract]:
        plans_by_stage = {
            plan.pipeline_stage: plan
            for plan in self.compile_stage_execution_plans(recipe, orchestration_run_id)
        }
        contracts: list[ValidationContract] = []
        for step in recipe.steps:
            stage_ref = step.orchestration_stage_ref or step.step_id
            plan = plans_by_stage[stage_ref]
            success = [
                f"{step.step_id} dependencies are satisfied",
                "PipelineStepReceipt has no blockers",
                "orchestration_run_id is preserved",
                "no providers, renderers, or workers are called by the recipe harness",
            ]
            failure = [
                "dependencies_not_satisfied",
                "approval_gate_not_approved",
                "sample_first_gate_not_approved",
                "pipeline_step_receipt_has_blockers",
                "parallel_harness_created",
                "provider_called",
                "renderer_called",
                "local_render_worker_called",
            ]
            if step.approval_gate_id:
                success.append(f"approval gate {step.approval_gate_id} passed")
            contracts.append(
                ValidationContract(
                    schema_version="cmf.validation_contract.v1",
                    validation_contract_id=self._validation_uuid(
                        orchestration_run_id, step.step_id
                    ),
                    stage_execution_plan_id=plan.stage_execution_plan_id,
                    success_criteria=success,
                    failure_criteria=failure,
                    thresholds={},
                    forbidden_skips=plan.blocked_actions,
                    required_evidence_refs=[
                        f"pipeline_recipe:{recipe.recipe_id.value}",
                        f"pipeline_step:{step.step_id}",
                    ],
                    required_receipt_types=["pipeline_step_receipt"],
                    created_at=utc_now(),
                )
            )
        return contracts

    def compile_stage_execution_receipts(
        self,
        run: PipelineRun,
        step_receipts: list[PipelineStepReceipt],
    ) -> list[StageExecutionReceipt]:
        if not run.orchestration_run_id:
            raise ValueError("PipelineRun requires orchestration_run_id for spine receipts")
        orchestration_run_id = self._orchestration_uuid(run.orchestration_run_id)
        receipts: list[StageExecutionReceipt] = []
        for receipt in step_receipts:
            receipts.append(
                StageExecutionReceipt(
                    schema_version="cmf.stage_execution_receipt.v1",
                    receipt_id=self._receipt_uuid(
                        orchestration_run_id, receipt.pipeline_step_receipt_id
                    ),
                    orchestration_run_id=orchestration_run_id,
                    stage_execution_plan_id=self._stage_plan_uuid(
                        orchestration_run_id, receipt.step_id
                    ),
                    receipt_type="pipeline_step_receipt",
                    status=self._stage_status(receipt.status, receipt.pass_status),
                    decision=self._decision(receipt),
                    evidence_refs=[
                        f"pipeline_run:{run.pipeline_run_id}",
                        f"pipeline_step:{receipt.step_id}",
                        *[f"pipeline_artifact:{artifact_id}" for artifact_id in receipt.output_artifact_ids],
                    ],
                    output_object=None,
                    created_event_id=None,
                    correlation_id=self._stable_uuid(
                        "pipeline_recipe_correlation", run.pipeline_run_id
                    ),
                    created_at=utc_now(),
                )
            )
        return receipts

    def compile_stage_plan_requests(
        self, recipe: PipelineRecipe, orchestration_run_id: str | UUID
    ) -> list[dict[str, object]]:
        binding = self.compile_binding(recipe, orchestration_run_id)
        return [
            {
                "orchestration_run_id": binding.orchestration_run_id,
                "stage_execution_plan_id": binding.stage_plan_refs[step.step_id],
                "validation_contract_id": binding.validation_contract_refs[step.step_id],
                "pipeline_recipe_id": recipe.recipe_id.value,
                "pipeline_step_id": step.step_id,
                "stage_ref": step.orchestration_stage_ref or step.step_id,
                "depends_on": list(step.depends_on),
                "existing_service_refs": list(step.existing_service_refs),
                "approval_gate_id": step.approval_gate_id,
            }
            for step in recipe.steps
        ]

    def compile_spine_bundle(
        self,
        recipe: PipelineRecipe,
        orchestration_run_id: str | UUID,
    ) -> dict[str, object]:
        return {
            "binding": self.compile_binding(recipe, orchestration_run_id),
            "stage_execution_plans": self.compile_stage_execution_plans(
                recipe, orchestration_run_id
            ),
            "validation_contracts": self.compile_validation_contracts(
                recipe, orchestration_run_id
            ),
            "stage_plan_requests": self.compile_stage_plan_requests(
                recipe, orchestration_run_id
            ),
        }

    def _active_object(self, recipe: PipelineRecipe) -> ActiveObjectRef:
        return ActiveObjectRef(
            object_type="pipeline_recipe",
            object_id=self._stable_uuid("pipeline_recipe", recipe.recipe_id.value),
            version_id=self._stable_uuid("pipeline_recipe_version", recipe.version),
        )

    def _stage_status(
        self, status: PipelineStepStatus, pass_status: PassStatus
    ) -> StageRunStatus:
        if pass_status == PassStatus.FAIL:
            return StageRunStatus.blocked
        if status == PipelineStepStatus.SUCCEEDED:
            return StageRunStatus.succeeded
        if status == PipelineStepStatus.FAILED:
            return StageRunStatus.failed
        if status == PipelineStepStatus.RUNNING:
            return StageRunStatus.executing
        if status == PipelineStepStatus.APPROVAL_REQUIRED:
            return StageRunStatus.waiting_for_human
        if status == PipelineStepStatus.BLOCKED:
            return StageRunStatus.blocked
        return StageRunStatus.planned

    def _decision(self, receipt: PipelineStepReceipt) -> str:
        if receipt.blockers:
            return "; ".join(f"{blocker.code}: {blocker.message}" for blocker in receipt.blockers)
        if receipt.message:
            return receipt.message
        return f"{receipt.step_id}_{receipt.status.value}"

    def _orchestration_uuid(self, value: str | UUID) -> UUID:
        if isinstance(value, UUID):
            return value
        try:
            return UUID(str(value))
        except ValueError:
            return self._stable_uuid("orchestration_run", str(value))

    def _stage_plan_uuid(self, orchestration_run_id: str | UUID, step_id: str) -> UUID:
        return self._stable_uuid(
            "stage_execution_plan", f"{self._orchestration_uuid(orchestration_run_id)}:{step_id}"
        )

    def _validation_uuid(self, orchestration_run_id: str | UUID, step_id: str) -> UUID:
        return self._stable_uuid(
            "validation_contract", f"{self._orchestration_uuid(orchestration_run_id)}:{step_id}"
        )

    def _receipt_uuid(self, orchestration_run_id: str | UUID, receipt_id: str) -> UUID:
        return self._stable_uuid(
            "stage_execution_receipt",
            f"{self._orchestration_uuid(orchestration_run_id)}:{receipt_id}",
        )

    def _stable_uuid(self, namespace: str, value: str) -> UUID:
        return uuid5(NAMESPACE_URL, f"cmf:{namespace}:{value}")

