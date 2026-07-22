import pytest
from ccp_studio.contracts.studio_pipeline_recipe_harness import *
from ccp_studio.services.pipeline_approval_gate_service import PipelineApprovalGateService
from ccp_studio.services.pipeline_artifact_ref_service import PipelineArtifactRefService
from ccp_studio.services.pipeline_orchestration_spine_adapter_service import PipelineOrchestrationSpineAdapterService
from ccp_studio.services.pipeline_recipe_catalog_service import PipelineRecipeCatalogService
from ccp_studio.services.pipeline_run_service import PipelineRunService
from ccp_studio.services.pipeline_run_summary_service import PipelineRunSummaryService
from ccp_studio.services.pipeline_step_run_service import PipelineStepRunService

def test_catalog_contains_five_canonical_recipes():
    assert {r.recipe_id for r in PipelineRecipeCatalogService().compile_catalog().recipes} == set(PipelineRecipeId)
def test_recipes_reuse_orchestration_spine():
    for r in PipelineRecipeCatalogService().compile_catalog().recipes:
        assert r.reuse_orchestration_spine is True
        assert all(s.orchestration_stage_ref for s in r.steps)
def test_recipe_rejects_duplicate_step_ids():
    with pytest.raises(Exception): PipelineRecipe(recipe_id=PipelineRecipeId.CAROUSEL_FROM_EXPRESSION_MOMENT, display_name='Bad', description='Bad', steps=[PipelineRecipeStep(step_id='x',display_name='X',step_kind=PipelineStepKind.SOURCE_INTAKE),PipelineRecipeStep(step_id='x',display_name='X2',step_kind=PipelineStepKind.QA)])
def test_recipe_rejects_missing_dependency():
    with pytest.raises(Exception): PipelineRecipe(recipe_id=PipelineRecipeId.CAROUSEL_FROM_EXPRESSION_MOMENT, display_name='Bad', description='Bad', steps=[PipelineRecipeStep(step_id='x',display_name='X',step_kind=PipelineStepKind.QA,depends_on=['missing'])])
def test_pipeline_run_requires_brand_context_version_id():
    with pytest.raises(Exception): PipelineRun(recipe_id=PipelineRecipeId.FORMAT02_GOLDEN_PATH, recipe_version='1.0.0', brand_context_version_id='')
def test_create_run_without_orchestration_binding_blocks():
    recipe=PipelineRecipeCatalogService().get_recipe(PipelineRecipeId.FORMAT02_GOLDEN_PATH); run=PipelineRunService().create_run(recipe=recipe, brand_context_version_id='bcv_1')
    assert run.status == PipelineRunStatus.BLOCKED and run.blockers[0].code == 'missing_orchestration_spine_binding'
def test_create_run_with_orchestration_binding_is_planned():
    recipe=PipelineRecipeCatalogService().get_recipe(PipelineRecipeId.FORMAT02_GOLDEN_PATH); run=PipelineRunService().create_run(recipe=recipe, brand_context_version_id='bcv_1', orchestration_run_id='orch_1')
    assert run.status == PipelineRunStatus.PLANNED and all(s.orchestration_stage_execution_id for s in run.step_runs)
def test_step_cannot_complete_before_dependencies():
    r=PipelineRecipeCatalogService().get_recipe(PipelineRecipeId.FORMAT02_GOLDEN_PATH); run=PipelineRunService().create_run(recipe=r, brand_context_version_id='bcv_1', orchestration_run_id='orch_1')
    receipt=PipelineStepRunService().complete_step(run, step_id='format_intelligence')
    assert receipt.pass_status == PassStatus.FAIL and receipt.blockers[0].code == 'dependencies_not_satisfied'
def test_step_completion_succeeds_after_dependencies():
    r=PipelineRecipeCatalogService().get_recipe(PipelineRecipeId.FORMAT02_GOLDEN_PATH); run=PipelineRunService().create_run(recipe=r, brand_context_version_id='bcv_1', orchestration_run_id='orch_1'); svc=PipelineStepRunService()
    assert svc.complete_step(run, step_id='source_intake').pass_status == PassStatus.PASS
    assert svc.complete_step(run, step_id='narrative_story_doctor').pass_status == PassStatus.PASS
def test_approval_gate_requires_approved_by():
    with pytest.raises(Exception): PipelineApprovalGate(gate_id='g', gate_type=PipelineApprovalGateType.OPERATOR_APPROVAL, status=PipelineApprovalStatus.APPROVED)
