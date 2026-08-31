"""API endpoint tests for Governed Program Registry & Package Discovery (TS-CAE-PROG-001)."""

from __future__ import annotations

from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from api.routers.programs import get_registry
from ca_runtime.program_registry import ProgramRegistry


@pytest.fixture
def test_registry() -> ProgramRegistry:
    root = Path("programs").resolve()
    reg = ProgramRegistry(discovery_roots=[root])
    reg.discover()
    return reg


def test_api_list_programs(api_app, test_registry: ProgramRegistry) -> None:
    api_app.dependency_overrides[get_registry] = lambda: test_registry
    try:
        client = TestClient(api_app)
        resp = client.get("/api/programs")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] >= 3
        ids = [p["program_id"] for p in data["programs"]]
        assert "interview_semantic_program" in ids
        assert "collision_discovery_program" in ids
        assert "editorial_storyboard_program" in ids
    finally:
        api_app.dependency_overrides.clear()


def test_api_get_program_details(api_app, test_registry: ProgramRegistry) -> None:
    api_app.dependency_overrides[get_registry] = lambda: test_registry
    try:
        client = TestClient(api_app)
        resp = client.get("/api/programs/interview_semantic_program")
        assert resp.status_code == 200
        data = resp.json()
        assert data["program_id"] == "interview_semantic_program"
        assert data["status"] == "ACTIVE"
        assert "HUNTER" in data["authority_lanes"]
        assert len(data["skills"]) == 1
        assert data["skills"][0]["name"] == "interview_elicitation"
        assert len(data["package_sha256"]) == 64
    finally:
        api_app.dependency_overrides.clear()


def test_api_get_program_not_found(api_app, test_registry: ProgramRegistry) -> None:
    api_app.dependency_overrides[get_registry] = lambda: test_registry
    try:
        client = TestClient(api_app)
        resp = client.get("/api/programs/nonexistent_program")
        assert resp.status_code == 404
        assert resp.json()["error_code"] == "NOT_FOUND"
    finally:
        api_app.dependency_overrides.clear()


def test_api_preflight_program_success(api_app, test_registry: ProgramRegistry) -> None:
    api_app.dependency_overrides[get_registry] = lambda: test_registry
    try:
        client = TestClient(api_app)
        resp = client.post(
            "/api/programs/interview_semantic_program/preflight",
            json={
                "workspace_id": "ws-test-99",
                "context_refs": ["workspace_active", "interview_brief_approved"],
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["eligible"] is True
        assert data["issues"] == []
        assert data["authority_lane_checks"] == {"HUNTER": True, "ANALYST": True}
        assert len(data["preflight_digest"]) == 64
    finally:
        api_app.dependency_overrides.clear()


def test_api_preflight_program_fail_closed(api_app, test_registry: ProgramRegistry) -> None:
    api_app.dependency_overrides[get_registry] = lambda: test_registry
    try:
        client = TestClient(api_app)
        resp = client.post(
            "/api/programs/interview_semantic_program/preflight",
            json={
                "workspace_id": "ws-test-99",
                "context_refs": [],  # Missing preconditions
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["eligible"] is False
        assert len(data["issues"]) >= 2
        assert any("Unsatisfied precondition" in issue for issue in data["issues"])
    finally:
        api_app.dependency_overrides.clear()


def test_api_preflight_program_not_found(api_app, test_registry: ProgramRegistry) -> None:
    api_app.dependency_overrides[get_registry] = lambda: test_registry
    try:
        client = TestClient(api_app)
        resp = client.post(
            "/api/programs/nonexistent/preflight",
            json={"workspace_id": "ws-1"},
        )
        assert resp.status_code == 404
    finally:
        api_app.dependency_overrides.clear()
