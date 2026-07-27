from __future__ import annotations

from cmf_builder.domain.evidence_index import KnowledgeStatus, SpecimenStatus
from tests.stories.st_01_03 import build_context, index_command


def test_complete_queryable_inventory_distinguishes_evidence_facets() -> None:
    service, repository, _, run_id, source_receipt = build_context()
    receipt = service.index(index_command(run_id))

    run = repository.load_run(run_id)
    index = repository.get_evidence_index(receipt.index_id)
    assert index is not None
    assert run.evidence_index_ref == index.index_id
    assert run.evidence_index_hash == index.index_hash
    assert index.source_lock_ref == source_receipt.source_lock_ref
    assert index.descriptor_count == index.specimen_count == 1
    specimen = index.specimens[0]
    assert specimen.observation.observed_size_bytes > 0
    assert specimen.governed_status is SpecimenStatus.ACTIVE
    assert specimen.knowledge_status is KnowledgeStatus.OBSERVED
    assert specimen.provenance.source_lock_ref == source_receipt.source_lock_ref
    assert specimen.observation != specimen.governed_status
    assert specimen.knowledge_status != specimen.provenance

    assert repository.query_evidence_index(index.index_id, specimen_id=specimen.specimen_id) == (specimen,)
    assert repository.query_evidence_index(index.index_id, source_id=specimen.source_id) == (specimen,)
    assert repository.query_evidence_index(index.index_id, role=specimen.role) == (specimen,)
    assert repository.query_evidence_index(index.index_id, governed_status="ACTIVE") == (specimen,)
    assert repository.query_evidence_index(index.index_id, knowledge_status="OBSERVED") == (specimen,)


def test_receipt_and_run_event_bind_exact_index_source_and_authority() -> None:
    service, repository, _, run_id, source_receipt = build_context()
    receipt = service.index(index_command(run_id))
    index = repository.get_evidence_index(receipt.index_id)
    stored = repository.get_evidence_index_receipt(receipt.receipt_id)
    run = repository.load_run(run_id)

    assert index is not None and stored == receipt
    receipt.validate(index)
    event = run.events[-1]
    assert event.event_type == "EvidenceIndexAttached"
    assert event.actor_id == receipt.authority_identity == index.authority_identity == "code-1"
    assert event.value("index_ref") == index.index_id
    assert event.value("index_hash") == index.index_hash
    assert event.value("source_lock_ref") == source_receipt.source_lock_ref
    assert receipt.event_ids == (event.event_id,)
