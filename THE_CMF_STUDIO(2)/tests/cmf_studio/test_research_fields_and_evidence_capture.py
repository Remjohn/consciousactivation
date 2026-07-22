from __future__ import annotations

import sys
from datetime import timedelta
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.research import (  # noqa: E402
    EvidenceCitation,
    ResearchEvidenceStatus,
    SourceRole,
    TemporalSensitivity,
)
from ccp_studio.services.research_service import ResearchService, ResearchServiceError  # noqa: E402
from ccp_studio.workflows.interview_preparation import InterviewPreparationWorkflow  # noqa: E402


def _citation(title="Primary interview article", source_hash="sha256-source"):
    return EvidenceCitation(
        schema_version="cmf.evidence_citation.v1",
        citation_id=uuid4(),
        uri="https://example.com/source",
        title=title,
        retrieved_at=utc_now(),
        quoted_span_ref="paragraph-3",
        source_hash=source_hash,
    )


def _field(service, org_id=None, brand_id=None, actor_id=None):
    org_id = org_id or uuid4()
    brand_id = brand_id or uuid4()
    actor_id = actor_id or uuid4()
    field = service.create_field(
        organization_id=org_id,
        brand_id=brand_id,
        guest_id=uuid4(),
        objective="Find the real tension behind founder burnout language.",
        source_scope=["public interviews", "guest notes", "CRAL signals"],
        created_by_actor_id=actor_id,
    )
    return org_id, brand_id, actor_id, field


def test_evidence_records_claim_source_citation_confidence_temporal_provenance_and_receipt():
    service = ResearchService()
    org_id, brand_id, actor_id, field = _field(service)
    evidence = service.attach_evidence(
        organization_id=org_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        claim="The guest frames burnout as nervous-system loyalty rather than weakness.",
        source_role=SourceRole.primary_source,
        citations=[_citation()],
        confidence=0.88,
        temporal_sensitivity=TemporalSensitivity.low,
        provenance_summary="Derived from a cited public interview and retained as claim-level evidence.",
        contradiction_notes=["burnout framed as failure vs loyalty"],
        created_by_actor_id=actor_id,
        primitive_family_hints=["meaning_reframe"],
    )

    ready = service.validate_evidence_provenance(
        organization_id=org_id,
        brand_id=brand_id,
        evidence_id=evidence.evidence_id,
        validator_actor_id=actor_id,
    )
    approved = service.approve_evidence(
        organization_id=org_id,
        brand_id=brand_id,
        evidence_id=evidence.evidence_id,
        validator_actor_id=actor_id,
    )
    receipt = next(receipt for receipt in service.repository.receipts.values() if receipt.decision_code == "RESEARCH_EVIDENCE_APPROVED")

    assert ready.status == ResearchEvidenceStatus.provenance_ready
    assert approved.status == ResearchEvidenceStatus.approved_for_use
    assert approved.claim.startswith("The guest frames burnout")
    assert approved.citations[0].source_hash == "sha256-source"
    assert approved.confidence == 0.88
    assert approved.provenance_summary
    assert receipt.evidence_ids == [evidence.evidence_id]
    assert receipt.citation_hashes


def test_temporal_evidence_is_marked_for_freshness_review_when_reused_after_expiry():
    service = ResearchService()
    org_id, brand_id, actor_id, field = _field(service)
    evidence = service.attach_evidence(
        organization_id=org_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        claim="A recent audience survey shows founders cite performance anxiety this quarter.",
        source_role=SourceRole.audience_signal,
        citations=[_citation(title="Quarterly audience survey", source_hash="sha256-survey")],
        confidence=0.8,
        temporal_sensitivity=TemporalSensitivity.high,
        freshness_due_at=utc_now() + timedelta(days=1),
        provenance_summary="Survey source has a date and must be refreshed before reuse.",
        contradiction_notes=["high stated confidence vs low recording completion"],
        created_by_actor_id=actor_id,
    )
    service.validate_evidence_provenance(
        organization_id=org_id,
        brand_id=brand_id,
        evidence_id=evidence.evidence_id,
        validator_actor_id=actor_id,
    )
    approved = service.approve_evidence(
        organization_id=org_id,
        brand_id=brand_id,
        evidence_id=evidence.evidence_id,
        validator_actor_id=actor_id,
    )
    expired = approved.model_copy(update={"freshness_due_at": utc_now() - timedelta(seconds=1)})
    service.repository.put_evidence(expired)

    with pytest.raises(ResearchServiceError) as exc:
        service.prepare_downstream_evidence_inputs(
            organization_id=org_id,
            brand_id=brand_id,
            evidence_ids=[approved.evidence_id],
        )

    assert exc.value.code == "RESEARCH_EVIDENCE_FRESHNESS_REVIEW_REQUIRED"
    assert service.repository.evidence[approved.evidence_id].status == ResearchEvidenceStatus.stale_review_required


