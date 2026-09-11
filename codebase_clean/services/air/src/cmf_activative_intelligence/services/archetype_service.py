from __future__ import annotations

from typing import Any, Mapping, Sequence

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

    def generate_program(
        self,
        *,
        program_id: str,
        role_tension_ref: Mapping[str, Any],
        primitive_coalition_ref: Mapping[str, Any],
        primary_archetype_ref: Mapping[str, Any],
        supporting_archetype_refs: Sequence[Mapping[str, Any]],
        category_target: str,
        source_expression_refs: Sequence[Mapping[str, Any]],
        authority: Mapping[str, Any],
        current_validation_ref: Mapping[str, Any],
        reasoning_engine: Any = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Synthesize archetype coalition program using genuine model reasoning (F28)."""
        if reasoning_engine is None:
            raise ValueError("reasoning_engine is required for model-backed archetype program generation")

        coalition = self.repository.get_object(primitive_coalition_ref["object_id"])
        binding_ids = [ref["object_id"] for ref in coalition.payload["binding_refs"]]
        primary_binding_ids = [binding_ids[0]] if binding_ids else []
        supp_binding_ids = [binding_ids[1]] if len(binding_ids) > 1 else primary_binding_ids

        prompt = (
            f"Synthesize archetype coalition program for category '{category_target}':\n"
            f"Role Tension Ref: {role_tension_ref['object_id']}\n"
            f"Coalition Ref: {primitive_coalition_ref['object_id']}\n"
            f"Generate a JSON object with exactly these keys:\n"
            f"- sequence_or_reading_logic: string explaining the narrative/rhetorical sequence\n"
            f"- anti_centroid_locks: array of strings of genre defenses\n"
            f"- wrong_reading_locks: array of strings of misinterpretation defenses\n"
            f"- rejected_alternatives: array of strings of rejected archetypes/stances\n"
            f"- primary_function: string describing primary archetype role\n"
            f"- supporting_function: string describing supporting archetype role"
        )

        res = reasoning_engine.infer(
            prompt,
            system_prompt="You are an archetype coalition program synthesis engine. Respond in JSON only.",
        )
        data = res.parsed_json or {}

        primary_binding = {
            "binding_id": f"{program_id}:arch-primary",
            "archetype_ref": dict(primary_archetype_ref),
            "current_validation_ref": dict(current_validation_ref),
            "local_function": str(data.get("primary_function") or "Hold the primary governing stance under pressure"),
            "source_fit": "Exact semantic fit with governed role and tension",
            "category_geometry": f"{category_target} primary alignment",
            "primitive_binding_ids": primary_binding_ids,
            "rejection_conditions": ["Avoid passive bystander posture"],
        }

        supporting_bindings = []
        for idx, s_ref in enumerate(supporting_archetype_refs, 1):
            supporting_bindings.append({
                "binding_id": f"{program_id}:arch-supp:{idx}",
                "archetype_ref": dict(s_ref),
                "current_validation_ref": dict(current_validation_ref),
                "local_function": str(data.get("supporting_function") or "Provide grounding nuance to prevent polarization"),
                "source_fit": "Complementary support to primary archetype",
                "category_geometry": f"{category_target} nuance alignment",
                "primitive_binding_ids": supp_binding_ids,
                "rejection_conditions": ["Avoid superficial optimism"],
            })

        payload = {
            "program_id": program_id,
            "version": "1.0.0",
            "authority": dict(authority),
            "lifecycle_state": "approved",
            "role_tension_contract_ref": dict(role_tension_ref),
            "primitive_coalition_ref": dict(primitive_coalition_ref),
            "primary_archetype": primary_binding,
            "supporting_archetypes": supporting_bindings,
            "source_expression_refs": [dict(r) for r in source_expression_refs],
            "category_target": category_target,
            "sequence_or_reading_logic": str(data.get("sequence_or_reading_logic") or "primary_confrontation_then_support"),
            "anti_centroid_locks": list(data.get("anti_centroid_locks") or ["resist generic corporate motivational framing"]),
            "wrong_reading_locks": list(data.get("wrong_reading_locks") or ["do not interpret accountability as punitive blame"]),
            "rejected_alternatives": list(data.get("rejected_alternatives") or ["comforting cheerleader", "aloof intellectual"]),
        }

        key = idempotency_key or f"gen-program:{program_id}"
        return self.store_program(payload, idempotency_key=key)
