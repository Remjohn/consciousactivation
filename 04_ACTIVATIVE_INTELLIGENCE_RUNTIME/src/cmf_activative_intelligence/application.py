from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .domain import validate_air_object
from .repositories.air_repository import AirRepository
from .repositories.registry_repository import RegistryRepository
from .services.archetype_service import ArchetypeService
from .services.brand_service import BrandService
from .services.coalition_service import CoalitionService
from .services.context_service import ContextService
from .services.failure_service import FailureService
from .services.learning_service import LearningService
from .services.primitive_service import PrimitiveService
from .services.semantic_authority import SemanticAuthorityService


class AirApplication:
    def __init__(self, database_path: str | Path | None = None):
        self.repository = AirRepository(database_path)
        self.registries = RegistryRepository(self.repository)
        self.semantic = SemanticAuthorityService(self.repository)
        self.context = ContextService(self.repository)
        self.primitives = PrimitiveService(self.repository, self.registries)
        self.coalitions = CoalitionService(self.repository, self.registries)
        self.archetypes = ArchetypeService(self.repository, self.registries)
        self.brand = BrandService(self.repository)
        self.learning = LearningService(self.repository)
        self.failures = FailureService(self.repository)

    def initialize(self) -> dict[str, Any]:
        return self.repository.initialize()

    def load_registries(self) -> dict[str, Any]:
        return self.registries.import_all()

    def validate(self, object_type: str, payload: Mapping[str, Any]) -> dict[str, Any]:
        return validate_air_object(object_type, payload)

    def store(
        self,
        object_type: str,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        if object_type == "matrix_of_edging":
            return self.context.store_matrix(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "activative_context":
            return self.context.store_context(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "identity_dna_candidate_observation":
            return self.context.store_identity_observation(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "psychological_role_tension_contract":
            return self.primitives.store_role_tension(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "primitive_misuse_risk":
            return self.primitives.store_misuse_risk(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "primitive_binding":
            return self.primitives.store_binding(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "primitive_coalition_contract":
            return self.coalitions.store_coalition(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "primitive_evaluation_receipt":
            return self.coalitions.store_evaluation(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "archetype_coalition_program":
            return self.archetypes.store_program(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "brand_context_version":
            return self.brand.store_brand_context(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "voice_dna":
            return self.brand.store_voice_dna(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "visual_dna":
            return self.brand.store_visual_dna(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "distillation_layer_receipt":
            return self.brand.store_distillation_receipt(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "human_resolution_episode":
            return self.learning.capture_human_resolution(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "failure_attribution":
            return self.failures.record_failure(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "repair_program":
            return self.failures.propose_repair(
                payload,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        if object_type == "epistemic_transition_receipt":
            normalized = self.semantic.validate_transition_receipt(payload)
            return self.semantic.store(
                object_type,
                normalized,
                idempotency_key=idempotency_key,
                expected_revision=expected_revision,
            )
        return self.semantic.store(
            object_type,
            payload,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def status(self) -> dict[str, Any]:
        health = self.repository.health()
        return {
            **health,
            "lifecycle_state": "phase_02_deterministic_semantic_core",
            "development_authorized": True,
            "claim_ceiling": "DETERMINISTIC_SEMANTIC_CORE_DEVELOPMENT_PASS",
            "semantic_runtime_executed": True,
            "external_model_calls": 0,
            "real_human_evidence_claimed": False,
            "format02_activated": False,
            "vae_stage5_authorized": False,
            "production_authorized": False,
            "certified": False,
        }
