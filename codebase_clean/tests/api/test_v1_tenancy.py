from __future__ import annotations
from datetime import datetime
from uuid import uuid4
from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient

from api.routers.v1_tenancy import get_db_connection


def test_v1_tenancy_validation_errors(api_app) -> None:
    client = TestClient(api_app)
    mock_conn = MagicMock()
    api_app.dependency_overrides[get_db_connection] = lambda: mock_conn
    try:
        # Invalid slug (uppercase/spaces)
        resp = client.post(
            "/api/v1/workspaces",
            json={"slug": "INVALID SLUG", "display_name": "Test"},
            headers={"X-Actor-Id": "operator-1", "X-Is-Operator": "true", "X-Operator-Grant-Id": str(uuid4())},
        )
        assert resp.status_code == 422
    finally:
        api_app.dependency_overrides.clear()


def test_v1_tenancy_header_parsing(api_app) -> None:
    client = TestClient(api_app)
    ws_id = str(uuid4())

    # Mock DB connection dependency
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur
    
    # Mock return for get_workspace
    mock_cur.fetchone.side_effect = [
        (ws_id, "test-ws", "Test Workspace", "ACTIVE", "2026-08-26T00:00:00Z", "2026-08-26T00:00:00Z"),
        (str(uuid4()),),  # receipt fetch
    ]

    api_app.dependency_overrides[get_db_connection] = lambda: mock_conn
    try:
        resp = client.get(
            f"/api/v1/workspaces/{ws_id}",
            headers={"X-Actor-Id": "actor-1", "X-Workspace-Id": ws_id, "X-Role": "MEMBER"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["workspace_id"] == ws_id
        assert data["slug"] == "test-ws"
    finally:
        api_app.dependency_overrides.clear()


def test_v1_tenancy_list_workspaces_endpoint(api_app) -> None:
    client = TestClient(api_app)
    ws_id = str(uuid4())
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur

    mock_cur.fetchall.return_value = [
        (ws_id, "test-ws", "Test Workspace", "ACTIVE", datetime(2026, 8, 26), datetime(2026, 8, 26))
    ]

    api_app.dependency_overrides[get_db_connection] = lambda: mock_conn
    try:
        resp = client.get(
            "/api/v1/workspaces",
            headers={"X-Actor-Id": "actor-1", "X-Workspace-Id": ws_id, "X-Role": "MEMBER"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["workspace_id"] == ws_id
        assert data[0]["slug"] == "test-ws"
    finally:
        api_app.dependency_overrides.clear()


def test_v1_tenancy_list_memberships_endpoint(api_app) -> None:
    client = TestClient(api_app)
    ws_id = str(uuid4())
    mem_id = str(uuid4())
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cur

    mock_cur.fetchall.return_value = [
        (mem_id, ws_id, "actor-admin", "ADMIN", "ACTIVE", datetime(2026, 8, 26))
    ]

    api_app.dependency_overrides[get_db_connection] = lambda: mock_conn
    try:
        resp = client.get(
            f"/api/v1/workspaces/{ws_id}/memberships",
            headers={"X-Actor-Id": "actor-admin", "X-Workspace-Id": ws_id, "X-Role": "ADMIN"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["membership_id"] == mem_id
        assert data[0]["actor_id"] == "actor-admin"
        assert data[0]["role"] == "ADMIN"
    finally:
        api_app.dependency_overrides.clear()


def test_v1_tenancy_list_memberships_cross_workspace_forbidden(api_app) -> None:
    client = TestClient(api_app)
    ws_id_1 = str(uuid4())
    ws_id_2 = str(uuid4())

    mock_conn = MagicMock()
    api_app.dependency_overrides[get_db_connection] = lambda: mock_conn
    try:
        resp = client.get(
            f"/api/v1/workspaces/{ws_id_2}/memberships",
            headers={"X-Actor-Id": "actor-1", "X-Workspace-Id": ws_id_1, "X-Role": "MEMBER"},
        )
        assert resp.status_code == 403
    finally:
        api_app.dependency_overrides.clear()

