from __future__ import annotations

from typing import Any, Mapping

from ..repositories.air_repository import AirRepository
from ..repositories.registry_repository import RegistryRepository
from .semantic_authority import SemanticAuthorityService


class PrimitiveService:
    def __init__(
        self,
        repository: AirRepository,
        registries: RegistryRepository,
    ):
        self.repository = repository
        self.registries = registries
        self.semantic = SemanticAuthorityService(repository)

    def store_role_tension(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        return self.semantic.store(
            "psychological_role_tension_contract",
            payload,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def store_misuse_risk(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate("primitive_misuse_risk", payload)
        record = self.registries.get_primitive(
            normalized["primitive_ref"]["object_id"],
            source_sha256=normalized["primitive_ref"]["sha256"],
        )
        if record.immutable_ref() != normalized["primitive_ref"]:
            raise ValueError("primitive_ref does not match exact registry bytes")
        return self.semantic.store(
            "primitive_misuse_risk",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )

    def store_binding(
        self,
        payload: Mapping[str, Any],
        *,
        idempotency_key: str,
        expected_revision: int | None = None,
    ) -> dict[str, Any]:
        normalized = self.semantic.validate("primitive_binding", payload)
        primitive = self.registries.get_primitive(
            normalized["primitive_ref"]["object_id"],
            source_sha256=normalized["primitive_ref"]["sha256"],
        )
        if primitive.immutable_ref() != normalized["primitive_ref"]:
            raise ValueError("primitive_ref does not match exact registry bytes")

        role_tension = self.repository.get_object(
            normalized["role_tension_ref"]["object_id"]
        )
        if role_tension.object_type != "psychological_role_tension_contract":
            raise ValueError(
                "role_tension_ref must identify a psychological role/tension contract"
            )
        if role_tension.canonical_sha256 != normalized["role_tension_ref"]["sha256"]:
            raise ValueError("role_tension_ref hash does not match current bytes")

        for relation in normalized["relation_set"]:
            self.registries.get_primitive(relation["target_primitive_id"])
        for risk_ref in normalized["misuse_risk_refs"]:
            risk = self.repository.get_object(risk_ref["object_id"])
            if risk.object_type != "primitive_misuse_risk":
                raise ValueError("misuse_risk_ref identifies the wrong object type")
            if risk.canonical_sha256 != risk_ref["sha256"]:
                raise ValueError("misuse_risk_ref hash does not match current bytes")

        return self.semantic.store(
            "primitive_binding",
            normalized,
            idempotency_key=idempotency_key,
            expected_revision=expected_revision,
        )
