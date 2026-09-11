"""CA-M032 / INV-MEM-001 executable proof.

The tests exercise the authoritative SQLite memory-promotion boundary, not a
mocked writer. They cover schema conformance, positive governed promotion,
raw-overwrite rejection, merge-consensus enforcement, stale-version conflict
rejection, provenance/receipt durability, idempotency, and false-proof input.
"""

from __future__ import annotations

import copy
from pathlib import Path
import importlib.util
import sys
from concurrent.futures import ThreadPoolExecutor

import pytest

MODULE_PATH = Path(__file__).parents[2] / "packages" / "ca_runtime" / "src" / "ca_runtime" / "memory_writeback.py"
_SPEC = importlib.util.spec_from_file_location("ca_runtime.memory_writeback", MODULE_PATH)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MODULE
_SPEC.loader.exec_module(_MODULE)

LearningCandidate = _MODULE.LearningCandidate
MemoryConflictError = _MODULE.MemoryConflictError
MemoryConsensusError = _MODULE.MemoryConsensusError
MemoryPolicyError = _MODULE.MemoryPolicyError
MemorySchemaError = _MODULE.MemorySchemaError
MemoryWritebackPolicy = _MODULE.MemoryWritebackPolicy
MemoryWritebackStore = _MODULE.MemoryWritebackStore
MergeConsensus = _MODULE.MergeConsensus
ProvenanceRef = _MODULE.ProvenanceRef
RawObservationWriteRejected = _MODULE.RawObservationWriteRejected



