"""
CA-M016 — Grounded Collision Tension Matrix.

This module owns the bounded, explainable scoring primitive for a grounded
Collision. Scores are descriptive evidence-weighted measurements; they are
never authority by themselves. Admission remains a fail-closed predicate over
required semantic poles, exact upstream revisions, admitted evidence,
verbatim anchors, relation semantics, and falsification conditions.
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import Mapping, Sequence

from pydantic import BaseModel, ConfigDict, Field, model_validator


MANDATE_ID = "CA-M016"
REQUIREMENT_ID = "FR-016"
INVARIANT_ID = "FR-COLL-001"
MATRIX_VERSION = "1.0.0"

DIMENSIONS: tuple[str, ...] = (
    "belief_tension",
    "genesis_pressure",
    "world_contradiction",
    "evidence_grounding",
)

FAILURE_CLASS = {
    "MISSING_POLE": "EVIDENCE_ERROR",
    "MISSING_EVIDENCE": "EVIDENCE_ERROR",
    "MISSING_ANCHOR": "EVIDENCE_ERROR",
    "INVALID_SCORE": "SCHEMA_ERROR",
    "UNSUPPORTED_RELATION": "RELATION_ERROR",
    "MISSING_FALSIFICATION": "EVIDENCE_ERROR",
    "STALE_REFERENCE": "PROVENANCE_ERROR",
    "FORGED_ANCHOR": "PROVENANCE_ERROR",
    "SHAPE_MISMATCH": "SCHEMA_ERROR",
}


class CollisionMatrixValidationError(ValueError):
    """Raised when CA-M016 input cannot be admitted as grounded evidence."""


class ArtifactRef(BaseModel):
    """Exact identity of an upstream canonical artifact revision."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    object_id: str = Field(min_length=1)
    revision_id: str = Field(min_length=1)
    sha256: str = Field(min_length=64, max_length=64)

    @model_validator(mode="after")
    def validate_digest(self) -> "ArtifactRef":
        _require_sha256(self.sha256, "sha256")
        return self


