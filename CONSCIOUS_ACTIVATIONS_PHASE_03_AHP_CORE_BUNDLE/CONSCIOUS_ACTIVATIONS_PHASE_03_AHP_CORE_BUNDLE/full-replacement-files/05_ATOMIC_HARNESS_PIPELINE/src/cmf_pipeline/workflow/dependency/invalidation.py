from __future__ import annotations

import sqlite3
from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_json_text

from ...domain.enums import NodeState, RunState
from ...domain.errors import PipelineValidationError
from ...domain.validation import require_string, require_string_list, semantic_identity
from ..infrastructure.repository import PipelineRepository
from .graph import RuntimeDependencyGraph


class RuntimeInvalidationPlanner:
    def __init__(self, repository: PipelineRepository):
        self.repository = repository
        self.graph = RuntimeDependencyGraph(repository)

    def plan(
        self,
        *,
        root_ids: list[str],
        reason: str,
        preserved_ids: list[str],
        replacement_refs: list[Mapping[str, Any]],
        idempotency_key: str,
    ) -> dict[str, Any]:
        roots = sorted(set(require_string(item, "root_id") for item in root_ids))
        if not roots:
            raise PipelineValidationError("invalidation requires at least one root")
        descendants = self.graph.descendants(roots)
        preserved = require_string_list(sorted(preserved_ids), "preserved_ids")
        overlap = sorted(set(descendants) & set(preserved))
        if overlap:
            raise PipelineValidationError(f"preserved IDs are descendants of invalidation roots: {overlap}")
        replacements = sorted((dict(item) for item in replacement_refs), key=lambda item: item["object_id"])
        core = {
            "root_ids": roots,
            "reason": require_string(reason, "reason"),
            "affected_descendant_ids": descendants,
            "preserved_ids": preserved,
            "replacement_refs": replacements,
            "historical_replay_policy": "PRESERVE_ALL_HISTORICAL_BYTES",
            "global_invalidation": False,
        }
        plan = {"plan_id": semantic_identity("runtime-invalidation", core), "plan_version": "1.0.0", **core}
        return self.repository.store_object(
            "runtime_invalidation_plan",
            plan,
            idempotency_key=idempotency_key,
            object_id=plan["plan_id"],
            lifecycle_state="PROPOSED",
        )

    def apply_to_run(self, run_id: str, plan: Mapping[str, Any], *, idempotency_key: str) -> dict[str, Any]:
        payload = {"run_id": require_string(run_id, "run_id"), "plan_id": require_string(plan["plan_id"], "plan_id")}

        def apply(connection: sqlite3.Connection, timestamp: str) -> dict[str, Any]:
            row = connection.execute("SELECT * FROM pipeline_runs WHERE run_id = ?", (run_id,)).fetchone()
            if row is None:
                raise PipelineValidationError(f"run not found: {run_id}")
            node_ids = {
                str(item[0])
                for item in connection.execute(
                    "SELECT node_id FROM pipeline_node_states WHERE run_id = ?", (run_id,)
                ).fetchall()
            }
            affected = sorted(node_ids & set(plan["affected_descendant_ids"] + plan["root_ids"]))
            if affected:
                placeholders = ",".join("?" for _ in affected)
                connection.execute(
                    f"UPDATE pipeline_node_states SET state = ?, updated_at_utc = ? WHERE run_id = ? AND node_id IN ({placeholders})",
                    (NodeState.INVALIDATED.value, timestamp, run_id, *affected),
                )
            connection.execute(
                "UPDATE pipeline_runs SET state = ?, revision = revision + 1, updated_at_utc = ? WHERE run_id = ?",
                (RunState.INVALIDATED.value, timestamp, run_id),
            )
            sequence = int(
                connection.execute(
                    "SELECT COALESCE(MAX(sequence),0)+1 FROM pipeline_run_events WHERE run_id = ?", (run_id,)
                ).fetchone()[0]
            )
            event_payload = {
                "plan_id": plan["plan_id"],
                "affected_node_ids": affected,
                "historical_bytes_preserved": True,
            }
            from ca_contracts import canonical_sha256
            connection.execute(
                "INSERT INTO pipeline_run_events(run_id, sequence, event_type, aggregate_id, payload_json, event_sha256, occurred_at_utc) VALUES(?, ?, 'RunInvalidated', ?, ?, ?, ?)",
                (run_id, sequence, run_id, canonical_json_text(event_payload), canonical_sha256(event_payload), timestamp),
            )
            return {"run_id": run_id, "state": RunState.INVALIDATED.value, "affected_node_ids": affected, "plan_id": plan["plan_id"]}

        return self.repository.execute_idempotent(
            command_type="apply_runtime_invalidation",
            idempotency_key=idempotency_key,
            payload=payload,
            callback=apply,
        )

    def rerun_plan(self, plan: Mapping[str, Any], *, reusable_checkpoint_ids: list[str]) -> dict[str, Any]:
        reusable = require_string_list(sorted(reusable_checkpoint_ids), "reusable_checkpoint_ids")
        core = {
            "invalidation_plan_id": plan["plan_id"],
            "rerun_target_ids": sorted(set(plan["root_ids"] + plan["affected_descendant_ids"])),
            "reusable_checkpoint_ids": reusable,
            "preserved_ids": plan["preserved_ids"],
            "unaffected_work_reused": True,
        }
        return {"rerun_plan_id": semantic_identity("selective-rerun", core), **core}
