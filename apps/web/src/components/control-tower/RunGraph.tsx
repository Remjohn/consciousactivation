// TS-APP-UI-003 - RunGraph component
// Live node DAG with WS-driven pulse animation

import { useMemo } from "react";
import type { RunNodeProjection, CoarseNodeState } from "../../lib/nodeState";
import { STUDIO_STATUS_TOKEN, coarseFromWsState } from "../../lib/nodeState";
import type { ConnectionState } from "../../hooks/usePipelineStatus";

interface RunGraphProps {
  runNodes: RunNodeProjection[];
  nodeVisual: Map<string, CoarseNodeState>;
  connectionState: ConnectionState;
}

// DAG layout algorithm (Section 6 of tech spec)
function layoutRunGraph(nodes: RunNodeProjection[]): Array<{ node_id: string; column: number }> {
  const byId = new Map(nodes.map((n) => [n.node_id, n]));
  const column = new Map<string, number>();

  function depth(id: string, seen: Set<string>): number {
    if (column.has(id)) return column.get(id)!;
    if (seen.has(id)) return 0; // cycle guard
    seen.add(id);
    const deps = byId.get(id)?.dependency_ids ?? [];
    const d = deps.length ? Math.max(...deps.map((dep) => depth(dep, seen))) + 1 : 0;
    column.set(id, d);
    return d;
  }

  nodes.forEach((n) => depth(n.node_id, new Set()));
  return nodes.map((n) => ({ node_id: n.node_id, column: column.get(n.node_id)! }));
}

export function RunGraph({ runNodes, nodeVisual, connectionState }: RunGraphProps) {
  // Handle special connection states
  if (connectionState === "no_run") {
    return (
      <div className="control-tower-card">
        <div className="control-tower-card-header">
          <span>Run Graph</span>
        </div>
        <p className="text-ca-text-secondary">
          No production run is linked to this campaign yet
        </p>
      </div>
    );
  }

  if (connectionState === "multiple_runs") {
    return (
      <div className="control-tower-card">
        <div className="control-tower-card-header">
          <span>Run Graph</span>
        </div>
        <p className="text-ca-text-secondary">
          This campaign has more than one linked run — status can't be resolved automatically
        </p>
      </div>
    );
  }

  // Layout nodes
  const layout = useMemo(() => layoutRunGraph(runNodes), [runNodes]);

  // Group nodes by column
  const columns = useMemo(() => {
    const cols: RunNodeProjection[][] = [];
    layout.forEach(({ node_id, column }) => {
      if (!cols[column]) cols[column] = [];
      const node = runNodes.find((n) => n.node_id === node_id);
      if (node) cols[column].push(node);
    });
    return cols;
  }, [layout, runNodes]);

  return (
    <div className="control-tower-card">
      <div className="control-tower-card-header">
        <span>Run Graph</span>
        {connectionState === "closed" && (
          <span className="text-xs text-ca-waiting">Reconnecting...</span>
        )}
      </div>

      {/* DAG Visualization */}
      <div className="flex gap-4 overflow-x-auto p-4">
        {columns.map((nodes, colIdx) => (
          <div key={colIdx} className="flex flex-col gap-2">
            {nodes.map((node) => {
              const studioStatus = node.status as keyof typeof STUDIO_STATUS_TOKEN;
              const statusInfo = STUDIO_STATUS_TOKEN[studioStatus] ?? {
                color: "var(--ca-idle)",
                label: studioStatus,
              };
              const visualState = nodeVisual.get(node.node_id) ?? "idle";
              const isPulsing = visualState === "active";

              return (
                <div
                  key={node.node_id}
                  className={`min-w-[200px] rounded-lg border p-3 transition-all ${
                    isPulsing ? "animate-pulse" : ""
                  }`}
                  style={{
                    borderColor: statusInfo.color,
                    backgroundColor: "var(--ca-surface-raised)",
                  }}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-ca-text-primary">
                      {node.node_id.slice(0, 8)}
                    </span>
                    <span
                      className="text-xs font-mono"
                      style={{ color: statusInfo.color }}
                    >
                      {statusInfo.label}
                    </span>
                  </div>
                  {node.blocker_codes && node.blocker_codes.length > 0 && (
                    <div className="mt-1 text-xs text-ca-danger">
                      Blocked: {node.blocker_codes.join(", ")}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        ))}
      </div>

      {runNodes.length === 0 && (
        <p className="text-center text-ca-text-tertiary">No nodes in this run</p>
      )}
    </div>
  );
}