def _sha(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _candidate(
    *,
    candidate_id: str = "cand-001",
    key: str = "audience.trust.pattern",
    value: object | None = None,
    expected_version: int = 0,
    mode: str = "INSERT",
    confidence_bps: int = 9000,
    basis: tuple[str, ...] = ("evidence-001",),
) -> LearningCandidate:
    if value is None:
        value = {"pattern": "clarify before persuasion"}
    evidence = (
        ProvenanceRef("evidence-001", _sha("evidence-001"), "OUTCOME", "outcome/1"),
        ProvenanceRef("evidence-002", _sha("evidence-002"), "HUMAN_CORRECTION", "correction/1"),
    )
    attribution = ProvenanceRef("release-001", _sha("release-001"), "RELEASE_MANIFEST", "release/1")
    import hashlib, json

    value_hash = hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    consensus = MergeConsensus(
        mode=mode,  # type: ignore[arg-type]
        expected_memory_version=expected_version,
        basis_refs=basis,
        resolved_value_sha256=value_hash,
        rationale="two independent evidence bases converge on the proposed memory update",
    )
    return LearningCandidate(
        candidate_id=candidate_id,
        workspace_id="workspace-a",
        memory_key=key,
        value=value,
        evidence_refs=evidence,
        attribution_ref=attribution,
        confidence_bps=confidence_bps,
        merge_consensus=consensus,
        actor_id="agent-17",
        created_at="2026-09-08T11:30:00Z",
    )


def _store(tmp_path: Path) -> MemoryWritebackStore:
    return MemoryWritebackStore(
        tmp_path / "memory.sqlite3",
        policy=MemoryWritebackPolicy(minimum_confidence_bps=8000, minimum_evidence_refs=2),
    )


def test_positive_governed_promotion_persists_memory_provenance_and_receipt(tmp_path: Path) -> None:
    store = _store(tmp_path)
    candidate = _candidate()

    receipt = store.promote(candidate)
    item = store.get_memory("workspace-a", candidate.memory_key)

    assert receipt.outcome == "PROMOTED"
    assert receipt.item_id == item.item_id
    assert receipt.resulting_version == 1
    assert item.value == candidate.value
    assert item.version == 1
    assert {ref.source_id for ref in item.provenance} == {
        "evidence-001",
        "evidence-002",
        "release-001",
    }
    persisted = store.get_receipt("workspace-a", candidate.candidate_id)
    assert persisted == receipt


def test_raw_observation_cannot_cross_durable_memory_boundary(tmp_path: Path) -> None:
    store = _store(tmp_path)

    with pytest.raises(RawObservationWriteRejected):
        store.write_raw_observation({"metric": "views", "value": 42}, workspace_id="workspace-a")

    assert store.get_memory("workspace-a", "audience.trust.pattern") is None


def test_false_proof_dict_labeled_learning_candidate_is_rejected_and_writes_nothing(tmp_path: Path) -> None:
    store = _store(tmp_path)
    candidate = _candidate().to_dict()
    fake = copy.deepcopy(candidate)
    fake["__type__"] = "LearningCandidate"

    with pytest.raises(MemorySchemaError):
        store.promote(fake)  # type: ignore[arg-type]

    assert store.get_memory("workspace-a", "audience.trust.pattern") is None


def test_under_threshold_candidate_is_fail_closed(tmp_path: Path) -> None:
    store = _store(tmp_path)
    candidate = _candidate(confidence_bps=7999)

    with pytest.raises(MemoryPolicyError):
        store.promote(candidate)

    assert store.get_memory("workspace-a", candidate.memory_key) is None


def test_merge_requires_explicit_consensus_and_rejects_unbacked_basis(tmp_path: Path) -> None:
    store = _store(tmp_path)
    initial = _candidate()
    store.promote(initial)

    update = _candidate(
        candidate_id="cand-002",
        value={"pattern": "clarify before persuasion", "confidence": "high"},
        expected_version=1,
        mode="MERGE",
        basis=("not-an-evidence-ref",),
    )

    with pytest.raises(MemoryConsensusError):
        store.promote(update)

    item = store.get_memory("workspace-a", initial.memory_key)
    assert item.version == 1
    assert item.value == initial.value


def test_stale_writer_is_rejected_without_lost_update(tmp_path: Path) -> None:
    store = _store(tmp_path)
    first = _candidate()
    store.promote(first)

    current = _candidate(
        candidate_id="cand-002",
        value={"pattern": "latest governed lesson"},
        expected_version=1,
        mode="MERGE",
    )
    stale = _candidate(
        candidate_id="cand-003",
        value={"pattern": "stale lesson must not win"},
        expected_version=1,
        mode="MERGE",
    )

    store.promote(current)

    with pytest.raises(MemoryConflictError):
        store.promote(stale)

    item = store.get_memory("workspace-a", first.memory_key)
    assert item.version == 2
    assert item.value == current.value


def test_candidate_id_is_idempotent_but_same_id_with_new_bytes_is_conflict(tmp_path: Path) -> None:
    store = _store(tmp_path)
    candidate = _candidate()
    first = store.promote(candidate)
    second = store.promote(candidate)
    assert second == first

    mutated = _candidate(value={"pattern": "different bytes"})
    with pytest.raises(MemoryConflictError):
        store.promote(mutated)


def test_persistence_survives_new_store_instance(tmp_path: Path) -> None:
    db = tmp_path / "shared-memory.sqlite3"
    policy = MemoryWritebackPolicy(minimum_confidence_bps=8000, minimum_evidence_refs=2)
    first_store = MemoryWritebackStore(db, policy=policy)
    candidate = _candidate()
    first_store.promote(candidate)
    first_store.close()

    second_store = MemoryWritebackStore(db, policy=policy)
    item = second_store.get_memory("workspace-a", candidate.memory_key)
    assert item is not None
    assert item.version == 1
    assert {ref.source_id for ref in item.provenance} == {
        "evidence-001",
        "evidence-002",
        "release-001",
    }


def test_two_concurrent_writers_cannot_both_promote_from_same_memory_version(tmp_path: Path) -> None:
    db = tmp_path / "concurrent.sqlite3"
    policy = MemoryWritebackPolicy(minimum_confidence_bps=8000, minimum_evidence_refs=2)
    bootstrap = MemoryWritebackStore(db, policy=policy)
    bootstrap.close()

    candidates = (
        _candidate(candidate_id="race-1", expected_version=0, mode="INSERT"),
        _candidate(candidate_id="race-2", value={"pattern": "competing lesson"}, expected_version=0, mode="INSERT"),
    )

    def attempt(candidate: LearningCandidate) -> str:
        store = MemoryWritebackStore(db, policy=policy)
        try:
            store.promote(candidate)
            return "PROMOTED"
        except MemoryConflictError:
            return "CONFLICT"
        finally:
            store.close()

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(attempt, candidates))

    assert sorted(outcomes) == ["CONFLICT", "PROMOTED"]
    final_store = MemoryWritebackStore(db, policy=policy)
    try:
        item = final_store.get_memory("workspace-a", "audience.trust.pattern")
        assert item is not None
        assert item.version == 1
    finally:
        final_store.close()
