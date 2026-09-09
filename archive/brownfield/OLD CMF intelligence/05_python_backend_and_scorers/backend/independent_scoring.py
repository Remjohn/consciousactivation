"""Independent dimension scoring and controlled mutation receipts for ST-08.03.

This is an offline development mechanism.  It preserves dimensions and hard
gates as visible independent facts and never defines production thresholds or
certification status.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import Enum
import hashlib
import json
import re
import weakref
from typing import Any, Iterable


STORY_ID = "ST-08.03"
MINIMUM_REPETITIONS = 3
BASE_DIMENSIONS = (
    "evidence_understanding",
    "visual_and_temporal_understanding",
    "atomicity",
    "product_architecture",
    "skill_system",
    "evaluation_and_repair_quality",
    "implementation_readiness",
    "downstream_performance",
)
NON_COMPENSABLE_GATES = (
    "critical_unsupported_decision",
    "evidence_failure",
    "wrong_atomicity",
    "contract_contradiction",
    "silent_rewrite",
    "untested_required_skill",
    "benchmark_leakage",
    "false_readiness",
    "anti_goal_violation",
)
SUPPORTED_MUTATIONS = (
    "preserve_topic_change_grammar",
    "preserve_grammar_change_topic",
    "remove_one_sequence_invariant",
    "swap_semantic_polarity",
    "inject_irrelevant_style_evidence",
)
SUPPORTED_CASE_ACCESS_CLASSES = ("public", "development")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_PROHIBITED_CLAIMS = frozenset(
    {
        "production_threshold",
        "production_ready",
        "certified",
        "empirical_superiority",
        "protected_benchmark_passed",
    }
)
_CONSTRUCTION_ANCHORS: dict[int, tuple[weakref.ReferenceType[Any], str]] = {}


class IndependentScoringError(ValueError):
    def __init__(self, code: str, message: str, **context: object) -> None:
        super().__init__(message)
        self.code = code
        self.context = dict(context)


class DimensionStatus(str, Enum):
    PASSING = "passing"
    FAILING = "failing"
    NOT_APPLICABLE = "not_applicable"


class GateStatus(str, Enum):
    PASSING = "passing"
    FAILING = "failing"
    NOT_APPLICABLE = "not_applicable"


class DownstreamResultType(str, Enum):
    IMPLEMENTATION_QUESTION = "implementation_question"
    SPECIFICATION_DELTA = "specification_delta"
    TEST_FAILURE = "test_failure"
    LATENCY_AND_COST = "latency_and_cost"
    REPAIR_ROUND = "repair_round"
    FIRST_PASS_ACCEPTANCE = "first_pass_acceptance"
    HUMAN_PREFERENCE_REFERENCE = "human_preference_reference"
    WRONG_READING_OUTCOME = "wrong_reading_outcome"
    CERTIFICATION_RESULT_REFERENCE = "certification_result_reference"


class ScoringAction(str, Enum):
    ISSUE = "issue_independent_scoring"
    INVALIDATE = "invalidate_independent_scoring"
    ROLLBACK = "rollback_independent_scoring"


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


def _payload(instance: Any) -> dict[str, Any]:
    builder = getattr(instance, "_construction_payload", None)
    return builder() if builder is not None else instance.as_dict()


def _seal(instance: Any) -> None:
    key = id(instance)

    def cleanup(reference: weakref.ReferenceType[Any], *, identity: int = key) -> None:
        current = _CONSTRUCTION_ANCHORS.get(identity)
        if current is not None and current[0] is reference:
            _CONSTRUCTION_ANCHORS.pop(identity, None)

    reference = weakref.ref(instance, cleanup)
    _CONSTRUCTION_ANCHORS[key] = (reference, canonical_sha256(_payload(instance)))


def _require_unmutated(instance: Any, field: str) -> None:
    anchor = _CONSTRUCTION_ANCHORS.get(id(instance))
    if anchor is None or anchor[0]() is not instance:
        raise IndependentScoringError(
            "UNANCHORED_GOVERNED_OBJECT",
            f"{field} lacks its construction anchor",
            field=field,
        )
    try:
        current = canonical_sha256(_payload(instance))
    except (AttributeError, TypeError, ValueError) as exc:
        raise IndependentScoringError(
            "MUTATED_GOVERNED_OBJECT",
            f"{field} cannot be serialized canonically",
            field=field,
        ) from exc
    if current != anchor[1]:
        raise IndependentScoringError(
            "MUTATED_GOVERNED_OBJECT",
            f"{field} changed after construction",
            field=field,
        )


def _safe_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return {item.name: _safe_value(getattr(value, item.name, None)) for item in fields(value) if item.init}
    if isinstance(value, dict):
        return {str(key): _safe_value(item) for key, item in sorted(value.items())}
    if isinstance(value, (tuple, list)):
        return [_safe_value(item) for item in value]
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    return {"unsupported_type": type(value).__qualname__}


def _require_text(value: str, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise IndependentScoringError("MISSING_GOVERNED_FIELD", f"{field} is required", field=field)
    normalized = re.sub(r"[^a-z0-9]+", "_", value.casefold()).strip("_")
    padded = f"_{normalized}_"
    matched = [token for token in _PROHIBITED_CLAIMS if f"_{token}_" in padded]
    if matched:
        raise IndependentScoringError(
            "PROHIBITED_PRODUCTION_OR_CERTIFICATION_CLAIM",
            f"{field} contains a prohibited claim",
            field=field,
            matched=tuple(sorted(matched)),
        )


def _require_sha256(value: str, field: str) -> None:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise IndependentScoringError(
            "INVALID_IMMUTABLE_IDENTITY",
            f"{field} must be a lowercase SHA-256 digest",
            field=field,
        )


def _require_bool(value: object, field: str) -> None:
    if type(value) is not bool:
        raise IndependentScoringError("INVALID_GOVERNED_TYPE", f"{field} must be boolean", field=field)


def _require_enum(value: object, enum_type: type[Enum], field: str) -> None:
    if not isinstance(value, enum_type):
        raise IndependentScoringError(
            "INVALID_GOVERNED_TYPE",
            f"{field} must be {enum_type.__name__}",
            field=field,
        )


@dataclass(frozen=True, slots=True, weakref_slot=True)
class ScoringAuthority:
    authority_id: str
    authority_version: str
    authority_sha256: str
    permitted_actions: tuple[ScoringAction, ...]
    story_id: str = STORY_ID

    def __post_init__(self) -> None:
        _require_text(self.authority_id, "authority_id")
        _require_text(self.authority_version, "authority_version")
        _require_sha256(self.authority_sha256, "authority_sha256")
        if self.story_id != STORY_ID:
            raise IndependentScoringError("AUTHORITY_SCOPE_MISMATCH", "authority is not scoped to ST-08.03")
        if not isinstance(self.permitted_actions, tuple) or not self.permitted_actions:
            raise IndependentScoringError("MISSING_AUTHORITY_GRANTS", "authority grants are required")
        if len(set(self.permitted_actions)) != len(self.permitted_actions):
            raise IndependentScoringError("DUPLICATE_AUTHORITY_GRANT", "authority grants must be unique")
        for action in self.permitted_actions:
            _require_enum(action, ScoringAction, "permitted_action")
        _seal(self)

    @property
    def authority_identity(self) -> str:
        _require_unmutated(self, "scoring_authority")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "authority_id": self.authority_id,
            "authority_version": self.authority_version,
            "authority_sha256": self.authority_sha256,
            "permitted_actions": [action.value for action in self.permitted_actions],
            "story_id": self.story_id,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "scoring_authority")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class ScoringCommand:
    command_id: str
    action: ScoringAction
    resource_id: str
    payload_sha256: str
    expected_authority_identity: str

    def __post_init__(self) -> None:
        _require_text(self.command_id, "command_id")
        _require_enum(self.action, ScoringAction, "action")
        _require_sha256(self.resource_id, "resource_id")
        _require_sha256(self.payload_sha256, "payload_sha256")
        _require_sha256(self.expected_authority_identity, "expected_authority_identity")
        _seal(self)

    @property
    def command_identity(self) -> str:
        _require_unmutated(self, "scoring_command")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "command_id": self.command_id,
            "action": self.action.value,
            "resource_id": self.resource_id,
            "payload_sha256": self.payload_sha256,
            "expected_authority_identity": self.expected_authority_identity,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "scoring_command")
        return self._construction_payload()


def _require_authorized(
    command: ScoringCommand,
    authority: ScoringAuthority,
    action: ScoringAction,
    *,
    resource_id: str,
) -> None:
    if not isinstance(command, ScoringCommand) or not isinstance(authority, ScoringAuthority):
        raise IndependentScoringError("INVALID_AUTHORITY_EVIDENCE", "typed command and authority are required")
    _require_unmutated(command, "scoring_command")
    _require_unmutated(authority, "scoring_authority")
    if command.action is not action:
        raise IndependentScoringError("COMMAND_ACTION_MISMATCH", "command action is not authorized for this operation")
    if action not in authority.permitted_actions:
        raise IndependentScoringError("UNAUTHORIZED_SCORING_ACTION", "authority does not grant this action")
    if command.expected_authority_identity != authority.authority_identity:
        raise IndependentScoringError("AUTHORITY_IDENTITY_MISMATCH", "command authority binding does not match")
    if command.resource_id != resource_id:
        raise IndependentScoringError("COMMAND_RESOURCE_MISMATCH", "command targets a different governed resource")


@dataclass(frozen=True, slots=True, weakref_slot=True)
class DevelopmentRubric:
    rubric_id: str
    rubric_version: str
    scoring_policy_version: str
    evaluator_contract_version: str
    threshold_policy_reference: str
    dimensions: tuple[str, ...] = BASE_DIMENSIONS
    hard_gates: tuple[str, ...] = NON_COMPENSABLE_GATES
    scoring_policy_sha256: str = ""
    threshold_policy_reference_sha256: str = ""

    def __post_init__(self) -> None:
        _require_text(self.rubric_id, "rubric_id")
        _require_text(self.rubric_version, "rubric_version")
        _require_text(self.scoring_policy_version, "scoring_policy_version")
        _require_text(self.evaluator_contract_version, "evaluator_contract_version")
        _require_text(self.threshold_policy_reference, "threshold_policy_reference")
        if self.dimensions != BASE_DIMENSIONS:
            raise IndependentScoringError(
                "RUBRIC_DIMENSION_DRIFT",
                "all eight base dimensions must remain visible and ordered",
            )
        if self.hard_gates != NON_COMPENSABLE_GATES:
            raise IndependentScoringError(
                "RUBRIC_GATE_DRIFT",
                "all nine non-compensable gates must remain visible and ordered",
            )
        _require_sha256(self.scoring_policy_sha256, "scoring_policy_sha256")
        _require_sha256(self.threshold_policy_reference_sha256, "threshold_policy_reference_sha256")
        _seal(self)

    @property
    def rubric_identity(self) -> str:
        _require_unmutated(self, "development_rubric")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "rubric_id": self.rubric_id,
            "rubric_version": self.rubric_version,
            "scoring_policy_version": self.scoring_policy_version,
            "evaluator_contract_version": self.evaluator_contract_version,
            "threshold_policy_reference": self.threshold_policy_reference,
            "dimensions": list(self.dimensions),
            "hard_gates": list(self.hard_gates),
            "scoring_policy_sha256": self.scoring_policy_sha256,
            "threshold_policy_reference_sha256": self.threshold_policy_reference_sha256,
            "production_threshold_defined": False,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "development_rubric")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class DimensionScorecard:
    dimension: str
    status: DimensionStatus
    score_basis_points: int | None
    evidence_refs: tuple[str, ...]
    failure_context: str | None = None
    not_applicable_justification: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.dimension, "dimension")
        if self.dimension not in BASE_DIMENSIONS:
            raise IndependentScoringError("UNKNOWN_DIMENSION", "dimension is not in the governed base rubric")
        _require_enum(self.status, DimensionStatus, "status")
        if not isinstance(self.evidence_refs, tuple) or not self.evidence_refs:
            raise IndependentScoringError("MISSING_EVIDENCE_REFS", "dimension evidence is required")
        for digest in self.evidence_refs:
            _require_sha256(digest, "evidence_ref")
        if self.status is DimensionStatus.NOT_APPLICABLE:
            _require_text(self.not_applicable_justification or "", "not_applicable_justification")
            if self.score_basis_points is not None:
                raise IndependentScoringError(
                    "NOT_APPLICABLE_SCORE_PRESENT",
                    "NOT_APPLICABLE dimensions cannot carry a score",
                )
            if self.failure_context is not None:
                raise IndependentScoringError(
                    "NOT_APPLICABLE_FAILURE_CONTEXT_PRESENT",
                    "NOT_APPLICABLE dimensions cannot carry failure context",
                )
        else:
            if self.not_applicable_justification is not None:
                raise IndependentScoringError(
                    "UNSUPPORTED_NOT_APPLICABLE_JUSTIFICATION",
                    "applicable dimensions cannot carry NOT_APPLICABLE justification",
                )
            if isinstance(self.score_basis_points, bool) or not isinstance(self.score_basis_points, int):
                raise IndependentScoringError("INVALID_DIMENSION_SCORE", "score must be an integer")
            if not 0 <= self.score_basis_points <= 10_000:
                raise IndependentScoringError("INVALID_DIMENSION_SCORE", "score is out of range")
            if self.status is DimensionStatus.FAILING:
                _require_text(self.failure_context or "", "failure_context")
        _seal(self)

    @property
    def scorecard_identity(self) -> str:
        _require_unmutated(self, "dimension_scorecard")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "dimension": self.dimension,
            "status": self.status.value,
            "score_basis_points": self.score_basis_points,
            "evidence_refs": list(self.evidence_refs),
            "failure_context": self.failure_context,
            "not_applicable_justification": self.not_applicable_justification,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "dimension_scorecard")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class ControlledMutation:
    mutation_id: str
    mutation_type: str
    base_case_sha256: str
    mutated_input_sha256: str
    changed_variables: tuple[str, ...]
    preserved_invariants: tuple[str, ...]
    expected_decision_sha256: str
    source_lineage_sha256: str

    def __post_init__(self) -> None:
        _require_text(self.mutation_id, "mutation_id")
        _require_text(self.mutation_type, "mutation_type")
        if self.mutation_type not in SUPPORTED_MUTATIONS:
            raise IndependentScoringError("UNSUPPORTED_MUTATION", "mutation type is not governed")
        for field in ("base_case_sha256", "mutated_input_sha256", "expected_decision_sha256", "source_lineage_sha256"):
            _require_sha256(getattr(self, field), field)
        if self.base_case_sha256 == self.mutated_input_sha256:
            raise IndependentScoringError("MISSING_ACTUAL_MUTATION", "mutation must change input identity")
        if not isinstance(self.changed_variables, tuple) or len(self.changed_variables) != 1:
            raise IndependentScoringError(
                "UNCONTROLLED_MUTATION",
                "controlled mutation must declare exactly one changed variable",
            )
        _require_text(self.changed_variables[0], "changed_variable")
        if not isinstance(self.preserved_invariants, tuple) or not self.preserved_invariants:
            raise IndependentScoringError("MISSING_MUTATION_INVARIANTS", "preserved invariants are required")
        for invariant in self.preserved_invariants:
            _require_text(invariant, "preserved_invariant")
        _seal(self)

    @property
    def mutation_identity(self) -> str:
        _require_unmutated(self, "controlled_mutation")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "mutation_id": self.mutation_id,
            "mutation_type": self.mutation_type,
            "base_case_sha256": self.base_case_sha256,
            "mutated_input_sha256": self.mutated_input_sha256,
            "changed_variables": list(self.changed_variables),
            "preserved_invariants": list(self.preserved_invariants),
            "expected_decision_sha256": self.expected_decision_sha256,
            "source_lineage_sha256": self.source_lineage_sha256,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "controlled_mutation")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class GateResult:
    gate_id: str
    status: GateStatus
    evidence_refs: tuple[str, ...]
    failure_context: str | None = None
    not_applicable_justification: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.gate_id, "gate_id")
        if self.gate_id not in NON_COMPENSABLE_GATES:
            raise IndependentScoringError("UNKNOWN_NON_COMPENSABLE_GATE", "gate is not governed")
        _require_enum(self.status, GateStatus, "status")
        if not isinstance(self.evidence_refs, tuple) or not self.evidence_refs:
            raise IndependentScoringError("MISSING_EVIDENCE_REFS", "gate evidence is required")
        for digest in self.evidence_refs:
            _require_sha256(digest, "evidence_ref")
        if self.status is GateStatus.FAILING:
            _require_text(self.failure_context or "", "failure_context")
        elif self.failure_context is not None:
            raise IndependentScoringError("UNEXPECTED_GATE_FAILURE_CONTEXT", "non-failing gate has failure context")
        if self.status is GateStatus.NOT_APPLICABLE:
            _require_text(self.not_applicable_justification or "", "not_applicable_justification")
        elif self.not_applicable_justification is not None:
            raise IndependentScoringError(
                "UNEXPECTED_GATE_NOT_APPLICABLE_JUSTIFICATION",
                "applicable gate has NOT_APPLICABLE justification",
            )
        _seal(self)

    @property
    def gate_identity(self) -> str:
        _require_unmutated(self, "gate_result")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "status": self.status.value,
            "evidence_refs": list(self.evidence_refs),
            "failure_context": self.failure_context,
            "not_applicable_justification": self.not_applicable_justification,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "gate_result")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class DimensionDistribution:
    dimension: str
    scores_basis_points: tuple[int, ...]

    def __post_init__(self) -> None:
        _require_text(self.dimension, "dimension")
        if self.dimension not in BASE_DIMENSIONS:
            raise IndependentScoringError("UNKNOWN_DIMENSION", "dimension is not in the base rubric")
        if not isinstance(self.scores_basis_points, tuple) or not self.scores_basis_points:
            raise IndependentScoringError("MISSING_DISTRIBUTION", "scores are required")
        for score in self.scores_basis_points:
            if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 10_000:
                raise IndependentScoringError("INVALID_DIMENSION_SCORE", "distribution score is invalid")
        _seal(self)

    @property
    def distribution_identity(self) -> str:
        _require_unmutated(self, "dimension_distribution")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {"dimension": self.dimension, "scores_basis_points": list(self.scores_basis_points)}

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "dimension_distribution")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class RepeatedRunSummary:
    repetition_identities: tuple[str, ...]
    distributions: tuple[DimensionDistribution, ...]
    dominant_failure_patterns: tuple[str, ...]
    missing_repetition_ids: tuple[str, ...] = ()
    rejected_repetition_identities: tuple[str, ...] = ()
    production_variance_threshold_defined: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.repetition_identities, tuple) or len(self.repetition_identities) < MINIMUM_REPETITIONS:
            raise IndependentScoringError(
                "INCOMPLETE_REPETITIONS",
                f"at least {MINIMUM_REPETITIONS} repetition identities are required",
            )
        for digest in self.repetition_identities:
            _require_sha256(digest, "repetition_identity")
        if len(set(self.repetition_identities)) != len(self.repetition_identities):
            raise IndependentScoringError("DUPLICATE_REPETITION_IDENTITY", "repetition identities must be unique")
        if not isinstance(self.distributions, tuple):
            raise IndependentScoringError("INVALID_GOVERNED_TYPE", "distributions must be a tuple")
        dimensions = tuple(item.dimension for item in self.distributions)
        if dimensions != BASE_DIMENSIONS:
            raise IndependentScoringError("INCOMPLETE_DISTRIBUTION_DIMENSIONS", "all dimensions need distributions")
        for item in self.distributions:
            _require_unmutated(item, "dimension_distribution")
            if len(item.scores_basis_points) != len(self.repetition_identities):
                raise IndependentScoringError(
                    "DISTRIBUTION_REPETITION_MISMATCH",
                    "each dimension distribution must cover every repetition",
                )
        if not isinstance(self.dominant_failure_patterns, tuple):
            raise IndependentScoringError("INVALID_GOVERNED_TYPE", "dominant failures must be a tuple")
        for pattern in self.dominant_failure_patterns:
            _require_text(pattern, "dominant_failure_pattern")
        if not isinstance(self.missing_repetition_ids, tuple):
            raise IndependentScoringError("INVALID_GOVERNED_TYPE", "missing repetitions must be a tuple")
        for repetition_id in self.missing_repetition_ids:
            _require_text(repetition_id, "missing_repetition_id")
        if not isinstance(self.rejected_repetition_identities, tuple):
            raise IndependentScoringError("INVALID_GOVERNED_TYPE", "rejected repetitions must be a tuple")
        for digest in self.rejected_repetition_identities:
            _require_sha256(digest, "rejected_repetition_identity")
        _require_bool(self.production_variance_threshold_defined, "production_variance_threshold_defined")
        if self.production_variance_threshold_defined:
            raise IndependentScoringError(
                "PRODUCTION_THRESHOLD_PROHIBITED",
                "OD-AM-001 cannot define production variance thresholds",
            )
        _seal(self)

    @property
    def summary_identity(self) -> str:
        _require_unmutated(self, "repeated_run_summary")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "repetition_identities": list(self.repetition_identities),
            "distributions": [item.as_dict() for item in self.distributions],
            "dominant_failure_patterns": list(self.dominant_failure_patterns),
            "missing_repetition_ids": list(self.missing_repetition_ids),
            "rejected_repetition_identities": list(self.rejected_repetition_identities),
            "production_variance_threshold_defined": False,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "repeated_run_summary")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class DownstreamResult:
    result_type: DownstreamResultType
    builder_version: str
    evaluated_artifact_sha256: str
    origin_receipt_sha256: str
    authority_sha256: str
    payload_sha256: str

    def __post_init__(self) -> None:
        _require_enum(self.result_type, DownstreamResultType, "result_type")
        _require_text(self.builder_version, "builder_version")
        for field in ("evaluated_artifact_sha256", "origin_receipt_sha256", "authority_sha256", "payload_sha256"):
            _require_sha256(getattr(self, field), field)
        _seal(self)

    @property
    def result_identity(self) -> str:
        _require_unmutated(self, "downstream_result")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "result_type": self.result_type.value,
            "builder_version": self.builder_version,
            "evaluated_artifact_sha256": self.evaluated_artifact_sha256,
            "origin_receipt_sha256": self.origin_receipt_sha256,
            "authority_sha256": self.authority_sha256,
            "payload_sha256": self.payload_sha256,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "downstream_result")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class IndependentScoringReceipt:
    rubric: DevelopmentRubric
    evaluated_artifact_sha256: str
    builder_version: str
    target_category: str
    target_profile: str
    source_ir_sha256: str
    predecessor_maturity_receipt_sha256: str
    benchmark_portfolio_sha256: str
    case_identity_sha256: str
    case_access_class: str
    run_id: str
    provenance_sha256: str
    command_identity: str
    authority_identity: str
    scorecards: tuple[DimensionScorecard, ...]
    mutations: tuple[ControlledMutation, ...]
    gates: tuple[GateResult, ...]
    stability_summary: RepeatedRunSummary
    downstream_results: tuple[DownstreamResult, ...]
    observations: tuple[str, ...]
    protected_label_accessed: bool = False
    composite_trend_basis_points: int | None = None
    evidence_gate_closed: bool = False
    production_threshold_defined: bool = False
    production_ready: bool = False
    certified: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.rubric, DevelopmentRubric):
            raise IndependentScoringError("INVALID_GOVERNED_TYPE", "rubric is required")
        _require_unmutated(self.rubric, "development_rubric")
        _require_text(self.builder_version, "builder_version")
        _require_text(self.target_category, "target_category")
        _require_text(self.target_profile, "target_profile")
        _require_text(self.run_id, "run_id")
        if self.case_access_class not in SUPPORTED_CASE_ACCESS_CLASSES:
            raise IndependentScoringError(
                "PROTECTED_OR_UNKNOWN_CASE_ACCESS",
                "offline scoring accepts only public or development case metadata",
            )
        for field in (
            "evaluated_artifact_sha256",
            "source_ir_sha256",
            "predecessor_maturity_receipt_sha256",
            "benchmark_portfolio_sha256",
            "case_identity_sha256",
            "provenance_sha256",
            "command_identity",
            "authority_identity",
        ):
            _require_sha256(getattr(self, field), field)
        if not isinstance(self.scorecards, tuple):
            raise IndependentScoringError("INVALID_GOVERNED_TYPE", "scorecards must be a tuple")
        if tuple(score.dimension for score in self.scorecards) != BASE_DIMENSIONS:
            raise IndependentScoringError("INCOMPLETE_DIMENSION_COVERAGE", "all dimensions must be present")
        for score in self.scorecards:
            _require_unmutated(score, "dimension_scorecard")
        scorecard_identities = tuple(score.scorecard_identity for score in self.scorecards)
        if len(set(scorecard_identities)) != len(scorecard_identities):
            raise IndependentScoringError("DUPLICATE_SCORECARD_IDENTITY", "scorecards must be distinct")
        if not isinstance(self.mutations, tuple) or not self.mutations:
            raise IndependentScoringError("MISSING_CONTROLLED_MUTATIONS", "mutations are required")
        for mutation in self.mutations:
            _require_unmutated(mutation, "controlled_mutation")
        mutation_identities = tuple(mutation.mutation_identity for mutation in self.mutations)
        if len(set(mutation_identities)) != len(mutation_identities):
            raise IndependentScoringError("DUPLICATE_MUTATION_IDENTITY", "mutations must be distinct")
        if not isinstance(self.gates, tuple):
            raise IndependentScoringError("INVALID_GOVERNED_TYPE", "gates must be a tuple")
        if tuple(gate.gate_id for gate in self.gates) != NON_COMPENSABLE_GATES:
            raise IndependentScoringError("INCOMPLETE_NON_COMPENSABLE_GATES", "all hard gates must be present")
        for gate in self.gates:
            _require_unmutated(gate, "gate_result")
        if any(gate.status is GateStatus.FAILING for gate in self.gates):
            raise IndependentScoringError(
                "NON_COMPENSABLE_GATE_FAILED",
                "gate failure cannot be overridden by score or stability summary",
                failed=tuple(gate.gate_id for gate in self.gates if gate.status is GateStatus.FAILING),
            )
        if not isinstance(self.stability_summary, RepeatedRunSummary):
            raise IndependentScoringError("INVALID_GOVERNED_TYPE", "stability summary is required")
        _require_unmutated(self.stability_summary, "repeated_run_summary")
        if self.stability_summary.missing_repetition_ids or self.stability_summary.rejected_repetition_identities:
            raise IndependentScoringError(
                "INCOMPLETE_OR_REJECTED_REPETITIONS",
                "incomplete repetitions cannot issue a conclusive scoring receipt",
            )
        if not isinstance(self.downstream_results, tuple):
            raise IndependentScoringError("INVALID_GOVERNED_TYPE", "downstream_results must be a tuple")
        for result in self.downstream_results:
            _require_unmutated(result, "downstream_result")
            if result.evaluated_artifact_sha256 != self.evaluated_artifact_sha256:
                raise IndependentScoringError("DOWNSTREAM_ARTIFACT_MISMATCH", "downstream result artifact differs")
            if result.origin_receipt_sha256 != self.predecessor_maturity_receipt_sha256:
                raise IndependentScoringError("DOWNSTREAM_ORIGIN_MISMATCH", "downstream result origin differs")
            if result.builder_version != self.builder_version:
                raise IndependentScoringError("DOWNSTREAM_BUILDER_VERSION_MISMATCH", "downstream result version differs")
        if not isinstance(self.observations, tuple) or not self.observations:
            raise IndependentScoringError("MISSING_OBSERVATIONS", "attributable observations are required")
        for observation in self.observations:
            if not isinstance(observation, str) or not observation.startswith(f"{STORY_ID}:"):
                raise IndependentScoringError("INVALID_OBSERVATION", "observations must be Story-scoped")
        _require_bool(self.protected_label_accessed, "protected_label_accessed")
        if self.protected_label_accessed:
            raise IndependentScoringError("PROTECTED_LABEL_ACCESS_PROHIBITED", "protected labels are outside OD-AM-001")
        if self.composite_trend_basis_points is not None:
            if isinstance(self.composite_trend_basis_points, bool) or not isinstance(
                self.composite_trend_basis_points, int
            ):
                raise IndependentScoringError("INVALID_COMPOSITE_TREND", "trend must be integer")
            if not 0 <= self.composite_trend_basis_points <= 10_000:
                raise IndependentScoringError("INVALID_COMPOSITE_TREND", "trend out of range")
        for field in (
            "evidence_gate_closed",
            "production_threshold_defined",
            "production_ready",
            "certified",
        ):
            _require_bool(getattr(self, field), field)
            if getattr(self, field):
                raise IndependentScoringError(
                    "PROHIBITED_PRODUCTION_OR_CERTIFICATION_CLAIM",
                    f"{field} must remain false",
                    field=field,
                )
        _seal(self)

    @property
    def receipt_identity(self) -> str:
        _require_unmutated(self, "independent_scoring_receipt")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "story_id": STORY_ID,
            "rubric": self.rubric.as_dict(),
            "evaluated_artifact_sha256": self.evaluated_artifact_sha256,
            "builder_version": self.builder_version,
            "target_category": self.target_category,
            "target_profile": self.target_profile,
            "source_ir_sha256": self.source_ir_sha256,
            "predecessor_maturity_receipt_sha256": self.predecessor_maturity_receipt_sha256,
            "benchmark_portfolio_sha256": self.benchmark_portfolio_sha256,
            "case_identity_sha256": self.case_identity_sha256,
            "case_access_class": self.case_access_class,
            "run_id": self.run_id,
            "provenance_sha256": self.provenance_sha256,
            "command_identity": self.command_identity,
            "authority_identity": self.authority_identity,
            "scorecards": [score.as_dict() for score in self.scorecards],
            "mutations": [mutation.as_dict() for mutation in self.mutations],
            "gates": [gate.as_dict() for gate in self.gates],
            "stability_summary": self.stability_summary.as_dict(),
            "downstream_results": [result.as_dict() for result in self.downstream_results],
            "observations": list(self.observations),
            "protected_label_accessed": False,
            "composite_trend_basis_points": self.composite_trend_basis_points,
            "composite_trend_authoritative": False,
            "evidence_gate_closed": False,
            "production_threshold_defined": False,
            "production_ready": False,
            "certified": False,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "independent_scoring_receipt")
        return self._construction_payload()


@dataclass(frozen=True, slots=True, weakref_slot=True)
class ScoringTransitionReceipt:
    prior_receipt_sha256: str
    command_identity: str
    authority_identity: str
    action: ScoringAction
    changed_identities: tuple[str, ...]
    rollback_target_sha256: str | None = None
    production_ready: bool = False
    certified: bool = False

    def __post_init__(self) -> None:
        _require_sha256(self.prior_receipt_sha256, "prior_receipt_sha256")
        _require_sha256(self.command_identity, "command_identity")
        _require_sha256(self.authority_identity, "authority_identity")
        _require_enum(self.action, ScoringAction, "action")
        if not isinstance(self.changed_identities, tuple):
            raise IndependentScoringError("INVALID_GOVERNED_TYPE", "changed identities must be a tuple")
        for digest in self.changed_identities:
            _require_sha256(digest, "changed_identity")
        if self.rollback_target_sha256 is not None:
            _require_sha256(self.rollback_target_sha256, "rollback_target_sha256")
        for field in ("production_ready", "certified"):
            _require_bool(getattr(self, field), field)
            if getattr(self, field):
                raise IndependentScoringError("PROHIBITED_PRODUCTION_OR_CERTIFICATION_CLAIM", field)
        _seal(self)

    @property
    def transition_identity(self) -> str:
        _require_unmutated(self, "scoring_transition_receipt")
        return canonical_sha256(self._construction_payload())

    def _construction_payload(self) -> dict[str, Any]:
        return {
            "story_id": STORY_ID,
            "prior_receipt_sha256": self.prior_receipt_sha256,
            "command_identity": self.command_identity,
            "authority_identity": self.authority_identity,
            "action": self.action.value,
            "changed_identities": list(self.changed_identities),
            "rollback_target_sha256": self.rollback_target_sha256,
            "observation": f"{STORY_ID}:ScoringReceiptTransitioned",
            "production_ready": False,
            "certified": False,
        }

    def as_dict(self) -> dict[str, Any]:
        _require_unmutated(self, "scoring_transition_receipt")
        return self._construction_payload()


def _issue_payload(
    *,
    rubric: DevelopmentRubric,
    evaluated_artifact_sha256: str,
    builder_version: str,
    target_category: str,
    target_profile: str,
    source_ir_sha256: str,
    predecessor_maturity_receipt_sha256: str,
    benchmark_portfolio_sha256: str,
    case_identity_sha256: str,
    case_access_class: str,
    run_id: str,
    provenance_sha256: str,
    scorecards: tuple[DimensionScorecard, ...],
    mutations: tuple[ControlledMutation, ...],
    gates: tuple[GateResult, ...],
    stability_summary: RepeatedRunSummary,
    downstream_results: tuple[DownstreamResult, ...],
    observations: tuple[str, ...],
    protected_label_accessed: bool,
    composite_trend_basis_points: int | None,
) -> dict[str, Any]:
    return {
        "rubric_identity": rubric.rubric_identity,
        "evaluated_artifact_sha256": evaluated_artifact_sha256,
        "builder_version": builder_version,
        "target_category": target_category,
        "target_profile": target_profile,
        "source_ir_sha256": source_ir_sha256,
        "predecessor_maturity_receipt_sha256": predecessor_maturity_receipt_sha256,
        "benchmark_portfolio_sha256": benchmark_portfolio_sha256,
        "case_identity_sha256": case_identity_sha256,
        "case_access_class": case_access_class,
        "run_id": run_id,
        "provenance_sha256": provenance_sha256,
        "scorecard_identities": [item.scorecard_identity for item in scorecards],
        "mutation_identities": [item.mutation_identity for item in mutations],
        "gate_identities": [item.gate_identity for item in gates],
        "stability_summary_identity": stability_summary.summary_identity,
        "downstream_result_identities": [item.result_identity for item in downstream_results],
        "observations": list(observations),
        "protected_label_accessed": protected_label_accessed,
        "composite_trend_basis_points": composite_trend_basis_points,
    }


def compute_issue_payload_sha256(**kwargs: Any) -> str:
    """Return the canonical payload binding required by an ISSUE command."""

    return canonical_sha256(_issue_payload(**kwargs))


def issue_independent_scoring_receipt(
    *,
    rubric: DevelopmentRubric,
    evaluated_artifact_sha256: str,
    builder_version: str,
    target_category: str,
    target_profile: str,
    source_ir_sha256: str,
    predecessor_maturity_receipt_sha256: str,
    benchmark_portfolio_sha256: str,
    case_identity_sha256: str,
    case_access_class: str,
    run_id: str,
    provenance_sha256: str,
    scorecards: tuple[DimensionScorecard, ...],
    mutations: tuple[ControlledMutation, ...],
    gates: tuple[GateResult, ...],
    stability_summary: RepeatedRunSummary,
    downstream_results: tuple[DownstreamResult, ...],
    observations: tuple[str, ...],
    command: ScoringCommand,
    authority: ScoringAuthority,
    protected_label_accessed: bool = False,
    composite_trend_basis_points: int | None = None,
) -> IndependentScoringReceipt:
    """Issue one immutable scoring receipt through the exact authority seam."""

    _require_authorized(
        command,
        authority,
        ScoringAction.ISSUE,
        resource_id=evaluated_artifact_sha256,
    )
    payload_arguments = {
        "rubric": rubric,
        "evaluated_artifact_sha256": evaluated_artifact_sha256,
        "builder_version": builder_version,
        "target_category": target_category,
        "target_profile": target_profile,
        "source_ir_sha256": source_ir_sha256,
        "predecessor_maturity_receipt_sha256": predecessor_maturity_receipt_sha256,
        "benchmark_portfolio_sha256": benchmark_portfolio_sha256,
        "case_identity_sha256": case_identity_sha256,
        "case_access_class": case_access_class,
        "run_id": run_id,
        "provenance_sha256": provenance_sha256,
        "scorecards": scorecards,
        "mutations": mutations,
        "gates": gates,
        "stability_summary": stability_summary,
        "downstream_results": downstream_results,
        "observations": observations,
        "protected_label_accessed": protected_label_accessed,
        "composite_trend_basis_points": composite_trend_basis_points,
    }
    expected_payload = compute_issue_payload_sha256(**payload_arguments)
    if command.payload_sha256 != expected_payload:
        raise IndependentScoringError("COMMAND_PAYLOAD_MISMATCH", "command payload is not the governed scoring input")
    return IndependentScoringReceipt(
        **payload_arguments,
        command_identity=command.command_identity,
        authority_identity=authority.authority_identity,
    )


def validate_repeat_receipt(existing: IndependentScoringReceipt, candidate: IndependentScoringReceipt) -> IndependentScoringReceipt:
    _require_unmutated(existing, "existing_scoring_receipt")
    _require_unmutated(candidate, "candidate_scoring_receipt")
    if existing.receipt_identity != candidate.receipt_identity:
        raise IndependentScoringError("CONFLICTING_REPEAT_COMMAND", "candidate receipt differs")
    return existing


def invalidate_scoring_receipt(
    receipt: IndependentScoringReceipt,
    changed_identities: Iterable[str],
    *,
    command: ScoringCommand,
    authority: ScoringAuthority,
) -> ScoringTransitionReceipt:
    _require_unmutated(receipt, "independent_scoring_receipt")
    changed = tuple(sorted(changed_identities))
    if not changed:
        raise IndependentScoringError("MISSING_INVALIDATION_INPUT", "changed identities are required")
    for digest in changed:
        _require_sha256(digest, "changed_identity")
    governed_lineage = {
        receipt.rubric.rubric_identity,
        receipt.evaluated_artifact_sha256,
        receipt.source_ir_sha256,
        receipt.predecessor_maturity_receipt_sha256,
        receipt.benchmark_portfolio_sha256,
        receipt.case_identity_sha256,
        receipt.provenance_sha256,
        *(item.mutation_identity for item in receipt.mutations),
        *(item.result_identity for item in receipt.downstream_results),
    }
    unrelated = tuple(digest for digest in changed if digest not in governed_lineage)
    if unrelated:
        raise IndependentScoringError(
            "UNRELATED_INVALIDATION_INPUT",
            "invalidation contains identities outside the receipt lineage",
            identities=unrelated,
        )
    _require_authorized(
        command,
        authority,
        ScoringAction.INVALIDATE,
        resource_id=receipt.receipt_identity,
    )
    if command.payload_sha256 != canonical_sha256({"changed_identities": list(changed)}):
        raise IndependentScoringError("COMMAND_PAYLOAD_MISMATCH", "invalidation payload differs")
    return ScoringTransitionReceipt(
        prior_receipt_sha256=receipt.receipt_identity,
        command_identity=command.command_identity,
        authority_identity=authority.authority_identity,
        action=ScoringAction.INVALIDATE,
        changed_identities=changed,
    )


def rollback_scoring_receipt(
    receipt: IndependentScoringReceipt,
    rollback_target_sha256: str,
    *,
    command: ScoringCommand,
    authority: ScoringAuthority,
) -> ScoringTransitionReceipt:
    _require_unmutated(receipt, "independent_scoring_receipt")
    _require_sha256(rollback_target_sha256, "rollback_target_sha256")
    _require_authorized(
        command,
        authority,
        ScoringAction.ROLLBACK,
        resource_id=receipt.receipt_identity,
    )
    if command.payload_sha256 != canonical_sha256({"rollback_target_sha256": rollback_target_sha256}):
        raise IndependentScoringError("COMMAND_PAYLOAD_MISMATCH", "rollback payload differs")
    return ScoringTransitionReceipt(
        prior_receipt_sha256=receipt.receipt_identity,
        command_identity=command.command_identity,
        authority_identity=authority.authority_identity,
        action=ScoringAction.ROLLBACK,
        changed_identities=(),
        rollback_target_sha256=rollback_target_sha256,
    )


def build_rejection_receipt(
    error: IndependentScoringError,
    *,
    rejected_input: Any,
    command: ScoringCommand | None = None,
    authority: ScoringAuthority | None = None,
    run_id: str | None = None,
    provenance_sha256: str | None = None,
) -> dict[str, Any]:
    if command is not None:
        _require_unmutated(command, "scoring_command")
    if authority is not None:
        _require_unmutated(authority, "scoring_authority")
    if run_id is not None:
        _require_text(run_id, "run_id")
    if provenance_sha256 is not None:
        _require_sha256(provenance_sha256, "provenance_sha256")
    rejection_payload = {
        "code": error.code,
        "context": _safe_value(error.context),
        "input": _safe_value(rejected_input),
        "command_identity": command.command_identity if command is not None else None,
        "authority_identity": authority.authority_identity if authority is not None else None,
        "run_id": run_id,
        "provenance_sha256": provenance_sha256,
    }
    return {
        "story_id": STORY_ID,
        "outcome": "REJECTED_NO_SCORING_RECEIPT",
        "failure_code": error.code,
        "failure_context": _safe_value(error.context),
        "command_identity": command.command_identity if command is not None else None,
        "authority_identity": authority.authority_identity if authority is not None else None,
        "run_id": run_id,
        "provenance_sha256": provenance_sha256,
        "rejected_input_identity": canonical_sha256(_safe_value(rejected_input)),
        "rejection_identity": canonical_sha256(rejection_payload),
        "observation": f"{STORY_ID}:OutcomeRejected",
        "production_threshold_defined": False,
        "production_ready": False,
        "certified": False,
    }
