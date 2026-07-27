/**
 * Preview Panel — @remotion/player integration for zero-cost in-browser preview.
 *
 * FR-VID-10 §4 Stage 2: Embeds <Player> with manifest as inputProps.
 * Preview updates reactively when manifest changes in Zustand store.
 * FR-VID-10 §3 TD2: Zero GPU cost — client-side React composition.
 */

"use client";

import React, { useCallback, useRef } from "react";
import { Player, type PlayerRef } from "@remotion/player";

import { CMFComposition } from "@cmf/remotion-compositions";
import type { CMFManifest } from "@cmf/remotion-compositions";

import { useEditorStore } from "../store";

interface PreviewPanelProps {
  manifest: CMFManifest;
}

export const PreviewPanel: React.FC<PreviewPanelProps> = ({ manifest }) => {
  const playerRef = useRef<PlayerRef>(null);
  const setPlayheadFrame = useEditorStore((s) => s.setPlayheadFrame);

  // FR-VID-10 §4 Stage 2 Step 8: Playback controls sync with timeline
  const handleFrameChange = useCallback(
    (frame: number) => {
      setPlayheadFrame(frame);
    },
    [setPlayheadFrame]
  );

  // FR-VID-10 §4 Stage 2 Steps 6-7: Player renders composition from manifest
  return (
    <div className="preview-panel">
      <Player
        ref={playerRef}
        component={CMFComposition}
        inputProps={{ manifest }}
        compositionWidth={1080}
        compositionHeight={1920}
        fps={manifest.fps}
        durationInFrames={manifest.total_frames}
        style={{ height: "100%", maxHeight: "80vh", aspectRatio: "9/16", margin: "0 auto", display: "block", borderRadius: "12px", overflow: "hidden" }}
        controls
        loop={false}
        clickToPlay
        doubleClickToFullscreen
      />
      <div className="preview-controls">
        <span>
          {Math.floor(
            (useEditorStore.getState().session.playhead_frame / manifest.fps) * 100
          ) / 100}
          s / {manifest.total_duration_sec}s
        </span>
        <span>{manifest.total_frames} frames @ {manifest.fps}fps</span>
      </div>
    </div>
  );
};
