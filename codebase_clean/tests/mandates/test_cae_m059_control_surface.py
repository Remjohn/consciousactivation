"""Executable M0059 evidence: product control operations remain authoritative and receipt-backed."""

from __future__ import annotations

import sys
import types
from pathlib import Path

# The supplied brownfield bundle is intentionally not a fully installed distribution.
# Bypass ca_runtime.__init__ so these mandate tests exercise the scoped runtime modules
# without importing unrelated optional products.
if "ca_runtime" not in sys.modules:
    ca_runtime_pkg = types.ModuleType("ca_runtime")
    ca_runtime_pkg.__path__ = [str(Path(__file__).resolve().parents[2] / "packages" / "ca_runtime" / "src" / "ca_runtime")]
    sys.modules["ca_runtime"] = ca_runtime_pkg

import pytest

from ca_runtime.pi_adapter import AuthorityLane
from ca_runtime.program_operator_runtime import ProgramOperatorRuntimeService
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_state_runtime import (
    InMemoryProgramStateStore,
    ProgramAuthorityLaneViolationError,
    ProgramStateLifecycle,
    UniversalProgramStateRuntime,
)


def _service() -> ProgramOperatorRuntimeService:
    registry = ProgramRegistry(discovery_roots=[Path("programs").resolve()])
    registry.discover()
    runtime = UniversalProgramStateRuntime(
        store=InMemoryProgramStateStore(),
        program_registry=registry,
    )
    return ProgramOperatorRuntimeService(runtime=runtime, program_registry=registry)


def test_m059_run_inspect_pause_resume_and_receipts_are_authoritative() -> None:
    service = _service()
    aggregate = service.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-m059",
        actor_id="commander-m059",
    )

    assert aggregate.lifecycle is ProgramStateLifecycle.RUNNING
    assert aggregate.version == 1
    assert aggregate.last_receipt_id

    inspected, context = service.get_execution(aggregate.aggregate_id)
    assert inspected.lifecycle is ProgramStateLifecycle.RUNNING
    assert context.aggregate.version == aggregate.version

    running_receipts = service.get_execution_receipts(aggregate.aggregate_id)
    assert [receipt.operation for receipt in running_receipts][:2] == ["REGISTER", "RUN"]
    assert running_receipts[1].receipt_id == aggregate.last_receipt_id
    assert running_receipts[1].version_after == 1

    paused = service.pause_program(
        aggregate_id=aggregate.aggregate_id,
        actor_id="commander-m059",
        actor_lane=AuthorityLane.COMMANDER,
        expected_version=aggregate.version,
        expected_state_sha256=aggregate.state_hash,
    )
    assert paused.lifecycle is ProgramStateLifecycle.PAUSED
    assert paused.version == aggregate.version + 1

    receipts_after_pause = service.get_execution_receipts(aggregate.aggregate_id)
    pause_receipt = next(r for r in receipts_after_pause if r.receipt_id == paused.last_receipt_id)
    assert pause_receipt.operation == "PAUSE"
    assert pause_receipt.source_lifecycle == "RUNNING"
    assert pause_receipt.target_lifecycle == "PAUSED"
    assert pause_receipt.version_before == aggregate.version
    assert pause_receipt.version_after == paused.version

    resumed = service.resume_program(
        aggregate_id=aggregate.aggregate_id,
        actor_id="commander-m059",
        actor_lane=AuthorityLane.COMMANDER,
        expected_version=paused.version,
        expected_state_sha256=paused.state_hash,
    )
    assert resumed.lifecycle is ProgramStateLifecycle.RUNNING
    assert resumed.version == paused.version + 1

    receipts_after_resume = service.get_execution_receipts(aggregate.aggregate_id)
    resume_receipt = next(r for r in receipts_after_resume if r.receipt_id == resumed.last_receipt_id)
    assert resume_receipt.operation == "RESUME"
    assert resume_receipt.source_lifecycle == "PAUSED"
    assert resume_receipt.target_lifecycle == "RUNNING"
    assert resume_receipt.version_before == paused.version
    assert resume_receipt.version_after == resumed.version

    # False-proof countercase: a caller must not be able to claim a receipt that
    # was never persisted or reconstructable from the canonical runtime ledger.
    assert service.get_execution_receipts(
        aggregate.aggregate_id, receipt_id="rcpt_never_committed"
    ) == []


def test_m059_pause_rejects_non_commander_lane_without_state_change() -> None:
    service = _service()
    aggregate = service.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-m059-auth",
        actor_id="commander-m059",
    )

    with pytest.raises(ProgramAuthorityLaneViolationError) as exc_info:
        service.pause_program(
            aggregate_id=aggregate.aggregate_id,
            actor_id="hunter-m059",
            actor_lane=AuthorityLane.HUNTER,
            expected_version=aggregate.version,
            expected_state_sha256=aggregate.state_hash,
        )

    assert "AUTHORITY" in str(exc_info.value).upper()
    unchanged = service.runtime.get_aggregate(aggregate.aggregate_id)
    assert unchanged.lifecycle is ProgramStateLifecycle.RUNNING
    assert unchanged.version == aggregate.version


