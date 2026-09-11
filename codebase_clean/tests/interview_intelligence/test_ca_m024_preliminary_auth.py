"""CA-M024 executable evidence for preliminary authorization policy."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SERVICE_SRC = Path(__file__).parents[2] / "services" / "interview-intelligence" / "src"
sys.path.insert(0, str(SERVICE_SRC))

from cae_interview_intelligence.preliminary_auth import (  # noqa: E402
    AuthorizationDecision,
    GapCode,
    InvalidPolicyError,
    PreliminaryAuthPolicy,
    PreliminaryAuthorizationBlocked,
    PreliminaryExecutionRequest,
    PolicyMode,
    ResourceQuota,
    authorize_preliminary_execution,
    evaluate_preliminary_auth,
    gate_preliminary_execution,
)


@pytest.fixture
def policy() -> PreliminaryAuthPolicy:
    return PreliminaryAuthPolicy(
        policy_id="test-preflight",
        mode=PolicyMode.CHECKPOINT,
        allowed_permissions=frozenset({"INTERVIEW_EXPLORE", "INTERVIEW_DRAFT", "PIPELINE_NON_PRODUCTION"}),
        quotas=ResourceQuota(
            max_tokens=10_000,
            max_wall_seconds=300,
            max_cost_units=1_000,
            max_concurrent_runs=2,
        ),
    )


def request(**overrides) -> PreliminaryExecutionRequest:
    values = {
        "execution_id": "exec-001",
        "actor_id": "operator-001",
        "authenticated": True,
        "execution_kind": "EXPLORATORY",
        "permission": "INTERVIEW_EXPLORE",
        "requested_tokens": 100,
        "requested_wall_seconds": 10,
        "requested_cost_units": 10,
    }
    values.update(overrides)
    return PreliminaryExecutionRequest(**values)


def test_positive_exploratory_preflight_is_allowed(policy):
    result = evaluate_preliminary_auth(request(), policy)
    assert result.allowed is True
    assert result.report.decision is AuthorizationDecision.ALLOW
    assert result.report.gaps == ()


def test_positive_drafting_preflight_is_allowed(policy):
    result = evaluate_preliminary_auth(
        request(execution_kind="DRAFTING", permission="INTERVIEW_DRAFT"), policy
    )
    assert result.allowed is True


def test_positive_non_production_preflight_is_allowed(policy):
    result = evaluate_preliminary_auth(
        request(execution_kind="NON_PRODUCTION", permission="PIPELINE_NON_PRODUCTION"), policy
    )
    assert result.allowed is True


def test_unauthenticated_actor_is_denied_even_with_valid_permission(policy):
    result = evaluate_preliminary_auth(request(authenticated=False), policy)
    assert result.allowed is False
    assert result.report.gaps[0].code == GapCode.UNAUTHENTICATED.value


def test_wrong_permission_is_denied(policy):
    result = evaluate_preliminary_auth(request(permission="INTERVIEW_DRAFT"), policy)
    assert result.allowed is False
    assert any(g.code == GapCode.PERMISSION_MISSING.value for g in result.report.gaps)


def test_policy_permission_must_include_required_capability(policy):
    restrictive = PreliminaryAuthPolicy(
        policy_id="restrictive",
        allowed_permissions=frozenset({"INTERVIEW_DRAFT"}),
        quotas=policy.quotas,
    )
    result = evaluate_preliminary_auth(request(), restrictive)
    assert result.allowed is False
    assert result.report.gaps[0].code == GapCode.PERMISSION_MISSING.value


@pytest.mark.parametrize(
    "overrides,expected_code",
    [
        ({"requested_tokens": 10_001}, GapCode.TOKEN_QUOTA_EXCEEDED),
        ({"requested_wall_seconds": 301}, GapCode.TIME_QUOTA_EXCEEDED),
        ({"requested_cost_units": 1_001}, GapCode.COST_QUOTA_EXCEEDED),
        ({"request_concurrent_runs": 3}, GapCode.CONCURRENCY_QUOTA_EXCEEDED),
    ],
)
def test_each_resource_quota_is_hard_gated(policy, overrides, expected_code):
    # Existing usage is zero; the request itself crosses exactly one hard bound.
    result = evaluate_preliminary_auth(request(**overrides), policy)
    assert result.allowed is False
    assert expected_code.value in {g.code for g in result.report.gaps}


def test_multiple_quota_and_permission_gaps_are_structured(policy):
    result = evaluate_preliminary_auth(
        request(
            authenticated=False,
            permission="WRONG",
            requested_tokens=20_000,
            requested_wall_seconds=1_000,
            requested_cost_units=2_000,
            request_concurrent_runs=3,
        ),
        policy,
    )
    codes = {gap.code for gap in result.report.gaps}
    assert codes == {
        GapCode.UNAUTHENTICATED.value,
        GapCode.PERMISSION_MISSING.value,
        GapCode.TOKEN_QUOTA_EXCEEDED.value,
        GapCode.TIME_QUOTA_EXCEEDED.value,
        GapCode.COST_QUOTA_EXCEEDED.value,
        GapCode.CONCURRENCY_QUOTA_EXCEEDED.value,
    }
    assert all(set(gap.to_dict()) == {"code", "control", "message", "observed", "required"} for gap in result.report.gaps)


def test_production_execution_is_denied_fail_closed(policy):
    result = evaluate_preliminary_auth(request(production=True), policy)
    assert result.allowed is False
    assert GapCode.PRODUCTION_EXECUTION_FORBIDDEN.value in {g.code for g in result.report.gaps}


def test_policy_cannot_enable_production(policy):
    with pytest.raises(InvalidPolicyError, match="production"):
        PreliminaryAuthPolicy(
            policy_id="bad",
            allow_production=True,
            quotas=policy.quotas,
        )


def test_mapping_input_uses_same_real_evaluation_boundary(policy):
    result = evaluate_preliminary_auth(
        {
            "execution_id": "exec-map",
            "actor_id": "operator-002",
            "authenticated": True,
            "execution_kind": "drafting",
            "permission": "interview_draft",
            "requested_tokens": 100,
            "requested_wall_seconds": 5,
            "requested_cost_units": 5,
        },
        policy,
    )
    assert result.allowed is True
    assert result.report.execution_kind == "DRAFTING"


def test_receipt_is_deterministic_for_same_policy_and_request(policy):
    first = authorize_preliminary_execution(request(), policy)
    second = authorize_preliminary_execution(request(), policy)
    assert first.to_dict() == second.to_dict()
    assert len(first.receipt_sha256) == 64


def test_policy_hash_changes_when_quota_changes(policy):
    changed = PreliminaryAuthPolicy(
        policy_id=policy.policy_id,
        policy_version=policy.policy_version,
        mode=policy.mode,
        allowed_permissions=policy.allowed_permissions,
        quotas=ResourceQuota(
            max_tokens=10_001,
            max_wall_seconds=300,
            max_cost_units=1_000,
            max_concurrent_runs=2,
        ),
    )
    assert policy.policy_sha256 != changed.policy_sha256


def test_false_proof_valid_names_alone_do_not_authorize(policy):
    result = evaluate_preliminary_auth(
        {
            "execution_id": "spoofed",
            "actor_id": "spoofed",
            "authenticated": False,
            "execution_kind": "EXPLORATORY",
            "permission": "INTERVIEW_EXPLORE",
            "requested_tokens": 1,
        },
        policy,
    )
    assert result.allowed is False
    assert result.report.gaps[0].code == GapCode.UNAUTHENTICATED.value


def test_gate_never_calls_downstream_on_denial(policy):
    calls: list[str] = []

    def downstream():
        calls.append("executed")
        return "unsafe"

    with pytest.raises(PreliminaryAuthorizationBlocked):
        gate_preliminary_execution(request(requested_tokens=20_000), policy, downstream)
    assert calls == []


def test_gate_calls_downstream_after_success(policy):
    calls: list[str] = []

    def downstream():
        calls.append("executed")
        return "drafted"

    assert gate_preliminary_execution(request(), policy, downstream) == "drafted"
    assert calls == ["executed"]
