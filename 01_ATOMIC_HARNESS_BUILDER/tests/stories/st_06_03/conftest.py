from __future__ import annotations

from hashlib import sha256

import pytest

from cmf_builder.domain.category_syntax import (
    CATEGORY_CONSTITUTION_VERSION,
    GRAMMAR_FAMILIES,
    CategorySyntaxInput,
    GovernedRef,
)


DEFAULT_PROFILES = {
    "short_form_edited_video": "format01_story_video",
    "2d_character_animation": "format02_minimal_coach_theatre",
    "carousels": None,
    "supervisuals": None,
    "conversational_activation_expression": "public_comment",
}


def make_ref(role: str, *, status: str = "ACTIVE", suffix: str = "v1") -> GovernedRef:
    return GovernedRef(
        object_id=f"{role}-{suffix}",
        version="1.0.0",
        sha256=sha256(f"{role}:{suffix}".encode("utf-8")).hexdigest(),
        authority="governed-test-authority",
        lineage_role=role,
        status=status,
    )


def make_source(
    category_id: str = "short_form_edited_video",
    *,
    profile_id: str | None = None,
) -> CategorySyntaxInput:
    if profile_id is None:
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
    return CategorySyntaxInput(
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
        wrong_reading_locks=(
            "do not flatten category semantics",
            "do not invent human truth",
        ),
        activation_direction="move from observation to owned participation",
        participant_role="active meaning-maker",
        states=("ATTENTION", "RECOGNITION", "OWNERSHIP", "COMMITMENT"),
        transitions=(
            "ATTENTION->RECOGNITION",
            "RECOGNITION->OWNERSHIP",
            "OWNERSHIP->COMMITMENT",
        ),
        pacing="category-native deliberate progression",
        sonic_or_silence_function="support pressure without replacing meaning",
        payoff="owned next step",
        intended_reaction="recognize agency without supplied emotion",
        micro_commitment="name one next action",
    )


@pytest.fixture
def source_factory():
    return make_source


@pytest.fixture
def ref_factory():
    return make_ref
