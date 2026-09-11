from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

FIXTURES = Path(__file__).parent / "fixtures" / "harnesses"
GENERIC_MANIFEST = FIXTURES / "generic_text_summary.json"
ACTIVATIVE_MANIFEST = FIXTURES / "activative_expression.json"


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    from api.main import app

    with TestClient(app) as c:
        yield c


def _post_manifest(client, path: Path):
    return client.post(
        "/api/harnesses/build",
        content=path.read_bytes(),
        headers={"Content-Type": "application/json"},
    )


def test_empty_library_returns_empty_list(client):
    """AC-001."""
    response = client.get("/api/harnesses")
    assert response.status_code == 200
    assert response.json() == []


def test_build_generic_then_list(client):
    """AC-002."""
    build = _post_manifest(client, GENERIC_MANIFEST)
    assert build.status_code == 201, build.text
    body = build.json()
    assert body["mode"] == "generic"
    assert body["category_id"] is None
    assert body["definition_id"].startswith("atomic-harness-definition_")

    listing = client.get("/api/harnesses")
    assert listing.status_code == 200
    assert body["definition_id"] in [item["definition_id"] for item in listing.json()]


def test_build_activative_records_category(client):
    """AC-003."""
    build = _post_manifest(client, ACTIVATIVE_MANIFEST)
    assert build.status_code == 201, build.text
    body = build.json()
    assert body["mode"] == "activative"
    assert body["category_id"] == "conversational_activation_expression"


def test_invalid_manifest_rejected(client):
    """AC-004."""
    manifest = json.loads(GENERIC_MANIFEST.read_bytes())
    del manifest["task"]["authority_ref"]
    response = client.post(
        "/api/harnesses/build",
        content=json.dumps(manifest).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400, response.text
    assert response.json()["error_code"] == "INVALID_MANIFEST"

    listing = client.get("/api/harnesses")
    assert listing.json() == []


def test_detail_view_full_contract(client):
    """AC-005."""
    build = _post_manifest(client, ACTIVATIVE_MANIFEST)
    definition_id = build.json()["definition_id"]

    response = client.get(f"/api/harnesses/{definition_id}")
    assert response.status_code == 200
    data = response.json()
    for field in ("goal", "success_condition", "input_contract", "output_contract"):
        assert field in data
    assert data["category_binding"]["category_id"] == "conversational_activation_expression"


def test_unknown_id_404(client):
    """AC-006."""
    response = client.get("/api/harnesses/does-not-exist")
    assert response.status_code == 404
    assert response.json()["error_code"] == "NOT_FOUND"


def test_eligibility_matrix(client):
    """AC-007."""
    activative = _post_manifest(client, ACTIVATIVE_MANIFEST).json()
    generic = _post_manifest(client, GENERIC_MANIFEST).json()

    eligible = client.get(
        f"/api/harnesses/{activative['definition_id']}/eligibility",
        params={"source_category": "conversational_activation_expression"},
    )
    assert eligible.status_code == 200
    assert eligible.json()["status"] == "ELIGIBLE"

    ineligible = client.get(
        f"/api/harnesses/{activative['definition_id']}/eligibility",
        params={"source_category": "carousels"},
    )
    assert ineligible.status_code == 200
    body = ineligible.json()
    assert body["status"] == "INELIGIBLE"
    assert "conversational_activation_expression" in body["reason"]
    assert "carousels" in body["reason"]

    not_applicable = client.get(
        f"/api/harnesses/{generic['definition_id']}/eligibility",
        params={"source_category": "carousels"},
    )
    assert not_applicable.status_code == 200
    assert not_applicable.json()["status"] == "NOT_APPLICABLE"


def test_rebuild_is_idempotent(client, tmp_path):
    """AC-008."""
    first = _post_manifest(client, GENERIC_MANIFEST)
    assert first.status_code == 201, first.text
    second = _post_manifest(client, GENERIC_MANIFEST)
    assert second.status_code == 201, second.text

    first_body, second_body = first.json(), second.json()
    assert first_body["definition_id"] == second_body["definition_id"]
    assert first_body["definition_hash"] == second_body["definition_hash"]
    assert first_body["package_hash"] == second_body["package_hash"]

    library_root = tmp_path / "state" / "harness-library"
    zips = list(library_root.glob("*.zip"))
    assert len(zips) == 1


def test_conflicting_manifest_id_rejected(client):
    """AC-009."""
    first = _post_manifest(client, GENERIC_MANIFEST)
    assert first.status_code == 201, first.text

    changed = json.loads(GENERIC_MANIFEST.read_bytes())
    changed["task"]["goal"] = "A completely different goal statement for this manifest."
    response = client.post(
        "/api/harnesses/build",
        content=json.dumps(changed).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 409, response.text
    assert response.json()["error_code"] == "CONFLICT"


def test_corrupt_package_excluded_not_fatal(client, tmp_path, caplog):
    """AC-010."""
    build = _post_manifest(client, GENERIC_MANIFEST)
    assert build.status_code == 201, build.text

    library_root = tmp_path / "state" / "harness-library"
    bad_zip_path = library_root / "atomic-harness-definition_deadbeef.zip"
    with zipfile.ZipFile(bad_zip_path, "w") as zf:
        zf.writestr("not_a_definition.txt", b"garbage")

    with caplog.at_level("WARNING", logger="ca.api.harness_library"):
        listing = client.get("/api/harnesses")

    assert listing.status_code == 200
    body = listing.json()
    assert len(body) == 1
    assert body[0]["definition_id"] == build.json()["definition_id"]
    assert any("skipping unreadable package" in message for message in caplog.messages)
