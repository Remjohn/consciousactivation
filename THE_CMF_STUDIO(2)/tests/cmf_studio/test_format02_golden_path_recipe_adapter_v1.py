from pathlib import Path

from ccp_studio.contracts.studio_pipeline_recipe_harness import (
    PipelineArtifactStorageState,
    PipelineRecipeId,
    PipelineRunStatus,
)
from ccp_studio.services.format02_golden_path_orchestrator_service import (
    Format02GoldenPathOrchestratorService,
)
from ccp_studio.services.format02_golden_path_recipe_adapter_service import (
    Format02GoldenPathRecipeAdapterService,
)


FIXTURES_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "golden_path"


def test_format02_golden_path_projects_to_pipeline_run_summary():
    golden_run = Format02GoldenPathOrchestratorService().run_fixture(
        fixtures_dir=FIXTURES_DIR,
        brand_id="brand_health_demo",
        brand_context_version_id="bcv_health_demo_v1",
    )

    read_model = Format02GoldenPathRecipeAdapterService().to_read_model(golden_run)
    pipeline_run = read_model["pipeline_run"]
    summary = read_model["summary"]

    assert pipeline_run.recipe_id == PipelineRecipeId.FORMAT02_GOLDEN_PATH
    assert pipeline_run.brand_context_version_id == "bcv_health_demo_v1"
    assert pipeline_run.orchestration_run_id
    assert pipeline_run.status == PipelineRunStatus.SUCCEEDED
    assert summary.recipe_id == PipelineRecipeId.FORMAT02_GOLDEN_PATH
    assert summary.succeeded_steps == summary.total_steps
    assert read_model["provider_calls_executed"] is False
    assert read_model["renderer_calls_executed"] is False
    assert read_model["local_worker_calls_executed"] is False


def test_format02_golden_path_adapter_preserves_pointer_artifacts():
    golden_run = Format02GoldenPathOrchestratorService().run_fixture(
        fixtures_dir=FIXTURES_DIR,
        brand_id="brand_health_demo",
        brand_context_version_id="bcv_health_demo_v1",
    )

    pipeline_run = Format02GoldenPathRecipeAdapterService().to_pipeline_run(golden_run)
    uris = {artifact.uri for artifact in pipeline_run.input_artifacts}

    assert all(
        artifact.storage_state == PipelineArtifactStorageState.POINTER_ONLY
        for artifact in pipeline_run.input_artifacts
    )
    assert any(uri.startswith("golden_path://source_span/") for uri in uris)
    assert f"golden_path://video_timeline/{golden_run.output.video_timeline_program_id}" in uris
    assert f"golden_path://proxy_render/{golden_run.output.proxy_render_receipt_id}" in uris
    assert f"golden_path://export_pack/{golden_run.output.export_pack_id}" in uris
    assert all(golden_run.input.source_span_refs[0] in artifact.source_ref_ids for artifact in pipeline_run.input_artifacts)

