from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

from ...domain.enums import NodeState
from ...domain.errors import PipelineValidationError
from ..admission.causal_admission import (
    AncestorBinding,
    CausalAdmissionService,
    RequiredAncestor,
)


class DeterministicScheduler:
    def __init__(self, causal_admission: CausalAdmissionService | None = None):
        self.causal_admission = causal_admission or CausalAdmissionService()

    def ready_nodes(
        self,
        workflow: Mapping[str, Any],
        states: Mapping[str, str],
        *,
        ancestor_bindings: Mapping[str, AncestorBinding] | None = None,
        enforce_causal: bool = True,
    ) -> list[str]:
        node_by_id = {item["node_id"]: item for item in workflow["nodes"]}
        predecessors: dict[str, set[str]] = defaultdict(set)
        for edge in workflow["edges"]:
            predecessors[edge["target_node_id"]].add(edge["source_node_id"])
        ready = []
        topo = workflow.get("topological_order")
        phase_orders = {
            item["node_id"]: item.get("phase_order", 0) for item in workflow["nodes"]
        }
        for node_id, node in node_by_id.items():
            state = states.get(node_id, NodeState.BLOCKED.value)
            if state not in {NodeState.BLOCKED.value, NodeState.READY.value}:
                continue
            # Classic predecessor SUCCEEDED check
            if not all(
                states.get(parent) == NodeState.SUCCEEDED.value
                for parent in predecessors[node_id]
            ):
                continue

            if enforce_causal and predecessors[node_id]:
                required = [
                    RequiredAncestor(
                        ancestor_id=pid,
                        required_state=NodeState.SUCCEEDED.value,
                    )
                    for pid in predecessors[node_id]
                ]
                bindings = ancestor_bindings or {}
                # If no bindings provided, derive minimal from states only when SUCCEEDED
                # (bindings_from will skip those without identity — fail closed for integrity)
                result = self.causal_admission.evaluate(
                    node_id,
                    required_ancestors=required,
                    bindings=bindings,
                    node_states=states,
                    topological_order=topo,
                    phase_order=node.get("phase_order"),
                    ancestor_phase_orders=phase_orders,
                    force=False,
                )
                if not result.is_admitted:
                    # Not ready — causal block
                    continue

            ready.append(node)
        return [
            item["node_id"]
            for item in sorted(ready, key=lambda item: (item["phase_order"], item["node_id"]))
        ]

    def safe_parallel_batch(
        self,
        workflow: Mapping[str, Any],
        states: Mapping[str, str],
        *,
        ancestor_bindings: Mapping[str, AncestorBinding] | None = None,
        enforce_causal: bool = True,
    ) -> list[str]:
        ready_ids = self.ready_nodes(
            workflow,
            states,
            ancestor_bindings=ancestor_bindings,
            enforce_causal=enforce_causal,
        )
        node_by_id = {item["node_id"]: item for item in workflow["nodes"]}
        selected: list[str] = []
        occupied_effects: set[str] = set()
        for node_id in ready_ids:
            node = node_by_id[node_id]
            effect = node["side_effect_class"]
            if effect not in {"NONE", "READ_ONLY"} and effect in occupied_effects:
                continue
            selected.append(node_id)
            if effect not in {"NONE", "READ_ONLY"}:
                occupied_effects.add(effect)
        return selected

    def validate_topological_order(self, workflow: Mapping[str, Any]) -> None:
        positions = {
            node_id: index for index, node_id in enumerate(workflow["topological_order"])
        }
        for edge in workflow["edges"]:
            if positions[edge["source_node_id"]] >= positions[edge["target_node_id"]]:
                raise PipelineValidationError("workflow topological order violates an edge")

    def admit_node(
        self,
        workflow: Mapping[str, Any],
        states: Mapping[str, str],
        node_id: str,
        *,
        ancestor_bindings: Mapping[str, AncestorBinding] | None = None,
        force: bool = False,
    ):
        """
        Explicit causal admission gate used by dispatch paths.

        Raises CausalAdmissionError on failure (fail-closed).
        """
        node_by_id = {item["node_id"]: item for item in workflow["nodes"]}
        if node_id not in node_by_id:
            raise PipelineValidationError(f"unknown node_id: {node_id}")
        node = node_by_id[node_id]
        predecessors: set[str] = set()
        for edge in workflow.get("edges", []):
            if edge.get("target_node_id") == node_id:
                predecessors.add(edge["source_node_id"])
        required = [
            RequiredAncestor(ancestor_id=pid, required_state=NodeState.SUCCEEDED.value)
            for pid in predecessors
        ]
        phase_orders = {
            item["node_id"]: item.get("phase_order", 0) for item in workflow["nodes"]
        }
        return self.causal_admission.require_admitted(
            node_id,
            required_ancestors=required,
            bindings=ancestor_bindings or {},
            node_states=states,
            topological_order=workflow.get("topological_order"),
            phase_order=node.get("phase_order"),
            ancestor_phase_orders=phase_orders,
            force=force,
        )
