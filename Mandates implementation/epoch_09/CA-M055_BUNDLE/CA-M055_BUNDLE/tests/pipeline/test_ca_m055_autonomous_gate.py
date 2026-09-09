"""Executable evidence for CA-M055 / INV-AUTO-001.

The tests load the mandate module directly so unrelated package bootstrap
requirements cannot create a false negative for this bounded gate.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "services" / "pipeline" / "src" / "cmf_pipeline" / "collision" / "autonomous_gate.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("cmf_pipeline_collision_autonomous_gate", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


mod = _load_module()
AutonomousApprovalDeniedError = mod.AutonomousApprovalDeniedError
AutonomousCollisionApprovalGate = mod.AutonomousCollisionApprovalGate
AutonomousGatePolicy = mod.AutonomousGatePolicy
CollisionScores = mod.CollisionScores
GateDecision = mod.GateDecision
GateReason = mod.GateReason


def _scores(value: float = 0.98) -> CollisionScores:
    return CollisionScores(value, value, value, value, value)


class TestAutonomousCollisionApprovalGate:
    def test_high_confidence_collision_is_autonomously_approved(self):
        result = AutonomousCollisionApprovalGate().evaluate("collision-001", _scores())
        assert result.decision is GateDecision.APPROVE_AUTONOMOUS
        assert result.reason is GateReason.ALL_THRESHOLDS_MET
        assert result.autonomous_approved
        assert not result.requires_manual_review
        assert len(result.receipt_sha256) == 64

    def test_exact_autonomous_threshold_is_inclusive(self):
        policy = AutonomousGatePolicy(minimum_score=0.90, autonomous_score=0.95)
        gate = AutonomousCollisionApprovalGate(policy)
        result = gate.evaluate("collision-002", _scores(0.95))
        assert result.decision is GateDecision.APPROVE_AUTONOMOUS
        assert result.aggregate_score == pytest.approx(0.95)

    def test_borderline_dimension_fails_closed_to_manual_review(self):
        scores = _scores()
        borderline = CollisionScores(0.90, 0.90, 0.90, 0.86, 0.90)
        result = AutonomousCollisionApprovalGate().evaluate("collision-003", borderline)
        assert result.decision is GateDecision.MANUAL_REVIEW
        assert result.reason is GateReason.BORDERLINE_CONFIDENCE
        assert result.failed_dimensions == ("novelty",)

    def test_aggregate_below_autonomous_threshold_requires_manual_review(self):
        policy = AutonomousGatePolicy(minimum_score=0.90, autonomous_score=0.95)
        scores = CollisionScores(0.92, 0.92, 0.92, 0.92, 0.92)
        result = AutonomousCollisionApprovalGate(policy).evaluate("collision-004", scores)
        assert result.aggregate_score < 0.95
        assert result.decision is GateDecision.MANUAL_REVIEW

    def test_far_below_threshold_is_rejected(self):
        scores = CollisionScores(0.50, 0.60, 0.70, 0.75, 0.80)
        result = AutonomousCollisionApprovalGate().evaluate("collision-005", scores)
        assert result.decision is GateDecision.REJECT
        assert result.reason is GateReason.BELOW_AUTONOMOUS_THRESHOLD
        assert set(result.failed_dimensions) == {"confidence", "grounding", "evidence_quality", "novelty", "safety"}

    def test_missing_score_is_fail_closed(self):
        with pytest.raises(ValueError):
            AutonomousCollisionApprovalGate().evaluate("collision-006", {"confidence": 0.99})

    @pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf"), -0.01, 1.01])
    def test_non_finite_or_out_of_range_score_is_rejected(self, value):
        scores = _scores()
        invalid = CollisionScores(value, scores.grounding, scores.evidence_quality, scores.novelty, scores.safety)
        with pytest.raises(ValueError):
            AutonomousCollisionApprovalGate().evaluate("collision-invalid", invalid)

    def test_unknown_score_dimension_is_rejected(self):
        scores = _scores().as_mapping()
        scores["operator_override"] = 1.0
        with pytest.raises(ValueError):
            AutonomousCollisionApprovalGate().evaluate("collision-008", scores)

    def test_require_autonomous_approval_blocks_borderline_false_proof(self):
        scores = CollisionScores(0.95, 0.95, 0.95, 0.85, 0.95)
        with pytest.raises(AutonomousApprovalDeniedError) as exc_info:
            AutonomousCollisionApprovalGate().require_autonomous_approval("collision-009", scores)
        assert exc_info.value.result.decision is GateDecision.MANUAL_REVIEW

    def test_false_proof_high_confidence_does_not_bypass_policy_dimension(self):
        # High confidence alone cannot authorize a collision when another policy
        # dimension remains below the strict threshold.
        scores = CollisionScores(0.999, 0.999, 0.999, 0.10, 0.999)
        result = AutonomousCollisionApprovalGate().evaluate("collision-010", scores)
        assert result.decision is GateDecision.REJECT
        assert result.autonomous_approved is False

    def test_receipt_is_deterministic_for_identical_evidence(self):
        gate = AutonomousCollisionApprovalGate()
        left = gate.evaluate("collision-011", _scores())
        right = gate.evaluate("collision-011", _scores())
        assert left.receipt_sha256 == right.receipt_sha256

    def test_receipt_binds_policy_identity_as_well_as_collision_evidence(self):
        left = AutonomousCollisionApprovalGate(AutonomousGatePolicy(autonomous_score=0.95)).evaluate("collision-012", _scores())
        right = AutonomousCollisionApprovalGate(AutonomousGatePolicy(autonomous_score=0.96)).evaluate("collision-012", _scores())
        assert left.receipt_sha256 != right.receipt_sha256

    def test_receipt_binds_collision_identity_and_decision_evidence(self):
        gate = AutonomousCollisionApprovalGate()
        first = gate.evaluate("collision-012", _scores())
        second = gate.evaluate("collision-013", _scores())
        assert first.receipt_sha256 != second.receipt_sha256

    def test_policy_rejects_invalid_threshold_relationship(self):
        with pytest.raises(ValueError):
            AutonomousGatePolicy(minimum_score=0.95, autonomous_score=0.90)

    def test_custom_policy_can_raise_bar_for_sensitive_collisions(self):
        policy = AutonomousGatePolicy(minimum_score=0.97, autonomous_score=0.985)
        result = AutonomousCollisionApprovalGate(policy).evaluate("collision-014", _scores(0.98))
        assert result.decision is GateDecision.MANUAL_REVIEW

    def test_mapping_input_matches_dataclass_input(self):
        gate = AutonomousCollisionApprovalGate()
        scores = _scores().as_mapping()
        as_object = gate.evaluate("collision-015", _scores())
        as_mapping = gate.evaluate("collision-015", scores)
        assert as_object.decision is as_mapping.decision
        assert as_object.receipt_sha256 == as_mapping.receipt_sha256
