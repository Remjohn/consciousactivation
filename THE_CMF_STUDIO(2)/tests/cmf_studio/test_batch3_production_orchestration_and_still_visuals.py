from __future__ import annotations

import sys
from pathlib import Path
from uuid import uuid4

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ccp_studio.contracts.composition_runtime import ApprovalStatus  # noqa: E402
from ccp_studio.contracts.production_orchestration import (  # noqa: E402
    CapabilityRouteRequest,
    FootageCandidate,
    RenderRuntimeCandidate,
    RenderRuntimeSelectionRequest,
    production_hash,
)
from ccp_studio.services.production_orchestration_service import (  # noqa: E402
    ProductionOrchestrationService,
)
from ccp_studio.services.still_visual_program_service import (  # noqa: E402
    StillVisualProgramService,
    StillVisualProgramServiceError,
)


def _production_service() -> ProductionOrchestrationService:
    return ProductionOrchestrationService()


def _still_visual_service() -> StillVisualProgramService:
    return StillVisualProgramService()


def test_batch3_production_manifest_openmontage_stage_director_is_source_receipt_backed():
    service = _production_service()

    candidate, decision = service.register_openmontage_reference()
    blocked_candidate, blocked_decision = service.register_openmontage_reference(direct_import_requested=True)
    draft = service.create_manifest_draft()
    snapshot = service.validate_manifest(draft)
    activation = service.activate_manifest(snapshot)
    skill_spec = service.register_stage_skill(stage_code="STAGE-COMPILE")
    context, command, output, receipt = service.invoke_stage_skill(
        skill_spec=skill_spec,
        manifest_snapshot_id=snapshot.production_pipeline_manifest_snapshot_id,
        source_context_refs=["source:transcript-beat-map", "source:brand-context"],
        requested_output_artifact_type="stage_artifact",
    )
    _, _, blocked_output, blocked_receipt = service.invoke_stage_skill(
        skill_spec=skill_spec,
        manifest_snapshot_id=snapshot.production_pipeline_manifest_snapshot_id,
        source_context_refs=["source:transcript-beat-map"],
        requested_output_artifact_type="unauthorized_output",
    )

    assert candidate.repo_url.endswith("/OpenMontage")
    assert decision.decision == "architectural_reference_only"
    assert "stage_graph" in decision.adopted_patterns
    assert blocked_candidate.direct_import_requested is True
    assert blocked_decision.decision == "blocked"
    assert "OPENMONTAGE_DIRECT_IMPORT_BLOCKED" in blocked_decision.blocker_codes
    assert snapshot.continuity_gate_passed is True
    assert activation.decision == "approved"
    assert service.repository.manifest_snapshots[snapshot.production_pipeline_manifest_snapshot_id].active is True
    assert context.manifest_snapshot_id == snapshot.production_pipeline_manifest_snapshot_id
    assert command.skill_ref == skill_spec.skill_ref
    assert output is not None
    assert output.source_refs == ["source:transcript-beat-map", "source:brand-context"]
    assert receipt.decision == "approved"
    assert blocked_output is None
    assert blocked_receipt.decision == "blocked"
    assert "STAGE_SKILL_OUTPUT_TYPE_NOT_ALLOWED" in blocked_receipt.blocker_codes


