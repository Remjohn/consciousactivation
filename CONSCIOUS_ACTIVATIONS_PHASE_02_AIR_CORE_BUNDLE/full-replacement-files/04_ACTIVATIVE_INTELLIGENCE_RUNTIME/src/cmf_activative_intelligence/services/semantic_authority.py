from __future__ import annotations

from typing import Any, Mapping

from ..domain import (
    require_epistemic_transition,
    supported_object_types,
    validate_air_object,
)
from ..repositories.air_repository import AirRepository


class SemanticAuthorityService:
    """Validate and persist AIR-owned semantic objects without model inference."""

    def __init__(self, repository: AirRepository):
        self.repository = repository

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
        return self.repository.store_object(
            object_type,
            payload,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def validate_transition_receipt(
        self, payload: Mapping[str, Any]
    ) -> dict[str, Any]:
        normalized = validate_air_object("epistemic_transition_receipt", payload)
        require_epistemic_transition(
            str(normalized["from_state"]),
            str(normalized["to_state"]),
            evidence_refs=normalized["evidence_refs"],
            operator_decision_ref=normalized["operator_decision_ref"],
        )
        return normalized

    def supported_types(self) -> tuple[str, ...]:
        return supported_object_types()