def test_m059_failure_surface_uses_persisted_authoritative_failure() -> None:
    service = _service()
    aggregate = service.run_program(
        program_id="interview_semantic_program",
        workspace_id="ws-m059-failure",
        actor_id="commander-m059",
    )

    failed = service.runtime.set_lifecycle(
        aggregate_id=aggregate.aggregate_id,
        new_lifecycle=ProgramStateLifecycle.FAILED,
        actor_id="runtime-failure",
        expected_version=aggregate.version,
        expected_state_sha256=aggregate.state_hash,
        state_updates={
            "failure": {
                "error_code": "WORKER_EXECUTION_FAILED",
                "failure_reason": "Fixture worker failed before downstream dispatch.",
                "worker_id": "fixture-worker-1",
            }
        },
    )

    projection = service.get_execution_failure(failed.aggregate_id)
    assert projection.failed is True
    assert projection.lifecycle is ProgramStateLifecycle.FAILED
    assert projection.error_code == "WORKER_EXECUTION_FAILED"
    assert projection.failure_reason == "Fixture worker failed before downstream dispatch."
    assert projection.receipt_id == failed.last_receipt_id
    assert projection.details["worker_id"] == "fixture-worker-1"
    assert failed.lifecycle is ProgramStateLifecycle.FAILED


def test_m059_receipts_survive_sqlite_reload() -> None:
    from tempfile import TemporaryDirectory

    from ca_runtime.program_state_runtime import SqliteProgramStateStore

    registry = ProgramRegistry(discovery_roots=[Path("programs").resolve()])
    registry.discover()

    with TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "m059.db"
        runtime = UniversalProgramStateRuntime(
            store=SqliteProgramStateStore(db_path),
            program_registry=registry,
        )
        service = ProgramOperatorRuntimeService(runtime=runtime, program_registry=registry)
        aggregate = service.run_program(
            program_id="interview_semantic_program",
            workspace_id="ws-m059-sqlite",
            actor_id="commander-m059",
        )
        paused = service.pause_program(
            aggregate_id=aggregate.aggregate_id,
            actor_id="commander-m059",
            expected_version=aggregate.version,
            expected_state_sha256=aggregate.state_hash,
        )

        restored_runtime = UniversalProgramStateRuntime(
            store=SqliteProgramStateStore(db_path),
            program_registry=registry,
        )
        restored_service = ProgramOperatorRuntimeService(
            runtime=restored_runtime,
            program_registry=registry,
        )
        restored = restored_runtime.get_aggregate(paused.aggregate_id)
        assert restored.lifecycle is ProgramStateLifecycle.PAUSED
        receipt_ids = {receipt.receipt_id for receipt in restored_service.get_execution_receipts(paused.aggregate_id)}
        assert paused.last_receipt_id in receipt_ids


