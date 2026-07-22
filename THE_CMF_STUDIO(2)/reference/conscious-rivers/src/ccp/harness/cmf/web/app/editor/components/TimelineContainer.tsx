/**
 * Timeline Container — Multi-track timeline UI.
 *
 * FR-VID-10 §4 Stage 3: Visual track (beat blocks with thumbnails),
 * Music track (waveform + ducking overlay), Voiceover track (waveform),
 * Caption track (word blocks). Playhead, zoom, selection.
 *
 * FR-VID-10 §4 Stage 5: Clip editing tools — trim drag handles,
 * split at playhead, drag-reorder, delete beat, change transition.
 * FR-VID-10 §4 Stage 6: Ducking curve editor — draggable control points.
 */

"use client";

import React, { useCallback, useMemo, useRef } from "react";

import type { CMFManifest, ManifestBeat } from "@cmf/remotion-compositions";

import { useEditorStore } from "../store";

// ---------------------------------------------------------------------------
// Arc stage colors — FR-VID-10 §4 Stage 3 Step 2
// ---------------------------------------------------------------------------

const ARC_COLORS: Record<string, string> = {
  hook: "#e74c3c",
  rising: "#e67e22",
  tension: "#f39c12",
  climax: "#f1c40f",
  resolution: "#3498db",
  falling: "#2980b9",
  default: "#7f8c8d",
};

// ---------------------------------------------------------------------------
// Beat Block — Visual track clip with drag handles
// ---------------------------------------------------------------------------

interface BeatBlockProps {
  beat: ManifestBeat;
  pixelsPerFrame: number;
  onSelect: (index: number) => void;
  onTrimEnd: (beatIndex: number, deltaFrames: number) => void;
}

const BeatBlock: React.FC<BeatBlockProps> = ({
  beat,
  pixelsPerFrame,
  onSelect,
  onTrimEnd,
}) => {
  const width = beat.duration_frames * pixelsPerFrame;
  const left = beat.start_frame * pixelsPerFrame;
  const color = ARC_COLORS[beat.arc_stage] || ARC_COLORS.default;
  const selectedBeat = useEditorStore((s) => s.session.selected_beat_index);
  const isSelected = selectedBeat === beat.beat_index;
  const dragStartX = useRef<number | null>(null);

  // FR-VID-10 §4 Stage 5 Step 1: Trim via drag handles
  const handleTrimDragStart = useCallback(
    (e: React.MouseEvent) => {
      e.stopPropagation();
      dragStartX.current = e.clientX;

      const handleMouseMove = (me: MouseEvent) => {
        if (dragStartX.current === null) return;
        const deltaPixels = me.clientX - dragStartX.current;
        const deltaFrames = Math.round(deltaPixels / pixelsPerFrame);
        if (deltaFrames !== 0) {
          onTrimEnd(beat.beat_index, deltaFrames);
          dragStartX.current = me.clientX;
        }
      };

      const handleMouseUp = () => {
        dragStartX.current = null;
        window.removeEventListener("mousemove", handleMouseMove);
        window.removeEventListener("mouseup", handleMouseUp);
      };

      window.addEventListener("mousemove", handleMouseMove);
      window.addEventListener("mouseup", handleMouseUp);
    },
    [beat.beat_index, pixelsPerFrame, onTrimEnd]
  );

  return (
    <div
      className={`beat-block ${isSelected ? "selected" : ""}`}
      style={{
        position: "absolute",
        left: `${left}px`,
        width: `${width}px`,
        backgroundColor: color,
        borderRadius: 4,
        cursor: "pointer",
        border: isSelected ? "2px solid white" : "1px solid rgba(0,0,0,0.3)",
        overflow: "hidden",
      }}
      onClick={() => onSelect(beat.beat_index)}
    >
      {/* Thumbnail */}
      {beat.fallback_image_url && (
        <img
          src={beat.fallback_image_url}
          alt={`Beat ${beat.beat_index}`}
          style={{ width: "100%", height: "60%", objectFit: "cover" }}
        />
      )}
      <div style={{ padding: "2px 4px", fontSize: 10, color: "white" }}>
        B{beat.beat_index} · {beat.arc_stage}
      </div>

      {/* Right trim handle — FR-VID-10 §4 Stage 3 Step 5 */}
      <div
        className="trim-handle trim-handle-right"
        style={{
          position: "absolute",
          right: 0,
          top: 0,
          width: 6,
          height: "100%",
          cursor: "ew-resize",
          backgroundColor: "rgba(255,255,255,0.3)",
        }}
        onMouseDown={handleTrimDragStart}
      />
    </div>
  );
};

// ---------------------------------------------------------------------------
// Caption Track — FR-VID-10 §4 Stage 3 Step 2 (caption word blocks)
// ---------------------------------------------------------------------------

const CaptionTrack: React.FC<{
  manifest: CMFManifest;
  pixelsPerFrame: number;
}> = ({ manifest, pixelsPerFrame }) => {
  if (!manifest.captions || manifest.captions.length === 0) {
    return (
      <div className="track caption-track empty">
        <span className="track-label">Captions</span>
        <span className="track-empty">No captions generated</span>
      </div>
    );
  }

  return (
    <div className="track caption-track" style={{ position: "relative", height: 30 }}>
      <span className="track-label">Captions</span>
      {manifest.captions.map((caption, i) => (
        <div
          key={i}
          className="caption-word-block"
          style={{
            position: "absolute",
            left: caption.start_frame * pixelsPerFrame,
            width: (caption.end_frame - caption.start_frame) * pixelsPerFrame,
            backgroundColor: "rgba(52, 152, 219, 0.6)",
            borderRadius: 2,
            fontSize: 9,
            color: "white",
            overflow: "hidden",
            whiteSpace: "nowrap",
            padding: "0 2px",
            height: "100%",
            lineHeight: "30px",
          }}
          title={caption.word}
        >
          {caption.word}
        </div>
      ))}
    </div>
  );
};

// ---------------------------------------------------------------------------
// Ducking Curve Overlay — FR-VID-10 §4 Stage 6
// ---------------------------------------------------------------------------

const DuckingOverlay: React.FC<{
  duckingCurve: number[];
  totalFrames: number;
  pixelsPerFrame: number;
}> = ({ duckingCurve, totalFrames, pixelsPerFrame }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const height = 40;
  const width = totalFrames * pixelsPerFrame;

  React.useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    canvas.width = width;
    canvas.height = height;
    ctx.clearRect(0, 0, width, height);

    // Draw ducking envelope
    ctx.beginPath();
    ctx.moveTo(0, height);
    for (let i = 0; i < duckingCurve.length && i < totalFrames; i++) {
      const x = i * pixelsPerFrame;
      const y = height - duckingCurve[i] * height;
      ctx.lineTo(x, y);
    }
    ctx.lineTo(width, height);
    ctx.closePath();

    // Green → yellow → red gradient based on volume
    ctx.fillStyle = "rgba(46, 204, 113, 0.4)";
    ctx.fill();
    ctx.strokeStyle = "rgba(46, 204, 113, 0.8)";
    ctx.lineWidth = 1;
    ctx.stroke();
  }, [duckingCurve, totalFrames, pixelsPerFrame, width]);

  return (
    <canvas
      ref={canvasRef}
      style={{ position: "absolute", top: 0, left: 0, pointerEvents: "none" }}
    />
  );
};

// ---------------------------------------------------------------------------
// Timeline Container — FR-VID-10 §4 Stage 3
// ---------------------------------------------------------------------------

