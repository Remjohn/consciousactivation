from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .repositories.air_repository import AirRepository
from .services.production_common import add_lineage_edges


def _authority() -> dict[str, str]:
    return {
        "authority_id": "ca-program-control-v2.1-candidate",
        "authority_version": "2.1.0-candidate",
        "authority_sha256": "a" * 64,
        "authority_state": "candidate_not_current",
    }


def _ref(value: Mapping[str, Any]) -> dict[str, str]:
    return {key: str(value[key]) for key in ("object_id", "version", "sha256")}


class ProgrammedModelEvidenceService:
    """Register bounded shadow evidence without live promotion or weight mutation."""

    def __init__(self, repository: AirRepository):
        self.repository = repository

    def register_claim_candidate(
        self,
        *,
        model_claim_ref: Mapping[str, Any],
        model_program_ref: Mapping[str, Any],
        semantic_scope_refs: Sequence[Mapping[str, Any]],
        human_resolution_refs: Sequence[Mapping[str, Any]],
        benchmark_ref: Mapping[str, Any],
        independent_evaluator_ref: Mapping[str, Any],
        producer_actor_id: str,
        evaluator_actor_id: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        if producer_actor_id == evaluator_actor_id:
            raise ValueError("producer and evaluator must differ")
        payload = {
            "evidence_candidate_id": f"pm-evidence:{model_claim_ref['object_id']}:{benchmark_ref['sha256'][:12]}",
            "version": "1.0.0",
            "model_claim_ref": _ref(model_claim_ref),
            "model_program_ref": _ref(model_program_ref),
            "semantic_scope_refs": [_ref(item) for item in semantic_scope_refs],
            "human_resolution_refs": [_ref(item) for item in human_resolution_refs],
            "benchmark_ref": _ref(benchmark_ref),
            "independent_evaluator_ref": _ref(independent_evaluator_ref),
            "producer_actor_id": str(producer_actor_id),
            "evaluator_actor_id": str(evaluator_actor_id),
            "promotion_ceiling": "SHADOW_ONLY_PENDING_SEPARATE_AUTHORITY",
            "automatic_weight_update": False,
            "automatic_doctrine_mutation": False,
            "lifecycle_state": "shadow_development",
            "epistemic_state": "observed",
            "authority": _authority(),
        }
        from .domain import validate_air_object

        normalized = validate_air_object("programmed_model_evidence_candidate", payload)
        result = self.repository.store_object(
            "programmed_model_evidence_candidate",
            normalized,
            idempotency_key=idempotency_key,
        )
        add_lineage_edges(
            self.repository,
            source_result=result,
            relation_type="programmed_model_evidence_candidate:depends_on",
            target_refs=[
                normalized["model_claim_ref"],
                normalized["model_program_ref"],
                *normalized["semantic_scope_refs"],
                *normalized["human_resolution_refs"],
                normalized["benchmark_ref"],
                normalized["independent_evaluator_ref"],
            ],
            evidence={"compiler": "programmed-model-evidence-service", "live_promotion": False},
        )
        return result