def test_batch3_provider_workspace_footage_and_runtime_locking_are_governed():
    service = _production_service()

    service.register_capability(
        provider_code="skia-renderer",
        capability_kind="rendering",
        tool_ref="skia:deterministic",
        cost_class="low",
        reproducibility_score=0.98,
        doctrine_fit_score=0.93,
        source_scope="internal",
    )
    service.register_capability(
        provider_code="blocked-cloud-renderer",
        capability_kind="rendering",
        tool_ref="external:cloud-renderer",
        cost_class="high",
        reproducibility_score=0.6,
        doctrine_fit_score=0.7,
        source_scope="external",
        available=False,
    )
    menu = service.build_provider_menu()
    route_request = CapabilityRouteRequest(
        required_capability_kind="rendering",
        source_scope_allowed=["internal", "self_hosted"],
        max_cost_class="medium",
        minimum_reproducibility_score=0.9,
        minimum_doctrine_fit_score=0.84,
        evidence_refs=["composition_program:still-visual-001"],
    )
    route = service.route_provider(route_request, menu)

    draft = service.create_manifest_draft()
    snapshot = service.validate_manifest(draft)
    workspace = service.create_workspace(
        organization_id=uuid4(),
        brand_id=uuid4(),
        guest_id=uuid4(),
        manifest_snapshot_id=snapshot.production_pipeline_manifest_snapshot_id,
    )
    slot, checkpoint = service.checkpoint_workspace(
        workspace_id=workspace.production_workspace_id,
        stage_code="STAGE-COMPILE",
        artifact_ref="artifact:provider-plan",
    )
    resume = service.resume_workspace(workspace_id=workspace.production_workspace_id)
    _, source_classification, source_inspection = service.intake_reference_media(
        media_ref="media://guest-interview.mp4",
        declared_use_mode="source_footage",
        source_evidence_refs=["consent-form:guest-001", "asset-contract:guest-001"],
        consent_scope_ref="consent:guest-pack-001",
    )
    _, blocked_classification, _ = service.intake_reference_media(
        media_ref="media://unknown.mp4",
        declared_use_mode="source_footage",
        source_evidence_refs=["drive:file:unknown"],
    )
    search, candidates = service.search_footage(
        query="quiet library archival plate",
        visual_role="memory_object_insert",
        allowed_license_families=["CC0", "CMF-owned"],
    )
    selection = service.select_footage(candidates[0], allowed_license_families=["CC0"])
    blocked_candidate = FootageCandidate(
        search_request_id=search.footage_search_request_id,
        source_url="https://source.example/restricted",
        license_family="restricted",
        media_hash=production_hash({"restricted": True}),
        relevance_score=0.91,
        visual_role="memory_object_insert",
        evidence_refs=["license:restricted"],
    )
    blocked_selection = service.select_footage(blocked_candidate, allowed_license_families=["CC0"])
    runtime_request = RenderRuntimeSelectionRequest(
        output_type="still_image",
        source_program_ref="still_visual_program:001",
        allowed_runtime_codes=["skia", "remotion"],
        minimum_replay_score=0.9,
    )
    lock = service.select_and_lock_runtime(
        runtime_request,
        [
            RenderRuntimeCandidate(
                runtime_code="skia",
                supported_output_types=["still_image", "storyboard_frame"],
                deterministic_replay_score=0.98,
                cost_class="low",
            ),
            RenderRuntimeCandidate(
                runtime_code="remotion",
                supported_output_types=["video"],
                deterministic_replay_score=0.91,
                cost_class="medium",
            ),
        ],
    )
    drift_ok = service.check_runtime_drift(lock=lock)
    drift_blocked = service.check_runtime_drift(lock=lock, observed_runtime_hash=production_hash({"runtime": "changed"}))

    assert route.decision == "approved"
    assert route.selected_provider_code == "skia-renderer"
    assert any("PROVIDER_NOT_AVAILABLE" in score.blocker_codes for score in route.candidate_scores)
    assert slot.artifact_ref == "artifact:provider-plan"
    assert checkpoint.valid is True
    assert resume.decision == "resume"
    assert source_classification.downstream_use_allowed is True
    assert source_inspection.transcription_ready is True
    assert blocked_classification.downstream_use_allowed is False
    assert "SOURCE_FOOTAGE_CONSENT_SCOPE_MISSING" in blocked_classification.blocker_codes
    assert selection.decision == "approved"
    assert blocked_selection.decision == "blocked"
    assert "FOOTAGE_LICENSE_EVIDENCE_BLOCKED" in blocked_selection.blocker_codes
    assert lock.runtime_code == "skia"
    assert drift_ok.decision == "approved"
    assert drift_blocked.decision == "blocked"
    assert "RENDER_RUNTIME_DRIFT_DETECTED" in drift_blocked.blocker_codes


