from __future__ import annotations

import pytest

from cmf_builder.domain.category_runtime_rules import (
    NOT_APPLICABLE,
    RULESET_MATURITY,
    STRUCTURAL_COMPATIBILITY,
    compile_category_operating_rules,
)


@pytest.mark.parametrize(
    ("category_id", "runtime_requirement", "evaluation_dimension"),
    [
        ("short_form_edited_video", "ordered_time_state_plan", "temporal_coherence"),
        (
            "2d_character_animation",
            "character_performance_registry_plan",
            "performance_continuity",
        ),
        ("carousels", "slide_role_plan", "swipe_progression"),
        ("supervisuals", "single_frame_hierarchy_plan", "attention_hierarchy"),
        (
            "conversational_activation_expression",
            "turn_relationship_plan",
            "human_authority_preservation",
        ),
    ],
)
def test_each_category_compiles_owned_runtime_and_evaluation_rules(
    policy_source_factory, category_id, runtime_requirement, evaluation_dimension
) -> None:
    rules = compile_category_operating_rules(policy_source_factory(category_id))
    assert rules.category_id == rules.atomic_owner_category_id == category_id
    assert runtime_requirement in rules.runtime_plan_requirements
    assert evaluation_dimension in rules.evaluation_dimensions
    assert "category_identity_preservation" in rules.evaluation_dimensions
    assert rules.evaluator_owner_ref.lineage_role == "evaluation_owner"
    assert rules.repair_owner_ref.lineage_role == "repair_owner"
    assert rules.maturity_status == RULESET_MATURITY
    assert rules.compatibility_status == STRUCTURAL_COMPATIBILITY
    assert rules.production_ready is False
    assert rules.certified is False


def test_operating_rules_bind_exact_syntax_sequence_and_constitution(
    policy_source_factory,
) -> None:
    source = policy_source_factory("2d_character_animation")
    rules = compile_category_operating_rules(source)
    assert rules.syntax_hash == source.syntax.syntax_hash
    assert rules.sequence_hash == source.sequence.sequence_hash
    assert rules.category_constitution_version == "1.1"
    assert "syntax_and_sequence_hash_validity" in rules.validation_gates
    assert "animation_performance_not_edited_video_alias" in rules.validation_gates


def test_external_handoff_is_contract_only_and_validation_pending(
    policy_source_factory,
) -> None:
    rules = compile_category_operating_rules(
        policy_source_factory("conversational_activation_expression")
    )
    boundary = rules.external_handoff_boundary
    assert boundary.mode == "BUILDER_CONTRACT_ONLY"
    assert boundary.external_validation_status == "BD-014:EXTERNAL_VALIDATION_PENDING"
    assert "local_deterministic_test_double" in boundary.allowed
    assert "external_runtime_execution" in boundary.prohibited
    assert "network_transport" in boundary.prohibited


def test_diagnostics_have_explicit_owners_repairs_and_stop_conditions(
    policy_source_factory,
) -> None:
    rules = compile_category_operating_rules(policy_source_factory("carousels"))
    assert len(rules.diagnostic_routes) == 3
    assert rules.diagnostic_routes[0].repair_unit in rules.repair_units
    assert rules.diagnostic_routes[1].repair_unit in rules.repair_units
    assert rules.diagnostic_routes[2].repair_unit is None
    assert all(route.owner and route.stop_condition for route in rules.diagnostic_routes)


def test_generic_task_preserves_not_applicable_policy(generic_policy_source) -> None:
    rules = compile_category_operating_rules(generic_policy_source)
    assert rules.applicability == NOT_APPLICABLE
    assert rules.category_id is rules.atomic_owner_category_id is None
    assert not rules.runtime_plan_requirements
    assert not rules.evaluation_dimensions
    assert rules.compatibility_policy == ("GENERIC_NON_ACTIVATIVE_TASK",)
    assert rules.external_handoff_boundary.mode == NOT_APPLICABLE


def test_identical_inputs_produce_byte_identical_rules(policy_source_factory) -> None:
    source = policy_source_factory("supervisuals")
    first = compile_category_operating_rules(source)
    second = compile_category_operating_rules(source)
    assert first.canonical_bytes == second.canonical_bytes
    assert first.ruleset_hash == second.ruleset_hash
