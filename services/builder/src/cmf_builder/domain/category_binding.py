from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Mapping


REGISTRY_VERSION = "1.2.0-aligned"
REGISTRY_SHA256 = "9a836e5cc80371719cce688884ca3f071ee500862d54e6533982266d15b553b1"
CONSTITUTIONAL_AUTHORITY = (
    "governance/CONSTITUTIONAL_PRECEDENCE_CONTRACT.yaml"
    "#sha256:328c2ec7a57de1bcc892631a2190a38d8f8e61972cbcb397c867a312f993b4ff"
)
ACTIVATION_FIRST = "Activation First"
VISUAL_SYNTAX_FIRST = "Visual Syntax First"


@dataclass(frozen=True, slots=True)
class CanonicalCategory:
    category_id: str
    canonical_name: str
    governance_owner: str


_CATEGORIES = (
    CanonicalCategory(
        "short_form_edited_video",
        "Short-Form Edited Video",
        "product_lead_and_category_steward",
    ),
    CanonicalCategory(
        "2d_character_animation",
        "2D Character Animation",
        "product_lead_and_category_steward",
    ),
    CanonicalCategory(
        "carousels",
        "Carousels",
        "product_lead_and_category_steward",
    ),
    CanonicalCategory(
        "supervisuals",
        "Supervisuals",
        "product_lead_and_category_steward",
    ),
    CanonicalCategory(
        "conversational_activation_expression",
        "Conversational Activation / Human Expression",
        "product_lead_and_conversational_category_steward",
    ),
)
CANONICAL_CATEGORY_IDS = tuple(item.category_id for item in _CATEGORIES)


class CategoryBindingError(ValueError):
    def __init__(self, message: str, *, code: str = "CATEGORY_BINDING_REJECTED") -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True, slots=True)
class CanonicalCategoryRegistry:
    version: str
    authority_ref: str
    registry_hash: str
    categories: tuple[CanonicalCategory, ...]

    @classmethod
    def from_bytes(cls, registry_bytes: bytes) -> "CanonicalCategoryRegistry":
        if not isinstance(registry_bytes, bytes) or not registry_bytes:
            raise CategoryBindingError("Canonical category registry bytes are required.")
        digest = sha256(registry_bytes).hexdigest()
        if digest != REGISTRY_SHA256:
            raise CategoryBindingError(
                "Canonical category registry hash does not match the governed registry."
            )
        return cls(
            version=REGISTRY_VERSION,
            authority_ref=CONSTITUTIONAL_AUTHORITY,
            registry_hash=f"sha256:{digest}",
            categories=_CATEGORIES,
        )

    @property
    def category_ids(self) -> tuple[str, ...]:
        return tuple(item.category_id for item in self.categories)


_SEMANTIC_REF_FIELDS = (
    "source_premise_ref",
    "identity_dna_ref",
    "context_premise_ref",
    "resonance_map_ref",
    "matrix_of_edging_ref",
    "activative_intelligence_pack_ref",
    "evaluation_contract_ref",
)


