from __future__ import annotations

import json
from pathlib import Path

import pytest

from api.services.studio_bridge import StudioBridge, StudioBridgeCrash, StudioBridgeError

ROOT = Path(__file__).resolve().parents[2]
RPC = ROOT / "services" / "studio" / "dist" / "rpc.js"


def _payload() -> dict:
    return {
        "projection_id": "projection:test",
        "campaign": {
            "campaign_id": "campaign:test",
            "order_ref": {"object_type": "campaign_order", "object_id": "order:test", "content_sha256": "a" * 64},
            "lifecycle_state": "AWAITING_REVIEW",
            "autonomy_mode": "REVIEW_BEFORE_SHIP",
            "active_checkpoint_id": "checkpoint:1",
            "exception_ids": [],
            "run_refs": [],
            "artifact_refs": [],
            "evaluation_refs": [],
            "version": 1,
        },
        "order": {
            "order_id": "order:test",
            "workspace_id": "workspace:test",
            "project_id": "project:test",
            "source_kind": "ASSET_PACKAGE_SPEC",
            "source_ref": {"object_type": "source_package", "object_id": "source:test", "content_sha256": "b" * 64},
            "harness_ref": {"object_type": "harness", "object_id": "harness:test", "content_sha256": "c" * 64},
            "category_id": "short_form_edited_video",
            "format_profile_id": "NOT_APPLICABLE",
            "objective": "Test",
            "initial_seed": "seed",
            "taste_direction": [],
            "output_targets": [],
            "budget_units": 1,
            "deadline_utc": None,
            "autonomy_policy": {"mode": "REVIEW_BEFORE_SHIP", "checkpoint_ids": [], "exception_only": False, "final_review_required": True, "publication_authority_required": True},
            "operator_actor": {"actor_id": "operator:test", "actor_type": "HUMAN", "display_name": "Test Operator"},
            "authority": {"authority_id": "authority:test", "authority_type": "SYSTEM", "basis_refs": []},
        },
        "studio_binding": {
            "binding_id": "binding:test",
            "harness_ref": {"object_type": "harness", "object_id": "harness:test", "content_sha256": "c" * 64},
            "category_id": "short_form_edited_video",
            "primary_surface": "VISUAL_ASSET_STUDIO",
            "supporting_surfaces": ["VIDEO_PRODUCTION_STUDIO"],
            "operator_entry_policy": "REVIEW_ALLOWED",
            "binding_reason": "test",
        },
        "source_package_ref": {"object_type": "source_package", "object_id": "source:test", "content_sha256": "b" * 64},
        "observed_activative_pack_ref": None,
        "semantic_production_package_ref": None,
        "final_script_ref": None,
        "activation_transfer_contract_ref": None,
        "run_nodes": [],
        "artifacts": [],
        "evaluations": [],
        "knowledge": {"skill_refs": [], "steering_recipe_refs": [], "retrieval_receipt_refs": [], "programmed_model_claim_refs": [], "exclusion_codes": []},
        "runtime_health": [],
        "timeline": None,
        "exception_packages": [],
        "available_actions": [],
        "projection_sha256": "",
    }


def test_bridge_happy_path() -> None:
    result = StudioBridge(RPC).call("build-control-tower-projection", _payload())
    assert "VISUAL_ASSET_STUDIO" in result["available_actions"]
    assert result["projection_sha256"]


def test_bridge_fails_closed_when_entrypoint_missing(tmp_path: Path) -> None:
    with pytest.raises(StudioBridgeCrash, match="not built"):
        StudioBridge(tmp_path / "missing.js").call("health", {})


def test_bridge_fails_closed_on_malformed_json(tmp_path: Path) -> None:
    script = tmp_path / "malformed.js"
    script.write_text("process.stdout.write('not-json\\n');")
    with pytest.raises(StudioBridgeCrash, match="malformed JSON"):
        StudioBridge(script).call("health", {})


def test_bridge_fails_closed_on_timeout(tmp_path: Path) -> None:
    script = tmp_path / "hang.js"
    script.write_text("setTimeout(() => process.exit(0), 10000);")
    with pytest.raises(StudioBridgeCrash, match="timed out"):
        StudioBridge(script).call("health", {}, timeout_seconds=0.05)
