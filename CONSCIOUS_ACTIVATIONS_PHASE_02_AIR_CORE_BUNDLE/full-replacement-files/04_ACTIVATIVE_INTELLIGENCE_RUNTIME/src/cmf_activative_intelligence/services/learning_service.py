from __future__ import annotations

from typing import Any, Mapping

from ..repositories.air_repository import AirRepository
from .semantic_authority import SemanticAuthorityService


class LearningService:
    def __init__(self, repository: AirRepository):
        self.repository = repository
        self.semantic = SemanticAuthorityService(repository)

    def capture_human_resolution(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate(
            "human_resolution_episode", payload
        )
        forbidden = {
            "promote_skill",
            "promote_recipe",
            "update_model_weights",
            "change_doctrine",
            "globalize_learning",
        }
        dispositions = set(normalized["programming_material_dispositions"])
        illegal = forbidden & dispositions
        if illegal:
            raise ValueError(
                f"HumanResolution capture cannot automatically promote: {sorted(illegal)}"
            )
        if normalized["promotion_status"] != "captured_not_promoted":
            raise ValueError("HumanResolution must be captured without automatic promotion")
        return self.semantic.store(
            "human_resolution_episode",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )
