from __future__ import annotations

from dataclasses import replace

import pytest

from cmf_builder.domain.category_syntax import (
    ACTIVATION_FIRST,
    CATEGORY_PROFILE_CONTRACTS,
    MATURITY_STATUS,
    NOT_APPLICABLE,
    VISUAL_SYNTAX_FIRST,
    CategorySyntaxInput,
    compile_category_native_syntax,
)


@pytest.mark.parametrize(
    ("category_id", "expected_family", "dimension", "expected_rule"),
    [
        (
            "short_form_edited_video",
            "SHORT_FORM_EDITED_VIDEO_TIMELINE",
            "temporal_grammar",
            "edited_transition_continuity",
        ),
        (
            "2d_character_animation",
            "TWO_D_CHARACTER_PERFORMANCE_CONTINUITY",
            "character_performance_grammar",
            "identity_pose_expression_gesture_gaze",
        ),
        (
            "carousels",
            "CAROUSEL_SWIPE_PROGRESSION",
            "reading_order",
            "swipe_progression",
        ),
        (
            "supervisuals",
            "SUPERVISUAL_STATIC_HIERARCHY",
            "spatial_grammar",
            "single_frame_attention_hierarchy",
        ),
        (
            "conversational_activation_expression",
            "CONVERSATIONAL_TURN_RELATIONSHIP",
            "conversational_turn_structure",
            "turn_relationship",
        ),
    ],
)
def test_each_constitutional_category_compiles_its_native_grammar(
    source_factory, category_id, expected_family, dimension, expected_rule
) -> None:
    syntax, sequence = compile_category_native_syntax(source_factory(category_id))
    assert syntax.category_id == category_id
    assert syntax.grammar_family == expected_family
    assert expected_rule in getattr(syntax, dimension).rules
    assert sequence.category_syntax_ref == syntax.syntax_hash
    assert syntax.runtime_law == sequence.runtime_law == ACTIVATION_FIRST
    assert syntax.development_law == sequence.development_law == VISUAL_SYNTAX_FIRST
    assert syntax.maturity_status == sequence.maturity_status == MATURITY_STATUS
    assert syntax.production_ready is sequence.production_ready is False
    assert syntax.certified is sequence.certified is False


def test_format02_is_character_performance_not_edited_video(source_factory) -> None:
    edited, _ = compile_category_native_syntax(
        source_factory("short_form_edited_video")
    )
    format02, _ = compile_category_native_syntax(
        source_factory("2d_character_animation")
    )
    assert format02.temporal_grammar.rules != edited.temporal_grammar.rules
    assert format02.character_performance_grammar.applicability == "REQUIRED"
    assert edited.character_performance_grammar.applicability == NOT_APPLICABLE


def test_static_categories_keep_temporal_non_applicability_explicit(source_factory) -> None:
    carousel, _ = compile_category_native_syntax(source_factory("carousels"))
    supervisual, _ = compile_category_native_syntax(source_factory("supervisuals"))
    assert carousel.temporal_grammar.applicability == NOT_APPLICABLE
    assert "FRAME_TIME" in carousel.temporal_grammar.basis
    assert supervisual.temporal_grammar.applicability == NOT_APPLICABLE
    assert "SINGLE_FRAME" in supervisual.temporal_grammar.basis


@pytest.mark.parametrize(
    "profile_id", CATEGORY_PROFILE_CONTRACTS["conversational_activation_expression"]
)
def test_conversational_profiles_are_turn_structures_not_timelines(
    source_factory, profile_id
) -> None:
    syntax, _ = compile_category_native_syntax(
        source_factory("conversational_activation_expression", profile_id=profile_id)
    )
    assert syntax.profile_id == profile_id
    assert syntax.temporal_grammar.applicability == NOT_APPLICABLE
    assert syntax.conversational_turn_structure.applicability == "REQUIRED"
    assert "reaction_receipt_reference_only" in syntax.conversational_turn_structure.rules
    assert "expression_moment_reference_only" in syntax.conversational_turn_structure.rules
    assert all("timeline" not in rule for rule in syntax.conversational_turn_structure.rules)


def test_generic_branch_is_explicit_not_applicable() -> None:
    source = CategorySyntaxInput(
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
    syntax, sequence = compile_category_native_syntax(source)
    assert syntax.applicability == sequence.applicability == NOT_APPLICABLE
    assert syntax.category_id is syntax.profile_id is None
    assert not syntax.semantic_lineage
    assert not sequence.semantic_lineage
    assert syntax.evidence_gate == "BD-007:EVIDENCE_PENDING"


def test_identical_inputs_are_byte_identical(source_factory) -> None:
    source = source_factory("short_form_edited_video")
    first = compile_category_native_syntax(source)
    second = compile_category_native_syntax(source)
    assert first[0].canonical_bytes == second[0].canonical_bytes
    assert first[1].canonical_bytes == second[1].canonical_bytes
    assert first[0].syntax_hash == second[0].syntax_hash
    assert first[1].sequence_hash == second[1].sequence_hash


def test_changed_governed_input_changes_identities(source_factory) -> None:
    source = source_factory("short_form_edited_video")
    changed = replace(source, payoff="a distinctly governed payoff")
    first = compile_category_native_syntax(source)
    second = compile_category_native_syntax(changed)
    assert first[0].syntax_hash == second[0].syntax_hash
    assert first[1].sequence_hash != second[1].sequence_hash
