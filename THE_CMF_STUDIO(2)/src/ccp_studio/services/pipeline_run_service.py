from ccp_studio.contracts.studio_pipeline_recipe_harness import PipelineRun, PipelineRunBlocker, PipelineRunStatus, PipelineStepRun, PipelineStepStatus
from ccp_studio.repositories.studio_pipeline_recipe_harness import InMemoryPipelineRecipeHarnessRepository
class PipelineRunService:
    def __init__(self, repository=None): self.repository = repository or InMemoryPipelineRecipeHarnessRepository()
    def create_run(self, recipe, brand_context_version_id: str, workspace_id=None, orchestration_run_id=None, input_artifacts=None):
        step_runs=[PipelineStepRun(step_id=s.step_id, step_kind=s.step_kind, status=PipelineStepStatus.PLANNED, depends_on_step_ids=list(s.depends_on), approval_gate_id=s.approval_gate_id, orchestration_stage_execution_id=f'{orchestration_run_id}:{s.orchestration_stage_ref}' if orchestration_run_id and s.orchestration_stage_ref else None) for s in recipe.steps]
        blockers=[]; status=PipelineRunStatus.PLANNED
        if recipe.reuse_orchestration_spine and not orchestration_run_id:
            blockers.append(PipelineRunBlocker(code='missing_orchestration_spine_binding', message='PipelineRun requires orchestration_run_id to reuse existing orchestration spine.')); status=PipelineRunStatus.BLOCKED
        run=PipelineRun(recipe_id=recipe.recipe_id, recipe_version=recipe.version, brand_context_version_id=brand_context_version_id, workspace_id=workspace_id, orchestration_run_id=orchestration_run_id, status=status, input_artifacts=input_artifacts or [], step_runs=step_runs, approval_gates=recipe.approval_gates, blockers=blockers, reuse_orchestration_spine=recipe.reuse_orchestration_spine)
        self.repository.upsert('runs', run.pipeline_run_id, run); return run
