from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re
from typing import Mapping


IMMUTABLE_REF_PATTERN = re.compile(
    r"^[A-Za-z0-9][A-Za-z0-9._:/-]*@[A-Za-z0-9][A-Za-z0-9._-]*"
    r"#sha256:[a-f0-9]{64}$"
)

TASK_FIELDS = frozenset(
    {
        "goal",
        "success_condition",
        "atomic_boundary",
        "input_contract",
        "output_contract",
        "required_context",
        "capability_requirements",
        "acceptance_tests",
        "authority_ref",
        "provenance_refs",
    }
)

FORBIDDEN_CLAIM_KEYS = frozenset(
    {
        "production",
        "production_ready",
        "production_eligible",
        "production_certified",
        "certified",
        "certification",
        "certification_state",
    }
)


class ManifestMode(str, Enum):
    GENERIC = "generic"
    ACTIVATIVE = "activative"


class OperatorManifestInvalid(ValueError):
    def __init__(self, message: str, *, field_path: str) -> None:
        super().__init__(message)
        self.field_path = field_path


@dataclass(frozen=True, slots=True)
class OperatorTaskDefinition:
    goal: str
    success_condition: str
    atomic_boundary: str
    input_contract: Mapping[str, object]
    output_contract: Mapping[str, object]
    required_context: tuple[str, ...]
    capability_requirements: tuple[str, ...]
    acceptance_tests: tuple[str, ...]
    authority_ref: str
    provenance_refs: tuple[str, ...]

    @classmethod
    def from_mapping(cls, value: object) -> "OperatorTaskDefinition":
        task = require_object(value, "task")
        require_exact_fields(task, TASK_FIELDS, "task")
        reject_forbidden_claims(task, "task")
        return cls(
            goal=require_text(task["goal"], "task.goal"),
            success_condition=require_text(
                task["success_condition"], "task.success_condition"
            ),
            atomic_boundary=require_text(
                task["atomic_boundary"], "task.atomic_boundary"
            ),
            input_contract=require_contract(
                task["input_contract"], "task.input_contract"
            ),
            output_contract=require_contract(
                task["output_contract"], "task.output_contract"
            ),
            required_context=require_text_tuple(
                task["required_context"], "task.required_context"
            ),
            capability_requirements=require_text_tuple(
                task["capability_requirements"], "task.capability_requirements"
            ),
            acceptance_tests=require_text_tuple(
                task["acceptance_tests"], "task.acceptance_tests"
            ),
            authority_ref=require_immutable_ref(
                task["authority_ref"], "task.authority_ref"
            ),
            provenance_refs=require_ref_tuple(
                task["provenance_refs"], "task.provenance_refs"
            ),
        )

    def canonical_dict(self) -> dict[str, object]:
        return {
            "goal": self.goal,
            "success_condition": self.success_condition,
            "atomic_boundary": self.atomic_boundary,
            "input_contract": normalize_json(self.input_contract),
            "output_contract": normalize_json(self.output_contract),
            "required_context": list(self.required_context),
            "capability_requirements": list(self.capability_requirements),
            "acceptance_tests": list(self.acceptance_tests),
            "authority_ref": self.authority_ref,
            "provenance_refs": list(self.provenance_refs),
        }


@dataclass(frozen=True, slots=True)
class OperatorManifestDocument:
    manifest_id: str
    manifest_version: str
    task_id: str
    mode: ManifestMode
    category_id: str | None
    task: OperatorTaskDefinition

    def canonical_dict(
        self, *, activative_input: Mapping[str, object] | None
    ) -> dict[str, object]:
        value: dict[str, object] = {
            "manifest_id": self.manifest_id,
            "manifest_version": self.manifest_version,
            "task_id": self.task_id,
            "mode": self.mode.value,
            "task": self.task.canonical_dict(),
        }
        if self.category_id is not None:
            value["category_id"] = self.category_id
        if activative_input is not None:
            value["activative_input"] = normalize_json(activative_input)
        return value


