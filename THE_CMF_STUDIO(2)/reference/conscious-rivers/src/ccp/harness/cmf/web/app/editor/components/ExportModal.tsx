/**
 * Export Modal — Platform presets, quality tiers, caption toggle, render progress.
 *
 * FR-VID-10 §4 Stage 7: Social media presets (TikTok 9:16, Instagram 4:5,
 * YouTube 16:9, Custom), quality tier (preview/review/final per DEP-VID-024),
 * caption toggle, SRT export, render progress polling.
 */

"use client";

import React, { useState, useCallback, useEffect, useRef } from "react";

import { useEditorStore } from "../store";
import { startRender, pollRender } from "../api-client";

// ─── Platform presets per FR-VID-10 §4 Stage 7 Step 2 ───
interface PlatformPreset {
  label: string;
  width: number;
  height: number;
  fps: number;
  codec: string;
  maxDurationSec?: number;
  maxDurationWarning?: string;
}

const PLATFORM_PRESETS: Record<string, PlatformPreset> = {
  "tiktok-9x16": {
    label: "TikTok / YouTube Shorts / Reels (9:16)",
    width: 1080,
    height: 1920,
    fps: 30,
    codec: "h264",
    maxDurationSec: 60,
    maxDurationWarning: "Video exceeds 60s — too long for Shorts/Reels",
  },
  "instagram-4x5": {
    label: "Instagram Feed (4:5)",
    width: 1080,
    height: 1350,
    fps: 30,
    codec: "h264",
  },
  "youtube-16x9": {
    label: "YouTube Long (16:9)",
    width: 1920,
    height: 1080,
    fps: 30,
    codec: "h264",
  },
  custom: {
    label: "Custom",
    width: 1920,
    height: 1080,
    fps: 30,
    codec: "h264",
  },
};

// ─── Quality tiers per DEP-VID-024 ───
const QUALITY_TIERS = [
  { id: "preview", label: "Preview (540p)", description: "Fast — for quick checks" },
  { id: "review", label: "Review (720p)", description: "Medium — for client sharing" },
  { id: "final", label: "Final (1080p)", description: "Full quality — for publishing" },
] as const;

type QualityTier = (typeof QUALITY_TIERS)[number]["id"];

interface RenderStatus {
  jobId: string;
  status: "PENDING" | "RUNNING" | "COMPLETE" | "FAILED";
  progressPct: number;
  outputUrl?: string;
  fileSizeMb?: number;
  error?: string;
}

interface ExportModalProps {
  open: boolean;
  onClose: () => void;
}

export const ExportModal: React.FC<ExportModalProps> = ({ open, onClose }) => {
  const manifest = useEditorStore((s) => s.manifest);
  const beatReviews = useEditorStore((s) => s.beatReviews);

  const [selectedPreset, setSelectedPreset] = useState("tiktok-9x16");
  const [qualityTier, setQualityTier] = useState<QualityTier>("final");
  const [includeCaptions, setIncludeCaptions] = useState(true);
  const [exportSrt, setExportSrt] = useState(false);
  const [customWidth, setCustomWidth] = useState(1920);
  const [customHeight, setCustomHeight] = useState(1080);
  const [customFps, setCustomFps] = useState(30);

  const [renderStatus, setRenderStatus] = useState<RenderStatus | null>(null);
  const [exporting, setExporting] = useState(false);
  const pollRef = useRef<ReturnType<typeof setInterval>>();

  // ─── Check if all beats are approved (AC7 prerequisite) ───
  const allApproved =
    manifest?.beats.every(
      (_, i) => beatReviews[i]?.status === "APPROVED"
    ) ?? false;

  const unapprovedCount = manifest
    ? manifest.beats.filter(
        (_, i) => beatReviews[i]?.status !== "APPROVED"
      ).length
    : 0;

  // ─── Duration warning check ───
  const preset = PLATFORM_PRESETS[selectedPreset];
  const totalDuration = manifest
    ? manifest.total_frames / manifest.fps
    : 0;
  const durationWarning =
    preset.maxDurationSec && totalDuration > preset.maxDurationSec
      ? preset.maxDurationWarning
      : null;

  // ─── Clean up polling on unmount or close ───
  useEffect(() => {
    return () => {
      if (pollRef.current) clearInterval(pollRef.current);
    };
  }, []);

  // ─── Start export ───
  const handleStartExport = useCallback(async () => {
    if (!manifest || !allApproved) return;

    const activePreset =
      selectedPreset === "custom"
        ? { width: customWidth, height: customHeight, fps: customFps }
        : { width: preset.width, height: preset.height, fps: preset.fps };

    setExporting(true);
    setRenderStatus({
      jobId: "",
      status: "PENDING",
      progressPct: 0,
    });

    try {
      const { job_id } = await startRender(
        manifest.video_id || "unknown",
        qualityTier,
        selectedPreset,
        includeCaptions,
        exportSrt
      );

      setRenderStatus({
        jobId: job_id,
        status: "RUNNING",
        progressPct: 0,
      });

      // Poll for render progress every 2 seconds
      pollRef.current = setInterval(async () => {
        try {
          const status = await pollRender(
            manifest.video_id || "unknown",
            job_id
          );
          setRenderStatus({
            jobId: job_id,
            status: status.status,
            progressPct: status.progress_pct || 0,
            outputUrl: status.output_url,
            fileSizeMb: status.file_size_mb,
          });

          if (
            status.status === "COMPLETE" ||
            status.status === "FAILED"
          ) {
            if (pollRef.current) clearInterval(pollRef.current);
            setExporting(false);
          }
        } catch {
          // Continue polling on transient errors
        }
      }, 2000);
    } catch (err) {
      setRenderStatus({
        jobId: "",
        status: "FAILED",
        progressPct: 0,
        error: err instanceof Error ? err.message : "Export failed",
      });
      setExporting(false);
    }
  }, [
    manifest,
    allApproved,
    selectedPreset,
    qualityTier,
    includeCaptions,
    exportSrt,
    preset,
    customWidth,
    customHeight,
    customFps,
  ]);

  if (!open) return null;

  return (
    <div className="export-modal-overlay" onClick={onClose}>
      <div
        className="export-modal"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-label="Export Video"
      >
        <div className="export-modal-header">
          <h2>Export Video</h2>
          <button onClick={onClose} className="export-close-btn">
            ✕
          </button>
        </div>

        <div className="export-modal-body">
          {/* Platform Preset Selection */}
          <section className="export-section">
            <h3>Platform</h3>
            {Object.entries(PLATFORM_PRESETS).map(([key, p]) => (
              <label key={key} className="export-radio">
                <input
                  type="radio"
                  name="platform"
                  value={key}
                  checked={selectedPreset === key}
                  onChange={() => setSelectedPreset(key)}
                  disabled={exporting}
                />
                <span>{p.label}</span>
                <span className="preset-detail">
                  {p.width}×{p.height} {p.fps}fps
                </span>
              </label>
            ))}

            {/* Custom dimensions */}
            {selectedPreset === "custom" && (
              <div className="export-custom-dims">
                <label>
                  Width:{" "}
                  <input
                    type="number"
                    value={customWidth}
                    onChange={(e) =>
                      setCustomWidth(parseInt(e.target.value, 10) || 1920)
                    }
                    min={320}
                    max={3840}
                    disabled={exporting}
                  />
                </label>
                <label>
                  Height:{" "}
                  <input
                    type="number"
                    value={customHeight}
                    onChange={(e) =>
                      setCustomHeight(parseInt(e.target.value, 10) || 1080)
                    }
                    min={320}
                    max={3840}
                    disabled={exporting}
                  />
                </label>
                <label>
                  FPS:{" "}
                  <input
                    type="number"
                    value={customFps}
                    onChange={(e) =>
                      setCustomFps(parseInt(e.target.value, 10) || 30)
                    }
                    min={15}
                    max={60}
                    disabled={exporting}
                  />
                </label>
              </div>
            )}

            {durationWarning && (
              <p className="export-warning">⚠️ {durationWarning}</p>
            )}
          </section>

          {/* Quality Tier */}
          <section className="export-section">
            <h3>Quality</h3>
            {QUALITY_TIERS.map((tier) => (
              <label key={tier.id} className="export-radio">
                <input
                  type="radio"
                  name="quality"
                  value={tier.id}
                  checked={qualityTier === tier.id}
                  onChange={() => setQualityTier(tier.id)}
                  disabled={exporting}
                />
                <span>{tier.label}</span>
                <span className="tier-description">{tier.description}</span>
              </label>
            ))}
          </section>

          {/* Caption + SRT options */}
          <section className="export-section">
            <h3>Captions</h3>
            <label className="export-checkbox">
              <input
                type="checkbox"
                checked={includeCaptions}
                onChange={(e) => setIncludeCaptions(e.target.checked)}
                disabled={exporting}
              />
              Burn-in captions
            </label>
            <label className="export-checkbox">
              <input
                type="checkbox"
                checked={exportSrt}
                onChange={(e) => setExportSrt(e.target.checked)}
                disabled={exporting}
              />
              Export SRT/VTT subtitle file
            </label>
          </section>

          {/* Approval gate — AC7 */}
          {!allApproved && (
            <p className="export-blocked">
              ⛔ {unapprovedCount} beat{unapprovedCount !== 1 ? "s" : ""}{" "}
              pending approval. Approve all beats before exporting.
            </p>
          )}

          {/* Render progress */}
          {renderStatus && (
            <section className="export-section export-progress">
              <h3>Render Progress</h3>
              <div className="progress-bar-container">
                <div
                  className="progress-bar-fill"
                  style={{ width: `${renderStatus.progressPct}%` }}
                />
                <span className="progress-bar-label">
                  {renderStatus.status === "COMPLETE"
                    ? "Complete!"
                    : renderStatus.status === "FAILED"
                      ? `Failed: ${renderStatus.error || "Unknown error"}`
                      : `${renderStatus.progressPct}%`}
                </span>
              </div>

              {renderStatus.status === "COMPLETE" && renderStatus.outputUrl && (
                <div className="export-result">
                  <a
                    href={renderStatus.outputUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="export-download-btn"
                  >
                    ⬇ Download{" "}
                    {renderStatus.fileSizeMb
                      ? `(${renderStatus.fileSizeMb.toFixed(1)} MB)`
                      : ""}
                  </a>
                </div>
              )}
            </section>
          )}
        </div>

        <div className="export-modal-footer">
          <button onClick={onClose} disabled={exporting}>
            Cancel
          </button>
          <button
            className="export-start-btn"
            onClick={handleStartExport}
            disabled={!allApproved || exporting}
            title={
              !allApproved
                ? `${unapprovedCount} beats pending approval`
                : "Start export"
            }
          >
            {exporting ? "Exporting..." : "Start Export"}
          </button>
        </div>
      </div>
    </div>
  );
};
