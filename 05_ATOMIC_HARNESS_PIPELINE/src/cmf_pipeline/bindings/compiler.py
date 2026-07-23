from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from ..domain.errors import PipelineValidationError
from ..domain.validation import semantic_identity
from ..workflow.infrastructure.repository import PipelineRepository
from .eligibility_registry import ImplementationEligibilityRegistry


class HarnessExecutionBindingCompiler:
    def __init__(self, repository: PipelineRepository, registry: ImplementationEligibilityRegistry):
        self.repository = repository
        self.registry = registry

    def compile(
        self,
        projection: Mapping[str, Any],
        graph_receipt: Mapping[str, Any],
        *,
        idempotency_key: str,
    ) -> dict[str, Any]:
        bindings: list[dict[str, Any]] = []
        blockers: list[dict[str, Any]] = []
        for capability in projection["capabilities"]:
            candidates = self.registry.eligible(capability["capability_id"], capability["required_features"])
            if not candidates:
                blockers.append(
                    {
                        "capability_id": capability["capability_id"],
                        "code": "NO_ELIGIBLE_IMPLEMENTATION",
                        "required_features": capability["required_features"],
                    }
                )
                continue
            if len(candidates) > 1:
                blockers.append(
                    {
                        "capability_id": capability["capability_id"],
                        "code": "AMBIGUOUS_IMPLEMENTATION_BINDING",
                        "candidate_ids": [f"{item['implementation_id']}@{item['implementation_version']}" for item in candidates],
                    }
                )
                continue
            selected = candidates[0]
            bindings.append(
                {
                    "capability_id": capability["capability_id"],
                    "implementation_id": selected["implementation_id"],
                    "implementation_version": selected["implementation_version"],
                    "implementation_sha256": selected["candidate_sha256"],
                    "owner_product": selected["owner_product"],
                    "implementation_kind": selected["implementation_kind"],
                    "side_effect_class": selected["side_effect_class"],
                    "authority_boundary": selected["authority_boundary"],
                    "required_features": capability["required_features"],
                }
            )
        bindings = sorted(bindings, key=lambda item: item["capability_id"])
        blockers = sorted(blockers, key=lambda item: item["capability_id"])
        manifest_core = {
            "definition_id": projection["definition_id"],
            "definition_version": projection["definition_version"],
            "definition_semantic_sha256": projection["definition_semantic_sha256"],
            "projection_id": projection["projection_id"],
            "category_id": projection["category_id"],
            "profile_id": projection["profile_id"],
            "semantic_dependency_refs": projection["semantic_dependencies"],
            "graph_receipt": dict(graph_receipt),
            "bindings": bindings,
            "blockers": blockers,
            "execution_eligible": not blockers,
            "production_authorized": False,
            "certified": False,
        }
        manifest = {
            "manifest_id": semantic_identity("harness-binding", manifest_core),
            "manifest_version": "1.0.0",
            **manifest_core,
        }
        stored = self.repository.store_object(
            "harness_execution_binding_manifest",
            manifest,
            idempotency_key=idempotency_key,
            object_id=manifest["manifest_id"],
            lifecycle_state="ELIGIBLE_FOR_EXECUTION" if not blockers else "DENIED",
        )
        self.repository.add_edge(projection["projection_id"], manifest["manifest_id"], "compiled_to_binding")
        for ref in projection["semantic_dependencies"]:
            self.repository.add_edge(ref["object_id"], manifest["manifest_id"], "semantic_dependency")
        return stored
