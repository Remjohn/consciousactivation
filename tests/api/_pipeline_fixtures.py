"""Shared fixture helpers for pipeline status WebSocket and REST tests.

Builds a minimal, valid runtime workflow and drives it exactly the way
demo.py drives one — dispatch/start/complete per node — since no
automatic worker exists yet (Gap A) to do this for us.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ca_contracts import canonical_sha256
from cmf_pipeline.application import PipelineApplication
from cmf_pipeline.demo import write_demo_harness


def make_run(
    pipeline: PipelineApplication,
    *,
    idempotency_key_prefix: str = "test-fixture",
    batch_ref: dict[str, Any] | None = None,
) -> str:
    """Create a workflow registration and a run from the demo reference harness.

    Returns the created ``run_id``.

    Parameters
    ----------
    batch_ref : dict, optional
        A batch reference dict with ``object_id``, ``version``, ``sha256``.
        When omitted (the default) the run is created with ``batch_ref=None``.
        Providing different batch refs produces distinct deterministic run IDs
        from the same workflow.
    """
    from cmf_pipeline.demo import write_demo_harness

    import tempfile

    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        package = root / "reference-harness.zip"
        write_demo_harness(package)
        imported = pipeline.import_harness_package(
            package, idempotency_key=f"{idempotency_key_prefix}-import"
        )
        binding_result = pipeline.compile_binding(
            imported["projection"],
            imported["graph_receipt"],
            idempotency_key=f"{idempotency_key_prefix}-binding",
        )
        binding = binding_result["object"]["payload"]
        workflow_result = pipeline.compile_workflow(
            imported["projection"],
            binding,
            imported["graph_receipt"],
            idempotency_key=f"{idempotency_key_prefix}-workflow",
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
            batch_ref=batch_ref,
            idempotency_key=f"{idempotency_key_prefix}-run",
        )
        return run["run_id"]


def drive_node_to_success(
    pipeline: PipelineApplication,
    run_id: str,
    node_id: str,
    ordinal: int,
    *,
    idempotency_key_prefix: str = "test-fixture",
) -> None:
    """Dispatch, start, and complete a single node synchronously."""
    pipeline.runs.dispatch_node(
        run_id,
        node_id,
        context_refs=[],
        allowed_actions=["inspect"],
        forbidden_actions=[],
        tool_ids=["test-adapter"],
        idempotency_key=f"{idempotency_key_prefix}-dispatch-{ordinal}",
    )
    pipeline.runs.start_node(
        run_id,
        node_id,
        idempotency_key=f"{idempotency_key_prefix}-start-{ordinal}",
    )
    pipeline.runs.complete_node(
        run_id,
        node_id,
        output_ref={
            "object_id": f"output:{node_id}",
            "sha256": "0" * 64,
            "version": "1.0.0",
        },
        validation_receipt_refs=[f"validation:{ordinal}"],
        idempotency_key=f"{idempotency_key_prefix}-complete-{ordinal}",
    )


def get_topological_order(pipeline: PipelineApplication, run_id: str) -> list[str]:
    """Get the topological order for nodes in a run by inspecting the workflow.

    This walks through the event stream to find the workflow_id, then reads it
    from the repository.
    """
    status = pipeline.runs.status(run_id)
    workflow_id = status["workflow_id"]

    # Read the workflow definition from the repository
    import sqlite3
    from contextlib import closing

    repo = pipeline.repository
    with closing(repo._connect()) as conn:
        row = conn.execute(
            "SELECT definition_json FROM pipeline_workflows WHERE workflow_id = ?",
            (workflow_id,),
        ).fetchone()
    if row is None:
        raise ValueError(f"workflow {workflow_id} not found")
    definition = json.loads(row["definition_json"])
    return definition["topological_order"]