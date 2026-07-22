import { useMemo, useState } from "react";
import { useTimelineWorkbench } from "./TimelineWorkbenchProvider.jsx";
import { TimelineTrackLane } from "./TimelineTrackLane.jsx";

const visibleCount = 12;

export function TrackLaneStack() {
  const { workbenchState, draftState, nudgePlayhead } = useTimelineWorkbench();
  const [startLane, setStartLane] = useState(0);
  const lanes = workbenchState?.lanes || [];
  const visibleLanes = useMemo(() => lanes.slice(startLane, startLane + visibleCount), [lanes, startLane]);

  if (!workbenchState) return null;

  const maxStart = Math.max(0, lanes.length - visibleCount);
  const playheadLeft = (draftState.playheadFrame / workbenchState.duration_frames) * 100;

  function onKeyDown(event) {
    if (event.key === "ArrowRight") nudgePlayhead(1);
    if (event.key === "ArrowLeft") nudgePlayhead(-1);
    if (event.key === "PageDown") nudgePlayhead(30);
    if (event.key === "PageUp") nudgePlayhead(-30);
  }

  return (
    <section className="timeline-stack" aria-label="Video timeline lanes">
      <div className="timeline-stack-header">
        <div>
          <span>Virtualized lane stack</span>
          <strong>Showing {visibleLanes.length} of {lanes.length} lanes</strong>
        </div>
        <div className="timeline-stack-actions">
          <button type="button" onClick={() => setStartLane(Math.max(0, startLane - 4))}>Prev lanes</button>
          <button type="button" onClick={() => setStartLane(Math.min(maxStart, startLane + 4))}>Next lanes</button>
        </div>
      </div>
      <div
        className="timeline-lanes"
        tabIndex={0}
        onKeyDown={onKeyDown}
        aria-label="Timeline. Use left and right arrows to nudge by one frame, page keys by one second."
      >
        <div className="timeline-playhead" style={{ left: `${playheadLeft}%` }}>
          <span>{draftState.playheadFrame}f</span>
        </div>
        {visibleLanes.map((lane) => (
          <TimelineTrackLane key={lane.lane_id} lane={lane} durationFrames={workbenchState.duration_frames} />
        ))}
      </div>
    </section>
  );
}

