import { useEffect, useMemo, useState } from "react";
import { randomId, submitOperatorUiCommand, testOperatorApi } from "./api/operatorRuntime.js";
import {
  agents,
  assets,
  compositionTemplates,
  contentFormats,
  evalReceipts,
  guests,
  interviewBrief,
  navItems,
  pipelineStages,
  stillVisualMockupBoards,
} from "./data.js";
import { VideoTimelineWorkbench } from "./screens/VideoTimelineWorkbench.jsx";
import { OperationsCommandCenter } from "./screens/OperationsCommandCenter.jsx";
import { SuperVisualStudio } from "./screens/SuperVisualStudio.jsx";
import { ClientWorkspaceReferencePanel } from "./components/workspace/ClientWorkspaceReferencePanel.jsx";
import {
  getGoldenPathRunDetail,
  getPipelineRunMonitor,
  listPipelineRuns,
} from "./api/pipelineRunMonitor.js";

const statusLabels = {
  current: "Current",
  attention: "Needs Review",
  waiting: "Waiting",
  blocked: "Blocked",
  ready: "Ready",
  "needs rig": "Needs Rig",
  passed: "Passed",
  revision: "Revision",
};

function cx(...names) {
  return names.filter(Boolean).join(" ");
}

function StatusPill({ status }) {
  const key = String(status || "").toLowerCase();
  return <span className={cx("status-pill", key.replaceAll(" ", "-"))}>{statusLabels[key] || status}</span>;
}

function ProgressRing({ value, label }) {
  const angle = Math.max(0, Math.min(100, value)) * 3.6;
  return (
    <div className="progress-ring" style={{ "--angle": `${angle}deg` }}>
      <div>
        <strong>{value}</strong>
        <span>{label}</span>
      </div>
    </div>
  );
}

function AppShell({ activeView, onViewChange, children, activeGuest, onGuestChange, onNewInterviewBrief }) {
  return (
    <div className="app-shell">
      <aside className="sidebar" aria-label="Main navigation">
        <div className="brand-mark">
          <div className="brand-c">C</div>
          <div>
            <strong>CONSCIOUS ELITE</strong>
            <span>CMF Studio</span>
          </div>
        </div>
        <nav className="nav-list">
          {navItems.map((item) => (
            <button
              className={cx("nav-item", activeView === item.id && "active")}
              key={item.id}
              type="button"
              onClick={() => onViewChange(item.id)}
              aria-current={activeView === item.id ? "page" : undefined}
            >
              <span>{item.code}</span>
              {item.label}
            </button>
          ))}
        </nav>
        <div className="sidebar-footer">
          <span>Contract</span>
          <strong>cmf-ui-contracts.2026-06-22</strong>
        </div>
      </aside>
      <div className="workspace">
        <header className="topbar">
          <div>
            <span className="eyebrow">Operator Cockpit</span>
            <h1>{navItems.find((item) => item.id === activeView)?.label}</h1>
          </div>
          <div className="topbar-controls">
            <label className="select-label">
              Brand Workspace
              <select value={activeGuest.id} onChange={(event) => onGuestChange(event.target.value)}>
                {guests.map((guest) => (
                  <option key={guest.id} value={guest.id}>
                    {guest.workspace} - {guest.name}
                  </option>
                ))}
              </select>
            </label>
            <button type="button" className="ghost-button" onClick={() => onViewChange("ops")}>
              Command Log
            </button>
            <button type="button" className="primary-button" onClick={onNewInterviewBrief}>
              New Interview Brief
            </button>
          </div>
        </header>
        {children}
      </div>
    </div>
  );
}

