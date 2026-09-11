"""API endpoint tests for VAE Delegation & Visual Asset Runtime (Mandate M44 / F15)."""

from __future__ import annotations

import copy
import hashlib
from pathlib import Path
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from ca_contracts import canonical_sha256

def get_delegation_root() -> Path:
    return Path(__file__).resolve().parents[2] / "services/delegation/delegation-contracts/1.1.0-rc.4"


def ref(object_id: str, seed: str) -> dict[str, str]:
    return {"object_id": object_id, "version": "1.0.0", "sha256": canonical_sha256({"seed": seed})}


def build_demand_payload(is_synthetic: bool = False, omit_locks: bool = False) -> dict:
    from cmf_pipeline.delegation import VisualDelegationService
    svc = VisualDelegationService(get_delegation_root())
    package = svc.compile_demand(
        source_package_ref=ref("source-package:api-test", "source"),
        reaction_receipt_refs=[ref("reaction-receipt:api-test", "reaction")],
        expression_moment_refs=[ref("expression-moment:api-test", "moment")],
        semantic_program_ref=ref("semantic-program:api-test", "semantic"),
        final_script_ref=ref("final-script:api-test", "script"),
        primitive_coalition_ref=ref("primitive:api-test", "primitive"),
        archetype_coalition_ref=ref("archetype:api-test", "archetype"),
        activation_transfer_contract_ref=ref("transfer:api-test", "transfer"),
        content_harness_ref=ref("harness:api-test", "harness"),
        category_profile_ref=ref("category:static", "category"),
        format_profile_ref=ref("format:supervisual", "format"),
        width_px=1080,
        height_px=1920,
        wrong_reading_locks=["Do not depict dystopia.", "Preserve operator dignity."],
    )
    demand = copy.deepcopy(package["demand"])
    if omit_locks:
        demand["wrong_reading_locks"] = []
    demand["metadata"] = {
        "scene_index": 1,
        "is_synthetic": is_synthetic,
        "evidence_segments": [
            {
                "segment_id": "seg-api-01",
                "spoken_text": "Authentic spoken quote from factory edge deployment.",
                "text_sha256": hashlib.sha256("Authentic spoken quote from factory edge deployment.".encode("utf-8")).hexdigest(),
            }
        ],
    }
    return demand


def test_api_vae_status(api_app):
    with TestClient(api_app) as client:
        resp = client.get("/api/vae/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "OPERATIONAL"
        assert data["contracts_version"] == "1.1.0-rc.4"


def test_api_vae_full_delegation_flow(api_app):
    with TestClient(api_app) as client:
        workspace_id = str(uuid4())
        demand = build_demand_payload()

        # 1. Admit Demand
        admit_resp = client.post(
            "/api/vae/demands/admit",
            json={
                "workspace_id": workspace_id,
                "program_id": "vae_delegation_program",
                "demand_payload": demand,
                "operator_id": "operator:commander",
            },
        )
        assert admit_resp.status_code == 201
        admit_data = admit_resp.json()
        assert admit_data["status"] == "ADMITTED"
        agg_id = admit_data["aggregate_id"]

        # 2. Inspect Aggregate
        agg_resp = client.get(f"/api/vae/aggregates/{agg_id}")
        assert agg_resp.status_code == 200
        assert agg_resp.json()["current_state"] == "DEMAND_ADMITTED"

        # 3. Execute Job (Plan + Generate + Technical QA)
        exec_resp = client.post(
            "/api/vae/jobs/execute",
            json={
                "aggregate_id": agg_id,
                "worker_id": "worker:agent",
                "producer_actor_id": "agent:hunter",
                "evaluator_actor_id": "agent:analyst",
            },
        )
        assert exec_resp.status_code == 200
        exec_data = exec_resp.json()
        assert exec_data["status"] == "EXECUTED"
        assert exec_data["technical_verdict"] == "PASS"

        # 4. Acknowledge Result & Emit Receipt
        ack_resp = client.post(
            "/api/vae/results/acknowledge",
            json={
                "aggregate_id": agg_id,
                "operator_id": "operator:commander",
                "decision": "ACCEPTED",
                "consumption_authorized": True,
            },
        )
        assert ack_resp.status_code == 200
        ack_data = ack_resp.json()
        assert ack_data["status"] == "ACKNOWLEDGED"
        assert ack_data["consumption_authorized"] is True
        assert ack_data["receipt_sha256"] is not None


def test_api_vae_rejects_synthetic(api_app):
    with TestClient(api_app) as client:
        synthetic_demand = build_demand_payload(is_synthetic=True)
        resp = client.post(
            "/api/vae/demands/admit",
            json={
                "workspace_id": str(uuid4()),
                "program_id": "vae_delegation_program",
                "demand_payload": synthetic_demand,
                "operator_id": "operator",
            },
        )
        assert resp.status_code == 400
        assert "Synthetic demand blocked" in resp.json()["detail"]


def test_api_vae_rejects_missing_locks(api_app):
    with TestClient(api_app) as client:
        no_locks_demand = build_demand_payload(omit_locks=True)
        resp = client.post(
            "/api/vae/demands/admit",
            json={
                "workspace_id": str(uuid4()),
                "program_id": "vae_delegation_program",
                "demand_payload": no_locks_demand,
                "operator_id": "operator",
            },
        )
        assert resp.status_code == 422
        assert "Wrong-reading lock missing" in resp.json()["detail"]
