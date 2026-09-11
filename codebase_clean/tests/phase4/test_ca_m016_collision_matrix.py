from __future__ import annotations

import copy
import hashlib

import pytest
from pydantic import ValidationError

from conscious_activations_interview_expression.collision_matrix import (
    DIMENSIONS,
    ArtifactRef,
    AudienceBeliefStructure,
    CollisionMatrixValidationError,
    CollisionTensionCell,
    FalsificationCondition,
    GroundedCollision,
    SubjectGenesisTerritory,
    VerbatimAnchor,
    WorldSignal,
    compute_collision_tension_matrix,
    compute_collision_tension_score,
    normalize_score,
    validate_collision_admission,
)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _ref(prefix: str, revision: str = "r1", seed: str | None = None) -> ArtifactRef:
    value = seed or f"{prefix}:{revision}"
    return ArtifactRef(
        object_id=prefix,
        revision_id=revision,
        sha256=_sha(value),
    )


RAW = "I thought success meant control. Um then I learned to listen."
QUOTE_A = "I thought success meant control."
QUOTE_B = "Um then I learned to listen."


def _anchor(anchor_id: str, quote: str, start: int, *, evidence_id: str = "EVID-1", evidence_revision: str = "r1") -> VerbatimAnchor:
    return VerbatimAnchor(
        anchor_id=anchor_id,
        evidence_ref=_ref(evidence_id, evidence_revision),
        source_ref=_ref("SOURCE-1", "r2"),
        media_ref=_ref("MEDIA-1", "r1"),
        speaker_id="guest",
        start_ms=1000 + start,
        end_ms=2000 + start,
        transcript_text=RAW,
        transcript_sha256=_sha(RAW),
        character_start=start,
        character_end=start + len(quote),
        quote_text=quote,
        quote_sha256=_sha(quote),
        admission_receipt_ref=_ref("RCP-EVID-1", "r1"),
    )


def _fixtures():
    beliefs = [
        AudienceBeliefStructure(
            belief_id="BELIEF-01",
            label="Control creates safety",
            artifact_ref=_ref("AUDIENCE-TENSIONS", "r7"),
        ),
        AudienceBeliefStructure(
            belief_id="BELIEF-02",
            label="Listening requires surrender",
            artifact_ref=_ref("AUDIENCE-TENSIONS", "r7"),
        ),
    ]
    territories = [
        SubjectGenesisTerritory(
            territory_id="GEN-01",
            label="Learning through relational practice",
            artifact_ref=_ref("SUBJECT-GENESIS", "r4"),
        ),
        SubjectGenesisTerritory(
            territory_id="GEN-02",
            label="Releasing inherited control patterns",
            artifact_ref=_ref("SUBJECT-GENESIS", "r5"),
        ),
    ]
    world = [
        WorldSignal(
            signal_id="WORLD-01",
            label="Knowledge-work leadership is becoming distributed",
            artifact_ref=_ref("WORLD-SIGNAL", "r3"),
        )
    ]
    anchors = {
        "A-1": _anchor("A-1", QUOTE_A, 0),
        "A-2": _anchor("A-2", QUOTE_B, RAW.index(QUOTE_B)),
    }
    cells = []
    for belief in beliefs:
        for territory in territories:
            cells.append(
                CollisionTensionCell(
                    belief_id=belief.belief_id,
                    territory_id=territory.territory_id,
                    dimension_scores={
                        "belief_tension": 0.80,
                        "genesis_pressure": 0.70,
                        "world_contradiction": 0.60,
                        "evidence_grounding": 1.00,
                    },
                    anchor_ids_by_dimension={
                        "belief_tension": ("A-1",),
                        "genesis_pressure": ("A-2",),
                        "world_contradiction": ("A-1",),
                        "evidence_grounding": ("A-1", "A-2"),
                    },
                )
            )
    matrix = compute_collision_tension_matrix(
        audience_beliefs=beliefs,
        subject_genesis_territories=territories,
        cells=cells,
        anchors=anchors,
    )
    collision = GroundedCollision(
        workspace_id="WS-01",
        collision_id="COLL-016-01",
        revision_id="rev-1",
        subject_genesis_territory_ref=territories[0].artifact_ref,
        audience_tension_ref=beliefs[0].artifact_ref,
        world_signal_refs=(world[0].artifact_ref,),
        relation_type="PARADOX",
        tension_relation=(
            "The audience seeks safety through control while the subject's lived genesis "
            "shows that listening became possible only after releasing control."
        ),
        falsification_condition=FalsificationCondition(
            refuting_observation="Repeated observations show control improves the stated outcome.",
            disconfirming_testimony="The subject says listening never required releasing control.",
            boundary_limitation="This relation does not claim to generalize outside this territory.",
        ),
        matrix=matrix,
        anchor_index=anchors,
        evidence_refs=(_ref("EVID-1", "r1"),),
        admission_receipt_ref=_ref("RCP-COLLISION-1", "r1"),
    )
    return beliefs, territories, world, anchors, cells, matrix, collision


