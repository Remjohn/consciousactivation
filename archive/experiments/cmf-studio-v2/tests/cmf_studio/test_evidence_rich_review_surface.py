from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.audio import AudioSourceType  # noqa: E402
from ccp_studio.contracts.brand_context import (  # noqa: E402
    BrandContextAssetBundle,
    BrandContextStatus,
    BrandContextVersion,
    brand_context_version_hash,
)
from ccp_studio.contracts.commands import ActorContext, ActorType, CommandStatus, new_command_envelope  # noqa: E402
from ccp_studio.contracts.consent import ConsentScope  # noqa: E402
from ccp_studio.contracts.evaluation_receipts import (  # noqa: E402
    EvaluationCategory,
    EvaluationCategoryInput,
    EvidenceClaimScope,
    EvidencePointer,
)
from ccp_studio.contracts.orchestration import utc_now  # noqa: E402
from ccp_studio.contracts.review_evidence import new_source_reference  # noqa: E402
from ccp_studio.contracts.review_state import EvidenceCompleteness, EvidencePanelType, TelegramComplexity  # noqa: E402
from ccp_studio.contracts.revision import (  # noqa: E402
    RevisionDelta,
    RevisionLineageRefs,
    RevisionRequest,
    RevisionVersion,
    new_revision_receipt,
)
from ccp_studio.contracts.source import SourceArtifactKind  # noqa: E402
from ccp_studio.repositories.brand_context_versions import InMemoryBrandContextRepository  # noqa: E402
from ccp_studio.repositories.revision import InMemoryRevisionRepository  # noqa: E402
from ccp_studio.services.audio_classification import AudioClassificationService  # noqa: E402
from ccp_studio.services.command_bus import create_in_memory_command_bus  # noqa: E402
from ccp_studio.services.consent_service import ConsentService  # noqa: E402
from ccp_studio.services.evaluation_receipt_service import EvaluationReceiptService  # noqa: E402
from ccp_studio.services.review_evidence_service import ReviewEvidenceService  # noqa: E402
from ccp_studio.services.review_state_service import (  # noqa: E402
    ReviewStateError,
    ReviewStateService,
    register_review_state_command_handlers,
)
from ccp_studio.services.source_ingestion import SourceIngestionService  # noqa: E402
from ccp_studio.workflows.review_workflow import ReviewWorkflow  # noqa: E402


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


def _evaluation_inputs(hard_failure: bool = False) -> list[EvaluationCategoryInput]:
    inputs: list[EvaluationCategoryInput] = []
    for category in EvaluationCategory:
        is_failure = hard_failure and category == EvaluationCategory.source_truth
        inputs.append(
            EvaluationCategoryInput(
                category=category,
                score=0.2 if is_failure else 0.94,
                evidence=[
                    EvidencePointer(
                        source_type="transcript_segment" if category == EvaluationCategory.source_truth else "legacy_eval_fixture",
                        source_id="source-artifact-001" if category == EvaluationCategory.source_truth else f"fixture:{category.value}",
                        start_ms=9000 if category == EvaluationCategory.source_truth else None,
                        end_ms=14000 if category == EvaluationCategory.source_truth else None,
                        transcript_segment_id="segment:truth:001" if category == EvaluationCategory.source_truth else None,
                        route="v9_1_evaluation_receipt_doctrine",
                        claim_scope=EvidenceClaimScope.supports,
                    )
                ],
                evaluator_version=f"cmf-{category.value}-critic.v1",
                hard_failure=is_failure,
                hard_failure_code="SOURCE_TRUTH_CONTRADICTION" if is_failure else None,
                hard_failure_message="Rendered claim contradicts the transcript." if is_failure else None,
            )
        )
    return inputs


def _source_fixture():
    source_service = SourceIngestionService()
    org_id = uuid4()
    brand_id = uuid4()
    session_id = uuid4()
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
        retention_policy_id=uuid4(),
        provenance="local recorder",
    )
    report = source_service.evaluate_quality(session_id=session_id, artifact=artifact)
    artifact = source_service.accept_source_artifact(artifact=artifact, report=report)
    return source_service, org_id, brand_id, artifact


