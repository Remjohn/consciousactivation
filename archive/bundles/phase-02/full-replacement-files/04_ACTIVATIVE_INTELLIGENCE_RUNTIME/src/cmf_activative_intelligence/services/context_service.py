from __future__ import annotations

from typing import Any, Mapping

from ..repositories.air_repository import AirRepository
from .semantic_authority import SemanticAuthorityService


class ContextService:
    def __init__(self, repository: AirRepository):
        self.repository = repository
        self.semantic = SemanticAuthorityService(repository)

    def store_matrix(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        return self.semantic.store(
            "matrix_of_edging",
            payload,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def store_context(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate("activative_context", payload)
        matrix = self.repository.get_object(
            normalized["matrix_of_edging_ref"]["object_id"]
        )
        if matrix.object_type != "matrix_of_edging":
            raise ValueError("matrix_of_edging_ref does not identify a Matrix of Edging")
        if matrix.canonical_sha256 != normalized["matrix_of_edging_ref"]["sha256"]:
            raise ValueError("matrix_of_edging_ref hash does not match current bytes")
        return self.semantic.store(
            "activative_context",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def store_identity_observation(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        return self.semantic.store(
            "identity_dna_candidate_observation",
            payload,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )
