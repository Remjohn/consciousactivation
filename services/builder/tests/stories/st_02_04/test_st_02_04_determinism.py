from dataclasses import replace

import pytest

from cmf_builder.visual.atomicity_contracts import BoundaryEvidenceInvalid

from tests.stories.st_02_04.fixtures import (
    all_candidates,
    changed_comparison_result,
    comparison_result,
    grammar_result,
)


def test_identical_inputs_are_byte_identical_across_fresh_contexts() -> None:
    first_source = grammar_result()
    second_source = grammar_result()
    first = comparison_result(source=first_source)
    second = comparison_result(
        source=second_source,
        candidates=tuple(reversed(all_candidates(second_source.grammar))),
    )

    assert first.as_dict() == second.as_dict()
    assert first.packet.artifact_sha256 == second.packet.artifact_sha256
    assert first.receipt.receipt_sha256 == second.receipt.receipt_sha256


def test_changed_governed_consequence_creates_new_immutable_identity() -> None:
    source = grammar_result()
    first = comparison_result(source=source)
    second = changed_comparison_result(source)

    assert first.packet.series_id == second.packet.series_id
    assert first.packet.packet_id != second.packet.packet_id
    assert first.packet.artifact_sha256 != second.packet.artifact_sha256


def test_mutated_predecessor_receipt_fails_closed() -> None:
    source = grammar_result()
    altered = replace(source, receipt=replace(source.receipt, outcome="ALTERED"))

    with pytest.raises(BoundaryEvidenceInvalid):
        comparison_result(source=altered)


def test_portable_packet_contains_no_absolute_workspace_path() -> None:
    serialized = str(comparison_result().as_dict()).replace("\\\\", "/")

    assert "D:/Work/" not in serialized
    assert "D:\\Work\\" not in serialized


def test_equivalent_set_orderings_produce_the_same_identity() -> None:
    source = grammar_result()
    canonical = all_candidates(source.grammar)
    reordered = tuple(
        replace(
            item,
            affected_specimen_ids=tuple(reversed(item.affected_specimen_ids)),
            shared_dimensions=tuple(reversed(item.shared_dimensions)),
            differing_dimensions=tuple(reversed(item.differing_dimensions)),
            breaking_dimensions=tuple(reversed(item.breaking_dimensions)),
            dimensions=tuple(
                replace(
                    dimension,
                    source_graph_ids=tuple(reversed(dimension.source_graph_ids)),
                    motif_ids=tuple(reversed(dimension.motif_ids)),
                    hypothesis_ids=tuple(reversed(dimension.hypothesis_ids)),
                )
                for dimension in reversed(item.dimensions)
            ),
            risks=tuple(
                replace(
                    risk,
                    source_graph_ids=tuple(reversed(risk.source_graph_ids)),
                    hypothesis_ids=tuple(reversed(risk.hypothesis_ids)),
                )
                for risk in reversed(item.risks)
            ),
        )
        for item in reversed(canonical)
    )

    first = comparison_result(source=source, candidates=canonical)
    second = comparison_result(source=source, candidates=reordered)
    assert first.as_dict() == second.as_dict()
