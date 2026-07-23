from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ca_contracts import canonical_sha256

from ..domain.errors import PipelineValidationError
from ..domain.validation import reject_noncanonical, require_semver, require_string, require_string_list


class ImplementationEligibilityRegistry:
    def __init__(self):
        self._candidates: dict[str, dict[str, Any]] = {}

    def register(self, candidate: Mapping[str, Any]) -> dict[str, Any]:
        required = {
            "implementation_id",
            "implementation_version",
            "owner_product",
            "implementation_kind",
            "capability_ids",
            "features",
            "side_effect_class",
            "authority_boundary",
            "development_eligible",
            "production_authorized",
            "evidence_refs",
        }
        if set(candidate) != required:
            raise PipelineValidationError("implementation candidate has unknown or missing fields")
        normalized = {
            "implementation_id": require_string(candidate["implementation_id"], "implementation_id"),
            "implementation_version": require_semver(candidate["implementation_version"], "implementation_version"),
            "owner_product": require_string(candidate["owner_product"], "owner_product"),
            "implementation_kind": require_string(candidate["implementation_kind"], "implementation_kind"),
            "capability_ids": require_string_list(candidate["capability_ids"], "capability_ids", non_empty=True),
            "features": require_string_list(candidate["features"], "features"),
            "side_effect_class": require_string(candidate["side_effect_class"], "side_effect_class"),
            "authority_boundary": require_string(candidate["authority_boundary"], "authority_boundary"),
            "development_eligible": candidate["development_eligible"] is True,
            "production_authorized": candidate["production_authorized"] is True,
            "evidence_refs": require_string_list(candidate["evidence_refs"], "evidence_refs"),
        }
        if normalized["production_authorized"]:
            raise PipelineValidationError("Phase 3 candidates cannot claim production authorization")
        reject_noncanonical(normalized)
        normalized["candidate_sha256"] = canonical_sha256(normalized)
        key = f"{normalized['implementation_id']}@{normalized['implementation_version']}"
        existing = self._candidates.get(key)
        if existing and existing != normalized:
            raise PipelineValidationError(f"implementation candidate identity collision: {key}")
        self._candidates[key] = normalized
        return dict(normalized)

    def eligible(self, capability_id: str, required_features: list[str]) -> list[dict[str, Any]]:
        required = set(required_features)
        result = [
            value
            for value in self._candidates.values()
            if capability_id in value["capability_ids"]
            and required.issubset(value["features"])
            and value["development_eligible"]
            and not value["production_authorized"]
        ]
        return [dict(item) for item in sorted(result, key=lambda item: (item["implementation_id"], item["implementation_version"]))]

    def all(self) -> list[dict[str, Any]]:
        return [dict(item) for item in sorted(self._candidates.values(), key=lambda item: (item["implementation_id"], item["implementation_version"]))]
