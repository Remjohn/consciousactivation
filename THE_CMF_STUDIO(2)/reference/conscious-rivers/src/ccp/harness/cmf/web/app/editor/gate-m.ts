/**
 * Gate M — Pre-Edit Constraint Network (Editor Readiness Assurance)
 *
 * FR-VID-10 §6: All 6 questions must be answered before opening the editor.
 * These are executable validation functions called by the editor page on load.
 *
 * 1. Pipeline State Validity
 * 2. Manifest Schema Compliance
 * 3. Asset Availability
 * 4. Audio File Availability
 * 5. Caption Data Presence
 * 6. Backend Connectivity
 */

import { checkBackendHealth } from "./api-client";

// ─── Gate M result types ───

export interface GateResult {
  passed: boolean;
  message: string;
  severity: "block" | "warn" | "info";
}

export interface GateMResults {
  pipelineState: GateResult;
  manifestSchema: GateResult;
  assetAvailability: GateResult;
  audioAvailability: GateResult;
  captionPresence: GateResult;
  backendConnectivity: GateResult;
  allBlocking: boolean;
}

// ─── Allowed pipeline states for editor access ───
const ALLOWED_STATES = ["READY_FOR_REVIEW", "REGENERATING", "APPROVED"];

// ─── Gate M Question 1: Pipeline State Validity ───
export function checkPipelineState(pipelineState: string): GateResult {
  if (ALLOWED_STATES.includes(pipelineState)) {
    return {
      passed: true,
      message: `Pipeline state "${pipelineState}" is valid for editing.`,
      severity: "info",
    };
  }
  return {
    passed: false,
    message: `Video is in "${pipelineState}" state — editor available after review stage.`,
    severity: "block",
  };
}

// ─── Gate M Question 2: Manifest Schema Compliance ───
export function checkManifestSchema(manifest: Record<string, unknown>): GateResult {
  const errors: string[] = [];

  if (!manifest) {
    return { passed: false, message: "Manifest is null or undefined.", severity: "block" };
  }
  if (!Array.isArray(manifest.beats)) {
    errors.push("Missing 'beats' array");
  } else if (manifest.beats.length === 0) {
    errors.push("Beats array is empty");
  }
  if (typeof manifest.fps !== "number" || manifest.fps <= 0) {
    errors.push(`Invalid fps: ${manifest.fps}`);
  }
  if (typeof manifest.total_frames !== "number" || manifest.total_frames <= 0) {
    errors.push(`Invalid total_frames: ${manifest.total_frames}`);
  }
  if (typeof manifest.width !== "number" || manifest.width <= 0) {
    errors.push(`Invalid width: ${manifest.width}`);
  }
  if (typeof manifest.height !== "number" || manifest.height <= 0) {
    errors.push(`Invalid height: ${manifest.height}`);
  }

  // Validate frame math: start_frame[i] = sum of previous durations
  if (Array.isArray(manifest.beats)) {
    let expectedStart = 0;
    for (let i = 0; i < manifest.beats.length; i++) {
      const beat = manifest.beats[i] as Record<string, unknown>;
      if (typeof beat.duration_frames !== "number" || beat.duration_frames < 12) {
        errors.push(`Beat ${i}: invalid duration_frames (${beat.duration_frames})`);
      }
      if (typeof beat.start_frame === "number" && beat.start_frame !== expectedStart) {
        errors.push(
          `Beat ${i}: start_frame mismatch (expected ${expectedStart}, got ${beat.start_frame})`
        );
      }
      expectedStart += (beat.duration_frames as number) || 0;
    }
  }

  if (errors.length > 0) {
    return {
      passed: false,
      message: `Manifest schema errors: ${errors.join("; ")}`,
      severity: "block",
    };
  }

  return {
    passed: true,
    message: "Manifest passes DEP-VID-002 schema validation.",
    severity: "info",
  };
}