def require_object(value: object, field_path: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise OperatorManifestInvalid(
            "A JSON object is required.", field_path=field_path
        )
    if not value:
        raise OperatorManifestInvalid(
            "The JSON object cannot be empty.", field_path=field_path
        )
    if any(not isinstance(key, str) or not key.strip() for key in value):
        raise OperatorManifestInvalid(
            "Object keys must be non-empty strings.", field_path=field_path
        )
    return value


def require_exact_fields(
    value: Mapping[str, object], required: frozenset[str], field_path: str
) -> None:
    observed = frozenset(value)
    if observed == required:
        return
    missing = sorted(required - observed)
    unexpected = sorted(observed - required)
    detail = []
    if missing:
        detail.append(f"missing={','.join(missing)}")
    if unexpected:
        detail.append(f"unexpected={','.join(unexpected)}")
    raise OperatorManifestInvalid(
        f"Object fields do not match the governed contract ({'; '.join(detail)}).",
        field_path=field_path,
    )


def require_text(value: object, field_path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise OperatorManifestInvalid(
            "A non-empty string is required.", field_path=field_path
        )
    return value.strip()


def require_text_tuple(value: object, field_path: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise OperatorManifestInvalid(
            "A non-empty JSON string list is required.", field_path=field_path
        )
    normalized = tuple(
        require_text(item, f"{field_path}[{index}]")
        for index, item in enumerate(value)
    )
    if len(set(normalized)) != len(normalized):
        raise OperatorManifestInvalid(
            "Duplicate list entries are not canonical.", field_path=field_path
        )
    return normalized


def require_ref_tuple(
    value: object, field_path: str, *, allow_empty: bool = False
) -> tuple[str, ...]:
    if not isinstance(value, list) or (not value and not allow_empty):
        qualifier = "a JSON list" if allow_empty else "a non-empty JSON list"
        raise OperatorManifestInvalid(
            f"{qualifier} of immutable references is required.",
            field_path=field_path,
        )
    normalized = tuple(
        require_immutable_ref(item, f"{field_path}[{index}]")
        for index, item in enumerate(value)
    )
    if len(set(normalized)) != len(normalized):
        raise OperatorManifestInvalid(
            "Duplicate immutable references are not canonical.", field_path=field_path
        )
    return normalized


def require_immutable_ref(value: object, field_path: str) -> str:
    text = require_text(value, field_path)
    if IMMUTABLE_REF_PATTERN.fullmatch(text) is None:
        raise OperatorManifestInvalid(
            "Reference must include an object identity, version, and sha256 digest.",
            field_path=field_path,
        )
    return text


def require_contract(value: object, field_path: str) -> dict[str, object]:
    contract = require_object(value, field_path)
    reject_forbidden_claims(contract, field_path)
    normalized = normalize_json(contract, field_path=field_path)
    assert isinstance(normalized, dict)
    return normalized


def reject_forbidden_claims(value: object, field_path: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{field_path}.{key}"
            if key.lower() in FORBIDDEN_CLAIM_KEYS:
                raise OperatorManifestInvalid(
                    "Production and certification claims are not accepted in an operator manifest.",
                    field_path=child,
                )
            reject_forbidden_claims(item, child)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_forbidden_claims(item, f"{field_path}[{index}]")


def reject_identity_dna_mutation(value: object, field_path: str) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{field_path}.{key}"
            normalized_key = key.lower().replace("-", "_")
            if "identity_dna" in normalized_key:
                raise OperatorManifestInvalid(
                    "Identity DNA is human-owned and may appear only as activative_input.identity_dna_ref.",
                    field_path=child,
                )
            reject_identity_dna_mutation(item, child)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            reject_identity_dna_mutation(item, f"{field_path}[{index}]")


def normalize_json(value: object, *, field_path: str = "value") -> object:
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if value != value or value in (float("inf"), float("-inf")):
            raise OperatorManifestInvalid(
                "Non-finite numbers are not valid governed JSON.", field_path=field_path
            )
        return value
    if isinstance(value, list) or isinstance(value, tuple):
        return [
            normalize_json(item, field_path=f"{field_path}[{index}]")
            for index, item in enumerate(value)
        ]
    if isinstance(value, Mapping):
        normalized: dict[str, object] = {}
        for key in sorted(value):
            if not isinstance(key, str) or not key.strip():
                raise OperatorManifestInvalid(
                    "Object keys must be non-empty strings.", field_path=field_path
                )
            normalized[key] = normalize_json(
                value[key], field_path=f"{field_path}.{key}"
            )
        return normalized
    raise OperatorManifestInvalid(
        "Value is not representable as governed JSON.", field_path=field_path
    )