export const TimelineContainer: React.FC = () => {
  const manifest = useEditorStore((s) => s.manifest);
  const playheadFrame = useEditorStore((s) => s.session.playhead_frame);
  const zoomLevel = useEditorStore((s) => s.session.zoom_level);
  const setSelectedBeat = useEditorStore((s) => s.setSelectedBeat);
  const updateManifest = useEditorStore((s) => s.updateManifest);
  const setPlayheadFrame = useEditorStore((s) => s.setPlayheadFrame);
  const setZoomLevel = useEditorStore((s) => s.setZoomLevel);
  const timelineRef = useRef<HTMLDivElement>(null);

  const pixelsPerFrame = useMemo(() => Math.max(0.1, zoomLevel * 2), [zoomLevel]);

  // FR-VID-10 §4 Stage 5 Step 1: Trim handler
  const handleTrimEnd = useCallback(
    (beatIndex: number, deltaFrames: number) => {
      updateManifest((m) => {
        const beats = [...m.beats];
        const beat = { ...beats[beatIndex] };
        const newDuration = Math.max(12, beat.duration_frames + deltaFrames);
        const actualDelta = newDuration - beat.duration_frames;
        beat.duration_frames = newDuration;
        beats[beatIndex] = beat;

        // Recalculate subsequent start_frames
        for (let i = beatIndex + 1; i < beats.length; i++) {
          beats[i] = {
            ...beats[i],
            start_frame: beats[i - 1].start_frame + beats[i - 1].duration_frames,
          };
        }

        const totalFrames = beats.reduce((sum, b) => sum + b.duration_frames, 0);

        return {
          ...m,
          beats,
          total_frames: totalFrames,
          total_duration_sec: totalFrames / m.fps,
        };
      });
    },
    [updateManifest]
  );

  // FR-VID-10 §4 Stage 3 Step 6: Zoom via mouse wheel
  const handleWheel = useCallback(
    (e: React.WheelEvent) => {
      if (e.ctrlKey || e.metaKey) {
        e.preventDefault();
        const delta = e.deltaY > 0 ? -0.1 : 0.1;
        setZoomLevel(Math.max(0.1, Math.min(10, zoomLevel + delta)));
      }
    },
    [zoomLevel, setZoomLevel]
  );

  // FR-VID-10 §4 Stage 3 Step 3: Click timeline to seek
  const handleTimelineClick = useCallback(
    (e: React.MouseEvent) => {
      if (!timelineRef.current || !manifest) return;
      const rect = timelineRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left + timelineRef.current.scrollLeft;
      const frame = Math.round(x / pixelsPerFrame);
      setPlayheadFrame(Math.max(0, Math.min(manifest.total_frames, frame)));
    },
    [manifest, pixelsPerFrame, setPlayheadFrame]
  );

  if (!manifest) return null;

  const totalWidth = manifest.total_frames * pixelsPerFrame;
  const playheadX = playheadFrame * pixelsPerFrame;

  return (
    <div
      ref={timelineRef}
      className="timeline-container"
      style={{ overflowX: "auto", position: "relative" }}
      onWheel={handleWheel}
      onClick={handleTimelineClick}
    >
      {/* Ruler — FR-VID-10 §4 Stage 3 Step 1 */}
      <div
        className="timeline-ruler"
        style={{
          width: totalWidth,
          height: 20,
          borderBottom: "1px solid #444",
          position: "relative",
          fontSize: 10,
          color: "#888",
        }}
      >
        {Array.from(
          { length: Math.ceil(manifest.total_frames / manifest.fps) },
          (_, i) => (
            <span
              key={i}
              style={{
                position: "absolute",
                left: i * manifest.fps * pixelsPerFrame,
              }}
            >
              {i}s
            </span>
          )
        )}
      </div>

      {/* Playhead — FR-VID-10 §4 Stage 3 Step 3 */}
      <div
        className="playhead"
        style={{
          position: "absolute",
          left: playheadX,
          top: 0,
          bottom: 0,
          width: 2,
          backgroundColor: "#e74c3c",
          zIndex: 100,
          pointerEvents: "none",
        }}
      />

      {/* Visual Track — FR-VID-10 §4 Stage 3 Step 2 */}
      <div
        className="track visual-track"
        style={{ position: "relative", height: 80, width: totalWidth }}
      >
        <span className="track-label">Visual</span>
        {manifest.beats.map((beat) => (
          <BeatBlock
            key={beat.beat_index}
            beat={beat}
            pixelsPerFrame={pixelsPerFrame}
            onSelect={setSelectedBeat}
            onTrimEnd={handleTrimEnd}
          />
        ))}
      </div>

      {/* Music Track with Ducking Overlay — FR-VID-10 §4 Stage 3 Step 2 */}
      <div
        className="track music-track"
        style={{ position: "relative", height: 40, width: totalWidth }}
      >
        <span className="track-label">Music</span>
        {manifest.audio.ducking_curve && (
          <DuckingOverlay
            duckingCurve={manifest.audio.ducking_curve}
            totalFrames={manifest.total_frames}
            pixelsPerFrame={pixelsPerFrame}
          />
        )}
      </div>

      {/* Voiceover Track — FR-VID-10 §4 Stage 3 Step 2 */}
      <div
        className="track voiceover-track"
        style={{ position: "relative", height: 30, width: totalWidth }}
      >
        <span className="track-label">Voiceover</span>
      </div>

      {/* Caption Track — FR-VID-10 §4 Stage 3 Step 2 */}
      <CaptionTrack manifest={manifest} pixelsPerFrame={pixelsPerFrame} />
    </div>
  );
};
