from __future__ import annotations

from contextlib import closing
import json
import sqlite3
from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_json_text, canonical_sha256, utc_now_rfc3339

from ...domain.enums import NodeState, RunState
from ...domain.errors import PipelineConflict, PipelineLifecycleError, PipelineNotFound, PipelineValidationError
from ...domain.validation import reject_noncanonical, require_ref, require_string, semantic_identity
from ..domain.models import validate_runtime_workflow
from ..infrastructure.repository import PipelineRepository
from .jit_context import JITContextCompiler
from .scheduler import DeterministicScheduler


class WorkflowRunService:
    def __init__(self, repository: PipelineRepository):
        self.repository = repository
        self.scheduler = DeterministicScheduler()
        self.jit = JITContextCompiler()

    def register_workflow(self, workflow: Mapping[str, Any]) -> dict[str, Any]:
        workflow_id = require_string(workflow.get("workflow_id"), "workflow_id")
        version = require_string(workflow.get("workflow_version"), "workflow_version")
        body = {key: value for key, value in workflow.items() if key not in {"workflow_id", "workflow_version"}}
        normalized = validate_runtime_workflow(body)
        expected = semantic_identity("runtime-workflow", normalized)
        if workflow_id != expected:
            raise PipelineValidationError("workflow_id does not match canonical runtime workflow")
        payload = {"workflow_id": workflow_id, "workflow_version": version, **normalized}
        self.scheduler.validate_topological_order(payload)
        self.repository.initialize()
        now = utc_now_rfc3339()
        with closing(self.repository._connect()) as connection:
            existing = connection.execute(
                "SELECT workflow_sha256, definition_json FROM pipeline_workflows WHERE workflow_id = ?",
                (workflow_id,),
            ).fetchone()
            workflow_sha = canonical_sha256(payload)
            if existing:
                if existing["workflow_sha256"] != workflow_sha or existing["definition_json"] != canonical_json_text(payload):
                    raise PipelineConflict("workflow identity collision with different bytes")
                return {"workflow": payload, "created": False}
            connection.execute(
                "INSERT INTO pipeline_workflows(workflow_id, workflow_sha256, definition_json, created_at_utc) VALUES(?, ?, ?, ?)",
                (workflow_id, workflow_sha, canonical_json_text(payload), now),
            )
        return {"workflow": payload, "created": True}

    def create_run(
        self,
        workflow_id: str,
        *,
        binding_manifest_ref: Mapping[str, Any],
        context_refs: list[Mapping[str, Any]],
        batch_ref: Mapping[str, Any] | None,
        idempotency_key: str,
        requested_run_id: str | None = None,
    ) -> dict[str, Any]:
        workflow_id = require_string(workflow_id, "workflow_id")
        binding_ref = require_ref(binding_manifest_ref, "binding_manifest_ref")
        context = [require_ref(item, f"context_refs[{index}]") for index, item in enumerate(context_refs)]
        context.sort(key=lambda item: item["object_id"])
        batch = require_ref(batch_ref, "batch_ref") if batch_ref is not None else None
        command_payload = {
            "workflow_id": workflow_id,
            "binding_manifest_ref": binding_ref,
            "context_refs": context,
            "batch_ref": batch,
            "requested_run_id": requested_run_id or "NOT_APPLICABLE",
        }

        def create(connection: sqlite3.Connection, timestamp: str) -> dict[str, Any]:
            workflow = self._workflow(connection, workflow_id)
            run_core = {
                "workflow_id": workflow_id,
                "workflow_sha256": canonical_sha256(workflow),
                "binding_manifest_ref": binding_ref,
                "context_refs": context,
                "batch_ref": batch,
            }
            derived = semantic_identity("pipeline-run", run_core)
            run_id = requested_run_id or derived
            if requested_run_id and requested_run_id != derived:
                raise PipelineValidationError("requested_run_id must equal the deterministic run identity")
            existing = connection.execute("SELECT * FROM pipeline_runs WHERE run_id = ?", (run_id,)).fetchone()
            if existing:
                return self._run_state(connection, run_id)
            run_json = {"run_id": run_id, "run_version": "1.0.0", **run_core}
            connection.execute(
                """
                INSERT INTO pipeline_runs(
                    run_id, workflow_id, state, revision, cancel_requested,
                    run_json, current_checkpoint_id, created_at_utc, updated_at_utc
                ) VALUES(?, ?, ?, 1, 0, ?, NULL, ?, ?)
                """,
                (run_id, workflow_id, RunState.CREATED.value, canonical_json_text(run_json), timestamp, timestamp),
            )
            for node in workflow["nodes"]:
                connection.execute(
                    """
                    INSERT INTO pipeline_node_states(
                        run_id, node_id, state, attempt_count, dispatch_ordinal,
                        output_ref_json, failure_json, updated_at_utc
                    ) VALUES(?, ?, ?, 0, NULL, NULL, NULL, ?)
                    """,
                    (run_id, node["node_id"], NodeState.BLOCKED.value, timestamp),
                )
            self._append_event(connection, run_id, "RunCreated", run_id, run_json, timestamp)
            connection.execute(
                "UPDATE pipeline_runs SET state = ?, revision = 2, updated_at_utc = ? WHERE run_id = ?",
                (RunState.RUNNING.value, timestamp, run_id),
            )
            self._append_event(connection, run_id, "RunStarted", run_id, {"state": RunState.RUNNING.value}, timestamp)
            return self._run_state(connection, run_id)

        return self.repository.execute_idempotent(
            command_type="create_pipeline_run",
            idempotency_key=idempotency_key,
            payload=command_payload,
            callback=create,
        )

    def ready_nodes(self, run_id: str) -> list[str]:
        self.repository.initialize()
        with closing(self.repository._connect()) as connection:
            run = self._run(connection, run_id)
            workflow = self._workflow(connection, run["workflow_id"])
            states = self._node_state_map(connection, run_id)
            return self.scheduler.ready_nodes(workflow, states)

    def safe_parallel_batch(self, run_id: str) -> list[str]:
        self.repository.initialize()
        with closing(self.repository._connect()) as connection:
            run = self._run(connection, run_id)
            workflow = self._workflow(connection, run["workflow_id"])
            states = self._node_state_map(connection, run_id)
            return self.scheduler.safe_parallel_batch(workflow, states)

    def dispatch_node(
        self,
        run_id: str,
        node_id: str,
        *,
        context_refs: list[Mapping[str, Any]],
        allowed_actions: list[str],
        forbidden_actions: list[str],
        tool_ids: list[str],
        idempotency_key: str,
    ) -> dict[str, Any]:
        run_id = require_string(run_id, "run_id")
        node_id = require_string(node_id, "node_id")
        command_payload = {
            "run_id": run_id,
            "node_id": node_id,
            "context_refs": list(context_refs),
            "allowed_actions": sorted(allowed_actions),
            "forbidden_actions": sorted(forbidden_actions),
            "tool_ids": sorted(tool_ids),
        }

        def dispatch(connection: sqlite3.Connection, timestamp: str) -> dict[str, Any]:
            run = self._run(connection, run_id)
            if run["state"] != RunState.RUNNING.value or run["cancel_requested"]:
                raise PipelineLifecycleError("run is not dispatchable")
            workflow = self._workflow(connection, run["workflow_id"])
            states = self._node_state_map(connection, run_id)
            if node_id not in self.scheduler.ready_nodes(workflow, states):
                raise PipelineLifecycleError(f"node is not ready: {node_id}")
            node = self._node(workflow, node_id)
            capsule = self.jit.compile(
                node,
                context_refs=context_refs,
                allowed_actions=allowed_actions,
                forbidden_actions=forbidden_actions,
                tool_ids=tool_ids,
                evaluation_requirements=workflow["evaluation_requirements"],
            )
            ordinal = int(
                connection.execute(
                    "SELECT COALESCE(MAX(dispatch_ordinal), 0) + 1 FROM pipeline_node_states WHERE run_id = ?",
                    (run_id,),
                ).fetchone()[0]
            )
            connection.execute(
                """
                UPDATE pipeline_node_states
                SET state = ?, attempt_count = attempt_count + 1,
                    dispatch_ordinal = ?, updated_at_utc = ?
                WHERE run_id = ? AND node_id = ?
                """,
                (NodeState.DISPATCHED.value, ordinal, timestamp, run_id, node_id),
            )
            self._bump_run(connection, run_id, timestamp)
            self._append_event(
                connection,
                run_id,
                "NodeDispatched",
                node_id,
                {"node_id": node_id, "dispatch_ordinal": ordinal, "jit_capsule": capsule},
                timestamp,
            )
            return {"run_id": run_id, "node_id": node_id, "state": NodeState.DISPATCHED.value, "jit_capsule": capsule}

        return self.repository.execute_idempotent(
            command_type="dispatch_workflow_node",
            idempotency_key=idempotency_key,
            payload=command_payload,
            callback=dispatch,
        )

    def start_node(self, run_id: str, node_id: str, *, idempotency_key: str) -> dict[str, Any]:
        return self._transition_node(
            run_id,
            node_id,
            expected={NodeState.DISPATCHED.value},
            target=NodeState.RUNNING.value,
            event_type="NodeStarted",
            idempotency_key=idempotency_key,
        )

    def complete_node(
        self,
        run_id: str,
        node_id: str,
        *,
        output_ref: Mapping[str, Any],
        validation_receipt_refs: list[str],
        idempotency_key: str,
    ) -> dict[str, Any]:
        output = require_ref(output_ref, "output_ref")
        if not validation_receipt_refs or validation_receipt_refs != sorted(set(validation_receipt_refs)):
            raise PipelineValidationError("validation_receipt_refs must be non-empty, sorted, and unique")
        payload = {
            "run_id": run_id,
            "node_id": node_id,
            "output_ref": output,
            "validation_receipt_refs": validation_receipt_refs,
        }

        def complete(connection: sqlite3.Connection, timestamp: str) -> dict[str, Any]:
            run = self._run(connection, run_id)
            row = self._node_row(connection, run_id, node_id)
            if row["state"] != NodeState.RUNNING.value:
                raise PipelineLifecycleError("only a RUNNING node can complete")
            late = bool(run["cancel_requested"]) or run["state"] in {
                RunState.CANCEL_REQUESTED.value,
                RunState.CANCELLED.value,
                RunState.INVALIDATED.value,
            }
            target = NodeState.QUARANTINED.value if late else NodeState.SUCCEEDED.value
            connection.execute(
                """
                UPDATE pipeline_node_states
                SET state = ?, output_ref_json = ?, updated_at_utc = ?
                WHERE run_id = ? AND node_id = ?
                """,
                (target, canonical_json_text(output), timestamp, run_id, node_id),
            )
            self._bump_run(connection, run_id, timestamp)
            event_type = "LateResultQuarantined" if late else "NodeSucceeded"
            self._append_event(
                connection,
                run_id,
                event_type,
                node_id,
                {"output_ref": output, "validation_receipt_refs": validation_receipt_refs, "consumable": not late},
                timestamp,
            )
            if late:
                self._finalize_cancel_if_possible(connection, run_id, timestamp)
            else:
                self._finalize_success_if_possible(connection, run_id, timestamp)
            return {"run_id": run_id, "node_id": node_id, "state": target, "output_ref": output, "consumable": not late}

        return self.repository.execute_idempotent(
            command_type="complete_workflow_node",
            idempotency_key=idempotency_key,
            payload=payload,
            callback=complete,
        )

    def fail_node(
        self,
        run_id: str,
        node_id: str,
        *,
        failure: Mapping[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        reject_noncanonical(failure)
        payload = {"run_id": run_id, "node_id": node_id, "failure": dict(failure)}

        def fail(connection: sqlite3.Connection, timestamp: str) -> dict[str, Any]:
            row = self._node_row(connection, run_id, node_id)
            if row["state"] != NodeState.RUNNING.value:
                raise PipelineLifecycleError("only a RUNNING node can fail")
            connection.execute(
                "UPDATE pipeline_node_states SET state = ?, failure_json = ?, updated_at_utc = ? WHERE run_id = ? AND node_id = ?",
                (NodeState.FAILED.value, canonical_json_text(failure), timestamp, run_id, node_id),
            )
            connection.execute(
                "UPDATE pipeline_runs SET state = ?, revision = revision + 1, updated_at_utc = ? WHERE run_id = ?",
                (RunState.FAILED.value, timestamp, run_id),
            )
            self._append_event(connection, run_id, "NodeFailed", node_id, dict(failure), timestamp)
            return {"run_id": run_id, "node_id": node_id, "state": NodeState.FAILED.value, "failure": dict(failure)}

        return self.repository.execute_idempotent(
            command_type="fail_workflow_node",
            idempotency_key=idempotency_key,
            payload=payload,
            callback=fail,
        )

    def pause_run(self, run_id: str, *, idempotency_key: str) -> dict[str, Any]:
        return self._transition_run(run_id, {RunState.RUNNING.value}, RunState.PAUSED.value, "RunPaused", idempotency_key)

    def resume_run(self, run_id: str, *, idempotency_key: str) -> dict[str, Any]:
        return self._transition_run(run_id, {RunState.PAUSED.value}, RunState.RUNNING.value, "RunResumed", idempotency_key)

    def cancel_run(self, run_id: str, *, reason: str, idempotency_key: str) -> dict[str, Any]:
        reason = require_string(reason, "reason")
        payload = {"run_id": run_id, "reason": reason}

        def cancel(connection: sqlite3.Connection, timestamp: str) -> dict[str, Any]:
            run = self._run(connection, run_id)
            if run["state"] in {RunState.CANCELLED.value, RunState.COMPLETED.value, RunState.FAILED.value}:
                raise PipelineLifecycleError(f"run cannot be cancelled from {run['state']}")
            connection.execute(
                "UPDATE pipeline_runs SET state = ?, cancel_requested = 1, revision = revision + 1, updated_at_utc = ? WHERE run_id = ?",
                (RunState.CANCEL_REQUESTED.value, timestamp, run_id),
            )
            connection.execute(
                """
                UPDATE pipeline_node_states
                SET state = ?, updated_at_utc = ?
                WHERE run_id = ? AND state IN (?, ?, ?)
                """,
                (
                    NodeState.CANCELLED.value,
                    timestamp,
                    run_id,
                    NodeState.BLOCKED.value,
                    NodeState.READY.value,
                    NodeState.DISPATCHED.value,
                ),
            )
            self._append_event(connection, run_id, "CancellationRequested", run_id, {"reason": reason}, timestamp)
            self._finalize_cancel_if_possible(connection, run_id, timestamp)
            return self._run_state(connection, run_id)

        return self.repository.execute_idempotent(
            command_type="cancel_pipeline_run",
            idempotency_key=idempotency_key,
            payload=payload,
            callback=cancel,
        )

    def checkpoint(self, run_id: str, *, idempotency_key: str) -> dict[str, Any]:
        payload = {"run_id": run_id}

        def save(connection: sqlite3.Connection, timestamp: str) -> dict[str, Any]:
            state = self._run_state(connection, run_id)
            sequence = int(
                connection.execute(
                    "SELECT COALESCE(MAX(sequence), 0) FROM pipeline_run_events WHERE run_id = ?",
                    (run_id,),
                ).fetchone()[0]
            )
            core = {"run_state": state, "event_sequence": sequence}
            checkpoint_id = semantic_identity("pipeline-checkpoint", core)
            snapshot_sha = canonical_sha256(core)
            connection.execute(
                """
                INSERT INTO pipeline_checkpoints(
                    checkpoint_id, run_id, event_sequence, snapshot_json,
                    snapshot_sha256, created_at_utc
                ) VALUES(?, ?, ?, ?, ?, ?)
                ON CONFLICT(checkpoint_id) DO NOTHING
                """,
                (checkpoint_id, run_id, sequence, canonical_json_text(core), snapshot_sha, timestamp),
            )
            connection.execute(
                "UPDATE pipeline_runs SET current_checkpoint_id = ?, revision = revision + 1, updated_at_utc = ? WHERE run_id = ?",
                (checkpoint_id, timestamp, run_id),
            )
            self._append_event(connection, run_id, "CheckpointAccepted", checkpoint_id, {"snapshot_sha256": snapshot_sha}, timestamp)
            return {"checkpoint_id": checkpoint_id, "run_id": run_id, "event_sequence": sequence, "snapshot_sha256": snapshot_sha}

        return self.repository.execute_idempotent(
            command_type="checkpoint_pipeline_run",
            idempotency_key=idempotency_key,
            payload=payload,
            callback=save,
        )

    def replay(self, run_id: str) -> dict[str, Any]:
        self.repository.initialize()
        with closing(self.repository._connect()) as connection:
            self._run(connection, run_id)
            rows = connection.execute(
                "SELECT * FROM pipeline_run_events WHERE run_id = ? ORDER BY sequence",
                (run_id,),
            ).fetchall()
            events = []
            expected_sequence = 1
            for row in rows:
                sequence = int(row["sequence"])
                if sequence != expected_sequence:
                    raise PipelineConflict("run event sequence contains a gap")
                payload = json.loads(row["payload_json"])
                if canonical_sha256(payload) != row["event_sha256"]:
                    raise PipelineConflict("run event payload hash mismatch")
                events.append({
                    "sequence": sequence,
                    "event_type": row["event_type"],
                    "aggregate_id": row["aggregate_id"],
                    "payload": payload,
                    "event_sha256": row["event_sha256"],
                })
                expected_sequence += 1
            state = self._run_state(connection, run_id)
            return {
                "run_id": run_id,
                "event_count": len(events),
                "event_stream_sha256": canonical_sha256(events),
                "events": events,
                "current_state": state,
                "historical_events_rewritten": False,
            }

    def status(self, run_id: str) -> dict[str, Any]:
        self.repository.initialize()
        with closing(self.repository._connect()) as connection:
            return self._run_state(connection, run_id)

    def _transition_node(
        self,
        run_id: str,
        node_id: str,
        *,
        expected: set[str],
        target: str,
        event_type: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        payload = {"run_id": run_id, "node_id": node_id, "target": target}

        def transition(connection: sqlite3.Connection, timestamp: str) -> dict[str, Any]:
            run = self._run(connection, run_id)
            if run["state"] != RunState.RUNNING.value or run["cancel_requested"]:
                raise PipelineLifecycleError("run is not executable")
            row = self._node_row(connection, run_id, node_id)
            if row["state"] not in expected:
                raise PipelineLifecycleError(f"node transition {row['state']} -> {target} is forbidden")
            connection.execute(
                "UPDATE pipeline_node_states SET state = ?, updated_at_utc = ? WHERE run_id = ? AND node_id = ?",
                (target, timestamp, run_id, node_id),
            )
            self._bump_run(connection, run_id, timestamp)
            self._append_event(connection, run_id, event_type, node_id, {"state": target}, timestamp)
            return {"run_id": run_id, "node_id": node_id, "state": target}

        return self.repository.execute_idempotent(
            command_type=event_type,
            idempotency_key=idempotency_key,
            payload=payload,
            callback=transition,
        )

    def _transition_run(self, run_id: str, expected: set[str], target: str, event_type: str, idempotency_key: str) -> dict[str, Any]:
        payload = {"run_id": run_id, "target": target}

        def transition(connection: sqlite3.Connection, timestamp: str) -> dict[str, Any]:
            run = self._run(connection, run_id)
            if run["state"] not in expected:
                raise PipelineLifecycleError(f"run transition {run['state']} -> {target} is forbidden")
            connection.execute(
                "UPDATE pipeline_runs SET state = ?, revision = revision + 1, updated_at_utc = ? WHERE run_id = ?",
                (target, timestamp, run_id),
            )
            self._append_event(connection, run_id, event_type, run_id, {"state": target}, timestamp)
            return self._run_state(connection, run_id)

        return self.repository.execute_idempotent(
            command_type=event_type,
            idempotency_key=idempotency_key,
            payload=payload,
            callback=transition,
        )

    @staticmethod
    def _workflow(connection: sqlite3.Connection, workflow_id: str) -> dict[str, Any]:
        row = connection.execute(
            "SELECT definition_json FROM pipeline_workflows WHERE workflow_id = ?",
            (workflow_id,),
        ).fetchone()
        if row is None:
            raise PipelineNotFound(f"workflow not found: {workflow_id}")
        return json.loads(row["definition_json"])

    @staticmethod
    def _node(workflow: Mapping[str, Any], node_id: str) -> dict[str, Any]:
        for node in workflow["nodes"]:
            if node["node_id"] == node_id:
                return dict(node)
        raise PipelineNotFound(f"workflow node not found: {node_id}")

    @staticmethod
    def _run(connection: sqlite3.Connection, run_id: str) -> sqlite3.Row:
        row = connection.execute("SELECT * FROM pipeline_runs WHERE run_id = ?", (run_id,)).fetchone()
        if row is None:
            raise PipelineNotFound(f"run not found: {run_id}")
        return row

    @staticmethod
    def _node_row(connection: sqlite3.Connection, run_id: str, node_id: str) -> sqlite3.Row:
        row = connection.execute(
            "SELECT * FROM pipeline_node_states WHERE run_id = ? AND node_id = ?",
            (run_id, node_id),
        ).fetchone()
        if row is None:
            raise PipelineNotFound(f"node state not found: {run_id}/{node_id}")
        return row

    @staticmethod
    def _node_state_map(connection: sqlite3.Connection, run_id: str) -> dict[str, str]:
        rows = connection.execute(
            "SELECT node_id, state FROM pipeline_node_states WHERE run_id = ? ORDER BY node_id",
            (run_id,),
        ).fetchall()
        return {str(row["node_id"]): str(row["state"]) for row in rows}

    def _run_state(self, connection: sqlite3.Connection, run_id: str) -> dict[str, Any]:
        run = self._run(connection, run_id)
        rows = connection.execute(
            "SELECT * FROM pipeline_node_states WHERE run_id = ? ORDER BY node_id",
            (run_id,),
        ).fetchall()
        nodes = [
            {
                "node_id": str(row["node_id"]),
                "state": str(row["state"]),
                "attempt_count": int(row["attempt_count"]),
                "dispatch_ordinal": row["dispatch_ordinal"],
                "output_ref": json.loads(row["output_ref_json"]) if row["output_ref_json"] else None,
                "failure": json.loads(row["failure_json"]) if row["failure_json"] else None,
            }
            for row in rows
        ]
        return {
            "run_id": run_id,
            "workflow_id": str(run["workflow_id"]),
            "state": str(run["state"]),
            "revision": int(run["revision"]),
            "cancel_requested": bool(run["cancel_requested"]),
            "current_checkpoint_id": run["current_checkpoint_id"],
            "nodes": nodes,
        }

    @staticmethod
    def _append_event(
        connection: sqlite3.Connection,
        run_id: str,
        event_type: str,
        aggregate_id: str,
        payload: Mapping[str, Any],
        timestamp: str,
    ) -> None:
        sequence = int(
            connection.execute(
                "SELECT COALESCE(MAX(sequence), 0) + 1 FROM pipeline_run_events WHERE run_id = ?",
                (run_id,),
            ).fetchone()[0]
        )
        connection.execute(
            """
            INSERT INTO pipeline_run_events(
                run_id, sequence, event_type, aggregate_id,
                payload_json, event_sha256, occurred_at_utc
            ) VALUES(?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                sequence,
                event_type,
                aggregate_id,
                canonical_json_text(payload),
                canonical_sha256(payload),
                timestamp,
            ),
        )

    @staticmethod
    def _bump_run(connection: sqlite3.Connection, run_id: str, timestamp: str) -> None:
        connection.execute(
            "UPDATE pipeline_runs SET revision = revision + 1, updated_at_utc = ? WHERE run_id = ?",
            (timestamp, run_id),
        )

    def _finalize_success_if_possible(self, connection: sqlite3.Connection, run_id: str, timestamp: str) -> None:
        states = [str(row[0]) for row in connection.execute("SELECT state FROM pipeline_node_states WHERE run_id = ?", (run_id,)).fetchall()]
        if states and all(state == NodeState.SUCCEEDED.value for state in states):
            connection.execute(
                "UPDATE pipeline_runs SET state = ?, revision = revision + 1, updated_at_utc = ? WHERE run_id = ?",
                (RunState.COMPLETED.value, timestamp, run_id),
            )
            self._append_event(connection, run_id, "RunCompleted", run_id, {"state": RunState.COMPLETED.value}, timestamp)

    def _finalize_cancel_if_possible(self, connection: sqlite3.Connection, run_id: str, timestamp: str) -> None:
        running = int(
            connection.execute(
                "SELECT COUNT(*) FROM pipeline_node_states WHERE run_id = ? AND state = ?",
                (run_id, NodeState.RUNNING.value),
            ).fetchone()[0]
        )
        if running == 0:
            connection.execute(
                "UPDATE pipeline_runs SET state = ?, revision = revision + 1, updated_at_utc = ? WHERE run_id = ?",
                (RunState.CANCELLED.value, timestamp, run_id),
            )
            self._append_event(connection, run_id, "RunCancelled", run_id, {"state": RunState.CANCELLED.value}, timestamp)
