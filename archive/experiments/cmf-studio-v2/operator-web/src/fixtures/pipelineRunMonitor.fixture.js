const now = new Date("2026-07-04T00:00:00.000Z").toISOString();

export const pipelineRunMonitorFixture = {
  schema_version: "cmf.pipeline_run_monitor.v1",
  run_status: {
    pipeline_run_id: "pipeline_run_format02_health_myth_demo",
    orchestration_run_id: "orch_format02_pipeline_monitor_demo",
    golden_path_run_id: "golden_path_health_myth_demo",
    recipe_id: "format02_golden_path",
    recipe_version: "1.0.0",
    brand_context_version_id: "bcv_health_myth_demo_v1",
    workspace_id: "workspace_health_myth_demo",
    status: "blocked",
    started_at: now,
    completed_at: null,
    current_step_id: "provider_samples",
    progress_percent: 56,
    source_mode: "fixture",
    blocker_count: 1,
    pending_approval_count: 2,
  },
  stage_receipts: [
    receipt("source_intake", "Source Intake", "source_intake", "succeeded", "pass"),
    receipt("narrative_story_doctor", "Narrative Story Doctor", "extraction", "succeeded", "pass"),
    receipt("format_intelligence", "Format Intelligence", "format_compile", "succeeded", "pass"),
    receipt("format02_composition", "Format 02 Composition", "composition", "succeeded", "pass"),
    receipt("avatar_assets", "Avatar Asset Production", "avatar_asset", "succeeded", "pass"),
    receipt("provider_samples", "Provider Samples", "provider_sample", "blocked", "fail", [
      blocker("provider_samples"),
    ]),
    receipt("timeline_render_contract", "Timeline + Render Contract", "timeline", "planned", "warn"),
    receipt("render_qa", "Render QA", "qa", "planned", "warn"),
    receipt("approval_export", "Approval + Export", "export", "planned", "warn"),
  ],
  artifacts: [
    artifact("pipeline_artifact_source_span", "source_ref", "golden_path://source_span/span_health_myth_1"),
    artifact("pipeline_artifact_scene", "intermediate", "golden_path://scene_program/format02_scene_01"),
    artifact(
      "pipeline_artifact_template_preview",
      "template_preview",
      "template-preview://format02_scene_01",
      "template_preview",
      "/template-preview/format02_scene_01",
    ),
    artifact(
      "pipeline_artifact_timeline",
      "render_output",
      "video-timeline://timeline_health_myth_demo",
      "video_preview",
      "/timeline?program_id=timeline_health_myth_demo",
    ),
  ],
  blockers: [blocker("provider_samples")],
  approvals: [
    {
      gate_id: "provider_sample_first",
      gate_type: "sample_first",
      required: true,
      status: "pending",
      approved_by: null,
      pending_reason: "Missing sample approvals: face_plate_sample, template_preview_sample",
      blockers: [blocker("provider_samples")],
      required_sample_types: ["scene_sample", "face_plate_sample", "template_preview_sample"],
      approved_sample_types: ["scene_sample"],
    },
    {
      gate_id: "operator_final_approval",
      gate_type: "operator_approval",
      required: true,
      status: "pending",
      approved_by: null,
      pending_reason: "Awaiting operator approval.",
      blockers: [],
      required_sample_types: [],
      approved_sample_types: [],
    },
  ],
  scene_output_links: [
    {
      scene_id: "format02_scene_01",
      step_id: "format02_composition",
      template_preview_url: "/template-preview/format02_scene_01",
      video_preview_url: "/timeline?program_id=timeline_health_myth_demo",
      artifact_refs: ["pipeline_artifact_template_preview", "pipeline_artifact_timeline"],
      status: "preview_available",
    },
  ],
  summary: {
    total_steps: 9,
    succeeded_steps: 5,
    failed_steps: 0,
    blocked_steps: 1,
    pending_approval_count: 2,
    next_step_id: "provider_samples",
  },
  provider_calls_executed: false,
  renderer_calls_executed: false,
  local_worker_jobs_executed: false,
  created_at: now,
};

