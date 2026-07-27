from __future__ import annotations

from collections import defaultdict, deque
from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from ..domain.errors import PipelineValidationError


class HarnessGraphReconciler:
    def reconcile(self, projection: Mapping[str, Any]) -> dict[str, Any]:
        workflow = projection["workflow"]
        nodes = workflow["nodes"]
        edges = workflow["edges"]
        ids = {item["node_id"] for item in nodes}
        indegree = {node_id: 0 for node_id in ids}
        adjacency: dict[str, list[str]] = defaultdict(list)
        for edge in edges:
            source = edge["source_node_id"]
            target = edge["target_node_id"]
            adjacency[source].append(target)
            indegree[target] += 1
        ready = deque(sorted(node for node, count in indegree.items() if count == 0))
        order: list[str] = []
        while ready:
            node = ready.popleft()
            order.append(node)
            for target in sorted(adjacency[node]):
                indegree[target] -= 1
                if indegree[target] == 0:
                    ready.append(target)
        if len(order) != len(ids):
            raise PipelineValidationError("Harness workflow contains a cycle")
        entries = sorted(node for node, count in {node: 0 for node in ids}.items() if not any(edge["target_node_id"] == node for edge in edges))
        terminals = sorted(node for node in ids if not adjacency[node])
        if not entries or not terminals:
            raise PipelineValidationError("Harness workflow requires entry and terminal nodes")
        node_by_id = {item["node_id"]: item for item in nodes}
        orphaned = [node for node in ids if node not in entries and not any(edge["source_node_id"] == node or edge["target_node_id"] == node for edge in edges)]
        if orphaned:
            raise PipelineValidationError(f"Harness workflow has orphaned nodes: {sorted(orphaned)}")
        semantic_parity = {
            "definition_id": projection["definition_id"],
            "purpose": projection["purpose"],
            "category_id": projection["category_id"],
            "profile_id": projection["profile_id"],
            "semantic_dependencies": projection["semantic_dependencies"],
            "wrong_reading_locks": projection["wrong_reading_locks"],
            "evaluation_requirements": projection["evaluation_requirements"],
            "repair_laws": projection["repair_laws"],
        }
        return {
            "projection_id": projection["projection_id"],
            "node_count": len(nodes),
            "edge_count": len(edges),
            "entry_node_ids": entries,
            "terminal_node_ids": terminals,
            "topological_order": order,
            "runtime_projection_digest": canonical_sha256(workflow),
            "semantic_parity_digest": canonical_sha256(semantic_parity),
            "actor_kinds": sorted({node["actor_kind"] for node in nodes}),
            "roles": sorted({node["role"] for node in nodes}),
            "product_boundaries": sorted({node["product_boundary"] for node in nodes}),
            "node_ids": sorted(node_by_id),
        }
