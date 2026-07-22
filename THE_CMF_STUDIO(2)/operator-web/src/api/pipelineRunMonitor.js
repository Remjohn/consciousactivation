import { apiFetch } from "../lib/apiClient.js";
import {
  createGoldenPathRunDetailFixture,
  createPipelineRunMonitorFixture,
  listPipelineRunFixtureStatuses,
} from "../fixtures/pipelineRunMonitor.fixture.js";

export const PIPELINE_RUN_MONITOR_FIXTURE_MODE =
  import.meta.env.VITE_CMF_PIPELINE_MONITOR_FIXTURE_MODE === "true";

function withSourceMode(payload, sourceMode) {
  if (Array.isArray(payload)) {
    return payload.map((item) => ({ ...item, source_mode: item.source_mode || sourceMode }));
  }
  return {
    ...payload,
    source_mode: payload.source_mode || sourceMode,
  };
}

export async function listPipelineRuns() {
  if (PIPELINE_RUN_MONITOR_FIXTURE_MODE) {
    return listPipelineRunFixtureStatuses();
  }
  try {
    return withSourceMode(await apiFetch("/api/v1/pipeline-runs"), "backend");
  } catch {
    return listPipelineRunFixtureStatuses();
  }
}

export async function getPipelineRunMonitor(pipelineRunId) {
  if (PIPELINE_RUN_MONITOR_FIXTURE_MODE) {
    return createPipelineRunMonitorFixture(pipelineRunId);
  }
  try {
    return withSourceMode(await apiFetch(`/api/v1/pipeline-runs/${pipelineRunId}`), "backend");
  } catch {
    return createPipelineRunMonitorFixture(pipelineRunId);
  }
}

export async function getPipelineSceneOutputs(pipelineRunId) {
  if (PIPELINE_RUN_MONITOR_FIXTURE_MODE) {
    return createPipelineRunMonitorFixture(pipelineRunId).scene_output_links;
  }
  try {
    return await apiFetch(`/api/v1/pipeline-runs/${pipelineRunId}/scene-outputs`);
  } catch {
    return createPipelineRunMonitorFixture(pipelineRunId).scene_output_links;
  }
}

export async function getGoldenPathRunDetail(goldenPathRunId) {
  if (PIPELINE_RUN_MONITOR_FIXTURE_MODE) {
    return createGoldenPathRunDetailFixture(goldenPathRunId);
  }
  try {
    return withSourceMode(await apiFetch(`/api/v1/golden-path-runs/${goldenPathRunId}`), "backend");
  } catch {
    return createGoldenPathRunDetailFixture(goldenPathRunId);
  }
}
