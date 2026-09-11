from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..domain.models import validate_runtime_node
from ...domain.validation import require_ref_list, require_string_list, semantic_identity


class JITContextCompiler:
    def compile(
        self,
        node: Mapping[str, Any],
        *,
        context_refs: list[Mapping[str, Any]],
        allowed_actions: list[str],
        forbidden_actions: list[str],
        tool_ids: list[str],
        output_contracts: list[str] | None = None,
        evaluation_requirements: list[str] | None = None,
        expires_after_ms: int = 300_000,
    ) -> dict[str, Any]:
        normalized_node = validate_runtime_node(node, 0)
        allowed = require_string_list(sorted(allowed_actions), "allowed_actions")
        forbidden = require_string_list(sorted(forbidden_actions), "forbidden_actions")
        overlap = sorted(set(allowed) & set(forbidden))
        if overlap:
            raise ValueError(f"actions cannot be both allowed and forbidden: {overlap}")
        core = {
            "node_id": normalized_node["node_id"],
            "implementation_ref": {
                "object_id": normalized_node["implementation"]["implementation_id"],
                "version": normalized_node["implementation"]["implementation_version"],
                "sha256": normalized_node["implementation"]["implementation_sha256"],
            },
            "actor_kind": normalized_node["actor_kind"],
            "role": normalized_node["role"],
            "product_boundary": normalized_node["product_boundary"],
            "context_refs": require_ref_list(list(context_refs), "context_refs"),
            "allowed_actions": allowed,
            "forbidden_actions": forbidden,
            "tool_ids": require_string_list(sorted(tool_ids), "tool_ids"),
            "input_contracts": normalized_node["input_contracts"],
            "output_contracts": output_contracts or normalized_node["output_contracts"],
            "evaluation_requirements": sorted(evaluation_requirements or []),
            "expires_after_ms": int(expires_after_ms),
            "secrets_included": False,
            "unrestricted_context_included": False,
        }
        return {"capsule_id": semantic_identity("jit-capsule", core), "capsule_version": "1.0.0", **core}
