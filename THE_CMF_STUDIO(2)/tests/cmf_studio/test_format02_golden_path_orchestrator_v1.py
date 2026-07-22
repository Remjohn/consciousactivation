from pathlib import Path

import pytest

from ccp_studio.contracts.golden_path_orchestrator import GoldenPathStatus, Format02GoldenPathInput
from ccp_studio.services.format02_golden_path_orchestrator_service import Format02GoldenPathOrchestratorService


FIXTURES_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "golden_path"


def test_health_myth_format02_golden_path_runs_source_to_fake_export():
    run = Format02GoldenPathOrchestratorService().run_fixture(
        fixtures_dir=FIXTURES_DIR,
        brand_id="brand_health_demo",
        brand_context_version_id="bcv_health_demo_v1",
    )

    assert run.status == GoldenPathStatus.PASS
    assert run.input.brand_context_version_id == "bcv_health_demo_v1"
    assert run.output.brand_context_version_id == "bcv_health_demo_v1"

    # source refs persist
    assert run.output.source_span_refs
    assert run.input.source_span_refs

    # stages
    assert len(run.stage_results) == 9
    assert all(stage.status == GoldenPathStatus.PASS for stage in run.stage_results)

    # 8 scene programs and locked compositions
    assert len(run.output.scene_program_ids) == 8
    assert len(run.output.composition_decision_receipt_ids) == 8
    assert run.output.composition_locked_count == 8

    # avatar and audience proxy plans
    assert len(run.output.avatar_performance_plan_ids) == 8
    assert len(run.output.audience_proxy_plan_ids) == 8
    assert run.output.no_lip_sync is True

    avatar_stage = next(stage for stage in run.stage_results if stage.stage_name.value == "avatar_plans_compile")
    assert avatar_stage.output_refs["no_lip_sync"] is True
    assert len(avatar_stage.output_refs["proxy_sfl_functions"]) == 8
    assert all(avatar_stage.output_refs["proxy_sfl_functions"])

    # video timeline and render artifacts
    assert run.output.video_timeline_program_id
    assert run.output.remotion_input_props_id
    assert run.output.otio_audit_timeline_id
    assert run.output.proxy_render_receipt_id
    assert run.output.evaluation_receipt_id
    assert run.output.final_render_receipt_id
    assert run.output.approval_packet_id
    assert run.output.export_pack_id

    # fake render only
    assert run.output.fake_render_only is True

    # object spine mapping preserves PRD object intent
    assert run.object_spine_map.brand_context_version_id == "bcv_health_demo_v1"
    assert len(run.object_spine_map.scene_spec_refs) == 8
    assert len(run.object_spine_map.composition_job_refs) == 8
    assert len(run.object_spine_map.render_output_refs) == 2
    assert run.object_spine_map.evaluation_receipt_refs
    assert run.object_spine_map.approval_event_refs

    # receipt passes
    assert run.receipt.pass_status == GoldenPathStatus.PASS
    assert run.receipt.output_id == run.output.format02_golden_path_output_id


def test_golden_path_fixture_requires_8_scene_seeds():
    service = Format02GoldenPathOrchestratorService()
    golden_input = service.load_fixture_input(fixtures_dir=FIXTURES_DIR)
    data = golden_input.model_dump() if hasattr(golden_input, "model_dump") else golden_input.dict()
    data["scene_seeds"] = data["scene_seeds"][:7]
    with pytest.raises(Exception):
        Format02GoldenPathInput(**data)


def test_golden_path_input_requires_brand_context_version():
    service = Format02GoldenPathOrchestratorService()
    golden_input = service.load_fixture_input(fixtures_dir=FIXTURES_DIR)
    data = golden_input.model_dump() if hasattr(golden_input, "model_dump") else golden_input.dict()
    data["brand_context_version_id"] = ""
    with pytest.raises(Exception):
        Format02GoldenPathInput(**data)


def test_golden_path_output_records_authorized_format_program():
    run = Format02GoldenPathOrchestratorService().run_fixture(fixtures_dir=FIXTURES_DIR)
    assert run.output.format_program_id
    assert run.output.format_program_authorized is True
