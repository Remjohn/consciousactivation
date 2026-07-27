from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope
from ccp_studio.contracts.roles import RoleKey
from ccp_studio.services.command_bus import create_in_memory_command_bus
from ccp_studio.services.role_policy import (
    RolePolicyError,
    RolePolicyService,
    register_role_command_handlers,
)


def _role_fixture():
    role_policy = RolePolicyService()
    bus = create_in_memory_command_bus()
    register_role_command_handlers(bus, role_policy)
    org_id = uuid4()
    brand_id = uuid4()
    owner_id = uuid4()
    bus.brands.add_scope(org_id, brand_id)
    role_policy.bootstrap_owner(
        actor_id=owner_id,
        organization_id=org_id,
        brand_id=brand_id,
    )
    return role_policy, bus, org_id, brand_id, owner_id


def _actor(actor_id):
    return ActorContext(
        actor_id=actor_id,
        actor_type=ActorType.human,
        role_ids=[],
    )


def _assign_role(bus, org_id, brand_id, owner_id, target_id, role_key: RoleKey):
    envelope = new_command_envelope(
        command_type="AssignRoleCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor(owner_id),
        payload={
            "target_actor_id": str(target_id),
            "role_key": role_key.value,
        },
    )
    result = bus.submit(envelope)
    assert result.status == CommandStatus.succeeded
    return result


def test_assign_role_command_derives_permission_from_active_scoped_assignment():
    role_policy, bus, org_id, brand_id, owner_id = _role_fixture()
    operator_id = uuid4()

    result = _assign_role(bus, org_id, brand_id, owner_id, operator_id, RoleKey.operator)
    decision = role_policy.evaluate(
        actor_id=operator_id,
        command_type="StartProductionCommand",
        organization_id=org_id,
        brand_id=brand_id,
        source_surface="pwa",
    )

    assert result.result_payload["role_key"] == "operator"
    assert decision.allowed is True
    assert decision.decision_code == "PERMISSION_ALLOWED"
    assert decision.matched_role_assignment_ids


def test_operator_publishing_approval_is_denied_by_command_bus_policy():
    _role_policy, bus, org_id, brand_id, owner_id = _role_fixture()
    operator_id = uuid4()
    _assign_role(bus, org_id, brand_id, owner_id, operator_id, RoleKey.operator)
    approve = new_command_envelope(
        command_type="ApprovePublishingCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor(operator_id),
    )

    result = bus.submit(approve)

    assert result.status == CommandStatus.rejected
    assert any(item.code == "PERMISSION_DENIED" for item in result.validation_results)


def test_migration_steward_approval_records_required_receipt_fields():
    role_policy, bus, org_id, brand_id, owner_id = _role_fixture()
    steward_id = uuid4()
    _assign_role(bus, org_id, brand_id, owner_id, steward_id, RoleKey.migration_steward)

    receipt = role_policy.approve_migration_registry_entry(
        reviewer_actor_id=steward_id,
        organization_id=org_id,
        brand_id=brand_id,
        source_hash="sha256:legacy-source",
        target_contract="ccp_studio.contracts.skills.SkillInvocationRecord",
        fixture_target="fixtures/migration/expression_extraction.json",
        eval_target="evals/source_truth_eval",
    )

    assert receipt.source_hash == "sha256:legacy-source"
    assert receipt.target_contract.endswith("SkillInvocationRecord")
    assert receipt.fixture_target
    assert receipt.eval_target

    with pytest.raises(RolePolicyError) as exc:
        role_policy.approve_migration_registry_entry(
            reviewer_actor_id=steward_id,
            organization_id=org_id,
            brand_id=brand_id,
            source_hash="",
            target_contract="contract",
            fixture_target="fixture",
            eval_target="eval",
        )
    assert exc.value.code == "MIGRATION_RECEIPT_INCOMPLETE"


def test_telegram_and_pwa_permission_decisions_are_identical():
    role_policy, bus, org_id, brand_id, owner_id = _role_fixture()
    reviewer_id = uuid4()
    _assign_role(bus, org_id, brand_id, owner_id, reviewer_id, RoleKey.reviewer)

    pwa = role_policy.evaluate(
        actor_id=reviewer_id,
        command_type="SubmitReviewCommand",
        organization_id=org_id,
        brand_id=brand_id,
        source_surface="pwa",
    )
    telegram = role_policy.evaluate(
        actor_id=reviewer_id,
        command_type="SubmitReviewCommand",
        organization_id=org_id,
        brand_id=brand_id,
        source_surface="telegram",
    )

    assert pwa.allowed == telegram.allowed == True
    assert pwa.decision_code == telegram.decision_code


def test_revoked_role_denies_previously_valid_action_immediately():
    role_policy, bus, org_id, brand_id, owner_id = _role_fixture()
    approver_id = uuid4()
    assign_result = _assign_role(bus, org_id, brand_id, owner_id, approver_id, RoleKey.publishing_approver)
    role_assignment_id = assign_result.result_payload["role_assignment_id"]
    before = role_policy.evaluate(
        actor_id=approver_id,
        command_type="ApprovePublishingCommand",
        organization_id=org_id,
        brand_id=brand_id,
        source_surface="pwa",
    )
    revoke = new_command_envelope(
        command_type="RevokeRoleCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=_actor(owner_id),
        payload={"role_assignment_id": role_assignment_id},
    )

    revoked_result = bus.submit(revoke)
    after = role_policy.evaluate(
        actor_id=approver_id,
        command_type="ApprovePublishingCommand",
        organization_id=org_id,
        brand_id=brand_id,
        source_surface="pwa",
    )

    assert before.allowed is True
    assert revoked_result.status == CommandStatus.succeeded
    assert after.allowed is False
    assert after.decision_code == "ROLE_REVOKED"


@pytest.mark.parametrize(
    ("role_key", "allowed_command", "blocked_command"),
    [
        (RoleKey.operator, "StartProductionCommand", "ApprovePublishingCommand"),
        (RoleKey.reviewer, "SubmitReviewCommand", "UpdateCommercialPolicyCommand"),
        (RoleKey.publishing_approver, "ApprovePublishingCommand", "UpdateCommercialPolicyCommand"),
        (RoleKey.commercial_administrator, "UpdateCommercialPolicyCommand", "ApprovePublishingCommand"),
        (RoleKey.service_actor, "RunServiceWorkflowCommand", "ApprovePublishingCommand"),
    ],
)
def test_role_matrix_has_allowed_and_blocked_command(role_key, allowed_command, blocked_command):
    role_policy, bus, org_id, brand_id, owner_id = _role_fixture()
    actor_id = uuid4()
    _assign_role(bus, org_id, brand_id, owner_id, actor_id, role_key)

    allowed = role_policy.evaluate(
        actor_id=actor_id,
        command_type=allowed_command,
        organization_id=org_id,
        brand_id=brand_id,
        source_surface="internal",
    )
    blocked = role_policy.evaluate(
        actor_id=actor_id,
        command_type=blocked_command,
        organization_id=org_id,
        brand_id=brand_id,
        source_surface="internal",
    )

    assert allowed.allowed is True
    assert blocked.allowed is False