class VerbatimAnchor(BaseModel):
    """
    A source-bound, character-exact quote with temporal and digest coordinates.

    The transcript slice is retained so the object can prove that quote_text is
    not a semantic paraphrase. source_ref identifies the exact upstream source
    revision, while evidence_ref identifies the admitted evidence object.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    anchor_id: str = Field(min_length=1)
    evidence_ref: ArtifactRef
    evidence_state: str = Field(default="ADMITTED")
    source_ref: ArtifactRef
    media_ref: ArtifactRef
    speaker_id: str = Field(min_length=1)
    start_ms: int = Field(ge=0)
    end_ms: int = Field(gt=0)
    transcript_text: str = Field(min_length=1)
    transcript_sha256: str = Field(min_length=64, max_length=64)
    character_start: int = Field(ge=0)
    character_end: int = Field(gt=0)
    quote_text: str = Field(min_length=1)
    quote_sha256: str = Field(min_length=64, max_length=64)
    admission_receipt_ref: ArtifactRef

    @model_validator(mode="after")
    def validate_exact_coordinates(self) -> "VerbatimAnchor":
        if self.evidence_state != "ADMITTED":
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['MISSING_EVIDENCE']}: anchor '{self.anchor_id}' "
                "must reference ADMITTED evidence"
            )
        if self.end_ms <= self.start_ms:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['FORGED_ANCHOR']}: end_ms must be greater than start_ms"
            )
        if self.character_end > len(self.transcript_text):
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['FORGED_ANCHOR']}: character span exceeds transcript"
            )
        exact = self.transcript_text[self.character_start : self.character_end]
        if exact != self.quote_text:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['FORGED_ANCHOR']}: quote_text must equal the exact "
                "transcript character slice"
            )
        if _sha256_text(self.transcript_text) != self.transcript_sha256:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['FORGED_ANCHOR']}: transcript digest mismatch"
            )
        if _sha256_text(self.quote_text) != self.quote_sha256:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['FORGED_ANCHOR']}: quote digest mismatch"
            )
        return self

    @property
    def coordinate(self) -> dict[str, object]:
        """Return only inspectable source coordinates and exact quote evidence."""
        return {
            "source_object_id": self.source_ref.object_id,
            "source_revision_id": self.source_ref.revision_id,
            "source_sha256": self.source_ref.sha256,
            "media_object_id": self.media_ref.object_id,
            "media_revision_id": self.media_ref.revision_id,
            "media_sha256": self.media_ref.sha256,
            "speaker_id": self.speaker_id,
            "start_ms": self.start_ms,
            "end_ms": self.end_ms,
            "character_start": self.character_start,
            "character_end": self.character_end,
            "quote_text": self.quote_text,
            "quote_sha256": self.quote_sha256,
            "evidence_object_id": self.evidence_ref.object_id,
            "evidence_revision_id": self.evidence_ref.revision_id,
            "evidence_sha256": self.evidence_ref.sha256,
        }


class AudienceBeliefStructure(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    belief_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    artifact_ref: ArtifactRef


class SubjectGenesisTerritory(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    territory_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    artifact_ref: ArtifactRef


class WorldSignal(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    signal_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    artifact_ref: ArtifactRef


class CollisionTensionCell(BaseModel):
    """
    One audience-belief × subject-genesis coordinate.

    The aggregate score is the equal-weight arithmetic mean of the declared
    dimensions. It is explanatory only; admission never uses this value as a
    substitute for pole/evidence predicates.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    belief_id: str = Field(min_length=1)
    territory_id: str = Field(min_length=1)
    dimension_scores: dict[str, float] = Field(min_length=1)
    anchor_ids_by_dimension: dict[str, tuple[str, ...]] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_scores_and_anchors(self) -> "CollisionTensionCell":
        expected = set(DIMENSIONS)
        actual = set(self.dimension_scores)
        if actual != expected:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['SHAPE_MISMATCH']}: dimensions must be "
                f"{sorted(expected)}, got {sorted(actual)}"
            )
        if set(self.anchor_ids_by_dimension) != expected:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['MISSING_ANCHOR']}: every score dimension requires anchors"
            )
        for dimension, score in self.dimension_scores.items():
            _validate_score(score, f"dimension_scores[{dimension!r}]")
            if not self.anchor_ids_by_dimension[dimension]:
                raise CollisionMatrixValidationError(
                    f"{FAILURE_CLASS['MISSING_ANCHOR']}: dimension '{dimension}' "
                    "has no verbatim anchor"
                )
            if any(not anchor_id.strip() for anchor_id in self.anchor_ids_by_dimension[dimension]):
                raise CollisionMatrixValidationError(
                    f"{FAILURE_CLASS['MISSING_ANCHOR']}: blank anchor id"
                )
        return self

    @property
    def overall_score(self) -> float:
        return normalize_score(sum(self.dimension_scores.values()) / len(DIMENSIONS))