@dataclass(frozen=True, slots=True)
class CategoryBinding:
    harness_id: str
    harness_version: str
    applicability: str
    category_id: str | None
    category_name: str | None
    category_registry_version: str
    category_registry_hash: str
    constitutional_authority_ref: str
    runtime_law: str
    harness_development_law: str
    semantic_lineage_refs: tuple[str, ...]
    wrong_reading_locks: tuple[str, ...]
    not_applicable_basis: str | None
    certification_state: str
    production_ready: bool
    certified: bool
    binding_hash: str

    @classmethod
    def create(
        cls,
        *,
        harness_id: str,
        harness_version: str,
        mode: str,
        category_ids: tuple[str, ...],
        activative_input: Mapping[str, object] | None,
        registry_bytes: bytes,
    ) -> "CategoryBinding":
        registry = CanonicalCategoryRegistry.from_bytes(registry_bytes)
        _require_text(harness_id, "harness_id")
        _require_text(harness_version, "harness_version")
        if mode == "generic":
            if category_ids or activative_input is not None:
                raise CategoryBindingError(
                    "A generic non-Activative task cannot claim category ownership."
                )
            values: dict[str, object] = {
                "harness_id": harness_id,
                "harness_version": harness_version,
                "applicability": "NOT_APPLICABLE",
                "category_id": None,
                "category_name": None,
                "category_registry_version": registry.version,
                "category_registry_hash": registry.registry_hash,
                "constitutional_authority_ref": registry.authority_ref,
                "runtime_law": ACTIVATION_FIRST,
                "harness_development_law": VISUAL_SYNTAX_FIRST,
                "semantic_lineage_refs": [],
                "wrong_reading_locks": [],
                "not_applicable_basis": "GENERIC_NON_ACTIVATIVE_TASK",
                "certification_state": "NOT_APPLICABLE_NONPRODUCTION",
                "production_ready": False,
                "certified": False,
            }
            return cls._from_values(values)
        if mode != "activative":
            raise CategoryBindingError("Harness mode is unsupported.")
        if len(category_ids) != 1:
            raise CategoryBindingError(
                "An Activative Harness must bind to exactly one canonical category."
            )
        category_id = category_ids[0]
        categories = {item.category_id: item for item in registry.categories}
        category = categories.get(category_id)
        if category is None:
            raise CategoryBindingError(f"Category '{category_id}' is unsupported.")
        if not isinstance(activative_input, Mapping):
            raise CategoryBindingError(
                "Activative semantic evidence is required.", code="HG-015"
            )
        semantic_refs: list[str] = []
        for field in _SEMANTIC_REF_FIELDS:
            semantic_refs.append(
                _require_text(
                    activative_input.get(field), f"activative_input.{field}", code="HG-015"
                )
            )
        provenance = _require_text_list(
            activative_input.get("evidence_provenance_refs"),
            "activative_input.evidence_provenance_refs",
            code="HG-015",
        )
        wrong_reading_locks = _require_text_list(
            activative_input.get("wrong_reading_locks"),
            "activative_input.wrong_reading_locks",
            code="HG-015",
        )
        semantic_refs.extend(provenance)
        values = {
            "harness_id": harness_id,
            "harness_version": harness_version,
            "applicability": "REQUIRED",
            "category_id": category.category_id,
            "category_name": category.canonical_name,
            "category_registry_version": registry.version,
            "category_registry_hash": registry.registry_hash,
            "constitutional_authority_ref": registry.authority_ref,
            "runtime_law": ACTIVATION_FIRST,
            "harness_development_law": VISUAL_SYNTAX_FIRST,
            "semantic_lineage_refs": list(semantic_refs),
            "wrong_reading_locks": list(wrong_reading_locks),
            "not_applicable_basis": None,
            "certification_state": "STRUCTURAL_UNCERTIFIED",
            "production_ready": False,
            "certified": False,
        }
        return cls._from_values(values)

    @classmethod
    def _from_values(cls, values: Mapping[str, object]) -> "CategoryBinding":
        digest = sha256(_canonical_json(values)).hexdigest()
        return cls(
            harness_id=str(values["harness_id"]),
            harness_version=str(values["harness_version"]),
            applicability=str(values["applicability"]),
            category_id=_optional_text(values["category_id"]),
            category_name=_optional_text(values["category_name"]),
            category_registry_version=str(values["category_registry_version"]),
            category_registry_hash=str(values["category_registry_hash"]),
            constitutional_authority_ref=str(values["constitutional_authority_ref"]),
            runtime_law=str(values["runtime_law"]),
            harness_development_law=str(values["harness_development_law"]),
            semantic_lineage_refs=tuple(values["semantic_lineage_refs"]),  # type: ignore[arg-type]
            wrong_reading_locks=tuple(values["wrong_reading_locks"]),  # type: ignore[arg-type]
            not_applicable_basis=_optional_text(values["not_applicable_basis"]),
            certification_state=str(values["certification_state"]),
            production_ready=False,
            certified=False,
            binding_hash=f"sha256:{digest}",
        )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "harness_id": self.harness_id,
            "harness_version": self.harness_version,
            "applicability": self.applicability,
            "category_id": self.category_id,
            "category_name": self.category_name,
            "category_registry_version": self.category_registry_version,
            "category_registry_hash": self.category_registry_hash,
            "constitutional_authority_ref": self.constitutional_authority_ref,
            "runtime_law": self.runtime_law,
            "harness_development_law": self.harness_development_law,
            "semantic_lineage_refs": list(self.semantic_lineage_refs),
            "wrong_reading_locks": list(self.wrong_reading_locks),
            "not_applicable_basis": self.not_applicable_basis,
            "certification_state": self.certification_state,
            "production_ready": self.production_ready,
            "certified": self.certified,
            "binding_hash": self.binding_hash,
        }

    def portable_projection(self) -> dict[str, object]:
        if self.applicability == "NOT_APPLICABLE":
            return {
                "applicability": self.applicability,
                "basis": self.not_applicable_basis,
                "category_id": None,
            }
        return self.canonical_dict()

    def validate_rebinding(
        self, *, candidate_harness_version: str, candidate_category_id: str
    ) -> None:
        if (
            candidate_category_id != self.category_id
            and candidate_harness_version == self.harness_version
        ):
            raise CategoryBindingError(
                "Changing category ownership requires a new immutable Harness version."
            )


def _require_text(value: object, field: str, *, code: str = "CATEGORY_BINDING_REJECTED") -> str:
    if not isinstance(value, str) or not value.strip():
        raise CategoryBindingError(f"{field} must be a non-empty string.", code=code)
    return value.strip()


def _require_text_list(value: object, field: str, *, code: str) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)) or not value:
        raise CategoryBindingError(f"{field} must be non-empty.", code=code)
    result = tuple(_require_text(item, field, code=code) for item in value)
    if len(set(result)) != len(result):
        raise CategoryBindingError(f"{field} contains duplicate values.", code=code)
    return result


def _optional_text(value: object) -> str | None:
    return None if value is None else str(value)


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
