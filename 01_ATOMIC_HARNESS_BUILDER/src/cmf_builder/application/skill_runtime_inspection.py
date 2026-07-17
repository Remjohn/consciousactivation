"""Skill, recipe, and runtime capsule inspection for OD-AM-004 / ST-10.05."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from typing import Any


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def sha256_of(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


class SkillRuntimeInspectionError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class RuntimeObjectClass(str, Enum):
    SKILL_DEFINITION = "SKILL_DEFINITION"
    SKILL_VERSION = "SKILL_VERSION"
    BEHAVIORAL_ANCHOR = "BEHAVIORAL_ANCHOR"
    SKILL_DECISION = "SKILL_DECISION"
    RECIPE = "RECIPE"
    PHASE_LOCAL_RECIPE_BINDING = "PHASE_LOCAL_RECIPE_BINDING"
    JIT_CAPSULE = "JIT_CAPSULE"
    PINNED_RUNTIME_CAPSULE = "PINNED_RUNTIME_CAPSULE"
    DISPOSED_CAPSULE = "DISPOSED_CAPSULE"
    INVALIDATED_CAPSULE = "INVALIDATED_CAPSULE"
    HISTORICAL_REPRODUCTION = "HISTORICAL_REPRODUCTION"


class ActivationState(str, Enum):
    NOT_LOADED = "NOT_LOADED"
    LOADED = "LOADED"
    ACTIVE = "ACTIVE"
    DISPOSED = "DISPOSED"
    INVALIDATED = "INVALIDATED"
    HISTORICAL = "HISTORICAL"


def _text(value: object, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise SkillRuntimeInspectionError("MISSING_GOVERNED_FIELD", f"{name} is required")


@dataclass(frozen=True)
class SkillRuntimeObject:
    object_id: str
    object_class: RuntimeObjectClass
    version: str
    source_registry: str
    capability_requirement: str
    necessity_decision: str
    behavioral_anchors: tuple[str, ...]
    recipe_components: tuple[str, ...]
    phase_applicability: tuple[str, ...]
    minimum_context_refs: tuple[str, ...]
    pin_identity: str
    load_identity: str
    activation_state: ActivationState
    predecessor_identities: tuple[str, ...]
    descendant_identities: tuple[str, ...]
    receipt_refs: tuple[str, ...]
    provenance: str
    maturity: str
    limitations: tuple[str, ...]
    source_lineage: str
    excess_context_included: bool = False
    certified: bool = False

    def __post_init__(self) -> None:
        for value, name in (
            (self.object_id, "object_id"),
            (self.version, "version"),
            (self.source_registry, "source_registry"),
            (self.capability_requirement, "capability_requirement"),
            (self.necessity_decision, "necessity_decision"),
            (self.pin_identity, "pin_identity"),
            (self.load_identity, "load_identity"),
            (self.provenance, "provenance"),
            (self.maturity, "maturity"),
            (self.source_lineage, "source_lineage"),
        ):
            _text(value, name)
        if not self.receipt_refs:
            raise SkillRuntimeInspectionError("RECEIPT_TRACE_REQUIRED", "runtime inspection object requires receipts")
        if self.object_class in {RuntimeObjectClass.SKILL_VERSION, RuntimeObjectClass.SKILL_DEFINITION} and not self.behavioral_anchors:
            raise SkillRuntimeInspectionError("MISSING_BEHAVIORAL_ANCHORS", "skill objects require behavioral anchors")
        if self.capability_requirement != "NOT_APPLICABLE" and not self.necessity_decision:
            raise SkillRuntimeInspectionError("CAPABILITY_DECISION_REQUIRED", "capability requires governed skill decision")
        if self.object_class is RuntimeObjectClass.PINNED_RUNTIME_CAPSULE and self.pin_identity == "UNPINNED":
            raise SkillRuntimeInspectionError("UNPINNED_RUNTIME_SKILL_USE", "runtime capsule must be pinned")
        if self.object_class is RuntimeObjectClass.INVALIDATED_CAPSULE and self.activation_state is ActivationState.ACTIVE:
            raise SkillRuntimeInspectionError("INVALIDATED_CAPSULE_DISPLAYED_ACTIVE", "invalidated capsule cannot display active")
        if self.object_class is RuntimeObjectClass.DISPOSED_CAPSULE and self.activation_state in {ActivationState.LOADED, ActivationState.ACTIVE}:
            raise SkillRuntimeInspectionError("DISPOSED_CAPSULE_DISPLAYED_LOADED", "disposed capsule cannot display loaded")
        if self.excess_context_included:
            raise SkillRuntimeInspectionError("EXCESS_CONTEXT_INCLUDED", "runtime capsule inspection must preserve minimum context")
        if self.certified:
            raise SkillRuntimeInspectionError("DEVELOPMENT_DISPLAYED_AS_CERTIFICATION", "development validation is not certification")

    def as_dict(self) -> dict[str, Any]:
        return {
            "object_id": self.object_id,
            "object_class": self.object_class.value,
            "version": self.version,
            "source_registry": self.source_registry,
            "capability_requirement": self.capability_requirement,
            "necessity_decision": self.necessity_decision,
            "behavioral_anchors": list(self.behavioral_anchors),
            "recipe_components": list(self.recipe_components),
            "phase_applicability": list(self.phase_applicability),
            "minimum_context_refs": list(self.minimum_context_refs),
            "pin_identity": self.pin_identity,
            "load_identity": self.load_identity,
            "activation_state": self.activation_state.value,
            "predecessor_identities": list(self.predecessor_identities),
            "descendant_identities": list(self.descendant_identities),
            "receipt_refs": list(self.receipt_refs),
            "provenance": self.provenance,
            "maturity": self.maturity,
            "limitations": list(self.limitations),
            "source_lineage": self.source_lineage,
            "excess_context_included": False,
            "certified": False,
        }

    @property
    def object_identity(self) -> str:
        return sha256_of(self.as_dict())


@dataclass(frozen=True)
class SkillRuntimeInspection:
    subject_identity: str
    objects: tuple[SkillRuntimeObject, ...]
    projection_revision: str
    _anchor: str = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        _text(self.subject_identity, "subject_identity")
        _text(self.projection_revision, "projection_revision")
        classes = {item.object_class for item in self.objects}
        if len(classes) != len(self.objects):
            pass
        object.__setattr__(self, "_anchor", sha256_of(self._payload()))

    def _payload(self) -> dict[str, Any]:
        return {
            "subject_identity": self.subject_identity,
            "objects": [item.as_dict() | {"object_identity": item.object_identity} for item in sorted(self.objects, key=lambda item: item.object_id)],
            "projection_revision": self.projection_revision,
        }

    @property
    def inspection_identity(self) -> str:
        return sha256_of(self._payload())

    def as_dict(self) -> dict[str, Any]:
        payload = self._payload()
        if sha256_of(payload) != self._anchor:
            raise SkillRuntimeInspectionError("MUTATED_GOVERNED_OBJECT", "inspection changed")
        payload["inspection_identity"] = sha256_of(payload)
        return payload


def trace_runtime_lineage(objects: tuple[SkillRuntimeObject, ...], start_object_id: str) -> tuple[str, ...]:
    known = {item.object_id: item for item in objects}
    if start_object_id not in known:
        return ()
    order = [start_object_id]
    current = known[start_object_id]
    while current.descendant_identities:
        next_id = current.descendant_identities[0]
        if next_id not in known or next_id in order:
            break
        order.append(next_id)
        current = known[next_id]
    return tuple(order)


def query_runtime_objects(objects: tuple[SkillRuntimeObject, ...], **filters: str) -> tuple[SkillRuntimeObject, ...]:
    supported = {"object_id", "version", "capability_requirement", "phase", "receipt_ref", "object_class"}
    unknown = set(filters) - supported
    if unknown:
        raise SkillRuntimeInspectionError("UNSUPPORTED_RUNTIME_INSPECTION_FILTER", "unsupported filter", filters=sorted(unknown))
    result = []
    for item in objects:
        if "object_id" in filters and item.object_id != filters["object_id"]:
            continue
        if "version" in filters and item.version != filters["version"]:
            continue
        if "capability_requirement" in filters and item.capability_requirement != filters["capability_requirement"]:
            continue
        if "phase" in filters and filters["phase"] not in item.phase_applicability:
            continue
        if "receipt_ref" in filters and filters["receipt_ref"] not in item.receipt_refs:
            continue
        if "object_class" in filters and item.object_class.value != filters["object_class"]:
            continue
        result.append(item)
    return tuple(sorted(result, key=lambda item: item.object_id))
