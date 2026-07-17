from __future__ import annotations

import pytest

from cmf_builder.domain.category_runtime_rules import (
    CategoryPolicyError,
    compile_category_operating_rules,
)


def test_category_local_repair_and_selective_rerun_are_accepted(
    policy_source_factory,
) -> None:
    rules = compile_category_operating_rules(
        policy_source_factory("short_form_edited_video")
    )
    rules.validate_repair_request(
        category_id="short_form_edited_video",
        repair_unit="time_state_unit",
        evaluator_owner_id=rules.evaluator_owner_ref.object_id,
        repair_owner_id=rules.repair_owner_ref.object_id,
    )
    rules.validate_selective_rerun(
        category_id="short_form_edited_video",
        affected_units=("time_state_unit", "reading_order_unit"),
    )


@pytest.mark.parametrize(
    ("category_id", "unit", "match"),
    [
        ("carousels", "time_state_unit", "Cross-category"),
        ("short_form_edited_video", "performance_unit", "not category-owned"),
    ],
)
def test_cross_category_or_unowned_repair_fails(
    policy_source_factory, category_id, unit, match
) -> None:
    rules = compile_category_operating_rules(
        policy_source_factory("short_form_edited_video")
    )
    with pytest.raises(CategoryPolicyError, match=match):
        rules.validate_repair_request(
            category_id=category_id,
            repair_unit=unit,
            evaluator_owner_id=rules.evaluator_owner_ref.object_id,
            repair_owner_id=rules.repair_owner_ref.object_id,
        )


def test_missing_evaluator_or_repair_ownership_fails(policy_source_factory) -> None:
    rules = compile_category_operating_rules(policy_source_factory("supervisuals"))
    with pytest.raises(CategoryPolicyError, match="Evaluator ownership"):
        rules.validate_repair_request(
            category_id="supervisuals",
            repair_unit="hierarchy_unit",
            evaluator_owner_id="wrong-owner",
            repair_owner_id=rules.repair_owner_ref.object_id,
        )
    with pytest.raises(CategoryPolicyError, match="Repair ownership"):
        rules.validate_repair_request(
            category_id="supervisuals",
            repair_unit="hierarchy_unit",
            evaluator_owner_id=rules.evaluator_owner_ref.object_id,
            repair_owner_id="wrong-owner",
        )


def test_same_category_new_version_migration_is_allowed(policy_source_factory) -> None:
    rules = compile_category_operating_rules(
        policy_source_factory("2d_character_animation")
    )
    rules.validate_migration(
        target_category_id="2d_character_animation",
        target_profile_id="format02_minimal_coach_theatre",
        target_ruleset_version="2.0.0",
        inherit_certification=False,
        transfer_atomic_ownership=False,
    )


@pytest.mark.parametrize(
    ("category", "profile", "version", "inherit", "transfer", "match"),
    [
        ("carousels", None, "2.0.0", False, False, "Cross-category"),
        (
            "2d_character_animation",
            "format01_story_video",
            "2.0.0",
            False,
            False,
            "not owned",
        ),
        (
            "2d_character_animation",
            "format02_minimal_coach_theatre",
            "1.0.0",
            False,
            False,
            "new immutable",
        ),
        (
            "2d_character_animation",
            "format02_minimal_coach_theatre",
            "2.0.0",
            True,
            False,
            "Certification",
        ),
        (
            "2d_character_animation",
            "format02_minimal_coach_theatre",
            "2.0.0",
            False,
            True,
            "ownership",
        ),
    ],
)
def test_incompatible_migration_and_ownership_transfer_fail(
    policy_source_factory, category, profile, version, inherit, transfer, match
) -> None:
    rules = compile_category_operating_rules(
        policy_source_factory("2d_character_animation")
    )
    with pytest.raises(CategoryPolicyError, match=match):
        rules.validate_migration(
            target_category_id=category,
            target_profile_id=profile,
            target_ruleset_version=version,
            inherit_certification=inherit,
            transfer_atomic_ownership=transfer,
        )


def test_invalidation_and_rollback_rules_are_explicit(policy_source_factory) -> None:
    rules = compile_category_operating_rules(policy_source_factory("carousels"))
    assert "category_native_syntax_hash_changed" in rules.invalidation_triggers
    assert "activative_sequence_hash_changed" in rules.invalidation_triggers
    assert "never_mutate_predecessor_artifacts" in rules.rollback_policy
    assert "preserve_historical_ruleset_bytes" in rules.rollback_policy
