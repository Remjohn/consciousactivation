/**
 * Editor API Client — HTTP client for FastAPI backend bridge.
 *
 * FR-VID-10 §3 TD5: FastAPI backend bridge (REST, not WebSocket).
 * FR-VID-10 §4 Stage 9: All endpoint paths match DEP-VID-029.
 */

import type { CMFManifest } from "@cmf/remotion-compositions";

const BASE_URL = process.env.NEXT_PUBLIC_CMF_API_URL || "http://localhost:8000";

// ---------------------------------------------------------------------------
// Error handling
// ---------------------------------------------------------------------------

interface ApiError {
  error: string;
  code: string;
  details?: Record<string, unknown>;
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const body: ApiError = await response.json().catch(() => ({
      error: response.statusText,
      code: `HTTP_${response.status}`,
    }));
    throw new Error(body.error || `API error: ${response.status}`);
  }
  return response.json();
}

function authHeaders(): HeadersInit {
  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("cmf_auth_token")
      : null;
  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

// ---------------------------------------------------------------------------
// Manifest CRUD — FR-VID-10 §4 Stage 9 Step 2
// ---------------------------------------------------------------------------

export async function fetchManifest(videoId: string): Promise<CMFManifest> {
  const res = await fetch(`${BASE_URL}/api/editor/${encodeURIComponent(videoId)}/manifest`, {
    headers: authHeaders(),
  });
  return handleResponse<CMFManifest>(res);
}

export async function saveManifest(
  videoId: string,
  manifest: CMFManifest
): Promise<CMFManifest> {
  const res = await fetch(`${BASE_URL}/api/editor/${encodeURIComponent(videoId)}/manifest`, {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(manifest),
  });
  return handleResponse<CMFManifest>(res);
}

export interface JsonPatchOp {
  op: "add" | "remove" | "replace" | "move" | "copy" | "test";
  path: string;
  value?: unknown;
  from?: string;
}

export async function patchManifest(
  videoId: string,
  patch: JsonPatchOp[]
): Promise<CMFManifest> {
  const res = await fetch(`${BASE_URL}/api/editor/${encodeURIComponent(videoId)}/manifest`, {
    method: "PATCH",
    headers: authHeaders(),
    body: JSON.stringify(patch),
  });
  return handleResponse<CMFManifest>(res);
}

// ---------------------------------------------------------------------------
// Generation — FR-VID-10 §4 Stage 9 Step 2
// ---------------------------------------------------------------------------

export interface RegenerateRequest {
  beat_index: number;
  mode: "T2I_ONLY" | "I2V_ONLY" | "BOTH";
  revision_note?: string;
}

export interface JobStatus {
  status: "PENDING" | "RUNNING" | "COMPLETE" | "FAILED";
  result_manifest?: CMFManifest;
  error?: string;
}

export async function startRegeneration(
  videoId: string,
  request: RegenerateRequest
): Promise<{ job_id: string }> {
  const res = await fetch(
    `${BASE_URL}/api/editor/${encodeURIComponent(videoId)}/regenerate`,
    {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify(request),
    }
  );
  return handleResponse<{ job_id: string }>(res);
}

export async function pollRegeneration(
  videoId: string,
  jobId: string
): Promise<JobStatus> {
  const res = await fetch(
    `${BASE_URL}/api/editor/${encodeURIComponent(videoId)}/regenerate/${encodeURIComponent(jobId)}`,
    { headers: authHeaders() }
  );
  return handleResponse<JobStatus>(res);
}

// ---------------------------------------------------------------------------
// Rendering — FR-VID-10 §4 Stage 9 Step 2
// ---------------------------------------------------------------------------

export interface RenderRequest {
  quality_tier: "preview" | "review" | "final";
  platform_preset: string;
  include_captions: boolean;
  export_srt: boolean;
}

export interface RenderStatus {
  status: string;
  progress_pct: number;
  output_url?: string;
  file_size_mb?: number;
}

export async function startRender(
  videoId: string,
  request: RenderRequest
): Promise<{ job_id: string }> {
  const res = await fetch(
    `${BASE_URL}/api/editor/${encodeURIComponent(videoId)}/render`,
    {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify(request),
    }
  );
  return handleResponse<{ job_id: string }>(res);
}

export async function pollRender(
  videoId: string,
  jobId: string
): Promise<RenderStatus> {
  const res = await fetch(
    `${BASE_URL}/api/editor/${encodeURIComponent(videoId)}/render/${encodeURIComponent(jobId)}`,
    { headers: authHeaders() }
  );
  return handleResponse<RenderStatus>(res);
}

// ---------------------------------------------------------------------------
// FFmpeg Operations — FR-VID-10 §4 Stage 9 Step 2
// ---------------------------------------------------------------------------

export async function ffmpegTrim(
  inputUrl: string,
  startSec: number,
  endSec: number
): Promise<{ output_url: string }> {
  const res = await fetch(`${BASE_URL}/api/editor/ffmpeg/trim`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ input_url: inputUrl, start_sec: startSec, end_sec: endSec }),
  });
  return handleResponse<{ output_url: string }>(res);
}

