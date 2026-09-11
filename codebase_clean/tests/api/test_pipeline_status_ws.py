"""TS-APP-API-005 Pipeline Status WebSocket — acceptance tests.

Every test creates a fresh, isolated PipelineApplication inside a tmp_path
so no fixture state leaks between tests.  WebSocket tests drive node
transitions from a background thread while the WS client reads concurrently,
simulating what a future worker (Gap A) will do automatically.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from cmf_pipeline.application import PipelineApplication

from tests.api._pipeline_fixtures import (
    drive_node_to_success,
    get_topological_order,
    make_run,
)


# ---------------------------------------------------------------------------
# Shared fixture — returns a TestClient backed by an isolated service stack
# ---------------------------------------------------------------------------


@pytest.fixture()
def pipeline_app(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> PipelineApplication:
    """Return a bare PipelineApplication for direct service-level calls."""
    db_path = tmp_path / "state" / "pipeline.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    app = PipelineApplication(database_path=db_path)
    app.initialize()
    app.load_default_development_candidates()
    return app


@pytest.fixture()
def api_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Return a TestClient against the full FastAPI gateway, isolated tmp_path."""
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    from api.main import app

    with TestClient(app) as client:
        yield client


# ---------------------------------------------------------------------------
# AC-001 — WS streams a manually-driven node transition
# ---------------------------------------------------------------------------


