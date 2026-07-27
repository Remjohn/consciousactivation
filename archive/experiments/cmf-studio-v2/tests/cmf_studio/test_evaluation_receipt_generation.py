from __future__ import annotations

import sys
from pathlib import Path
from uuid import UUID, uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.audio import AudioSourceType  # noqa: E402
from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.consent import ConsentScope  # noqa: E402
from ccp_studio.contracts.evaluation_receipts import (  # noqa: E402
    EvaluationCategory,
    EvaluationCategoryInput,
    EvaluationDecision,
    EvidenceClaimScope,
    EvidencePointer,
)
from ccp_studio.contracts.review_evidence import ApprovalBlockerCode, new_source_reference  # noqa: E402
from ccp_studio.contracts.source import SourceArtifactKind  # noqa: E402
from ccp_studio.services.audio_classification import AudioClassificationService  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.consent_service import ConsentService  # noqa: E402
from ccp_studio.services.evaluation_receipt_service import (  # noqa: E402
    EvaluationReceiptError,
    EvaluationReceiptService,
    register_evaluation_command_handlers,
)
from ccp_studio.services.review_evidence_service import ReviewEvidenceError, ReviewEvidenceService  # noqa: E402
from ccp_studio.services.source_ingestion import SourceIngestionService  # noqa: E402
from ccp_studio.workflows.evaluation_workflow import EvaluationWorkflow  # noqa: E402


def _scope(**overrides):
    values = {
        "recording_allowed": True,
        "source_storage_allowed": True,
        "likeness_use_allowed": True,
        "derivative_generation_allowed": True,
        "provider_processing_allowed": True,
        "synthetic_voice_eligible": True,
        "reuse_allowed": True,
        "retention_allowed": True,
        "publication_allowed": True,
    }
    values.update(overrides)
    return ConsentScope(**values)


def _evidence(category: EvaluationCategory) -> EvidencePointer:
    return EvidencePointer(
        source_type="transcript_segment" if category == EvaluationCategory.source_truth else "evaluation_fixture",
        source_id="source-artifact-001" if category == EvaluationCategory.source_truth else f"fixture:{category.value}",
        start_ms=12000 if category == EvaluationCategory.source_truth else None,
        end_ms=18500 if category == EvaluationCategory.source_truth else None,
        transcript_segment_id="segment:core-truth:001" if category == EvaluationCategory.source_truth else None,
        route="interview_first_expression_engine",
        claim_scope=EvidenceClaimScope.supports,
        note=f"{category.value} evaluator cites source, CBAR, or legacy critic fixture.",
    )


def _category_inputs(
    *,
    score: float = 0.92,
    hard_failure_category: EvaluationCategory | None = None,
) -> list[EvaluationCategoryInput]:
    inputs: list[EvaluationCategoryInput] = []
    for category in EvaluationCategory:
        is_hard_failure = category == hard_failure_category
        inputs.append(
            EvaluationCategoryInput(
                category=category,
                score=0.21 if is_hard_failure else score,
                evidence=[_evidence(category)],
                evaluator_version=f"cmf-{category.value}-critic.v1",
                hard_failure=is_hard_failure,
                hard_failure_code="SOURCE_TRUTH_CONTRADICTION" if is_hard_failure else None,
                hard_failure_message="Rendered claim contradicts the interview transcript." if is_hard_failure else None,
            )
        )
    return inputs


def _source_fixture():
    source_service = SourceIngestionService()
    org_id = uuid4()
    brand_id = uuid4()
    session_id = uuid4()
    retention_policy_id = uuid4()
    source_service.submit_recording_configuration(
        organization_id=org_id,
        brand_id=brand_id,
        session_id=session_id,
        expected_master_source="local wav master",
        backup_route="secondary recorder",
        platform_source=None,
        upload_method="operator_upload",
        file_safety_expectations=["hash required"],
        quality_requirements=["master wav"],
    )
    artifact = source_service.create_source_artifact(
        organization_id=org_id,
        brand_id=brand_id,
        session_id=session_id,
        kind=SourceArtifactKind.master_recording,
        filename="master.wav",
        content_hash="sha256-master",
        source_hash="sha256-source",
        retention_policy_id=retention_policy_id,
        provenance="local recorder",
    )
    report = source_service.evaluate_quality(session_id=session_id, artifact=artifact)
    artifact = source_service.accept_source_artifact(artifact=artifact, report=report)
    return source_service, org_id, brand_id, artifact


