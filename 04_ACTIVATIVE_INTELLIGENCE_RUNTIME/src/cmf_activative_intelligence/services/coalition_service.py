from __future__ import annotations

from typing import Any, Mapping

from ca_contracts import canonical_sha256

from ..repositories.air_repository import AirRepository
from ..repositories.registry_repository import RegistryRepository
from .semantic_authority import SemanticAuthorityService


class CoalitionService:
    def __init__(
        self,
        repository: AirRepository,
        registries: RegistryRepository,
    ):
        self.repository = repository
        self.registries = registries
        self.semantic = SemanticAuthorityService(repository)

    @staticmethod
    def signature_fingerprint(signature: Mapping[str, Any]) -> str:
        payload = dict(signature)
        payload.pop("canonical_fingerprint", None)
        return canonical_sha256(payload)

    def store_coalition(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate(
            "primitive_coalition_contract", payload
        )
        expected_fingerprint = self.signature_fingerprint(normalized["signature"])
        if normalized["signature"]["canonical_fingerprint"] != expected_fingerprint:
            raise ValueError("Coalition Signature fingerprint does not match signature fields")

        bindings = []
        role_refs: set[tuple[str, str]] = set()
        primitive_refs: list[dict[str, str]] = []
        for binding_ref in normalized["binding_refs"]:
            binding = self.repository.get_object(binding_ref["object_id"])
            if binding.object_type != "primitive_binding":
                raise ValueError("binding_ref identifies the wrong object type")
            if binding.canonical_sha256 != binding_ref["sha256"]:
                raise ValueError("binding_ref hash does not match current bytes")
            bindings.append(binding)
            role_ref = binding.payload["role_tension_ref"]
            role_refs.add((role_ref["object_id"], role_ref["sha256"]))
            primitive_refs.append(dict(binding.payload["primitive_ref"]))
        if len(role_refs) != 1:
            raise ValueError("all Primitive Bindings in one coalition must share one role/tension contract")

        known_conflicts: set[tuple[str, str]] = set()
        primitive_ids = [item["object_id"] for item in primitive_refs]
        for primitive_ref in primitive_refs:
            primitive_id = primitive_ref["object_id"]
            record = self.registries.get_primitive(
                primitive_id, source_sha256=primitive_ref["sha256"]
            )
            for other in record.conflicts_with:
                if other in primitive_ids:
                    known_conflicts.add(tuple(sorted((primitive_id, other))))
        if known_conflicts:
            resolution_text = " ".join(normalized["conflict_resolutions"])
            unresolved = [
                pair
                for pair in sorted(known_conflicts)
                if not all(item in resolution_text for item in pair)
            ]
            if unresolved:
                raise ValueError(
                    f"known Primitive conflicts require explicit pair-specific resolution: {unresolved}"
                )

        matrix_ref = normalized["edge_product"]["matrix_of_edging_ref"]
        matrix = self.repository.get_object(matrix_ref["object_id"])
        if matrix.object_type != "matrix_of_edging":
            raise ValueError("Edge Product matrix_of_edging_ref identifies wrong type")
        if matrix.canonical_sha256 != matrix_ref["sha256"]:
            raise ValueError("Edge Product matrix reference hash mismatch")

        for risk_ref in normalized["misuse_risk_refs"]:
            risk = self.repository.get_object(risk_ref["object_id"])
            if risk.object_type != "primitive_misuse_risk":
                raise ValueError("coalition misuse_risk_ref identifies wrong type")
            if risk.canonical_sha256 != risk_ref["sha256"]:
                raise ValueError("coalition misuse risk hash mismatch")

        return self.semantic.store(
            "primitive_coalition_contract",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def store_evaluation(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate(
            "primitive_evaluation_receipt", payload
        )
        coalition_ref = normalized["coalition_ref"]
        coalition = self.repository.get_object(coalition_ref["object_id"])
        if coalition.object_type != "primitive_coalition_contract":
            raise ValueError("coalition_ref identifies wrong object type")
        if coalition.canonical_sha256 != coalition_ref["sha256"]:
            raise ValueError("coalition_ref hash does not match current bytes")
        expected = {
            ref["object_id"] for ref in coalition.payload["binding_refs"]
        }
        observed = {
            item["binding_ref"]["object_id"]
            for item in normalized["binding_results"]
        }
        if expected != observed:
            raise ValueError(
                "Primitive Evaluation Receipt must evaluate every coalition binding exactly once"
            )
        return self.semantic.store(
            "primitive_evaluation_receipt",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )
