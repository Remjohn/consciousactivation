import { useState } from "react";
import { timelineFormatOptions } from "../fixtures/videoTimelineWorkbench.fixture.js";
import { TimelineWorkbenchProvider, useTimelineWorkbench } from "../components/timeline/TimelineWorkbenchProvider.jsx";
import { ProxyPreviewPanel } from "../components/timeline/ProxyPreviewPanel.jsx";
import { TranscriptBeatPanel } from "../components/timeline/TranscriptBeatPanel.jsx";
import { TimelineRuler } from "../components/timeline/TimelineRuler.jsx";
import { TrackLaneStack } from "../components/timeline/TrackLaneStack.jsx";
import { TimelineInspector } from "../components/timeline/TimelineInspector.jsx";
import { TimelineCommandDrawer } from "../components/timeline/TimelineCommandDrawer.jsx";
import "../styles/timeline.css";

export function VideoTimelineWorkbench({ activeGuest, onCommandReceipt, onStartRender }) {
  const [activeFormat, setActiveFormat] = useState("SV-RRC");

  return (
    <TimelineWorkbenchProvider activeFormat={activeFormat} onCommandReceipt={onCommandReceipt} onStartRender={onStartRender}>
      <TimelineWorkbenchInner activeGuest={activeGuest} activeFormat={activeFormat} setActiveFormat={setActiveFormat} />
    </TimelineWorkbenchProvider>
  );
}

function TimelineWorkbenchInner({ activeGuest, activeFormat, setActiveFormat }) {
  const { workbenchState, loadState, error, fixtureMode } = useTimelineWorkbench();

  if (loadState === "failed") {
    return (
      <main className="screen">
        <section className="panel">
          <h2>Timeline unavailable</h2>
          <p>{error?.message || "The timeline read model could not be loaded."}</p>
        </section>
      </main>
    );
  }

  return (
    <main className="screen video-timeline-workbench">
      {fixtureMode && (
        <section className="timeline-fixture-banner" role="status">
          <strong>Fixture mode</strong>
          <span>Design QA only. Production must load `VideoTimelineWorkbenchState` from the backend read model.</span>
        </section>
      )}

      <section className="timeline-hero">
        <div>
          <span className="eyebrow amber">TS-CMF-144</span>
          <h2>Video Timeline Workbench</h2>
          <p>
            Frame-accurate review surface for `VideoEditProgram`, transcript beats, composition lanes, proxy preview,
            primitive markers, repair commands, and OTIO readiness.
          </p>
        </div>
        <div className="timeline-scope-card">
          <span>Active scope</span>
          <strong>{activeGuest.workspace} / {activeGuest.name}</strong>
          <small>{workbenchState?.asset_code || "Loading timeline state"}</small>
        </div>
      </section>

      <section className="timeline-format-strip" aria-label="Video format selection">
        {timelineFormatOptions.map((format) => (
          <button
            type="button"
            key={format.formatSlot}
            className={activeFormat === format.formatSlot ? "active" : ""}
            onClick={() => setActiveFormat(format.formatSlot)}
          >
            <span>{format.formatSlot}</span>
            <strong>{format.name}</strong>
            <small>{format.role}</small>
          </button>
        ))}
      </section>

      <section className="timeline-workbench-grid">
        <div className="timeline-left-column">
          <ProxyPreviewPanel />
          <TranscriptBeatPanel />
        </div>
        <div className="timeline-center-column">
          <TimelineRuler />
          <TrackLaneStack />
          <TimelineCommandDrawer />
        </div>
        <TimelineInspector />
      </section>
    </main>
  );
}
