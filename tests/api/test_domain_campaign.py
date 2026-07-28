"""Pure unit tests for api/domain/campaign.py — no FastAPI, no database.

Covers AC-006 (FORMAT02_DEFERRED), AC-007 (OUTPUT_TARGET_REQUIRED),
AC-008 (INVALID_INTEGER), plus state-machine and ID-minting tests.
"""

from __future__ import annotations
import pytest
from api.domain.campaign import (
    CampaignValidationError,
    create_campaign_order,
    default_autonomy_policy,
    deterministic_id,
    launch_campaign,
    transition_campaign,
    validate_campaign_order,
    ALLOWED_TRANSITIONS,
)


# ---------------------------------------------------------------------------
# deterministic_id
# ---------------------------------------------------------------------------

def test_deterministic_id_format():
    result = deterministic_id("campaign-order", {"workspace_id": "ws-1"})
    assert result.startswith("campaign-order:")
    assert len(result) == len("campaign-order:") + 24


def test_deterministic_id_stable():
    payload = {"workspace_id": "ws-1", "objective": "same"}
    a = deterministic_id("campaign", payload)
    b = deterministic_id("campaign", payload)
    assert a == b


def test_deterministic_id_prefix_rejects_invalid():
    with pytest.raises(CampaignValidationError) as exc_info:
        deterministic_id("bad prefix!", {})
    assert exc_info.value.code == "INVALID_ID_PREFIX"


# ---------------------------------------------------------------------------
# validate_campaign_order
# ---------------------------------------------------------------------------

def _minimal_order():
    return {
        "workspace_id": "ws-1", "project_id": "prj-1",
        "source_kind": "CANONICAL_INTERVIEW_SOURCE_PACKAGE",
        "source_ref": {"object_id": "src-1", "version": "1.0.0", "sha256": "a" * 64},
        "harness_ref": {"object_id": "hr-1", "version": "1.0.0", "sha256": "b" * 64},
        "category_id": "short_form_edited_video",
        "format_profile_id": "format07_direct_coaching_a_roll",
        "objective": "test objective",
        "initial_seed": "seed",
        "taste_direction": [],
        "output_targets": [{"output_type": "SOURCE_LED_SHORT", "quantity": 1, "profile_id": "p1"}],
        "budget_units": 100,
        "deadline_utc": None,
        "autonomy_policy": default_autonomy_policy("REVIEW_BEFORE_SHIP"),
        "operator_actor": {"actor_id": "op-1", "actor_type": "human", "product_id": "studio", "workflow_role": "operator"},
        "authority": {"authority_id": "a1", "authority_version": "1.0.0", "authority_sha256": "c" * 64, "authority_state": "candidate_not_current"},
    }


class TestValidateCampaignOrder:
    """AC-007, AC-008, AC-006 (unit half)."""

    def test_passes_minimal_valid(self):
        validate_campaign_order(_minimal_order())  # no raise

    def test_empty_workspace_rejected(self):
        o = _minimal_order()
        o["workspace_id"] = ""
        with pytest.raises(CampaignValidationError) as exc_info:
            validate_campaign_order(o)
        assert exc_info.value.code == "EMPTY_VALUE"

    def test_output_target_required(self):
        o = _minimal_order()
        o["output_targets"] = []
        with pytest.raises(CampaignValidationError) as exc_info:
            validate_campaign_order(o)
        assert exc_info.value.code == "OUTPUT_TARGET_REQUIRED"

    def test_budget_units_minimum(self):
        o = _minimal_order()
        o["budget_units"] = 0
        with pytest.raises(CampaignValidationError) as exc_info:
            validate_campaign_order(o)
        assert exc_info.value.code == "INVALID_INTEGER"

    def test_format02_category_deferred(self):
        o = _minimal_order()
        o["category_id"] = "2d_character_animation"
        with pytest.raises(CampaignValidationError) as exc_info:
            validate_campaign_order(o)
        assert exc_info.value.code == "FORMAT02_DEFERRED"

    def test_format02_profile_deferred(self):
        o = _minimal_order()
        o["format_profile_id"] = "format02_experimental"
        with pytest.raises(CampaignValidationError) as exc_info:
            validate_campaign_order(o)
        assert exc_info.value.code == "FORMAT02_DEFERRED"

    def test_invalid_sha256_rejected(self):
        o = _minimal_order()
        o["source_ref"]["sha256"] = "zzz"
        with pytest.raises(CampaignValidationError) as exc_info:
            validate_campaign_order(o)
        assert exc_info.value.code == "INVALID_SHA256"