def _brand_context(org_id, brand_id) -> tuple[InMemoryBrandContextRepository, BrandContextVersion]:
    repository = InMemoryBrandContextRepository()
    bundle = BrandContextAssetBundle(
        schema_version="cmf.brand_context_asset_bundle.v1",
        acting_library_version_id=uuid4(),
        rig_manifest_id=uuid4(),
        micro_semiotic_anchor_ids=[uuid4()],
        creative_library_receipt_ids=[uuid4()],
    )
    version_hash = brand_context_version_hash(bundle.model_dump(mode="json"))
    version = BrandContextVersion(
        schema_version="cmf.brand_context_version.v1",
        brand_context_version_id=uuid4(),
        organization_id=org_id,
        brand_id=brand_id,
        brand_genesis_session_id=uuid4(),
        status=BrandContextStatus.locked,
        version_hash=version_hash,
        asset_bundle=bundle,
        created_by_actor_id=uuid4(),
        locked_by_actor_id=uuid4(),
        created_at=utc_now(),
        updated_at=utc_now(),
        locked_at=utc_now(),
    )
    repository.put_version(version)
    return repository, version


def _revision_repository(object_type: str, object_id, actor_id) -> InMemoryRevisionRepository:
    repository = InMemoryRevisionRepository()
    lineage = RevisionLineageRefs(
        schema_version="cmf.revision_lineage_refs.v1",
        complete_editing_session_id=uuid4(),
        source_expression_moment_id=uuid4(),
        asset_route_receipt_id=uuid4(),
        brand_context_version_id=uuid4(),
        scene_spec_ids=[uuid4()],
    )
    delta = RevisionDelta(
        field_path="caption_manifest.cues[0].text",
        previous_value_hash="sha256-before",
        new_value_hash="sha256-after",
        reason="tighten source quote without changing meaning",
    )
    request = RevisionRequest(
        schema_version="cmf.revision_request.v1",
        revision_request_id=uuid4(),
        complete_editing_session_id=lineage.complete_editing_session_id,
        requested_by_user_id=actor_id,
        reason="caption repair after evaluation",
        target_object_type=object_type,
        target_object_id=object_id,
        deltas=[delta],
        prior_version_id=uuid4(),
        lineage_refs=lineage,
        evaluation_state="reviewed_for_revision",
        created_at=utc_now(),
    )
    version = RevisionVersion(
        schema_version="cmf.revision_version.v1",
        revision_version_id=uuid4(),
        revision_request_id=request.revision_request_id,
        complete_editing_session_id=request.complete_editing_session_id,
        target_object_type=object_type,
        target_object_id=object_id,
        prior_version_id=request.prior_version_id,
        version_hash="sha256-revision-version",
        lineage_refs=lineage,
        created_at=utc_now(),
    )
    receipt = new_revision_receipt(
        organization_id=uuid4(),
        brand_id=uuid4(),
        actor_id=actor_id,
        revision_request_id=request.revision_request_id,
        prior_version_id=request.prior_version_id,
        new_version_id=version.revision_version_id,
        target_object_type=object_type,
        target_object_id=object_id,
        deltas=[delta],
        lineage_refs=lineage,
        evaluation_state="reviewed_for_revision",
        decision_code="REVISION_REQUESTED",
        evidence_refs=["caption repair after evaluation"],
    )
    repository.put_revision_request(request)
    repository.put_revision_version(version)
    repository.put_receipt(receipt)
    return repository


def _fixture(*, hard_failure: bool = False):
    source_service, org_id, brand_id, artifact = _source_fixture()
    actor_id = uuid4()
    guest_id = uuid4()
    consent_service = ConsentService()
    consent = consent_service.grant_consent(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        scope=_scope(),
        actor_id=actor_id,
        evidence_refs=["consent:review-state"],
    )
    evaluation_service = EvaluationReceiptService()
    object_id = uuid4()
    evaluation = evaluation_service.generate_evaluation_receipt(
        organization_id=org_id,
        brand_id=brand_id,
        object_type="render_output",
        object_id=object_id,
        object_hash="sha256-render-output",
        actor_id=actor_id,
        category_inputs=_evaluation_inputs(hard_failure),
    )
    review_evidence = ReviewEvidenceService(
        consent_repository=consent_service.repository,
        source_repository=source_service.repository,
        evaluation_repository=evaluation_service.repository,
    )
    transcript = review_evidence.append_transcript_revision(
        source_artifact_id=artifact.source_artifact_id,
        revision_number=1,
        transcript_hash="transcript-hash-v1",
        source_hash=artifact.source_hash,
        text_ref="transcripts/session/v1.json",
    )
    audio = AudioClassificationService()
    segment = audio.classify_segment(
        source_type=AudioSourceType.source_voice,
        start_seconds=9.0,
        end_seconds=14.0,
        source_ref=str(artifact.source_artifact_id),
    )
    audio_manifest = audio.create_manifest(render_output_id=object_id, segments=[segment])
    source_reference = new_source_reference(
        source_artifact_id=artifact.source_artifact_id,
        transcript_revision_id=transcript.transcript_revision_id,
        start_seconds=9.0,
        end_seconds=14.0,
        claim_ref="claim:truth:001",
    )
    view = review_evidence.generate_evidence_view(
        organization_id=org_id,
        brand_id=brand_id,
        guest_or_client_id=guest_id,
        object_type="render_output",
        object_id=object_id,
        source_references=[source_reference],
        evaluation_receipt_ids=[evaluation.evaluation_receipt_id],
        audio_mix_manifest_id=audio_manifest.audio_mix_manifest_id,
        file_provenance_refs=["source:sha256-master", "render:sha256-render-output"],
    )
    brand_repo, brand_context = _brand_context(org_id, brand_id)
    revision_repo = _revision_repository("render_output", object_id, actor_id)
    state_service = ReviewStateService(
        review_read_repository=review_evidence.repository,
        consent_repository=consent_service.repository,
        evaluation_repository=evaluation_service.repository,
        revision_repository=revision_repo,
        brand_context_repository=brand_repo,
    )
    return {
        "org_id": org_id,
        "brand_id": brand_id,
        "actor_id": actor_id,
        "guest_id": guest_id,
        "consent": consent,
        "consent_service": consent_service,
        "evaluation": evaluation,
        "evaluation_service": evaluation_service,
        "review_evidence": review_evidence,
        "view": view,
        "brand_context": brand_context,
        "state_service": state_service,
    }


