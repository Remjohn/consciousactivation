/**
 * Review Panel — Beat-level review with approve/reject/regenerate controls.
 *
 * FR-VID-10 §4 Stage 4: Thumbnail gallery, per-beat action buttons,
 * global controls (Approve All, Auto-Approve, Render Final, Cost Counter).
 * Regeneration status polling. Limit: 10 per beat.
 */

"use client";

import React, { useCallback, useState } from "react";

import {
  fetchManifest,
  pollRegeneration,
  startRegeneration,
} from "../api-client";
import type { ReviewBeatState } from "../store";
import { useEditorStore } from "../store";

interface ReviewPanelProps {
  videoId: string;
}

// FR-VID-10 §4 Stage 4 Step 2: Quality score color coding
function scoreColor(score: number): string {
  if (score >= 0.8) return "#2ecc71";
  if (score >= 0.6) return "#f1c40f";
  return "#e74c3c";
}

// ---------------------------------------------------------------------------
// Beat Review Card
// ---------------------------------------------------------------------------

const BeatReviewCard: React.FC<{
  review: ReviewBeatState;
  videoId: string;
  manifest: ReturnType<typeof useEditorStore.getState>["manifest"];
}> = ({ review, videoId, manifest }) => {
  const updateBeatReview = useEditorStore((s) => s.updateBeatReview);
  const setManifest = useEditorStore((s) => s.setManifest);
  const [regenLoading, setRegenLoading] = useState(false);
  const [revisionNote, setRevisionNote] = useState("");
  const [showNoteInput, setShowNoteInput] = useState(false);

  const beat = manifest?.beats[review.beat_index];
  if (!beat) return null;

  // FR-VID-10 §4 Stage 4 Step 3: Per-beat actions
  const handleApprove = useCallback(() => {
    updateBeatReview(review.beat_index, "APPROVED");
  }, [review.beat_index, updateBeatReview]);

  const handleRegenerate = useCallback(
    async (mode: "T2I_ONLY" | "I2V_ONLY" | "BOTH") => {
      // FR-VID-10 §4 Stage 4 Step 6: Regeneration limit (10 max)
      if (review.regen_count >= 10) {
        alert(
          "Maximum regenerations reached — consider manual asset upload."
        );
        return;
      }

      setRegenLoading(true);
      updateBeatReview(review.beat_index, "REGENERATING");

      try {
        const { job_id } = await startRegeneration(videoId, {
          beat_index: review.beat_index,
          mode,
          revision_note: revisionNote || undefined,
        });

        // Poll for completion
        let status = await pollRegeneration(videoId, job_id);
        while (status.status === "PENDING" || status.status === "RUNNING") {
          await new Promise((r) => setTimeout(r, 2000));
          status = await pollRegeneration(videoId, job_id);
        }

        if (status.status === "COMPLETE" && status.result_manifest) {
          setManifest(status.result_manifest);
        }

        updateBeatReview(
          review.beat_index,
          status.status === "COMPLETE" ? "PENDING_REVIEW" : "PENDING_REVIEW"
        );
      } catch (err) {
        console.error("Regeneration failed:", err);
        updateBeatReview(review.beat_index, "PENDING_REVIEW");
      } finally {
        setRegenLoading(false);
        setShowNoteInput(false);
        setRevisionNote("");
      }
    },
    [
      review.beat_index,
      review.regen_count,
      videoId,
      revisionNote,
      updateBeatReview,
      setManifest,
    ]
  );

  return (
    <div className="beat-review-card">
      {/* Thumbnail */}
      <div className="beat-thumbnail">
        {regenLoading && <div className="spinner-overlay">⏳</div>}
        {beat.fallback_image_url ? (
          <img src={beat.fallback_image_url} alt={`Beat ${beat.beat_index}`} />
        ) : (
          <div className="no-thumbnail">B{beat.beat_index}</div>
        )}
      </div>

      {/* Info */}
      <div className="beat-info">
        <span>Beat {beat.beat_index}</span>
        <span className="arc-badge">{beat.arc_stage}</span>
        <span
          className="quality-score"
          style={{ color: scoreColor(review.quality_score) }}
        >
          {review.quality_score.toFixed(2)}
        </span>
        <span className="status-badge">{review.status}</span>
        {review.regen_count > 0 && (
          <span className="regen-count">
            Regens: {review.regen_count}/10
            {review.regen_count >= 5 && " ⚠️"}
          </span>
        )}
      </div>

      {/* Actions — FR-VID-10 §4 Stage 4 Step 3 */}
      <div className="beat-actions">
        <button onClick={handleApprove} disabled={regenLoading} title="Approve">
          ✅
        </button>
        <button
          onClick={() => setShowNoteInput(true)}
          disabled={regenLoading}
          title="Regen T2I"
        >
          🖼️
        </button>
        <button
          onClick={() => handleRegenerate("I2V_ONLY")}
          disabled={regenLoading}
          title="Regen I2V"
        >
          🎬
        </button>
        <button
          onClick={() => handleRegenerate("BOTH")}
          disabled={regenLoading}
          title="Regen Both"
        >
          🔄
        </button>
      </div>

      {/* Revision note input */}
      {showNoteInput && (
        <div className="revision-note">
          <input
            type="text"
            value={revisionNote}
            onChange={(e) => setRevisionNote(e.target.value)}
            placeholder="Revision note (e.g., warmer color palette)"
          />
          <button onClick={() => handleRegenerate("T2I_ONLY")}>Submit</button>
          <button onClick={() => setShowNoteInput(false)}>Cancel</button>
        </div>
      )}
    </div>
  );
};

// ---------------------------------------------------------------------------
// Review Panel — FR-VID-10 §4 Stage 4
// ---------------------------------------------------------------------------

export const ReviewPanel: React.FC<ReviewPanelProps> = ({ videoId }) => {
  const manifest = useEditorStore((s) => s.manifest);
  const beatReviews = useEditorStore((s) => s.beatReviews);
  const updateBeatReview = useEditorStore((s) => s.updateBeatReview);

  // FR-VID-10 §4 Stage 4 Step 4: Global controls
  const allApproved = beatReviews.every((r) => r.status === "APPROVED");
  const allHighQuality = beatReviews.every((r) => r.quality_score >= 0.8);

  const handleApproveAll = useCallback(() => {
    beatReviews.forEach((r) => updateBeatReview(r.beat_index, "APPROVED"));
  }, [beatReviews, updateBeatReview]);

  return (
    <div className="review-panel">
      <h3>Review</h3>

      {/* Global controls — FR-VID-10 §4 Stage 4 Step 4 */}
      <div className="review-global-controls">
        <button
          onClick={handleApproveAll}
          disabled={allApproved}
          title="Approve all beats"
        >
          Approve All
        </button>
        <button disabled={!allApproved} title="All beats must be approved">
          🎬 Render Final
        </button>
        {allHighQuality && (
          <span className="auto-approve-hint">
            All scores ≥ 0.8 — auto-approve eligible
          </span>
        )}
      </div>

      {/* Beat gallery — FR-VID-10 §4 Stage 4 Steps 1-2 */}
      <div className="beat-gallery">
        {beatReviews.map((review) => (
          <BeatReviewCard
            key={review.beat_index}
            review={review}
            videoId={videoId}
            manifest={manifest}
          />
        ))}
      </div>
    </div>
  );
};
