import { useTimelineWorkbench } from "./TimelineWorkbenchProvider.jsx";

export function ProxyPreviewPanel() {
  const { workbenchState, draftState } = useTimelineWorkbench();
  if (!workbenchState) return null;

  const format = workbenchState.format_slot;
  const meta = workbenchState.format_meta;
  const progress = (draftState.playheadFrame / workbenchState.duration_frames) * 100;
  const renderJob = workbenchState.last_render_job_state;
  const renderQa = workbenchState.last_render_qa;
  const previewUrl = workbenchState.output_preview_url || workbenchState.proxy_render_ref;

  return (
    <section className={`proxy-preview-panel ${format.toLowerCase()}`} aria-label="Proxy preview">
      <div className="proxy-frame">
        <div className="proxy-chrome">
          <span>{format}</span>
          <strong>{workbenchState.playback_proxy_status}</strong>
        </div>
        <PreviewComposition format={format} meta={meta} />
        <div className="proxy-progress">
          <span style={{ width: `${progress}%` }} />
        </div>
      </div>
      <div className="proxy-proof">
        <div>
          <span>Renderer props hash</span>
          <strong>{workbenchState.renderer_props_hash}</strong>
        </div>
        <div>
          <span>Proxy ref</span>
          <strong>{workbenchState.proxy_render_ref}</strong>
        </div>
      </div>
      <div className="proxy-render-state">
        <div>
          <span>Render job</span>
          <strong>{renderJob?.job_status || workbenchState.playback_proxy_status}</strong>
          <small>{renderJob?.render_job_id || "No worker job yet"}</small>
        </div>
        <div>
          <span>Worker lease</span>
          <strong>{renderJob?.worker_id || "pending"}</strong>
          <small>{renderJob?.lease_id || "no lease"}</small>
        </div>
      </div>
      <div className="proxy-output-link">
        <span>Output preview</span>
        {previewUrl ? (
          <a href={previewUrl} target="_blank" rel="noreferrer">{previewUrl}</a>
        ) : (
          <strong>pending</strong>
        )}
      </div>
      {renderQa && (
        <div className={`proxy-qa-panel ${renderQa.pass_status}`}>
          <div>
            <span>Render QA</span>
            <strong>{renderQa.pass_status}</strong>
          </div>
          <div className="proxy-qa-grid">
            <small>ffprobe: {renderQa.ffprobe_status}</small>
            <small>frames: {renderQa.frame_sampling_status}</small>
            <small>audio: {renderQa.audio_level_status}</small>
            <small>duration: {renderQa.duration_tolerance_status}</small>
          </div>
          {renderQa.blockers?.length > 0 && <small>{renderQa.blockers.join(", ")}</small>}
        </div>
      )}
    </section>
  );
}

function PreviewComposition({ format, meta }) {
  if (format === "SV-EDU") {
    return (
      <div className="preview-composition papercut-preview">
        <div className="paper-chip">MYTH</div>
        <h3>{meta.previewSubhead}</h3>
        <div className="paper-path">
          <span>Claim</span>
          <span>Evidence</span>
          <span>Truth</span>
        </div>
        <div className="paper-human">2D avatar rig</div>
      </div>
    );
  }

  if (format === "SV-FRB") {
    return (
      <div className="preview-composition frame-breaker-preview">
        <h3>{meta.previewHeadline}</h3>
        <p>{meta.previewSubhead}</p>
        <div className="versus-block">
          <span>Protects you</span>
          <strong>VS</strong>
          <span>Betrays you</span>
        </div>
        <div className="lower-host">Human reaction</div>
      </div>
    );
  }

  if (format === "SV-RRC") {
    return (
      <div className="preview-composition living-reaction-preview">
        <div className="reaction-board">
          <h3>{meta.previewHeadline}</h3>
          <p>{meta.previewSubhead}</p>
          <div className="reaction-options">
            <span>Survival</span>
            <span>Betrayal</span>
          </div>
        </div>
        <div className="reaction-people">
          <span>Guest</span>
          <span>Interviewer</span>
        </div>
      </div>
    );
  }

  return (
    <div className="preview-composition cinematic-preview">
      <span>Memory object insert</span>
      <h3>{meta.previewHeadline}</h3>
      <p>{meta.previewSubhead}</p>
      <div className="cinematic-subtitle">emotional subtitle lane</div>
    </div>
  );
}
