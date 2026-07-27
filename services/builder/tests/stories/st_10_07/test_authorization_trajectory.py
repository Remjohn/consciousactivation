import pytest

from cmf_builder.application.authorization_trajectory import (
    AuthorizationTrajectoryError,
    TrajectoryRecord,
    TrajectoryStage,
    blocked_stage_explanation,
    current_trajectory,
    validate_trajectory,
)


def rec(stage, pred=None, status="PASS", evidence=("evidence",), open_gates=(), invalidated=False):
    return TrajectoryRecord(
        "subject:1",
        stage,
        status,
        pred,
        f"receipt:{stage.value}",
        evidence,
        "authority:builder",
        "development",
        ("offline only",),
        open_gates,
        ("invalidation:source",),
        (),
        "2026-07-17T00:00:00Z",
        "current",
        invalidated,
    )


def test_trajectory_preserves_gate_separation_and_blocked_explanation():
    records = (
        rec(TrajectoryStage.IMPLEMENTATION_COMPLETION),
        rec(TrajectoryStage.EVALUATION, TrajectoryStage.IMPLEMENTATION_COMPLETION),
        rec(TrajectoryStage.EVIDENCE_CLOSURE, TrajectoryStage.EVALUATION, "PENDING", open_gates=("BD-007",)),
    )
    validate_trajectory(records)

    assert blocked_stage_explanation(records) == {"EVIDENCE_CLOSURE": ["BD-007"]}
    assert current_trajectory(records) == records


def test_repair_requires_diagnosis_and_maturity_requires_evidence():
    with pytest.raises(AuthorizationTrajectoryError) as repair:
        validate_trajectory((rec(TrajectoryStage.IMPLEMENTATION_COMPLETION), rec(TrajectoryStage.REPAIR, TrajectoryStage.IMPLEMENTATION_COMPLETION)))
    assert repair.value.code == "REPAIR_WITHOUT_DIAGNOSIS"

    with pytest.raises(AuthorizationTrajectoryError) as maturity:
        validate_trajectory((rec(TrajectoryStage.MATURITY_PROMOTION, evidence=()),))
    assert maturity.value.code == "MATURITY_PROMOTION_WITHOUT_EVIDENCE"


def test_production_certification_noncompensable_and_invalidated_fail_closed():
    with pytest.raises(AuthorizationTrajectoryError) as production:
        validate_trajectory((rec(TrajectoryStage.PRODUCTION_READINESS),))
    assert production.value.code == "FALSE_PRODUCTION_OR_CERTIFICATION_INFERENCE"

    with pytest.raises(AuthorizationTrajectoryError) as hidden:
        validate_trajectory((rec(TrajectoryStage.NON_COMPENSABLE_FAILURE, status="HIDDEN_BY_AGGREGATE"),))
    assert hidden.value.code == "NON_COMPENSABLE_FAILURE_HIDDEN"

    with pytest.raises(AuthorizationTrajectoryError) as invalidated:
        validate_trajectory((rec(TrajectoryStage.INVALIDATION, status="ACTIVE", invalidated=True),))
    assert invalidated.value.code == "INVALIDATED_EVIDENCE_SHOWN_ACTIVE"
