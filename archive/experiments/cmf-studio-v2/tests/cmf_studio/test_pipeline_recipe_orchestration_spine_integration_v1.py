from ccp_studio.contracts.orchestration import StageExecutionPlan, ValidationContract
from ccp_studio.contracts.studio_pipeline_recipe_harness import PipelineRecipeId, PipelineRunStatus
from ccp_studio.services.pipeline_orchestration_spine_adapter_service import (
    PipelineOrchestrationSpineAdapterService,
)
from ccp_studio.services.pipeline_recipe_catalog_service import PipelineRecipeCatalogService
from ccp_studio.services.pipeline_run_service import PipelineRunService


def test_pipeline_recipe_maps_to_existing_spine_contracts():
    recipe = PipelineRecipeCatalogService().get_recipe(PipelineRecipeId.FORMAT02_GOLDEN_PATH)
    adapter = PipelineOrchestrationSpineAdapterService()
    binding = adapter.compile_binding(recipe, "orch_recipe_mapping_1")
    plans = adapter.compile_stage_execution_plans(recipe, binding.orchestration_run_id)
    validation_contracts = adapter.compile_validation_contracts(recipe, binding.orchestration_run_id)

    assert binding.spine_available is True
    assert len(plans) == len(recipe.steps)
    assert len(validation_contracts) == len(recipe.steps)
    assert all(isinstance(plan, StageExecutionPlan) for plan in plans)
    assert all(isinstance(contract, ValidationContract) for contract in validation_contracts)
    assert {plan.stage_execution_plan_id for plan in plans} == {
        contract.stage_execution_plan_id for contract in validation_contracts
    }
    assert all("create_parallel_harness" in plan.blocked_actions for plan in plans)
    assert all("call_provider" in plan.blocked_actions for plan in plans)
    assert all("call_renderer" in plan.blocked_actions for plan in plans)
    assert all("call_local_render_worker" in plan.blocked_actions for plan in plans)


def test_active_pipeline_run_requires_orchestration_run_id():
    recipe = PipelineRecipeCatalogService().get_recipe(PipelineRecipeId.FORMAT02_GOLDEN_PATH)
    blocked = PipelineRunService().create_run(
        recipe=recipe,
        brand_context_version_id="bcv_recipe_mapping_v1",
    )
    planned = PipelineRunService().create_run(
        recipe=recipe,
        brand_context_version_id="bcv_recipe_mapping_v1",
        orchestration_run_id="orch_recipe_mapping_1",
    )

    assert blocked.status == PipelineRunStatus.BLOCKED
    assert blocked.blockers[0].code == "missing_orchestration_spine_binding"
    assert planned.status == PipelineRunStatus.PLANNED
    assert planned.orchestration_run_id


def test_pipeline_recipe_adapter_emits_request_dicts_without_new_engine():
    recipe = PipelineRecipeCatalogService().get_recipe(PipelineRecipeId.FORMAT02_GOLDEN_PATH)
    requests = PipelineOrchestrationSpineAdapterService().compile_stage_plan_requests(
        recipe,
        "orch_recipe_mapping_1",
    )

    assert len(requests) == len(recipe.steps)
    assert requests[0]["pipeline_recipe_id"] == "format02_golden_path"
    assert requests[0]["stage_execution_plan_id"]
    assert requests[0]["validation_contract_id"]
    assert "new_engine" not in requests[0]

