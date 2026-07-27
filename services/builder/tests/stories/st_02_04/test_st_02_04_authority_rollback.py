from dataclasses import replace

import pytest

from cmf_builder.application.authority import AuthorityDenied
from cmf_builder.visual.atomicity_contracts import (
    AtomicityCommitRejected,
)
from cmf_builder.visual.boundary_comparison import (
    InMemoryAtomicityComparisonWorkspace,
    _expected_receipt_id,
    _packet_core,
)
from cmf_builder.visual.ontology import canonical_sha256
from tests.stories.st_02_04.fixtures import (
    COMPARISON_AUTHORITY,
    NOW,
    authority_service,
    changed_comparison_result,
    comparison_result,
    grammar_result,
)


def _workspace(result) -> InMemoryAtomicityComparisonWorkspace:
    return InMemoryAtomicityComparisonWorkspace(
        authority=authority_service(result.packet.series_id)
    )


def _rebind_packet(result, staged_packet):
    artifact_sha256 = canonical_sha256(_packet_core(staged_packet))
    packet = replace(
        staged_packet,
        packet_id=f"ST-02.04:AtomicityComparison:{artifact_sha256}",
        version=f"0.0.0-development+{artifact_sha256[:16]}",
        artifact_sha256=artifact_sha256,
    )
    staged_receipt = replace(
        result.receipt,
        receipt_id="PENDING_CANONICAL_BINDING",
        packet_id=packet.packet_id,
        packet_version=packet.version,
        packet_artifact_sha256=packet.artifact_sha256,
    )
    return replace(
        result,
        packet=packet,
        receipt=replace(
            staged_receipt,
            receipt_id=_expected_receipt_id(staged_receipt),
        ),
    )


def test_self_asserted_packet_actor_is_denied_without_registration() -> None:
    source = grammar_result()
    result = comparison_result(source=source, authority_ref="self_asserted_actor")
    workspace = InMemoryAtomicityComparisonWorkspace(
        authority=authority_service(
            result.packet.series_id,
            actor_id=COMPARISON_AUTHORITY,
        )
    )

    with pytest.raises(AuthorityDenied, match="not registered"):
        workspace.commit(
            result,
            grammar_result=source,
            actor_id="self_asserted_actor",
            now=NOW,
            expected_active_packet_id=None,
        )
    assert workspace.active(result.packet.series_id) is None


def test_exact_resource_and_current_time_are_authorized_fail_closed() -> None:
    source = grammar_result()
    result = comparison_result(source=source)
    wrong_resource = InMemoryAtomicityComparisonWorkspace(
        authority=authority_service(
            result.packet.series_id,
            grant_resource_id="different_series",
        )
    )
    expired = InMemoryAtomicityComparisonWorkspace(
        authority=authority_service(
            result.packet.series_id,
            expires_at=NOW,
        )
    )

    with pytest.raises(AuthorityDenied, match="No active exact authority grant"):
        wrong_resource.commit(
            result,
            grammar_result=source,
            actor_id=COMPARISON_AUTHORITY,
            now=NOW,
            expected_active_packet_id=None,
        )
    with pytest.raises(AuthorityDenied, match="No active exact authority grant"):
        expired.commit(
            result,
            grammar_result=source,
            actor_id=COMPARISON_AUTHORITY,
            now=NOW,
            expected_active_packet_id=None,
        )


def test_commit_is_payload_safe_and_idempotent() -> None:
    source = grammar_result()
    result = comparison_result(source=source)
    workspace = _workspace(result)

    first = workspace.commit(
        result,
        grammar_result=source,
        actor_id=COMPARISON_AUTHORITY,
        now=NOW,
        expected_active_packet_id=None,
    )
    replay = workspace.commit(
        result,
        grammar_result=source,
        actor_id=COMPARISON_AUTHORITY,
        now=NOW,
        expected_active_packet_id=None,
    )

    assert replay == first
    assert workspace.history(first.series_id) == (first,)


def test_conflicting_same_identity_receipt_fails_closed() -> None:
    source = grammar_result()
    result = comparison_result(source=source)
    workspace = _workspace(result)
    workspace.commit(
        result,
        grammar_result=source,
        actor_id=COMPARISON_AUTHORITY,
        now=NOW,
        expected_active_packet_id=None,
    )
    altered = replace(result, receipt=replace(result.receipt, run_id="conflict"))

    with pytest.raises(AtomicityCommitRejected):
        workspace.commit(
            altered,
            grammar_result=source,
            actor_id=COMPARISON_AUTHORITY,
            now=NOW,
            expected_active_packet_id=None,
        )


