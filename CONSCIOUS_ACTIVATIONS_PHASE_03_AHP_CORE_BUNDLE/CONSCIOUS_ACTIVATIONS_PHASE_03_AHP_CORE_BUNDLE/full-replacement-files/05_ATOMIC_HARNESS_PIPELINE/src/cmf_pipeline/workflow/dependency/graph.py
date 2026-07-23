from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ...domain.validation import require_string, semantic_identity
from ..infrastructure.repository import PipelineRepository


class RuntimeDependencyGraph:
    def __init__(self, repository: PipelineRepository):
        self.repository = repository

    def add_dependency(
        self,
        source_id: str,
        target_id: str,
        relation_type: str,
        *,
        evidence: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self.repository.add_edge(source_id, target_id, relation_type, evidence=evidence)

    def descendants(self, roots: list[str], relation_types: set[str] | None = None) -> list[str]:
        return self.repository.descendants(roots, relation_types=relation_types)

    def traversal_receipt(self, roots: list[str], relation_types: set[str] | None = None) -> dict[str, Any]:
        roots = sorted(set(require_string(item, "root_id") for item in roots))
        descendants = self.descendants(roots, relation_types)
        core = {
            "root_ids": roots,
            "relation_types": sorted(relation_types) if relation_types else ["ALL_CURRENT_RELATIONS"],
            "descendant_ids": descendants,
            "historical_edges_preserved": True,
        }
        return {"traversal_receipt_id": semantic_identity("graph-traversal", core), **core}