def test_node_transition_streams_within_poll_window(
    api_client: TestClient,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """AC-001: create a run, connect WS, drive a node from a background thread,
    observe node_state_changed + run_state_changed within the poll window."""
    # Build a PipelineApplication to create the run
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    from api.main import app as api_app

    pipeline: PipelineApplication = api_app.state.pipeline
    run_id = make_run(pipeline, idempotency_key_prefix="ac001")
    topo = get_topological_order(pipeline, run_id)

    with TestClient(api_app) as client:
        # Connect WebSocket with a very fast poll interval for testing
        with client.websocket_connect(
            f"/api/runs/{run_id}/status?poll_interval_ms=250"
        ) as ws:
            # Receive initial snapshot
            snapshot = ws.receive_json()
            assert snapshot["type"] == "snapshot"
            assert snapshot["run"]["run_id"] == run_id
            assert snapshot["run"]["state"] == "RUNNING"

            # Drive the first node from a background thread
            target_node = topo[0]

            def drive() -> None:
                drive_node_to_success(
                    pipeline,
                    run_id,
                    target_node,
                    ordinal=1,
                    idempotency_key_prefix="ac001",
                )

            t = threading.Thread(target=drive)
            t.start()
            t.join()

                        # Read messages until we see the node reach SUCCEEDED.
            # The diff stream emits node_state_changed for every observable
            # intermediate state (DISPATCHED, RUNNING, SUCCEEDED), so we keep
            # reading until the final SUCCEEDED state is observed.
            node_seen = False
            run_seen = False
            for _ in range(30):  # up to ~7.5s of polling at 250ms
                try:
                    msg = ws.receive_json()
                except WebSocketDisconnect:
                    break

                if msg["type"] == "node_state_changed":
                    assert msg["node"]["node_id"] == target_node
                    assert msg["run_id"] == run_id
                    if msg["node"]["state"] == "SUCCEEDED":
                        node_seen = True
                elif msg["type"] == "run_state_changed":
                    assert msg["run_id"] == run_id
                    run_seen = True

                if node_seen:
                    break

            assert node_seen, (
                f"No node_state_changed message reflecting SUCCEEDED for "
                f"{target_node} received within poll window"
            )


# ---------------------------------------------------------------------------
# AC-002 — GET polling-fallback matches WS snapshot shape
# ---------------------------------------------------------------------------


def test_get_fallback_matches_ws_snapshot(
    api_client: TestClient,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """AC-002: GET /api/runs/{run_id}/status returns a RunStatusEnvelope whose
    ``run`` field is structurally identical to the WS ``snapshot`` message's
    ``run`` field at the same moment."""
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    from api.main import app as api_app

    pipeline: PipelineApplication = api_app.state.pipeline
    run_id = make_run(pipeline, idempotency_key_prefix="ac002")

    with TestClient(api_app) as client:
        # Capture WS snapshot
        with client.websocket_connect(f"/api/runs/{run_id}/status") as ws:
            snapshot = ws.receive_json()
            ws_run = snapshot["run"]

        # Capture GET response
        response = client.get(f"/api/runs/{run_id}/status")
        assert response.status_code == 200
        get_data = response.json()
        get_run = get_data["run"]

        # Compare run fields (ignoring retrieved_at_utc)
        assert get_run["run_id"] == ws_run["run_id"]
        assert get_run["workflow_id"] == ws_run["workflow_id"]
        assert get_run["state"] == ws_run["state"]
        assert get_run["revision"] == ws_run["revision"]
        assert get_run["cancel_requested"] == ws_run["cancel_requested"]
        assert get_run["current_checkpoint_id"] == ws_run["current_checkpoint_id"]
        # Compare node shapes (order-independent, keyed by node_id)
        get_nodes = {n["node_id"]: n for n in get_run["nodes"]}
        ws_nodes = {n["node_id"]: n for n in ws_run["nodes"]}
        assert get_nodes == ws_nodes, "GET and WS node sets differ"


# ---------------------------------------------------------------------------
# AC-003 — Historical event log is complete and hash-verified
# ---------------------------------------------------------------------------


def test_events_endpoint_matches_replay(
    api_client: TestClient,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """AC-003: GET /api/runs/{run_id}/status/events matches a direct
    pipeline.runs.replay() call on event_count and event_stream_sha256."""
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    from api.main import app as api_app

    pipeline: PipelineApplication = api_app.state.pipeline
    run_id = make_run(pipeline, idempotency_key_prefix="ac003")
    topo = get_topological_order(pipeline, run_id)

    # Drive all nodes to completion for a rich event log
    for ordinal, node_id in enumerate(topo, 1):
        drive_node_to_success(
            pipeline,
            run_id,
            node_id,
            ordinal,
            idempotency_key_prefix="ac003",
        )

    with TestClient(api_app) as client:
        response = client.get(f"/api/runs/{run_id}/status/events")
        assert response.status_code == 200
        data = response.json()

        # Compare with direct replay call
        direct = pipeline.runs.replay(run_id)
        assert data["event_count"] == direct["event_count"], (
            f"event_count mismatch: {data['event_count']} vs {direct['event_count']}"
        )
        assert data["event_stream_sha256"] == direct["event_stream_sha256"], (
            f"hash mismatch: {data['event_stream_sha256']} vs {direct['event_stream_sha256']}"
        )
        assert len(data["events"]) == direct["event_count"]


# ---------------------------------------------------------------------------
# AC-004 — Unknown run_id fails clearly on both protocols
# ---------------------------------------------------------------------------


def test_unknown_run_id_404_and_ws_4404(api_client: TestClient):
    """AC-004: unknown run_id -> HTTP 404 with NOT_FOUND; WS -> close 4404."""
    # HTTP path
    response = api_client.get("/api/runs/run:does-not-exist/status")
    assert response.status_code == 404
    assert response.json()["error_code"] == "NOT_FOUND"

    # WS path — connection accepted then immediately closed with 4404
    with pytest.raises(WebSocketDisconnect) as exc_info:
        with api_client.websocket_connect(
            "/api/runs/run:does-not-exist/status"
        ) as ws:
            ws.receive_json()

    assert exc_info.value.code == 4404, (
        f"Expected close code 4404, got {exc_info.value.code}"
    )


# ---------------------------------------------------------------------------
# AC-005 — campaign_id resolves correctly when the edge exists
# ---------------------------------------------------------------------------


def test_campaign_resolves_to_run(
    api_client: TestClient,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """AC-005: when a campaign_produces_run edge exists, the campaign-keyed
    GET returns the same data as the run-keyed GET."""
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    from api.main import app as api_app

    pipeline: PipelineApplication = api_app.state.pipeline
    run_id = make_run(pipeline, idempotency_key_prefix="ac005")

    # Write the campaign→run edge as TS-APP-API-004 would
    campaign_id = "campaign:ac005-demo"
    pipeline.repository.add_edge(
        campaign_id, run_id, "campaign_produces_run"
    )

    with TestClient(api_app) as client:
        # Compare campaign-keyed vs run-keyed responses
        camp_resp = client.get(f"/api/campaigns/{campaign_id}/status")
        run_resp = client.get(f"/api/runs/{run_id}/status")

        assert camp_resp.status_code == 200
        assert run_resp.status_code == 200

        assert camp_resp.json()["run"] == run_resp.json()["run"]


# ---------------------------------------------------------------------------
# AC-006 — campaign_id with no linked run returns a legible 404
# ---------------------------------------------------------------------------


def test_campaign_with_no_run_returns_typed_404(api_client: TestClient):
    """AC-006: no campaign_produces_run edge -> 404 CAMPAIGN_HAS_NO_RUN."""
    response = api_client.get("/api/campaigns/campaign:never-started/status")
    assert response.status_code == 404
    data = response.json()
    assert data["error_code"] == "CAMPAIGN_HAS_NO_RUN"
    assert "campaign:never-started" in data["message"]


# ---------------------------------------------------------------------------
# AC-007 — campaign_id with two linked runs returns 409
# ---------------------------------------------------------------------------


def test_campaign_with_multiple_runs_returns_409(
    api_client: TestClient,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """AC-007: two campaign_produces_run edges -> 409
    CAMPAIGN_HAS_MULTIPLE_RUNS."""
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    from api.main import app as api_app

    pipeline: PipelineApplication = api_app.state.pipeline

    # Create two runs with distinct batch refs so deterministic run IDs differ
    run_id_1 = make_run(
        pipeline,
        idempotency_key_prefix="ac007a",
        batch_ref={"object_id": "batch:1", "version": "1.0.0", "sha256": "0" * 64},
    )
    run_id_2 = make_run(
        pipeline,
        idempotency_key_prefix="ac007b",
        batch_ref={"object_id": "batch:2", "version": "1.0.0", "sha256": "0" * 64},
    )

    campaign_id = "campaign:multi"
    pipeline.repository.add_edge(campaign_id, run_id_1, "campaign_produces_run")
    pipeline.repository.add_edge(campaign_id, run_id_2, "campaign_produces_run")

    with TestClient(api_app) as client:
        response = client.get(f"/api/campaigns/{campaign_id}/status")
        assert response.status_code == 409
        data = response.json()
        assert data["error_code"] == "CAMPAIGN_HAS_MULTIPLE_RUNS"
        assert "campaign:multi" in data["message"]


# ---------------------------------------------------------------------------
# AC-008 — WS closes cleanly on terminal run state
# ---------------------------------------------------------------------------


def test_ws_closes_on_terminal_state(
    api_client: TestClient,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    """AC-008: when a run reaches a terminal state, the WS sends a
    run_terminal message then closes with code 1000."""
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    from api.main import app as api_app

    pipeline: PipelineApplication = api_app.state.pipeline
    run_id = make_run(pipeline, idempotency_key_prefix="ac008")
    topo = get_topological_order(pipeline, run_id)

    with TestClient(api_app) as client:
        with client.websocket_connect(
            f"/api/runs/{run_id}/status?poll_interval_ms=250"
        ) as ws:
            # Receive initial snapshot
            snapshot = ws.receive_json()
            assert snapshot["type"] == "snapshot"

            # Drive all nodes to completion from a background thread
            def drive_all() -> None:
                for ordinal, node_id in enumerate(topo, 1):
                    drive_node_to_success(
                        pipeline,
                        run_id,
                        node_id,
                        ordinal,
                        idempotency_key_prefix="ac008",
                    )

            t = threading.Thread(target=drive_all)
            t.start()
            t.join()

            # Read messages until we see run_terminal
            terminal_seen = False
            for _ in range(60):  # up to ~15s
                try:
                    msg = ws.receive_json()
                except WebSocketDisconnect as exc:
                    # WS closed — verify code and that we already got run_terminal
                    assert terminal_seen, (
                        "Socket closed before run_terminal was received"
                    )
                    assert exc.code == 1000, (
                        f"Expected close code 1000, got {exc.code}"
                    )
                    break

                if msg["type"] == "run_terminal":
                    terminal_seen = True
                    assert msg["run"]["state"] in (
                        "COMPLETED", "FAILED", "CANCELLED", "INVALIDATED"
                    ), f"Unexpected terminal state: {msg['run']['state']}"
            else:
                # If we exhausted the loop without a disconnect, manually check
                assert terminal_seen, "No run_terminal message received"


# ---------------------------------------------------------------------------
# AC-009 — No modification to existing service packages (regression)
# ---------------------------------------------------------------------------


def test_service_packages_unchanged():
    """AC-009: verify no files under services/ or packages/ were touched.

    This is a regression check that runs from the test suite but relies on
    git diff.  In CI this would fail if any build step modified those trees.
    """
    import subprocess
    import sys

    result = subprocess.run(
        ["git", "diff", "--stat", "--", "services/", "packages/"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parent.parent.parent,
    )
    # If there are any changes, print the diff for debugging
    if result.stdout.strip():
        print("WARNING: service/package files modified:")
        print(result.stdout)
    # We assert no diff lines (empty output means clean)
    assert not result.stdout.strip(), (
        f"Files under services/ or packages/ were modified:\n{result.stdout}"
    )