export const goldenPathRunDetailFixture = {
  schema_version: "cmf.golden_path_run_detail.v1",
  golden_path_run_id: "golden_path_health_myth_demo",
  pipeline_run_id: "pipeline_run_format02_health_myth_demo",
  orchestration_run_id: "orch_format02_pipeline_monitor_demo",
  brand_context_version_id: "bcv_health_myth_demo_v1",
  recipe_id: "format02_golden_path",
  input_fixture_refs: ["fixtures/golden_path/health_myth_interview_brief.json"],
  narrative_outputs: [{ ref: "golden_path://extraction/extraction_health_myth_demo", status: "ready" }],
  format_outputs: [{ ref: "golden_path://format_program/format02_health_myth_demo", status: "ready" }],
  composition_scene_outputs: [
    { scene_id: "format02_scene_01", ref: "golden_path://scene_program/format02_scene_01", status: "locked" },
  ],
  avatar_outputs: [{ ref: "golden_path://avatar_plan/avatar_health_myth_demo", no_lip_sync: true }],
  timeline_outputs: [{ ref: "video-timeline://timeline_health_myth_demo", timeline_program_id: "timeline_health_myth_demo" }],
  render_outputs: [{ ref: "golden_path://proxy_render/proxy_health_myth_demo", fake_or_dry_run: true }],
  approval_outputs: [{ ref: "golden_path://approval/approval_health_myth_demo", status: "pending" }],
  scene_output_links: pipelineRunMonitorFixture.scene_output_links,
  receipts: pipelineRunMonitorFixture.stage_receipts.map((stage) => ({
    receipt_id: stage.receipt_id,
    step_id: stage.step_id,
    pass_status: stage.pass_status,
  })),
  blockers: pipelineRunMonitorFixture.blockers,
  approvals: pipelineRunMonitorFixture.approvals,
  source_mode: "fixture",
  provider_calls_executed: false,
  renderer_calls_executed: false,
  local_worker_jobs_executed: false,
  created_at: now,
};

export function listPipelineRunFixtureStatuses() {
  return [pipelineRunMonitorFixture.run_status];
}

export function createPipelineRunMonitorFixture(pipelineRunId = pipelineRunMonitorFixture.run_status.pipeline_run_id) {
  return {
    ...pipelineRunMonitorFixture,
    run_status: {
      ...pipelineRunMonitorFixture.run_status,
      pipeline_run_id: pipelineRunId || pipelineRunMonitorFixture.run_status.pipeline_run_id,
      source_mode: "fixture",
    },
  };
}

export function createGoldenPathRunDetailFixture(goldenPathRunId = goldenPathRunDetailFixture.golden_path_run_id) {
  return {
    ...goldenPathRunDetailFixture,
    golden_path_run_id: goldenPathRunId || goldenPathRunDetailFixture.golden_path_run_id,
    source_mode: "fixture",
  };
}

function receipt(stepId, stepName, stepKind, status, passStatus, blockers = []) {
  return {
    step_id: stepId,
    step_name: stepName,
    step_kind: stepKind,
    status,
    pass_status: passStatus,
    receipt_id: `pipeline_step_receipt_${stepId}`,
    orchestration_stage_execution_id: `orch_format02_pipeline_monitor_demo:${stepId}`,
    started_at: status === "planned" ? null : now,
    completed_at: status === "succeeded" ? now : null,
    message: status === "blocked" ? "Step is waiting on operator-visible approval gates." : "Fixture monitor receipt.",
    blockers,
  };
}

function blocker(stepId) {
  return {
    blocker_id: "pipeline_blocker_provider_sample_first",
    code: "approval_gate_not_approved",
    message: "Provider batch is blocked until scene, face plate, and template preview samples are approved.",
    severity: "blocking",
    step_id: stepId,
    recoverable: true,
  };
}

function artifact(artifactId, role, uri, linkedPreviewType = "none", linkedPreviewUrl = null) {
  return {
    artifact_id: artifactId,
    artifact_ref_id: null,
    pipeline_artifact_ref_id: artifactId,
    role,
    uri,
    storage_state: "pointer_only",
    sha256: null,
    source_ref_ids: ["span_health_myth_1"],
    linked_preview_type: linkedPreviewType,
    linked_preview_url: linkedPreviewUrl,
    raw_bytes_included: false,
  };
}