# ---------------------------------------------------------------------------
# create_campaign_order / launch_campaign
# ---------------------------------------------------------------------------

class TestCreateAndLaunch:
    def test_create_mints_order_id(self):
        order = create_campaign_order(_minimal_order())
        assert order["order_id"].startswith("campaign-order:")

    def test_launch_produces_launched(self):
        order = create_campaign_order(_minimal_order())
        state = launch_campaign(order)
        assert state["lifecycle_state"] == "LAUNCHED"
        assert state["version"] == 1

    def test_launch_sets_campaign_id(self):
        order = create_campaign_order(_minimal_order())
        state = launch_campaign(order)
        assert state["campaign_id"].startswith("campaign:")


# ---------------------------------------------------------------------------
# transition_campaign
# ---------------------------------------------------------------------------

class TestTransitionCampaign:
    def _launched_state(self):
        order = create_campaign_order(_minimal_order())
        return launch_campaign(order)

    def test_cancel_from_launched(self):
        state = self._launched_state()
        new = transition_campaign(state, "CANCELLED")
        assert new["lifecycle_state"] == "CANCELLED"
        assert new["version"] == 2

    def test_cancel_twice_denied(self):
        state = self._launched_state()
        cancelled = transition_campaign(state, "CANCELLED")
        with pytest.raises(CampaignValidationError) as exc_info:
            transition_campaign(cancelled, "CANCELLED")
        assert exc_info.value.code == "CAMPAIGN_TRANSITION_DENIED"

    def test_shadow_cannot_ship(self):
        """SHADOW campaigns cannot reach SHIPPED.  Must be in READY_TO_SHIP
        (which allows SHIPPED) for the SHADOW check to fire."""
        order = create_campaign_order(_minimal_order())
        order["autonomy_policy"]["mode"] = "SHADOW"
        state = launch_campaign(order)
        # Manually set lifecycle_state to READY_TO_SHIP to pass the
        # allowed-transitions gate; the SHADOW check is evaluated after.
        state["lifecycle_state"] = "READY_TO_SHIP"
        with pytest.raises(CampaignValidationError) as exc_info:
            transition_campaign(state, "SHIPPED")
        assert exc_info.value.code == "SHADOW_CANNOT_SHIP"

    def test_run_transition_allowed_from_launched(self):
        """LAUNCHED → RUNNING is a valid transition per ALLOWED_TRANSITIONS."""
        state = self._launched_state()
        new = transition_campaign(state, "RUNNING")
        assert new["lifecycle_state"] == "RUNNING"

    @pytest.mark.parametrize("current,allowed", [
        ("DRAFT", ["LAUNCHED", "CANCELLED"]),
        ("LAUNCHED", ["RUNNING", "CANCELLED"]),
        ("RUNNING", ["AWAITING_REVIEW", "BLOCKED_EXCEPTION", "READY_TO_SHIP", "CANCELLED"]),
        ("CANCELLED", []),
        ("SHIPPED", []),
    ])
    def test_allowed_transitions(self, current, allowed):
        assert set(ALLOWED_TRANSITIONS.get(current, ())) == set(allowed)


# ---------------------------------------------------------------------------
# default_autonomy_policy
# ---------------------------------------------------------------------------

class TestDefaultAutonomyPolicy:
    def test_checkpointed_has_checkpoints(self):
        policy = default_autonomy_policy("CHECKPOINTED")
        assert policy["checkpoint_ids"] == ["final-script-approval", "final-artifact-review"]

    def test_autopilot_exception_only(self):
        policy = default_autonomy_policy("AUTOPILOT")
        assert policy["exception_only"] is True

    def test_review_before_ship_final_review_required(self):
        policy = default_autonomy_policy("REVIEW_BEFORE_SHIP")
        assert policy["final_review_required"] is True
