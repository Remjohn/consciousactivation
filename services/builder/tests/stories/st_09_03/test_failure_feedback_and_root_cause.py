import pytest

from cmf_builder.workflow.node_validation import (
    FailureFeedbackPackage,
    NodeValidationError,
    RepairEligibilityReceipt,
    RootCauseEvidence,
    determine_repair_eligibility,
)


def feedback(**overrides):
    values = {
        "validation_receipt_identity": "receipt:validation:1",
        "failed_node_identity": "node:semantic-check",
        "failed_criterion": "hard_gate:HG-013",
        "reproduction_evidence_refs": ("repro:test:1",),
        "responsible_root_cause_owner": "owner:semantic-validator",
        "repair_and_invalidation_graph_ref": "repair-graph:1",
        "allowed_diagnosis_scope": ("node:semantic-check",),
        "frozen_state_ref": "frozen-state:1",
        "affected_descendant_refs": ("node:downstream",),
        "targeted_regression_requirements": ("tests/stories/st_09_03",),
        "escalation_conditions": ("root_cause_unlocalized",),
        "delivered_to_owner": "owner:semantic-validator",
    }
    values.update(overrides)
    return FailureFeedbackPackage(**values)


def root_cause():
    return RootCauseEvidence(
        reproduced_failure_ref="repro:test:1",
        localized_boundary_ref="boundary:node:semantic-check",
        working_failing_comparison_ref="comparison:1",
        hypothesis_ref="hypothesis:validator-threshold",
        hypothesis_test_result_ref="test-result:1",
        selected_cause="missing semantic evaluator receipt",
        confidence_basis="localized fixture and negative case agree",
    )


def test_minimal_feedback_routes_only_to_graph_declared_owner():
    package = feedback()

    assert package.delivered_to_owner == package.responsible_root_cause_owner
    assert package.as_dict()["broadcast"] is False
    assert package.package_identity


def test_feedback_rejects_broadcast_or_wrong_owner():
    with pytest.raises(NodeValidationError) as wrong_owner:
        feedback(delivered_to_owner="owner:other")
    assert wrong_owner.value.code == "FAILURE_FEEDBACK_OWNER_MISMATCH"

    with pytest.raises(NodeValidationError) as broadcast:
        feedback(broadcast=True)
    assert broadcast.value.code == "BROAD_FAILURE_FEEDBACK_PROHIBITED"


def test_repair_eligibility_requires_reproduced_localized_root_cause():
    blocked = determine_repair_eligibility(feedback(), None)
    assert isinstance(blocked, RepairEligibilityReceipt)
    assert blocked.repair_eligible is False
    assert blocked.block_reason == "ROOT_CAUSE_EVIDENCE_REQUIRED"

    eligible = determine_repair_eligibility(feedback(), root_cause())
    assert eligible.repair_eligible is True
    assert eligible.block_reason == ""


def test_root_cause_evidence_requires_every_required_field():
    with pytest.raises(NodeValidationError) as missing:
        RootCauseEvidence(
            reproduced_failure_ref="",
            localized_boundary_ref="boundary",
            working_failing_comparison_ref="comparison",
            hypothesis_ref="hypothesis",
            hypothesis_test_result_ref="result",
            selected_cause="cause",
            confidence_basis="basis",
        )
    assert missing.value.code == "MISSING_GOVERNED_FIELD"