export async function ffmpegConcat(
  inputUrls: string[]
): Promise<{ output_url: string }> {
  const res = await fetch(`${BASE_URL}/api/editor/ffmpeg/concat`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ input_urls: inputUrls }),
  });
  return handleResponse<{ output_url: string }>(res);
}

export async function ffmpegExtractAudio(
  inputUrl: string
): Promise<{ waveform_data: number[] }> {
  const res = await fetch(`${BASE_URL}/api/editor/ffmpeg/extract-audio`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ input_url: inputUrl }),
  });
  return handleResponse<{ waveform_data: number[] }>(res);
}

// ---------------------------------------------------------------------------
// Assets — FR-VID-10 §4 Stage 9 Step 2
// ---------------------------------------------------------------------------

export interface AssetSearchResult {
  url: string;
  thumbnail: string;
  source: string;
  license: string;
}

export async function uploadAsset(
  videoId: string,
  file: File
): Promise<{ asset_url: string }> {
  const formData = new FormData();
  formData.append("file", file);
  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("cmf_auth_token")
      : null;
  const res = await fetch(
    `${BASE_URL}/api/editor/${encodeURIComponent(videoId)}/assets/upload`,
    {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: formData,
    }
  );
  return handleResponse<{ asset_url: string }>(res);
}

export async function searchAssets(
  videoId: string,
  query: string,
  source: "pexels" | "pixabay" | "local"
): Promise<{ results: AssetSearchResult[] }> {
  const params = new URLSearchParams({ q: query, source });
  const res = await fetch(
    `${BASE_URL}/api/editor/${encodeURIComponent(videoId)}/assets/search?${params}`,
    { headers: authHeaders() }
  );
  return handleResponse<{ results: AssetSearchResult[] }>(res);
}

// ---------------------------------------------------------------------------
// AI Copilot — FR-VID-10 §4 Stage 9 Step 2
// ---------------------------------------------------------------------------

export interface CopilotMessage {
  role: "user" | "assistant";
  content: string;
}

export interface CopilotResponse {
  edit_class: string;
  intent_summary: string;
  patch?: JsonPatchOp[];
  beat_index?: number;
  regeneration_mode?: string;
  revision_note?: string;
}

export async function sendCopilotMessage(
  message: string,
  manifest: CMFManifest,
  conversationHistory: CopilotMessage[]
): Promise<CopilotResponse> {
  const res = await fetch(`${BASE_URL}/api/editor/copilot`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({
      message,
      manifest,
      conversation_history: conversationHistory,
    }),
  });
  return handleResponse<CopilotResponse>(res);
}

// ---------------------------------------------------------------------------
// Health Check
// ---------------------------------------------------------------------------

export async function checkBackendHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${BASE_URL}/health`, {
      signal: AbortSignal.timeout(3000),
    });
    return res.ok;
  } catch {
    return false;
  }
}
