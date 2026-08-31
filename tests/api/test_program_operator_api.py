"""API endpoint tests for Governed Program Operator Application (M46 / Contract 18)."""

from __future__ import annotations

from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from api.routers.programs import get_operator_service, get_registry
from ca_runtime.program_registry import ProgramRegistry
from ca_runtime.program_operator_runtime import ProgramOperatorRuntimeService
from ca_runtime.program_state_runtime import UniversalProgramStateRuntime, InMemoryProgramStateStore


@pytest.fixture
def operator_service() -> ProgramOperatorRuntimeService:
    root = Path("programs").resolve()
    reg = ProgramRegistry(discovery_roots=[root])
    reg.discover()
    runtime = UniversalProgramStateRuntime(store=InMemoryProgramStateStore())
    return ProgramOperatorRuntimeService(runtime=runtime, program_registry=reg)


def test_api_create_and_get_execution(api_app, operator_service: ProgramOperatorRuntimeService) -> None:
    api_app.dependency_overrides[get_operator_service] = lambda: operator_service
    try:
        client = TestClient(api_app)
        
        # 1. Start execution
        resp = client.post(
            "/api/programs/executions",
            json={
                "program_id": "interview_semantic_program",
                "workspace_id": "ws-tenant-01",
                "initial_data": {"guest_name": "Audrey"},
            },
        )
        assert resp.status_code == 201, resp.text
        data = resp.json()
        assert data["program_id"] == "interview_semantic_program"
        assert data["lifecycle"] == "RUNNING"
        agg_id = data["aggregate_id"]
        assert resp.headers.get("x-cae-state-version") == str(data["version"])
        assert resp.headers.get("x-cae-state-sha256") == data["state_hash"]

        # 2. Get execution detail
        get_resp = client.get(f"/api/programs/executions/{agg_id}")
        assert get_resp.status_code == 200
        get_data = get_resp.json()
        assert get_data["aggregate"]["aggregate_id"] == agg_id
        assert "allowable_transitions" in get_data

        # 3. List executions
        list_resp = client.get("/api/programs/executions?workspace_id=ws-tenant-01")
        assert list_resp.status_code == 200
        list_data = list_resp.json()
        assert list_data["total"] >= 1
        assert any(e["aggregate_id"] == agg_id for e in list_data["executions"])
    finally:
        api_app.dependency_overrides.clear()


def test_api_pause_resume_with_cas_headers(api_app, operator_service: ProgramOperatorRuntimeService) -> None:
    api_app.dependency_overrides[get_operator_service] = lambda: operator_service
    try:
        client = TestClient(api_app)

        # Create
        start_resp = client.post(
            "/api/programs/executions",
            json={"program_id": "interview_semantic_program", "workspace_id": "ws-01"},
        )
        assert start_resp.status_code == 201, start_resp.text
        agg_id = start_resp.json()["aggregate_id"]
        v1 = start_resp.json()["version"]
        hash1 = start_resp.json()["state_hash"]

        # CAS Conflict test: mismatch version
        bad_pause = client.post(
            f"/api/programs/executions/{agg_id}/pause",
            headers={"if-match-state-version": "999", "if-match-state-sha256": hash1},
            json={"reason": "Testing CAS"},
        )
        assert bad_pause.status_code == 409
        assert bad_pause.json()["detail"]["error_code"] == "STALE_STATE_MUTATION_REJECTED"

        # Valid Pause
        pause_resp = client.post(
            f"/api/programs/executions/{agg_id}/pause",
            headers={"if-match-state-version": str(v1), "if-match-state-sha256": hash1},
            json={"reason": "Operator manual inspection"},
        )
        assert pause_resp.status_code == 200
        pause_data = pause_resp.json()
        assert pause_data["lifecycle"] == "PAUSED"
        v2 = pause_data["version"]
        hash2 = pause_data["state_hash"]
        assert v2 == v1 + 1

        # Valid Resume
        resume_resp = client.post(
            f"/api/programs/executions/{agg_id}/resume",
            headers={"if-match-state-version": str(v2), "if-match-state-sha256": hash2},
            json={"reason": "Resuming after approval"},
        )
        assert resume_resp.status_code == 200
        assert resume_resp.json()["lifecycle"] == "RUNNING"
        assert resume_resp.json()["version"] == v2 + 1
    finally:
        api_app.dependency_overrides.clear()