function ControlTower({ activeGuest, setView, onGenerateBrief, onRunPipelineCommand }) {
  const blockedCount = pipelineStages.filter((stage) => stage.status === "blocked").length;
  const reviewCount = assets.filter((asset) => asset.state === "Review" || asset.state === "Blocked").length;
  return (
    <main className="screen control-grid">
      <section className="hero-panel">
        <div className="hero-copy">
          <span className="eyebrow amber">Interview-first production</span>
          <h2>Monthly Interview Brief is the first artifact.</h2>
          <p>
            The operator starts with brand context, CRAL research, Context Premises, Voice DNA, Emotional DNA, and
            primitive proof before the team generates content. Existing transcript and video ingestion is only the
            fallback when no new interview will be conducted.
          </p>
          <div className="hero-actions">
            <button type="button" className="primary-button" onClick={onGenerateBrief}>
              Create Interview Brief
            </button>
            <button type="button" className="ghost-button" onClick={() => onRunPipelineCommand("run_cral_context_research", "CRAL context research requested")}>
              Run CRAL
            </button>
            <button type="button" className="ghost-button" onClick={() => setView("ops")}>
              Open Command Center
            </button>
          </div>
        </div>
        <div className="hero-metrics">
          <ProgressRing value={activeGuest.primitiveScore} label="Primitive Fit" />
          <div className="metric-card">
            <span>Active Guest</span>
            <strong>{activeGuest.name}</strong>
            <p>{activeGuest.status}</p>
          </div>
          <div className="metric-card warning">
            <span>Approval Blockers</span>
            <strong>{blockedCount + activeGuest.openBlockers}</strong>
            <p>{activeGuest.nextAction}</p>
          </div>
        </div>
      </section>

      <section className="panel span-2">
        <PanelHeader kicker="Pipeline" title="Factory State" action="View all stages" onAction={() => setView("pipeline")} />
        <div className="pipeline-strip">
          {pipelineStages.map((stage) => (
            <button key={stage.id} type="button" className={cx("stage-node", stage.status)} onClick={() => setView("pipeline")}>
              <span>{stage.count}</span>
              <strong>{stage.label}</strong>
              <small>{stage.owner}</small>
            </button>
          ))}
        </div>
      </section>

      <section className="panel">
        <PanelHeader kicker="Guests" title="Workspace Health" action="Manage guests" onAction={() => setView("guests")} />
        <div className="guest-stack">
          {guests.map((guest) => (
            <div className={cx("guest-mini", guest.id === activeGuest.id && "selected")} key={guest.id}>
              <div>
                <strong>{guest.name}</strong>
                <span>{guest.workspace}</span>
              </div>
              <StatusPill status={guest.openBlockers ? "attention" : "ready"} />
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <PanelHeader kicker="Review" title="Assets Needing Judgment" action="Open review" onAction={() => setView("review")} />
        <div className="asset-list compact">
          {assets.slice(0, 3).map((asset) => (
            <AssetRow asset={asset} key={asset.code} />
          ))}
        </div>
      </section>

      <section className="panel">
        <PanelHeader kicker="Queues" title="Production Load" />
        <div className="queue-grid">
          <Metric label="Interview briefs" value="2" tone="amber" />
          <Metric label="Render jobs" value="3" tone="cyan" />
          <Metric label="Eval receipts" value="4" tone="green" />
          <Metric label="Hard blockers" value={String(reviewCount - 1)} tone="red" />
        </div>
      </section>
    </main>
  );
}

function GuestWorkspace({ activeGuest, onUpdateGuest, onRunPipelineCommand }) {
  const [draft, setDraft] = useState(activeGuest);
  const setField = (field, value) => setDraft((current) => ({ ...current, [field]: value }));

  return (
    <main className="screen two-column">
      <section className="panel large">
        <PanelHeader kicker="Guest Workspace" title={activeGuest.name} />
        <div className="guest-profile">
          <div className="avatar">{activeGuest.code.slice(0, 2)}</div>
          <div>
            <h2>{activeGuest.name}</h2>
            <span>{activeGuest.handle}</span>
            <p>{activeGuest.pack}</p>
          </div>
          <StatusPill status={activeGuest.openBlockers ? "attention" : "ready"} />
        </div>
        <div className="detail-grid">
          <InfoCard title="Workspace Code" value={activeGuest.workspace} />
          <InfoCard title="Consent State" value={activeGuest.consent} />
          <InfoCard title="Voice DNA" value={activeGuest.voiceDna} />
          <InfoCard title="Emotional DNA" value={activeGuest.emotionalDna} />
        </div>
      </section>
      <section className="panel">
        <PanelHeader kicker="Brand Data" title="Editable Context" />
        <div className="brand-form">
          <label>
            Display name
            <input value={draft.name} onChange={(event) => setField("name", event.target.value)} />
          </label>
          <label>
            Handle
            <input value={draft.handle} onChange={(event) => setField("handle", event.target.value)} />
          </label>
          <label>
            Voice DNA
            <textarea value={draft.voiceDna} onChange={(event) => setField("voiceDna", event.target.value)} />
          </label>
          <label>
            Emotional DNA
            <textarea value={draft.emotionalDna} onChange={(event) => setField("emotionalDna", event.target.value)} />
          </label>
          <div className="form-actions">
            <button type="button" className="primary-button" onClick={() => onUpdateGuest(draft)}>
              Save Brand Data
            </button>
            <button type="button" className="ghost-button" onClick={() => onRunPipelineCommand("run_brand_context_gate", "Brand context gate requested")}>
              Run Context Gate
            </button>
          </div>
        </div>
      </section>
      <section className="panel">
        <PanelHeader kicker="Scope" title="Operator Safety" />
        <div className="checklist">
          <CheckRow label="Only approved offers shown" good detail="$99/month and $29/week only" />
          <CheckRow label="Newsletter format forbidden" good detail="Registry gate active" />
          <CheckRow label="Guest scope isolated" good detail="Workspace and codes visible" />
          <CheckRow label="Approval requires receipts" good={activeGuest.openBlockers === 0} detail={activeGuest.nextAction} />
        </div>
      </section>
      <section className="panel span-2">
        <PanelHeader kicker="Content Assets" title="Guest Asset Ledger" />
        <div className="asset-list">
          {assets
            .filter((asset) => asset.owner === activeGuest.name || activeGuest.id === "claude")
            .map((asset) => (
              <AssetRow asset={asset} key={asset.code} />
            ))}
        </div>
      </section>
      <ClientWorkspaceReferencePanel activeGuest={activeGuest} />
    </main>
  );
}

function InterviewBrief({ activeGuest, briefState, onGenerateBrief, onRunPipelineCommand }) {
  const [selectedMove, setSelectedMove] = useState(briefState.moves[0]);
  const selectedMoveIsCurrent = briefState.moves.some((move) => move.id === selectedMove.id);
  const activeMove = selectedMoveIsCurrent ? selectedMove : briefState.moves[0];
  return (
    <main className="screen brief-layout">
      <section className="panel large brief-main">
        <PanelHeader kicker={briefState.id} title={briefState.title} action="Create / Refresh" onAction={onGenerateBrief} />
        <p className="lead">{briefState.objective}</p>
        <div className="brief-command-strip">
          <button type="button" className="primary-button" onClick={onGenerateBrief}>
            Generate Monthly Brief
          </button>
          <button type="button" className="ghost-button" onClick={() => onRunPipelineCommand("compile_interview_brief_skill", "JIT Interview Skill compile requested")}>
            Compile JIT Skill
          </button>
          <button type="button" className="ghost-button" onClick={() => onRunPipelineCommand("run_matrix_of_edging", "Matrix of Edging route requested")}>
            Score Matrix
          </button>
        </div>
        <div className="brief-status-line">
          <span>Guest</span>
          <strong>{activeGuest.name}</strong>
          <span>{briefState.status}</span>
        </div>
        <div className="context-list">
          {briefState.contextPremises.map((premise) => (
            <div className="context-card" key={premise}>
              <span>Context Premise</span>
              <strong>{premise}</strong>
            </div>
          ))}
        </div>
        <div className="move-timeline">
          {briefState.moves.map((move) => (
            <button
              key={move.id}
              type="button"
              className={cx("move-card", activeMove.id === move.id && "active")}
              onClick={() => setSelectedMove(move)}
            >
              <span>{move.id}</span>
              <strong>{move.label}</strong>
              <small>{move.score}% fit</small>
            </button>
          ))}
        </div>
      </section>
      <section className="panel brief-inspector">
        <PanelHeader kicker="Selected Move" title={activeMove.label} />
        <div className="question-card">
          <span>Interview Question</span>
          <h2>{activeMove.question}</h2>
        </div>
        <InfoCard title="Target Extraction" value={activeMove.target} />
        <InfoCard title="Evidence" value={activeMove.evidence} />
        <div className="doctrine-row">
          {briefState.doctrines.map((doctrine) => (
            <span key={doctrine}>{doctrine}</span>
          ))}
        </div>
      </section>
    </main>
  );
}

function PipelineView({ onView }) {
  const [filter, setFilter] = useState("all");
  const [pipelineRuns, setPipelineRuns] = useState([]);
  const [selectedRunId, setSelectedRunId] = useState("");
  const [monitor, setMonitor] = useState(null);
  const [goldenPathDetail, setGoldenPathDetail] = useState(null);
  const [monitorStatus, setMonitorStatus] = useState("loading");
  const visible = filter === "all" ? pipelineStages : pipelineStages.filter((stage) => stage.status === filter);

  useEffect(() => {
    let cancelled = false;
    async function loadRuns() {
      setMonitorStatus("loading");
      const runs = await listPipelineRuns();
      if (cancelled) return;
      setPipelineRuns(runs);
      setSelectedRunId((current) => current || runs[0]?.pipeline_run_id || "");
      setMonitorStatus(runs.length ? "ready" : "empty");
    }
    loadRuns();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!selectedRunId) return undefined;
    let cancelled = false;
    async function loadMonitor() {
      setMonitorStatus("loading");
      const nextMonitor = await getPipelineRunMonitor(selectedRunId);
      if (cancelled) return;
      setMonitor(nextMonitor);
      setMonitorStatus("ready");
      if (nextMonitor?.run_status?.golden_path_run_id) {
        const detail = await getGoldenPathRunDetail(nextMonitor.run_status.golden_path_run_id);
        if (!cancelled) setGoldenPathDetail(detail);
      } else {
        setGoldenPathDetail(null);
      }
    }
    loadMonitor();
    return () => {
      cancelled = true;
    };
  }, [selectedRunId]);

  return (
    <main className="screen">
      <section className="panel">
        <PanelHeader kicker="Factory Map" title="End-to-End Production Pipeline" />
        <div className="segmented">
          {["all", "current", "attention", "waiting", "blocked"].map((item) => (
            <button key={item} type="button" className={filter === item ? "active" : ""} onClick={() => setFilter(item)}>
              {item}
            </button>
          ))}
        </div>
        <div className="stage-grid">
          {visible.map((stage) => (
            <article className={cx("stage-card", stage.status)} key={stage.id}>
              <div>
                <StatusPill status={stage.status} />
                <strong>{stage.label}</strong>
                <span>{stage.owner}</span>
              </div>
              <p>{stage.detail}</p>
            </article>
          ))}
        </div>
      </section>
      <section className="panel pipeline-monitor-panel">
        <PanelHeader
          kicker="Run Monitor"
          title="Pipeline Runs, Receipts, Artifacts, Approvals"
        />
        <div className="pipeline-monitor-layout">
          <div className="pipeline-run-list">
            {pipelineRuns.length === 0 && <p className="muted-copy">No pipeline run read model is available yet.</p>}
            {pipelineRuns.map((run) => (
              <button
                key={run.pipeline_run_id}
                type="button"
                className={cx("pipeline-run-button", selectedRunId === run.pipeline_run_id && "active")}
                onClick={() => setSelectedRunId(run.pipeline_run_id)}
              >
                <div>
                  <strong>{run.recipe_id}</strong>
                  <span>{run.pipeline_run_id}</span>
                </div>
                <StatusPill status={run.status} />
                <small>{run.progress_percent}% / {run.current_step_id || "waiting"}</small>
                <small>{run.blocker_count} blockers / {run.pending_approval_count} approvals</small>
              </button>
            ))}
          </div>
          <div className="pipeline-monitor-detail">
            {monitorStatus === "loading" && <p className="muted-copy">Loading pipeline monitor read model...</p>}
            {monitor && (
              <>
                <PipelineRunSummaryPanel monitor={monitor} />
                <PipelineStageReceiptPanel receipts={monitor.stage_receipts} />
                <div className="pipeline-monitor-subgrid">
                  <PipelineArtifactPanel artifacts={monitor.artifacts} />
                  <PipelineApprovalPanel approvals={monitor.approvals} blockers={monitor.blockers} />
                </div>
                <PipelineSceneOutputPanel links={monitor.scene_output_links} onView={onView} />
                {goldenPathDetail && <GoldenPathDetailPanel detail={goldenPathDetail} />}
              </>
            )}
          </div>
        </div>
      </section>
    </main>
  );
}

function PipelineRunSummaryPanel({ monitor }) {
  const run = monitor.run_status;
  return (
    <div className="pipeline-run-summary">
      <div>
        <span className="eyebrow">Active Run</span>
        <h3>{run.recipe_id}</h3>
        <p>{run.pipeline_run_id}</p>
      </div>
      <div className="pipeline-run-summary-metrics">
        <InfoCard title="Status" value={run.status} />
        <InfoCard title="Progress" value={`${run.progress_percent}%`} />
        <InfoCard title="Current Step" value={run.current_step_id || "waiting"} />
        <InfoCard title="Source" value={run.source_mode} />
      </div>
    </div>
  );
}

function PipelineStageReceiptPanel({ receipts }) {
  return (
    <section className="pipeline-section">
      <h3>Stage Receipts</h3>
      <div className="pipeline-stage-receipt-list">
        {receipts.map((receipt) => (
          <article className="pipeline-stage-receipt" key={receipt.step_id}>
            <div>
              <strong>{receipt.step_name}</strong>
              <span>{receipt.receipt_id}</span>
            </div>
            <StatusPill status={receipt.status} />
            <StatusPill status={receipt.pass_status} />
            <small>{receipt.message}</small>
          </article>
        ))}
      </div>
    </section>
  );
}

function PipelineArtifactPanel({ artifacts }) {
  return (
    <section className="pipeline-section">
      <h3>Artifacts</h3>
      <div className="pipeline-compact-list">
        {artifacts.map((artifact) => (
          <article className="pipeline-compact-row" key={artifact.artifact_id}>
            <div>
              <strong>{artifact.role}</strong>
              <span>{artifact.uri}</span>
            </div>
            {artifact.linked_preview_url ? (
              <a href={artifact.linked_preview_url}>Open preview</a>
            ) : (
              <small>Pointer only</small>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}

function PipelineApprovalPanel({ approvals, blockers }) {
  return (
    <section className="pipeline-section">
      <h3>Approvals + Blockers</h3>
      <div className="pipeline-compact-list">
        {approvals.map((approval) => (
          <article className="pipeline-compact-row" key={approval.gate_id}>
            <div>
              <strong>{approval.gate_id}</strong>
              <span>{approval.pending_reason || approval.gate_type}</span>
            </div>
            <StatusPill status={approval.status} />
          </article>
        ))}
        {blockers.map((blocker) => (
          <article className="pipeline-blocker-row" key={blocker.blocker_id}>
            <strong>{blocker.code}</strong>
            <span>{blocker.message}</span>
          </article>
        ))}
      </div>
    </section>
  );
}

function PipelineSceneOutputPanel({ links, onView }) {
  return (
    <section className="pipeline-section">
      <h3>Scene Output Links</h3>
      <div className="scene-output-link-grid">
        {links.map((link) => (
          <article className="scene-output-link-card" key={`${link.scene_id}-${link.step_id}`}>
            <div>
              <strong>{link.scene_id}</strong>
              <span>{link.step_id}</span>
            </div>
            <div className="scene-output-actions">
              {link.template_preview_url ? <a href={link.template_preview_url}>Template preview</a> : <small>Template unavailable</small>}
              {link.video_preview_url ? (
                <button type="button" className="small-button" onClick={() => onView("timeline")}>
                  Video preview
                </button>
              ) : (
                <small>Video unavailable</small>
              )}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

function GoldenPathDetailPanel({ detail }) {
  const sections = [
    ["Source", detail.input_fixture_refs],
    ["Narrative", detail.narrative_outputs],
    ["Format", detail.format_outputs],
    ["Composition", detail.composition_scene_outputs],
    ["Avatar", detail.avatar_outputs],
    ["Timeline", detail.timeline_outputs],
    ["Render", detail.render_outputs],
    ["Approval", detail.approval_outputs],
  ];
  return (
    <section className="pipeline-section golden-path-detail">
      <div className="panel-header compact">
        <div>
          <span className="eyebrow amber">Golden Path Detail</span>
          <h3>{detail.golden_path_run_id}</h3>
        </div>
        <StatusPill status={detail.source_mode} />
      </div>
      <div className="golden-path-section-grid">
        {sections.map(([label, items]) => (
          <article className="golden-path-section" key={label}>
            <strong>{label}</strong>
            <pre>{JSON.stringify(items, null, 2)}</pre>
          </article>
        ))}
      </div>
    </section>
  );
}

function CompositionStudio() {
  const [selected, setSelected] = useState(compositionTemplates[0]);
  const [tab, setTab] = useState("json");
  return (
    <main className="screen composition-layout">
      <section className="panel preview-panel">
        <PanelHeader kicker={selected.format} title={selected.title} />
        <CompositionPreview template={selected} />
      </section>
      <section className="panel large">
        <PanelHeader kicker="Composition Truth" title="Template Runtime" />
        <div className="template-list">
          {compositionTemplates.map((template) => (
            <button
              className={cx("template-row", selected.id === template.id && "active")}
              key={template.id}
              type="button"
              onClick={() => setSelected(template)}
            >
              <div>
                <strong>{template.title}</strong>
                <span>{template.id} / {template.engine}</span>
              </div>
              <StatusPill status={template.status} />
            </button>
          ))}
        </div>
        <div className="tabbar">
          {["json", "layers", "timing", "eval"].map((item) => (
            <button key={item} type="button" className={tab === item ? "active" : ""} onClick={() => setTab(item)}>
              {item}
            </button>
          ))}
        </div>
        <CompositionInspector selected={selected} tab={tab} />
      </section>
      <section className="panel span-2">
        <PanelHeader kicker="Still Visuals" title="Carousel and SuperVisual Composition Boards" />
        <div className="still-board-grid">
          {stillVisualMockupBoards.map((board) => (
            <article className="still-board-card" key={board.id}>
              <div className="still-board-copy">
                <span className="eyebrow amber">{board.family}</span>
                <h3>{board.title}</h3>
                <p>{board.count} / {board.status}</p>
                <div className="format-chip-row">
                  {board.formats.map((format) => (
                    <span key={format}>{format}</span>
                  ))}
                </div>
                <InfoCard title="Primitive Policy" value={board.primitivePolicy} />
                <InfoCard title="Manifest" value={board.manifest} />
                <InfoCard title="Source Registry" value={board.sourceRegistry} />
              </div>
              <img src={board.preview} alt={`${board.title} contact sheet`} />
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

function CompositionPreview({ template }) {
  const isPaper = template.format === "SV-EDU";
  const isReaction = template.format === "SV-RRC" || template.format === "SV-FRB";
  return (
    <div className={cx("phone-preview", isPaper && "paper", isReaction && "reaction")}>
      <div className="preview-top">
        <span>{template.format}</span>
        <strong>{template.title}</strong>
      </div>
      {isReaction ? (
        <>
          <div className="reaction-ui">
            <h3>Silence: survival or betrayal?</h3>
            <div className="poll-bars">
              <span style={{ "--w": "62%" }}>Survival</span>
              <span style={{ "--w": "38%" }}>Betrayal</span>
            </div>
          </div>
          <div className="human-zone">
            <div className="person">Guest</div>
            <div className="person interviewer">Interviewer</div>
          </div>
        </>
      ) : isPaper ? (
        <>
          <div className="paper-note pink">MYTH 1</div>
          <div className="paper-note big">Natural = always safe?</div>
          <div className="paper-diagram">
            <span>Claim</span>
            <span>Evidence</span>
            <span>Truth</span>
          </div>
          <div className="paper-avatar">Avatar rig</div>
        </>
      ) : (
        <>
          <div className="cinema-frame">
            <span>Memory object</span>
          </div>
          <h3>"I entered as a friend and left as a suspect."</h3>
          <div className="subtitle">emotional subtitle lane</div>
        </>
      )}
    </div>
  );
}

function CompositionInspector({ selected, tab }) {
  if (tab === "layers") {
    return (
      <div className="layer-stack">
        {selected.json.layers.map((layer, index) => (
          <div className="layer-item" key={layer}>
            <span>{String(index + 1).padStart(2, "0")}</span>
            <strong>{layer}</strong>
          </div>
        ))}
      </div>
    );
  }
  if (tab === "timing") {
    return (
      <div className="inspector-block">
        <InfoCard title="Timing Source" value={selected.json.timing_source} />
        <InfoCard title="Timing Rule" value={selected.timing} />
      </div>
    );
  }
  if (tab === "eval") {
    return (
      <div className="doctrine-row tall">
        {selected.primitiveProof.map((proof) => (
          <span key={proof}>{proof}</span>
        ))}
      </div>
    );
  }
  return <pre className="json-view">{JSON.stringify(selected.json, null, 2)}</pre>;
}

function ReviewWorkbench() {
  const [selected, setSelected] = useState(assets[1]);
  const [decision, setDecision] = useState("pending");
  const receipt = evalReceipts.find((item) => item.target === selected.code) || evalReceipts[0];
  const hasBlocker = selected.blockers > 0 || receipt.status === "blocked";
  return (
    <main className="screen review-layout">
      <section className="panel">
        <PanelHeader kicker="Queue" title="Review Objects" />
        <div className="asset-list">
          {assets.map((asset) => (
            <button
              type="button"
              className={cx("asset-button", selected.code === asset.code && "active")}
              onClick={() => {
                setSelected(asset);
                setDecision("pending");
              }}
              key={asset.code}
            >
              <AssetRow asset={asset} />
            </button>
          ))}
        </div>
      </section>
      <section className="panel large">
        <PanelHeader kicker={selected.format} title={selected.title} />
        <div className="review-surface">
          <CompositionPreview template={compositionTemplates.find((item) => item.format === selected.format) || compositionTemplates[0]} />
          <div className="evidence-panel">
            <InfoCard title="Content Asset Code" value={selected.code} />
            <InfoCard title="Source Range" value={selected.source} />
            <InfoCard title="Evaluation Receipt" value={`${receipt.id} / ${receipt.status} / ${receipt.score}`} />
            <div className="checklist">
              {receipt.gates.map((gate) => (
                <CheckRow key={gate} label={gate} good={!hasBlocker || gate !== "Source Truth"} detail="Registry-backed check" />
              ))}
            </div>
            <p className="receipt-note">{receipt.note}</p>
            <div className="review-actions">
              <button type="button" className="danger-button" onClick={() => setDecision("rejected")}>
                Reject
              </button>
              <button type="button" className="ghost-button" onClick={() => setDecision("revision requested")}>
                Request Revision
              </button>
              <button type="button" className="primary-button" disabled={hasBlocker} onClick={() => setDecision("approved")}>
                Approve
              </button>
            </div>
            <div className={cx("decision-banner", decision !== "pending" && "visible")}>Decision: {decision}</div>
          </div>
        </div>
      </section>
    </main>
  );
}

function AgentFactory() {
  return (
    <main className="screen">
      <section className="panel">
        <PanelHeader kicker="Runtime Team" title="Agent Factory" />
        <div className="agent-grid">
          {agents.map((agent) => (
            <article className="agent-card" key={agent.code}>
              <div>
                <span>{agent.code}</span>
                <StatusPill status={agent.state === "active" ? "current" : "attention"} />
              </div>
              <h3>{agent.name}</h3>
              <p>{agent.responsibility}</p>
              <div className="tool-row">
                {agent.tools.map((tool) => (
                  <span key={tool}>{tool}</span>
                ))}
              </div>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

function EvalsView() {
  return (
    <main className="screen two-column">
      <section className="panel large">
        <PanelHeader kicker="Evaluation Receipts" title="Doctrine and Primitive Gates" />
        <div className="receipt-list">
          {evalReceipts.map((receipt) => (
            <article className="receipt-card" key={receipt.id}>
              <div>
                <strong>{receipt.id}</strong>
                <StatusPill status={receipt.status} />
              </div>
              <span>{receipt.target}</span>
              <p>{receipt.note}</p>
              <div className="doctrine-row">
                {receipt.gates.map((gate) => (
                  <span key={gate}>{gate}</span>
                ))}
              </div>
            </article>
          ))}
        </div>
      </section>
      <section className="panel">
        <PanelHeader kicker="Targets" title="Eval Registry" />
        <div className="checklist">
          <CheckRow label="Source truth blocker" good detail="Required before approval" />
          <CheckRow label="Primitive minimum" good detail="At least 3 primitives per composition" />
          <CheckRow label="Composition JSON hash" good detail="Required for reproducibility" />
          <CheckRow label="Operator approval" good detail="No self-approval by generating agent" />
        </div>
      </section>
    </main>
  );
}

function FormatsPanel() {
  return (
    <div className="format-grid">
      {contentFormats.map((format) => (
        <article className="format-card" key={format.code}>
          <span>{format.code} / {format.family}</span>
          <h3>{format.name}</h3>
          <p>{format.role}</p>
          <small>{format.visual}</small>
        </article>
      ))}
    </div>
  );
}

function PanelHeader({ kicker, title, action, onAction }) {
  return (
    <div className="panel-header">
      <div>
        {kicker && <span className="eyebrow">{kicker}</span>}
        <h2>{title}</h2>
      </div>
      {action && (
        <button type="button" className="small-button" onClick={onAction}>
          {action}
        </button>
      )}
    </div>
  );
}

function Metric({ label, value, tone }) {
  return (
    <div className={cx("metric", tone)}>
      <strong>{value}</strong>
      <span>{label}</span>
    </div>
  );
}

function InfoCard({ title, value }) {
  return (
    <div className="info-card">
      <span>{title}</span>
      <strong>{value}</strong>
    </div>
  );
}

function CheckRow({ label, good = true, detail }) {
  return (
    <div className={cx("check-row", good ? "good" : "bad")}>
      <span>{good ? "OK" : "FIX"}</span>
      <div>
        <strong>{label}</strong>
        <small>{detail}</small>
      </div>
    </div>
  );
}

function AssetRow({ asset }) {
  return (
    <div className="asset-row">
      <div>
        <strong>{asset.title}</strong>
        <span>{asset.code}</span>
      </div>
      <div className="asset-meta">
        <span>{asset.eval}</span>
        <StatusPill status={asset.blockers ? "blocked" : asset.state.toLowerCase()} />
      </div>
    </div>
  );
}

function createInitialRuntime() {
  return {
    apiStatus: {
      state: "untested",
      detail: "Click Test CMF API to check /api/v1/operator-ui/content-formats",
    },
    harnessStatus: {
      state: "offline",
      detail: "Pi harness is represented as command receipts until a live runner is connected.",
    },
    commandReceipts: [],
    agentRuns: [],
    outputs: [],
  };
}

function buildGeneratedBrief(activeGuest) {
  const today = new Date().toISOString().slice(0, 10);
  return {
    ...interviewBrief,
    id: `IBF-${today}-${activeGuest.code}`,
    guest: activeGuest.name,
    status: "Generated by operator command",
    objective: `Prepare a monthly interview path for ${activeGuest.name} that extracts identity-specific stories, teaching frames, human recognition moments, and reaction-ready tensions without flattening the guest into generic content.`,
    contextPremises: [
      `${activeGuest.name}'s audience needs a question path grounded in ${activeGuest.voiceDna}.`,
      `The interview should surface ${activeGuest.emotionalDna} as lived evidence, not as a slogan.`,
      `${activeGuest.nextAction} must be converted into a question, extraction target, and approval gate.`,
    ],
    moves: interviewBrief.moves.map((move, index) => ({
      ...move,
      id: `M${String(index + 1).padStart(2, "0")}`,
      evidence: `${move.evidence}; generated from ${activeGuest.workspace} brand workspace state.`,
    })),
  };
}

function commandToAgentRun(receipt, label) {
  const agentCodeMap = {
    update_brand_workspace_context: "BRD-GENESIS-AG",
    generate_monthly_interview_brief: "INT-BRIEF-AG",
    run_cral_context_research: "RES-CRAL-AG",
    compile_interview_brief_skill: "INT-BRIEF-AG",
    run_matrix_of_edging: "RTE-ASSET-AG",
    run_render_job: "RND-VIDEO-AG",
    operator_chat_command: "PI-HARNESS-AG",
  };
  return {
    run_id: randomId("run"),
    receipt_id: receipt.receipt_id,
    command_id: receipt.command_id,
    agent_code: agentCodeMap[receipt.command_type] || "PI-HARNESS-AG",
    status: receipt.runtime_mode === "cmf-api" ? "accepted by CMF API" : "captured in offline ledger",
    goal: label,
    created_at: receipt.created_at,
  };
}

function renderOutputFromReceipt(receipt, activeGuest) {
  return {
    output_id: randomId("render-output"),
    receipt_id: receipt.receipt_id,
    label: `${activeGuest.code} active reaction clip`,
    status: receipt.runtime_mode === "cmf-api" ? "queued" : "manifest-only",
    output_ref: `render://${activeGuest.workspace}/${receipt.command_id}/active-clip.mp4`,
    created_at: receipt.created_at,
  };
}

export function App() {
  const [activeView, setActiveView] = useState("control");
  const [guestRecords, setGuestRecords] = useState(guests);
  const [guestId, setGuestId] = useState(guests[0].id);
  const [briefState, setBriefState] = useState(interviewBrief);
  const [runtime, setRuntime] = useState(createInitialRuntime);
  const [commandText, setCommandText] = useState("");
  const activeGuest = useMemo(() => guestRecords.find((guest) => guest.id === guestId) || guestRecords[0], [guestId, guestRecords]);

  async function runCommand({ commandType, label, payload = {}, sourceRoute = activeView, contentAssetCode, activeObjectType }) {
    const receipt = await submitOperatorUiCommand({
      commandType,
      commandPayload: {
        ...payload,
        label,
        source_route: sourceRoute,
      },
      activeGuest,
      sourceRoute,
      contentAssetCode,
      activeObjectType,
    });
    setRuntime((current) => ({
      ...current,
      commandReceipts: [receipt, ...current.commandReceipts].slice(0, 30),
      agentRuns: [commandToAgentRun(receipt, label), ...current.agentRuns].slice(0, 16),
      harnessStatus: {
        state: receipt.runtime_mode === "cmf-api" ? "connected" : "offline",
        detail:
          receipt.runtime_mode === "cmf-api"
            ? "Last command was accepted by the CMF operator API."
            : "Last command is stored in the local UI ledger; backend runner is not connected.",
      },
    }));
    return receipt;
  }

  async function handleGenerateBrief() {
    const generated = buildGeneratedBrief(activeGuest);
    const receipt = await runCommand({
      commandType: "generate_monthly_interview_brief",
      label: `Generate monthly Interview Brief for ${activeGuest.name}`,
      payload: {
        brief_id: generated.id,
        context_premises: generated.contextPremises,
        doctrine_gates: generated.doctrines,
        guest_workspace: activeGuest.workspace,
      },
      sourceRoute: "interview-brief",
      activeObjectType: "interview_brief",
    });
    setBriefState({ ...generated, status: `Command ${receipt.status}: ${receipt.runtime_mode}` });
    setActiveView("brief");
  }

  async function handleUpdateGuest(updatedGuest) {
    setGuestRecords((current) => current.map((guest) => (guest.id === updatedGuest.id ? updatedGuest : guest)));
    await runCommand({
      commandType: "update_brand_workspace_context",
      label: `Update Brand Workspace for ${updatedGuest.name}`,
      payload: {
        guest_name: updatedGuest.name,
        handle: updatedGuest.handle,
        voice_dna: updatedGuest.voiceDna,
        emotional_dna: updatedGuest.emotionalDna,
        workspace_code: updatedGuest.workspace,
      },
      sourceRoute: "guest-workspace",
    });
  }

  async function handleRunPipelineCommand(commandType, label) {
    await runCommand({
      commandType,
      label: `${label} for ${activeGuest.name}`,
      payload: {
        guest_workspace: activeGuest.workspace,
        required_primitives: ["Source Truth", "Human Dignity", "Primitive Proof"],
      },
      sourceRoute: "operations",
    });
    setActiveView("ops");
  }

  async function handleStartRender() {
    const receipt = await runCommand({
      commandType: "run_render_job",
      label: `Render active clip for ${activeGuest.name}`,
      payload: {
        render_target: "active_video_edit_program",
        deterministic_runtime: ["Remotion", "FFmpeg", "renderer_props_hash"],
        provider_state: "requires live renderer worker for final mp4",
      },
      sourceRoute: "timeline",
      contentAssetCode: assets.find((asset) => asset.owner === activeGuest.name)?.code,
      activeObjectType: "video_edit_program",
    });
    setRuntime((current) => ({
      ...current,
      outputs: [renderOutputFromReceipt(receipt, activeGuest), ...current.outputs].slice(0, 12),
    }));
    setActiveView("ops");
  }

  async function handleSubmitCommandText() {
    const text = commandText.trim();
    if (!text) return;
    const lowered = text.toLowerCase();
    let commandType = "operator_chat_command";
    if (lowered.includes("brief") || lowered.includes("interview")) commandType = "generate_monthly_interview_brief";
    if (lowered.includes("render") || lowered.includes("export")) commandType = "run_render_job";
    if (lowered.includes("repair") || lowered.includes("fix")) commandType = "request_revision_repair";
    if (lowered.includes("cral") || lowered.includes("research")) commandType = "run_cral_context_research";
    await runCommand({
      commandType,
      label: text,
      payload: {
        operator_message: text,
        routed_from: "chat_command_console",
      },
      sourceRoute: "operations-command-console",
    });
    setCommandText("");
  }

  async function handleTestApi() {
    const apiStatus = await testOperatorApi();
    setRuntime((current) => ({ ...current, apiStatus }));
  }

  function handleTimelineReceipt(receipt, label = "Timeline edit command submitted") {
    const normalized = {
      ...receipt,
      command_type: receipt.command_type || receipt.edit_type || "submit_timeline_edit",
      runtime_mode: receipt.runtime_mode || "timeline-workbench",
      created_at: receipt.created_at || new Date().toISOString(),
      payload: receipt.payload || {},
    };
    setRuntime((current) => ({
      ...current,
      commandReceipts: [normalized, ...current.commandReceipts].slice(0, 30),
      agentRuns: [commandToAgentRun(normalized, label), ...current.agentRuns].slice(0, 16),
    }));
  }

  let content = null;
  if (activeView === "control") content = <ControlTower activeGuest={activeGuest} setView={setActiveView} onGenerateBrief={handleGenerateBrief} onRunPipelineCommand={handleRunPipelineCommand} />;
  if (activeView === "ops") content = (
    <OperationsCommandCenter
      activeGuest={activeGuest}
      runtime={runtime}
      commandText={commandText}
      setCommandText={setCommandText}
      onSubmitCommandText={handleSubmitCommandText}
      onGenerateBrief={handleGenerateBrief}
      onRunPipelineCommand={handleRunPipelineCommand}
      onStartRender={handleStartRender}
      onTestApi={handleTestApi}
      onView={setActiveView}
    />
  );
  if (activeView === "guests") content = <GuestWorkspace key={activeGuest.id} activeGuest={activeGuest} onUpdateGuest={handleUpdateGuest} onRunPipelineCommand={handleRunPipelineCommand} />;
  if (activeView === "brief") content = <InterviewBrief activeGuest={activeGuest} briefState={briefState} onGenerateBrief={handleGenerateBrief} onRunPipelineCommand={handleRunPipelineCommand} />;
  if (activeView === "pipeline") content = <PipelineView onView={setActiveView} />;
  if (activeView === "composition") content = <CompositionStudio />;
  if (activeView === "supervisual") content = <SuperVisualStudio activeGuest={activeGuest} onCommandReceipt={handleTimelineReceipt} />;
  if (activeView === "timeline") content = <VideoTimelineWorkbench activeGuest={activeGuest} onCommandReceipt={handleTimelineReceipt} onStartRender={handleStartRender} />;
  if (activeView === "review") content = <ReviewWorkbench />;
  if (activeView === "agents") content = <AgentFactory />;
  if (activeView === "evals") content = <EvalsView />;

  return (
    <AppShell activeView={activeView} onViewChange={setActiveView} activeGuest={activeGuest} onGuestChange={setGuestId} onNewInterviewBrief={handleGenerateBrief}>
      {content}
      {activeView === "control" && (
        <section className="screen flush">
          <section className="panel">
            <PanelHeader kicker="Format Registry" title="Supported Output Families" />
            <FormatsPanel />
          </section>
        </section>
      )}
    </AppShell>
  );
}
