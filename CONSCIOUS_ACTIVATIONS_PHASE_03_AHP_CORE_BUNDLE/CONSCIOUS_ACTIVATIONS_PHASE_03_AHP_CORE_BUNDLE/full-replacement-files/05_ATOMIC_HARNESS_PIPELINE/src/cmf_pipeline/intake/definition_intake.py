from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from ..domain.errors import PipelineValidationError
from ..domain.validation import reject_noncanonical, require_ref_list, require_semver, require_string, require_string_list, semantic_identity
from .compiler_profile_registry import CompilerProfile


class AtomicHarnessDefinitionIntake:
    REQUIRED_KEYS = {
        "definition_id",
        "definition_version",
        "category_id",
        "profile_id",
        "purpose",
        "semantic_dependencies",
        "capabilities",
        "workflow",
        "evaluation_requirements",
        "repair_laws",
        "wrong_reading_locks",
        "production_ready",
        "certified",
        "invalidation_state",
    }

    def validate(self, definition: Mapping[str, Any], profile: CompilerProfile) -> dict[str, Any]:
        if set(definition) != self.REQUIRED_KEYS:
            missing = sorted(self.REQUIRED_KEYS - set(definition))
            unknown = sorted(set(definition) - self.REQUIRED_KEYS)
            raise PipelineValidationError(f"Harness definition keys mismatch; missing={missing}, unknown={unknown}")
        normalized = {
            "definition_id": require_string(definition["definition_id"], "definition_id"),
            "definition_version": require_semver(definition["definition_version"], "definition_version"),
            "category_id": require_string(definition["category_id"], "category_id"),
            "profile_id": require_string(definition["profile_id"], "profile_id"),
            "purpose": require_string(definition["purpose"], "purpose"),
            "semantic_dependencies": require_ref_list(definition["semantic_dependencies"], "semantic_dependencies"),
            "capabilities": self._capabilities(definition["capabilities"]),
            "workflow": self._workflow(definition["workflow"]),
            "evaluation_requirements": require_string_list(definition["evaluation_requirements"], "evaluation_requirements", non_empty=True),
            "repair_laws": require_string_list(definition["repair_laws"], "repair_laws", non_empty=True),
            "wrong_reading_locks": require_string_list(definition["wrong_reading_locks"], "wrong_reading_locks"),
            "production_ready": definition["production_ready"],
            "certified": definition["certified"],
            "invalidation_state": require_string(definition["invalidation_state"], "invalidation_state"),
            "compiler_profile_id": profile.profile_id,
        }
        if normalized["production_ready"] is not False or normalized["certified"] is not False:
            raise PipelineValidationError("imported Harness cannot claim production or certification in Phase 3")
        if normalized["invalidation_state"] not in {"ACTIVE", "NOT_INVALIDATED"}:
            raise PipelineValidationError("invalidated or superseded Harness definition cannot be admitted")
        if normalized["category_id"] == "format02" or "format02" in normalized["profile_id"].lower():
            raise PipelineValidationError("Format 02 remains deferred")
        reject_noncanonical(normalized)
        normalized["definition_semantic_sha256"] = canonical_sha256(normalized)
        normalized["projection_id"] = semantic_identity("harness-projection", normalized)
        return normalized

    @staticmethod
    def _capabilities(value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list) or not value:
            raise PipelineValidationError("capabilities must be a non-empty list")
        normalized: list[dict[str, Any]] = []
        for index, item in enumerate(value):
            if not isinstance(item, Mapping) or set(item) != {"capability_id", "owner_kind", "required_features", "authority_boundary"}:
                raise PipelineValidationError(f"capabilities[{index}] has invalid shape")
            required = require_string_list(item["required_features"], f"capabilities[{index}].required_features")
            normalized.append(
                {
                    "capability_id": require_string(item["capability_id"], f"capabilities[{index}].capability_id"),
                    "owner_kind": require_string(item["owner_kind"], f"capabilities[{index}].owner_kind"),
                    "required_features": required,
                    "authority_boundary": require_string(item["authority_boundary"], f"capabilities[{index}].authority_boundary"),
                }
            )
        ids = [item["capability_id"] for item in normalized]
        if len(ids) != len(set(ids)):
            raise PipelineValidationError("capability IDs must be unique")
        return sorted(normalized, key=lambda item: item["capability_id"])

    @staticmethod
    def _workflow(value: Any) -> dict[str, Any]:
        if not isinstance(value, Mapping) or set(value) != {"nodes", "edges"}:
            raise PipelineValidationError("workflow must contain exactly nodes and edges")
        nodes = value["nodes"]
        edges = value["edges"]
        if not isinstance(nodes, list) or not nodes:
            raise PipelineValidationError("workflow.nodes must be non-empty")
        if not isinstance(edges, list):
            raise PipelineValidationError("workflow.edges must be a list")
        normalized_nodes = []
        for index, node in enumerate(nodes):
            required = {"node_id", "capability_id", "phase_order", "purpose", "actor_kind", "role", "product_boundary", "input_contracts", "output_contracts", "side_effect_class"}
            if not isinstance(node, Mapping) or set(node) != required:
                raise PipelineValidationError(f"workflow.nodes[{index}] has invalid shape")
            normalized_nodes.append(
                {
                    "node_id": require_string(node["node_id"], f"workflow.nodes[{index}].node_id"),
                    "capability_id": require_string(node["capability_id"], f"workflow.nodes[{index}].capability_id"),
                    "phase_order": int(node["phase_order"]),
                    "purpose": require_string(node["purpose"], f"workflow.nodes[{index}].purpose"),
                    "actor_kind": require_string(node["actor_kind"], f"workflow.nodes[{index}].actor_kind"),
                    "role": require_string(node["role"], f"workflow.nodes[{index}].role"),
                    "product_boundary": require_string(node["product_boundary"], f"workflow.nodes[{index}].product_boundary"),
                    "input_contracts": require_string_list(node["input_contracts"], f"workflow.nodes[{index}].input_contracts"),
                    "output_contracts": require_string_list(node["output_contracts"], f"workflow.nodes[{index}].output_contracts"),
                    "side_effect_class": require_string(node["side_effect_class"], f"workflow.nodes[{index}].side_effect_class"),
                }
            )
        ids = [item["node_id"] for item in normalized_nodes]
        if len(ids) != len(set(ids)):
            raise PipelineValidationError("workflow node IDs must be unique")
        normalized_edges = []
        for index, edge in enumerate(edges):
            if not isinstance(edge, Mapping) or set(edge) != {"source_node_id", "target_node_id", "contract_id"}:
                raise PipelineValidationError(f"workflow.edges[{index}] has invalid shape")
            source = require_string(edge["source_node_id"], f"workflow.edges[{index}].source_node_id")
            target = require_string(edge["target_node_id"], f"workflow.edges[{index}].target_node_id")
            if source not in ids or target not in ids or source == target:
                raise PipelineValidationError("workflow edge references unknown or identical nodes")
            normalized_edges.append(
                {
                    "source_node_id": source,
                    "target_node_id": target,
                    "contract_id": require_string(edge["contract_id"], f"workflow.edges[{index}].contract_id"),
                }
            )
        return {
            "nodes": sorted(normalized_nodes, key=lambda item: item["node_id"]),
            "edges": sorted(normalized_edges, key=lambda item: (item["source_node_id"], item["target_node_id"], item["contract_id"])),
        }
