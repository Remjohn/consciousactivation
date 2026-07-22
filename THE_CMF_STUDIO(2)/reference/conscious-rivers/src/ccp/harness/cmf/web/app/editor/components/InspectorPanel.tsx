/**
 * Inspector Panel — Selected beat properties, asset details, editing controls.
 *
 * FR-VID-10 §4 Stage 3 Step 4: Beat selection populates Inspector with properties.
 * FR-VID-10 §4 Stage 5 Steps 3, 6: Asset swap and transition change.
 */

"use client";

import React, { useCallback } from "react";

import { useEditorStore } from "../store";

// Available transitions from DEP-VID-003
const TRANSITIONS = [
  "cut",
  "crossfade",
  "dissolve",
  "wipe",
  "slide",
  "zoom",
];

export const InspectorPanel: React.FC = () => {
  const manifest = useEditorStore((s) => s.manifest);
  const selectedBeatIndex = useEditorStore(
    (s) => s.session.selected_beat_index
  );
  const updateManifest = useEditorStore((s) => s.updateManifest);

  const beat =
    manifest && selectedBeatIndex !== null
      ? manifest.beats[selectedBeatIndex]
      : null;

  // FR-VID-10 §4 Stage 5 Step 6: Change transition
  const handleTransitionChange = useCallback(
    (newType: string) => {
      if (selectedBeatIndex === null) return;
      updateManifest((m) => ({
        ...m,
        beats: m.beats.map((b, i) =>
          i === selectedBeatIndex
            ? {
                ...b,
                transition: { ...b.transition, type: newType },
              }
            : b
        ),
      }));
    },
    [selectedBeatIndex, updateManifest]
  );

  // FR-VID-10 §4 Stage 5 Step 5: Delete beat
  const handleDeleteBeat = useCallback(() => {
    if (selectedBeatIndex === null || !manifest) return;
    if (
      manifest.beats.length <= 1 &&
      manifest.beats[0]?.arc_stage === beat?.arc_stage
    ) {
      if (
        !confirm(
          `This is the only beat of arc_stage "${beat?.arc_stage}". Delete anyway?`
        )
      ) {
        return;
      }
    }
    updateManifest((m) => {
      const beats = m.beats
        .filter((_, i) => i !== selectedBeatIndex)
        .map((b, i) => ({
          ...b,
          beat_index: i,
          start_frame:
            i === 0
              ? 0
              : m.beats
                  .filter((_, j) => j !== selectedBeatIndex)
                  .slice(0, i)
                  .reduce((sum, prev) => sum + prev.duration_frames, 0),
        }));
      const totalFrames = beats.reduce(
        (sum, b) => sum + b.duration_frames,
        0
      );
      return {
        ...m,
        beats,
        total_frames: totalFrames,
        total_duration_sec: totalFrames / m.fps,
      };
    });
  }, [selectedBeatIndex, manifest, beat, updateManifest]);

  // FR-VID-10 §4 Stage 5 Step 2: Split at playhead
  const handleSplit = useCallback(() => {
    if (selectedBeatIndex === null || !manifest) return;
    const playhead = useEditorStore.getState().session.playhead_frame;
    const selectedBeat = manifest.beats[selectedBeatIndex];

    const splitFrame = playhead - selectedBeat.start_frame;
    if (splitFrame <= 0 || splitFrame >= selectedBeat.duration_frames) {
      alert("Playhead is not within the selected beat.");
      return;
    }
    if (splitFrame < 12 || selectedBeat.duration_frames - splitFrame < 12) {
      alert("Split would create a beat shorter than 12 frames (0.5s).");
      return;
    }

    updateManifest((m) => {
      const beats = [...m.beats];
      const original = beats[selectedBeatIndex];

      const beatA = {
        ...original,
        duration_frames: splitFrame,
        transition: { type: "cut", duration_frames: 0, preset_id: "" },
      };
      const beatB = {
        ...original,
        beat_index: selectedBeatIndex + 1,
        start_frame: original.start_frame + splitFrame,
        duration_frames: original.duration_frames - splitFrame,
      };

      beats.splice(selectedBeatIndex, 1, beatA, beatB);

      // Re-index all beats
      const reindexed = beats.map((b, i) => ({
        ...b,
        beat_index: i,
        start_frame:
          i === 0
            ? 0
            : beats
                .slice(0, i)
                .reduce((sum, prev) => sum + prev.duration_frames, 0),
      }));

      return { ...m, beats: reindexed };
    });
  }, [selectedBeatIndex, manifest, updateManifest]);

  if (!beat) {
    return (
      <div className="inspector-panel">
        <h3>Inspector</h3>
        <p className="no-selection">Select a beat in the timeline</p>
      </div>
    );
  }

  return (
    <div className="inspector-panel">
      <h3>Inspector — Beat {beat.beat_index}</h3>

      <div className="inspector-fields">
        <div className="field">
          <label>Beat Type</label>
          <span>{beat.beat_type}</span>
        </div>
        <div className="field">
          <label>Arc Stage</label>
          <span>{beat.arc_stage}</span>
        </div>
        <div className="field">
          <label>Duration</label>
          <span>{beat.duration_frames} frames ({(beat.duration_frames / (manifest?.fps || 24)).toFixed(2)}s)</span>
        </div>
        <div className="field">
          <label>Start Frame</label>
          <span>{beat.start_frame}</span>
        </div>
        <div className="field">
          <label>Asset Status</label>
          <span>{beat.asset_status}</span>
        </div>
        <div className="field">
          <label>Video URL</label>
          <span className="url-field">{beat.video_clip_url || "—"}</span>
        </div>

        {/* Transition — FR-VID-10 §4 Stage 5 Step 6 */}
        <div className="field">
          <label>Transition</label>
          <select
            value={beat.transition.type}
            onChange={(e) => handleTransitionChange(e.target.value)}
          >
            {TRANSITIONS.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
        </div>

        {/* Asset thumbnail — click to swap (FR-VID-10 §4 Stage 5 Step 3) */}
        <div className="field">
          <label>Asset</label>
          {beat.fallback_image_url && (
            <img
              src={beat.fallback_image_url}
              alt="Beat asset"
              className="asset-thumbnail"
              title="Click to swap asset"
            />
          )}
        </div>
      </div>

      {/* Beat actions */}
      <div className="inspector-actions">
        <button onClick={handleSplit} title="Split at playhead">
          ✂️ Split
        </button>
        <button
          onClick={handleDeleteBeat}
          title="Delete beat"
          className="danger"
        >
          🗑️ Delete
        </button>
      </div>
    </div>
  );
};
