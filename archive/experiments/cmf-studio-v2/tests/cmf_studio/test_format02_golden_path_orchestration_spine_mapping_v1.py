from pathlib import Path

from ccp_studio.contracts.orchestration import StageRunStatus
from ccp_studio.services.format02_golden_path_orchestrator_service import (
    Format02GoldenPathOrchestratorService,
)
from ccp_studio.services.golden_path_orchestration_spine_adapter_service import (
    GoldenPathOrchestrationSpineAdapterService,
)


FIXTURES_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "golden_path"


def test_format02_golden_path_maps_to_existing_orchestration_spine():
    golden_run = Format02GoldenPathOrchestratorService().run_fixture(
        fixtures_dir=FIXTURES_DIR,
        brand_id="brand_health_demo",
        brand_context_version_id="bcv_health_demo_v1",
    )
    adapter = GoldenPathOrchestrationSpineAdapterService()

    orchestration_run = adapter.map_to_orchestration_run(golden_run)
    plans = adapter.compile_stage_execution_plans(golden_run)
    validation_contracts = adapter.compile_validation_contracts(golden_run)
    receipts = adapter.compile_stage_execution_receipts(golden_run)

    assert orchestration_run.status == StageRunStatus.succeeded
    assert orchestration_run.active_object.object_type == "golden_path_run"
    assert orchestration_run.active_object.version_id is not None

    assert len(plans) == len(golden_run.stage_results) == 9
    assert len(validation_contracts) == len(plans)
    assert len(receipts) == len(golden_run.stage_results)

    plan_ids = {plan.stage_execution_plan_id for plan in plans}
    assert all(plan.orchestration_run_id == orchestration_run.orchestration_run_id for plan in plans)
    assert all(contract.stage_execution_plan_id in plan_ids for contract in validation_contracts)
    assert all(receipt.stage_execution_plan_id in plan_ids for receipt in receipts)
    assert all(receipt.orchestration_run_id == orchestration_run.orchestration_run_id for receipt in receipts)

    assert all("call_provider" in plan.blocked_actions for plan in plans)
    assert all("call_remotion" in plan.blocked_actions for plan in plans)
    assert all("call_ffmpeg" in plan.blocked_actions for plan in plans)
    assert all("create_second_harness" in plan.blocked_actions for plan in plans)

    all_contract_failures = {
        failure
        for contract in validation_contracts
        for failure in contract.failure_criteria
    }
    assert "missing_brand_context_version_id" in all_contract_failures
    assert "missing_source_span_refs" in all_contract_failures
    assert "composition_not_locked" in all_contract_failures
    assert "avatar_lipsync_detected" in all_contract_failures
    assert "fake_render_hash_missing" in all_contract_failures
    assert "export_not_approved" in all_contract_failures

    evidence_refs = {ref for receipt in receipts for ref in receipt.evidence_refs}
    assert "brand_context_version_id:bcv_health_demo_v1" in evidence_refs
    assert any(ref.startswith("source_span_ref:") for ref in evidence_refs)
    assert any(ref.startswith("video_timeline:") for ref in evidence_refs)
    assert any(ref.startswith("proxy_render:") for ref in evidence_refs)
    assert any(ref.startswith("final_render:") for ref in evidence_refs)
    assert any(ref.startswith("export_pack:") for ref in evidence_refs)

    export_receipt = next(
        receipt
        for receipt in receipts
        if receipt.output_object.object_type == "golden_path.export_compile.output"
    )
    assert export_receipt.status == StageRunStatus.succeeded
    assert export_receipt.output_object.version_id == orchestration_run.active_object.version_id


def test_golden_path_spine_mapping_bundle_is_deterministic():
    golden_run = Format02GoldenPathOrchestratorService().run_fixture(
        fixtures_dir=FIXTURES_DIR
    )
    adapter = GoldenPathOrchestrationSpineAdapterService()

    first = adapter.map_to_spine_bundle(golden_run)
    second = adapter.map_to_spine_bundle(golden_run)

    assert first["orchestration_run"].orchestration_run_id == second["orchestration_run"].orchestration_run_id
    assert [
        plan.stage_execution_plan_id for plan in first["stage_execution_plans"]
    ] == [
        plan.stage_execution_plan_id for plan in second["stage_execution_plans"]
    ]
    assert [
        receipt.receipt_id for receipt in first["stage_execution_receipts"]
    ] == [
        receipt.receipt_id for receipt in second["stage_execution_receipts"]
    ]
