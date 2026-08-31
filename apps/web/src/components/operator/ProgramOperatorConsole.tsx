import React, { useState, useEffect, useCallback } from "react";
import {
  fetchPrograms,
  fetchExecutions,
  fetchExecutionDetail,
  fetchLineageGraph,
  fetchExecutionTrace,
  runProgram,
  pauseExecution,
  resumeExecution,
  approveExecutionGate,
  rejectExecutionGate,
  repairExecutionState,
  type ProgramSummary,
  type ProgramExecutionSummary,
  type ProgramExecutionDetail,
  type ArtifactLineageGraph,
  type ExecutionTraceProjection,
} from "../../api/operator";
import { LineageGraphViewer } from "./LineageGraphViewer";
import { ChatSupervisionConsole } from "./ChatSupervisionConsole";
import { Badge } from "../ui/Badge";
import { Button } from "../ui/Button";

interface ProgramOperatorConsoleProps {
  workspaceId?: string;
}

export function ProgramOperatorConsole({ workspaceId = "ws-default" }: ProgramOperatorConsoleProps) {
  // State
  const [programs, setPrograms] = useState<ProgramSummary[]>([]);
  const [executions, setExecutions] = useState<ProgramExecutionSummary[]>([]);
  const [selectedAggregateId, setSelectedAggregateId] = useState<string | null>(null);
  const [executionDetail, setExecutionDetail] = useState<ProgramExecutionDetail | null>(null);
  const [lineageGraph, setLineageGraph] = useState<ArtifactLineageGraph | null>(null);
  const [executionTrace, setExecutionTrace] = useState<ExecutionTraceProjection | null>(null);

  // Active sub-view tab
  const [activeTab, setActiveTab] = useState<"trace" | "lineage" | "chat" | "state">("trace");

  // Loading & error state
  const [isLoading, setIsLoading] = useState(false);
  const [actionError, setActionError] = useState<{ message: string; isConflict?: boolean } | null>(null);
  const [actionSuccess, setActionSuccess] = useState<string | null>(null);

  // Rejection modal state
  const [isRejectModalOpen, setIsRejectModalOpen] = useState(false);
  const [rejectReason, setRejectReason] = useState("");
  const [rejectRoute, setRejectRoute] = useState("RETURN_TO_HUNTER");

  // State repair modal state
  const [isRepairModalOpen, setIsRepairModalOpen] = useState(false);
  const [repairAction, setRepairAction] = useState("");
  const [repairPayloadStr, setRepairPayloadStr] = useState("{}");

  // 1. Initial Load: Programs & Executions
  const loadInitialData = useCallback(async () => {
    setIsLoading(true);
    setActionError(null);
    try {
      const [progRes, execRes] = await Promise.all([
        fetchPrograms(),
        fetchExecutions({ workspace_id: workspaceId }),
      ]);
      setPrograms(progRes.programs);
      setExecutions(execRes.executions);

      if (execRes.executions.length > 0 && !selectedAggregateId) {
        setSelectedAggregateId(execRes.executions[0].aggregate_id);
      }
    } catch (err: any) {
      setActionError({ message: `Failed to load catalog/executions: ${err.message}` });
    } finally {
      setIsLoading(false);
    }
  }, [workspaceId, selectedAggregateId]);

  useEffect(() => {
    loadInitialData();
  }, [loadInitialData]);

  // 2. Load Selected Execution Detail, Lineage & Trace
  const loadExecutionDetails = useCallback(async (aggId: string) => {
    setActionError(null);
    try {
      const [detail, lineage, trace] = await Promise.all([
        fetchExecutionDetail(aggId),
        fetchLineageGraph(aggId),
        fetchExecutionTrace(aggId),
      ]);
      setExecutionDetail(detail);
      setLineageGraph(lineage);
      setExecutionTrace(trace);
    } catch (err: any) {
      setActionError({ message: `Failed to load execution details: ${err.message}` });
    }
  }, []);

  useEffect(() => {
    if (selectedAggregateId) {
      loadExecutionDetails(selectedAggregateId);
    }
  }, [selectedAggregateId, loadExecutionDetails]);

  // Handler: Run a Program
  const handleRunProgram = async (programId: string) => {
    setActionError(null);
    setActionSuccess(null);
    try {
      const newExec = await runProgram({
        program_id: programId,
        workspace_id: workspaceId,
      });
      setActionSuccess(`Program '${programId}' started successfully.`);
      const execRes = await fetchExecutions({ workspace_id: workspaceId });
      setExecutions(execRes.executions);
      setSelectedAggregateId(newExec.aggregate_id);
    } catch (err: any) {
      setActionError({ message: err.message || "Failed to start program" });
    }
  };

  // Handler: Pause Execution
  const handlePause = async () => {
    if (!executionDetail) return;
    setActionError(null);
    setActionSuccess(null);
    try {
      await pauseExecution(
        executionDetail.aggregate.aggregate_id,
        executionDetail.aggregate.version,
        executionDetail.aggregate.state_hash
      );
      setActionSuccess("Execution paused successfully.");
      loadExecutionDetails(executionDetail.aggregate.aggregate_id);
    } catch (err: any) {
      const isConflict = err.status === 409 || err.message?.includes("conflict");
      setActionError({ message: err.message || "Failed to pause execution", isConflict });
    }
  };

  // Handler: Resume Execution
  const handleResume = async () => {
    if (!executionDetail) return;
    setActionError(null);
    setActionSuccess(null);
    try {
      await resumeExecution(
        executionDetail.aggregate.aggregate_id,
        executionDetail.aggregate.version,
        executionDetail.aggregate.state_hash
      );
      setActionSuccess("Execution resumed successfully.");
      loadExecutionDetails(executionDetail.aggregate.aggregate_id);
    } catch (err: any) {
      const isConflict = err.status === 409 || err.message?.includes("conflict");
      setActionError({ message: err.message || "Failed to resume execution", isConflict });
    }
  };

  // Handler: Authorize Gate (Approve)
  const handleApprove = async () => {
    if (!executionDetail) return;
    setActionError(null);
    setActionSuccess(null);
    try {
      await approveExecutionGate(
        executionDetail.aggregate.aggregate_id,
        executionDetail.aggregate.version,
        executionDetail.aggregate.state_hash,
        {
          notes: "Approved via Operator Console",
        }
      );
      setActionSuccess("Milestone authorized and signed successfully.");
      loadExecutionDetails(executionDetail.aggregate.aggregate_id);
    } catch (err: any) {
      const isConflict = err.status === 409 || err.message?.includes("conflict");
      setActionError({ message: err.message || "Failed to approve milestone", isConflict });
    }
  };

  // Handler: Reject Gate with Disposition Route
  const handleRejectSubmit = async () => {
    if (!executionDetail || !rejectReason.trim()) return;
    setActionError(null);
    setActionSuccess(null);
    try {
      await rejectExecutionGate(
        executionDetail.aggregate.aggregate_id,
        executionDetail.aggregate.version,
        executionDetail.aggregate.state_hash,
        {
          rejection_reason: rejectReason.trim(),
          disposition_route: rejectRoute,
        }
      );
      setIsRejectModalOpen(false);
      setRejectReason("");
      setActionSuccess(`Milestone rejected. Routed to '${rejectRoute}'.`);
      loadExecutionDetails(executionDetail.aggregate.aggregate_id);
    } catch (err: any) {
      const isConflict = err.status === 409 || err.message?.includes("conflict");
      setActionError({ message: err.message || "Failed to reject milestone", isConflict });
    }
  };

  // Handler: Governed State Repair
  const handleRepairSubmit = async () => {
    if (!executionDetail || !repairAction.trim()) return;
    let payload = {};
    try {
      payload = JSON.parse(repairPayloadStr);
    } catch {
      setActionError({ message: "Invalid JSON format in repair payload." });
      return;
    }

    setActionError(null);
    setActionSuccess(null);
    try {
      await repairExecutionState(
        executionDetail.aggregate.aggregate_id,
        executionDetail.aggregate.version,
        executionDetail.aggregate.state_hash,
        {
          repair_action: repairAction.trim(),
          repair_payload: payload,
        }
      );
      setIsRepairModalOpen(false);
      setRepairAction("");
      setRepairPayloadStr("{}");
      setActionSuccess("State repair applied successfully.");
      loadExecutionDetails(executionDetail.aggregate.aggregate_id);
    } catch (err: any) {
      const isConflict = err.status === 409 || err.message?.includes("conflict");
      setActionError({ message: err.message || "Failed to repair state", isConflict });
    }
  };

  const agg = executionDetail?.aggregate;

  return (
    <div className="flex h-full min-h-screen flex-col bg-background text-foreground">
      {/* Top Bar */}
      <header className="border-b border-border bg-surface px-6 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="rounded bg-accent-solid/20 p-1.5 text-accent">
              <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h1 className="text-base font-bold tracking-tight text-foreground">
                CAE Program & Artifact Operator Application
              </h1>
              <p className="text-xs text-muted-foreground">
                Authoritative multi-lane supervision, anti-stale CAS control, cryptographic lineage
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Badge tone="accent">Workspace: {workspaceId}</Badge>
            <Button variant="ghost" onClick={loadInitialData} disabled={isLoading}>
              {isLoading ? "Refreshing..." : "Refresh"}
            </Button>
          </div>
        </div>
      </header>

      {/* Conflict / Error Banner */}
      {actionError && (
        <div
          className={`flex items-center justify-between border-b px-6 py-2.5 text-xs ${
            actionError.isConflict
              ? "border-amber-600/40 bg-amber-950/40 text-amber-200"
              : "border-danger/40 bg-danger/10 text-danger"
          }`}
        >
          <div className="flex items-center space-x-2">
            <span className="font-bold uppercase">
              {actionError.isConflict ? "CAS Concurrency Conflict:" : "Error:"}
            </span>
            <span>{actionError.message}</span>
          </div>
          {actionError.isConflict && selectedAggregateId && (
            <Button
              variant="solid"
              onClick={() => loadExecutionDetails(selectedAggregateId)}
              className="!py-0.5 text-xs"
            >
              Reload Latest State
            </Button>
          )}
        </div>
      )}

      {/* Success Notification */}
      {actionSuccess && (
        <div className="flex items-center justify-between border-b border-emerald-600/40 bg-emerald-950/30 px-6 py-2 text-xs text-emerald-300">
          <span>{actionSuccess}</span>
          <button onClick={() => setActionSuccess(null)} className="text-muted-foreground hover:text-foreground">
            &times;
          </button>
        </div>
      )}

      {/* Main Split Layout */}
      <div className="grid flex-1 grid-cols-12 gap-0 overflow-hidden">
        {/* Left Column: Programs Catalog & Executions List (3 cols) */}
        <div className="col-span-12 flex flex-col border-r border-border bg-surface lg:col-span-3">
          {/* Programs Catalog */}
          <div className="border-b border-border p-4">
            <h2 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Governed Programs ({programs.length})
            </h2>
            <div className="max-h-48 space-y-1.5 overflow-y-auto">
              {programs.map((p) => (
                <div
                  key={p.program_id}
                  className="flex items-center justify-between rounded border border-border bg-surface-elevated/40 p-2 text-xs hover:border-accent/50"
                >
                  <div className="truncate pr-2">
                    <div className="font-semibold text-foreground truncate" title={p.program_id}>
                      {p.program_id}
                    </div>
                    <div className="text-[10px] text-muted-foreground">
                      v{p.version} &bull; {p.lanes.join(", ")}
                    </div>
                  </div>
                  <button
                    onClick={() => handleRunProgram(p.program_id)}
                    className="rounded bg-accent-solid px-2 py-1 text-[11px] font-medium text-accent-foreground hover:brightness-110"
                  >
                    Run
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Active Execution Aggregates */}
          <div className="flex-1 overflow-y-auto p-4">
            <div className="mb-2 flex items-center justify-between">
              <h2 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Executions ({executions.length})
              </h2>
            </div>
            <div className="space-y-2">
              {executions.length === 0 ? (
                <div className="py-6 text-center text-xs text-muted-foreground">No active executions</div>
              ) : (
                executions.map((e) => {
                  const isSelected = selectedAggregateId === e.aggregate_id;
                  return (
                    <div
                      key={e.aggregate_id}
                      onClick={() => setSelectedAggregateId(e.aggregate_id)}
                      className={`cursor-pointer rounded-lg border p-3 transition-all ${
                        isSelected
                          ? "border-accent bg-surface-elevated shadow-sm"
                          : "border-border bg-surface-elevated/20 hover:border-accent/40"
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-mono text-xs font-semibold text-foreground truncate max-w-[140px]">
                          {e.program_id}
                        </span>
                        <Badge
                          tone={
                            e.lifecycle === "COMPLETED"
                              ? "success"
                              : e.lifecycle === "PAUSED"
                              ? "accent"
                              : e.lifecycle === "AWAITING_APPROVAL"
                              ? "accent"
                              : "muted"
                          }
                        >
                          {e.lifecycle}
                        </Badge>
                      </div>
                      <div className="mt-1 flex items-center justify-between text-[11px] text-muted-foreground">
                        <span>State: <b className="text-foreground">{e.current_state}</b></span>
                        <span>v{e.version}</span>
                      </div>
                      <div className="mt-1 font-mono text-[10px] text-muted-foreground truncate" title={e.aggregate_id}>
                        ID: {e.aggregate_id}
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </div>
        </div>

        {/* Center/Right Area: Execution Inspection, Action Rail & Tabs (9 cols) */}
        <div className="col-span-12 flex flex-col overflow-y-auto bg-background p-6 lg:col-span-9">
          {agg ? (
            <div className="flex flex-col space-y-6">
              {/* Execution Header & Action Bar */}
              <div className="rounded-xl border border-border bg-surface p-5 shadow-sm">
                <div className="flex flex-wrap items-start justify-between gap-4 border-b border-border pb-4">
                  <div>
                    <div className="flex items-center space-x-2">
                      <h2 className="text-lg font-bold text-foreground">{agg.program_id}</h2>
                      <Badge tone="accent">v{agg.program_version}</Badge>
                      <Badge tone={agg.lifecycle === "COMPLETED" ? "success" : "muted"}>
                        {agg.lifecycle}
                      </Badge>
                    </div>
                    <p className="mt-1 font-mono text-xs text-muted-foreground">
                      Aggregate ID: <span className="text-foreground">{agg.aggregate_id}</span>
                    </p>
                  </div>

                  {/* Operator Authority Actions */}
                  <div className="flex flex-wrap items-center gap-2">
                    {agg.lifecycle === "RUNNING" && (
                      <Button variant="ghost" onClick={handlePause}>
                        Pause Execution
                      </Button>
                    )}
                    {agg.lifecycle === "PAUSED" && (
                      <Button variant="solid" onClick={handleResume}>
                        Resume Execution
                      </Button>
                    )}
                    <Button variant="solid" onClick={handleApprove} className="!bg-emerald-600 hover:!bg-emerald-500">
                      Authorize Gate
                    </Button>
                    <Button variant="ghost" onClick={() => setIsRejectModalOpen(true)} className="text-danger hover:bg-danger/10">
                      Reject Milestone
                    </Button>
                    <Button variant="ghost" onClick={() => setIsRepairModalOpen(true)}>
                      State Repair
                    </Button>
                  </div>
                </div>

                {/* State Vector & Concurrency Metrics */}
                <div className="mt-4 grid grid-cols-2 gap-4 text-xs md:grid-cols-4">
                  <div className="rounded border border-border bg-surface-elevated/40 p-2.5">
                    <span className="text-muted-foreground">Current State</span>
                    <p className="mt-0.5 font-bold text-foreground">{agg.current_state}</p>
                  </div>
                  <div className="rounded border border-border bg-surface-elevated/40 p-2.5">
                    <span className="text-muted-foreground">State Version</span>
                    <p className="mt-0.5 font-mono font-bold text-foreground">v{agg.version}</p>
                  </div>
                  <div className="rounded border border-border bg-surface-elevated/40 p-2.5">
                    <span className="text-muted-foreground">SHA-256 State Hash</span>
                    <p className="mt-0.5 font-mono text-[11px] text-foreground truncate" title={agg.state_hash}>
                      {agg.state_hash.slice(0, 16)}...
                    </p>
                  </div>
                  <div className="rounded border border-border bg-surface-elevated/40 p-2.5">
                    <span className="text-muted-foreground">Allowable Transitions</span>
                    <p className="mt-0.5 font-semibold text-accent">
                      {executionDetail?.allowable_transitions.length || 0} valid paths
                    </p>
                  </div>
                </div>
              </div>

              {/* View Tabs */}
              <div className="flex space-x-1 border-b border-border">
                <button
                  onClick={() => setActiveTab("trace")}
                  className={`border-b-2 px-4 py-2 text-xs font-semibold uppercase tracking-wider transition-all ${
                    activeTab === "trace"
                      ? "border-accent text-accent"
                      : "border-transparent text-muted-foreground hover:text-foreground"
                  }`}
                >
                  Execution Trace DAG
                </button>
                <button
                  onClick={() => setActiveTab("lineage")}
                  className={`border-b-2 px-4 py-2 text-xs font-semibold uppercase tracking-wider transition-all ${
                    activeTab === "lineage"
                      ? "border-accent text-accent"
                      : "border-transparent text-muted-foreground hover:text-foreground"
                  }`}
                >
                  Artifact Lineage DAG
                </button>
                <button
                  onClick={() => setActiveTab("chat")}
                  className={`border-b-2 px-4 py-2 text-xs font-semibold uppercase tracking-wider transition-all ${
                    activeTab === "chat"
                      ? "border-accent text-accent"
                      : "border-transparent text-muted-foreground hover:text-foreground"
                  }`}
                >
                  Chat Supervision Terminal
                </button>
                <button
                  onClick={() => setActiveTab("state")}
                  className={`border-b-2 px-4 py-2 text-xs font-semibold uppercase tracking-wider transition-all ${
                    activeTab === "state"
                      ? "border-accent text-accent"
                      : "border-transparent text-muted-foreground hover:text-foreground"
                  }`}
                >
                  Raw State Data
                </button>
              </div>

              {/* Tab Content */}
              {activeTab === "trace" && (
                <div className="rounded-lg border border-border bg-surface p-4">
                  <div className="mb-3 flex items-center justify-between">
                    <h3 className="text-xs font-semibold uppercase tracking-wider text-foreground">
                      Execution Trace & Transition Audit Ledger
                    </h3>
                    <span className="text-xs text-muted-foreground">
                      {executionTrace?.trace_nodes.length || 0} transitions recorded
                    </span>
                  </div>

                  {executionTrace && executionTrace.trace_nodes.length > 0 ? (
                    <div className="space-y-2">
                      {executionTrace.trace_nodes.map((node) => (
                        <div
                          key={node.transition_id}
                          className="flex items-center justify-between rounded border border-border bg-surface-elevated/30 p-3 text-xs"
                        >
                          <div className="flex items-center space-x-3">
                            <span className="font-mono text-muted-foreground">#{node.step_index}</span>
                            <div>
                              <div className="flex items-center space-x-2">
                                <span className="font-semibold text-foreground">{node.transition_name}</span>
                                <span
                                  className={`rounded px-1.5 py-0.2 text-[10px] font-semibold ${
                                    node.lane === "COMMANDER"
                                      ? "bg-purple-950/60 text-purple-300"
                                      : node.lane === "COMPOSER"
                                      ? "bg-blue-950/60 text-blue-300"
                                      : node.lane === "ANALYST"
                                      ? "bg-emerald-950/60 text-emerald-300"
                                      : "bg-amber-950/60 text-amber-300"
                                  }`}
                                >
                                  {node.lane}
                                </span>
                              </div>
                              <div className="mt-0.5 text-[11px] text-muted-foreground">
                                <span>{node.from_state} &rarr; {node.to_state}</span>
                                <span className="ml-2 font-mono">By: {node.actor_id}</span>
                              </div>
                            </div>
                          </div>

                          <div className="text-right font-mono text-[11px] text-muted-foreground">
                            <div>Receipt: <span className="text-accent">{node.receipt_id.slice(0, 12)}...</span></div>
                            <div>v{node.committed_version} &bull; {node.timestamp}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="py-8 text-center text-xs text-muted-foreground">
                      No transitions executed yet for this aggregate.
                    </div>
                  )}
                </div>
              )}

              {activeTab === "lineage" && (
                <LineageGraphViewer
                  lineage={lineageGraph}
                  onRefresh={() => loadExecutionDetails(agg.aggregate_id)}
                />
              )}

              {activeTab === "chat" && (
                <div className="h-[520px]">
                  <ChatSupervisionConsole
                    workspaceId={workspaceId}
                    activeExecution={agg}
                    onStateMutated={() => loadExecutionDetails(agg.aggregate_id)}
                  />
                </div>
              )}

              {activeTab === "state" && (
                <div className="rounded-lg border border-border bg-surface p-4">
                  <h3 className="mb-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                    State Aggregate Payload
                  </h3>
                  <pre className="max-h-96 overflow-y-auto rounded border border-border bg-surface-elevated p-3 font-mono text-xs text-foreground">
                    {JSON.stringify(executionDetail?.state_data || {}, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          ) : (
            <div className="flex h-96 flex-col items-center justify-center text-center text-muted-foreground">
              <p className="text-sm font-medium">Select an execution aggregate on the left to inspect</p>
              <p className="mt-1 text-xs">Or run a program from the Governed Programs catalog above.</p>
            </div>
          )}
        </div>
      </div>

      {/* Reject Milestone Modal */}
      {isRejectModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
          <div className="w-full max-w-md rounded-xl border border-border bg-surface p-5 shadow-xl">
            <h3 className="text-sm font-bold text-foreground">Reject Milestone with Disposition Routing</h3>
            <p className="mt-1 text-xs text-muted-foreground">
              Typed rejection will record a rejection receipt and transition the state machine according to the disposition route.
            </p>

            <div className="mt-4 space-y-3 text-xs">
              <div>
                <label className="font-semibold text-muted-foreground">Disposition Route</label>
                <select
                  value={rejectRoute}
                  onChange={(e) => setRejectRoute(e.target.value)}
                  className="mt-1 w-full rounded border border-border bg-surface-elevated p-2 text-foreground focus:outline-none"
                >
                  <option value="RETURN_TO_HUNTER">RETURN_TO_HUNTER (Evidence acquisition)</option>
                  <option value="RETURN_TO_COMPOSER">RETURN_TO_COMPOSER (Revision)</option>
                  <option value="TERMINATE_FAILED">TERMINATE_FAILED (Terminal fail)</option>
                  <option value="QUARANTINE_REPAIR">QUARANTINE_REPAIR (Operator repair)</option>
                </select>
              </div>

              <div>
                <label className="font-semibold text-muted-foreground">Rejection Reason</label>
                <textarea
                  value={rejectReason}
                  onChange={(e) => setRejectReason(e.target.value)}
                  placeholder="Explain why this candidate/milestone was rejected..."
                  rows={3}
                  className="mt-1 w-full rounded border border-border bg-surface-elevated p-2 text-foreground focus:outline-none"
                />
              </div>
            </div>

            <div className="mt-5 flex justify-end space-x-2">
              <Button variant="ghost" onClick={() => setIsRejectModalOpen(false)}>
                Cancel
              </Button>
              <Button
                variant="solid"
                onClick={handleRejectSubmit}
                disabled={!rejectReason.trim()}
                className="!bg-danger text-white"
              >
                Confirm Rejection
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* State Repair Modal */}
      {isRepairModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
          <div className="w-full max-w-md rounded-xl border border-border bg-surface p-5 shadow-xl">
            <h3 className="text-sm font-bold text-foreground">Governed State Repair</h3>
            <p className="mt-1 text-xs text-muted-foreground">
              Apply governed direct manipulation to state fields under COMMANDER authorization.
            </p>

            <div className="mt-4 space-y-3 text-xs">
              <div>
                <label className="font-semibold text-muted-foreground">Repair Action</label>
                <input
                  type="text"
                  value={repairAction}
                  onChange={(e) => setRepairAction(e.target.value)}
                  placeholder="e.g. override_candidate, reset_state..."
                  className="mt-1 w-full rounded border border-border bg-surface-elevated p-2 text-foreground focus:outline-none"
                />
              </div>

              <div>
                <label className="font-semibold text-muted-foreground">Repair Payload (JSON)</label>
                <textarea
                  value={repairPayloadStr}
                  onChange={(e) => setRepairPayloadStr(e.target.value)}
                  rows={4}
                  className="mt-1 w-full rounded border border-border bg-surface-elevated p-2 font-mono text-xs text-foreground focus:outline-none"
                />
              </div>
            </div>

            <div className="mt-5 flex justify-end space-x-2">
              <Button variant="ghost" onClick={() => setIsRepairModalOpen(false)}>
                Cancel
              </Button>
              <Button
                variant="solid"
                onClick={handleRepairSubmit}
                disabled={!repairAction.trim()}
              >
                Apply Repair
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
