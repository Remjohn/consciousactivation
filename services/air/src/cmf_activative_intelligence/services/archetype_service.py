from __future__ import annotations

from typing import Any, Mapping

from ..repositories.air_repository import AirRepository
from ..repositories.registry_repository import RegistryRepository
from .semantic_authority import SemanticAuthorityService


class ArchetypeService:
    def __init__(
        self,
        repository: AirRepository,
        registries: RegistryRepository,
    ):
        self.repository = repository
        self.registries = registries
        self.semantic = SemanticAuthorityService(repository)

    def _validate_binding(self, binding: Mapping[str, Any]) -> None:
        evidence = self.registries.get_archetype(
            binding["archetype_ref"]["object_id"]
        )
        if evidence.immutable_ref() != binding["archetype_ref"]:
            raise ValueError("archetype_ref does not match exact historical evidence bytes")
        if not binding.get("current_validation_ref"):
            raise ValueError("historical archetype evidence requires current_validation_ref")
        if evidence.evidence_status != "historical_evidence_requires_current_coalition_validation":
            raise ValueError("unexpected archetype evidence lifecycle state")

    def store_program(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate(
            "archetype_coalition_program", payload
        )
        role_ref = normalized["role_tension_contract_ref"]
        role = self.repository.get_object(role_ref["object_id"])
        if role.object_type != "psychological_role_tension_contract":
            raise ValueError("role_tension_contract_ref identifies wrong type")
        if role.canonical_sha256 != role_ref["sha256"]:
            raise ValueError("role/tension contract hash mismatch")

        coalition_ref = normalized["primitive_coalition_ref"]
        coalition = self.repository.get_object(coalition_ref["object_id"])
        if coalition.object_type != "primitive_coalition_contract":
            raise ValueError("primitive_coalition_ref identifies wrong type")
        if coalition.canonical_sha256 != coalition_ref["sha256"]:
            raise ValueError("Primitive Coalition hash mismatch")

        coalition_binding_ids = {
            ref["object_id"] for ref in coalition.payload["binding_refs"]
        }
        bindings = [
            normalized["primary_archetype"],
            *normalized["supporting_archetypes"],
        ]
        archetype_binding_ids: set[str] = set()
        for binding in bindings:
            self._validate_binding(binding)
            unknown = set(binding["primitive_binding_ids"]) - coalition_binding_ids
            if unknown:
                raise ValueError(
                    f"archetype binding references Primitive Bindings outside coalition: {sorted(unknown)}"
                )
            binding_id = binding["binding_id"]
            if binding_id in archetype_binding_ids:
                raise ValueError("archetype binding IDs must be unique")
            archetype_binding_ids.add(binding_id)

        return self.semantic.store(
            "archetype_coalition_program",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )
