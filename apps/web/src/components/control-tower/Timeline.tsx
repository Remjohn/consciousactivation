// TS-APP-UI-003 - Timeline component
// Read-only track/item visualization

import { useMemo } from "react";
import type { TimelineProjection } from "../../api/campaigns";

interface TimelineProps {
  campaignId: string;
  timeline: TimelineProjection | null;
}

export function Timeline({ campaignId, timeline }: TimelineProps) {
  // Handle null timeline (nothing compiled yet)
  if (!timeline) {
    return (
      <div className="control-tower-card">
        <div className="control-tower-card-header">
          <span>Timeline</span>
        </div>
        <p className="text-ca-text-secondary">
          Nothing has been compiled yet for this campaign
        </p>
      </div>
    );
  }

  const { tracks, duration_frames, fps_numerator, fps_denominator } = timeline;

  // Calculate duration in seconds
  const durationSeconds = useMemo(() => {
    if (!duration_frames || !fps_numerator || !fps_denominator) return 0;
    return (duration_frames / (fps_numerator / fps_denominator)).toFixed(1);
  }, [duration_frames, fps_numerator, fps_denominator]);

  // Sort tracks by z_index (highest first = top of timeline)
  const sortedTracks = useMemo(() => {
    return [...(tracks ?? [])].sort((a, b) => b.z_index - a.z_index);
  }, [tracks]);

  return (
    <div className="control-tower-card">
      <div className="control-tower-card-header">
        <span>Timeline</span>
        <span className="text-xs text-ca-text-secondary">
          {durationSeconds}s ({duration_frames} frames @ {fps_numerator}/{fps_denominator} fps)
        </span>
      </div>

      {/* Timeline ruler */}
      <div className="relative mb-4 h-8 rounded bg-ca-surface-raised">
        <div className="absolute inset-0 flex items-end justify-between px-2 pb-1">
          {[0, 25, 50, 75, 100].map((pct) => (
            <div key={pct} className="text-xs text-ca-text-tertiary">
              {((parseFloat(durationSeconds) * pct) / 100).toFixed(1)}s
            </div>
          ))}
        </div>
      </div>

      {/* Tracks */}
      <div className="space-y-2">
        {sortedTracks.map((track) => (
          <div key={track.track_id} className="rounded bg-ca-surface-raised p-2">
            <div className="mb-1 text-xs text-ca-text-secondary">
              Track: {track.track_id} (z-index: {track.z_index})
            </div>
            <div className="relative h-12 rounded bg-ca-bg">
              {track.items?.map((item: any) => {
                // Calculate position and width as percentage
                const leftPct = duration_frames
                  ? (item.start_frame / duration_frames) * 100
                  : 0;
                const widthPct = duration_frames
                  ? ((item.end_frame - item.start_frame) / duration_frames) * 100
                  : 0;

                return (
                  <div
                    key={item.item_id}
                    className="absolute top-1 bottom-1 rounded bg-ca-gold-500/20 border border-ca-gold-500 cursor-pointer hover:bg-ca-gold-500/30 transition-colors"
                    style={{
                      left: `${leftPct}%`,
                      width: `${widthPct}%`,
                    }}
                    title={`${item.item_id}: ${item.start_frame}-${item.end_frame}`}
                  >
                    <div className="px-1 text-xs text-ca-gold-300 truncate">
                      {item.item_id.slice(0, 8)}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {(!tracks || tracks.length === 0) && (
        <p className="text-center text-ca-text-tertiary">No tracks in timeline</p>
      )}
    </div>
  );
}
