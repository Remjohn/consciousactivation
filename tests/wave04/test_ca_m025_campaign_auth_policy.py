"""CA-M025 production campaign authorization policy tests.

These tests exercise the real policy evaluator boundary, not a parser or a
mocked downstream call.
"""

from __future__ import annotations

import pytest

from ca_runtime.campaign_auth_policy import (
    AuthorizationDecision,
    CampaignAuthorizationPolicy,
    CampaignAuthorizationPolicyEngine,
    CampaignExecutionRequest,
    DenialReasonCode,
    InvalidPolicyError,
    authorize_campaign_execution,
)


POLICY = CampaignAuthorizationPolicy.production_default(
    budget_limit_units=1_000,
    max_run_spend_units=700,
    policy_id="campaign-prod",
    policy_version="1.0.0",
)


def request(**overrides):
    values = {
        "campaign_id": "camp-001",
        "actor_id": "operator-001",
        "actor_role": "OPERATOR",
        "authenticated": True,
        "campaign_tier": "PRODUCTION",
        "estimated_spend_units": 100,
        "spend_to_date_units": 200,
    }
    values.update(overrides)
    return CampaignExecutionRequest(**values)


def test_authorize_production_run_for_authenticated_operator_within_budget():
    engine = CampaignAuthorizationPolicyEngine(POLICY)

    receipt = engine.evaluate(request(), now_utc="2026-09-08T08:00:00Z")

    assert receipt.decision is AuthorizationDecision.ALLOW
    assert receipt.allowed is True
    assert receipt.reason_code == "AUTHORIZED"
    assert receipt.campaign_id == "camp-001"
    assert receipt.policy_id == "campaign-prod"
    assert receipt.policy_sha256 == POLICY.policy_sha256
    assert receipt.remaining_budget_units == 800
    assert receipt.non_waivable_controls
    assert "SPEND_WITHIN_BUDGET" in receipt.non_waivable_controls


@pytest.mark.parametrize("role", ["COMMANDER", "OPERATOR"])
def test_production_control_roles_are_authorized(role):
    receipt = authorize_campaign_execution(
        request(actor_role=role),
        POLICY,
        now_utc="2026-09-08T08:01:00Z",
    )
    assert receipt.allowed is True


def test_rejects_authenticated_non_control_role():
    receipt = CampaignAuthorizationPolicyEngine(POLICY).evaluate(
        request(actor_role="COMPOSER"),
        now_utc="2026-09-08T08:02:00Z",
    )

    assert receipt.allowed is False
    assert receipt.reason_code == DenialReasonCode.ROLE_NOT_AUTHORIZED.value
    assert "COMPOSER" in receipt.message
    assert receipt.details["control"] == "AUTHORIZED_ROLE"
    assert receipt.receipt_id


def test_rejects_unauthenticated_production_execution_with_descriptive_receipt():
    receipt = CampaignAuthorizationPolicyEngine(POLICY).evaluate(
        request(authenticated=False),
        now_utc="2026-09-08T08:03:00Z",
    )

    assert receipt.allowed is False
    assert receipt.reason_code == DenialReasonCode.UNAUTHENTICATED_EXECUTION.value
    assert "not authenticated" in receipt.message
    assert receipt.details["control"] == "AUTHENTICATED_ACTOR"
    assert receipt.receipt_id
    assert receipt.actor_id == "operator-001"


@pytest.mark.parametrize(
    "tier",
    ["DEVELOPMENT", "STAGING"],
)
def test_rejects_non_production_tiers(tier):
    receipt = CampaignAuthorizationPolicyEngine(POLICY).evaluate(
        request(campaign_tier=tier),
        now_utc="2026-09-08T08:04:00Z",
    )

    assert receipt.allowed is False
    assert receipt.reason_code == DenialReasonCode.TIER_NOT_ALLOWED.value
    assert receipt.details["required_tier"] == "PRODUCTION"
    assert receipt.details["actual_tier"] == tier


def test_rejects_when_cumulative_spend_would_exceed_campaign_budget():
    receipt = CampaignAuthorizationPolicyEngine(POLICY).evaluate(
        request(estimated_spend_units=101, spend_to_date_units=900),
        now_utc="2026-09-08T08:05:00Z",
    )

    assert receipt.allowed is False
    assert receipt.reason_code == DenialReasonCode.SPEND_BUDGET_EXCEEDED.value
    assert "remaining campaign budget 100 units" in receipt.message
    assert receipt.remaining_budget_units == 100
    assert receipt.details["control"] == "SPEND_WITHIN_BUDGET"


