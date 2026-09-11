from __future__ import annotations

from fastapi.testclient import TestClient

from tests.api.fixtures.air_script_fixture import build_script_fixture


def _client(tmp_path, monkeypatch):
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path))
    from api.main import app
    return TestClient(app)


def test_ac008_unapproved_script_reports_script_not_approved(tmp_path, monkeypatch):
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        fx = build_script_fixture(air, prefix="ac008")

        response = client.get(f"/api/air/scripts/{fx['script_id']}")
        assert response.status_code == 200
        body = response.json()
        assert body["operator_approved"] is False
        assert body["batch_compilation_refs"] == {"reason": "SCRIPT_NOT_APPROVED"}


def test_ac014_get_only_ever_resolves_the_current_revision(tmp_path, monkeypatch):
    """Documented limitation (Section 3, list_edges note), not a bug: GET
    resolves whatever AirRepository.get_object considers "current" for the
    object_id, never a specific historical revision. Demonstrated here by
    approving a script (which creates a new revision) and confirming GET
    reflects the new (current) revision's state, not the pre-approval one
    that .history()[0] still holds.
    """
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        fx = build_script_fixture(air, prefix="ac014")

        pre_approval_revision = air.repository.history(fx["script_id"])[0]
        assert pre_approval_revision.payload["operator_approved"] is False

        approve = client.post(f"/api/air/scripts/{fx['script_id']}/approve", json=fx["approve_request"])
        assert approve.status_code == 200

        # .history()[0] is still the pre-approval revision -- untouched.
        assert air.repository.history(fx["script_id"])[0].payload["operator_approved"] is False
        # But GET (like every route in this spec) only ever resolves current.
        current = client.get(f"/api/air/scripts/{fx['script_id']}")
        assert current.json()["operator_approved"] is True


def test_ac015_stale_transfer_contract_not_returned_for_a_later_revision(tmp_path, monkeypatch):
    with _client(tmp_path, monkeypatch) as client:
        air = client.app.state.air
        fx = build_script_fixture(air, prefix="ac015")

        approve = client.post(f"/api/air/scripts/{fx['script_id']}/approve", json=fx["approve_request"])
        assert approve.status_code == 200

        contract = client.post(f"/api/air/scripts/{fx['script_id']}/transfer-contract", json=fx["transfer_contract_request"])
        assert contract.status_code == 200

        after_contract = client.get(f"/api/air/scripts/{fx['script_id']}")
        assert "final_script_ref" in after_contract.json()["batch_compilation_refs"]

        # Directly construct an unrelated N+1 revision of the *same*
        # script_id (out of scope to trigger via this spec's own routes --
        # AC-015 explicitly allows building it straight against
        # AirRepository/DerivativeService in the test).
        current = air.repository.get_object(fx["script_id"])
        successor_payload = dict(current.payload)
        successor_payload["limitations"] = [*current.payload["limitations"], "revision N+1: unrelated correction"]
        successor_payload["supersedes_ref"] = current.immutable_ref()
        air.derivatives.store_script(
            successor_payload,
            idempotency_key=f"{fx['script_id']}:revision-n-plus-1",
            expected_revision=current.revision,
        )

        after_new_revision = client.get(f"/api/air/scripts/{fx['script_id']}")
        assert after_new_revision.status_code == 200
        # The stale (revision N) transfer contract must NOT be surfaced for
        # revision N+1 -- exact-ref match, not just matching object_id.
        assert after_new_revision.json()["batch_compilation_refs"] == {"reason": "NO_TRANSFER_CONTRACT_YET"}
