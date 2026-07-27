"""Deterministic offline fresh-context evaluation contracts for ST-08.01.

The module evaluates supplied, repository-owned synthetic observations.  It does
not invoke a model or provider, assert empirical superiority, promote maturity,
or close any human, external-product, production, or certification evidence gate.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from datetime import datetime
from enum import Enum
from fractions import Fraction
import hashlib
import json
import re
import weakref
from typing import Any, Iterable, Sequence

from cmf_builder.application.authority import Action, AuthorityDenied, AuthorityService


STORY_ID = "ST-08.01"
MINIMUM_REPETITIONS = 3
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_PROHIBITED_CLAIM_TOKENS = frozenset(
    {
        "empirical_superiority",
        "behavioral_improvement_proven",
        "protected_benchmark_passed",
        "real_profile_validated",
        "provider_validated",
        "maturity_promoted",
        "production_ready",
        "production_certified",
        "certified",
        "conversational_certified",
        "external_target_compatible",
    }
)
_CONSTRUCTION_ANCHORS: dict[int, tuple[weakref.ReferenceType[Any], str]] = {}


class EvaluationLayer(str, Enum):
    CANONICAL_SKILL = "canonical_skill"
    HARNESS_ADAPTATION = "harness_adaptation"
    COMPOSITION_RECIPE = "composition_recipe"
    JIT_CAPSULE = "jit_capsule"
    END_TO_END_PHASE = "end_to_end_phase"


LAYER_ORDER = tuple(EvaluationLayer)


class CaseClass(str, Enum):
    POSITIVE_APPLICATION = "positive_application"
    NEAR_MISS = "near_miss"
    COUNTEREXAMPLE = "counterexample"
    MISSING_EVIDENCE = "missing_evidence"
    CONTRADICTION = "contradiction"
    TEMPTING_IRRELEVANT_CONTEXT = "tempting_irrelevant_context"
    RULE_VIOLATION_PRESSURE = "rule_violation_pressure"


class EvaluationArm(str, Enum):
    NO_GUIDANCE_CONTROL = "no_guidance_control"
    GOVERNED_CANDIDATE = "governed_candidate_behavior"


ARM_ORDER = (EvaluationArm.NO_GUIDANCE_CONTROL, EvaluationArm.GOVERNED_CANDIDATE)


class FreshContextEvaluationError(ValueError):
    """A typed, fail-closed rejection with no mutation side effects."""

    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)

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


def _safe_rejection_value(value: Any) -> Any:
    """Canonicalize even tampered dataclass values without trusting their methods."""

    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Fraction):
        return _fraction_dict(value)
    if is_dataclass(value) and not isinstance(value, type):
        return {
            item.name: _safe_rejection_value(getattr(value, item.name, None))
            for item in fields(value)
            if item.init
        }
    if isinstance(value, dict):
        return {
            str(key): _safe_rejection_value(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (tuple, list)):
        return [_safe_rejection_value(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return {"unsupported_type": type(value).__qualname__}


def _construction_payload(instance: Any) -> dict[str, Any]:
    payload_builder = getattr(instance, "_construction_payload", None)
    return payload_builder() if payload_builder is not None else instance.as_dict()


def _seal_constructed_identity(instance: Any) -> None:
    key = id(instance)

    def remove_anchor(reference: weakref.ReferenceType[Any], *, identity: int = key) -> None:
        current = _CONSTRUCTION_ANCHORS.get(identity)
        if current is not None and current[0] is reference:
            _CONSTRUCTION_ANCHORS.pop(identity, None)

    reference = weakref.ref(instance, remove_anchor)
    _CONSTRUCTION_ANCHORS[key] = (
        reference,
        canonical_sha256(_construction_payload(instance)),
    )


def _require_unmutated_constructed_identity(instance: Any, field_name: str) -> None:
    anchored = _CONSTRUCTION_ANCHORS.get(id(instance))
    if anchored is None or anchored[0]() is not instance:
        raise FreshContextEvaluationError(
            "UNANCHORED_GOVERNED_OBJECT",
            f"{field_name} lacks its module-private construction anchor",
            field=field_name,
        )
    sealed = anchored[1]
    try:
        current = canonical_sha256(_construction_payload(instance))
    except (AttributeError, TypeError, ValueError) as exc:
        raise FreshContextEvaluationError(
            "MUTATED_GOVERNED_OBJECT",
            f"{field_name} no longer has valid canonical semantics",
            field=field_name,
        ) from exc
    if current != sealed:
        raise FreshContextEvaluationError(
            "MUTATED_GOVERNED_OBJECT",
            f"{field_name} changed after immutable construction",
            field=field_name,
        )


def _require_text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FreshContextEvaluationError("MISSING_GOVERNED_FIELD", f"{field} is required", field=field)
    return value


def _require_sha256(value: str, field: str) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise FreshContextEvaluationError(
            "INVALID_IMMUTABLE_IDENTITY",
            f"{field} must be a lowercase SHA-256 digest",
            field=field,
        )
    return value


def _require_enum(value: object, enum_type: type[Enum], field: str) -> None:
    if not isinstance(value, enum_type):
        raise FreshContextEvaluationError(
            "INVALID_GOVERNED_TYPE",
            f"{field} must be a {enum_type.__name__}",
            field=field,
        )


def _require_bool(value: object, field: str) -> None:
    if type(value) is not bool:
        raise FreshContextEvaluationError(
            "INVALID_GOVERNED_TYPE", f"{field} must be a boolean", field=field
        )


def _reject_claim_vocabulary(value: str, field: str) -> None:
    normalized = re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")
    padded = f"_{normalized}_"
    matched = [token for token in _PROHIBITED_CLAIM_TOKENS if f"_{token}_" in padded]
    if matched:
        raise FreshContextEvaluationError(
            "PROHIBITED_MATURITY_OR_CERTIFICATION_CLAIM",
            f"{field} contains a prohibited evidence or maturity claim",
            field=field,
            matched=sorted(matched),
        )


def _fraction_dict(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def _ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


@dataclass(frozen=True, slots=True, weakref_slot=True)
class EvaluationObservation:
    event_type: str
    artifact_identity: str
    outcome: str
    failure_code: str | None
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text(self.event_type, "event_type")
        _require_sha256(self.artifact_identity, "artifact_identity")
        _require_text(self.outcome, "outcome")
        allowed = {
            f"{STORY_ID}:OfflineTrialPlanValidated": ("VALIDATED", None),
            f"{STORY_ID}:OfflineEvaluationCompleted": (
                "OFFLINE_SYNTHETIC_DELTAS_COMPUTED",
                None,
            ),
            f"{STORY_ID}:OfflineEvaluationRejected": ("REJECTED_NO_RECEIPT", "REQUIRED"),
        }
        expected = allowed.get(self.event_type)
        if expected is None or self.outcome != expected[0]:
            raise FreshContextEvaluationError(
                "INVALID_OBSERVATION_SEMANTICS",
                "observation event and outcome are not governed for ST-08.01",
            )
        if expected[1] is None and self.failure_code is not None:
            raise FreshContextEvaluationError(
                "INVALID_OBSERVATION_SEMANTICS", "success observations cannot carry a failure"
            )
        if expected[1] == "REQUIRED":
            _require_text(self.failure_code, "failure_code")
        if not isinstance(self.evidence_refs, tuple):
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE", "evidence_refs must be an immutable tuple"
            )
        for index, digest in enumerate(self.evidence_refs):
            _require_sha256(digest, f"evidence_refs[{index}]")
        _seal_constructed_identity(self)

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "story_id": STORY_ID,
            "artifact_identity": self.artifact_identity,
            "outcome": self.outcome,
            "failure_code": self.failure_code,
            "evidence_refs": list(self.evidence_refs),
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated_constructed_identity(self, "evaluation_observation")
        return self._construction_payload()


def fresh_context_construction_receipt_sha256(
    *,
    case_sha256: str,
    case_id: str,
    arm: EvaluationArm,
    repeat_index: int,
    evaluator_version: str,
    evaluator_identity: str,
    evaluator_input_sha256: str,
    generator_history: tuple[str, ...],
    mutable_cache_entries: tuple[str, ...],
    structural_isolation_only: bool = True,
) -> str:
    """Derive the construction receipt from the complete declared isolation boundary."""

    return canonical_sha256(
        {
            "story_id": STORY_ID,
            "case_sha256": case_sha256,
            "case_id": case_id,
            "arm": arm.value,
            "repeat_index": repeat_index,
            "evaluator_version": evaluator_version,
            "evaluator_identity": evaluator_identity,
            "evaluator_input_sha256": evaluator_input_sha256,
            "generator_history": list(generator_history),
            "mutable_cache_entries": list(mutable_cache_entries),
            "isolation_claim": "STRUCTURAL_ISOLATION_ONLY_NOT_RUNTIME_PROOF",
            "structural_isolation_only": structural_isolation_only,
        }
    )


@dataclass(frozen=True, slots=True, weakref_slot=True)
class FreshContextEvidence:
    """Immutable structural isolation evidence; not proof of runtime/process isolation."""

    case_sha256: str
    case_id: str
    arm: EvaluationArm
    repeat_index: int
    evaluator_version: str
    evaluator_identity: str
    evaluator_input_sha256: str
    generator_history: tuple[str, ...]
    mutable_cache_entries: tuple[str, ...]
    construction_receipt_sha256: str
    structural_isolation_only: bool = True

    def __post_init__(self) -> None:
        _require_sha256(self.case_sha256, "case_sha256")
        _require_sha256(self.evaluator_input_sha256, "evaluator_input_sha256")
        _require_sha256(self.construction_receipt_sha256, "construction_receipt_sha256")
        _require_text(self.case_id, "case_id")
        _require_enum(self.arm, EvaluationArm, "arm")
        _require_text(self.evaluator_version, "evaluator_version")
        _reject_claim_vocabulary(self.evaluator_version, "evaluator_version")
        _require_text(self.evaluator_identity, "evaluator_identity")
        if isinstance(self.repeat_index, bool) or not isinstance(self.repeat_index, int):
            raise FreshContextEvaluationError("INVALID_REPEAT_INDEX", "repeat_index must be an integer")
        if self.repeat_index < 1:
            raise FreshContextEvaluationError("INVALID_REPEAT_INDEX", "repeat_index must be positive")
        if not isinstance(self.generator_history, tuple) or self.generator_history:
            raise FreshContextEvaluationError(
                "NON_EMPTY_GENERATOR_HISTORY",
                "fresh evaluation context must declare empty generator history",
            )
        if not isinstance(self.mutable_cache_entries, tuple) or self.mutable_cache_entries:
            raise FreshContextEvaluationError(
                "NON_EMPTY_MUTABLE_CACHE",
                "fresh evaluation context must declare empty mutable cache",
            )
        _require_bool(self.structural_isolation_only, "structural_isolation_only")
        if not self.structural_isolation_only:
            raise FreshContextEvaluationError(
                "UNSUPPORTED_RUNTIME_ISOLATION_CLAIM",
                "ST-08.01 evidence proves structural isolation only",
            )
        expected_receipt = fresh_context_construction_receipt_sha256(
            case_sha256=self.case_sha256,
            case_id=self.case_id,
            arm=self.arm,
            repeat_index=self.repeat_index,
            evaluator_version=self.evaluator_version,
            evaluator_identity=self.evaluator_identity,
            evaluator_input_sha256=self.evaluator_input_sha256,
            generator_history=self.generator_history,
            mutable_cache_entries=self.mutable_cache_entries,
            structural_isolation_only=self.structural_isolation_only,
        )
        if self.construction_receipt_sha256 != expected_receipt:
            raise FreshContextEvaluationError(
                "FORGED_FRESH_CONTEXT_CONSTRUCTION_RECEIPT",
                "construction receipt must derive from the exact declared isolation boundary",
            )
        _seal_constructed_identity(self)

    @property
    def evidence_identity(self) -> str:
        return canonical_sha256(self.as_dict())

    @property
    def context_id(self) -> str:
        return f"fresh-context:{self.evidence_identity}"

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_sha256": self.case_sha256,
            "case_id": self.case_id,
            "arm": self.arm.value,
            "repeat_index": self.repeat_index,
            "evaluator_version": self.evaluator_version,
            "evaluator_identity": self.evaluator_identity,
            "evaluator_input_sha256": self.evaluator_input_sha256,
            "generator_history": list(self.generator_history),
            "mutable_cache_entries": list(self.mutable_cache_entries),
            "construction_receipt_sha256": self.construction_receipt_sha256,
            "isolation_claim": "STRUCTURAL_ISOLATION_ONLY_NOT_RUNTIME_PROOF",
            "structural_isolation_only": self.structural_isolation_only,
        }


@dataclass(frozen=True, slots=True, weakref_slot=True)
class EvaluationRejection:
    failure_code: str
    plan_identity: str
    results_identity: str
    approval_authority_identity_sha256: str
    rejected_input_identity: str
    observation: EvaluationObservation

    def __post_init__(self) -> None:
        _require_text(self.failure_code, "failure_code")
        for field in (
            "plan_identity",
            "results_identity",
            "approval_authority_identity_sha256",
            "rejected_input_identity",
        ):
            _require_sha256(getattr(self, field), field)
        if not isinstance(self.observation, EvaluationObservation):
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE", "observation must be EvaluationObservation"
            )
        if self.observation.event_type != f"{STORY_ID}:OfflineEvaluationRejected":
            raise FreshContextEvaluationError(
                "INVALID_REJECTION_EVIDENCE", "rejection must carry the governed rejection observation"
            )
        if self.observation.failure_code != self.failure_code:
            raise FreshContextEvaluationError(
                "INVALID_REJECTION_EVIDENCE", "failure code and observation must agree"
            )
        if self.observation.artifact_identity != self.rejected_input_identity:
            raise FreshContextEvaluationError(
                "INVALID_REJECTION_EVIDENCE",
                "rejection observation must identify the exact rejected input",
            )
        expected_refs = (
            self.plan_identity,
            self.results_identity,
            self.approval_authority_identity_sha256,
        )
        if self.observation.evidence_refs != expected_refs:
            raise FreshContextEvaluationError(
                "INVALID_REJECTION_EVIDENCE",
                "rejection observation evidence references must bind plan, results, and authority",
            )
        _require_unmutated_constructed_identity(self.observation, "rejection_observation")
        _seal_constructed_identity(self)

    @property
    def rejection_identity(self) -> str:
        validate_evaluation_rejection(self)
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "story_id": STORY_ID,
            "failure_code": self.failure_code,
            "plan_identity": self.plan_identity,
            "results_identity": self.results_identity,
            "approval_authority_identity_sha256": self.approval_authority_identity_sha256,
            "rejected_input_identity": self.rejected_input_identity,
            "observation": self.observation._construction_payload(),
            "result_status": "REJECTED_NO_EVALUATION_RECEIPT",
            "production_ready": False,
            "certified": False,
        }

    def as_dict(self) -> dict[str, Any]:
        validate_evaluation_rejection(self)
        return self._construction_payload()


def validate_evaluation_rejection(rejection: EvaluationRejection) -> None:
    if not isinstance(rejection, EvaluationRejection):
        raise FreshContextEvaluationError(
            "INVALID_GOVERNED_TYPE", "rejection must be EvaluationRejection"
        )
    _require_unmutated_constructed_identity(rejection, "evaluation_rejection")
    observation = rejection.observation
    if not isinstance(observation, EvaluationObservation):
        raise FreshContextEvaluationError(
            "INVALID_GOVERNED_TYPE", "rejection observation must be EvaluationObservation"
        )
    _require_unmutated_constructed_identity(observation, "rejection_observation")
    expected_refs = (
        rejection.plan_identity,
        rejection.results_identity,
        rejection.approval_authority_identity_sha256,
    )
    if (
        observation.event_type != f"{STORY_ID}:OfflineEvaluationRejected"
        or observation.outcome != "REJECTED_NO_RECEIPT"
        or observation.failure_code != rejection.failure_code
        or observation.artifact_identity != rejection.rejected_input_identity
        or observation.evidence_refs != expected_refs
    ):
        raise FreshContextEvaluationError(
            "INVALID_REJECTION_EVIDENCE",
            "rejection and observation no longer satisfy their exact governed bindings",
        )


@dataclass(frozen=True, slots=True, weakref_slot=True)
class EvaluationCase:
    case_id: str
    layer: EvaluationLayer
    case_class: CaseClass
    governed_input_sha256: str
    output_contract_sha256: str
    budget_contract_sha256: str
    expected_behavior_sha256: str
    dimensions: tuple[str, ...]
    authority_sha256: str
    provenance_sha256: str

    def __post_init__(self) -> None:
        _require_text(self.case_id, "case_id")
        _require_enum(self.layer, EvaluationLayer, "layer")
        _require_enum(self.case_class, CaseClass, "case_class")
        for field in (
            "governed_input_sha256",
            "output_contract_sha256",
            "budget_contract_sha256",
            "expected_behavior_sha256",
            "authority_sha256",
            "provenance_sha256",
        ):
            _require_sha256(getattr(self, field), field)
        if not isinstance(self.dimensions, tuple) or not self.dimensions:
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE", "dimensions must be a non-empty immutable tuple"
            )
        if len(self.dimensions) != len(set(self.dimensions)):
            raise FreshContextEvaluationError(
                "INVALID_EVALUATION_DIMENSIONS",
                "dimensions must be non-empty and duplicate-free",
                case_id=self.case_id,
            )
        if tuple(sorted(self.dimensions)) != self.dimensions:
            raise FreshContextEvaluationError(
                "NON_CANONICAL_DIMENSION_ORDER",
                "dimensions must use canonical lexical order",
                case_id=self.case_id,
            )
        for dimension in self.dimensions:
            _require_text(dimension, "dimension")
        _seal_constructed_identity(self)

    @property
    def case_identity(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "layer": self.layer.value,
            "case_class": self.case_class.value,
            "governed_input_sha256": self.governed_input_sha256,
            "output_contract_sha256": self.output_contract_sha256,
            "budget_contract_sha256": self.budget_contract_sha256,
            "expected_behavior_sha256": self.expected_behavior_sha256,
            "dimensions": list(self.dimensions),
            "authority_sha256": self.authority_sha256,
            "provenance_sha256": self.provenance_sha256,
        }


@dataclass(frozen=True, slots=True, weakref_slot=True)
class LayerSuite:
    suite_version: str
    layer: EvaluationLayer
    cases: tuple[EvaluationCase, ...]

    def __post_init__(self) -> None:
        _require_text(self.suite_version, "suite_version")
        _reject_claim_vocabulary(self.suite_version, "suite_version")
        _require_enum(self.layer, EvaluationLayer, "layer")
        if not isinstance(self.cases, tuple):
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE", "cases must be an immutable tuple"
            )
        if any(not isinstance(case, EvaluationCase) for case in self.cases):
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE", "suite cases must be EvaluationCase values"
            )
        if not self.cases:
            raise FreshContextEvaluationError("EMPTY_LAYER_SUITE", "every layer requires its own cases")
        if any(case.layer is not self.layer for case in self.cases):
            raise FreshContextEvaluationError(
                "CROSS_LAYER_CASE_INHERITANCE",
                "a layer suite cannot inherit cases from another layer",
                layer=self.layer.value,
            )
        case_ids = tuple(case.case_id for case in self.cases)
        if len(case_ids) != len(set(case_ids)):
            raise FreshContextEvaluationError("DUPLICATE_CASE_ID", "case IDs must be unique")
        if case_ids != tuple(sorted(case_ids)):
            raise FreshContextEvaluationError(
                "NON_CANONICAL_CASE_ORDER", "suite cases must be ordered by case_id"
            )
        _seal_constructed_identity(self)

    @property
    def suite_identity(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "suite_version": self.suite_version,
            "layer": self.layer.value,
            "cases": [case.as_dict() for case in self.cases],
        }


@dataclass(frozen=True, slots=True, weakref_slot=True)
class TrialPlan:
    plan_version: str
    suites: tuple[LayerSuite, ...]
    repetition_count: int
    evaluator_version: str
    benchmark_version: str
    authority_sha256: str
    provenance_sha256: str
    randomization_policy: str = "NONE_CANONICAL_LAYER_CASE_ARM_REPEAT_ORDER"

    def __post_init__(self) -> None:
        for field in ("plan_version", "evaluator_version", "benchmark_version"):
            value = _require_text(getattr(self, field), field)
            _reject_claim_vocabulary(value, field)
        if not isinstance(self.suites, tuple):
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE", "suites must be an immutable tuple"
            )
        if any(not isinstance(suite, LayerSuite) for suite in self.suites):
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE", "suites must contain LayerSuite values"
            )
        for field in ("authority_sha256", "provenance_sha256"):
            _require_sha256(getattr(self, field), field)
        if isinstance(self.repetition_count, bool) or not isinstance(self.repetition_count, int):
            raise FreshContextEvaluationError(
                "INVALID_REPETITION_COUNT",
                "repetition_count must be an integer",
            )
        if self.repetition_count < MINIMUM_REPETITIONS:
            raise FreshContextEvaluationError(
                "INSUFFICIENT_REPETITIONS",
                f"at least {MINIMUM_REPETITIONS} repetitions are required",
                repetition_count=self.repetition_count,
            )
        layers = tuple(suite.layer for suite in self.suites)
        if layers != LAYER_ORDER:
            raise FreshContextEvaluationError(
                "INCOMPLETE_OR_NON_CANONICAL_LAYER_COVERAGE",
                "the five layer suites must be distinct and canonically ordered",
                layers=[layer.value for layer in layers],
            )
        classes = {case.case_class for suite in self.suites for case in suite.cases}
        case_ids = [case.case_id for suite in self.suites for case in suite.cases]
        if len(case_ids) != len(set(case_ids)):
            raise FreshContextEvaluationError(
                "DUPLICATE_CASE_ID_ACROSS_LAYERS",
                "case IDs must be globally unique across all layer suites",
            )
        missing = [case_class.value for case_class in CaseClass if case_class not in classes]
        if missing:
            raise FreshContextEvaluationError(
                "INCOMPLETE_CASE_CLASS_COVERAGE",
                "all seven governed case classes are required",
                missing=missing,
            )
        if self.randomization_policy != "NONE_CANONICAL_LAYER_CASE_ARM_REPEAT_ORDER":
            raise FreshContextEvaluationError(
                "UNDECLARED_RANDOMIZATION_POLICY",
                "offline trials use the governed canonical ordering policy",
            )
        _seal_constructed_identity(self)

    @property
    def plan_identity(self) -> str:
        return canonical_sha256(self.as_dict())

    @property
    def cases(self) -> tuple[EvaluationCase, ...]:
        return tuple(case for suite in self.suites for case in suite.cases)

    @property
    def expected_trial_keys(self) -> tuple[tuple[str, str, int], ...]:
        return tuple(
            (case.case_id, arm.value, repeat)
            for suite in self.suites
            for case in suite.cases
            for arm in ARM_ORDER
            for repeat in range(1, self.repetition_count + 1)
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "plan_version": self.plan_version,
            "suites": [suite.as_dict() for suite in self.suites],
            "repetition_count": self.repetition_count,
            "evaluator_version": self.evaluator_version,
            "benchmark_version": self.benchmark_version,
            "authority_sha256": self.authority_sha256,
            "provenance_sha256": self.provenance_sha256,
            "randomization_policy": self.randomization_policy,
            "execution_mode": "OFFLINE_REPOSITORY_OWNED_SYNTHETIC_ONLY",
        }


@dataclass(frozen=True, slots=True, weakref_slot=True)
class DimensionScore:
    dimension: str
    score_basis_points: int

    def __post_init__(self) -> None:
        _require_text(self.dimension, "dimension")
        if (
            isinstance(self.score_basis_points, bool)
            or not isinstance(self.score_basis_points, int)
            or not 0 <= self.score_basis_points <= 10_000
        ):
            raise FreshContextEvaluationError(
                "INVALID_DIMENSION_SCORE",
                "score_basis_points must be an integer from 0 through 10000",
                dimension=self.dimension,
            )
        _seal_constructed_identity(self)

    def as_dict(self) -> dict[str, Any]:
        return {"dimension": self.dimension, "score_basis_points": self.score_basis_points}


@dataclass(frozen=True, slots=True, weakref_slot=True)
class TrialResult:
    plan_sha256: str
    case_sha256: str
    case_id: str
    layer: EvaluationLayer
    arm: EvaluationArm
    repeat_index: int
    fresh_context: FreshContextEvidence
    output_sha256: str
    evaluator_version: str
    generator_identity: str
    evaluator_identity: str
    approval_authority_identity: str
    dimension_scores: tuple[DimensionScore, ...]
    expected_behavior_passed: bool
    result_provenance_sha256: str

    def __post_init__(self) -> None:
        for field in ("plan_sha256", "case_sha256", "output_sha256", "result_provenance_sha256"):
            _require_sha256(getattr(self, field), field)
        for field in (
            "case_id",
            "evaluator_version",
            "generator_identity",
            "evaluator_identity",
            "approval_authority_identity",
        ):
            _require_text(getattr(self, field), field)
        _reject_claim_vocabulary(self.evaluator_version, "evaluator_version")
        _require_enum(self.layer, EvaluationLayer, "layer")
        _require_enum(self.arm, EvaluationArm, "arm")
        if not isinstance(self.fresh_context, FreshContextEvidence):
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE", "fresh_context must be FreshContextEvidence"
            )
        if not isinstance(self.dimension_scores, tuple) or any(
            not isinstance(score, DimensionScore) for score in self.dimension_scores
        ):
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE",
                "dimension_scores must be an immutable tuple of DimensionScore values",
            )
        if isinstance(self.repeat_index, bool) or not isinstance(self.repeat_index, int):
            raise FreshContextEvaluationError(
                "INVALID_REPEAT_INDEX", "repeat_index must be an integer"
            )
        if self.repeat_index < 1:
            raise FreshContextEvaluationError("INVALID_REPEAT_INDEX", "repeat_index must be positive")
        _require_bool(self.expected_behavior_passed, "expected_behavior_passed")
        if self.generator_identity == self.evaluator_identity:
            raise FreshContextEvaluationError(
                "GENERATOR_CONTEXT_REUSED_BY_EVALUATOR",
                "the independent evaluator cannot be the generator",
                case_id=self.case_id,
            )
        if self.generator_identity == self.approval_authority_identity:
            raise FreshContextEvaluationError(
                "GENERATOR_IS_SOLE_APPROVER",
                "the generator cannot solely approve its own output",
                case_id=self.case_id,
            )
        if (
            self.fresh_context.case_sha256 != self.case_sha256
            or self.fresh_context.case_id != self.case_id
            or self.fresh_context.arm is not self.arm
            or self.fresh_context.repeat_index != self.repeat_index
            or self.fresh_context.evaluator_version != self.evaluator_version
            or self.fresh_context.evaluator_identity != self.evaluator_identity
        ):
            raise FreshContextEvaluationError(
                "FRESH_CONTEXT_BINDING_MISMATCH",
                "fresh-context evidence must bind the exact case, arm, repeat, and evaluator",
            )
        dimensions = tuple(score.dimension for score in self.dimension_scores)
        if not dimensions or len(dimensions) != len(set(dimensions)):
            raise FreshContextEvaluationError(
                "INVALID_RESULT_DIMENSION_COVERAGE",
                "result dimensions must be non-empty and unique",
            )
        if dimensions != tuple(sorted(dimensions)):
            raise FreshContextEvaluationError(
                "NON_CANONICAL_RESULT_DIMENSION_ORDER",
                "result dimensions must use canonical lexical order",
            )
        _seal_constructed_identity(self)

    @property
    def aggregate_score(self) -> Fraction:
        return Fraction(
            sum(score.score_basis_points for score in self.dimension_scores),
            len(self.dimension_scores),
        )

    @property
    def fresh_context_id(self) -> str:
        return self.fresh_context.context_id

    @property
    def trial_identity(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "plan_sha256": self.plan_sha256,
            "case_sha256": self.case_sha256,
            "case_id": self.case_id,
            "layer": self.layer.value,
            "arm": self.arm.value,
            "repeat_index": self.repeat_index,
            "fresh_context": self.fresh_context.as_dict(),
            "fresh_context_identity": self.fresh_context.evidence_identity,
            "output_sha256": self.output_sha256,
            "evaluator_version": self.evaluator_version,
            "generator_identity": self.generator_identity,
            "evaluator_identity": self.evaluator_identity,
            "approval_authority_identity": self.approval_authority_identity,
            "dimension_scores": [score.as_dict() for score in self.dimension_scores],
            "expected_behavior_passed": self.expected_behavior_passed,
            "result_provenance_sha256": self.result_provenance_sha256,
        }


@dataclass(frozen=True, slots=True)
class ArmStatistics:
    trial_count: int
    mean_score: Fraction
    minimum_score: Fraction
    variance: Fraction
    failure_frequency: Fraction
    confidence_estimate_basis_points: int
    confidence_method: str = "DEVELOPMENT_DESCRIPTIVE_STABILITY_V1_NOT_A_THRESHOLD"

    def __post_init__(self) -> None:
        if isinstance(self.trial_count, bool) or not isinstance(self.trial_count, int) or self.trial_count < 1:
            raise FreshContextEvaluationError("INVALID_ARM_STATISTICS", "trial_count must be positive")
        for field in ("mean_score", "minimum_score", "variance", "failure_frequency"):
            if not isinstance(getattr(self, field), Fraction):
                raise FreshContextEvaluationError(
                    "INVALID_ARM_STATISTICS", f"{field} must be an exact Fraction"
                )
        if self.variance < 0 or not 0 <= self.failure_frequency <= 1:
            raise FreshContextEvaluationError("INVALID_ARM_STATISTICS", "statistics are out of range")
        if (
            isinstance(self.confidence_estimate_basis_points, bool)
            or not isinstance(self.confidence_estimate_basis_points, int)
            or not 0 <= self.confidence_estimate_basis_points <= 10_000
        ):
            raise FreshContextEvaluationError("INVALID_ARM_STATISTICS", "confidence is out of range")
        _require_text(self.confidence_method, "confidence_method")
        _reject_claim_vocabulary(self.confidence_method, "confidence_method")

    @classmethod
    def from_results(cls, results: Sequence[TrialResult]) -> "ArmStatistics":
        if not results:
            raise FreshContextEvaluationError("MISSING_ARM_RESULTS", "each arm requires results")
        scores = tuple(result.aggregate_score for result in results)
        mean = sum(scores, Fraction()) / len(scores)
        variance = sum(((score - mean) ** 2 for score in scores), Fraction()) / len(scores)
        failures = sum(not result.expected_behavior_passed for result in results)
        failure_frequency = Fraction(failures, len(results))
        score_range = max(scores) - min(scores)
        confidence = max(
            0,
            10_000
            - _ceil_fraction(failure_frequency * 10_000)
            - _ceil_fraction(score_range),
        )
        return cls(
            trial_count=len(results),
            mean_score=mean,
            minimum_score=min(scores),
            variance=variance,
            failure_frequency=failure_frequency,
            confidence_estimate_basis_points=confidence,
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "trial_count": self.trial_count,
            "mean_score": _fraction_dict(self.mean_score),
            "minimum_score": _fraction_dict(self.minimum_score),
            "variance": _fraction_dict(self.variance),
            "failure_frequency": _fraction_dict(self.failure_frequency),
            "confidence_estimate_basis_points": self.confidence_estimate_basis_points,
            "confidence_method": self.confidence_method,
        }


@dataclass(frozen=True, slots=True)
class CaseComparison:
    case_id: str
    case_identity: str
    control: ArmStatistics
    candidate: ArmStatistics
    candidate_minus_control_mean: Fraction
    control_target_failure_absent: bool
    skill_necessity_signal: str

    def __post_init__(self) -> None:
        _require_text(self.case_id, "case_id")
        _require_sha256(self.case_identity, "case_identity")
        if not isinstance(self.control, ArmStatistics) or not isinstance(self.candidate, ArmStatistics):
            raise FreshContextEvaluationError(
                "INVALID_CASE_COMPARISON", "both comparison arms require governed statistics"
            )
        if not isinstance(self.candidate_minus_control_mean, Fraction):
            raise FreshContextEvaluationError(
                "INVALID_CASE_COMPARISON", "candidate delta must be an exact Fraction"
            )
        if self.candidate_minus_control_mean != self.candidate.mean_score - self.control.mean_score:
            raise FreshContextEvaluationError(
                "FORGED_CASE_COMPARISON", "reported delta does not match arm statistics"
            )
        _require_bool(self.control_target_failure_absent, "control_target_failure_absent")
        expected_signal = (
            "CONTROL_SUCCEEDS_NO_SKILL_NECESSITY_ATTRIBUTION"
            if self.control_target_failure_absent
            else "CONTROL_FAILURE_OBSERVED_DELTA_ONLY"
        )
        if self.skill_necessity_signal != expected_signal:
            raise FreshContextEvaluationError(
                "FORGED_CASE_COMPARISON", "skill-necessity signal is inconsistent"
            )

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "case_identity": self.case_identity,
            "control": self.control.as_dict(),
            "candidate": self.candidate.as_dict(),
            "candidate_minus_control_mean": _fraction_dict(self.candidate_minus_control_mean),
            "control_target_failure_absent": self.control_target_failure_absent,
            "skill_necessity_signal": self.skill_necessity_signal,
            "claim_ceiling": "COMPUTED_OFFLINE_DELTA_ONLY",
        }


@dataclass(frozen=True, slots=True)
class LayerEvaluation:
    layer: EvaluationLayer
    suite_identity: str
    comparisons: tuple[CaseComparison, ...]
    status: str = "OFFLINE_DELTAS_COMPUTED_NO_INHERITED_LAYER_PASS"

    def __post_init__(self) -> None:
        _require_enum(self.layer, EvaluationLayer, "layer")
        _require_sha256(self.suite_identity, "suite_identity")
        if not isinstance(self.comparisons, tuple) or not self.comparisons:
            raise FreshContextEvaluationError(
                "INVALID_LAYER_EVALUATION", "layer comparisons must be a non-empty immutable tuple"
            )
        if any(not isinstance(item, CaseComparison) for item in self.comparisons):
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE", "comparisons must contain CaseComparison values"
            )
        ids = tuple(item.case_id for item in self.comparisons)
        if ids != tuple(sorted(ids)) or len(ids) != len(set(ids)):
            raise FreshContextEvaluationError(
                "INVALID_LAYER_EVALUATION", "layer comparison order and identities must be canonical"
            )
        if self.status != "OFFLINE_DELTAS_COMPUTED_NO_INHERITED_LAYER_PASS":
            raise FreshContextEvaluationError(
                "PROHIBITED_LAYER_STATUS", "layer status cannot assert or inherit a pass claim"
            )

    def as_dict(self) -> dict[str, Any]:
        return {
            "layer": self.layer.value,
            "suite_identity": self.suite_identity,
            "comparisons": [comparison.as_dict() for comparison in self.comparisons],
            "status": self.status,
            "inherits_other_layer_result": False,
        }


@dataclass(frozen=True, slots=True)
class EvaluationReceipt:
    plan_identity: str
    benchmark_version: str
    evaluator_version: str
    authority_sha256: str
    approval_authority_identity_sha256: str
    provenance_sha256: str
    layer_evaluations: tuple[LayerEvaluation, ...]
    result_identities: tuple[str, ...]
    observations: tuple[EvaluationObservation, ...]

    def __post_init__(self) -> None:
        for field in (
            "plan_identity",
            "authority_sha256",
            "approval_authority_identity_sha256",
            "provenance_sha256",
        ):
            _require_sha256(getattr(self, field), field)
        for field in ("benchmark_version", "evaluator_version"):
            value = _require_text(getattr(self, field), field)
            _reject_claim_vocabulary(value, field)
        if not isinstance(self.layer_evaluations, tuple) or any(
            not isinstance(layer, LayerEvaluation) for layer in self.layer_evaluations
        ):
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE", "layer_evaluations must contain LayerEvaluation values"
            )
        if tuple(layer.layer for layer in self.layer_evaluations) != LAYER_ORDER:
            raise FreshContextEvaluationError(
                "FORGED_EVALUATION_RECEIPT", "receipt must contain exactly five canonical layers"
            )
        if not isinstance(self.result_identities, tuple):
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE", "result_identities must be an immutable tuple"
            )
        if not self.result_identities or len(self.result_identities) != len(set(self.result_identities)):
            raise FreshContextEvaluationError(
                "FORGED_EVALUATION_RECEIPT", "result identities must be non-empty and unique"
            )
        for index, digest in enumerate(self.result_identities):
            _require_sha256(digest, f"result_identities[{index}]")
        if not isinstance(self.observations, tuple) or any(
            not isinstance(item, EvaluationObservation) for item in self.observations
        ):
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE", "observations must contain EvaluationObservation values"
            )
        if len(self.observations) != 2:
            raise FreshContextEvaluationError(
                "FORGED_EVALUATION_RECEIPT", "receipt requires exactly two governed success observations"
            )
        expected_events = (
            f"{STORY_ID}:OfflineTrialPlanValidated",
            f"{STORY_ID}:OfflineEvaluationCompleted",
        )
        if tuple(item.event_type for item in self.observations) != expected_events:
            raise FreshContextEvaluationError(
                "FORGED_EVALUATION_RECEIPT", "receipt observations are not canonical"
            )
        plan_observation, completion_observation = self.observations
        expected_suite_refs = tuple(layer.suite_identity for layer in self.layer_evaluations)
        if (
            plan_observation.artifact_identity != self.plan_identity
            or plan_observation.evidence_refs != expected_suite_refs
            or plan_observation.outcome != "VALIDATED"
            or plan_observation.failure_code is not None
        ):
            raise FreshContextEvaluationError(
                "FORGED_EVALUATION_RECEIPT",
                "plan observation must exactly bind the plan and five suite identities",
            )
        expected_result_set_identity = canonical_sha256(list(self.result_identities))
        if (
            completion_observation.artifact_identity != expected_result_set_identity
            or completion_observation.evidence_refs != (self.plan_identity,)
            or completion_observation.outcome != "OFFLINE_SYNTHETIC_DELTAS_COMPUTED"
            or completion_observation.failure_code is not None
        ):
            raise FreshContextEvaluationError(
                "FORGED_EVALUATION_RECEIPT",
                "completion observation must exactly bind canonical results and the plan",
            )

    @property
    def receipt_identity(self) -> str:
        return canonical_sha256(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "story_id": STORY_ID,
            "plan_identity": self.plan_identity,
            "benchmark_version": self.benchmark_version,
            "evaluator_version": self.evaluator_version,
            "authority_sha256": self.authority_sha256,
            "approval_authority_identity_sha256": self.approval_authority_identity_sha256,
            "provenance_sha256": self.provenance_sha256,
            "layer_evaluations": [layer.as_dict() for layer in self.layer_evaluations],
            "result_identities": list(self.result_identities),
            "observations": [observation.as_dict() for observation in self.observations],
            "result_status": "OFFLINE_SYNTHETIC_STRUCTURAL_DELTAS_ONLY",
            "fresh_context_claim": "STRUCTURAL_ISOLATION_ONLY_NOT_RUNTIME_PROOF",
            "empirical_superiority_claimed": False,
            "behavioral_improvement_proven": False,
            "maturity_promoted": False,
            "evidence_gate_closed": False,
            "production_ready": False,
            "certified": False,
        }


def compile_trial_plan(
    *,
    plan_version: str,
    suites: Sequence[LayerSuite],
    repetition_count: int,
    evaluator_version: str,
    benchmark_version: str,
    authority_sha256: str,
    provenance_sha256: str,
) -> TrialPlan:
    """Compile the exact offline plan without executing a trial."""

    return TrialPlan(
        plan_version=plan_version,
        suites=tuple(suites),
        repetition_count=repetition_count,
        evaluator_version=evaluator_version,
        benchmark_version=benchmark_version,
        authority_sha256=authority_sha256,
        provenance_sha256=provenance_sha256,
    )


def fresh_context_evaluator_input_sha256(
    *,
    case: EvaluationCase,
    arm: EvaluationArm,
    repeat_index: int,
    evaluator_version: str,
    evaluator_identity: str,
) -> str:
    """Return the governed evaluator-input identity for one isolated trial."""

    _require_enum(arm, EvaluationArm, "arm")
    if isinstance(repeat_index, bool) or not isinstance(repeat_index, int) or repeat_index < 1:
        raise FreshContextEvaluationError("INVALID_REPEAT_INDEX", "repeat_index must be positive")
    _require_text(evaluator_version, "evaluator_version")
    _reject_claim_vocabulary(evaluator_version, "evaluator_version")
    _require_text(evaluator_identity, "evaluator_identity")
    return canonical_sha256(
        {
            "story_id": STORY_ID,
            "case_identity": case.case_identity,
            "case_id": case.case_id,
            "arm": arm.value,
            "repeat_index": repeat_index,
            "evaluator_version": evaluator_version,
            "evaluator_identity": evaluator_identity,
            "governed_input_sha256": case.governed_input_sha256,
            "output_contract_sha256": case.output_contract_sha256,
            "budget_contract_sha256": case.budget_contract_sha256,
            "expected_behavior_sha256": case.expected_behavior_sha256,
            "dimensions": list(case.dimensions),
        }
    )


def _revalidate_case_graph(case: EvaluationCase) -> EvaluationCase:
    if not isinstance(case, EvaluationCase):
        raise FreshContextEvaluationError(
            "INVALID_GOVERNED_TYPE", "plan cases must be EvaluationCase values"
        )
    _require_unmutated_constructed_identity(case, "evaluation_case")
    if not isinstance(case.dimensions, tuple):
        raise FreshContextEvaluationError(
            "MUTATED_GOVERNED_OBJECT", "evaluation case dimensions lost immutable tuple form"
        )
    reconstructed = EvaluationCase(
        case_id=case.case_id,
        layer=case.layer,
        case_class=case.case_class,
        governed_input_sha256=case.governed_input_sha256,
        output_contract_sha256=case.output_contract_sha256,
        budget_contract_sha256=case.budget_contract_sha256,
        expected_behavior_sha256=case.expected_behavior_sha256,
        dimensions=case.dimensions,
        authority_sha256=case.authority_sha256,
        provenance_sha256=case.provenance_sha256,
    )
    if canonical_json_bytes(case.as_dict()) != canonical_json_bytes(reconstructed.as_dict()):
        raise FreshContextEvaluationError(
            "MUTATED_GOVERNED_OBJECT", "evaluation case cannot be reconstructed exactly"
        )
    return reconstructed


def _revalidate_plan_graph(plan: TrialPlan) -> TrialPlan:
    if not isinstance(plan, TrialPlan):
        raise FreshContextEvaluationError(
            "INVALID_GOVERNED_TYPE", "plan must be a TrialPlan"
        )
    _require_unmutated_constructed_identity(plan, "trial_plan")
    if not isinstance(plan.suites, tuple):
        raise FreshContextEvaluationError(
            "MUTATED_GOVERNED_OBJECT", "trial plan suites lost immutable tuple form"
        )
    suites: list[LayerSuite] = []
    for suite_index, suite in enumerate(plan.suites):
        if not isinstance(suite, LayerSuite):
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE", "plan suites must be LayerSuite values"
            )
        _require_unmutated_constructed_identity(suite, f"layer_suite[{suite_index}]")
        if not isinstance(suite.cases, tuple):
            raise FreshContextEvaluationError(
                "MUTATED_GOVERNED_OBJECT", "layer suite cases lost immutable tuple form"
            )
        cases = tuple(_revalidate_case_graph(case) for case in suite.cases)
        reconstructed_suite = LayerSuite(
            suite_version=suite.suite_version,
            layer=suite.layer,
            cases=cases,
        )
        if canonical_json_bytes(suite.as_dict()) != canonical_json_bytes(
            reconstructed_suite.as_dict()
        ):
            raise FreshContextEvaluationError(
                "MUTATED_GOVERNED_OBJECT", "layer suite cannot be reconstructed exactly"
            )
        suites.append(reconstructed_suite)
    reconstructed = TrialPlan(
        plan_version=plan.plan_version,
        suites=tuple(suites),
        repetition_count=plan.repetition_count,
        evaluator_version=plan.evaluator_version,
        benchmark_version=plan.benchmark_version,
        authority_sha256=plan.authority_sha256,
        provenance_sha256=plan.provenance_sha256,
        randomization_policy=plan.randomization_policy,
    )
    if canonical_json_bytes(plan.as_dict()) != canonical_json_bytes(reconstructed.as_dict()):
        raise FreshContextEvaluationError(
            "MUTATED_GOVERNED_OBJECT", "trial plan cannot be reconstructed exactly"
        )
    return reconstructed


def _revalidate_result_graph(result: TrialResult) -> TrialResult:
    if not isinstance(result, TrialResult):
        raise FreshContextEvaluationError(
            "INVALID_GOVERNED_TYPE", "results must contain TrialResult values"
        )
    _require_unmutated_constructed_identity(result, "trial_result")
    if not isinstance(result.dimension_scores, tuple):
        raise FreshContextEvaluationError(
            "MUTATED_GOVERNED_OBJECT", "dimension scores lost immutable tuple form"
        )
    context = result.fresh_context
    if not isinstance(context, FreshContextEvidence):
        raise FreshContextEvaluationError(
            "INVALID_GOVERNED_TYPE", "trial result requires FreshContextEvidence"
        )
    _require_unmutated_constructed_identity(context, "fresh_context")
    if not isinstance(context.generator_history, tuple) or not isinstance(
        context.mutable_cache_entries, tuple
    ):
        raise FreshContextEvaluationError(
            "MUTATED_GOVERNED_OBJECT", "fresh-context isolation collections lost tuple form"
        )
    reconstructed_context = FreshContextEvidence(
        case_sha256=context.case_sha256,
        case_id=context.case_id,
        arm=context.arm,
        repeat_index=context.repeat_index,
        evaluator_version=context.evaluator_version,
        evaluator_identity=context.evaluator_identity,
        evaluator_input_sha256=context.evaluator_input_sha256,
        generator_history=context.generator_history,
        mutable_cache_entries=context.mutable_cache_entries,
        construction_receipt_sha256=context.construction_receipt_sha256,
        structural_isolation_only=context.structural_isolation_only,
    )
    scores: list[DimensionScore] = []
    for score_index, score in enumerate(result.dimension_scores):
        if not isinstance(score, DimensionScore):
            raise FreshContextEvaluationError(
                "INVALID_GOVERNED_TYPE", "dimension_scores must contain DimensionScore values"
            )
        _require_unmutated_constructed_identity(score, f"dimension_score[{score_index}]")
        scores.append(DimensionScore(score.dimension, score.score_basis_points))
    reconstructed = TrialResult(
        plan_sha256=result.plan_sha256,
        case_sha256=result.case_sha256,
        case_id=result.case_id,
        layer=result.layer,
        arm=result.arm,
        repeat_index=result.repeat_index,
        fresh_context=reconstructed_context,
        output_sha256=result.output_sha256,
        evaluator_version=result.evaluator_version,
        generator_identity=result.generator_identity,
        evaluator_identity=result.evaluator_identity,
        approval_authority_identity=result.approval_authority_identity,
        dimension_scores=tuple(scores),
        expected_behavior_passed=result.expected_behavior_passed,
        result_provenance_sha256=result.result_provenance_sha256,
    )
    if canonical_json_bytes(result.as_dict()) != canonical_json_bytes(reconstructed.as_dict()):
        raise FreshContextEvaluationError(
            "MUTATED_GOVERNED_OBJECT", "trial result cannot be reconstructed exactly"
        )
    return reconstructed


def build_rejection_evidence(
    error: FreshContextEvaluationError,
    *,
    plan: TrialPlan,
    results: Iterable[TrialResult],
    approval_actor_id: str,
) -> EvaluationRejection:
    """Derive deterministic rejection evidence from the exact governed boundary inputs."""

    supplied = tuple(results)
    _require_text(approval_actor_id, "approval_actor_id")
    plan_snapshot = _safe_rejection_value(plan)
    result_snapshots = tuple(_safe_rejection_value(result) for result in supplied)
    plan_identity = canonical_sha256(
        {"type": "REJECTED_TRIAL_PLAN_SNAPSHOT", "value": plan_snapshot}
    )
    result_identities = tuple(sorted(canonical_sha256(item) for item in result_snapshots))
    results_identity = canonical_sha256(result_identities)
    actor_identity = canonical_sha256(
        {
            "actor_id": approval_actor_id,
            "action": Action.EVALUATE_FRESH_CONTEXTS.value,
            "resource_id": plan_identity,
        }
    )
    rejected_input = canonical_sha256(
        {
            "plan": plan_snapshot,
            "results": sorted(result_snapshots, key=canonical_sha256),
            "approval_actor_id": approval_actor_id,
            "failure_code": error.code,
            "failure_context": _safe_rejection_value(error.context),
        }
    )
    observation = EvaluationObservation(
        event_type=f"{STORY_ID}:OfflineEvaluationRejected",
        artifact_identity=rejected_input,
        outcome="REJECTED_NO_RECEIPT",
        failure_code=error.code,
        evidence_refs=(plan_identity, results_identity, actor_identity),
    )
    return EvaluationRejection(
        failure_code=error.code,
        plan_identity=plan_identity,
        results_identity=results_identity,
        approval_authority_identity_sha256=actor_identity,
        rejected_input_identity=rejected_input,
        observation=observation,
    )


def _build_evaluation_receipt(
    *, plan: TrialPlan, results: Iterable[TrialResult], approval_actor_id: str
) -> EvaluationReceipt:
    """Validate supplied offline results and compute deterministic descriptive deltas."""

    supplied = tuple(results)
    cases = {case.case_id: case for case in plan.cases}
    expected_keys = set(plan.expected_trial_keys)
    actual: dict[tuple[str, str, int], TrialResult] = {}
    contexts: set[str] = set()

    for result in supplied:
        case = cases.get(result.case_id)
        if case is None:
            raise FreshContextEvaluationError(
                "UNKNOWN_EVALUATION_CASE", "result references a case outside the plan"
            )
        if result.plan_sha256 != plan.plan_identity:
            raise FreshContextEvaluationError("STALE_OR_ALTERED_PLAN", "result plan identity differs")
        if result.case_sha256 != case.case_identity or result.layer is not case.layer:
            raise FreshContextEvaluationError(
                "STALE_OR_ALTERED_CASE", "result case identity or layer differs"
            )
        if result.evaluator_version != plan.evaluator_version:
            raise FreshContextEvaluationError(
                "EVALUATOR_VERSION_DRIFT", "result evaluator version differs from the plan"
            )
        if result.repeat_index > plan.repetition_count:
            raise FreshContextEvaluationError("UNDECLARED_REPEAT", "repeat is outside the plan")
        dimensions = tuple(score.dimension for score in result.dimension_scores)
        if dimensions != case.dimensions:
            raise FreshContextEvaluationError(
                "RESULT_DIMENSION_DRIFT",
                "both arms must use the exact governed dimensions",
                case_id=case.case_id,
            )
        expected_evaluator_input = fresh_context_evaluator_input_sha256(
            case=case,
            arm=result.arm,
            repeat_index=result.repeat_index,
            evaluator_version=result.evaluator_version,
            evaluator_identity=result.evaluator_identity,
        )
        if result.fresh_context.evaluator_input_sha256 != expected_evaluator_input:
            raise FreshContextEvaluationError(
                "ALTERED_EVALUATOR_INPUT",
                "fresh-context evidence does not bind the governed evaluator input",
                case_id=case.case_id,
            )
        if result.approval_authority_identity != approval_actor_id:
            raise FreshContextEvaluationError(
                "APPROVAL_AUTHORITY_IDENTITY_MISMATCH",
                "all results must bind the exact authorized approval actor",
            )
        if result.evaluator_identity == approval_actor_id:
            raise FreshContextEvaluationError(
                "EVALUATOR_IS_APPROVAL_AUTHORITY",
                "the independent evaluator cannot approve its own result",
            )
        key = (result.case_id, result.arm.value, result.repeat_index)
        if key in actual:
            raise FreshContextEvaluationError("DUPLICATE_TRIAL_RESULT", "trial result is duplicated")
        if result.fresh_context_id in contexts:
            raise FreshContextEvaluationError(
                "REUSED_EVALUATOR_CONTEXT",
                "every arm and repetition requires a fresh evaluator context",
            )
        contexts.add(result.fresh_context_id)
        actual[key] = result

    missing = sorted(expected_keys - set(actual))
    unexpected = sorted(set(actual) - expected_keys)
    if missing or unexpected:
        raise FreshContextEvaluationError(
            "INCOMPLETE_PAIRED_TRIALS",
            "every case requires both arms and all declared repetitions",
            missing=missing,
            unexpected=unexpected,
        )

    layer_evaluations: list[LayerEvaluation] = []
    ordered_results: list[TrialResult] = []
    for suite in plan.suites:
        comparisons: list[CaseComparison] = []
        for case in suite.cases:
            control = tuple(
                actual[(case.case_id, EvaluationArm.NO_GUIDANCE_CONTROL.value, repeat)]
                for repeat in range(1, plan.repetition_count + 1)
            )
            candidate = tuple(
                actual[(case.case_id, EvaluationArm.GOVERNED_CANDIDATE.value, repeat)]
                for repeat in range(1, plan.repetition_count + 1)
            )
            ordered_results.extend(control)
            ordered_results.extend(candidate)
            control_stats = ArmStatistics.from_results(control)
            candidate_stats = ArmStatistics.from_results(candidate)
            control_absence = all(item.expected_behavior_passed for item in control)
            signal = (
                "CONTROL_SUCCEEDS_NO_SKILL_NECESSITY_ATTRIBUTION"
                if control_absence
                else "CONTROL_FAILURE_OBSERVED_DELTA_ONLY"
            )
            comparisons.append(
                CaseComparison(
                    case_id=case.case_id,
                    case_identity=case.case_identity,
                    control=control_stats,
                    candidate=candidate_stats,
                    candidate_minus_control_mean=(
                        candidate_stats.mean_score - control_stats.mean_score
                    ),
                    control_target_failure_absent=control_absence,
                    skill_necessity_signal=signal,
                )
            )
        layer_evaluations.append(
            LayerEvaluation(
                layer=suite.layer,
                suite_identity=suite.suite_identity,
                comparisons=tuple(comparisons),
            )
        )

    plan_observation = EvaluationObservation(
        event_type=f"{STORY_ID}:OfflineTrialPlanValidated",
        artifact_identity=plan.plan_identity,
        outcome="VALIDATED",
        failure_code=None,
        evidence_refs=tuple(suite.suite_identity for suite in plan.suites),
    )
    result_identity = canonical_sha256([result.trial_identity for result in ordered_results])
    completion_observation = EvaluationObservation(
        event_type=f"{STORY_ID}:OfflineEvaluationCompleted",
        artifact_identity=result_identity,
        outcome="OFFLINE_SYNTHETIC_DELTAS_COMPUTED",
        failure_code=None,
        evidence_refs=(plan.plan_identity,),
    )
    return EvaluationReceipt(
        plan_identity=plan.plan_identity,
        benchmark_version=plan.benchmark_version,
        evaluator_version=plan.evaluator_version,
        authority_sha256=plan.authority_sha256,
        approval_authority_identity_sha256=canonical_sha256(
            {
                "actor_id": approval_actor_id,
                "action": Action.EVALUATE_FRESH_CONTEXTS.value,
                "resource_id": plan.plan_identity,
            }
        ),
        provenance_sha256=plan.provenance_sha256,
        layer_evaluations=tuple(layer_evaluations),
        result_identities=tuple(result.trial_identity for result in ordered_results),
        observations=(plan_observation, completion_observation),
    )


def validate_evaluation_receipt(
    *,
    receipt: EvaluationReceipt,
    plan: TrialPlan,
    results: Iterable[TrialResult],
    approval_actor_id: str,
) -> None:
    """Recompile and compare every nested semantic before a receipt is trusted or committed."""

    expected = _build_evaluation_receipt(
        plan=plan, results=tuple(results), approval_actor_id=approval_actor_id
    )
    if canonical_json_bytes(receipt.as_dict()) != canonical_json_bytes(expected.as_dict()):
        raise FreshContextEvaluationError(
            "FORGED_OR_DRIFTED_EVALUATION_RECEIPT",
            "receipt does not exactly reproduce from its governed plan and results",
        )


def evaluate_fresh_contexts(
    *,
    plan: TrialPlan,
    results: Iterable[TrialResult],
    authority: AuthorityService,
    approval_actor_id: str,
    now: datetime,
) -> EvaluationReceipt:
    """Authorize, validate, and deterministically compile one offline structural receipt."""

    validated_plan = _revalidate_plan_graph(plan)
    supplied = tuple(_revalidate_result_graph(result) for result in tuple(results))
    if type(authority) is not AuthorityService:
        raise FreshContextEvaluationError(
            "INVALID_AUTHORITY_SERVICE",
            "the exact deny-by-default AuthorityService implementation is required",
        )
    if not isinstance(now, datetime):
        raise FreshContextEvaluationError("INVALID_AUTHORITY_TIME", "now must be a datetime")
    _require_text(approval_actor_id, "approval_actor_id")
    try:
        authority.authorize_exact(
            actor_id=approval_actor_id,
            action=Action.EVALUATE_FRESH_CONTEXTS,
            resource_id=validated_plan.plan_identity,
            now=now,
        )
    except AuthorityDenied as exc:
        raise FreshContextEvaluationError(
            "EVALUATION_AUTHORITY_DENIED",
            "the approval actor lacks an active exact evaluation grant",
            authority_context=exc.context,
        ) from exc
    receipt = _build_evaluation_receipt(
        plan=validated_plan, results=supplied, approval_actor_id=approval_actor_id
    )
    validate_evaluation_receipt(
        receipt=receipt,
        plan=validated_plan,
        results=supplied,
        approval_actor_id=approval_actor_id,
    )
    return receipt