def test_normalize_score_accepts_only_bounded_finite_values():
    assert normalize_score(0.0) == 0.0
    assert normalize_score(1.0) == 1.0
    assert normalize_score(0.1250000000004) == 0.125

    with pytest.raises(CollisionMatrixValidationError):
        normalize_score(-0.001)
    with pytest.raises(CollisionMatrixValidationError):
        normalize_score(1.001)
    with pytest.raises(CollisionMatrixValidationError):
        normalize_score(float("nan"))
    with pytest.raises(CollisionMatrixValidationError):
        normalize_score(float("inf"))


def test_collision_tension_score_is_mathematically_normalized():
    score = compute_collision_tension_score(
        {dimension: value for dimension, value in zip(DIMENSIONS, [0.25, 0.5, 0.75, 1.0])}
    )
    assert score == 0.625
    assert 0.0 <= score <= 1.0


def test_matrix_is_rectangular_and_retains_separate_dimension_matrices():
    *_, matrix, _ = _fixtures()

    assert matrix.row_ids == ("BELIEF-01", "BELIEF-02")
    assert matrix.column_ids == ("GEN-01", "GEN-02")
    assert set(matrix.matrices_by_dimension) == set(DIMENSIONS)
    assert all(
        len(row) == 2
        for dimension_matrix in matrix.matrices_by_dimension.values()
        for row in dimension_matrix
    )
    assert len(matrix.aggregate_matrix) == 2
    assert all(0.0 <= value <= 1.0 for rows in matrix.matrices_by_dimension.values() for row in rows for value in row)
    assert all(0.0 <= value <= 1.0 for row in matrix.aggregate_matrix for value in row)


def test_every_score_cell_is_explainable_by_verbatim_coordinates():
    *_, matrix, _ = _fixtures()

    explanation = matrix.explain("BELIEF-01", "GEN-02")
    assert explanation["aggregate_score"] == 0.775
    assert explanation["dimension_scores"]["belief_tension"] == 0.80
    assert {item["anchor_id"] for item in explanation["verbatim_anchors"]} == {"A-1", "A-2"}
    coords = {item["anchor_id"]: item["coordinate"] for item in explanation["verbatim_anchors"]}
    assert coords["A-1"]["start_ms"] == 1000
    assert coords["A-1"]["quote_text"] == QUOTE_A
    assert coords["A-2"]["character_start"] == RAW.index(QUOTE_B)
    assert coords["A-2"]["quote_text"] == QUOTE_B


def test_positive_grounded_collision_admits_and_returns_digest():
    *_, collision = _fixtures()

    result = validate_collision_admission(collision=collision)

    assert result.admitted is True
    assert result.failure_codes == ()
    assert result.collision_digest
    assert len(result.collision_digest) == 64
    assert all(result.checks.values())


def test_score_only_admission_is_impossible_without_structural_poles():
    *_, matrix, _ = _fixtures()

    draft = GroundedCollision.model_construct(
        workspace_id="WS-01",
        collision_id="COLL-SCORE-ONLY",
        revision_id="rev-1",
        subject_genesis_territory_ref=_ref("SUBJECT-GENESIS", "r4"),
        audience_tension_ref=_ref("AUDIENCE-TENSIONS", "r7"),
        world_signal_refs=(),
        relation_type="PARADOX",
        tension_relation="A high score cannot establish a collision.",
        falsification_condition=FalsificationCondition(
            refuting_observation="A refuting observation exists.",
            disconfirming_testimony="A refuting testimony exists.",
            boundary_limitation="A boundary exists.",
        ),
        matrix=matrix,
        anchor_index={},
        evidence_refs=(),
        admission_receipt_ref=_ref("RCP-COLLISION-SCORE", "r1"),
    )

    result = validate_collision_admission(collision=draft)

    assert result.admitted is False
    assert "EVIDENCE_ERROR" in result.failure_codes
    assert result.checks["score_only_not_authoritative"] is True
    assert result.checks["world_signal_pole"] is False


def test_beautiful_single_pole_statement_fails_closed():
    *_, matrix, _ = _fixtures()

    draft = GroundedCollision.model_construct(
        workspace_id="WS-01",
        collision_id="COLL-ONE-POLE",
        revision_id="rev-1",
        subject_genesis_territory_ref=_ref("SUBJECT-GENESIS", "r4"),
        audience_tension_ref=_ref("AUDIENCE-TENSIONS", "r7"),
        world_signal_refs=(),
        relation_type="LATENT_TRUTH",
        tension_relation="A compelling emotional statement with insufficient grounding.",
        falsification_condition=FalsificationCondition(
            refuting_observation="A refuting observation exists.",
            disconfirming_testimony="A refuting testimony exists.",
            boundary_limitation="A boundary exists.",
        ),
        matrix=matrix,
        anchor_index={},
        evidence_refs=(),
        admission_receipt_ref=_ref("RCP-ONE-POLE", "r1"),
    )

    result = validate_collision_admission(collision=draft)

    assert result.admitted is False
    assert "EVIDENCE_ERROR" in result.failure_codes
    assert result.checks["world_signal_pole"] is False