class CollisionTensionMatrix(BaseModel):
    """Complete rectangular set of normalized dimension matrices."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    version: str = MATRIX_VERSION
    row_ids: tuple[str, ...]
    column_ids: tuple[str, ...]
    cells: tuple[CollisionTensionCell, ...]
    matrices_by_dimension: dict[str, tuple[tuple[float, ...], ...]]
    aggregate_matrix: tuple[tuple[float, ...], ...]
    explanation_by_coordinate: dict[str, tuple[dict[str, object], ...]]

    @model_validator(mode="after")
    def validate_matrix_integrity(self) -> "CollisionTensionMatrix":
        if not self.row_ids or not self.column_ids:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['MISSING_POLE']}: matrix requires at least one "
                "audience belief and one subject genesis territory"
            )

        expected_cells = {
            (belief_id, territory_id)
            for belief_id in self.row_ids
            for territory_id in self.column_ids
        }
        actual_cells = {(cell.belief_id, cell.territory_id) for cell in self.cells}
        if actual_cells != expected_cells:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['SHAPE_MISMATCH']}: cells do not form a complete rectangle"
            )

        if set(self.matrices_by_dimension) != set(DIMENSIONS):
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['SHAPE_MISMATCH']}: dimension matrices are incomplete"
            )

        rows = len(self.row_ids)
        cols = len(self.column_ids)
        for dimension in DIMENSIONS:
            matrix = self.matrices_by_dimension[dimension]
            _validate_matrix_shape(matrix, rows, cols, dimension)
        _validate_matrix_shape(
            self.aggregate_matrix, rows, cols, "aggregate_matrix"
        )

        expected_explanations = {
            _coordinate_key(belief_id, territory_id)
            for belief_id in self.row_ids
            for territory_id in self.column_ids
        }
        if set(self.explanation_by_coordinate) != expected_explanations:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['SHAPE_MISMATCH']}: explanation coordinates are incomplete"
            )
        return self

    def explain(self, belief_id: str, territory_id: str) -> dict[str, object]:
        """Return verbatim anchors and scores for an exact matrix coordinate."""
        key = _coordinate_key(belief_id, territory_id)
        try:
            explanations = self.explanation_by_coordinate[key]
        except KeyError as exc:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['EVIDENCE_ERROR']}: unknown matrix coordinate '{key}'"
            ) from exc
        return {
            "coordinate": {"belief_id": belief_id, "territory_id": territory_id},
            "aggregate_score": self.aggregate_matrix[
                self.row_ids.index(belief_id)
            ][self.column_ids.index(territory_id)],
            "dimension_scores": {
                dimension: self.matrices_by_dimension[dimension][
                    self.row_ids.index(belief_id)
                ][self.column_ids.index(territory_id)]
                for dimension in DIMENSIONS
            },
            "verbatim_anchors": [dict(item) for item in explanations],
        }


class FalsificationCondition(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    refuting_observation: str = Field(min_length=10)
    disconfirming_testimony: str = Field(min_length=10)
    boundary_limitation: str = Field(min_length=10)


class GroundedCollision(BaseModel):
    """
    Admissible Collision relation. The relation is grounded in three semantic
    poles and a complete, explainable tension matrix.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    workspace_id: str = Field(min_length=1)
    collision_id: str = Field(min_length=1)
    revision_id: str = Field(min_length=1)
    subject_genesis_territory_ref: ArtifactRef
    audience_tension_ref: ArtifactRef
    world_signal_refs: tuple[ArtifactRef, ...]
    relation_type: str = Field(min_length=1)
    tension_relation: str = Field(min_length=10)
    falsification_condition: FalsificationCondition
    matrix: CollisionTensionMatrix
    anchor_index: dict[str, VerbatimAnchor]
    evidence_refs: tuple[ArtifactRef, ...]
    admission_receipt_ref: ArtifactRef

    @model_validator(mode="after")
    def validate_grounding(self) -> "GroundedCollision":
        allowed_relations = {
            "ANALOGY",
            "INVERSION",
            "PARADOX",
            "SYSTEMS_LENS",
            "COUNTER_POSITION",
            "LATENT_TRUTH",
            "MEANINGFUL_TENSION",
        }
        if self.relation_type not in allowed_relations:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['UNSUPPORTED_RELATION']}: '{self.relation_type}'"
            )
        if not self.world_signal_refs:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['MISSING_POLE']}: at least one world signal is required"
            )
        if not self.anchor_index:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['MISSING_ANCHOR']}: collision requires verbatim evidence anchors"
            )
        if not self.evidence_refs:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['MISSING_EVIDENCE']}: collision requires admitted evidence refs"
            )
        if all(not value.strip() for value in (
            self.falsification_condition.refuting_observation,
            self.falsification_condition.disconfirming_testimony,
            self.falsification_condition.boundary_limitation,
        )):
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['MISSING_FALSIFICATION']}: falsification is required"
            )
        expected_anchor_ids = {
            anchor_id
            for cell in self.matrix.cells
            for ids in cell.anchor_ids_by_dimension.values()
            for anchor_id in ids
        }
        if not expected_anchor_ids.issubset(self.anchor_index):
            missing = sorted(expected_anchor_ids - set(self.anchor_index))
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['MISSING_ANCHOR']}: missing anchors {missing}"
            )
        for anchor in self.anchor_index.values():
            if not any(
                ref.object_id == anchor.evidence_ref.object_id
                and ref.revision_id == anchor.evidence_ref.revision_id
                and ref.sha256 == anchor.evidence_ref.sha256
                for ref in self.evidence_refs
            ):
                raise CollisionMatrixValidationError(
                    f"{FAILURE_CLASS['FORGED_ANCHOR']}: anchor '{anchor.anchor_id}' "
                    "does not point to a declared collision evidence ref"
                )
        return self


class AdmissionResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    admitted: bool
    invariant: str = INVARIANT_ID
    mandate_id: str = MANDATE_ID
    failure_codes: tuple[str, ...] = ()
    checks: dict[str, bool]
    collision_digest: str | None = None


