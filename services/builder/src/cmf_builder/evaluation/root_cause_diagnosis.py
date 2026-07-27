"""Typed root-cause diagnosis and repair-scope declarations for ST-08.04.

This module is deliberately diagnostic.  It records the smallest supported
responsible layer and the descendant state a later, separately-authorized
repair would need to invalidate.  It never selects or executes a repair and
never closes an evidence, production, or certification gate.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
import hashlib
import json
import re
import weakref
from typing import Any


STORY_ID = "ST-08.04"
PRIMARY_FAILURE_CLASSES = (
    "evidence",
    "visual_parse",
    "atomicity",
    "authority",
    "contract",
    "module",
    "skill",
    "capsule",
    "benchmark",
    "budget",
    "provider",
    "observability",
    "migration",
    "downstream_implementation",
)
DIAGNOSTIC_LAYER_NAMES = (
    "source_and_evidence",
    "authority",
    "semantic",
    "category",
    "skill",
    "context",
    "workflow",
    "external_boundary",
)
UNKNOWN_FAILURE_CODE = "UNKNOWN_REQUIRES_TRIAGE"
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_ANCHORS: dict[int, tuple[weakref.ReferenceType[Any], str]] = {}


class RootCauseDiagnosisError(ValueError):
    """Typed, payload-safe ST-08.04 failure."""

    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class PrimaryFailureClass(str, Enum):
    EVIDENCE = "evidence"
    VISUAL_PARSE = "visual_parse"
    ATOMICITY = "atomicity"
    AUTHORITY = "authority"
    CONTRACT = "contract"
    MODULE = "module"
    SKILL = "skill"
    CAPSULE = "capsule"
    BENCHMARK = "benchmark"
    BUDGET = "budget"
    PROVIDER = "provider"
    OBSERVABILITY = "observability"
    MIGRATION = "migration"
    DOWNSTREAM_IMPLEMENTATION = "downstream_implementation"


class DiagnosticLayer(str, Enum):
    SOURCE_AND_EVIDENCE = "source_and_evidence"
    AUTHORITY = "authority"
    SEMANTIC = "semantic"
    CATEGORY = "category"
    SKILL = "skill"
    CONTEXT = "context"
    WORKFLOW = "workflow"
    EXTERNAL_BOUNDARY = "external_boundary"


class DiagnosisStatus(str, Enum):
    LOCALIZED = "localized"
    UNKNOWN_REQUIRES_TRIAGE = "unknown_requires_triage"


class HypothesisTestStatus(str, Enum):
    SUPPORTED = "supported"
    REJECTED = "rejected"
    INCONCLUSIVE = "inconclusive"


# Compatibility alias retained inside this Story's new module only.
HypothesisStatus = HypothesisTestStatus


class DiagnosisAction(str, Enum):
    ISSUE = "issue_root_cause_diagnosis"
    INVALIDATE = "invalidate_root_cause_diagnosis"
    ROLLBACK = "rollback_root_cause_diagnosis"


class AuthorityStatus(str, Enum):
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    INVALIDATED = "invalidated"


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _safe(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return {
            item.name: _safe(getattr(value, item.name))
            for item in fields(value)
            if item.init
        }
    if isinstance(value, dict):
        return {str(key): _safe(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list, set, frozenset)):
        return [_safe(item) for item in value]
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    return {"unsupported_type": type(value).__qualname__}


def _construction_payload(instance: Any) -> dict[str, Any]:
    builder = getattr(instance, "_construction_payload", None)
    if builder is not None:
        return builder()
    return {
        item.name: _safe(getattr(instance, item.name))
        for item in fields(instance)
        if item.init
    }


def _seal(instance: Any) -> None:
    key = id(instance)

    def cleanup(reference: weakref.ReferenceType[Any], identity: int = key) -> None:
        current = _ANCHORS.get(identity)
        if current is not None and current[0] is reference:
            _ANCHORS.pop(identity, None)

    reference = weakref.ref(instance, cleanup)
    _ANCHORS[key] = (reference, canonical_sha256(_construction_payload(instance)))


def _require_unmutated(instance: Any, field: str) -> None:
    anchor = _ANCHORS.get(id(instance))
    if anchor is None or anchor[0]() is not instance:
        raise RootCauseDiagnosisError(
            "UNANCHORED_GOVERNED_OBJECT", f"{field} lacks a construction anchor", field=field
        )
    try:
        current = canonical_sha256(_construction_payload(instance))
    except (AttributeError, TypeError, ValueError) as exc:
        raise RootCauseDiagnosisError(
            "MUTATED_GOVERNED_OBJECT", f"{field} cannot be serialized", field=field
        ) from exc
    if current != anchor[1]:
        raise RootCauseDiagnosisError(
            "MUTATED_GOVERNED_OBJECT", f"{field} changed after construction", field=field
        )


def _text(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise RootCauseDiagnosisError("MISSING_GOVERNED_FIELD", f"{field} is required", field=field)


def _sha(value: str, field: str) -> None:
    if not isinstance(value, str) or _SHA256.fullmatch(value) is None:
        raise RootCauseDiagnosisError(
            "INVALID_IMMUTABLE_IDENTITY", f"{field} must be a lowercase SHA-256", field=field
        )


def _strings(value: tuple[str, ...], field: str, *, hashes: bool = False) -> None:
    if not isinstance(value, tuple) or not value:
        raise RootCauseDiagnosisError("MISSING_GOVERNED_FIELD", f"{field} is required", field=field)
    if len(set(value)) != len(value):
        raise RootCauseDiagnosisError("DUPLICATE_GOVERNED_VALUE", f"{field} must be unique", field=field)
    for item in value:
        (_sha if hashes else _text)(item, field)


@dataclass(frozen=True, slots=True, weakref_slot=True)
class FailureClassification:
    failure_id: str
    stable_code: str
    primary_class: PrimaryFailureClass | None
    localization_layer: DiagnosticLayer | None
    contributing_factors: tuple[str, ...]

    def __post_init__(self) -> None:
        _text(self.failure_id, "failure_id")
        _text(self.stable_code, "stable_code")
        _strings(self.contributing_factors, "contributing_factors")
        unknown = self.stable_code == UNKNOWN_FAILURE_CODE
        if unknown and (self.primary_class is not None or self.localization_layer is not None):
            raise RootCauseDiagnosisError(
                "UNKNOWN_CLASSIFICATION_FORCED", "unknown failure cannot be forced into a known class or layer"
            )
        if not unknown:
            if not isinstance(self.primary_class, PrimaryFailureClass):
                raise RootCauseDiagnosisError("MISSING_PRIMARY_FAILURE_CLASS", "primary class is required")
            if not isinstance(self.localization_layer, DiagnosticLayer):
                raise RootCauseDiagnosisError("MISSING_RESPONSIBLE_LAYER", "localization layer is required")
        _seal(self)

    @property
    def classification_identity(self) -> str:
        _require_unmutated(self, "failure_classification")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "failure_id": self.failure_id,
            "stable_code": self.stable_code,
            "primary_class": None if self.primary_class is None else self.primary_class.value,
            "localization_layer": None if self.localization_layer is None else self.localization_layer.value,
            "contributing_factors": list(self.contributing_factors),
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "failure_classification")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class HypothesisTestResult:
    hypothesis_id: str
    hypothesis: str
    test_description: str
    status: HypothesisTestStatus
    evidence_refs: tuple[str, ...]
    result_summary: str
    rejection_reason: str | None = None

    def __post_init__(self) -> None:
        _text(self.hypothesis_id, "hypothesis_id")
        _text(self.hypothesis, "hypothesis")
        _text(self.test_description, "test_description")
        if not isinstance(self.status, HypothesisTestStatus):
            raise RootCauseDiagnosisError("INVALID_HYPOTHESIS_STATUS", "hypothesis status is invalid")
        _strings(self.evidence_refs, "evidence_refs", hashes=True)
        _text(self.result_summary, "result_summary")
        if self.status is HypothesisTestStatus.REJECTED:
            if self.rejection_reason is None:
                raise RootCauseDiagnosisError("MISSING_REJECTION_REASON", "rejected hypothesis needs a reason")
            _text(self.rejection_reason, "rejection_reason")
        elif self.rejection_reason is not None:
            _text(self.rejection_reason, "rejection_reason")
        _seal(self)

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "hypothesis_id": self.hypothesis_id,
            "hypothesis": self.hypothesis,
            "test_description": self.test_description,
            "status": self.status.value,
            "evidence_refs": list(self.evidence_refs),
            "result_summary": self.result_summary,
            "rejection_reason": self.rejection_reason,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "hypothesis_test_result")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True, init=False)
class RootCauseDiagnosis:
    diagnosis_id: str
    diagnosis_version: str
    classification: FailureClassification
    observed_symptom: str
    reproduction_or_evidence_refs: tuple[str, ...]
    affected_boundary: str
    competing_hypotheses: tuple[str, ...]
    hypothesis_tests_and_results: tuple[HypothesisTestResult, ...]
    status: DiagnosisStatus
    selected_root_cause: str | None
    confidence_basis: tuple[str, ...]
    smallest_supported_responsible_layer: DiagnosticLayer | None
    responsible_owner: str | None
    responsible_authority_ref: str | None
    unaffected_frozen_state: tuple[str, ...]
    exact_lineage: tuple[str, ...]
    escalation_route: str | None
    repair_selected: bool
    repair_executed: bool
    evidence_gate_closed: bool
    production_ready: bool
    certified: bool

    def __init__(
        self,
        diagnosis_id: str,
        diagnosis_version: str,
        classification: FailureClassification,
        observed_symptom: str,
        reproduction_or_evidence_refs: tuple[str, ...],
        affected_boundary: str,
        competing_hypotheses: tuple[str, ...],
        hypothesis_tests_and_results: tuple[HypothesisTestResult, ...],
        status: DiagnosisStatus,
        selected_root_cause: str | None,
        confidence_basis: tuple[str, ...],
        smallest_supported_responsible_layer: DiagnosticLayer | None,
        responsible_owner: str | None,
        responsible_authority_ref: str | None,
        unaffected_frozen_state: tuple[str, ...],
        exact_lineage: tuple[str, ...],
        escalation_route: str | None,
        repair_selected: bool = False,
        repair_executed: bool = False,
        evidence_gate_closed: bool = False,
        production_ready: bool = False,
        certified: bool = False,
    ) -> None:
        values = locals().copy()
        values.pop("self")
        for name, value in values.items():
            object.__setattr__(self, name, value)
        self._validate()
        _seal(self)

    def _validate(self) -> None:
        _text(self.diagnosis_id, "diagnosis_id")
        _text(self.diagnosis_version, "diagnosis_version")
        if not isinstance(self.classification, FailureClassification):
            raise RootCauseDiagnosisError("INVALID_CLASSIFICATION", "classification is required")
        self.classification.as_dict()
        _text(self.observed_symptom, "observed_symptom")
        _strings(self.reproduction_or_evidence_refs, "reproduction_or_evidence_refs", hashes=True)
        _text(self.affected_boundary, "affected_boundary")
        _strings(self.competing_hypotheses, "competing_hypotheses")
        if not isinstance(self.hypothesis_tests_and_results, tuple):
            raise RootCauseDiagnosisError("MISSING_HYPOTHESIS_TEST_EVIDENCE", "hypothesis results are required")
        tested = tuple(item.hypothesis_id for item in self.hypothesis_tests_and_results)
        if set(tested) != set(self.competing_hypotheses) or len(tested) != len(self.competing_hypotheses):
            raise RootCauseDiagnosisError(
                "MISSING_HYPOTHESIS_TEST_EVIDENCE", "every competing hypothesis needs exactly one result"
            )
        for result in self.hypothesis_tests_and_results:
            if not isinstance(result, HypothesisTestResult):
                raise RootCauseDiagnosisError("INVALID_HYPOTHESIS_RESULT", "typed result required")
            result.as_dict()
        if not isinstance(self.status, DiagnosisStatus):
            raise RootCauseDiagnosisError("INVALID_DIAGNOSIS_STATUS", "diagnosis status is invalid")
        if not isinstance(self.confidence_basis, tuple) or not self.confidence_basis:
            raise RootCauseDiagnosisError("MISSING_CONFIDENCE_BASIS", "confidence basis is required")
        _strings(self.confidence_basis, "confidence_basis")
        _strings(self.unaffected_frozen_state, "unaffected_frozen_state", hashes=True)
        _strings(self.exact_lineage, "exact_lineage", hashes=True)
        if self.repair_selected or self.repair_executed:
            raise RootCauseDiagnosisError("PROHIBITED_REPAIR_EXECUTION", "ST-08.04 cannot select or execute repair")
        if self.evidence_gate_closed or self.production_ready or self.certified:
            raise RootCauseDiagnosisError(
                "PROHIBITED_PRODUCTION_OR_CERTIFICATION_CLAIM",
                "diagnosis cannot close evidence, production, or certification",
            )
        supported = [item for item in self.hypothesis_tests_and_results if item.status is HypothesisTestStatus.SUPPORTED]
        if self.status is DiagnosisStatus.LOCALIZED:
            if self.selected_root_cause == self.observed_symptom:
                raise RootCauseDiagnosisError("SYMPTOM_IS_NOT_ROOT_CAUSE", "symptom cannot be root cause")
            if len(supported) > 1:
                raise RootCauseDiagnosisError("MULTIPLE_SUPPORTED_ROOT_CAUSES", "only one cause may be supported")
            if len(supported) != 1 or self.selected_root_cause != supported[0].hypothesis:
                raise RootCauseDiagnosisError(
                    "UNSUPPORTED_ROOT_CAUSE_SELECTION", "selected cause must be the sole supported hypothesis"
                )
            if self.smallest_supported_responsible_layer is None:
                raise RootCauseDiagnosisError("MISSING_RESPONSIBLE_LAYER", "localized diagnosis needs one layer")
            if self.smallest_supported_responsible_layer is not self.classification.localization_layer:
                raise RootCauseDiagnosisError("LAYER_LOCALIZATION_MISMATCH", "diagnostic layers disagree")
            if self.responsible_owner is None or self.responsible_authority_ref is None:
                raise RootCauseDiagnosisError("MISSING_RESPONSIBLE_OWNER", "localized diagnosis needs owner authority")
            _text(self.responsible_owner, "responsible_owner")
            _sha(self.responsible_authority_ref, "responsible_authority_ref")
            if self.escalation_route is not None:
                raise RootCauseDiagnosisError("UNEXPECTED_ESCALATION", "localized diagnosis cannot escalate")
        else:
            unresolved_values = (
                self.selected_root_cause,
                self.smallest_supported_responsible_layer,
                self.responsible_owner,
                self.responsible_authority_ref,
            )
            if any(value is not None for value in unresolved_values) or supported:
                raise RootCauseDiagnosisError(
                    "UNKNOWN_DIAGNOSIS_MUST_REMAIN_UNRESOLVED", "unknown diagnosis cannot guess cause or owner"
                )
            if self.classification.stable_code != UNKNOWN_FAILURE_CODE:
                raise RootCauseDiagnosisError("UNKNOWN_STATUS_CLASSIFICATION_MISMATCH", "unknown status needs unknown code")
            if self.escalation_route is None:
                raise RootCauseDiagnosisError("MISSING_TRIAGE_ESCALATION", "unknown diagnosis needs escalation")
            _text(self.escalation_route, "escalation_route")

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "diagnosis_id": self.diagnosis_id,
            "diagnosis_version": self.diagnosis_version,
            "failure_id_and_stable_code": self.classification._construction_payload(),
            "observed_symptom": self.observed_symptom,
            "reproduction_or_evidence_refs": list(self.reproduction_or_evidence_refs),
            "affected_boundary": self.affected_boundary,
            "competing_hypotheses": list(self.competing_hypotheses),
            "hypothesis_tests_and_results": [item._construction_payload() for item in self.hypothesis_tests_and_results],
            "selected_root_cause_or_unresolved_status": {
                "status": self.status.value,
                "selected_root_cause": self.selected_root_cause,
                "escalation_route": self.escalation_route,
            },
            "confidence_basis": list(self.confidence_basis),
            "smallest_supported_responsible_layer": (
                None if self.smallest_supported_responsible_layer is None else self.smallest_supported_responsible_layer.value
            ),
            "responsible_owner_and_authority_ref": {
                "responsible_owner": self.responsible_owner,
                "responsible_authority_ref": self.responsible_authority_ref,
            },
            "unaffected_frozen_state": list(self.unaffected_frozen_state),
            "exact_lineage": list(self.exact_lineage),
            "repair_route": (
                "BLOCKED" if self.status is DiagnosisStatus.UNKNOWN_REQUIRES_TRIAGE else "DIAGNOSIS_ONLY_NO_EXECUTION"
            ),
            "repair_selected": self.repair_selected,
            "repair_executed": self.repair_executed,
            "evidence_gate_closed": self.evidence_gate_closed,
            "production_ready": self.production_ready,
            "certified": self.certified,
        }

    @property
    def diagnosis_identity(self) -> str:
        _require_unmutated(self, "root_cause_diagnosis")
        return canonical_sha256(self._construction_payload())

    @property
    def diagnosis_receipt_id(self) -> str:
        return canonical_sha256({"story_id": STORY_ID, "diagnosis_identity": self.diagnosis_identity})

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "root_cause_diagnosis")
        payload = self._construction_payload()
        payload["diagnosis_identity"] = canonical_sha256(payload)
        payload["diagnosis_receipt_id"] = self.diagnosis_receipt_id
        return payload


@dataclass(frozen=True, slots=True, weakref_slot=True)
class RepairField:
    layer: DiagnosticLayer
    field_name: str

    def __post_init__(self) -> None:
        if not isinstance(self.layer, DiagnosticLayer):
            raise RootCauseDiagnosisError("INVALID_REPAIR_LAYER", "repair field needs typed layer")
        _text(self.field_name, "field_name")
        _seal(self)

    def as_dict(self) -> dict[str, str]:
        _require_unmutated(self, "repair_field")
        return {"layer": self.layer.value, "field_name": self.field_name}


@dataclass(frozen=True, slots=True, weakref_slot=True)
class DependencyEdge:
    parent_identity: str
    child_identity: str
    relation: str

    def __post_init__(self) -> None:
        _text(self.parent_identity, "parent_identity")
        _sha(self.child_identity, "child_identity")
        if self.parent_identity == self.child_identity:
            raise RootCauseDiagnosisError("CYCLIC_DEPENDENCY_EDGE", "self edge is prohibited")
        _text(self.relation, "relation")
        _seal(self)

    def as_dict(self) -> dict[str, str]:
        _require_unmutated(self, "dependency_edge")
        return {
            "parent_identity": self.parent_identity,
            "child_identity": self.child_identity,
            "relation": self.relation,
        }


@dataclass(frozen=True, slots=True, weakref_slot=True)
class RepairAndInvalidationGraph:
    root_cause_diagnosis_ref: str
    responsible_phase_or_capability: str
    responsible_layer: DiagnosticLayer
    permitted_repair_fields: tuple[RepairField, ...]
    frozen_upstream_and_unaffected_state: tuple[str, ...]
    dependency_edges: tuple[DependencyEdge, ...]
    invalidated_descendant_set: tuple[str, ...]
    targeted_regression_suite: tuple[str, ...]
    escalation_conditions: tuple[str, ...]
    required_repair_authority: str
    rollback_requirements: tuple[str, ...]
    repair_executed: bool = False
    artifact_mutated: bool = False
    production_ready: bool = False
    certified: bool = False

    def __post_init__(self) -> None:
        _sha(self.root_cause_diagnosis_ref, "root_cause_diagnosis_ref")
        _text(self.responsible_phase_or_capability, "responsible_phase_or_capability")
        if not isinstance(self.responsible_layer, DiagnosticLayer):
            raise RootCauseDiagnosisError("RESPONSIBLE_LAYER_MISMATCH", "typed responsible layer required")
        if not isinstance(self.permitted_repair_fields, tuple) or not self.permitted_repair_fields:
            raise RootCauseDiagnosisError("MISSING_PERMITTED_REPAIR_FIELDS", "bounded fields are required")
        if any(item.layer is not self.responsible_layer for item in self.permitted_repair_fields):
            raise RootCauseDiagnosisError("CROSS_LAYER_REPAIR_FIELD", "repair field crosses responsible layer")
        _strings(self.frozen_upstream_and_unaffected_state, "frozen_upstream_and_unaffected_state", hashes=True)
        if not isinstance(self.dependency_edges, tuple) or not self.dependency_edges:
            raise RootCauseDiagnosisError("MISSING_DEPENDENCY_EVIDENCE", "dependency evidence is required")
        for edge in self.dependency_edges:
            if not isinstance(edge, DependencyEdge):
                raise RootCauseDiagnosisError("INVALID_DEPENDENCY_EDGE", "typed edge is required")
            edge.as_dict()
        object.__setattr__(self, "permitted_repair_fields", tuple(sorted(self.permitted_repair_fields, key=lambda item: (item.layer.value, item.field_name))))
        object.__setattr__(self, "frozen_upstream_and_unaffected_state", tuple(sorted(self.frozen_upstream_and_unaffected_state)))
        object.__setattr__(self, "dependency_edges", tuple(sorted(self.dependency_edges, key=lambda item: (item.parent_identity, item.child_identity, item.relation))))
        object.__setattr__(self, "invalidated_descendant_set", tuple(sorted(self.invalidated_descendant_set)))
        object.__setattr__(self, "targeted_regression_suite", tuple(sorted(self.targeted_regression_suite)))
        object.__setattr__(self, "escalation_conditions", tuple(sorted(self.escalation_conditions)))
        object.__setattr__(self, "rollback_requirements", tuple(sorted(self.rollback_requirements)))
        _strings(self.invalidated_descendant_set, "invalidated_descendant_set", hashes=True)
        if set(self.invalidated_descendant_set) & set(self.frozen_upstream_and_unaffected_state):
            raise RootCauseDiagnosisError("FROZEN_STATE_INVALIDATED", "unaffected state cannot be invalidated")
        reachable: set[str] = set()
        frontier = {self.responsible_phase_or_capability}
        while frontier:
            parent = frontier.pop()
            children = {edge.child_identity for edge in self.dependency_edges if edge.parent_identity == parent}
            new = children - reachable
            reachable.update(new)
            frontier.update(new)
        expected = reachable - set(self.frozen_upstream_and_unaffected_state)
        if set(self.invalidated_descendant_set) != expected:
            raise RootCauseDiagnosisError(
                "INVALIDATION_SCOPE_MISMATCH",
                "invalidated set must equal the dependency-proven descendants",
                expected=tuple(sorted(expected)),
            )
        if not self.targeted_regression_suite:
            raise RootCauseDiagnosisError("MISSING_TARGETED_REGRESSION_SUITE", "targeted regressions are required")
        _strings(self.targeted_regression_suite, "targeted_regression_suite")
        if not self.escalation_conditions:
            raise RootCauseDiagnosisError("MISSING_ESCALATION_CONDITIONS", "escalation conditions are required")
        _strings(self.escalation_conditions, "escalation_conditions")
        if not self.required_repair_authority:
            raise RootCauseDiagnosisError("MISSING_REPAIR_AUTHORITY", "repair authority is required")
        _sha(self.required_repair_authority, "required_repair_authority")
        if not self.rollback_requirements:
            raise RootCauseDiagnosisError("MISSING_ROLLBACK_REQUIREMENTS", "rollback requirements are required")
        _strings(self.rollback_requirements, "rollback_requirements")
        if self.repair_executed or self.artifact_mutated:
            raise RootCauseDiagnosisError("PROHIBITED_REPAIR_EXECUTION", "graph is declaration-only")
        if self.production_ready or self.certified:
            raise RootCauseDiagnosisError("PROHIBITED_PRODUCTION_OR_CERTIFICATION_CLAIM", "claim exceeds authority")
        _seal(self)

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "root_cause_diagnosis_ref": self.root_cause_diagnosis_ref,
            "responsible_phase_or_capability": self.responsible_phase_or_capability,
            "responsible_layer": self.responsible_layer.value,
            "permitted_repair_fields": [item.as_dict() for item in self.permitted_repair_fields],
            "frozen_upstream_and_unaffected_state": list(self.frozen_upstream_and_unaffected_state),
            "dependency_edges": [item.as_dict() for item in self.dependency_edges],
            "invalidated_descendant_set": list(self.invalidated_descendant_set),
            "targeted_regression_suite": list(self.targeted_regression_suite),
            "escalation_conditions": list(self.escalation_conditions),
            "required_repair_authority": self.required_repair_authority,
            "rollback_requirements": list(self.rollback_requirements),
            "repair_executed": self.repair_executed,
            "artifact_mutated": self.artifact_mutated,
            "production_ready": self.production_ready,
            "certified": self.certified,
        }

    @property
    def graph_identity(self) -> str:
        _require_unmutated(self, "repair_and_invalidation_graph")
        return canonical_sha256(self._construction_payload())

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "repair_and_invalidation_graph")
        payload = self._construction_payload()
        payload["graph_identity"] = canonical_sha256(payload)
        return payload


def compile_repair_and_invalidation_graph(**values: Any) -> RepairAndInvalidationGraph:
    """Compile the immutable declaration; no repair is selected or executed."""

    diagnosis = values.pop("diagnosis", values.pop("root_cause_diagnosis_ref", None))
    if not isinstance(diagnosis, RootCauseDiagnosis):
        raise RootCauseDiagnosisError("INVALID_DIAGNOSIS_REFERENCE", "typed diagnosis is required")
    diagnosis.as_dict()
    if diagnosis.status is not DiagnosisStatus.LOCALIZED:
        raise RootCauseDiagnosisError(
            "UNRESOLVED_DIAGNOSIS_CANNOT_AUTHORIZE_GRAPH", "triage must finish first"
        )
    layer = diagnosis.smallest_supported_responsible_layer
    if layer is None:
        raise RootCauseDiagnosisError("MISSING_RESPONSIBLE_LAYER", "localized diagnosis needs layer")
    values["root_cause_diagnosis_ref"] = diagnosis.diagnosis_identity
    values["responsible_layer"] = layer
    graph = RepairAndInvalidationGraph(**values)
    if set(graph.frozen_upstream_and_unaffected_state) != set(diagnosis.unaffected_frozen_state):
        raise RootCauseDiagnosisError("UNAFFECTED_STATE_MISMATCH", "frozen state must match diagnosis")
    return graph


@dataclass(frozen=True, slots=True, weakref_slot=True)
class DiagnosisAuthority:
    authority_id: str
    authority_version: str
    authority_sha256: str
    permitted_actions: tuple[DiagnosisAction, ...]
    status: AuthorityStatus | str = AuthorityStatus.ACTIVE
    story_id: str = STORY_ID

    def __post_init__(self) -> None:
        _text(self.authority_id, "authority_id")
        _text(self.authority_version, "authority_version")
        _sha(self.authority_sha256, "authority_sha256")
        if self.story_id != STORY_ID:
            raise RootCauseDiagnosisError("AUTHORITY_SCOPE_MISMATCH", "authority is not scoped to ST-08.04")
        if isinstance(self.status, str):
            try:
                object.__setattr__(self, "status", AuthorityStatus(self.status))
            except ValueError as exc:
                raise RootCauseDiagnosisError("INVALID_AUTHORITY_STATUS", "authority status is invalid") from exc
        if not isinstance(self.status, AuthorityStatus):
            raise RootCauseDiagnosisError("INVALID_AUTHORITY_STATUS", "authority status is invalid")
        if not isinstance(self.permitted_actions, tuple) or not self.permitted_actions:
            raise RootCauseDiagnosisError("MISSING_AUTHORITY_GRANTS", "authority grants are required")
        if any(not isinstance(item, DiagnosisAction) for item in self.permitted_actions):
            raise RootCauseDiagnosisError("INVALID_AUTHORITY_GRANT", "typed grants are required")
        _seal(self)

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "authority_id": self.authority_id,
            "authority_version": self.authority_version,
            "authority_sha256": self.authority_sha256,
            "permitted_actions": [item.value for item in self.permitted_actions],
            "status": self.status.value,
            "story_id": self.story_id,
        }

    @property
    def authority_identity(self) -> str:
        _require_unmutated(self, "diagnosis_authority")
        return canonical_sha256(self._construction_payload())

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "diagnosis_authority")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class DiagnosisCommand:
    command_id: str
    action: DiagnosisAction
    resource_id: str
    payload_sha256: str
    expected_authority_identity: str

    def __post_init__(self) -> None:
        _text(self.command_id, "command_id")
        if not isinstance(self.action, DiagnosisAction):
            raise RootCauseDiagnosisError("INVALID_COMMAND_ACTION", "typed action is required")
        _sha(self.resource_id, "resource_id")
        _sha(self.payload_sha256, "payload_sha256")
        _sha(self.expected_authority_identity, "expected_authority_identity")
        _seal(self)

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "command_id": self.command_id,
            "action": self.action.value,
            "resource_id": self.resource_id,
            "payload_sha256": self.payload_sha256,
            "expected_authority_identity": self.expected_authority_identity,
        }

    @property
    def command_identity(self) -> str:
        _require_unmutated(self, "diagnosis_command")
        return canonical_sha256(self._construction_payload())

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "diagnosis_command")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class RootCauseDiagnosisReceipt:
    diagnosis: RootCauseDiagnosis
    graph: RepairAndInvalidationGraph | None
    failure_subject_sha256: str
    predecessor_scoring_receipt_sha256: str
    dependency_graph_sha256: str
    run_id: str
    provenance_sha256: str
    command_identity: str
    authority_identity: str
    observations: tuple[str, ...]
    active: bool = True

    def __post_init__(self) -> None:
        self.diagnosis.as_dict()
        if self.graph is not None:
            self.graph.as_dict()
            if self.graph.root_cause_diagnosis_ref != self.diagnosis.diagnosis_identity:
                raise RootCauseDiagnosisError("DIAGNOSIS_GRAPH_MISMATCH", "graph refers to another diagnosis")
        for name in (
            "failure_subject_sha256",
            "predecessor_scoring_receipt_sha256",
            "dependency_graph_sha256",
            "provenance_sha256",
            "command_identity",
            "authority_identity",
        ):
            _sha(getattr(self, name), name)
        _text(self.run_id, "run_id")
        _strings(self.observations, "observations")
        if any(not item.startswith(f"{STORY_ID}:") for item in self.observations):
            raise RootCauseDiagnosisError(
                "INVALID_OBSERVATION", "every observation must be scoped to ST-08.04"
            )
        _seal(self)

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "story_id": STORY_ID,
            "diagnosis_identity": self.diagnosis.diagnosis_identity,
            "graph_identity": None if self.graph is None else self.graph.graph_identity,
            "failure_subject_sha256": self.failure_subject_sha256,
            "predecessor_scoring_receipt_sha256": self.predecessor_scoring_receipt_sha256,
            "dependency_graph_sha256": self.dependency_graph_sha256,
            "run_id": self.run_id,
            "provenance_sha256": self.provenance_sha256,
            "command_identity": self.command_identity,
            "authority_identity": self.authority_identity,
            "observations": list(self.observations),
            "active": self.active,
            "repair_executed": False,
            "production_ready": False,
            "certified": False,
        }

    @property
    def receipt_identity(self) -> str:
        _require_unmutated(self, "root_cause_diagnosis_receipt")
        return canonical_sha256(self._construction_payload())

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "root_cause_diagnosis_receipt")
        payload = self._construction_payload()
        payload["receipt_identity"] = canonical_sha256(payload)
        return payload


@dataclass(frozen=True, slots=True, weakref_slot=True)
class DiagnosisTransitionReceipt:
    prior_receipt_identity: str
    action: DiagnosisAction
    command_identity: str
    authority_identity: str
    active_after: bool
    historical_receipt_preserved: bool = True

    def __post_init__(self) -> None:
        _sha(self.prior_receipt_identity, "prior_receipt_identity")
        if self.action not in {DiagnosisAction.INVALIDATE, DiagnosisAction.ROLLBACK}:
            raise RootCauseDiagnosisError("INVALID_TRANSITION_ACTION", "transition action is invalid")
        _sha(self.command_identity, "command_identity")
        _sha(self.authority_identity, "authority_identity")
        if not self.historical_receipt_preserved:
            raise RootCauseDiagnosisError("DESTRUCTIVE_HISTORY_CHANGE", "history must remain reproducible")
        _seal(self)

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "prior_receipt_identity": self.prior_receipt_identity,
            "action": self.action.value,
            "command_identity": self.command_identity,
            "authority_identity": self.authority_identity,
            "active_after": self.active_after,
            "historical_receipt_preserved": self.historical_receipt_preserved,
        }

    @property
    def transition_identity(self) -> str:
        _require_unmutated(self, "diagnosis_transition_receipt")
        return canonical_sha256(self._construction_payload())

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "diagnosis_transition_receipt")
        payload = self._construction_payload()
        payload["transition_identity"] = canonical_sha256(payload)
        return payload


@dataclass(frozen=True, slots=True, weakref_slot=True)
class DiagnosisRejectionReceipt:
    error_code: str
    command_id: str
    payload_sha256: str
    authority_identity: str | None
    partial_state_count: int = 0

    def __post_init__(self) -> None:
        _text(self.error_code, "error_code")
        _text(self.command_id, "command_id")
        _sha(self.payload_sha256, "payload_sha256")
        if self.authority_identity is not None:
            _sha(self.authority_identity, "authority_identity")
        if self.partial_state_count != 0:
            raise RootCauseDiagnosisError("PARTIAL_STATE_PROHIBITED", "failed command must leave zero state")
        _seal(self)

    @property
    def rejection_identity(self) -> str:
        _require_unmutated(self, "diagnosis_rejection_receipt")
        return canonical_sha256(_construction_payload(self))

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "diagnosis_rejection_receipt")
        payload = _construction_payload(self)
        payload["rejection_identity"] = canonical_sha256(payload)
        return payload


def compute_issue_payload_sha256(
    *,
    diagnosis: RootCauseDiagnosis,
    graph: RepairAndInvalidationGraph | None,
    failure_subject_sha256: str,
    predecessor_scoring_receipt_sha256: str,
    dependency_graph_sha256: str,
    run_id: str,
    provenance_sha256: str,
    observations: tuple[str, ...],
) -> str:
    return canonical_sha256(
        {
            "diagnosis_identity": diagnosis.diagnosis_identity,
            "graph_identity": None if graph is None else graph.graph_identity,
            "failure_subject_sha256": failure_subject_sha256,
            "predecessor_scoring_receipt_sha256": predecessor_scoring_receipt_sha256,
            "dependency_graph_sha256": dependency_graph_sha256,
            "run_id": run_id,
            "provenance_sha256": provenance_sha256,
            "observations": list(observations),
        }
    )


# Descriptive alias accepted by graph-oriented clients.
compute_diagnosis_payload_sha256 = compute_issue_payload_sha256


def _authorize(command: DiagnosisCommand, authority: DiagnosisAuthority, action: DiagnosisAction) -> None:
    if not isinstance(command, DiagnosisCommand):
        raise RootCauseDiagnosisError("INVALID_COMMAND_EVIDENCE", "typed command evidence is required")
    if not isinstance(authority, DiagnosisAuthority):
        raise RootCauseDiagnosisError("INVALID_AUTHORITY_EVIDENCE", "typed authority evidence is required")
    command.as_dict()
    authority.as_dict()
    if authority.status is not AuthorityStatus.ACTIVE:
        raise RootCauseDiagnosisError("INACTIVE_AUTHORITY", "authority is not active")
    if command.action is not action or action not in authority.permitted_actions:
        raise RootCauseDiagnosisError("UNAUTHORIZED_ACTION", "command action is not authorized")
    if command.expected_authority_identity != authority.authority_identity:
        raise RootCauseDiagnosisError("AUTHORITY_IDENTITY_MISMATCH", "authority identity differs")


def issue_root_cause_diagnosis_receipt(
    *,
    diagnosis: RootCauseDiagnosis,
    graph: RepairAndInvalidationGraph | None,
    failure_subject_sha256: str,
    predecessor_scoring_receipt_sha256: str,
    dependency_graph_sha256: str,
    run_id: str,
    provenance_sha256: str,
    observations: tuple[str, ...],
    command: DiagnosisCommand,
    authority: DiagnosisAuthority,
) -> RootCauseDiagnosisReceipt:
    _authorize(command, authority, DiagnosisAction.ISSUE)
    if predecessor_scoring_receipt_sha256 not in diagnosis.exact_lineage:
        raise RootCauseDiagnosisError(
            "PREDECESSOR_SCORING_LINEAGE_MISMATCH",
            "predecessor scoring receipt is not in diagnosis lineage",
        )
    if (
        failure_subject_sha256 not in diagnosis.exact_lineage
        and failure_subject_sha256 not in diagnosis.reproduction_or_evidence_refs
    ):
        raise RootCauseDiagnosisError(
            "FAILURE_SUBJECT_LINEAGE_MISMATCH", "failure subject is not bound to diagnosis evidence"
        )
    expected = compute_issue_payload_sha256(
        diagnosis=diagnosis,
        graph=graph,
        failure_subject_sha256=failure_subject_sha256,
        predecessor_scoring_receipt_sha256=predecessor_scoring_receipt_sha256,
        dependency_graph_sha256=dependency_graph_sha256,
        run_id=run_id,
        provenance_sha256=provenance_sha256,
        observations=observations,
    )
    if command.payload_sha256 != expected:
        raise RootCauseDiagnosisError("COMMAND_PAYLOAD_MISMATCH", "issue payload differs from command")
    if command.resource_id != diagnosis.diagnosis_identity:
        raise RootCauseDiagnosisError("COMMAND_RESOURCE_MISMATCH", "command targets another diagnosis")
    return RootCauseDiagnosisReceipt(
        diagnosis=diagnosis,
        graph=graph,
        failure_subject_sha256=failure_subject_sha256,
        predecessor_scoring_receipt_sha256=predecessor_scoring_receipt_sha256,
        dependency_graph_sha256=dependency_graph_sha256,
        run_id=run_id,
        provenance_sha256=provenance_sha256,
        command_identity=command.command_identity,
        authority_identity=authority.authority_identity,
        observations=observations,
    )


# Concise alias used by graph clients.
issue_root_cause_diagnosis = issue_root_cause_diagnosis_receipt


def validate_repeat_receipt(
    existing: RootCauseDiagnosisReceipt, repeated: RootCauseDiagnosisReceipt
) -> RootCauseDiagnosisReceipt:
    if existing.receipt_identity != repeated.receipt_identity:
        raise RootCauseDiagnosisError("CONFLICTING_REPEAT_COMMAND", "repeat payload conflicts with existing receipt")
    return existing


def _transition(
    receipt: RootCauseDiagnosisReceipt,
    command: DiagnosisCommand,
    authority: DiagnosisAuthority,
    action: DiagnosisAction,
    *,
    active_after: bool,
) -> DiagnosisTransitionReceipt:
    _authorize(command, authority, action)
    expected = canonical_sha256({"prior_receipt_identity": receipt.receipt_identity, "action": action.value})
    if command.payload_sha256 != expected:
        raise RootCauseDiagnosisError("COMMAND_PAYLOAD_MISMATCH", "transition payload differs")
    if command.resource_id != receipt.receipt_identity:
        raise RootCauseDiagnosisError("COMMAND_RESOURCE_MISMATCH", "transition targets another receipt")
    return DiagnosisTransitionReceipt(
        prior_receipt_identity=receipt.receipt_identity,
        action=action,
        command_identity=command.command_identity,
        authority_identity=authority.authority_identity,
        active_after=active_after,
    )


def invalidate_diagnosis_receipt(
    receipt: RootCauseDiagnosisReceipt,
    command: DiagnosisCommand,
    authority: DiagnosisAuthority,
) -> DiagnosisTransitionReceipt:
    return _transition(receipt, command, authority, DiagnosisAction.INVALIDATE, active_after=False)


def rollback_diagnosis_receipt(
    receipt: RootCauseDiagnosisReceipt,
    command: DiagnosisCommand,
    authority: DiagnosisAuthority,
) -> DiagnosisTransitionReceipt:
    return _transition(receipt, command, authority, DiagnosisAction.ROLLBACK, active_after=False)


def build_rejection_receipt(
    *, error: RootCauseDiagnosisError, command_id: str, payload_sha256: str, authority_identity: str | None
) -> DiagnosisRejectionReceipt:
    return DiagnosisRejectionReceipt(
        error_code=error.code,
        command_id=command_id,
        payload_sha256=payload_sha256,
        authority_identity=authority_identity,
    )
