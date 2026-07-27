import pytest

from cmf_builder.workflow.profile_lifecycle import (
    ActorType,
    LifecycleAction,
    ProfileAuthority,
    ProfileLifecycleState,
    WorkflowProfileLifecycleError,
    WorkflowProfileVersion,
    apply_hotfix,
    invalidate_profile,
    migrate_profile,
    promote_development,
    request_promotion,
    rollback_profile,
)


def authority(actor=ActorType.HUMAN, actions=None):
    return ProfileAuthority(
        "authority:od-am-002",
        "a" * 64,
        actor,
        tuple(actions or list(LifecycleAction)),
        ("OD-AM-002", "offline_development"),
    )


def profile(**overrides):
    values = {
        "profile_id": "workflow-profile:category-native-v1",
        "version": "1.0.0",
        "state": ProfileLifecycleState.DEVELOPMENT_VALIDATED,
        "workflow_graph_identity": "workflow-graph:sha256:1",
        "compatibility_evidence_refs": ("compatibility:local-fixture",),
        "migration_evidence_refs": (),
        "predecessor_profile_identity": None,
        "supersedes_profile_identity": None,
        "rollback_target_identity": None,
        "authority_identity": authority().authority_identity,
        "evidence_refs": ("receipt:st-09.06",),
    }
    values.update(overrides)
    return WorkflowProfileVersion(**values)


def test_profile_promotion_requires_human_authority_and_stays_development_only():
    pending, pending_receipt = request_promotion(profile(), authority())
    promoted, receipt = promote_development(pending, authority())

    assert pending.state is ProfileLifecycleState.PROMOTION_PENDING
    assert promoted.state is ProfileLifecycleState.PROMOTED_DEVELOPMENT
    assert promoted.production_ready is False
    assert promoted.certified is False
    assert pending_receipt.receipt_identity
    assert "production_deployment" in receipt.excluded_scope


def test_agent_cannot_promote_or_impersonate_human_authority():
    with pytest.raises(WorkflowProfileLifecycleError) as exc:
        request_promotion(profile(), authority(actor=ActorType.GOVERNED_AGENT))

    assert exc.value.code == "HUMAN_AUTHORITY_REQUIRED"


def test_migration_creates_new_immutable_profile_with_lineage():
    original = profile()
    migrated, receipt = migrate_profile(original, "1.1.0", ("migration:contract-proof",), authority(actions=(LifecycleAction.MIGRATE,)))

    assert migrated.profile_identity != original.profile_identity
    assert migrated.predecessor_profile_identity == original.profile_identity
    assert migrated.supersedes_profile_identity == original.profile_identity
    assert migrated.migration_evidence_refs == ("migration:contract-proof",)
    assert receipt.resulting_profile_identity == migrated.profile_identity


def test_rollback_requires_exact_governed_target():
    original = profile()
    migrated, _ = migrate_profile(original, "1.1.0", ("migration:contract-proof",), authority(actions=(LifecycleAction.MIGRATE,)))

    rolled_back, receipt = rollback_profile(migrated, original, authority(actions=(LifecycleAction.ROLLBACK,)))
    assert rolled_back.rollback_target_identity == original.profile_identity
    assert rolled_back.state is ProfileLifecycleState.ROLLED_BACK
    assert receipt.receipt_identity

    unrelated = profile(profile_id="workflow-profile:other")
    with pytest.raises(WorkflowProfileLifecycleError) as exc:
        rollback_profile(migrated, unrelated, authority(actions=(LifecycleAction.ROLLBACK,)))
    assert exc.value.code == "ROLLBACK_TARGET_MISMATCH"


def test_hotfix_preserves_history_and_does_not_rewrite_original_profile():
    original = profile()
    fixed, receipt = apply_hotfix(original, "001", ("hotfix:test-only",), authority(actions=(LifecycleAction.APPLY_HOTFIX,)))

    assert fixed.profile_identity != original.profile_identity
    assert fixed.supersedes_profile_identity == original.profile_identity
    assert fixed.predecessor_profile_identity == original.profile_identity
    assert original.state is ProfileLifecycleState.DEVELOPMENT_VALIDATED
    assert receipt.receipt_identity


def test_invalidation_records_descendants_and_blocks_hotfix_afterwards():
    invalidated, receipt = invalidate_profile(profile(), ("node-output:1", "run-index:1"), authority(actions=(LifecycleAction.INVALIDATE,)))

    assert invalidated.state is ProfileLifecycleState.INVALIDATED
    assert invalidated.invalidated_descendants == ("node-output:1", "run-index:1")
    assert receipt.receipt_identity

    with pytest.raises(WorkflowProfileLifecycleError) as exc:
        apply_hotfix(invalidated, "002", ("hotfix:late",), authority(actions=(LifecycleAction.APPLY_HOTFIX,)))
    assert exc.value.code == "INVALIDATED_PROFILE_CANNOT_HOTFIX"


def test_false_production_or_certification_claims_fail_closed():
    with pytest.raises(WorkflowProfileLifecycleError) as exc:
        profile(production_ready=True)
    assert exc.value.code == "FALSE_READINESS_CLAIM"

    with pytest.raises(WorkflowProfileLifecycleError) as auth_exc:
        ProfileAuthority("authority:bad", "b" * 64, ActorType.HUMAN, (LifecycleAction.PROMOTE_DEVELOPMENT,), ("scope",), production_authority=True)
    assert auth_exc.value.code == "PRODUCTION_OR_CERTIFICATION_AUTHORITY_PROHIBITED"