def test_sample_first_gate_requires_all_samples():
    gate=PipelineApprovalGate(gate_id='sample', gate_type=PipelineApprovalGateType.SAMPLE_FIRST, required_sample_types=['scene_sample','face_plate_sample','template_preview_sample'], approved_sample_types=['scene_sample'])
    with pytest.raises(Exception): PipelineApprovalGateService().approve(gate, approved_by='operator', approved_sample_types=['scene_sample'])
def test_gated_step_blocks_until_gate_approved():
    r=PipelineRecipeCatalogService().get_recipe(PipelineRecipeId.FORMAT02_GOLDEN_PATH); run=PipelineRunService().create_run(recipe=r, brand_context_version_id='bcv_1', orchestration_run_id='orch_1'); svc=PipelineStepRunService()
    for sid in ['source_intake','narrative_story_doctor','format_intelligence','format02_composition','avatar_assets']: svc.complete_step(run, step_id=sid)
    receipt=svc.complete_step(run, step_id='provider_samples'); assert receipt.pass_status == PassStatus.FAIL and 'approval_gate_not_approved' in [b.code for b in receipt.blockers]
def test_gated_step_succeeds_after_gate_approved():
    r=PipelineRecipeCatalogService().get_recipe(PipelineRecipeId.FORMAT02_GOLDEN_PATH); run=PipelineRunService().create_run(recipe=r, brand_context_version_id='bcv_1', orchestration_run_id='orch_1'); gate=next(g for g in run.approval_gates if g.gate_id=='provider_sample_first')
    run.approval_gates=[PipelineApprovalGateService().approve(gate, approved_by='operator') if g.gate_id==gate.gate_id else g for g in run.approval_gates]
    svc=PipelineStepRunService()
    for sid in ['source_intake','narrative_story_doctor','format_intelligence','format02_composition','avatar_assets']: svc.complete_step(run, step_id=sid)
    assert svc.complete_step(run, step_id='provider_samples').pass_status == PassStatus.PASS
def test_step_receipt_cannot_pass_with_blockers():
    with pytest.raises(Exception): PipelineStepReceipt(pipeline_step_run_id='sr', step_id='s', status=PipelineStepStatus.BLOCKED, pass_status=PassStatus.PASS, blockers=[{'code':'blocked','message':'blocked'}])
def test_artifact_ref_pointer_and_materialized_rules():
    p=PipelineArtifactRefService().pointer(role=PipelineArtifactRole.SOURCE_REF, uri='artifact://source'); assert p.storage_state == PipelineArtifactStorageState.POINTER_ONLY
    with pytest.raises(Exception): PipelineArtifactRefService().materialized(role=PipelineArtifactRole.RENDER_OUTPUT, uri='file://render.mp4', sha256='')
def test_summary_surfaces_pending_approvals_and_next_step():
    r=PipelineRecipeCatalogService().get_recipe(PipelineRecipeId.FORMAT02_GOLDEN_PATH); run=PipelineRunService().create_run(recipe=r, brand_context_version_id='bcv_1', orchestration_run_id='orch_1'); s=PipelineRunSummaryService().summarize(run)
    assert s.pending_approval_count == 2 and s.next_step_id == 'source_intake'
def test_orchestration_spine_adapter_compiles_stage_plan_requests():
    r=PipelineRecipeCatalogService().get_recipe(PipelineRecipeId.FORMAT02_GOLDEN_PATH); req=PipelineOrchestrationSpineAdapterService().compile_stage_plan_requests(recipe=r, orchestration_run_id='orch_1')
    assert len(req) == len(r.steps) and req[0]['pipeline_recipe_id'] == PipelineRecipeId.FORMAT02_GOLDEN_PATH.value
def test_avatar_library_recipe_has_batch_step_behind_sample_gate():
    r=PipelineRecipeCatalogService().get_recipe(PipelineRecipeId.AVATAR_LIBRARY_GENERATION); b=next(s for s in r.steps if s.step_id=='avatar_batch_generation')
    assert b.step_kind == PipelineStepKind.PROVIDER_BATCH and b.approval_gate_id == 'avatar_sample_first'
def test_format01_story_video_recipe_preserves_story_spine():
    r=PipelineRecipeCatalogService().get_recipe(PipelineRecipeId.FORMAT01_STORY_VIDEO); assert r.steps[0].step_id == 'source_intake' and any(s.step_id=='story_video_plan' for s in r.steps)
def test_supervisual_and_carousel_start_from_expression_moment():
    c=PipelineRecipeCatalogService()
    for rid in [PipelineRecipeId.SUPERVISUAL_FROM_EXPRESSION_MOMENT, PipelineRecipeId.CAROUSEL_FROM_EXPRESSION_MOMENT]: assert c.get_recipe(rid).steps[0].step_id == 'expression_moment_input'
