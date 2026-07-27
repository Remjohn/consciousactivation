from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping
from typing import Any

from ...domain.enums import NodeState
from ...domain.errors import PipelineValidationError


class DeterministicScheduler:
    def ready_nodes(
        self,
        workflow: Mapping[str, Any],
        states: Mapping[str, str],
    ) -> list[str]:
        node_by_id = {item["node_id"]: item for item in workflow["nodes"]}
        predecessors: dict[str, set[str]] = defaultdict(set)
        for edge in workflow["edges"]:
            predecessors[edge["target_node_id"]].add(edge["source_node_id"])
        ready = []
        for node_id, node in node_by_id.items():
            state = states.get(node_id, NodeState.BLOCKED.value)
            if state not in {NodeState.BLOCKED.value, NodeState.READY.value}:
                continue
            if all(states.get(parent) == NodeState.SUCCEEDED.value for parent in predecessors[node_id]):
                ready.append(node)
        return [item["node_id"] for item in sorted(ready, key=lambda item: (item["phase_order"], item["node_id"]))]

    def safe_parallel_batch(
        self,
        workflow: Mapping[str, Any],
        states: Mapping[str, str],
    ) -> list[str]:
        ready_ids = self.ready_nodes(workflow, states)
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
        positions = {node_id: index for index, node_id in enumerate(workflow["topological_order"])}
        for edge in workflow["edges"]:
            if positions[edge["source_node_id"]] >= positions[edge["target_node_id"]]:
                raise PipelineValidationError("workflow topological order violates an edge")
