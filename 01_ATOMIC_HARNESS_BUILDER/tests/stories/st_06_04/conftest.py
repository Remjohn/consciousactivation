from __future__ import annotations

from hashlib import sha256

import pytest

from cmf_builder.domain.category_runtime_rules import CategoryPolicyInput
from cmf_builder.domain.category_syntax import (
    CATEGORY_CONSTITUTION_VERSION,
    GRAMMAR_FAMILIES,
    CategorySyntaxInput,
    GovernedRef,
    compile_category_native_syntax,
)


DEFAULT_PROFILES = {
    "short_form_edited_video": "format01_story_video",
    "2d_character_animation": "format02_minimal_coach_theatre",
    "carousels": None,
    "supervisuals": None,
    "conversational_activation_expression": "public_comment",
}


def make_ref(role: str, *, suffix: str = "v1", status: str = "ACTIVE") -> GovernedRef:
    return GovernedRef(
        object_id=f"{role}-{suffix}",
        version="1.0.0",
        sha256=sha256(f"{role}:{suffix}".encode()).hexdigest(),
        authority="governed-test-authority",
        lineage_role=role,
        status=status,
    )


def make_policy_source(category_id: str = "short_form_edited_video") -> CategoryPolicyInput:
    profile_id = DEFAULT_PROFILES[category_id]
    rich_roles = (
        "source_premise",
        "identity_dna",
        "context_premise",
        "resonance_map",
        "matrix_of_edging",
        "activative_intelligence_pack",
        "evaluation_contract",
    )
    syntax_input = CategorySyntaxInput(
        harness_id=f"harness-{category_id}",
        harness_version="1.0.0",
        mode="activative",
        category_id=category_id,
        profile_id=profile_id,
        category_constitution_version=CATEGORY_CONSTITUTION_VERSION,
        requested_grammar_family=GRAMMAR_FAMILIES[category_id],
        category_binding_ref=make_ref("category_binding"),
        structural_profile_ref=make_ref("structural_profile"),
        shared_activative_core_ref=make_ref("shared_activative_core"),
        evidence_refs=(make_ref("syntax_evidence"),),
        rich_source_object_refs=tuple(make_ref(role) for role in rich_roles),
        authority_refs=(make_ref("constitutional_authority"),),
        wrong_reading_locks=("preserve category meaning", "do not invent human truth"),
        activation_direction="recognition to owned action",
        participant_role="active meaning-maker",
        states=("ATTENTION", "RECOGNITION", "OWNERSHIP"),
        transitions=("ATTENTION->RECOGNITION", "RECOGNITION->OWNERSHIP"),
        pacing="category-native progression",
        sonic_or_silence_function="support without replacing meaning",
        payoff="owned next step",
        intended_reaction="recognize agency",
        micro_commitment="name one next action",
    )
    syntax, sequence = compile_category_native_syntax(syntax_input)
    return CategoryPolicyInput(
        ruleset_name=f"rules-{category_id}",
        ruleset_version="1.0.0",
        syntax=syntax,
        sequence=sequence,
        evaluator_owner_ref=make_ref("evaluation_owner"),
        repair_owner_ref=make_ref("repair_owner"),
        migration_authority_ref=make_ref("migration_authority"),
        compatibility_authority_ref=make_ref("compatibility_authority"),
    )


def make_generic_source() -> CategoryPolicyInput:
    syntax_input = CategorySyntaxInput(
        harness_id="generic-task",
        harness_version="1.0.0",
        mode="generic",
        category_id=None,
        profile_id=None,
        category_constitution_version=None,
        requested_grammar_family=None,
        category_binding_ref=None,
        structural_profile_ref=None,
        shared_activative_core_ref=None,
        evidence_refs=(),
        rich_source_object_refs=(),
        authority_refs=(),
        wrong_reading_locks=(),
        activation_direction=None,
        participant_role=None,
        states=(),
        transitions=(),
        pacing=None,
        sonic_or_silence_function=None,
        payoff=None,
        intended_reaction=None,
        micro_commitment=None,
    )
    syntax, sequence = compile_category_native_syntax(syntax_input)
    return CategoryPolicyInput(
        ruleset_name="generic-not-applicable",
        ruleset_version="1.0.0",
        syntax=syntax,
        sequence=sequence,
        evaluator_owner_ref=None,
        repair_owner_ref=None,
        migration_authority_ref=None,
        compatibility_authority_ref=None,
    )


@pytest.fixture
def policy_source_factory():
    return make_policy_source


@pytest.fixture
def generic_policy_source():
    return make_generic_source()


@pytest.fixture
def ref_factory():
    return make_ref
