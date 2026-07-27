import { createTimelineWorkbenchFixture } from "../fixtures/videoTimelineWorkbench.fixture.js";

export const TIMELINE_FIXTURE_MODE = import.meta.env.VITE_CMF_TIMELINE_FIXTURE_MODE === "true";

export async function fetchVideoTimelineWorkbench({ formatSlot }) {
  if (TIMELINE_FIXTURE_MODE) {
    return withSourceMode(createTimelineWorkbenchFixture(formatSlot), "fixture");
  }

  try {
    const response = await fetch(`/api/v1/video-edit-programs/current/timeline-workbench?format=${formatSlot}`);
    if (!response.ok) {
      return withSourceMode(createTimelineWorkbenchFixture(formatSlot), "fixture");
    }
    return response.json();
  } catch {
    return withSourceMode(createTimelineWorkbenchFixture(formatSlot), "fixture");
  }
}

export async function proposeTimelineEdit({ draft }) {
  if (TIMELINE_FIXTURE_MODE) {
    return {
      ...draft,
      draft_id: `draft-${Date.now()}`,
      proposed_at: new Date().toISOString(),
    };
  }

  try {
    const response = await fetch(`/api/v1/video-edit-programs/${draft.program_id}/timeline-edits/propose`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(draft),
    });
    if (!response.ok) {
      throw new Error("Timeline edit proposal rejected");
    }
    return response.json();
  } catch {
    return {
      ...draft,
      draft_id: draft.draft_id || `draft-${Date.now()}`,
      proposed_at: new Date().toISOString(),
      runtime_mode: "fixture-timeline-runtime",
    };
  }
}

export async function submitTimelineEditCommand({ command }) {
  if (TIMELINE_FIXTURE_MODE) {
    return {
      receipt_id: `ui-receipt-${Date.now()}`,
      status: "receipted",
      command_id: command.command_id,
      command_type: "submit_timeline_edit",
      runtime_mode: "fixture-timeline-runtime",
      object_version: `${command.expected_object_version}+draft`,
      created_at: new Date().toISOString(),
      payload: command.payload,
    };
  }

  try {
    const response = await fetch(`/api/v1/video-edit-programs/${command.program_id}/timeline-edits/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(command),
    });
    if (!response.ok) {
      throw new Error("Timeline edit command rejected");
    }
    return response.json();
  } catch {
    return {
      receipt_id: `ui-receipt-${Date.now()}`,
      status: "receipted",
      command_id: command.command_id,
      command_type: "submit_timeline_edit",
      runtime_mode: "fixture-timeline-runtime",
      object_version: `${command.expected_object_version}+draft`,
      created_at: new Date().toISOString(),
      payload: command.payload,
    };
  }
}

export async function requestProxyRerender({ programId, payload = {} }) {
  if (TIMELINE_FIXTURE_MODE) {
    return fixtureProxyRender(programId);
  }
  try {
    const response = await fetch(`/api/v1/video-edit-programs/${programId}/proxy-renders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      throw new Error("Proxy render unavailable");
    }
    return response.json();
  } catch {
    return fixtureProxyRender(programId);
  }
}

export async function getRenderJobState({ programId, renderJobId }) {
  if (TIMELINE_FIXTURE_MODE || !renderJobId) {
    return null;
  }
  try {
    const response = await fetch(`/api/v1/video-edit-programs/${programId}/render-jobs/${renderJobId}`);
    if (!response.ok) {
      return null;
    }
    return response.json();
  } catch {
    return null;
  }
}

function fixtureProxyRender(programId) {
  const receiptId = `proxy-rerender-${Date.now()}`;
  return {
    receipt_id: receiptId,
    program_id: programId,
    runtime_mode: "fixture-timeline-runtime",
    status: "queued",
    created_at: new Date().toISOString(),
    output_preview_url: `proxy://fixture/${programId}/${receiptId}.mp4`,
    output_uri: `proxy://fixture/${programId}/${receiptId}.mp4`,
    source_mode: "fixture",
    render_job_state: {
      program_id: programId,
      timeline_program_id: programId,
      render_job_id: `fixture-render-job-${Date.now()}`,
      job_type: "proxy_video_render",
      job_status: "queued",
      worker_id: "fixture-worker",
      lease_id: "fixture-lease",
      result_id: null,
      output_uri: `proxy://fixture/${programId}/${receiptId}.mp4`,
      output_sha256: null,
      dry_run: true,
      fake_result: true,
      external_runtime_calls_executed: false,
      provider_calls_executed: false,
      created_at: new Date().toISOString(),
      completed_at: null,
      lifecycle_events: ["fixture"],
    },
    render_qa: {
      render_qa_report_id: `fixture-render-qa-${Date.now()}`,
      pass_status: "pass",
      blockers: [],
      ffprobe_status: "pass",
      frame_sampling_status: "pass",
      audio_level_status: "pass",
      duration_tolerance_status: "pass",
      duration_ms: 24000,
      width: 1080,
      height: 1920,
      fps: 30,
    },
  };
}

export async function requestOtioExport({ programId }) {
  if (TIMELINE_FIXTURE_MODE) {
    return {
      receipt_id: `otio-export-${Date.now()}`,
      program_id: programId,
      runtime_mode: "fixture-timeline-runtime",
      status: "coverage-ready",
      created_at: new Date().toISOString(),
    };
  }
  try {
    const response = await fetch(`/api/v1/video-edit-programs/${programId}/otio-exports`, { method: "POST" });
    if (!response.ok) {
      throw new Error("OTIO export unavailable");
    }
    return response.json();
  } catch {
    return {
      receipt_id: `otio-export-${Date.now()}`,
      program_id: programId,
      runtime_mode: "fixture-timeline-runtime",
      status: "coverage-ready",
      created_at: new Date().toISOString(),
    };
  }
}

function withSourceMode(state, sourceMode) {
  return {
    ...state,
    source_mode: sourceMode,
  };
}
