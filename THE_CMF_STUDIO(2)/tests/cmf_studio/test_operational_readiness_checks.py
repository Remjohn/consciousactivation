from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.operational_readiness import ReadinessCheckType, ReadinessOverallStatus  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.operational_readiness_service import (  # noqa: E402
    FULL_BRAND_CYCLE_STAGE_REFS,
    OperationalReadinessService,
    register_operational_readiness_command_handlers,
)
from ccp_studio.services.operations_board_service import OperationsBoardService  # noqa: E402
from ccp_studio.workflows.operations import OperationsWorkflow  # noqa: E402


def _ids():
    return uuid4(), uuid4(), uuid4()


def _service() -> OperationalReadinessService:
    return OperationalReadinessService()


def test_restore_drill_verifies_canonical_state_object_storage_receipts_and_projection_rebuild():
    service = _service()
    org_id, brand_id, actor_id = _ids()

    report = service.run_restore_drill(
        organization_id=org_id,
        brand_id=brand_id,
        triggered_by_user_id=actor_id,
        fixture_pack_id="readiness:restore",
    )

    assert report.canonical_state_verified is True
    assert report.object_storage_verified is True
    assert report.receipts_verified is True
    assert report.projection_rebuild_verified is True
    assert any(ref.startswith("object://") for ref in report.evidence_refs)
    assert any(event.event_type == "RestoreDrillCompleted" for event in service.repository.events)


def test_provider_outage_simulation_preserves_completed_artifacts_and_blocks_duplicate_side_effects():
    service = _service()
    org_id, brand_id, actor_id = _ids()

    report = service.simulate_provider_outage(
        organization_id=org_id,
        brand_id=brand_id,
        triggered_by_user_id=actor_id,
        fixture_pack_id="readiness:outage",
    )

    assert report.preserved_artifact_refs == ["sha256-readiness-partial-render"]
    assert report.requeued_work_refs == ["outage-render-2"]
    assert report.duplicate_side_effect_blocked is True
    duplicate_receipt = service.provider_recovery.repository.receipts[report.duplicate_block_receipt_id]
    assert duplicate_receipt.decision_code == "DUPLICATE_COST_RECOVERY_BLOCKED"


def test_gpu_worker_shutdown_records_drain_final_status_and_cost():
    service = _service()
    org_id, brand_id, actor_id = _ids()

    report = service.run_gpu_worker_shutdown_check(
        organization_id=org_id,
        brand_id=brand_id,
        triggered_by_user_id=actor_id,
        fixture_pack_id="readiness:gpu",
    )

    assert report.shutdown_status == "shutdown"
    assert report.final_cost_amount > 0
    assert report.gpu_cost_report_id in service.gpu_worker.repository.cost_reports
    assert any(receipt.decision_code == "GPU_WORKER_SHUTDOWN" for receipt in service.gpu_worker.repository.receipts.values())


def test_memory_rebuild_preserves_active_expired_reversed_and_quarantined_states():
    service = _service()
    org_id, brand_id, actor_id = _ids()

    report = service.run_memory_rebuild_check(
        organization_id=org_id,
        brand_id=brand_id,
        triggered_by_user_id=actor_id,
        fixture_pack_id="readiness:memory",
    )

    assert report.replay_preserved_governance_state is True
    assert len(report.active_memory_event_ids) == 1
    assert len(report.expired_memory_event_ids) == 1
    assert len(report.reversed_memory_event_ids) == 1
    assert len(report.quarantined_memory_event_ids) == 1


def test_full_brand_cycle_completes_without_manual_database_edits_and_detects_them_when_present():
    service = _service()
    org_id, brand_id, _actor_id = _ids()

    clean = service.run_complete_brand_cycle_check(
        organization_id=org_id,
        brand_id=brand_id,
        manual_database_edits_detected=False,
    )
    dirty = service.run_complete_brand_cycle_check(
        organization_id=org_id,
        brand_id=brand_id,
        manual_database_edits_detected=True,
    )

    assert clean.completed_stage_refs == FULL_BRAND_CYCLE_STAGE_REFS
    assert clean.projection_health == "healthy"
    assert clean.manual_database_edits_detected is False
    dirty_result = service._brand_cycle_result(dirty)
    assert dirty_result.passed is False
    assert "MANUAL_DATABASE_EDIT_DETECTED" in dirty_result.blocker_codes


def test_operational_readiness_suite_emits_report_receipt_and_all_required_check_results():
    service = _service()
    org_id, brand_id, actor_id = _ids()

    report = service.run_operational_readiness_suite(
        organization_id=org_id,
        brand_id=brand_id,
        triggered_by_user_id=actor_id,
        role_ids=["operator"],
        fixture_pack_id="readiness:suite",
        idempotency_key="readiness:suite:one",
    )
    replay = service.run_operational_readiness_suite(
        organization_id=org_id,
        brand_id=brand_id,
        triggered_by_user_id=actor_id,
        role_ids=["operator"],
        fixture_pack_id="readiness:suite",
        idempotency_key="readiness:suite:one",
    )

    assert report.readiness_report_id == replay.readiness_report_id
    assert report.run.overall_status == ReadinessOverallStatus.passed
    assert {result.check_type for result in report.run.results} == set(ReadinessCheckType)
    assert report.receipt.passed_check_count == 6
    assert report.receipt.failed_check_count == 0
    assert report.receipt.manual_database_edits_detected is False
    assert report.receipt.receipt_id in service.repository.receipts


def test_operations_workflow_and_command_bus_route_operational_readiness_suite():
    service = _service()
    org_id, brand_id, actor_id = _ids()
    workflow = OperationsWorkflow(OperationsBoardService(), operational_readiness_service=service)

    workflow_report = workflow.release_readiness_overlay(
        organization_id=org_id,
        brand_id=brand_id,
        triggered_by_user_id=actor_id,
        role_ids=["operator"],
        fixture_pack_id="readiness:workflow",
        idempotency_key="readiness:workflow:one",
    )
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    register_operational_readiness_command_handlers(bus, service)
    actor = ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=["operator"])
    envelope = new_command_envelope(
        command_type="RunOperationalReadinessSuiteCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        idempotency_key="readiness:command:one",
        payload={"fixture_pack_id": "readiness:command"},
    )

    first = bus.submit(envelope)
    second = bus.submit(envelope)

    assert workflow_report.run.overall_status == ReadinessOverallStatus.passed
    assert first.status == CommandStatus.succeeded
    assert second.status == CommandStatus.replayed
    assert first.result_payload["run"]["overall_status"] == "passed"
    assert first.result_payload["receipt"]["passed_check_count"] == 6
    assert bus.event_outbox.events[-1].event_type == "RunOperationalReadinessSuiteCommand.succeeded"