def _build_state(fixture, **overrides):
    values = {
        "organization_id": fixture["org_id"],
        "brand_id": fixture["brand_id"],
        "approval_evidence_view_id": fixture["view"].approval_evidence_view_id,
        "actor_id": fixture["actor_id"],
        "preview_ref": "preview:render-output",
        "source_quote_ref": "quote:truth:001",
        "archetype_route_ref": "route:public-idea-asset",
        "brand_context_version_id": fixture["brand_context"].brand_context_version_id,
        "selected_asset_refs": ["asset:selected:plate", "asset:selected:caption-style"],
        "render_output_refs": ["render:sha256-render-output"],
        "rendered_with_consent_record_version_id": fixture["view"].consent_record_version_id,
        "telegram_complexity_score": 1,
    }
    values.update(overrides)
    return fixture["state_service"].build_review_evidence_state(**values)


def test_review_state_shows_all_required_evidence_panels_and_writes_receipt():
    fixture = _fixture()

    state = _build_state(fixture)
    panels = {panel.panel_type: panel for panel in state.panels}
    receipt = next(iter(fixture["state_service"].repository.receipts.values()))

    assert set(panels) == set(EvidencePanelType)
    assert all(panel.completeness == EvidenceCompleteness.complete for panel in panels.values())
    assert state.consent_snapshot.compatible is True
    assert state.telegram_complexity == TelegramComplexity.quick_allowed
    assert panels[EvidencePanelType.transcript].object_refs[0].endswith("transcript-hash-v1")
    assert receipt.panel_completeness["preview"] == "complete"
    assert receipt.surface_route == state.pwa_route


def test_evaluation_failure_expands_exact_evidence_and_repair_recommendation():
    fixture = _fixture(hard_failure=True)
    state = _build_state(fixture)

    failure = fixture["state_service"].expand_evaluation_failure(
        review_state_id=state.review_state_id,
        category="source_truth",
    )

    assert failure.failure_code == "SOURCE_TRUTH_CONTRADICTION"
    assert failure.evidence_refs[0].startswith("transcript_segment:source-artifact-001")
    assert failure.repair_recommendation == "repair_source_truth"
    assert state.telegram_complexity == TelegramComplexity.pwa_required
    assert state.pwa_deep_link is not None


def test_revision_history_exposes_prior_versions_and_reasons():
    fixture = _fixture()

    state = _build_state(fixture)

    assert len(state.revision_history) == 1
    assert state.revision_history[0].reason == "caption repair after evaluation"
    assert state.revision_history[0].prior_version_id is not None
    assert state.revision_history[0].decision_code == "REVISION_REQUESTED"


