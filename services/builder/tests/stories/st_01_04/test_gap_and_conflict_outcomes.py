from __future__ import annotations

from cmf_builder.domain.evidence_saturation import (
    ConcernKind,
    DownstreamConsequence,
    GapKind,
    SaturationConcern,
    SaturationContract,
    SaturationEvaluation,
    SaturationOutcome,
)
from tests.stories.st_01_04 import build_context, evaluation_command


def _inputs():
    _, repository, _, run_id, source_receipt, index_receipt, contract = build_context()
    lock = repository.get_source_lock(source_receipt.source_lock_ref)
    index = repository.get_evidence_index(index_receipt.index_id)
    assert lock is not None and index is not None
    return repository, run_id, lock, index, contract


def test_missing_required_role_is_typed_and_blocks() -> None:
    _, run_id, lock, index, _ = _inputs()
    contract = SaturationContract.create(
        contract_id="missing-role-contract",
        source_profile_ref=lock.source_profile_ref,
        required_roles=("governed_task_definition", "missing_role"),
    )
    evaluation = SaturationEvaluation.evaluate(
        run_id=run_id, source_lock=lock, index=index, contract=contract, authority_identity="code-1"
    )
    assert evaluation.outcome is SaturationOutcome.BLOCKED_MISSING_EVIDENCE
    assert GapKind.MISSING_EVIDENCE in {item.kind for item in evaluation.gaps}
    assert evaluation.downstream_consequence is DownstreamConsequence.BLOCK


def test_sparse_target_evidence_is_distinct_from_missing() -> None:
    _, run_id, lock, index, _ = _inputs()
    contract = SaturationContract.create(
        contract_id="sparse-contract",
        source_profile_ref=lock.source_profile_ref,
        required_roles=("governed_task_definition",),
        specimens_per_required_role=2,
    )
    evaluation = SaturationEvaluation.evaluate(
        run_id=run_id, source_lock=lock, index=index, contract=contract, authority_identity="code-1"
    )
    assert evaluation.outcome is SaturationOutcome.INSUFFICIENT_TARGET_EVIDENCE
    assert {item.kind for item in evaluation.gaps} == {GapKind.SPARSE_TARGET_EVIDENCE}


def test_contradictory_authority_is_a_distinct_non_downgradable_block() -> None:
    _, run_id, lock, index, contract = _inputs()
    concern = SaturationConcern.create(
        kind=ConcernKind.CONTRADICTORY_AUTHORITY,
        evidence_refs=(index.specimens[0].specimen_id,),
        detail_code="governed_authority_conflict",
        authority_identity="code-1",
    )
    evaluation = SaturationEvaluation.evaluate(
        run_id=run_id,
        source_lock=lock,
        index=index,
        contract=contract,
        authority_identity="code-1",
        concerns=(concern,),
    )
    assert evaluation.outcome is SaturationOutcome.BLOCKED_CONTRADICTORY_AUTHORITY
    assert len(evaluation.authority_conflicts) == 1
    assert evaluation.downstream_consequence is DownstreamConsequence.BLOCK


def test_contradictory_sources_and_unresolved_provenance_remain_distinct() -> None:
    _, run_id, lock, index, contract = _inputs()
    specimen_ref = index.specimens[0].specimen_id
    contradictory = SaturationConcern.create(
        kind=ConcernKind.CONTRADICTORY_SOURCES,
        evidence_refs=(specimen_ref,),
        detail_code="source_claims_conflict",
        authority_identity="code-1",
    )
    unresolved = SaturationConcern.create(
        kind=ConcernKind.UNRESOLVED_PROVENANCE,
        evidence_refs=(specimen_ref,),
        detail_code="source_span_unresolved",
        authority_identity="code-1",
    )
    first = SaturationEvaluation.evaluate(
        run_id=run_id, source_lock=lock, index=index, contract=contract,
        authority_identity="code-1", concerns=(contradictory,)
    )
    second = SaturationEvaluation.evaluate(
        run_id=run_id, source_lock=lock, index=index, contract=contract,
        authority_identity="code-1", concerns=(unresolved,)
    )
    assert first.outcome is SaturationOutcome.INSUFFICIENT_TARGET_EVIDENCE
    assert {item.kind for item in first.gaps} == {GapKind.CONTRADICTORY_SOURCES}
    assert second.outcome is SaturationOutcome.BLOCKED_MISSING_EVIDENCE
    assert {item.kind for item in second.gaps} == {GapKind.UNRESOLVED_PROVENANCE}


def test_hg_002_critical_claim_without_evidence_fails_closed() -> None:
    _, run_id, lock, index, contract = _inputs()
    concern = SaturationConcern.create(
        kind=ConcernKind.CRITICAL_CLAIM_WITHOUT_EVIDENCE,
        evidence_refs=(),
        detail_code="unsupported_critical_claim",
        authority_identity="code-1",
    )
    evaluation = SaturationEvaluation.evaluate(
        run_id=run_id, source_lock=lock, index=index, contract=contract,
        authority_identity="code-1", concerns=(concern,)
    )
    assert evaluation.outcome is SaturationOutcome.BLOCKED_MISSING_EVIDENCE
    assert GapKind.CRITICAL_CLAIM_WITHOUT_EVIDENCE in {item.kind for item in evaluation.gaps}


def test_pass_with_limitations_requires_explicit_human_waiver() -> None:
    _, run_id, lock, index, contract = _inputs()
    concern = SaturationConcern.create(
        kind=ConcernKind.NONCRITICAL_LIMITATION,
        evidence_refs=(index.specimens[0].specimen_id,),
        detail_code="bounded_noncritical_limitation",
        authority_identity="code-1",
    )
    without_waiver = SaturationEvaluation.evaluate(
        run_id=run_id, source_lock=lock, index=index, contract=contract,
        authority_identity="code-1", concerns=(concern,)
    )
    with_waiver = SaturationEvaluation.evaluate(
        run_id=run_id, source_lock=lock, index=index, contract=contract,
        authority_identity="code-1", concerns=(concern,),
        human_waiver_ref="human-waiver-receipt-1", waiver_authority_kind="HUMAN"
    )
    assert without_waiver.outcome is SaturationOutcome.INSUFFICIENT_TARGET_EVIDENCE
    assert with_waiver.outcome is SaturationOutcome.PASS_WITH_LIMITATIONS
    assert with_waiver.downstream_consequence is DownstreamConsequence.PROCEED_PROVISIONALLY