def _review_fixture(evaluation_service: EvaluationReceiptService):
    source_service, org_id, brand_id, artifact = _source_fixture()
    consent_service = ConsentService()
    guest_id = uuid4()
    actor_id = uuid4()
    consent_service.grant_consent(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        scope=_scope(),
        actor_id=actor_id,
        evidence_refs=["consent:evaluation-review"],
    )
    review_service = ReviewEvidenceService(
        consent_repository=consent_service.repository,
        source_repository=source_service.repository,
        evaluation_repository=evaluation_service.repository,
    )
    transcript = review_service.append_transcript_revision(
        source_artifact_id=artifact.source_artifact_id,
        revision_number=1,
        transcript_hash="transcript-hash-v1",
        source_hash=artifact.source_hash,
        text_ref="transcripts/session/v1.json",
    )
    audio = AudioClassificationService()
    segment = audio.classify_segment(
        source_type=AudioSourceType.source_voice,
        start_seconds=12.0,
        end_seconds=18.5,
        source_ref=str(artifact.source_artifact_id),
    )
    audio_manifest = audio.create_manifest(render_output_id=uuid4(), segments=[segment])
    source_reference = new_source_reference(
        source_artifact_id=artifact.source_artifact_id,
        transcript_revision_id=transcript.transcript_revision_id,
        start_seconds=12.0,
        end_seconds=18.5,
        claim_ref="claim:source-truth:001",
    )
    return review_service, org_id, brand_id, guest_id, source_reference, audio_manifest


def _receipt(service: EvaluationReceiptService, **overrides):
    values = {
        "organization_id": uuid4(),
        "brand_id": uuid4(),
        "object_type": "render_output",
        "object_id": uuid4(),
        "object_hash": "sha256-render-output",
        "actor_id": uuid4(),
        "category_inputs": _category_inputs(),
    }
    values.update(overrides)
    return service.generate_evaluation_receipt(**values)


def test_review_ready_render_generates_required_category_receipt_with_evidence():
    service = EvaluationReceiptService()

    receipt = _receipt(service)
    read_model = service.build_review_read_model(receipt.evaluation_receipt_id)

    assert receipt.decision == EvaluationDecision.passes_for_human_review
    assert {score.category for score in receipt.scores} == set(EvaluationCategory)
    assert receipt.receipt_hash
    assert receipt.hard_failures == []
    source_truth = next(score for score in read_model.category_scores if score.category == EvaluationCategory.source_truth)
    assert source_truth.evidence[0].transcript_segment_id == "segment:core-truth:001"
    assert source_truth.evidence[0].start_ms == 12000
    assert source_truth.evaluator_version == "cmf-source_truth-critic.v1"


def test_category_hard_failure_creates_approval_blocker_and_blocks_review_approval():
    evaluation_service = EvaluationReceiptService()
    receipt = _receipt(
        evaluation_service,
        category_inputs=_category_inputs(hard_failure_category=EvaluationCategory.source_truth),
    )
    review_service, org_id, brand_id, guest_id, source_reference, audio_manifest = _review_fixture(evaluation_service)

    view = review_service.generate_evidence_view(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        object_type="render_output",
        object_id=receipt.object_id,
        source_references=[source_reference],
        evaluation_receipt_ids=[receipt.evaluation_receipt_id],
        audio_mix_manifest_id=audio_manifest.audio_mix_manifest_id,
        file_provenance_refs=["source:sha256-master", "render:sha256-render-output"],
    )

    assert receipt.decision == EvaluationDecision.blocked
    assert receipt.hard_failures[0].approval_blocker_code == "evaluation_hard_failure"
    assert any(blocker.blocker_code == ApprovalBlockerCode.evaluation_hard_failure for blocker in view.blockers)
    with pytest.raises(ReviewEvidenceError) as exc:
        review_service.approve_with_evidence(
            approval_evidence_view_id=view.approval_evidence_view_id,
            approved_by_actor_id=uuid4(),
        )
    assert exc.value.code == "EVALUATION_HARD_FAILURE"


