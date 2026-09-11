"""Fixture helpers for Studio supervision tests (TS-APP-API-006).

Provides ``make_running_campaign()`` and ``make_failed_node_run()`` helpers
that store a campaign in the PipelineRepository's content-addressed object
store (via the ``store_campaign()`` function in campaign_projection.py)
and optionally create a real pipeline run for it.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from cmf_pipeline.application import PipelineApplication

from api.services.campaign_projection import store_campaign


def minimal_order(campaign_id: str, **overrides: Any) -> dict[str, Any]:
    """Return a minimal CampaignOrder dict suitable for store_campaign()."""
    order = {
        "order_id": f"campaign-order:{campaign_id}",
        "workspace_id": "workspace:test",
        "project_id": "project:test",
        "source_kind": "CANONICAL_INTERVIEW_SOURCE_PACKAGE",
        "source_ref": {
            "object_id": "source:test",
            "version": "1.0.0",
            "sha256": "0" * 64,
        },
        "harness_ref": {
            "object_id": "harness:test",
            "version": "1.0.0",
            "sha256": "0" * 64,
        },
        "category_id": "conversational_activation_expression",
        "format_profile_id": "format07_direct_coaching_a_roll",
        "objective": "Test objective",
        "initial_seed": "Test seed",
        "taste_direction": ["identity-first"],
        "output_targets": [
            {
                "output_type": "SOURCE_LED_SHORT",
                "quantity": 1,
                "profile_id": "format07_direct_coaching_a_roll",
            }
        ],
        "budget_units": 100,
        "deadline_utc": None,
        "autonomy_policy": {
            "mode": "AUTOPILOT",
            "checkpoint_ids": [],
            "exception_only": True,
            "final_review_required": False,
            "publication_authority_required": True,
        },
        "operator_actor": {
            "actor_id": "operator:test",
            "actor_type": "human",
            "product_id": "conscious-activations-studio",
            "workflow_role": "operator",
        },
        "authority": {
            "authority_id": "ca-program-control-v2.1-candidate",
            "authority_version": "2.1.0-candidate",
            "authority_sha256": "0" * 64,
            "authority_state": "candidate_not_current",
        },
    }
    order.update(overrides)
    return order


def minimal_state(campaign_id: str, **overrides: Any) -> dict[str, Any]:
    """Return a minimal CampaignState dict for the given campaign_id."""
    state = {
        "campaign_id": campaign_id,
        "order_ref": {
            "object_id": f"campaign-order:{campaign_id}",
            "version": "1.0.0",
            "sha256": "0" * 64,
        },
        "lifecycle_state": "RUNNING",
        "autonomy_mode": "AUTOPILOT",
        "active_checkpoint_id": None,
        "exception_ids": [],
        "run_refs": [],
        "artifact_refs": [],
        "evaluation_refs": [],
        "version": 1,
    }
    state.update(overrides)
    return state


def make_running_campaign(
    pipeline: PipelineApplication,
    campaign_id: str,
    *,
    idempotency_key: str = "fixture-running",
    lifecycle_state: str = "RUNNING",
) -> dict[str, Any]:
    """Store a campaign in ``RUNNING`` lifecycle state.

    Returns the stored state dict.
    """
    state = minimal_state(campaign_id, lifecycle_state=lifecycle_state)
    order = minimal_order(campaign_id)
    return store_campaign(
        pipeline, campaign_id, order, state,
        idempotency_key=idempotency_key,
    )


def make_failed_node_run(
    pipeline: PipelineApplication,
    campaign_id: str,
    *,
    idempotency_key: str = "fixture-failed",
) -> dict[str, Any]:
    """Store a campaign with a real pipeline run that has a failed node.

    Creates a demo harness run, lets one node fail, and records the run_ref
    in the campaign state.
    """
    import tempfile
    from pathlib import Path

    from cmf_pipeline.demo import write_demo_harness
    from ca_contracts import canonical_sha256

    # Create a run
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        package = root / "reference-harness.zip"
        write_demo_harness(package)
        imported = pipeline.import_harness_package(
            package, idempotency_key=f"{idempotency_key}-import"
        )
        binding_result = pipeline.compile_binding(
            imported["projection"],
            imported["graph_receipt"],
            idempotency_key=f"{idempotency_key}-binding",
        )
        binding = binding_result["object"]["payload"]
        workflow_result = pipeline.compile_workflow(
            imported["projection"],
            binding,
            imported["graph_receipt"],
            idempotency_key=f"{idempotency_key}-workflow",
        )
        workflow = workflow_result["object"]["payload"]

        binding_ref = {
            "object_id": binding["manifest_id"],
            "version": "1.0.0",
            "sha256": canonical_sha256(
                {"seed": binding_result["object"]["canonical_sha256"]}
            ),
        }
        run = pipeline.runs.create_run(
            workflow["workflow_id"],
            binding_manifest_ref=binding_ref,
            context_refs=imported["projection"]["semantic_dependencies"],
            batch_ref=None,
            idempotency_key=f"{idempotency_key}-run",
        )
        run_id = run["run_id"]

    # Dispatch, start, then fail the first node. fail_node() requires the
    # node to be in RUNNING state, so we must dispatch and start it first
    # (exactly as drive_node_to_success does, but calling fail_node instead
    # of complete_node at the end).
    from tests.api._pipeline_fixtures import get_topological_order
    topo = get_topological_order(pipeline, run_id)
    if topo:
        first_node_id = topo[0]
        pipeline.runs.dispatch_node(
            run_id, first_node_id,
            context_refs=[], allowed_actions=["inspect"], forbidden_actions=[],
            tool_ids=["test-adapter"],
            idempotency_key=f"{idempotency_key}-dispatch",
        )
        pipeline.runs.start_node(
            run_id, first_node_id,
            idempotency_key=f"{idempotency_key}-start",
        )
        pipeline.runs.fail_node(
            run_id, first_node_id,
            failure={"code": "TEST_FAILURE", "message": "Intentional test failure"},
            idempotency_key=f"{idempotency_key}-fail",
        )

    # Store campaign with the run ref
    run_ref = {
        "object_id": run_id,
        "version": "1.0.0",
        "sha256": canonical_sha256({"run_id": run_id}),
    }
    state = minimal_state(
        campaign_id,
        lifecycle_state="BLOCKED_EXCEPTION",
        run_refs=[run_ref],
    )
    order = minimal_order(campaign_id)
    return store_campaign(
        pipeline, campaign_id, order, state,
        idempotency_key=f"{idempotency_key}-store",
    )