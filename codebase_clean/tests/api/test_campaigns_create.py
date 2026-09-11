"""Integration tests for POST /api/campaigns — AC-001 through AC-010.

Uses FastAPI's TestClient with an isolated tmp_path CA_DATA_ROOT for each
test.  Source packages are created by posting to /api/interviews/import
(first-party endpoint, real ffprobe-readable mp4 + SRT).  Harnesses are
installed by posting a manifest to /api/harnesses/build then extracting the
definition_id from the response.

Error-code assertions match the global handler behaviour documented in
TS-APP-API-004 §5 and confirmed empirically in the AIR test suite:
  - 404s: response.json()["error_code"] == "NOT_FOUND"  (global not_found_handler)
  - 400/409/422: response.json()["detail"]["error_code"]  (http_exception_handler)
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Reuse the interview import helper from the existing test suite
from tests.api.test_interviews_import import _post_import

FIXTURES = Path(__file__).parent / "fixtures"
HARNESS_MANIFEST = FIXTURES / "harnesses" / "activative_expression.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_harness(client: TestClient) -> str:
    """POST a real activative harness manifest, return definition_id."""
    resp = client.post(
        "/api/harnesses/build",
        content=HARNESS_MANIFEST.read_bytes(),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["definition_id"]


def _import_source_package(client: TestClient, fixtures_dir: Path) -> str:
    """Import a real mp4+SRT, return the package_id (source_package_id)."""
    with open(fixtures_dir / "synthetic_interview.mp4", "rb") as video, \
         open(fixtures_dir / "sample_transcript.srt", "rb") as transcript:
        resp = client.post(
            "/api/interviews/import",
            files={
                "video": ("synthetic_interview.mp4", video, "video/mp4"),
                "transcript": ("sample_transcript.srt", transcript, "text/plain"),
            },
            data={
                "workspace_id": "ws-test", "project_id": "prj-test",
                "operator_id": "op-1", "authority_scope": "DEVELOPMENT_TEST",
                "assertion_id": "assert-1", "transcript_format": "SRT",
                "speaker_id": "guest",
            },
        )
    assert resp.status_code == 201, resp.text
    return resp.json()["package_id"]


def _minimal_create_body(source_package_id: str, harness_definition_id: str, **overrides) -> dict:
    body = {
        "idempotency_key": "test-key-1",
        "workspace_id": "workspace:test",
        "project_id": "project:test",
        "source_package_id": source_package_id,
        "harness_definition_id": harness_definition_id,
        "category_id": "conversational_activation_expression",
        "format_profile_id": "format07_direct_coaching_a_roll",
        "objective": "Preserve source expression",
        "initial_seed": "A source-backed seed",
        "taste_direction": ["identity-first"],
        "output_targets": [{"output_type": "SOURCE_LED_SHORT", "quantity": 1, "profile_id": "format07_direct_coaching_a_roll"}],
        "budget_units": 100,
        "deadline_utc": None,
        "autonomy_mode": "REVIEW_BEFORE_SHIP",
        "operator_id": "operator:jane",
    }
    body.update(overrides)
    return body


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    from api.main import app
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def fixtures_dir():
    return Path(__file__).parent / "fixtures"


@pytest.fixture()
def ready_source_package_id(client, fixtures_dir) -> str:
    """A source package at COMPONENTS_IN_PROGRESS (import endpoint does this)."""
    return _import_source_package(client, fixtures_dir)


@pytest.fixture()
def eligible_harness_definition_id(client) -> str:
    """A harness in the library whose category_binding matches the request."""
    return _build_harness(client)


# ---------------------------------------------------------------------------
# AC-001 — Campaign creation succeeds
# ---------------------------------------------------------------------------

def test_create_succeeds(client, fixtures_dir, ready_source_package_id, eligible_harness_definition_id):
    body = _minimal_create_body(ready_source_package_id, eligible_harness_definition_id)
    resp = client.post("/api/campaigns", json=body)
    assert resp.status_code == 201, resp.text
    b = resp.json()
    assert b["state"]["lifecycle_state"] == "LAUNCHED"
    assert b["state"]["version"] == 1
    assert b["pipeline_ingestion_status"] == "NOT_YET_TRIGGERED"
    assert b["pipeline_ingestion_blocked_reason"] is None
    assert b["idempotent_replay"] is False
    assert b["order"]["order_id"].startswith("campaign-order:")
    assert b["state"]["campaign_id"].startswith("campaign:")


# ---------------------------------------------------------------------------
# AC-002 — Unknown source package
# ---------------------------------------------------------------------------

def test_unknown_source_package_returns_404(client, eligible_harness_definition_id):
    body = _minimal_create_body("ie:source-package:nonexistent", eligible_harness_definition_id)
    resp = client.post("/api/campaigns", json=body)
    assert resp.status_code == 404
    # Global not_found_handler wraps as {"error_code": "NOT_FOUND", ...}
    assert resp.json()["error_code"] == "NOT_FOUND"


# ---------------------------------------------------------------------------
# AC-003 — Source package not yet ready (ADMITTED)
# ---------------------------------------------------------------------------

def test_admitted_only_source_rejected(client, fixtures_dir, eligible_harness_definition_id):
    """An ADMITTED package (no components bound) must be rejected.

    The import endpoint produces COMPONENTS_IN_PROGRESS directly, so to get
    an ADMITTED package we directly patch the SQLite row via the repository's
    own connection helper.
    """
    pkg_id = _import_source_package(client, fixtures_dir)

    # Patch lifecycle_state to ADMITTED directly in the interview DB
    repo = client.app.state.interview.repository
    import sqlite3
    conn = sqlite3.connect(repo.path)
    conn.execute(
        "UPDATE ie_objects SET payload_json = json_set(payload_json, '$.lifecycle_state', 'ADMITTED') WHERE object_id = ?",
        (pkg_id,),
    )
    conn.commit()
    conn.close()

    body = _minimal_create_body(pkg_id, eligible_harness_definition_id)
    resp = client.post("/api/campaigns", json=body)
    assert resp.status_code == 422
    assert resp.json()["detail"]["error_code"] == "SOURCE_PACKAGE_NOT_READY"


# ---------------------------------------------------------------------------
# AC-004 — Unknown harness
# ---------------------------------------------------------------------------

def test_unknown_harness_returns_404(client, ready_source_package_id):
    body = _minimal_create_body(ready_source_package_id, "nonexistent-harness-id")
    resp = client.post("/api/campaigns", json=body)
    assert resp.status_code == 404
    assert resp.json()["error_code"] == "NOT_FOUND"


# ---------------------------------------------------------------------------
# AC-005 — Category-mismatched harness
# ---------------------------------------------------------------------------

def test_harness_category_mismatch_rejected(client, fixtures_dir, ready_source_package_id):
    # Build a harness (activative_expression -> conversational_activation_expression)
    harness_id = _build_harness(client)
    # Request a different category
    body = _minimal_create_body(
        ready_source_package_id, harness_id,
        category_id="short_form_edited_video",  # mismatched
    )
    resp = client.post("/api/campaigns", json=body)
    assert resp.status_code == 422
    assert resp.json()["detail"]["error_code"] == "HARNESS_INELIGIBLE"


# ---------------------------------------------------------------------------
# AC-006 — Format 02 deferred (end-to-end)
# ---------------------------------------------------------------------------

def test_format02_rejected_end_to_end(client, fixtures_dir, eligible_harness_definition_id):
    pkg_id = _import_source_package(client, fixtures_dir)

    # format_profile_id trigger: keep the harness-matching category, vary only
    # the format_profile_id so the HARNESS_INELIGIBLE check doesn't fire first.
    # (The category_id == "2d_character_animation" trigger is covered in the
    # pure unit test suite, since no harness fixture is bound to that category.)
    body = _minimal_create_body(pkg_id, eligible_harness_definition_id, format_profile_id="format02_test")
    resp = client.post("/api/campaigns", json=body)
    assert resp.status_code == 422
    assert resp.json()["detail"]["error_code"] == "FORMAT02_DEFERRED"


# ---------------------------------------------------------------------------
# AC-009 — Exact-retry idempotency
# ---------------------------------------------------------------------------

def test_exact_idempotency_key_replay(client, fixtures_dir, ready_source_package_id, eligible_harness_definition_id):
    body = _minimal_create_body(ready_source_package_id, eligible_harness_definition_id, idempotency_key="k-exact-1")
    r1 = client.post("/api/campaigns", json=body)
    assert r1.status_code == 201
    campaign_id = r1.json()["state"]["campaign_id"]

    r2 = client.post("/api/campaigns", json=body)
    assert r2.status_code == 201
    assert r2.json()["state"]["campaign_id"] == campaign_id
    assert r2.json()["idempotent_replay"] is True


# ---------------------------------------------------------------------------
# AC-010 — Content-addressed idempotency across different keys
# ---------------------------------------------------------------------------

def test_content_addressed_replay_preserves_current_state(client, fixtures_dir, ready_source_package_id, eligible_harness_definition_id):
    body1 = _minimal_create_body(ready_source_package_id, eligible_harness_definition_id, idempotency_key="k-content-1")
    r1 = client.post("/api/campaigns", json=body1)
    assert r1.status_code == 201
    campaign_id = r1.json()["state"]["campaign_id"]
    assert r1.json()["state"]["lifecycle_state"] == "LAUNCHED"

    # Cancel the campaign
    cancel_resp = client.post(
        f"/api/campaigns/{campaign_id}/cancel",
        json={"expected_version": 1, "reason": "test cancel"},
    )
    assert cancel_resp.status_code == 200
    assert cancel_resp.json()["state"]["lifecycle_state"] == "CANCELLED"

    # Now create with a different idempotency key but same logical content
    body2 = _minimal_create_body(ready_source_package_id, eligible_harness_definition_id, idempotency_key="k-content-2")
    r2 = client.post("/api/campaigns", json=body2)
    assert r2.status_code == 201
    # Must return the EXISTING campaign, not create a new one
    assert r2.json()["state"]["campaign_id"] == campaign_id
    assert r2.json()["state"]["lifecycle_state"] == "CANCELLED"  # preserved!
    assert r2.json()["idempotent_replay"] is True