def test_changed_consent_after_render_is_flagged_in_review_state():
    fixture = _fixture()
    rendered_with = fixture["view"].consent_record_version_id
    narrowed = fixture["consent_service"].narrow_consent(
        organization_id=fixture["org_id"],
        brand_id=fixture["brand_id"],
        guest_or_client_id=fixture["guest_id"],
        scope=_scope(publication_allowed=False),
        actor_id=fixture["actor_id"],
        evidence_refs=["consent:narrowed-after-render"],
    )
    refreshed_view = fixture["review_evidence"].generate_evidence_view(
        organization_id=fixture["org_id"],
        brand_id=fixture["brand_id"],
        guest_or_client_id=fixture["guest_id"],
        object_type="render_output",
        object_id=fixture["evaluation"].object_id,
        source_references=fixture["view"].source_references,
        evaluation_receipt_ids=[fixture["evaluation"].evaluation_receipt_id],
        audio_mix_manifest_id=fixture["view"].audio_mix_manifest_id,
        file_provenance_refs=fixture["view"].file_provenance_refs,
    )
    fixture["view"] = refreshed_view

    state = _build_state(fixture, rendered_with_consent_record_version_id=rendered_with)

    assert refreshed_view.consent_record_version_id == narrowed.consent_record_version_id
    assert state.consent_snapshot.changed_after_render is True
    assert state.consent_snapshot.compatible is False
    assert "consent_changed_after_render" in state.consent_snapshot.blocker_codes


def test_cross_brand_evaluation_receipt_is_blocked_from_review_state():
    fixture = _fixture()
    other_eval = fixture["evaluation_service"].generate_evaluation_receipt(
        organization_id=uuid4(),
        brand_id=uuid4(),
        object_type="render_output",
        object_id=fixture["evaluation"].object_id,
        object_hash="sha256-cross-brand-render",
        actor_id=fixture["actor_id"],
        category_inputs=_evaluation_inputs(),
    )
    cross_brand_view = fixture["review_evidence"].generate_evidence_view(
        organization_id=fixture["org_id"],
        brand_id=fixture["brand_id"],
        guest_or_client_id=fixture["guest_id"],
        object_type="render_output",
        object_id=fixture["evaluation"].object_id,
        source_references=fixture["view"].source_references,
        evaluation_receipt_ids=[other_eval.evaluation_receipt_id],
        audio_mix_manifest_id=fixture["view"].audio_mix_manifest_id,
        file_provenance_refs=fixture["view"].file_provenance_refs,
    )
    fixture["view"] = cross_brand_view

    with pytest.raises(ReviewStateError) as exc:
        _build_state(fixture)

    assert exc.value.code == "BRAND_SCOPE_VIOLATION"


def test_review_workflow_stage13_builds_evidence_state():
    fixture = _fixture()
    workflow = ReviewWorkflow(revision_service=None, review_state_service=fixture["state_service"])

    state = workflow.stage13_build_evidence_state(
        organization_id=fixture["org_id"],
        brand_id=fixture["brand_id"],
        approval_evidence_view_id=fixture["view"].approval_evidence_view_id,
        actor_id=fixture["actor_id"],
        preview_ref="preview:render-output",
        source_quote_ref="quote:truth:001",
        archetype_route_ref="route:public-idea-asset",
        brand_context_version_id=fixture["brand_context"].brand_context_version_id,
        selected_asset_refs=["asset:selected:plate"],
        render_output_refs=["render:sha256-render-output"],
    )

    assert state.object_id == fixture["evaluation"].object_id
    assert state.review_state_id in fixture["state_service"].repository.states


def test_review_state_command_bus_emits_review_state_receipt_event():
    fixture = _fixture()
    bus = create_in_memory_command_bus()
    bus.brands.add_scope(fixture["org_id"], fixture["brand_id"])
    register_review_state_command_handlers(bus, fixture["state_service"])
    actor = ActorContext(actor_id=fixture["actor_id"], actor_type=ActorType.human, role_ids=["reviewer"])
    envelope = new_command_envelope(
        command_type="BuildReviewEvidenceStateCommand",
        organization_id=fixture["org_id"],
        brand_id=fixture["brand_id"],
        actor=actor,
        payload={
            "approval_evidence_view_id": str(fixture["view"].approval_evidence_view_id),
            "preview_ref": "preview:render-output",
            "source_quote_ref": "quote:truth:001",
            "archetype_route_ref": "route:public-idea-asset",
            "brand_context_version_id": str(fixture["brand_context"].brand_context_version_id),
            "selected_asset_refs": ["asset:selected:plate"],
            "render_output_refs": ["render:sha256-render-output"],
        },
    )

    result = bus.submit(envelope)

    assert result.status == CommandStatus.succeeded
    assert result.result_payload["schema_version"] == "cmf.review_evidence_state.v1"
    assert bus.event_outbox.events[-1].event_type == "BuildReviewEvidenceStateCommand.succeeded"
    assert any(event.event_type == "ReviewStateReceiptRecorded" for event in fixture["state_service"].repository.events)

