import { useTimelineWorkbench } from "./TimelineWorkbenchProvider.jsx";

const beats = [
  { frame: 90, label: "Question lands", role: "interviewer cue" },
  { frame: 340, label: "Guest pauses", role: "emotional evidence" },
  { frame: 620, label: "Phrase: not empty", role: "source quote" },
  { frame: 910, label: "Room calculation", role: "alignment blocker" },
  { frame: 1290, label: "Audience mirror", role: "reaction prompt" },
];

export function TranscriptBeatPanel() {
  const { workbenchState, draftState, setPlayhead } = useTimelineWorkbench();
  if (!workbenchState) return null;

  return (
    <section className="transcript-beat-panel" aria-label="Transcript beat map">
      <div className="timeline-panel-heading">
        <span>Transcript Beat Map</span>
        <strong>{workbenchState.beat_map_ref}</strong>
      </div>
      <div className="beat-list">
        {beats.map((beat) => (
          <button
            type="button"
            key={beat.frame}
            className={Math.abs(draftState.playheadFrame - beat.frame) < 45 ? "active" : ""}
            onClick={() => setPlayhead(beat.frame)}
          >
            <span>{formatFrame(beat.frame, workbenchState.fps)}</span>
            <strong>{beat.label}</strong>
            <small>{beat.role}</small>
          </button>
        ))}
      </div>
    </section>
  );
}

function formatFrame(frame, fps) {
  const seconds = Math.round(frame / fps);
  return `00:${String(seconds).padStart(2, "0")}`;
}

