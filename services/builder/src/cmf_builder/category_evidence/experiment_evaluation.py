"""Immutable BD-007 rubric and scorecard validation.

No score in this module is generated or inferred.  It validates independently
produced scorecards and prevents non-compensable semantic failures from passing.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Sequence

from .experiment_contracts import (
    EvidenceGateError,
    ExperimentArm,
    canonical_sha256,
    require_sha256,
)


DIMENSIONS = (
    "category_identity_preservation",
    "category_native_syntax",
    "spatial_structure",
    "temporal_structure",
    "reading_order_integrity",
    "conversational_turn_integrity",
    "identity_fidelity",
    "audience_context_fidelity",
    "edge_pressure_preservation",
    "activative_call_integrity",
    "desired_human_role_integrity",
    "desired_reaction_integrity",
    "micro_commitment_integrity",
    "wrong_reading_resistance",
    "semantic_lineage_completeness",
    "non_invention_of_human_truth",
    "output_contract_compliance",
)

NONCOMPENSABLE_FAILURES = (
    "constitutional_category_changed",
    "identity_dna_invented",
    "human_truth_invented",
    "reaction_receipt_invented",
    "expression_moment_invented",
    "mandatory_wrong_reading_lock_missing_or_weakened",
    "immutable_lineage_lost",
    "production_or_certification_claimed",
    "non_admitted_corpus_evidence_used",
)


class Applicability(str, Enum):
    APPLICABLE = "APPLICABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True)
class DimensionScore:
    dimension: str
    applicability: Applicability
    score: int | None
    justification: str
    evidence_sha256s: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.dimension not in DIMENSIONS:
            raise EvidenceGateError(f"unknown evaluation dimension: {self.dimension}")
        if not self.justification:
            raise EvidenceGateError("dimension justification is required")
        if self.applicability is Applicability.APPLICABLE:
            if self.score not in range(0, 5):
                raise EvidenceGateError("applicable dimensions require a score from 0 through 4")
            if not self.evidence_sha256s:
                raise EvidenceGateError("applicable dimensions require immutable evidence")
            for index, digest in enumerate(self.evidence_sha256s):
                require_sha256(digest, f"evidence_sha256s[{index}]")
        elif self.score is not None or self.evidence_sha256s:
            raise EvidenceGateError("NOT_APPLICABLE dimensions cannot carry scores or evidence")

    def as_dict(self) -> dict[str, Any]:
        return {
            "dimension": self.dimension,
            "applicability": self.applicability.value,
            "score": self.score,
            "justification": self.justification,
            "evidence_sha256s": list(self.evidence_sha256s),
        }


@dataclass(frozen=True)
class Scorecard:
    scorecard_version: str
    case_identity: str
    case_id: str
    arm: ExperimentArm
    provider_configuration_sha256: str
    repeat_index: int
    output_sha256: str
    scores: tuple[DimensionScore, ...]
    noncompensable_failures: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.scorecard_version:
            raise EvidenceGateError("scorecard_version is required")
        if not self.case_id:
            raise EvidenceGateError("case_id is required")
        for field in ("case_identity", "provider_configuration_sha256", "output_sha256"):
            require_sha256(getattr(self, field), field)
        dimensions = tuple(item.dimension for item in self.scores)
        if len(dimensions) != len(set(dimensions)):
            raise EvidenceGateError("scorecard dimensions must be unique")
        if set(dimensions) != set(DIMENSIONS):
            missing = sorted(set(DIMENSIONS) - set(dimensions))
            raise EvidenceGateError(f"scorecard dimension coverage is incomplete: {missing}")
        unknown = set(self.noncompensable_failures) - set(NONCOMPENSABLE_FAILURES)
        if unknown:
            raise EvidenceGateError(f"unknown non-compensable failure: {sorted(unknown)}")
        if self.repeat_index < 1:
            raise EvidenceGateError("repeat_index must be positive")

    @property
    def scorecard_identity(self) -> str:
        return canonical_sha256(self.as_dict())

    @property
    def passes_noncompensable_gate(self) -> bool:
        return not self.noncompensable_failures

    def score(self, dimension: str) -> int | None:
        return next(item.score for item in self.scores if item.dimension == dimension)

    def as_dict(self) -> dict[str, Any]:
        return {
            "scorecard_version": self.scorecard_version,
            "case_identity": self.case_identity,
            "case_id": self.case_id,
            "arm": self.arm.value,
            "provider_configuration_sha256": self.provider_configuration_sha256,
            "repeat_index": self.repeat_index,
            "output_sha256": self.output_sha256,
            "scores": [item.as_dict() for item in sorted(self.scores, key=lambda x: x.dimension)],
            "noncompensable_failures": sorted(self.noncompensable_failures),
        }


def validate_paired_scorecards(native: Scorecard, flattened: Scorecard) -> str:
    """Validate one repeat without inventing a campaign-wide numeric threshold."""

    if native.arm is not ExperimentArm.NATIVE or flattened.arm is not ExperimentArm.FLATTENED:
        raise EvidenceGateError("scorecard arms do not form a native/flattened pair")
    pair_fields = ("case_identity", "case_id", "provider_configuration_sha256", "repeat_index")
    if any(getattr(native, field) != getattr(flattened, field) for field in pair_fields):
        raise EvidenceGateError("scorecards do not belong to the same governed paired trial")
    if not native.passes_noncompensable_gate:
        return "NATIVE_NONCOMPENSABLE_FAILURE"
    if not flattened.passes_noncompensable_gate:
        return "FLATTENED_CONTROL_NONCOMPENSABLE_FAILURE"
    native_category = native.score("category_native_syntax")
    flat_category = flattened.score("category_native_syntax")
    native_locks = native.score("wrong_reading_resistance")
    flat_locks = flattened.score("wrong_reading_resistance")
    comparison_values = (native_category, flat_category, native_locks, flat_locks)
    if all(value is None for value in comparison_values):
        return "GOVERNED_NON_ACTIVATIVE_CONTROL_NO_ADVANTAGE_CLAIM"
    if any(value is None for value in comparison_values):
        raise EvidenceGateError("comparison dimensions must have identical applicability in both arms")
    assert native_category is not None and flat_category is not None
    assert native_locks is not None and flat_locks is not None
    if native_category > flat_category and native_locks > flat_locks:
        return "DEVELOPMENT_ADVANTAGE_OBSERVED_FOR_REPEAT"
    return "NO_GOVERNED_DEVELOPMENT_ADVANTAGE_FOR_REPEAT"


def rubric_identity() -> str:
    return canonical_sha256(
        {
            "rubric_id": "BD007-ST0603-EVALUATION-RUBRIC-v1",
            "dimensions": list(DIMENSIONS),
            "score_scale": {
                "0": "contradiction_invention_or_missing_required_evidence",
                "1": "major_semantic_loss_or_category_flattening",
                "2": "partial_preservation_with_material_gaps",
                "3": "complete_development_result_with_recorded_noncritical_limitations",
                "4": "complete_precise_traceable_development_result",
            },
            "noncompensable_failures": list(NONCOMPENSABLE_FAILURES),
            "paired_repeat_decision": {
                "native_noncompensable_failure": "NATIVE_NONCOMPENSABLE_FAILURE",
                "flattened_control_noncompensable_failure": "FLATTENED_CONTROL_NONCOMPENSABLE_FAILURE",
                "activative_advantage": "native strictly exceeds flattened on category_native_syntax and wrong_reading_resistance",
                "governed_non_activative_control": "both comparison dimensions explicitly NOT_APPLICABLE in both arms; no advantage claim",
                "mixed_applicability": "FAIL_CLOSED",
            },
            "production_threshold": "NOT_AUTHORIZED",
            "certification_threshold": "NOT_AUTHORIZED",
        }
    )