def test_m059_api_control_surface_publishes_state_failure_and_receipts() -> None:
    import importlib
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    # Isolate the scoped router from optional product wiring absent from the bundle.
    cmf_application = types.ModuleType("cmf_pipeline.application")
    cmf_application.PipelineApplication = type("PipelineApplication", (), {})
    sys.modules.setdefault("cmf_pipeline", types.ModuleType("cmf_pipeline"))
    sys.modules["cmf_pipeline.application"] = cmf_application

    deps = types.ModuleType("api.dependencies")
    for name in ("get_air", "get_campaign_repository", "get_interview", "get_pipeline", "get_studio_bridge"):
        setattr(deps, name, lambda: None)
    sys.modules["api.dependencies"] = deps

    harnesses = types.ModuleType("api.routers.harnesses")
    harnesses.find_by_definition_id = lambda *args, **kwargs: None
    harnesses.get_harness_library_root = lambda: None
    sys.modules["api.routers.harnesses"] = harnesses

    programs_router = importlib.import_module("api.routers.programs")
    service = _service()
    app = FastAPI()
    app.include_router(programs_router.router, prefix="/api/programs")
    app.dependency_overrides[programs_router.get_operator_service] = lambda: service
    client = TestClient(app)
    try:
        started = client.post(
            "/api/programs/executions",
            json={
                "program_id": "interview_semantic_program",
                "workspace_id": "ws-m059-api",
                "actor_id": "commander-api",
            },
        )
        assert started.status_code == 201, started.text
        payload = started.json()
        aggregate_id = payload["aggregate_id"]

        receipts = client.get(f"/api/programs/executions/{aggregate_id}/receipts")
        assert receipts.status_code == 200, receipts.text
        receipt_data = receipts.json()
        assert receipt_data["total"] >= 2
        assert {item["operation"] for item in receipt_data["receipts"]} >= {"REGISTER", "RUN"}

        state = client.get(f"/api/programs/executions/{aggregate_id}")
        assert state.status_code == 200
        assert state.json()["aggregate"]["lifecycle"] == "RUNNING"

        missing_receipt = client.get(
            f"/api/programs/executions/{aggregate_id}/receipts/rcpt_never_committed"
        )
        assert missing_receipt.status_code == 404
        assert missing_receipt.json()["detail"]["error_code"] == "RECEIPT_NOT_FOUND"

        failed = service.runtime.set_lifecycle(
            aggregate_id=aggregate_id,
            new_lifecycle=ProgramStateLifecycle.FAILED,
            actor_id="fixture-worker",
            expected_version=payload["version"],
            expected_state_sha256=payload["state_hash"],
            state_updates={
                "failure": {
                    "error_code": "FIXTURE_FAILURE",
                    "failure_reason": "Controlled M0059 failure fixture.",
                }
            },
        )
        assert failed.lifecycle is ProgramStateLifecycle.FAILED

        failure = client.get(f"/api/programs/executions/{aggregate_id}/failure")
        assert failure.status_code == 200, failure.text
        failure_data = failure.json()
        assert failure_data["failed"] is True
        assert failure_data["lifecycle"] == "FAILED"
        assert failure_data["error_code"] == "FIXTURE_FAILURE"

        blocked_resume = client.post(
            f"/api/programs/executions/{aggregate_id}/resume",
            json={
                "actor_id": "commander-api",
                "expected_version": failed.version,
                "expected_state_sha256": failed.state_hash,
            },
        )
        assert blocked_resume.status_code == 400
        assert blocked_resume.json()["detail"]["error_code"] == "TRANSITION_BLOCKED"
        # Terminal failure stays terminal: the control surface cannot paper over
        # authoritative runtime failure with a UI-only RUNNING state.
    finally:
        app.dependency_overrides.clear()


def test_m059_campaign_control_is_read_only_and_does_not_fake_launch_or_pause() -> None:
    import importlib
    import sys

    cmf_application = types.ModuleType("cmf_pipeline.application")
    cmf_application.PipelineApplication = type("PipelineApplication", (), {})
    sys.modules.setdefault("cmf_pipeline", types.ModuleType("cmf_pipeline"))
    sys.modules["cmf_pipeline.application"] = cmf_application

    deps = types.ModuleType("api.dependencies")
    for name in ("get_air", "get_campaign_repository", "get_interview", "get_pipeline", "get_studio_bridge"):
        setattr(deps, name, lambda: None)
    sys.modules["api.dependencies"] = deps

    harnesses = types.ModuleType("api.routers.harnesses")
    harnesses.find_by_definition_id = lambda *args, **kwargs: None
    harnesses.get_harness_library_root = lambda: None
    sys.modules["api.routers.harnesses"] = harnesses

    projection = types.ModuleType("api.services.campaign_projection")
    projection.CampaignNotFound = type("CampaignNotFound", (RuntimeError,), {})
    projection.load_campaign = lambda *args, **kwargs: {}
    sys.modules["api.services.campaign_projection"] = projection

    studio_bridge = types.ModuleType("api.services.studio_bridge")
    studio_bridge.StudioBridge = type("StudioBridge", (), {})
    studio_bridge.StudioBridgeError = type("StudioBridgeError", (RuntimeError,), {})
    studio_bridge.StudioBridgeCrash = type("StudioBridgeCrash", (RuntimeError,), {})
    sys.modules["api.services.studio_bridge"] = studio_bridge

    campaigns_router = importlib.import_module("api.routers.campaigns")

    class FakeRepository:
        def get(self, campaign_id: str) -> dict:
            return {
                "order": {
                    "workspace_id": "ws-m059-campaign",
                    "project_id": "project-m059",
                    "authority": {"authority_state": "candidate_not_current"},
                    "operator_actor": {"actor_id": "operator-m059"},
                },
                "state": {
                    "campaign_id": campaign_id,
                    "lifecycle_state": "LAUNCHED",
                    "version": 1,
                    "active_checkpoint_id": None,
                    "run_refs": [],
                    "artifact_refs": [],
                    "evaluation_refs": [],
                    "exception_ids": [],
                },
            }

    projection = campaigns_router.get_campaign_control_surface(
        "campaign-m059",
        repository=FakeRepository(),
    )
    assert projection["lifecycle_state"] == "LAUNCHED"
    assert projection["version"] == 1
    assert projection["capabilities"]["launch"] is False
    assert projection["capabilities"]["pause"] is False
    assert projection["capabilities"]["resume"] is False
    assert "does not invent a second launch transition" in projection["launch_note"]
