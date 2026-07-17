from __future__ import annotations

from dataclasses import replace

import pytest

from cmf_builder.visual.grammar_contracts import (
    AtomicGrammarCommitRejected,
    GrammarAuthorityRejected,
)
from cmf_builder.visual.induction import (
    InMemoryProvisionalGrammarWorkspace,
    induce_provisional_grammar,
)

from fixtures import AUTHORITY, graph_fixture, induction_policy, supported_graphs


def result(graphs):
    return induce_provisional_grammar(
        run_id="workspace_induction", graphs=graphs, policy=induction_policy()
    )


def test_only_declared_authority_can_commit() -> None:
    workspace = InMemoryProvisionalGrammarWorkspace()
    with pytest.raises(GrammarAuthorityRejected):
        workspace.commit(
            result(supported_graphs()),
            actor_authority_ref="unauthorized_actor",
            expected_active_grammar_id=None,
        )
    assert workspace.history(result(supported_graphs()).grammar.series_id) == ()


def test_injected_atomic_failure_leaves_zero_partial_state() -> None:
    workspace = InMemoryProvisionalGrammarWorkspace()
    candidate = result(supported_graphs())
    with pytest.raises(AtomicGrammarCommitRejected):
        workspace.commit(
            candidate,
            actor_authority_ref=AUTHORITY,
            expected_active_grammar_id=None,
            inject_failure=True,
        )

    assert workspace.active(candidate.grammar.series_id) is None
    assert workspace.history(candidate.grammar.series_id) == ()


def test_repeat_commit_is_payload_safe_and_idempotent() -> None:
    workspace = InMemoryProvisionalGrammarWorkspace()
    candidate = result(supported_graphs())
    first = workspace.commit(
        candidate,
        actor_authority_ref=AUTHORITY,
        expected_active_grammar_id=None,
    )
    second = workspace.commit(
        candidate,
        actor_authority_ref=AUTHORITY,
        expected_active_grammar_id="stale_expectation_is_ignored_for_identical_payload",
    )

    assert first is second
    assert workspace.history(first.series_id) == (first,)


def test_repeat_same_grammar_identity_with_different_receipt_payload_fails() -> None:
    workspace = InMemoryProvisionalGrammarWorkspace()
    candidate = result(supported_graphs())
    workspace.commit(
        candidate,
        actor_authority_ref=AUTHORITY,
        expected_active_grammar_id=None,
    )
    changed_receipt = replace(candidate.receipt, run_id="different_command_payload")
    with pytest.raises(AtomicGrammarCommitRejected, match="receipt"):
        workspace.commit(
            replace(candidate, receipt=changed_receipt),
            actor_authority_ref=AUTHORITY,
            expected_active_grammar_id=candidate.grammar.grammar_id,
        )


def test_commit_revalidates_canonical_grammar_hash_and_invariant_flags() -> None:
    workspace = InMemoryProvisionalGrammarWorkspace()
    candidate = result(supported_graphs())
    for changed_grammar in (
        replace(candidate.grammar, artifact_sha256="f" * 64),
        replace(candidate.grammar, certified=True),
    ):
        with pytest.raises(AtomicGrammarCommitRejected):
            workspace.commit(
                replace(candidate, grammar=changed_grammar),
                actor_authority_ref=AUTHORITY,
                expected_active_grammar_id=None,
            )
    assert workspace.active(candidate.grammar.series_id) is None


def test_commit_rejects_receipt_not_exactly_bound_to_grammar() -> None:
    workspace = InMemoryProvisionalGrammarWorkspace()
    candidate = result(supported_graphs())
    changed_receipt = replace(
        candidate.receipt,
        grammar_artifact_sha256="f" * 64,
    )
    with pytest.raises(AtomicGrammarCommitRejected, match="receipt"):
        workspace.commit(
            replace(candidate, receipt=changed_receipt),
            actor_authority_ref=AUTHORITY,
            expected_active_grammar_id=None,
        )


def test_stale_expected_active_identity_fails_closed() -> None:
    workspace = InMemoryProvisionalGrammarWorkspace()
    first = result(supported_graphs())
    workspace.commit(
        first, actor_authority_ref=AUTHORITY, expected_active_grammar_id=None
    )
    changed = result((graph_fixture(0), graph_fixture(2, geometry_offset=5)))
    with pytest.raises(AtomicGrammarCommitRejected):
        workspace.commit(
            changed,
            actor_authority_ref=AUTHORITY,
            expected_active_grammar_id="wrong_active_identity",
        )

    assert workspace.active(first.grammar.series_id) == first.grammar
    assert workspace.history(first.grammar.series_id) == (first.grammar,)


def test_non_destructive_rollback_preserves_both_versions() -> None:
    workspace = InMemoryProvisionalGrammarWorkspace()
    first = result(supported_graphs())
    workspace.commit(
        first, actor_authority_ref=AUTHORITY, expected_active_grammar_id=None
    )
    second = result((graph_fixture(0), graph_fixture(2, geometry_offset=5)))
    workspace.commit(
        second,
        actor_authority_ref=AUTHORITY,
        expected_active_grammar_id=first.grammar.grammar_id,
    )

    rolled_back = workspace.rollback_to(
        series_id=first.grammar.series_id,
        grammar_id=first.grammar.grammar_id,
        actor_authority_ref=AUTHORITY,
    )

    assert rolled_back == first.grammar
    assert workspace.active(first.grammar.series_id) == first.grammar
    assert set(workspace.history(first.grammar.series_id)) == {
        first.grammar,
        second.grammar,
    }


def test_unauthorized_rollback_fails_without_state_change() -> None:
    workspace = InMemoryProvisionalGrammarWorkspace()
    candidate = result(supported_graphs())
    workspace.commit(
        candidate, actor_authority_ref=AUTHORITY, expected_active_grammar_id=None
    )
    with pytest.raises(GrammarAuthorityRejected):
        workspace.rollback_to(
            series_id=candidate.grammar.series_id,
            grammar_id=candidate.grammar.grammar_id,
            actor_authority_ref="unauthorized_actor",
        )
    assert workspace.active(candidate.grammar.series_id) == candidate.grammar