def test_batch3_qa_budget_approval_blocks_low_integrity_outputs():
    service = _production_service()
    workspace_id = uuid4()
    reviewer_id = uuid4()

    precompose, repair_plan = service.run_pre_compose_gate(
        delivery_promise_id=uuid4(),
        risk_score=0.24,
        runtime_lock_ref="runtime_lock:skia",
        eval_refs=["eval:primitive", "eval:doctrine"],
    )
    blocked_precompose, blocked_repair_plan = service.run_pre_compose_gate(
        delivery_promise_id=uuid4(),
        risk_score=0.81,
        runtime_lock_ref="",
        eval_refs=[],
    )
    expected_hash = production_hash({"render": "clean"})
    _, clean_probe, clean_qa, clean_repair = service.run_post_render_qa(
        render_ref="render://asset/clean.mp4",
        runtime_lock_ref="runtime_lock:remotion",
        source_program_ref="video_edit_program:001",
        expected_render_hash=expected_hash,
    )
    _, overlap_probe, overlap_qa, overlap_repair = service.run_post_render_qa(
        render_ref="render://asset/overlap.mp4",
        runtime_lock_ref="runtime_lock:remotion",
        source_program_ref="video_edit_program:002",
        expected_render_hash=expected_hash,
        text_overlap_detected=True,
    )
    approved_estimate = service.estimate_budget(
        workspace_id=workspace_id,
        provider_code="skia-renderer",
        estimated_units=10,
        estimated_cost_usd=12,
        cap_usd=20,
    )
    reservation = service.reserve_budget(approved_estimate)
    reconciliation = service.reconcile_budget(reservation, actual_cost_usd=13)
    blocked_estimate = service.estimate_budget(
        workspace_id=workspace_id,
        provider_code="external-video-renderer",
        estimated_units=100,
        estimated_cost_usd=120,
        cap_usd=20,
    )
    artifact, review_request = service.create_artifact_review(
        workspace_id=workspace_id,
        stage_code="STAGE-QA",
        artifact_ref="artifact:rendered-output",
        reviewer_id=reviewer_id,
        source_refs=["transcript:001", "brand_context:001"],
    )
    warning = service.add_reviewer_finding(
        review_request_id=review_request.stage_artifact_review_request_id,
        severity="warning",
        finding_code="CAPTION_WEIGHT_NEEDS_POLISH",
        message="Caption styling should be refined before final package handoff.",
    )
    critical = service.add_reviewer_finding(
        review_request_id=review_request.stage_artifact_review_request_id,
        severity="critical",
        finding_code="SOURCE_TRUTH_UNVERIFIED",
        message="The artifact makes a claim without source backing.",
    )
    approval = service.decide_human_approval(
        review_request_id=review_request.stage_artifact_review_request_id,
        reviewer_id=reviewer_id,
        approve=True,
    )
    waived_artifact, waived_review_request = service.create_artifact_review(
        workspace_id=workspace_id,
        stage_code="STAGE-QA",
        artifact_ref="artifact:waived-output",
        reviewer_id=reviewer_id,
        source_refs=["transcript:002"],
    )
    service.add_reviewer_finding(
        review_request_id=waived_review_request.stage_artifact_review_request_id,
        severity="critical",
        finding_code="NON_BLOCKING_EDITORIAL_NOTE",
        message="Approved with explicit waiver.",
        waived=True,
    )
    waived_approval = service.decide_human_approval(
        review_request_id=waived_review_request.stage_artifact_review_request_id,
        reviewer_id=reviewer_id,
        approve=True,
    )

    assert precompose.decision == "approved"
    assert repair_plan is None
    assert blocked_precompose.decision == "blocked"
    assert blocked_repair_plan is not None
    assert "PRECOMPOSE_SLIDESHOW_RISK" in blocked_precompose.blocker_codes
    assert clean_probe.text_overlap_detected is False
    assert clean_qa.decision == "approved"
    assert clean_repair is None
    assert overlap_probe.text_overlap_detected is True
    assert overlap_qa.decision == "blocked"
    assert overlap_repair is not None
    assert "POST_RENDER_TEXT_OVERLAP" in overlap_qa.blocker_codes
    assert approved_estimate.decision == "approved"
    assert reservation.decision == "approved"
    assert reconciliation.decision == "approved"
    assert blocked_estimate.decision == "blocked"
    assert artifact.source_refs == ["transcript:001", "brand_context:001"]
    assert warning.severity == "warning"
    assert critical.severity == "critical"
    assert approval.decision == "blocked"
    assert "SOURCE_TRUTH_UNVERIFIED" in approval.blocker_codes
    assert waived_artifact.artifact_ref == "artifact:waived-output"
    assert waived_approval.decision == "approved"