def normalize_score(value: float) -> float:
    """
    Validate an already-normalized score.

    No clamping is performed: accepting an out-of-range score by silently
    clipping it would conceal upstream corruption and weaken explainability.
    """
    _validate_score(value, "score")
    return round(float(value), 12)


def compute_collision_tension_score(
    dimension_scores: Mapping[str, float],
) -> float:
    """Compute the equal-weight normalized descriptive collision score."""
    if set(dimension_scores) != set(DIMENSIONS):
        raise CollisionMatrixValidationError(
            f"{FAILURE_CLASS['SHAPE_MISMATCH']}: collision score requires "
            f"dimensions {list(DIMENSIONS)}"
        )
    for name, value in dimension_scores.items():
        _validate_score(value, f"dimension_scores[{name!r}]")
    return normalize_score(sum(dimension_scores.values()) / len(DIMENSIONS))


def compute_collision_tension_matrix(
    *,
    audience_beliefs: Sequence[AudienceBeliefStructure],
    subject_genesis_territories: Sequence[SubjectGenesisTerritory],
    cells: Sequence[CollisionTensionCell | Mapping[str, object]],
    anchors: Mapping[str, VerbatimAnchor],
) -> CollisionTensionMatrix:
    """
    Build a rectangular audience-belief × subject-genesis matrix.

    Every dimension is retained as its own normalized matrix. The aggregate is
    included for ranking/inspection only and is never sufficient for admission.
    """
    if not audience_beliefs:
        raise CollisionMatrixValidationError(
            f"{FAILURE_CLASS['MISSING_POLE']}: audience_beliefs cannot be empty"
        )
    if not subject_genesis_territories:
        raise CollisionMatrixValidationError(
            f"{FAILURE_CLASS['MISSING_POLE']}: subject_genesis_territories cannot be empty"
        )
    if not anchors:
        raise CollisionMatrixValidationError(
            f"{FAILURE_CLASS['MISSING_ANCHOR']}: at least one verbatim anchor is required"
        )

    row_ids = tuple(item.belief_id for item in audience_beliefs)
    column_ids = tuple(item.territory_id for item in subject_genesis_territories)

    if len(set(row_ids)) != len(row_ids) or len(set(column_ids)) != len(column_ids):
        raise CollisionMatrixValidationError(
            f"{FAILURE_CLASS['SHAPE_MISMATCH']}: audience and territory ids must be unique"
        )

    normalized_cells: list[CollisionTensionCell] = []
    for raw_cell in cells:
        cell = (
            raw_cell
            if isinstance(raw_cell, CollisionTensionCell)
            else CollisionTensionCell.model_validate(raw_cell)
        )
        if cell.belief_id not in row_ids or cell.territory_id not in column_ids:
            raise CollisionMatrixValidationError(
                f"{FAILURE_CLASS['SHAPE_MISMATCH']}: cell references unknown matrix coordinate"
            )
        for dimension, anchor_ids in cell.anchor_ids_by_dimension.items():
            missing = [anchor_id for anchor_id in anchor_ids if anchor_id not in anchors]
            if missing:
                raise CollisionMatrixValidationError(
                    f"{FAILURE_CLASS['MISSING_ANCHOR']}: {dimension} missing {missing}"
                )
        normalized_cells.append(cell)

    expected = {
        (belief_id, territory_id)
        for belief_id in row_ids
        for territory_id in column_ids
    }
    actual = {(cell.belief_id, cell.territory_id) for cell in normalized_cells}
    if actual != expected:
        raise CollisionMatrixValidationError(
            f"{FAILURE_CLASS['SHAPE_MISMATCH']}: expected {len(expected)} unique cells, "
            f"received {len(actual)}"
        )

    matrices_by_dimension: dict[str, tuple[tuple[float, ...], ...]] = {}
    aggregate_rows: list[tuple[float, ...]] = []
    explanation_by_coordinate: dict[str, tuple[dict[str, object], ...]] = {}

    cell_lookup = {(cell.belief_id, cell.territory_id): cell for cell in normalized_cells}
    for dimension in DIMENSIONS:
        matrix_rows: list[tuple[float, ...]] = []
        for belief_id in row_ids:
            row: list[float] = []
            for territory_id in column_ids:
                cell = cell_lookup[(belief_id, territory_id)]
                score = normalize_score(cell.dimension_scores[dimension])
                row.append(score)
                explanation_by_coordinate.setdefault(
                    _coordinate_key(belief_id, territory_id),
                    tuple(),
                )
            matrix_rows.append(tuple(row))
        matrices_by_dimension[dimension] = tuple(matrix_rows)

    for belief_id in row_ids:
        row: list[float] = []
        for territory_id in column_ids:
            cell = cell_lookup[(belief_id, territory_id)]
            row.append(cell.overall_score)
            coordinate = _coordinate_key(belief_id, territory_id)
            anchor_rows = []
            seen: set[str] = set()
            for dimension in DIMENSIONS:
                for anchor_id in cell.anchor_ids_by_dimension[dimension]:
                    if anchor_id in seen:
                        continue
                    seen.add(anchor_id)
                    anchor_rows.append(
                        {
                            "anchor_id": anchor_id,
                            "dimension": dimension,
                            "coordinate": anchors[anchor_id].coordinate,
                        }
                    )
            explanation_by_coordinate[coordinate] = tuple(anchor_rows)
        aggregate_rows.append(tuple(row))

    return CollisionTensionMatrix(
        row_ids=row_ids,
        column_ids=column_ids,
        cells=tuple(normalized_cells),
        matrices_by_dimension=matrices_by_dimension,
        aggregate_matrix=tuple(aggregate_rows),
        explanation_by_coordinate=explanation_by_coordinate,
    )


