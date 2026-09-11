"""Unit and integration tests for CAE Mandate M17 (Workflow + Capability Metadata Bridge).

Governed by:
- 00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md
- 00_CONTROL/17_PHASE1_AGENT_SKILL_OPERATION_OWNERSHIP_GRAPH.md (M05)
- 00_CONTROL/21_PHASE2_CAPABILITY_SECURITY_MATRIX.md
- 02_PHASE_2_RUNTIME_FOUNDATION/M17_workflow_capability_metadata_bridge.md
- CURRENT.md runtime blockers
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest
from fastapi.testclient import TestClient

from ca_contracts import canonical_sha256
from ca_runtime.metadata_bridge import (
    GOVERNED_BASELINE_CAPABILITIES,
    BridgeCompilationResult,
    WorkflowCapabilityMetadataBridge,
)
from ca_runtime.pi_adapter import AuthorityLane
from cmf_builder.application.export_service import PortableAtomicHarnessCompiler
from cmf_builder.application.manifest_parser import OperatorManifestParser
from cmf_builder.application.productization_contracts import OperatorManifestRequest
from cmf_builder.domain.portable_export import PortableAtomicHarnessDefinition
from cmf_pipeline.bindings.eligibility_registry import ImplementationEligibilityRegistry
from cmf_pipeline.domain.enums import NodeKind, ProductBoundary

FIXTURES = Path(__file__).parent.parent / "api" / "fixtures"
HARNESS_PATH = FIXTURES / "harnesses" / "activative_expression.json"


def _make_pilot_definition(**overrides) -> PortableAtomicHarnessDefinition:
    manifest_res = OperatorManifestParser().parse(
        OperatorManifestRequest(
            manifest_bytes=HARNESS_PATH.read_bytes(),
            source_name="activative_expression.json",
        )
    )
    durable_record = PortableAtomicHarnessCompiler().compile(manifest_res)

    compiled = PortableAtomicHarnessDefinition.from_payload_bytes(durable_record.payload)
    if not overrides:
        return compiled
    content = dict(compiled.content)
    content.update(overrides)
    content_bytes = json.dumps(content, separators=(",", ":"), sort_keys=True).encode("utf-8")
    digest = canonical_sha256(content)
    definition_id = f"atomic-harness-definition_{digest}"
    definition_hash = f"sha256:{digest}"
    payload_bytes = json.dumps(
        {
            "artifact_type": "AtomicHarnessDefinition",
            "definition_id": definition_id,
            "definition_hash": definition_hash,
            "definition": content,
        },
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return PortableAtomicHarnessDefinition(
        definition_id=definition_id,
        definition_hash=definition_hash,
        content_bytes=content_bytes,
        payload_bytes=payload_bytes,
    )





# ---------------------------------------------------------------------------
# Unit Tests: Bridge Resolution & Fail-Closed Semantics
# ---------------------------------------------------------------------------

def test_pilot_harness_compiles_end_to_end_with_governed_metadata():
    """Verify that a real pilot activative harness resolves real capability and workflow metadata."""
    definition = _make_pilot_definition()
    bridge = WorkflowCapabilityMetadataBridge()

    result: BridgeCompilationResult = bridge.compile(definition)

    assert result.success is True
    assert result.blocked_field is None
    assert result.blocked_reason is None
    assert result.intake_projection is not None

    # Check 14-key canonical intake projection
    projection = result.intake_projection
    assert projection["category_id"] == "conversational_activation_expression"
    assert projection["profile_id"] == "portable-activative-v1"
    assert len(projection["capabilities"]) > 0

    assert len(projection["workflow"]["nodes"]) > 0
    assert len(projection["workflow"]["edges"]) >= 0

    # Verify resolved capabilities contain governed metadata
    assert result.resolved_capabilities is not None
    for cap_id, meta in result.resolved_capabilities.items():
        assert "owner_kind" in meta
        assert "required_features" in meta
        assert "authority_boundary" in meta
        assert meta["owner_kind"] in {"CODE", "AGENT", "HUMAN", "EXTERNAL", "tool"}

    # Verify 4 Authority Lanes in workflow nodes
    assert result.resolved_workflow is not None
    valid_roles = {lane.value for lane in AuthorityLane}
    for node in result.resolved_workflow["nodes"]:
        assert node["role"] in valid_roles
        assert node["actor_kind"] in {item.value for item in NodeKind}
        assert node["product_boundary"] in {item.value for item in ProductBoundary}


def test_missing_capability_metadata_fails_closed_blocker_2():
    """Verify that unresolvable capabilities fail closed explicitly with Blocker 2."""
    definition = _make_pilot_definition(
        capability_requirements=["unregistered_alien_capability_999"]
    )
    bridge = WorkflowCapabilityMetadataBridge()

    result: BridgeCompilationResult = bridge.compile(definition)

    assert result.success is False
    assert result.blocked_field == "capabilities"
    assert result.blocker_ref == "TS-APP-BRIDGE-001#blocker-2"
    assert "unregistered_alien_capability_999" in str(result.blocked_reason)
    assert "BRIDGE-001 Blocker (capabilities)" in result.formatted_blocked_reason


def test_missing_workflow_fails_closed_blocker_5():
    """Verify that an empty workflow with no derivation source fails closed explicitly with Blocker 5."""
    definition = _make_pilot_definition(
        capability_requirements=[],
        execution_plan=[],
        workflow={},
    )
    bridge = WorkflowCapabilityMetadataBridge()

    result: BridgeCompilationResult = bridge.compile(definition)

    assert result.success is False
    assert result.blocked_field == "workflow"
    assert result.blocker_ref == "TS-APP-BRIDGE-001#blocker-5"
    assert "BRIDGE-001 Blocker (workflow)" in result.formatted_blocked_reason


def test_invalid_authority_lane_fails_closed():
    """Verify that a workflow node claiming an invalid authority lane is rejected."""
    definition = _make_pilot_definition()
    bridge = WorkflowCapabilityMetadataBridge()

    invalid_workflow = {
        "nodes": [
            {
                "node_id": "node:test",
                "capability_id": "activative_contract_validation",
                "phase_order": 1,
                "role": "INVALID_SUPER_LANE",
                "actor_kind": "DETERMINISTIC_MODULE",
                "product_boundary": "ATOMIC_HARNESS_PIPELINE",
                "input_contracts": ["in"],
                "output_contracts": ["out"],
            }
        ],
        "edges": [],
    }

    result: BridgeCompilationResult = bridge.compile(
        definition,
        override_workflow=invalid_workflow,
    )

    assert result.success is False
    assert result.blocked_field == "workflow"
    assert "INVALID_SUPER_LANE" in str(result.blocked_reason)


def test_missing_semantic_dependencies_fails_closed_blocker_1():
    """Verify that harnesses with no resolvable semantic lineage fail closed with Blocker 1."""
    definition = _make_pilot_definition(
        provenance_refs=[],
        category_binding={"category_id": "conversational_activation_expression", "semantic_lineage_refs": []},
    )
    bridge = WorkflowCapabilityMetadataBridge()

    result: BridgeCompilationResult = bridge.compile(definition)

    assert result.success is False
    assert result.blocked_field == "semantic_dependencies"
    assert result.blocker_ref == "TS-APP-BRIDGE-001#blocker-1"
    assert "BRIDGE-001 Blocker (semantic_dependencies)" in result.formatted_blocked_reason


def test_eligibility_registry_dynamic_resolution():
    """Verify that capabilities registered in ImplementationEligibilityRegistry are resolved dynamically."""
    registry = ImplementationEligibilityRegistry()
    registry.register({
        "implementation_id": "custom-candidate-impl",
        "implementation_version": "1.0.0",
        "owner_product": "CUSTOM_INTEL",
        "implementation_kind": "AGENT",
        "capability_ids": ["custom_dynamic_capability"],
        "features": ["custom_feature_token_bounded"],
        "side_effect_class": "LOCAL_STATE_WRITE",
        "authority_boundary": "custom_governed_boundary",
        "development_eligible": True,
        "production_authorized": False,
        "evidence_refs": ["evidence:candidate:1"],
    })

    definition = _make_pilot_definition(
        capability_requirements=["custom_dynamic_capability"],
    )
    bridge = WorkflowCapabilityMetadataBridge(eligibility_registry=registry)

    result = bridge.compile(definition)

    assert result.success is True
    assert "custom_dynamic_capability" in result.resolved_capabilities
    meta = result.resolved_capabilities["custom_dynamic_capability"]
    assert meta["owner_kind"] == "AGENT"
    assert meta["authority_boundary"] == "custom_governed_boundary"
    assert "custom_feature_token_bounded" in meta["required_features"]


# ---------------------------------------------------------------------------
# Integration Tests: Campaign Creation Route with Governed Metadata Bridge
# ---------------------------------------------------------------------------

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("CA_DATA_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("CA_MEDIA_ROOT", str(tmp_path / "media"))
    from api.main import app
    with TestClient(app) as c:
        yield c


def _import_source_pkg(client: TestClient) -> str:
    with open(FIXTURES / "synthetic_interview.mp4", "rb") as video, \
         open(FIXTURES / "sample_transcript.srt", "rb") as transcript:
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


def _build_activative_harness(client: TestClient) -> str:
    resp = client.post(
        "/api/harnesses/build",
        content=HARNESS_PATH.read_bytes(),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["definition_id"]


def test_campaign_creation_with_governed_bridge_succeeds(client):
    """Verify that POST /api/campaigns with pipeline_trigger succeeds when the harness is governed."""
    pkg_id = _import_source_pkg(client)
    harness_id = _build_activative_harness(client)

    body = {
        "idempotency_key": "k-bridge-success-1",
        "workspace_id": "workspace:test",
        "project_id": "project:test",
        "source_package_id": pkg_id,
        "harness_definition_id": harness_id,
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
        "pipeline_trigger": {"final_script_id": None},
    }

    resp = client.post("/api/campaigns", json=body)
    assert resp.status_code == 201, resp.text
    data = resp.json()

    assert data["pipeline_ingestion_status"] == "BRIDGE_SUCCEEDED"
    assert data["pipeline_ingestion_blocked_reason"] is None