def test_batch3_still_visual_workbench_runs_full_supervisual_operator_lifecycle():
    service = _still_visual_service()
    operator_id = uuid4()

    program = service.create_program(
        workspace_id=uuid4(),
        brand_context_version_ref="brand_context:claude:v1",
        source_evidence_refs=["transcript:moment-001", "primitive_eval:edge-001"],
        target_format_family="supervisual",
        package_slot="monthly-pack:slot-01",
    )
    routed = service.route_program(
        program_id=program.still_visual_composition_program_id,
        archetype_ref="archetype.challenger_frame_breaker.v1",
        target_subtype_hint="SPV-CON",
    )
    materialized = service.materialize_program(program_id=program.still_visual_composition_program_id)
    rendered = service.render_program(program_id=program.still_visual_composition_program_id)
    evaluated = service.evaluate_program(program_id=program.still_visual_composition_program_id)
    read_model = service.build_review_read_model(program_id=program.still_visual_composition_program_id)
    telegram_card = service.build_telegram_card(program_id=program.still_visual_composition_program_id)
    approval = service.approve_program(program_id=program.still_visual_composition_program_id, operator_id=operator_id)
    export = service.export_program(program_id=program.still_visual_composition_program_id)
    final_program = service.repository.programs[program.still_visual_composition_program_id]

    assert program.request.source_evidence_refs == ["transcript:moment-001", "primitive_eval:edge-001"]
    assert routed.family_route is not None
    assert routed.family_route.selected_builder_ref == "SuperVisualSingleImageSkiaBuilder"
    assert routed.family_route.grammar_binding_ref is not None
    assert len(routed.family_route.primitive_validation_ids) >= 3
    assert materialized.provider_plan is not None
    assert materialized.provider_plan.final_authority == "cmf_skia_renderer"
    assert any("ideogram_4" in ref for ref in materialized.provider_plan.provider_job_refs)
    assert rendered.render_manifest is not None
    assert rendered.render_manifest.deterministic_replay_required is True
    assert evaluated.eval_summary is not None
    assert evaluated.eval_summary.decision == "approved"
    assert read_model.approval_eligible is True
    assert read_model.blockers == []
    assert telegram_card.blocker_count == 0
    assert {"approve", "revise", "export"}.issubset(set(telegram_card.commands))
    assert approval.decision == "approved"
    assert final_program.approval_status == ApprovalStatus.approved
    assert export.exported_asset_refs == [rendered.render_manifest.render_ref]
    assert export.package_handoff_ref.startswith("package_handoff:still-visual:")


def test_batch3_still_visual_workbench_blocks_missing_route_source_truth_and_unapproved_export():
    service = _still_visual_service()
    program = service.create_program(
        workspace_id=uuid4(),
        brand_context_version_ref="brand_context:claude:v1",
        source_evidence_refs=["transcript:moment-002"],
        target_format_family="supervisual",
        package_slot="monthly-pack:slot-02",
    )

    with pytest.raises(StillVisualProgramServiceError) as route_exc:
        service.materialize_program(program_id=program.still_visual_composition_program_id)
    assert route_exc.value.code == "STILL_VISUAL_ROUTE_REQUIRED"

    service.route_program(program_id=program.still_visual_composition_program_id, target_subtype_hint="SPV-CON")
    service.materialize_program(program_id=program.still_visual_composition_program_id)
    service.render_program(program_id=program.still_visual_composition_program_id)
    evaluated = service.evaluate_program(program_id=program.still_visual_composition_program_id, source_truth_score=0.52)
    read_model = service.build_review_read_model(program_id=program.still_visual_composition_program_id)
    approval = service.approve_program(program_id=program.still_visual_composition_program_id, operator_id=uuid4())
    revision = service.revise_program(
        program_id=program.still_visual_composition_program_id,
        revision_scope="primitive",
        reason="Repair source-truth and primitive evidence before operator approval.",
    )

    with pytest.raises(StillVisualProgramServiceError) as export_exc:
        service.export_program(program_id=program.still_visual_composition_program_id)

    assert evaluated.eval_summary is not None
    assert evaluated.eval_summary.decision == "blocked"
    assert "STILL_VISUAL_SOURCE_TRUTH_BELOW_THRESHOLD" in evaluated.eval_summary.blocker_codes
    assert read_model.approval_eligible is False
    assert "STILL_VISUAL_SOURCE_TRUTH_BELOW_THRESHOLD" in read_model.blockers
    assert "revise-source-evidence" in read_model.repair_commands
    assert approval.decision == "blocked"
    assert "STILL_VISUAL_SOURCE_TRUTH_BELOW_THRESHOLD" in approval.blocker_codes
    assert revision.command_ref.startswith("command:still-visual-revision:")
    assert export_exc.value.code == "STILL_VISUAL_APPROVAL_REQUIRED"