def validate_collision_admission(
    *,
    collision: GroundedCollision,
    current_pole_refs: Mapping[str, ArtifactRef] | None = None,
    current_evidence_refs: Mapping[str, ArtifactRef] | None = None,
) -> AdmissionResult:
    """
    Apply the CA-M016 fail-closed admission predicate.

    current_* mappings are optional integration hooks for repository-backed
    verification. When supplied, exact object/revision/digest identity is
    required; this prevents stale or forged lineage from being admitted.
    """
    checks: dict[str, bool] = {
        "subject_genesis_pole": bool(collision.subject_genesis_territory_ref.object_id),
        "audience_tension_pole": bool(collision.audience_tension_ref.object_id),
        "world_signal_pole": bool(collision.world_signal_refs),
        "evidence_present": bool(collision.evidence_refs),
        "verbatim_anchors_present": bool(collision.anchor_index),
        "relation_supported": bool(collision.relation_type and collision.tension_relation.strip()),
        "falsification_present": _has_falsification(collision.falsification_condition),
        "matrix_bounded": _matrix_is_bounded(collision.matrix),
        "matrix_explainable": _matrix_is_explainable(collision.matrix),
        "score_only_not_authoritative": True,
        "lineage_current": True,
    }
    failures: list[str] = []

    if current_pole_refs is not None:
        required_poles = {
            "subject_genesis": collision.subject_genesis_territory_ref,
            "audience_tension": collision.audience_tension_ref,
        }
        for key, expected in required_poles.items():
            actual = current_pole_refs.get(key)
            if actual != expected:
                checks["lineage_current"] = False
                failures.append(FAILURE_CLASS["STALE_REFERENCE"])
                break

        if checks["lineage_current"]:
            for index, expected in enumerate(collision.world_signal_refs):
                actual = current_pole_refs.get(f"world_signal:{index}")
                if actual != expected:
                    checks["lineage_current"] = False
                    failures.append(FAILURE_CLASS["STALE_REFERENCE"])
                    break

    if current_evidence_refs is not None and checks["lineage_current"]:
        for expected in collision.evidence_refs:
            actual = current_evidence_refs.get(expected.object_id)
            if actual != expected:
                checks["lineage_current"] = False
                failures.append(FAILURE_CLASS["STALE_REFERENCE"])
                break

    for cell in collision.matrix.cells:
        for dimension in DIMENSIONS:
            if not cell.anchor_ids_by_dimension[dimension]:
                failures.append(FAILURE_CLASS["MISSING_ANCHOR"])
                break

    if not all(checks.values()):
        if not checks["subject_genesis_pole"] or not checks["audience_tension_pole"] or not checks["world_signal_pole"]:
            failures.append(FAILURE_CLASS["MISSING_POLE"])
        if not checks["evidence_present"] or not checks["verbatim_anchors_present"]:
            failures.append(FAILURE_CLASS["MISSING_EVIDENCE"])
        if not checks["relation_supported"]:
            failures.append(FAILURE_CLASS["UNSUPPORTED_RELATION"])
        if not checks["falsification_present"]:
            failures.append(FAILURE_CLASS["MISSING_FALSIFICATION"])

    failure_codes = tuple(sorted(set(failures)))
    if failure_codes:
        return AdmissionResult(
            admitted=False,
            checks=checks,
            failure_codes=failure_codes,
        )

    digest = canonical_collision_digest(collision)
    return AdmissionResult(
        admitted=True,
        checks=checks,
        failure_codes=(),
        collision_digest=digest,
    )


