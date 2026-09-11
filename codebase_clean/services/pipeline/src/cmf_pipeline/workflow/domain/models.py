from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from ...domain.enums import NodeKind, ProductBoundary, WorkflowRole
from ...domain.errors import PipelineValidationError
from ...domain.validation import reject_noncanonical, require_int, require_string, require_string_list, semantic_identity


def validate_runtime_node(node: Mapping[str, Any], index: int) -> dict[str, Any]:
    required = {
        "node_id",
        "capability_id",
        "phase_order",
        "purpose",
        "actor_kind",
        "role",
        "product_boundary",
        "input_contracts",
        "output_contracts",
        "side_effect_class",
        "implementation",
    }
    if set(node) != required:
        raise PipelineValidationError(f"runtime node {index} contains unknown or missing fields")
    actor = require_string(node["actor_kind"], f"nodes[{index}].actor_kind")
    role = require_string(node["role"], f"nodes[{index}].role")
    boundary = require_string(node["product_boundary"], f"nodes[{index}].product_boundary")
    if actor not in {item.value for item in NodeKind}:
        raise PipelineValidationError(f"unsupported node actor kind: {actor}")
    if role not in {item.value for item in WorkflowRole}:
        raise PipelineValidationError(f"unsupported workflow role: {role}")
    if boundary not in {item.value for item in ProductBoundary}:
        raise PipelineValidationError(f"unsupported product boundary: {boundary}")
    implementation = node["implementation"]
    if not isinstance(implementation, Mapping):
        raise PipelineValidationError("runtime node implementation must be an object")
    if set(implementation) != {
        "implementation_id",
        "implementation_version",
        "implementation_sha256",
        "owner_product",
        "implementation_kind",
        "side_effect_class",
        "authority_boundary",
    }:
        raise PipelineValidationError("runtime node implementation has invalid shape")
    normalized = {
        "node_id": require_string(node["node_id"], f"nodes[{index}].node_id"),
        "capability_id": require_string(node["capability_id"], f"nodes[{index}].capability_id"),
        "phase_order": require_int(node["phase_order"], f"nodes[{index}].phase_order"),
        "purpose": require_string(node["purpose"], f"nodes[{index}].purpose"),
        "actor_kind": actor,
        "role": role,
        "product_boundary": boundary,
        "input_contracts": require_string_list(node["input_contracts"], f"nodes[{index}].input_contracts"),
        "output_contracts": require_string_list(node["output_contracts"], f"nodes[{index}].output_contracts"),
        "side_effect_class": require_string(node["side_effect_class"], f"nodes[{index}].side_effect_class"),
        "implementation": {
            "implementation_id": require_string(implementation["implementation_id"], "implementation_id"),
            "implementation_version": require_string(implementation["implementation_version"], "implementation_version"),
            "implementation_sha256": require_string(implementation["implementation_sha256"], "implementation_sha256"),
            "owner_product": require_string(implementation["owner_product"], "owner_product"),
            "implementation_kind": require_string(implementation["implementation_kind"], "implementation_kind"),
            "side_effect_class": require_string(implementation["side_effect_class"], "implementation.side_effect_class"),
            "authority_boundary": require_string(implementation["authority_boundary"], "implementation.authority_boundary"),
        },
    }
    if normalized["side_effect_class"] != normalized["implementation"]["side_effect_class"]:
        raise PipelineValidationError("node side-effect class differs from bound implementation")
    if actor == NodeKind.HUMAN_GATE.value and boundary != ProductBoundary.STUDIO.value:
        raise PipelineValidationError("human gate must be projected through the Studio product boundary")
    if actor == NodeKind.EXTERNAL_PRODUCT.value and boundary == ProductBoundary.AHP.value:
        raise PipelineValidationError("external product node cannot claim the Pipeline product boundary")
    reject_noncanonical(normalized)
    return normalized


def validate_runtime_workflow(payload: Mapping[str, Any]) -> dict[str, Any]:
    required = {
        "source_projection_id",
        "binding_manifest_id",
        "category_id",
        "profile_id",
        "purpose",
        "semantic_dependency_refs",
        "nodes",
        "edges",
        "topological_order",
        "runtime_projection_digest",
        "semantic_parity_digest",
        "wrong_reading_locks",
        "evaluation_requirements",
        "repair_laws",
    }
    if set(payload) != required:
        raise PipelineValidationError("runtime workflow contains unknown or missing fields")
    nodes = [validate_runtime_node(item, index) for index, item in enumerate(payload["nodes"])]
    node_ids = [item["node_id"] for item in nodes]
    if len(node_ids) != len(set(node_ids)):
        raise PipelineValidationError("runtime workflow node IDs must be unique")
    edges = []
    for index, edge in enumerate(payload["edges"]):
        if not isinstance(edge, Mapping) or set(edge) != {"source_node_id", "target_node_id", "contract_id"}:
            raise PipelineValidationError(f"edge {index} has invalid shape")
        source = require_string(edge["source_node_id"], f"edges[{index}].source_node_id")
        target = require_string(edge["target_node_id"], f"edges[{index}].target_node_id")
        if source not in node_ids or target not in node_ids or source == target:
            raise PipelineValidationError("runtime edge references invalid nodes")
        edges.append({
            "source_node_id": source,
            "target_node_id": target,
            "contract_id": require_string(edge["contract_id"], f"edges[{index}].contract_id"),
        })
    topological = require_string_list(payload["topological_order"], "topological_order", non_empty=True, sorted_unique=False)
    if set(topological) != set(node_ids) or len(topological) != len(node_ids):
        raise PipelineValidationError("topological_order must include every node exactly once")
    normalized = {
        "source_projection_id": require_string(payload["source_projection_id"], "source_projection_id"),
        "binding_manifest_id": require_string(payload["binding_manifest_id"], "binding_manifest_id"),
        "category_id": require_string(payload["category_id"], "category_id"),
        "profile_id": require_string(payload["profile_id"], "profile_id"),
        "purpose": require_string(payload["purpose"], "purpose"),
        "semantic_dependency_refs": list(payload["semantic_dependency_refs"]),
        "nodes": sorted(nodes, key=lambda item: item["node_id"]),
        "edges": sorted(edges, key=lambda item: (item["source_node_id"], item["target_node_id"], item["contract_id"])),
        "topological_order": topological,
        "runtime_projection_digest": require_string(payload["runtime_projection_digest"], "runtime_projection_digest"),
        "semantic_parity_digest": require_string(payload["semantic_parity_digest"], "semantic_parity_digest"),
        "wrong_reading_locks": require_string_list(payload["wrong_reading_locks"], "wrong_reading_locks"),
        "evaluation_requirements": require_string_list(payload["evaluation_requirements"], "evaluation_requirements", non_empty=True),
        "repair_laws": require_string_list(payload["repair_laws"], "repair_laws", non_empty=True),
    }
    reject_noncanonical(normalized)
    return normalized
