from __future__ import annotations

from dataclasses import replace

from cmf_builder.domain.evidence_index import EvidenceIndex, source_lock_identity_hash
from cmf_builder.domain.evidence_workspace import SourceDescriptor
from tests.stories.st_01_03 import (
    build_context,
    index_command,
    invalidation_command,
)


def test_compiles_one_hundred_thousand_descriptors_deterministically() -> None:
    _, repository, _, run_id, source_receipt = build_context()
    lock = repository.get_source_lock(source_receipt.source_lock_ref)
    assert lock is not None
    descriptors = tuple(
        SourceDescriptor(
            source_id=f"source_{number:06d}",
            canonical_uri=f"repo://synthetic-corpus/{number:06d}.txt",
            relative_path=f"{number:06d}.txt",
            source_kind="file",
            role="governed_task_definition",
            precedence=number + 1,
            authority="repository_owner",
            license="repository_owned_test_fixture",
            privacy_class="non_personal_synthetic",
            media_type="text/plain",
            size_bytes=1,
            observed_mtime=None,
            sha256=f"{number:064x}"[-64:],
            discovered_from="repo://synthetic-corpus",
        )
        for number in range(100_000)
    )
    large_lock = replace(lock, ordered_descriptors=descriptors)
    large_lock = replace(
        large_lock, aggregate_hash=source_lock_identity_hash(large_lock)
    )
    first = EvidenceIndex.create(run_id=run_id, source_lock=large_lock, authority_identity="code-1")
    second = EvidenceIndex.create(run_id=run_id, source_lock=large_lock, authority_identity="code-1")
    assert first.specimen_count == first.descriptor_count == 100_000
    assert first.index_hash == second.index_hash
    assert first.specimens[0].source_id == "source_000000"
    assert first.specimens[-1].source_id == "source_099999"


def test_invalidation_preserves_historical_reproduction_and_clears_active_state() -> None:
    service, repository, _, run_id, _ = build_context()
    receipt = service.index(index_command(run_id))
    index = repository.get_evidence_index(receipt.index_id)
    assert index is not None
    before = index.canonical_bytes()

    invalidation = service.invalidate(invalidation_command(run_id, index.index_id))
    run = repository.load_run(run_id)
    assert run.evidence_index_ref == index.index_id
    assert run.evidence_index_invalidation_ref == invalidation.invalidation_id
    assert repository.is_evidence_index_invalidated(index.index_id)
    assert repository.active_evidence_index(run_id) is None
    assert repository.get_evidence_index(index.index_id).canonical_bytes() == before  # type: ignore[union-attr]
    assert repository.get_evidence_index_invalidation(invalidation.invalidation_id) == invalidation