def test_receipt_without_evidence_is_invalid_before_persistence():
    service = EvaluationReceiptService()
    invalid = [item.model_copy() for item in _category_inputs()]
    invalid[0] = EvaluationCategoryInput.model_construct(
        category=EvaluationCategory.source_truth,
        score=0.91,
        evidence=[],
        evaluator_version="cmf-source-truth-critic.v1",
        hard_failure=False,
        approval_blocker_code="evaluation_hard_failure",
    )

    with pytest.raises(ValueError):
        _receipt(service, category_inputs=invalid)
    assert service.repository.receipts == {}


def test_incomplete_category_set_is_rejected():
    service = EvaluationReceiptService()
    incomplete = _category_inputs()[:-1]

    with pytest.raises(EvaluationReceiptError) as exc:
        _receipt(service, category_inputs=incomplete)

    assert exc.value.code == "EVALUATION_CATEGORIES_INCOMPLETE"


def test_rerun_after_revision_links_prior_receipt_without_overwriting_history():
    service = EvaluationReceiptService()
    first = _receipt(service, object_hash="sha256-render-v1")

    second = service.rerun_after_revision(
        previous_receipt_id=first.evaluation_receipt_id,
        revised_object_hash="sha256-render-v2",
        actor_id=uuid4(),
        category_inputs=_category_inputs(score=0.96),
    )

    assert second.previous_receipt_id == first.evaluation_receipt_id
    assert first.evaluation_receipt_id in service.repository.receipts
    assert second.evaluation_receipt_id in service.repository.receipts
    assert service.repository.receipts[first.evaluation_receipt_id].object_hash == "sha256-render-v1"
    assert service.repository.latest_for_object(
        organization_id=first.organization_id,
        brand_id=first.brand_id,
        object_type=first.object_type,
        object_id=first.object_id,
    ).evaluation_receipt_id == second.evaluation_receipt_id


def test_command_bus_generates_evaluation_receipt_and_domain_event():
    service = EvaluationReceiptService()
    bus = create_in_memory_command_bus()
    org_id = uuid4()
    brand_id = uuid4()
    bus.brands.add_scope(org_id, brand_id)
    register_evaluation_command_handlers(bus, service)
    object_id = uuid4()
    actor = ActorContext(actor_id=uuid4(), actor_type=ActorType.human, role_ids=["reviewer"])
    envelope = new_command_envelope(
        command_type="GenerateEvaluationReceiptCommand",
        organization_id=org_id,
        brand_id=brand_id,
        actor=actor,
        payload={
            "object_type": "asset_package",
            "object_id": str(object_id),
            "object_hash": "sha256-asset-package",
            "category_inputs": [item.model_dump(mode="json") for item in _category_inputs()],
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert UUID(result.result_payload["object_id"]) == object_id
    assert result.result_payload["decision"] == EvaluationDecision.passes_for_human_review.value
    assert bus.event_outbox.events[-1].event_type == "GenerateEvaluationReceiptCommand.succeeded"
    assert any(event.event_type == "EvaluationReceiptCreated" for event in service.repository.events)


def test_evaluation_workflow_stage13_returns_receipt_for_review():
    service = EvaluationReceiptService()
    workflow = EvaluationWorkflow(service)

    receipt = workflow.stage13_generate_receipts(
        organization_id=uuid4(),
        brand_id=uuid4(),
        object_type="scene_output",
        object_id=uuid4(),
        object_hash="sha256-scene-output",
        actor_id=uuid4(),
        category_inputs=[item.model_dump(mode="json") for item in _category_inputs(score=0.9)],
    )

    assert receipt.object_type.value == "scene_output"
    assert receipt.decision == EvaluationDecision.passes_for_human_review
    assert receipt.evaluation_receipt_id in service.repository.receipts

