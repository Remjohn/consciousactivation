from __future__ import annotations

from fastapi.testclient import TestClient

from cmf_pipeline.domain.validation import require_ref
from tests.api.fixtures.air_script_fixture import build_script_fixture


def _client(tmp_path, monkeypatch):
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path))
    from api.main import app
    return TestClient(app)


def test_ac011_transfer_contract_on_unapproved_script_returns_409(tmp_path, monkeypatch):
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        fx = build_script_fixture(air, prefix="ac011")

        response = client.post(f"/api/air/scripts/{fx['script_id']}/transfer-contract", json=fx["transfer_contract_request"])
        assert response.status_code == 409
        assert response.json()["detail"]["error_code"] == "SCRIPT_NOT_APPROVED"


def test_ac012_and_ac013_transfer_contract_on_approved_script(tmp_path, monkeypatch):
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        fx = build_script_fixture(air, prefix="ac012")

        approve = client.post(f"/api/air/scripts/{fx['script_id']}/approve", json=fx["approve_request"])
        assert approve.status_code == 200

        contract = client.post(f"/api/air/scripts/{fx['script_id']}/transfer-contract", json=fx["transfer_contract_request"])
        assert contract.status_code == 200

        followup = client.get(f"/api/air/scripts/{fx['script_id']}")
        assert followup.status_code == 200
        refs = followup.json()["batch_compilation_refs"]

        # AC-012: each of the five fields independently passes the real
        # Pipeline require_ref validator unchanged.
        expected_fields = {
            "final_script_ref",
            "semantic_program_ref",
            "archetype_coalition_ref",
            "primitive_coalition_ref",
            "activation_transfer_contract_ref",
        }
        assert set(refs) == expected_fields
        for field in expected_fields:
            normalized = require_ref(refs[field], field)  # raises PipelineValidationError if invalid
            assert normalized == refs[field]

        # AC-013: semantic_program_ref is byte-identical to the script's own
        # program_ref (proves the field-name projection is a rename, not a
        # different value).
        assert refs["semantic_program_ref"] == followup.json()["program_ref"]