def test_atomic_failure_leaves_zero_partial_state() -> None:
    source = grammar_result()
    result = comparison_result(source=source)
    workspace = _workspace(result)

    with pytest.raises(AtomicityCommitRejected):
        workspace.commit(
            result,
            grammar_result=source,
            actor_id=COMPARISON_AUTHORITY,
            now=NOW,
            expected_active_packet_id=None,
            inject_failure=True,
        )
    assert workspace.active(result.packet.series_id) is None
    assert workspace.history(result.packet.series_id) == ()


def test_rollback_requires_current_expectation_and_preserves_history() -> None:
    source = grammar_result()
    first = comparison_result(source=source)
    second = changed_comparison_result(source)
    workspace = _workspace(first)
    workspace.commit(
        first,
        grammar_result=source,
        actor_id=COMPARISON_AUTHORITY,
        now=NOW,
        expected_active_packet_id=None,
    )
    workspace.commit(
        second,
        grammar_result=source,
        actor_id=COMPARISON_AUTHORITY,
        now=NOW,
        expected_active_packet_id=first.packet.packet_id,
    )

    with pytest.raises(AtomicityCommitRejected, match="rollback expectation"):
        workspace.rollback_to(
            series_id=first.packet.series_id,
            packet_id=first.packet.packet_id,
            actor_id=COMPARISON_AUTHORITY,
            now=NOW,
            expected_active_packet_id=first.packet.packet_id,
        )
    rolled_back = workspace.rollback_to(
        series_id=first.packet.series_id,
        packet_id=first.packet.packet_id,
        actor_id=COMPARISON_AUTHORITY,
        now=NOW,
        expected_active_packet_id=second.packet.packet_id,
    )

    assert rolled_back == first.packet
    assert workspace.active(first.packet.series_id) == first.packet
    assert set(workspace.history(first.packet.series_id)) == {first.packet, second.packet}


def test_forged_canonical_payload_cannot_bypass_source_semantics_at_commit() -> None:
    source = grammar_result()
    result = comparison_result(source=source)
    forged_candidate = replace(
        result.packet.candidates[0],
        affected_specimen_ids=("forged_specimen",),
    )
    forged = _rebind_packet(
        result,
        replace(
            result.packet,
            candidates=(forged_candidate, *result.packet.candidates[1:]),
            packet_id="PENDING_CANONICAL_BINDING",
            version="PENDING_CANONICAL_BINDING",
            artifact_sha256="PENDING_CANONICAL_BINDING",
        ),
    )

    workspace = _workspace(result)
    with pytest.raises(AtomicityCommitRejected, match="semantic validation"):
        workspace.commit(
            forged,
            grammar_result=source,
            actor_id=COMPARISON_AUTHORITY,
            now=NOW,
            expected_active_packet_id=None,
        )
    assert workspace.history(forged.packet.series_id) == ()


def test_forged_noncanonical_alternative_order_fails_at_commit() -> None:
    source = grammar_result()
    result = comparison_result(source=source)
    forged = _rebind_packet(
        result,
        replace(
            result.packet,
            candidates=tuple(reversed(result.packet.candidates)),
            packet_id="PENDING_CANONICAL_BINDING",
            version="PENDING_CANONICAL_BINDING",
            artifact_sha256="PENDING_CANONICAL_BINDING",
        ),
    )

    with pytest.raises(AtomicityCommitRejected, match="canonical order"):
        _workspace(result).commit(
            forged,
            grammar_result=source,
            actor_id=COMPARISON_AUTHORITY,
            now=NOW,
            expected_active_packet_id=None,
        )


def test_forged_series_identity_cannot_bypass_active_history() -> None:
    source = grammar_result()
    result = comparison_result(source=source)
    forged = _rebind_packet(
        result,
        replace(
            result.packet,
            series_id="f" * 64,
            packet_id="PENDING_CANONICAL_BINDING",
            version="PENDING_CANONICAL_BINDING",
            artifact_sha256="PENDING_CANONICAL_BINDING",
        ),
    )
    workspace = InMemoryAtomicityComparisonWorkspace(
        authority=authority_service(forged.packet.series_id)
    )

    with pytest.raises(AtomicityCommitRejected, match="exactly bound"):
        workspace.commit(
            forged,
            grammar_result=source,
            actor_id=COMPARISON_AUTHORITY,
            now=NOW,
            expected_active_packet_id=None,
        )
