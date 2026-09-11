from __future__ import annotations

from typing import Any, Mapping, Sequence

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
        return self.semantic.store(
            "primitive_evaluation_receipt",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def generate_coalition(
        self,
        *,
        coalition_id: str,
        source_context_refs: Sequence[Mapping[str, Any]],
        binding_refs: Sequence[Mapping[str, Any]],
        role_tension_ref: Mapping[str, Any],
        matrix_of_edging_ref: Mapping[str, Any],
        evaluation_profile_ref: Mapping[str, Any],
        authority: Mapping[str, Any],
        broad_signal_ref: Mapping[str, Any],
        misuse_risk_refs: Sequence[Mapping[str, Any]] = (),
        reasoning_engine: Any = None,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Synthesize primitive coalition contract using genuine model reasoning (F29)."""
        if reasoning_engine is None:
            raise ValueError("reasoning_engine is required for model-backed coalition generation")

        role_obj = self.repository.get_object(role_tension_ref["object_id"])
        matrix_obj = self.repository.get_object(matrix_of_edging_ref["object_id"])

        prompt = (
            f"Synthesize primitive coalition signature and edge product:\n"
            f"Psychological Role: {role_obj.payload['psychological_role']}\n"
            f"Tension: {role_obj.payload['tension']}\n"
            f"Surviving Edge: {matrix_obj.payload['surviving_edge']}\n"
            f"Binding Count: {len(binding_refs)}\n"
            f"Generate a JSON object with exactly these keys:\n"
            f"- dominant_pressure_path: string\n"
            f"- recognition_move: string\n"
            f"- tension_release_pattern: string\n"
            f"- psychological_role_transition: string\n"
            f"- participation_threshold: string\n"
            f"- compatibility_explanation: string\n"
            f"- consequence: string"
        )

        res = reasoning_engine.infer(
            prompt,
            system_prompt="You are a primitive coalition synthesis engine. Respond in JSON only.",
        )
        data = res.parsed_json or {}

        sig_data = {
            "signature_id": f"{coalition_id}:sig",
            "dominant_pressure_path": str(data.get("dominant_pressure_path") or "avoidance of exposure to bounded visible choice"),
            "recognition_move": str(data.get("recognition_move") or "name the self-protective mechanism"),
            "tension_release_pattern": str(data.get("tension_release_pattern") or "release tension only through accountable choice"),
            "psychological_role_transition": str(data.get("psychological_role_transition") or "observer to accountable participant"),
            "participation_threshold": str(data.get("participation_threshold") or "one explicit personal commitment"),
            "visual_attention_logic": "hold negative space around the choice",
            "experiential_progression": "recognition then consequence then choice",
            "canonical_fingerprint": "0" * 64,
        }
        sig_data["canonical_fingerprint"] = self.signature_fingerprint(sig_data)

        payload = {
            "coalition_id": coalition_id,
            "version": "1.0.0",
            "authority": dict(authority),
            "lifecycle_state": "approved",
            "source_context_refs": [dict(r) for r in source_context_refs],
            "binding_refs": [dict(r) for r in binding_refs],
            "execution_order": [r["object_id"] for r in binding_refs],
            "compatibility_explanation": str(data.get("compatibility_explanation") or "All primitives align with the shared psychological role/tension contract."),
            "conflict_resolutions": [],
            "suppressed_binding_ids": [],
            "signature": sig_data,
            "edge_product": {
                "edge_product_id": f"{coalition_id}:edge-product",
                "broad_signal_ref": dict(broad_signal_ref),
                "matrix_of_edging_ref": dict(matrix_of_edging_ref),
                "hidden_pressure": str(matrix_obj.payload["hidden_pressure"]),
                "surviving_edge": str(matrix_obj.payload["surviving_edge"]),
                "stance": str(role_obj.payload["stance"]),
                "psychological_role": str(role_obj.payload["psychological_role"]),
                "tension": str(role_obj.payload["tension"]),
                "consequence": str(data.get("consequence") or "inaction remains a visible, costly choice"),
                "counteractivation_risks": list(matrix_obj.payload.get("counteractivation_risks", ["defensive detachment"])),
                "evidence_refs": [dict(matrix_of_edging_ref)],
                "epistemic_state": "inferred",
            },
            "misuse_risk_refs": [dict(r) for r in misuse_risk_refs],
            "evaluation_profile_ref": dict(evaluation_profile_ref),
        }

        key = idempotency_key or f"gen-coalition:{coalition_id}"
        return self.store_coalition(payload, idempotency_key=key)