// ─── Gate M Question 3: Asset Availability ───
export async function checkAssetAvailability(
  beats: Array<Record<string, unknown>>
): Promise<GateResult> {
  const missingAssets: number[] = [];

  for (let i = 0; i < beats.length; i++) {
    const beat = beats[i];
    const videoUrl = beat.video_clip_url as string | undefined;
    const imageUrl = beat.fallback_image_url as string | undefined;

    if (!videoUrl && !imageUrl) {
      missingAssets.push(i);
      continue;
    }

    // HEAD request check for asset reachability
    const urlToCheck = videoUrl || imageUrl;
    if (urlToCheck) {
      try {
        const response = await fetch(urlToCheck, { method: "HEAD" });
        if (!response.ok) {
          missingAssets.push(i);
        }
      } catch {
        missingAssets.push(i);
      }
    }
  }

  if (missingAssets.length > 0) {
    return {
      passed: false,
      message: `${missingAssets.length} beat(s) have unreachable assets: [${missingAssets.join(", ")}]`,
      severity: "warn",
    };
  }

  return {
    passed: true,
    message: "All beat asset URLs are reachable.",
    severity: "info",
  };
}

// ─── Gate M Question 4: Audio File Availability ───
export async function checkAudioAvailability(
  audio: Record<string, unknown> | undefined
): Promise<GateResult> {
  if (!audio) {
    return {
      passed: false,
      message: "No audio configuration in manifest.",
      severity: "warn",
    };
  }

  const problems: string[] = [];
  const voiceoverPath = audio.voiceover_path as string | undefined;
  const musicPath = audio.music_path as string | undefined;

  if (voiceoverPath) {
    try {
      const res = await fetch(voiceoverPath, { method: "HEAD" });
      if (!res.ok) problems.push("Voiceover file unreachable");
    } catch {
      problems.push("Voiceover file unreachable");
    }
  } else {
    problems.push("No voiceover_path in manifest");
  }

  if (musicPath) {
    try {
      const res = await fetch(musicPath, { method: "HEAD" });
      if (!res.ok) problems.push("Music file unreachable");
    } catch {
      problems.push("Music file unreachable");
    }
  } else {
    problems.push("No music_path in manifest");
  }

  if (problems.length > 0) {
    return {
      passed: false,
      message: `Audio issues: ${problems.join("; ")}`,
      severity: "warn",
    };
  }

  return {
    passed: true,
    message: "All audio files are reachable.",
    severity: "info",
  };
}

// ─── Gate M Question 5: Caption Data Presence ───
export function checkCaptionPresence(manifest: Record<string, unknown>): GateResult {
  const captions = manifest.captions as Array<unknown> | undefined;

  if (!captions || !Array.isArray(captions) || captions.length === 0) {
    return {
      passed: false,
      message: "Captions not yet generated — generate captions before final export.",
      severity: "warn",
    };
  }

  return {
    passed: true,
    message: `Caption data present: ${captions.length} caption entries.`,
    severity: "info",
  };
}

// ─── Gate M Question 6: Backend Connectivity ───
export async function checkBackendConnectivity(): Promise<GateResult> {
  try {
    const result = await checkBackendHealth();
    if (result.status === "ok") {
      return {
        passed: true,
        message: "FastAPI backend is online.",
        severity: "info",
      };
    }
    return {
      passed: false,
      message: "Backend health check returned non-ok status.",
      severity: "warn",
    };
  } catch {
    return {
      passed: false,
      message: "FastAPI backend is offline — local edits work, regeneration/render unavailable.",
      severity: "warn",
    };
  }
}

// ─── Run all Gate M checks ───
export async function runGateM(
  pipelineState: string,
  manifest: Record<string, unknown>
): Promise<GateMResults> {
  const pipelineResult = checkPipelineState(pipelineState);
  const schemaResult = checkManifestSchema(manifest);
  const captionResult = checkCaptionPresence(manifest);

  const beats = (manifest.beats as Array<Record<string, unknown>>) || [];
  const audio = manifest.audio as Record<string, unknown> | undefined;

  const [assetResult, audioResult, backendResult] = await Promise.all([
    checkAssetAvailability(beats),
    checkAudioAvailability(audio),
    checkBackendConnectivity(),
  ]);

  // allBlocking = true if any "block" severity gate failed
  const allBlocking = [
    pipelineResult,
    schemaResult,
    assetResult,
    audioResult,
    captionResult,
    backendResult,
  ].some((r) => !r.passed && r.severity === "block");

  return {
    pipelineState: pipelineResult,
    manifestSchema: schemaResult,
    assetAvailability: assetResult,
    audioAvailability: audioResult,
    captionPresence: captionResult,
    backendConnectivity: backendResult,
    allBlocking,
  };
}
