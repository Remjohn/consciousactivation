import { useTimelineWorkbench } from "./TimelineWorkbenchProvider.jsx";

export function TimelineSegment({ segment, durationFrames }) {
  const { draftState, selectSegment } = useTimelineWorkbench();
  const start = (segment.time_range.start_frame / durationFrames) * 100;
  const width = ((segment.time_range.end_frame - segment.time_range.start_frame) / durationFrames) * 100;
  const active = draftState.selectedSegmentId === segment.segment_id;
  const blocked = segment.blocker_codes?.length > 0;

  return (
    <button
      type="button"
      className={`timeline-segment ${segment.segment_type} ${active ? "active" : ""} ${blocked ? "blocked" : ""}`}
      style={{ left: `${start}%`, width: `${Math.max(width, 1.2)}%` }}
      onClick={() => selectSegment(segment.segment_id)}
      aria-pressed={active}
      aria-label={`${segment.label}, frames ${segment.time_range.start_frame} to ${segment.time_range.end_frame}`}
    >
      <span>{segment.label}</span>
    </button>
  );
}