def test_rejects_when_single_run_spend_threshold_is_exceeded():
    receipt = CampaignAuthorizationPolicyEngine(POLICY).evaluate(
        request(estimated_spend_units=701, spend_to_date_units=0),
        now_utc="2026-09-08T08:06:00Z",
    )

    assert receipt.allowed is False
    assert receipt.reason_code == DenialReasonCode.SPEND_BUDGET_EXCEEDED.value
    assert "per-run spend threshold 700 units" in receipt.message
    assert receipt.details["max_run_spend_units"] == 700


def test_rejects_negative_spend_fail_closed():
    receipt = CampaignAuthorizationPolicyEngine(POLICY).evaluate(
        request(estimated_spend_units=-1),
        now_utc="2026-09-08T08:07:00Z",
    )

    assert receipt.allowed is False
    assert receipt.reason_code == DenialReasonCode.INVALID_SPEND_AMOUNT.value
    assert "cannot be negative" in receipt.message


def test_mapping_input_uses_same_canonical_evaluator_boundary():
    receipt = CampaignAuthorizationPolicyEngine(POLICY).evaluate(
        {
            "campaign_id": "camp-002",
            "actor_id": "commander-001",
            "actor_role": "commander",
            "authenticated": True,
            "campaign_tier": "production",
            "estimated_spend_units": 250,
            "spend_to_date_units": 100,
            "requested_operation": "execute",
        },
        now_utc="2026-09-08T08:08:00Z",
    )

    assert receipt.allowed is True
    assert receipt.actor_role == "COMMANDER"
    assert receipt.campaign_tier == "PRODUCTION"
    assert receipt.remaining_budget_units == 900


def test_invalid_policy_cannot_be_used_as_a_silent_less_restrictive_fallback():
    with pytest.raises(InvalidPolicyError):
        CampaignAuthorizationPolicy(
            budget_limit_units=1_000,
            authorized_roles={"COMPOSER"},
            production_tier="STAGING",
        )


def test_false_proof_countercase_role_and_tier_strings_alone_do_not_authorize():
    """Contrastive failure: names that look valid are insufficient without auth.

    A parser/string-only implementation could incorrectly pass because the role
    and tier values look correct. The real boundary must still deny an
    unauthenticated request.
    """
    receipt = CampaignAuthorizationPolicyEngine(POLICY).evaluate(
        {
            "campaign_id": "camp-003",
            "actor_id": "spoofed",
            "actor_role": "OPERATOR",
            "authenticated": False,
            "campaign_tier": "PRODUCTION",
            "estimated_spend_units": 10,
            "spend_to_date_units": 0,
        },
        now_utc="2026-09-08T08:09:00Z",
    )

    assert receipt.allowed is False
    assert receipt.reason_code == DenialReasonCode.UNAUTHENTICATED_EXECUTION.value


def test_receipt_identity_is_deterministic_for_same_evaluation_inputs():
    engine = CampaignAuthorizationPolicyEngine(POLICY)
    req = request()

    first = engine.evaluate(req, now_utc="2026-09-08T08:10:00Z")
    second = engine.evaluate(req, now_utc="2026-09-08T08:10:00Z")

    assert first.receipt_id == second.receipt_id
    assert first.policy_sha256 == second.policy_sha256


def test_policy_identity_changes_when_budget_threshold_changes():
    lower = CampaignAuthorizationPolicy.production_default(
        budget_limit_units=900,
        max_run_spend_units=700,
        policy_id="campaign-prod",
        policy_version="1.0.0",
    )
    assert lower.policy_sha256 != POLICY.policy_sha256


def test_receipts_are_descriptive_for_over_budget_denial():
    receipt = CampaignAuthorizationPolicyEngine(POLICY).evaluate(
        request(estimated_spend_units=500, spend_to_date_units=600),
        now_utc="2026-09-08T08:11:00Z",
    )

    assert receipt.allowed is False
    assert receipt.denial_reason == DenialReasonCode.SPEND_BUDGET_EXCEEDED.value
    assert receipt.to_dict()["decision"] == "DENY"
    assert receipt.to_dict()["budget_limit_units"] == 1_000
    assert receipt.to_dict()["remaining_budget_units"] == 400
    assert receipt.to_dict()["estimated_spend_units"] == 500


def test_production_tier_is_a_hard_constraint_even_for_commanders():
    receipt = CampaignAuthorizationPolicyEngine(POLICY).evaluate(
        request(
            actor_role="COMMANDER",
            campaign_tier="STAGING",
            estimated_spend_units=1,
        ),
        now_utc="2026-09-08T08:12:00Z",
    )

    assert receipt.allowed is False
    assert receipt.reason_code == DenialReasonCode.TIER_NOT_ALLOWED.value
