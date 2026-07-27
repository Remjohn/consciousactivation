import { useTimelineWorkbench } from "./TimelineWorkbenchProvider.jsx";

export function TimelineInspector() {
  const { workbenchState, selectedSegment, selectedLane, createDraft, rerenderProxy, exportOtio, onStartRender } = useTimelineWorkbench();
  if (!workbenchState) return null;

  const markers = selectedSegment
    ? workbenchState.markers.filter((marker) => marker.lane_id === selectedSegment.lane_id)
    : workbenchState.markers;
  const renderJob = workbenchState.last_render_job_state;
  const renderQa = workbenchState.last_render_qa;

  return (
    <aside className="timeline-inspector" aria-label="Timeline inspector">
      <div className="timeline-panel-heading">
        <span>Inspector</span>
        <strong>{selectedSegment ? selectedSegment.label : "No segment selected"}</strong>
      </div>

      {selectedSegment && (
        <>
          <div className="inspector-grid">
            <Info label="Lane" value={selectedLane?.display_name || selectedSegment.lane_id} />
            <Info label="Type" value={selectedSegment.segment_type} />
            <Info label="Frames" value={`${selectedSegment.time_range.start_frame}-${selectedSegment.time_range.end_frame}`} />
            <Info label="Locked" value={selectedSegment.locked ? "yes" : "no"} />
          </div>

          <div className="primitive-list">
            <span>Primitive IDs</span>
            {selectedSegment.primitive_refs.map((primitive) => (
              <strong key={primitive}>{primitive}</strong>
            ))}
          </div>

          {selectedSegment.blocker_codes.length > 0 && (
            <div className="blocker-callout">
              <span>Hard blocker</span>
              <strong>{selectedSegment.blocker_codes.join(", ")}</strong>
            </div>
          )}

          <div className="inspector-actions">
            <button type="button" onClick={() => createDraft("trim", { nudge_frames: 12 })} disabled={selectedSegment.locked}>
              Create trim draft
            </button>
            <button type="button" onClick={() => createDraft("remove_segment", { reason: "operator_cut_out" })} disabled={selectedSegment.locked}>
              Cut out segment
            </button>
            <button
              type="button"
              onClick={() => createDraft("fix_quote_alignment", { replacement_label: "The silence was full of calculations." })}
              disabled={selectedSegment.blocker_codes.length === 0}
            >
              Fix quote alignment
            </button>
            <button type="button" onClick={() => createDraft("request_repair", { target: selectedSegment.blocker_codes[0] || "timing_review" })}>
              Request repair
            </button>
          </div>
        </>
      )}

      <div className="marker-list">
        <span>Markers</span>
        {markers.map((marker) => (
          <article className={`marker-row ${marker.severity}`} key={marker.marker_id}>
            <strong>{marker.label}</strong>
            <small>{marker.marker_type} / {marker.severity}</small>
          </article>
        ))}
      </div>
      <div className="inspector-render-status">
        <span>Proxy render</span>
        <strong>{renderJob?.job_status || workbenchState.playback_proxy_status}</strong>
        <small>{renderJob?.output_uri || workbenchState.output_preview_url || workbenchState.proxy_render_ref}</small>
        {renderQa && <small>QA {renderQa.pass_status} / {renderQa.blockers?.length || 0} blockers</small>}
      </div>
      <div className="timeline-render-actions">
        <button type="button" onClick={rerenderProxy}>Rerender proxy</button>
        <button type="button" onClick={exportOtio}>Export OTIO</button>
        <button type="button" onClick={onStartRender}>Start final render</button>
      </div>
    </aside>
  );
}

function Info({ label, value }) {
  return (
    <div>
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
