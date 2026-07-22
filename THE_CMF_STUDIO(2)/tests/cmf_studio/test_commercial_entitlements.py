from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope
from ccp_studio.contracts.commercial import EntitlementStatus, PublicContentOffer
from ccp_studio.contracts.roles import RoleKey
from ccp_studio.services.command_bus import create_in_memory_command_bus
from ccp_studio.services.commercial_policy_service import (
    CommercialPolicyError,
    CommercialPolicyService,
    register_commercial_command_handlers,
)
from ccp_studio.services.role_policy import RolePolicyService, register_role_command_handlers


def _actor(actor_id):
    return ActorContext(actor_id=actor_id, actor_type=ActorType.human, role_ids=[])


def _commercial_fixture(public_offer=PublicContentOffer.monthly_asset_engine, **policy):
    org_id = uuid4()
    brand_id = uuid4()
    owner_id = uuid4()
    operator_id = uuid4()
    commercial = CommercialPolicyService()
    roles = RolePolicyService()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    roles.bootstrap_owner(actor_id=owner_id, organization_id=org_id, brand_id=brand_id)
    roles.assign_role(
        assigner_actor_id=owner_id,
        target_actor_id=operator_id,
        organization_id=org_id,
        brand_id=brand_id,
        role_key=RoleKey.operator,
    )
    register_role_command_handlers(bus, roles)
    register_commercial_command_handlers(bus, commercial)
    entitlement = commercial.create_entitlement(
        organization_id=org_id,
        brand_id=brand_id,
        public_offer=public_offer,
        **policy,
    )
    return commercial, roles, bus, org_id, brand_id, owner_id, operator_id, entitlement


def _production_payload(**overrides):
    payload = {
        "source_lineage_ref": "source:session:1",
        "consent_receipt_id": "consent:1",
        "evaluation_receipt_required": True,
        "human_approval_required": True,
        "valid_format_key": "guest_asset_pack.clip",
        "provider_job_count": 1,
        "estimated_cost_cents": 150,
    }
    payload.update(overrides)
    return payload


def test_public_offer_copy_only_renders_documented_charges_and_blocks_drift():
    commercial = CommercialPolicyService()

    assert commercial.render_public_offer_copy(PublicContentOffer.trial_guest_asset_pack) == "$29/week trial Guest Asset Pack"
    assert commercial.render_public_offer_copy(PublicContentOffer.monthly_asset_engine) == "$99/month Monthly Asset Engine"
    with pytest.raises(CommercialPolicyError) as exc:
        commercial.render_public_offer_copy("credit_bundle")
    assert exc.value.code == "PUBLIC_OFFER_NOT_ALLOWED"

    with pytest.raises(CommercialPolicyError) as drift:
        commercial.validate_public_copy("$49 lite plan with newsletters and credits")
    assert drift.value.code == "PUBLIC_OFFER_DRIFT_BLOCKED"


def test_commercial_admin_can_create_entitlement_through_command_bus():
    org_id = uuid4()
    brand_id = uuid4()
    owner_id = uuid4()
    commercial = CommercialPolicyService()
    roles = RolePolicyService()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(org_id, brand_id)
    roles.bootstrap_owner(actor_id=owner_id, organization_id=org_id, brand_id=brand_id)
    register_role_command_handlers(bus, roles)
    register_commercial_command_handlers(bus, commercial)
    envelope = new_command_envelope(
        command_type="CreateCommercialEntitlementCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor(owner_id),
        payload={
            "public_offer": "trial_guest_asset_pack",
            "max_provider_jobs_per_period": 3,
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["public_offer"] == "trial_guest_asset_pack"
    assert commercial.repository.get_entitlement(org_id, brand_id) is not None


def test_expired_or_suspended_entitlement_blocks_new_production_with_cost_receipt():
    commercial, _roles, bus, org_id, brand_id, _owner_id, operator_id, _entitlement = _commercial_fixture()
    commercial.update_entitlement_status(
        organization_id=org_id,
        brand_id=brand_id,
        status=EntitlementStatus.expired,
    )
    envelope = new_command_envelope(
        command_type="StartProductionCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor(operator_id),
        payload=_production_payload(),
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.rejected
    assert any(item.code == "COMMERCIAL_ENTITLEMENT_EXPIRED" for item in result.validation_results)
    assert list(commercial.repository.cost_receipts.values())[0].policy_decision == "COMMERCIAL_ENTITLEMENT_EXPIRED"


def test_trial_and_monthly_entitlements_do_not_remove_lineage_review_consent_or_approval():
    for offer in [PublicContentOffer.trial_guest_asset_pack, PublicContentOffer.monthly_asset_engine]:
        commercial, _roles, bus, org_id, brand_id, _owner_id, operator_id, _entitlement = _commercial_fixture(offer)
        envelope = new_command_envelope(
            command_type="GenerateAssetPackageSpecCommand",
            organization_id=org_id,
            brand_id=brand_id,
            actor=_actor(operator_id),
            payload=_production_payload(human_approval_required=False),
        )

        result = bus.submit(envelope)

        assert result.status == CommandStatus.rejected
        assert any(item.code == "PRODUCTION_REQUIREMENTS_INCOMPLETE" for item in result.validation_results)
        assert list(commercial.repository.cost_receipts.values())[0].policy_decision == "PRODUCTION_REQUIREMENTS_INCOMPLETE"


def test_quota_exceeded_blocks_internal_usage_without_public_offer_drift():
    commercial, _roles, bus, org_id, brand_id, _owner_id, operator_id, entitlement = _commercial_fixture(
        max_provider_jobs_per_period=1
    )
    commercial.record_usage(
        organization_id=org_id,
        brand_id=brand_id,
        usage_type="provider_job",
        quantity=1,
    )
    envelope = new_command_envelope(
        command_type="SubmitProviderJobCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor(operator_id),
        payload=_production_payload(provider_job_count=1),
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.rejected
    assert any(item.code == "QUOTA_EXCEEDED" for item in result.validation_results)
    assert commercial.render_public_offer_copy(entitlement.public_offer) == "$99/month Monthly Asset Engine"


def test_cost_threshold_requires_manual_override_before_provider_work():
    commercial, _roles, bus, org_id, brand_id, _owner_id, operator_id, _entitlement = _commercial_fixture(
        manual_override_above_cents=100
    )
    blocked = new_command_envelope(
        command_type="QueueRenderCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor(operator_id),
        payload=_production_payload(estimated_cost_cents=250),
    )
    allowed_commercial_but_missing_handler = new_command_envelope(
        command_type="QueueRenderCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor(operator_id),
        payload=_production_payload(estimated_cost_cents=250, manual_override_approved=True),
    )

    blocked_result = bus.submit(blocked)
    allowed_result = bus.submit(allowed_commercial_but_missing_handler)

    assert blocked_result.status == CommandStatus.rejected
    assert any(item.code == "MANUAL_OVERRIDE_REQUIRED" for item in blocked_result.validation_results)
    assert any(item.code == "COST_QUOTA_POLICY" for item in allowed_result.validation_results)
    assert any(receipt.policy_decision == "COMMERCIAL_POLICY_ALLOWED" for receipt in commercial.repository.cost_receipts.values())