def test_api_approve_reject_repair(api_app, operator_service: ProgramOperatorRuntimeService) -> None:
    api_app.dependency_overrides[get_operator_service] = lambda: operator_service
    try:
        client = TestClient(api_app)

        # Create
        start_resp = client.post(
            "/api/programs/executions",
            json={"program_id": "interview_semantic_program", "workspace_id": "ws-01"},
        )
        assert start_resp.status_code == 201, start_resp.text
        agg_id = start_resp.json()["aggregate_id"]
        v = start_resp.json()["version"]
        h = start_resp.json()["state_hash"]

        # Approve
        appr_resp = client.post(
            f"/api/programs/executions/{agg_id}/approve",
            headers={"if-match-state-version": str(v), "if-match-state-sha256": h},
            json={"gate_id": "BRIEF_GATE", "decision": "APPROVE", "payload": {"notes": "Approved"}},
        )
        assert appr_resp.status_code == 200
        appr_data = appr_resp.json()
        assert appr_data["last_receipt_id"] is not None
        v_appr = appr_data["version"]
        h_appr = appr_data["state_hash"]

        # Reject with disposition
        rej_resp = client.post(
            f"/api/programs/executions/{agg_id}/reject",
            headers={"if-match-state-version": str(v_appr), "if-match-state-sha256": h_appr},
            json={
                "rejection_reason": "Tone shift needed",
                "disposition_route": "RETURN_TO_HUNTER",
                "gate_id": "BRIEF_GATE",
            },
        )
        assert rej_resp.status_code == 200
        rej_data = rej_resp.json()
        v_rej = rej_data["version"]
        h_rej = rej_data["state_hash"]

        # State Repair
        repair_resp = client.post(
            f"/api/programs/executions/{agg_id}/repair",
            headers={"if-match-state-version": str(v_rej), "if-match-state-sha256": h_rej},
            json={
                "repair_action": "patch_brief",
                "repair_payload": {"brief_status": "MANUALLY_PATCHED"},
            },
        )
        assert repair_resp.status_code == 200
        repair_data = repair_resp.json()
        assert repair_data["aggregate_id"] == agg_id
        assert repair_data["version"] == v_rej + 1
    finally:
        api_app.dependency_overrides.clear()


def test_api_lineage_and_trace_projections(api_app, operator_service: ProgramOperatorRuntimeService) -> None:
    api_app.dependency_overrides[get_operator_service] = lambda: operator_service
    try:
        client = TestClient(api_app)

        # Create
        start_resp = client.post(
            "/api/programs/executions",
            json={
                "program_id": "interview_semantic_program",
                "workspace_id": "ws-01",
                "initial_data": {
                    "evidence_spans": [{"id": "ev-01", "text": "Evidence snippet"}]
                },
            },
        )
        assert start_resp.status_code == 201, start_resp.text
        agg_id = start_resp.json()["aggregate_id"]

        # Lineage
        lin_resp = client.get(f"/api/programs/executions/{agg_id}/lineage")
        assert lin_resp.status_code == 200
        lin_data = lin_resp.json()
        assert lin_data["aggregate_id"] == agg_id
        assert lin_data["is_lossless"] is True
        assert len(lin_data["nodes"]) >= 1

        # Trace
        tr_resp = client.get(f"/api/programs/executions/{agg_id}/trace")
        assert tr_resp.status_code == 200
        tr_data = tr_resp.json()
        assert tr_data["aggregate_id"] == agg_id
        assert tr_data["program_id"] == "interview_semantic_program"
    finally:
        api_app.dependency_overrides.clear()


def test_api_chat_supervision_dispatcher(api_app, operator_service: ProgramOperatorRuntimeService) -> None:
    api_app.dependency_overrides[get_operator_service] = lambda: operator_service
    try:
        client = TestClient(api_app)

        # Discover
        chat_disc = client.post(
            "/api/programs/operator/chat",
            json={"command": "/discover", "workspace_id": "ws-01"},
        )
        assert chat_disc.status_code == 200
        assert chat_disc.json()["success"] is True
        assert chat_disc.json()["action_type"] == "DISCOVER"

        # Run via chat
        chat_run = client.post(
            "/api/programs/operator/chat",
            json={"command": "/run interview_semantic_program", "workspace_id": "ws-01"},
        )
        assert chat_run.status_code == 200
        run_data = chat_run.json()
        assert run_data["success"] is True
        agg_id = run_data["aggregate_id"]
        v = run_data["state_version"]
        h = run_data["state_hash"]

        # Pause via chat
        chat_pause = client.post(
            "/api/programs/operator/chat",
            headers={"if-match-state-version": str(v), "if-match-state-sha256": h},
            json={"command": f"/pause {agg_id}", "workspace_id": "ws-01", "current_aggregate_id": agg_id},
        )
        assert chat_pause.status_code == 200
        assert chat_pause.json()["success"] is True
        assert chat_pause.json()["action_type"] == "PAUSE"
    finally:
        api_app.dependency_overrides.clear()
