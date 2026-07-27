from __future__ import annotations

from typing import Any, Mapping

from ..repositories.air_repository import AirRepository
from .semantic_authority import SemanticAuthorityService


class BrandService:
    def __init__(self, repository: AirRepository):
        self.repository = repository
        self.semantic = SemanticAuthorityService(repository)

    def store_brand_context(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        return self.semantic.store(
            "brand_context_version",
            payload,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def _require_brand(self, ref: Mapping[str, Any]) -> None:
        brand = self.repository.get_object(ref["object_id"])
        if brand.object_type != "brand_context_version":
            raise ValueError("brand_context_ref identifies wrong object type")
        if brand.canonical_sha256 != ref["sha256"]:
            raise ValueError("brand_context_ref hash does not match current bytes")

    def store_voice_dna(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate("voice_dna", payload)
        self._require_brand(normalized["brand_context_ref"])
        return self.semantic.store(
            "voice_dna",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def store_visual_dna(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate("visual_dna", payload)
        self._require_brand(normalized["brand_context_ref"])
        return self.semantic.store(
            "visual_dna",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def store_distillation_receipt(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate(
            "distillation_layer_receipt", payload
        )
        if normalized["layer"] in {"compression", "evaluation", "recursion"}:
            if not normalized["edge_product_preserved"]:
                raise ValueError(
                    f"RSCS {normalized['layer']} cannot pass while Edge Product is lost"
                )
            if not normalized["role_tension_preserved"]:
                raise ValueError(
                    f"RSCS {normalized['layer']} cannot pass while role/tension is lost"
                )
        return self.semantic.store(
            "distillation_layer_receipt",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )
