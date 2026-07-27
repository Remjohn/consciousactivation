from __future__ import annotations

from dataclasses import replace

from cmf_builder.domain.category_syntax import (
    REQUIRED_RICH_LINEAGE_ROLES,
    compile_category_native_syntax,
)


def test_complete_rich_lineage_is_preserved_with_versions_and_hashes(
    source_factory,
) -> None:
    source = source_factory("2d_character_animation")
    syntax, sequence = compile_category_native_syntax(source)
    observed_roles = {ref.lineage_role for ref in syntax.semantic_lineage}
    assert REQUIRED_RICH_LINEAGE_ROLES <= observed_roles
    assert syntax.semantic_lineage == sequence.semantic_lineage
    assert all(ref.version == "1.0.0" for ref in syntax.semantic_lineage)
    assert all(len(ref.sha256) == 64 for ref in syntax.semantic_lineage)
    assert all(ref.authority for ref in syntax.semantic_lineage)


def test_wrong_reading_locks_are_preserved_canonically(source_factory) -> None:
    source = source_factory("carousels")
    syntax, sequence = compile_category_native_syntax(source)
    assert syntax.wrong_reading_locks == tuple(sorted(source.wrong_reading_locks))
    assert sequence.wrong_reading_locks == syntax.wrong_reading_locks


def test_sequence_preserves_frozen_shared_core_and_activative_semantics(
    source_factory,
) -> None:
    source = source_factory("supervisuals")
    _, sequence = compile_category_native_syntax(source)
    assert sequence.shared_core_ref == source.shared_activative_core_ref
    assert sequence.activation_direction == source.activation_direction
    assert sequence.participant_role == source.participant_role
    assert sequence.states == source.states
    assert sequence.transitions == source.transitions
    assert sequence.payoff == source.payoff
    assert sequence.intended_reaction == source.intended_reaction
    assert sequence.micro_commitment == source.micro_commitment


def test_canonical_lineage_order_does_not_depend_on_input_tuple_order(
    source_factory,
) -> None:
    source = source_factory("short_form_edited_video")
    reversed_source = replace(
        source,
        rich_source_object_refs=tuple(reversed(source.rich_source_object_refs)),
    )
    first = compile_category_native_syntax(source)
    second = compile_category_native_syntax(reversed_source)
    assert first[0].canonical_bytes == second[0].canonical_bytes
    assert first[1].canonical_bytes == second[1].canonical_bytes