def test_evidence_without_provenance_remains_draft_and_cannot_support_asset_contracts():
    service = ResearchService()
    org_id, brand_id, actor_id, field = _field(service)
    evidence = service.attach_evidence(
        organization_id=org_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        claim="Founders hate camera work.",
        source_role=SourceRole.public_context,
        citations=[],
        confidence=0.62,
        temporal_sensitivity=TemporalSensitivity.evergreen,
        provenance_summary="",
        created_by_actor_id=actor_id,
    )

    draft = service.validate_evidence_provenance(
        organization_id=org_id,
        brand_id=brand_id,
        evidence_id=evidence.evidence_id,
        validator_actor_id=actor_id,
    )

    assert draft.status == ResearchEvidenceStatus.draft
    with pytest.raises(ResearchServiceError) as exc:
        service.approve_evidence(
            organization_id=org_id,
            brand_id=brand_id,
            evidence_id=evidence.evidence_id,
            validator_actor_id=actor_id,
        )
    assert exc.value.code == "RESEARCH_EVIDENCE_PROVENANCE_REQUIRED"


def test_brand_scope_prevents_research_evidence_leakage():
    service = ResearchService()
    org_id, brand_id, actor_id, field = _field(service)
    evidence = service.attach_evidence(
        organization_id=org_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        claim="The audience wants practical language, not abstract mindset content.",
        source_role=SourceRole.audience_signal,
        citations=[_citation()],
        confidence=0.76,
        temporal_sensitivity=TemporalSensitivity.low,
        provenance_summary="Audience comment cluster with cited source hash.",
        contradiction_notes=["practical demand vs abstract existing content"],
        created_by_actor_id=actor_id,
    )

    with pytest.raises(ResearchServiceError) as exc:
        service.validate_evidence_provenance(
            organization_id=org_id,
            brand_id=uuid4(),
            evidence_id=evidence.evidence_id,
            validator_actor_id=actor_id,
        )

    assert exc.value.code == "BRAND_SCOPE_VIOLATION"


def test_frozen_research_snapshot_retains_approved_evidence_ids_and_receipts_for_downstream_compilers():
    service = ResearchService()
    org_id, brand_id, actor_id, field = _field(service)
    evidence = service.attach_evidence(
        organization_id=org_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        claim="CRAL signal: the market believes recording resistance is laziness, while guests experience it as exposure risk.",
        source_role=SourceRole.cral_signal,
        citations=[_citation(title="CRAL research note", source_hash="sha256-cral")],
        confidence=0.86,
        temporal_sensitivity=TemporalSensitivity.medium,
        freshness_due_at=utc_now() + timedelta(days=30),
        provenance_summary="CRAL-labeled contradiction from source-backed research note.",
        contradiction_notes=["laziness story vs exposure risk reality"],
        created_by_actor_id=actor_id,
        primitive_family_hints=["exposure", "trust", "reframe"],
    )
    service.validate_evidence_provenance(
        organization_id=org_id,
        brand_id=brand_id,
        evidence_id=evidence.evidence_id,
        validator_actor_id=actor_id,
    )
    service.approve_evidence(
        organization_id=org_id,
        brand_id=brand_id,
        evidence_id=evidence.evidence_id,
        validator_actor_id=actor_id,
    )
    workflow = InterviewPreparationWorkflow(service)

    snapshot = workflow.stage3_collect_research_evidence(
        organization_id=org_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        evidence_ids=[evidence.evidence_id],
        actor_id=actor_id,
    )

    assert snapshot.approved_evidence_ids == [evidence.evidence_id]
    assert snapshot.research_evidence_receipt_ids
    assert snapshot.saturation_quality == "rscs_saturated"
    assert snapshot.research_snapshot_id in service.repository.fields[field.research_field_id].frozen_snapshot_ids


def test_rscs_gate_keeps_unsupported_inference_as_research_gap_instead_of_fact():
    service = ResearchService()
    org_id, brand_id, actor_id, field = _field(service)
    evidence = service.attach_evidence(
        organization_id=org_id,
        brand_id=brand_id,
        research_field_id=field.research_field_id,
        claim="This audience is obviously afraid of visibility.",
        source_role=SourceRole.inference,
        citations=[_citation(title="Thin source", source_hash="sha256-thin")],
        confidence=0.41,
        temporal_sensitivity=TemporalSensitivity.evergreen,
        provenance_summary="Single weak source and no contradiction scan.",
        contradiction_notes=[],
        research_gap=False,
        created_by_actor_id=actor_id,
    )

    draft = service.validate_evidence_provenance(
        organization_id=org_id,
        brand_id=brand_id,
        evidence_id=evidence.evidence_id,
        validator_actor_id=actor_id,
    )

    assert draft.status == ResearchEvidenceStatus.draft
    receipt_codes = {receipt.decision_code for receipt in service.repository.receipts.values()}
    assert "INFERENCE_CONTRADICTION_NOTES_REQUIRED" in receipt_codes