def canonical_collision_digest(collision: GroundedCollision) -> str:
    """Return a deterministic digest over the semantically authoritative payload."""
    payload = collision.model_dump(mode="json", exclude_none=True)
    canonical = _canonical_json(payload).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _has_falsification(condition: FalsificationCondition) -> bool:
    return all(
        isinstance(value, str) and len(value.strip()) >= 10
        for value in (
            condition.refuting_observation,
            condition.disconfirming_testimony,
            condition.boundary_limitation,
        )
    )


def _matrix_is_bounded(matrix: CollisionTensionMatrix) -> bool:
    values: list[float] = []
    for dimension in DIMENSIONS:
        for row in matrix.matrices_by_dimension[dimension]:
            values.extend(row)
    for row in matrix.aggregate_matrix:
        values.extend(row)
    return all(math.isfinite(value) and 0.0 <= value <= 1.0 for value in values)


def _matrix_is_explainable(matrix: CollisionTensionMatrix) -> bool:
    for coordinate, items in matrix.explanation_by_coordinate.items():
        if not items:
            return False
        if any(
            not item.get("coordinate", {}).get("source_object_id")
            or not item.get("coordinate", {}).get("start_ms") is not None
            or not item.get("coordinate", {}).get("end_ms") is not None
            or not str(item.get("coordinate", {}).get("quote_text", "")).strip()
            for item in items
        ):
            return False
    return True


def _validate_matrix_shape(
    matrix: Sequence[Sequence[float]],
    rows: int,
    cols: int,
    name: str,
) -> None:
    if len(matrix) != rows or any(len(row) != cols for row in matrix):
        raise CollisionMatrixValidationError(
            f"{FAILURE_CLASS['SHAPE_MISMATCH']}: {name} must be {rows}x{cols}"
        )
    for row_index, row in enumerate(matrix):
        for col_index, value in enumerate(row):
            _validate_score(value, f"{name}[{row_index}][{col_index}]")


def _validate_score(value: float, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CollisionMatrixValidationError(
            f"{FAILURE_CLASS['INVALID_SCORE']}: {name} must be numeric"
        )
    if not math.isfinite(float(value)) or not 0.0 <= float(value) <= 1.0:
        raise CollisionMatrixValidationError(
            f"{FAILURE_CLASS['INVALID_SCORE']}: {name} must be finite and within [0.0, 1.0]"
        )


def _require_sha256(value: str, name: str) -> None:
    if not re.fullmatch(r"[0-9a-fA-F]{64}", value):
        raise CollisionMatrixValidationError(
            f"{FAILURE_CLASS['FORGED_ANCHOR']}: {name} must be a SHA-256 hex digest"
        )


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _canonical_json(value: object) -> str:
    import json

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _coordinate_key(belief_id: str, territory_id: str) -> str:
    return f"{belief_id}::{territory_id}"


__all__ = [
    "AdmissionResult",
    "ArtifactRef",
    "AudienceBeliefStructure",
    "CollisionMatrixValidationError",
    "CollisionTensionCell",
    "CollisionTensionMatrix",
    "DIMENSIONS",
    "FalsificationCondition",
    "GroundedCollision",
    "MANDATE_ID",
    "MATRIX_VERSION",
    "REQUIREMENT_ID",
    "SubjectGenesisTerritory",
    "VerbatimAnchor",
    "WorldSignal",
    "canonical_collision_digest",
    "compute_collision_tension_matrix",
    "compute_collision_tension_score",
    "normalize_score",
    "validate_collision_admission",
]
