import { useTimelineWorkbench } from "./TimelineWorkbenchProvider.jsx";

export function TimelineRuler() {
  const { workbenchState, draftState, setPlayhead, setZoom } = useTimelineWorkbench();
  if (!workbenchState) return null;

  const ticks = Array.from({ length: 11 }, (_, index) => {
    const frame = Math.round((workbenchState.duration_frames / 10) * index);
    return { frame, left: (frame / workbenchState.duration_frames) * 100 };
  });
  const playheadLeft = (draftState.playheadFrame / workbenchState.duration_frames) * 100;

  return (
    <div className="timeline-ruler" aria-label="Timeline ruler">
      <div className="timeline-controls">
        <button type="button" onClick={() => setPlayhead(Math.max(0, draftState.playheadFrame - 30))}>-1s</button>
        <button type="button" onClick={() => setPlayhead(Math.min(workbenchState.duration_frames, draftState.playheadFrame + 30))}>+1s</button>
        <button type="button" onClick={() => setZoom(draftState.zoom + 0.2)}>Zoom in</button>
        <button type="button" onClick={() => setZoom(draftState.zoom - 0.2)}>Zoom out</button>
      </div>
      <div className="ruler-track">
        {ticks.map((tick) => (
          <button
            type="button"
            key={tick.frame}
            className="ruler-tick"
            style={{ left: `${tick.left}%` }}
            onClick={() => setPlayhead(tick.frame)}
            aria-label={`Move playhead to frame ${tick.frame}`}
          >
            <span>{formatTime(tick.frame, workbenchState.fps)}</span>
          </button>
        ))}
        <div className="ruler-playhead" style={{ left: `${playheadLeft}%` }} />
      </div>
    </div>
  );
}

function formatTime(frame, fps) {
  const seconds = Math.floor(frame / fps);
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${String(secs).padStart(2, "0")}`;
}

