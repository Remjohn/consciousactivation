from __future__ import annotations

from dataclasses import replace

import pytest

from cmf_builder.domain.evidence_index import (
    EvidenceIndex,
    EvidenceIndexIncomplete,
    EvidenceIdentityCollision,
    EvidenceProvenanceInvalid,
    KnowledgeStatus,
    source_lock_identity_hash,
)
from tests.stories.st_01_03 import build_context, index_command


def test_fresh_contexts_produce_byte_identical_index_and_receipt() -> None:
    outputs = []
    for _ in range(2):
        service, repository, _, run_id, _ = build_context(seed="fresh-equality")
        receipt = service.index(index_command(run_id))
        index = repository.get_evidence_index(receipt.index_id)
        assert index is not None
        outputs.append((index.canonical_bytes(), receipt.canonical_bytes()))
    assert outputs[0] == outputs[1]


def test_changed_descriptor_produces_new_identity() -> None:
    _, repository, _, run_id, source_receipt = build_context()
    lock = repository.get_source_lock(source_receipt.source_lock_ref)
    assert lock is not None
    first = EvidenceIndex.create(run_id=run_id, source_lock=lock, authority_identity="code-1")
    descriptor = replace(lock.ordered_descriptors[0], sha256="1" * 64)
    changed_lock = replace(lock, ordered_descriptors=(descriptor,))
    changed_lock = replace(
        changed_lock, aggregate_hash=source_lock_identity_hash(changed_lock)
    )
    second = EvidenceIndex.create(run_id=run_id, source_lock=changed_lock, authority_identity="code-1")
    assert first.index_id != second.index_id
    assert first.index_hash != second.index_hash


def test_incomplete_or_colliding_specimen_inventory_fails_closed() -> None:
    _, repository, _, run_id, source_receipt = build_context()
    lock = repository.get_source_lock(source_receipt.source_lock_ref)
    assert lock is not None
    index = EvidenceIndex.create(run_id=run_id, source_lock=lock, authority_identity="code-1")
    with pytest.raises(EvidenceIndexIncomplete):
        replace(index, descriptor_count=2).validate(lock)
    duplicate = replace(lock.ordered_descriptors[0], canonical_uri="repo://duplicate")
    colliding_lock = replace(lock, ordered_descriptors=(lock.ordered_descriptors[0], duplicate))
    colliding_lock = replace(
        colliding_lock, aggregate_hash=source_lock_identity_hash(colliding_lock)
    )
    with pytest.raises(EvidenceIdentityCollision):
        EvidenceIndex.create(run_id=run_id, source_lock=colliding_lock, authority_identity="code-1")


def test_unsupported_or_missing_knowledge_provenance_fails_closed() -> None:
    _, repository, _, run_id, source_receipt = build_context()
    lock = repository.get_source_lock(source_receipt.source_lock_ref)
    assert lock is not None
    index = EvidenceIndex.create(run_id=run_id, source_lock=lock, authority_identity="code-1")
    specimen = index.specimens[0]
    with pytest.raises(ValueError):
        replace(specimen, knowledge_status="ASSUMED").validate()
    with pytest.raises(EvidenceProvenanceInvalid):
        replace(specimen, provenance=replace(specimen.provenance, source_lock_ref="")).validate()
    assert specimen.knowledge_status is KnowledgeStatus.OBSERVED
