from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from ...domain.errors import PipelineValidationError
from ...domain.validation import semantic_identity
from ..domain.models import validate_runtime_workflow
from ..infrastructure.repository import PipelineRepository


class RuntimeWorkflowCompiler:
    def __init__(self, repository: PipelineRepository):
        self.repository = repository

    def compile(
        self,
        projection: Mapping[str, Any],
        binding_manifest: Mapping[str, Any],
        graph_receipt: Mapping[str, Any],
        *,
        idempotency_key: str,
    ) -> dict[str, Any]:
        if not binding_manifest.get("execution_eligible"):
            raise PipelineValidationError("binding manifest is not execution eligible")
        if binding_manifest["projection_id"] != projection["projection_id"]:
            raise PipelineValidationError("binding manifest and Harness projection mismatch")
        bindings = {item["capability_id"]: item for item in binding_manifest["bindings"]}
        nodes: list[dict[str, Any]] = []
        for node in projection["workflow"]["nodes"]:
            try:
                binding = bindings[node["capability_id"]]
            except KeyError as exc:
                raise PipelineValidationError(
                    f"workflow node capability has no binding: {node['capability_id']}"
                ) from exc
            nodes.append(
                {
                    **node,
                    "implementation": {
                        "implementation_id": binding["implementation_id"],
                        "implementation_version": binding["implementation_version"],
                        "implementation_sha256": binding["implementation_sha256"],
                        "owner_product": binding["owner_product"],
                        "implementation_kind": binding["implementation_kind"],
                        "side_effect_class": binding["side_effect_class"],
                        "authority_boundary": binding["authority_boundary"],
                    },
                }
            )
        runtime_projection = {
            "source_projection_id": projection["projection_id"],
            "binding_manifest_id": binding_manifest["manifest_id"],
            "category_id": projection["category_id"],
            "profile_id": projection["profile_id"],
            "purpose": projection["purpose"],
            "semantic_dependency_refs": projection["semantic_dependencies"],
            "nodes": nodes,
            "edges": projection["workflow"]["edges"],
            "topological_order": graph_receipt["topological_order"],
            "runtime_projection_digest": canonical_sha256({"nodes": nodes, "edges": projection["workflow"]["edges"]}),
            "semantic_parity_digest": graph_receipt["semantic_parity_digest"],
            "wrong_reading_locks": projection["wrong_reading_locks"],
            "evaluation_requirements": projection["evaluation_requirements"],
            "repair_laws": projection["repair_laws"],
        }
        normalized = validate_runtime_workflow(runtime_projection)
        workflow = {
            "workflow_id": semantic_identity("runtime-workflow", normalized),
            "workflow_version": "1.0.0",
            **normalized,
        }
        stored = self.repository.store_object(
            "runtime_workflow_definition",
            workflow,
            idempotency_key=idempotency_key,
            object_id=workflow["workflow_id"],
            lifecycle_state="COMPILED",
        )
        self.repository.add_edge(projection["projection_id"], workflow["workflow_id"], "compiled_to_runtime_workflow")
        self.repository.add_edge(binding_manifest["manifest_id"], workflow["workflow_id"], "bound_by_manifest")
        for edge in workflow["edges"]:
            self.repository.add_edge(
                edge["source_node_id"],
                edge["target_node_id"],
                "workflow_dependency",
                evidence={"workflow_id": workflow["workflow_id"], "contract_id": edge["contract_id"]},
            )
        return stored
