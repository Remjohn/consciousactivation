import { TimelineSegment } from "./TimelineSegment.jsx";

export function TimelineTrackLane({ lane, durationFrames }) {
  return (
    <div className={`timeline-lane ${lane.editable ? "editable" : "locked"}`}>
      <div className="lane-label">
        <strong>{lane.display_name}</strong>
        <span>{lane.lane_kind} / {lane.editable ? "editable" : "locked"}</span>
      </div>
      <div className="lane-track">
        {lane.segments.map((segment) => (
          <TimelineSegment key={segment.segment_id} segment={segment} durationFrames={durationFrames} />
        ))}
      </div>
    </div>
  );
}

