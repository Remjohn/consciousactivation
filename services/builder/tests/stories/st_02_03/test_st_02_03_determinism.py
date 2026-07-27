from __future__ import annotations

from cmf_builder.visual.induction import induce_provisional_grammar
from cmf_builder.visual.ontology import canonical_json_bytes

from fixtures import graph_fixture, induction_policy, provisional_hypothesis, supported_graphs


def grammar_bytes(graphs, hypotheses=()) -> bytes:
    return canonical_json_bytes(
        induce_provisional_grammar(
            run_id="deterministic_induction",
            graphs=graphs,
            policy=induction_policy(),
            hypotheses=hypotheses,
        ).as_dict()
    )


def test_repeat_induction_is_byte_identical() -> None:
    graphs = supported_graphs()
    hypothesis = provisional_hypothesis(graphs)
    assert grammar_bytes(graphs, (hypothesis,)) == grammar_bytes(
        graphs, (hypothesis,)
    )


def test_graph_input_order_does_not_change_identity() -> None:
    graphs = supported_graphs()
    assert grammar_bytes(graphs) == grammar_bytes(tuple(reversed(graphs)))


def test_changed_evidence_creates_new_immutable_grammar_version() -> None:
    baseline = supported_graphs()
    changed = (graph_fixture(0), graph_fixture(2, geometry_offset=5))
    first = induce_provisional_grammar(
        run_id="versioned_induction", graphs=baseline, policy=induction_policy()
    ).grammar
    second = induce_provisional_grammar(
        run_id="versioned_induction", graphs=changed, policy=induction_policy()
    ).grammar

    assert first.series_id == second.series_id
    assert first.grammar_id != second.grammar_id
    assert first.version != second.version
    assert first.artifact_sha256 != second.artifact_sha256


def test_changed_provisional_hypothesis_creates_new_version() -> None:
    graphs = supported_graphs()
    first = induce_provisional_grammar(
        run_id="hypothesis_version",
        graphs=graphs,
        policy=induction_policy(),
        hypotheses=(provisional_hypothesis(graphs, statement="Effect A may apply."),),
    ).grammar
    second = induce_provisional_grammar(
        run_id="hypothesis_version",
        graphs=graphs,
        policy=induction_policy(),
        hypotheses=(provisional_hypothesis(graphs, statement="Effect B may apply."),),
    ).grammar

    assert first.series_id == second.series_id
    assert first.version != second.version


def test_portable_grammar_contains_no_absolute_workspace_path() -> None:
    rendered = grammar_bytes(supported_graphs()).decode("utf-8")
    assert "D:\\" not in rendered
    assert "C:\\" not in rendered
    assert "CONSCIOUS_ACTIVATIONS" not in rendered