def test_three_labeled_poles_without_real_evidence_or_falsification_fails():
    *_, matrix, _ = _fixtures()

    draft = GroundedCollision.model_construct(
        workspace_id="WS-01",
        collision_id="COLL-LABELS-ONLY",
        revision_id="rev-1",
        subject_genesis_territory_ref=_ref("SUBJECT-GENESIS", "r4"),
        audience_tension_ref=_ref("AUDIENCE-TENSIONS", "r7"),
        world_signal_refs=(_ref("WORLD-SIGNAL", "r3"),),
        relation_type="PARADOX",
        tension_relation="Three labels alone do not constitute evidence.",
        falsification_condition=FalsificationCondition.model_construct(
            refuting_observation="",
            disconfirming_testimony="",
            boundary_limitation="",
        ),
        matrix=matrix,
        anchor_index={},
        evidence_refs=(),
        admission_receipt_ref=_ref("RCP-LABELS-ONLY", "r1"),
    )

    result = validate_collision_admission(collision=draft)

    assert result.admitted is False
    assert {"EVIDENCE_ERROR"} & set(result.failure_codes)


def test_stale_pole_revision_is_rejected():
    *_, collision = _fixtures()
    current = {
        "subject_genesis": _ref("SUBJECT-GENESIS", "r999"),
        "audience_tension": collision.audience_tension_ref,
        "world_signal:0": collision.world_signal_refs[0],
    }

    result = validate_collision_admission(
        collision=collision,
        current_pole_refs=current,
    )

    assert result.admitted is False
    assert "PROVENANCE_ERROR" in result.failure_codes
    assert result.checks["lineage_current"] is False


def test_stale_evidence_revision_is_rejected():
    *_, collision = _fixtures()
    stale_current = {
        "EVID-1": _ref("EVID-1", "r999"),
    }

    result = validate_collision_admission(
        collision=collision,
        current_evidence_refs=stale_current,
    )

    assert result.admitted is False
    assert "PROVENANCE_ERROR" in result.failure_codes


def test_forged_verbatim_quote_fails_before_matrix_admission():
    with pytest.raises((CollisionMatrixValidationError, ValidationError)) as exc_info:
        _anchor("A-FORGED", "Then I learned to listen.", RAW.index(QUOTE_B))

    assert "PROVENANCE_ERROR" in str(exc_info.value)


def test_missing_dimension_anchor_fails_cell_creation():
    with pytest.raises((CollisionMatrixValidationError, ValidationError)) as exc_info:
        CollisionTensionCell(
            belief_id="B",
            territory_id="G",
            dimension_scores={dimension: 0.5 for dimension in DIMENSIONS},
            anchor_ids_by_dimension={
                "belief_tension": ("A-1",),
                "genesis_pressure": ("A-1",),
                "world_contradiction": ("A-1",),
                "evidence_grounding": (),
            },
        )

    assert "EVIDENCE_ERROR" in str(exc_info.value)


def test_matrix_rejects_incomplete_rectangle():
    beliefs, territories, _, anchors, cells, _, _ = _fixtures()
    with pytest.raises(CollisionMatrixValidationError) as exc_info:
        compute_collision_tension_matrix(
            audience_beliefs=beliefs,
            subject_genesis_territories=territories,
            cells=cells[:2],
            anchors=anchors,
        )

    assert "SCHEMA_ERROR" in str(exc_info.value)


def test_matrix_rejects_out_of_range_scores_without_clamping():
    beliefs, territories, _, anchors, cells, _, _ = _fixtures()
    changed = copy.deepcopy(cells)
    raw = changed[0].model_dump()
    raw["dimension_scores"]["belief_tension"] = 2.0
    changed[0] = raw

    with pytest.raises((CollisionMatrixValidationError, ValidationError)) as exc_info:
        compute_collision_tension_matrix(
            audience_beliefs=beliefs,
            subject_genesis_territories=territories,
            cells=changed,
            anchors=anchors,
        )

    assert "SCHEMA_ERROR" in str(exc_info.value)


def test_anchor_coordinates_include_exact_upstream_revision_and_media_coordinates():
    anchor = _anchor("A-1", QUOTE_A, 0)
    coordinate = anchor.coordinate

    assert coordinate["source_object_id"] == "SOURCE-1"
    assert coordinate["source_revision_id"] == "r2"
    assert coordinate["source_sha256"] == _ref("SOURCE-1", "r2").sha256
    assert coordinate["media_object_id"] == "MEDIA-1"
    assert coordinate["start_ms"] == 1000
    assert coordinate["end_ms"] == 2000
    assert coordinate["character_start"] == 0
    assert coordinate["character_end"] == len(QUOTE_A)
    assert coordinate["quote_sha256"] == _sha(QUOTE_A)
