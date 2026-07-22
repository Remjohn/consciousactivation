import { useEffect, useState } from "react";
import { listPipelineRuns } from "../api/pipelineRunMonitor.js";

export function OperationsCommandCenter({
  activeGuest,
  runtime,
  commandText,
  setCommandText,
  onSubmitCommandText,
  onGenerateBrief,
  onRunPipelineCommand,
  onStartRender,
  onTestApi,
  onView,
}) {
  const latestReceipt = runtime.commandReceipts[0];
  const [pipelineRuns, setPipelineRuns] = useState([]);

  useEffect(() => {
    let cancelled = false;
    async function loadPipelineRuns() {
      const runs = await listPipelineRuns();
      if (!cancelled) setPipelineRuns(runs);
    }
    loadPipelineRuns();
    return () => {
      cancelled = true;
    };
  }, []);

  const blockedCount = pipelineRuns.reduce((count, run) => count + (run.blocker_count || 0), 0);
  const pendingApprovalCount = pipelineRuns.reduce((count, run) => count + (run.pending_approval_count || 0), 0);

  return (
    <main className="screen ops-layout">
      <section className="panel large ops-command-panel">
        <div className="panel-header">
          <div>
            <span className="eyebrow amber">Agentic Command Surface</span>
            <h2>Factory Command Center</h2>
          </div>
          <button type="button" className="small-button" onClick={onTestApi}>
            Test CMF API
          </button>
        </div>

        <div className="ops-status-grid">
          <StatusCard label="API" value={runtime.apiStatus.state} detail={runtime.apiStatus.detail} tone={runtime.apiStatus.state} />
          <StatusCard label="Harness" value={runtime.harnessStatus.state} detail={runtime.harnessStatus.detail} tone={runtime.harnessStatus.state} />
          <StatusCard label="Latest Command" value={latestReceipt?.command_type || "none"} detail={latestReceipt?.runtime_mode || "waiting"} />
        </div>

        <div className="command-console">
          <label htmlFor="operator-command">Operator command</label>
          <textarea
            id="operator-command"
            value={commandText}
            onChange={(event) => setCommandText(event.target.value)}
            placeholder="Ask the factory: create an interview brief, repair the quote alignment, render the reaction clip..."
          />
          <div className="command-console-actions">
            <button type="button" className="primary-button" onClick={onSubmitCommandText}>
              Send to Command Bus
            </button>
            <button type="button" className="ghost-button" onClick={() => onView("timeline")}>
              Open Timeline
            </button>
          </div>
        </div>

        <div className="quick-command-grid">
          <QuickCommand
            code="IBF"
            title="Create Interview Brief"
            detail="CRAL, Context Premises, Matrix of Edging, JIT Interview Skill"
            onClick={onGenerateBrief}
          />
          <QuickCommand
            code="CRAL"
            title="Run Context Research"
            detail="Audience signal, comment mining, premise evidence"
            onClick={() => onRunPipelineCommand("run_cral_context_research", "CRAL research requested")}
          />
          <QuickCommand
            code="JIT"
            title="Compile Interview Skill"
            detail="Extraction targets, narrative induction, question engineering"
            onClick={() => onRunPipelineCommand("compile_interview_brief_skill", "JIT Interview Skill compile requested")}
          />
          <QuickCommand
            code="RND"
            title="Render Active Clip"
            detail="VideoEditProgram, timeline edit state, render receipt"
            onClick={onStartRender}
          />
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <span className="eyebrow">Scope</span>
            <h2>{activeGuest.workspace}</h2>
          </div>
        </div>
        <div className="ops-scope-stack">
          <InfoLine label="Guest" value={activeGuest.name} />
          <InfoLine label="Voice DNA" value={activeGuest.voiceDna} />
          <InfoLine label="Emotional DNA" value={activeGuest.emotionalDna} />
          <InfoLine label="Next action" value={activeGuest.nextAction} />
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <span className="eyebrow">Agent Runs</span>
            <h2>Harness Trace</h2>
          </div>
        </div>
        <div className="agent-run-list">
          {runtime.agentRuns.length === 0 && <p className="muted-copy">No agent run has been requested from this browser session yet.</p>}
          {runtime.agentRuns.map((run) => (
            <article className="agent-run-card" key={run.run_id}>
              <div>
                <strong>{run.agent_code}</strong>
                <span>{run.status}</span>
              </div>
              <p>{run.goal}</p>
              <small>{run.receipt_id}</small>
            </article>
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <span className="eyebrow">Pipeline Runs</span>
            <h2>Monitor Snapshot</h2>
          </div>
          <button type="button" className="small-button" onClick={() => onView("pipeline")}>
            Open Pipeline
          </button>
        </div>
        <div className="ops-status-grid">
          <StatusCard label="Runs" value={pipelineRuns.length} detail="read-model rows" />
          <StatusCard label="Blockers" value={blockedCount} detail="operator-visible" tone={blockedCount ? "blocked" : "ready"} />
          <StatusCard label="Approvals" value={pendingApprovalCount} detail="pending gates" tone={pendingApprovalCount ? "waiting" : "ready"} />
        </div>
        <div className="agent-run-list">
          {pipelineRuns.length === 0 && <p className="muted-copy">Pipeline run monitor is using fixture fallback or no runs are available.</p>}
          {pipelineRuns.slice(0, 3).map((run) => (
            <article className="agent-run-card" key={run.pipeline_run_id}>
              <div>
                <strong>{run.recipe_id}</strong>
                <span>{run.status}</span>
              </div>
              <p>{run.current_step_id || "waiting"} / {run.progress_percent}%</p>
              <small>{run.pipeline_run_id}</small>
            </article>
          ))}
        </div>
      </section>

      <section className="panel large">
        <div className="panel-header">
          <div>
            <span className="eyebrow">Receipts</span>
            <h2>Command Ledger</h2>
          </div>
        </div>
        <div className="receipt-table">
          {runtime.commandReceipts.length === 0 && <p className="muted-copy">Receipts will appear here after an operator command is submitted.</p>}
          {runtime.commandReceipts.map((receipt) => (
            <article className="receipt-table-row" key={receipt.receipt_id}>
              <div>
                <strong>{receipt.command_type}</strong>
                <span>{receipt.receipt_id}</span>
              </div>
              <span>{receipt.status}</span>
              <span>{receipt.runtime_mode}</span>
              <small>{receipt.backend_error || receipt.created_at}</small>
            </article>
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <span className="eyebrow">Outputs</span>
            <h2>Render Receipts</h2>
          </div>
        </div>
        <div className="output-list">
          {runtime.outputs.length === 0 && <p className="muted-copy">No render output receipt yet.</p>}
          {runtime.outputs.map((output) => (
            <article className="output-card" key={output.output_id}>
              <strong>{output.label}</strong>
              <span>{output.status}</span>
              <small>{output.output_ref}</small>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

function StatusCard({ label, value, detail, tone }) {
  return (
    <div className={`ops-status-card ${tone || ""}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{detail}</small>
    </div>
  );
}

function QuickCommand({ code, title, detail, onClick }) {
  return (
    <button type="button" className="quick-command-card" onClick={onClick}>
      <span>{code}</span>
      <strong>{title}</strong>
      <small>{detail}</small>
    </button>
  );
}

function InfoLine({ label, value }) {
  return (
    <div className="info-line">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}
