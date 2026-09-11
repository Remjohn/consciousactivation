from __future__ import annotations

from typing import Any, Mapping

from ..domain import AIR_OWNED_LAYERS, expected_owner_for_layer
from ..repositories.air_repository import AirRepository
from .semantic_authority import SemanticAuthorityService


class FailureService:
    def __init__(self, repository: AirRepository):
        self.repository = repository
        self.semantic = SemanticAuthorityService(repository)

    def record_failure(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate("failure_attribution", payload)
        layer = normalized["responsible_layer"]
        expected_owner = expected_owner_for_layer(layer)
        if normalized["owner_product"] != expected_owner:
            raise ValueError("failure owner does not match responsible layer")
        return self.semantic.store(
            "failure_attribution",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def propose_repair(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate("repair_program", payload)
        failure_ref = normalized["failure_ref"]
        failure = self.repository.get_object(failure_ref["object_id"])
        if failure.object_type != "failure_attribution":
            raise ValueError("failure_ref identifies wrong object type")
        if failure.canonical_sha256 != failure_ref["sha256"]:
            raise ValueError("failure_ref hash does not match current bytes")
        if failure.payload["responsible_layer"] != normalized["responsible_layer"]:
            raise ValueError("repair responsible_layer differs from failure")
        if failure.payload["owner_product"] != normalized["owner_product"]:
            raise ValueError("repair owner differs from failure owner")
        is_air_owned = normalized["responsible_layer"] in AIR_OWNED_LAYERS
        if is_air_owned and normalized["repair_mode"] != "local_repair":
            raise ValueError("AIR-owned failure must use local_repair")
        if not is_air_owned and normalized["repair_mode"] != "owner_referral":
            raise ValueError("external-product failure must use owner_referral")
        return self.semantic.store(
            "repair_program",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )
