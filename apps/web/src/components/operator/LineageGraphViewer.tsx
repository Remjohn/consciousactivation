import React, { useState } from "react";
import type { ArtifactLineageGraph, LineageNode, LineageEdge } from "../../api/operator";
import { Badge } from "../ui/Badge";

interface LineageGraphViewerProps {
  lineage: ArtifactLineageGraph | null;
  isLoading?: boolean;
  onRefresh?: () => void;
}

export function LineageGraphViewer({ lineage, isLoading = false, onRefresh }: LineageGraphViewerProps) {
  const [selectedNode, setSelectedNode] = useState<LineageNode | null>(null);

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center rounded-lg border border-border bg-surface p-6 text-muted-foreground">
        <span className="animate-pulse">Loading artifact lineage graph...</span>
      </div>
    );
  }

  if (!lineage || lineage.nodes.length === 0) {
    return (
      <div className="flex h-64 flex-col items-center justify-center rounded-lg border border-border bg-surface p-6 text-center text-muted-foreground">
        <p className="mb-2 text-sm font-medium">No artifact lineage recorded yet</p>
        <p className="text-xs">Lineage nodes will populate as program state transitions execute.</p>
      </div>
    );
  }

  const isVerified = lineage.is_lossless && lineage.verification_status === "LOSSLESS_VERIFIED";

  return (
    <div className="flex flex-col space-y-4 rounded-lg border border-border bg-surface p-4">
      {/* Header & Verification Status */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-border pb-3">
        <div className="flex items-center space-x-2">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-foreground">
            Artifact Lineage DAG
          </h3>
          <Badge tone={isVerified ? "success" : "danger"}>
            {isVerified ? "Lossless Verified" : "Verification Warning"}
          </Badge>
          <span className="text-xs text-muted-foreground">
            {lineage.nodes.length} Nodes &bull; {lineage.edges.length} Edges
          </span>
        </div>
        <div className="flex items-center space-x-2">
          {onRefresh && (
            <button
              onClick={onRefresh}
              className="rounded border border-border px-2 py-1 text-xs text-muted-foreground hover:bg-surface-elevated hover:text-foreground"
            >
              Refresh
            </button>
          )}
          <span className="font-mono text-xs text-muted-foreground" title={`Digest: ${lineage.verification_digest}`}>
            Digest: {lineage.verification_digest.slice(0, 12)}...
          </span>
        </div>
      </div>

      {/* DAG Visualization Canvas */}
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        {/* Nodes & Edges Column */}
        <div className="space-y-3 lg:col-span-2">
          <div className="text-xs font-semibold text-muted-foreground">LINEAGE NODES & TRANSFORMATIONS</div>
          <div className="max-h-96 space-y-2 overflow-y-auto pr-1">
            {lineage.nodes.map((node) => {
              const isSelected = selectedNode?.node_id === node.node_id;
              const isRoot = lineage.root_evidence_ids.includes(node.node_id);
              const isTerminal = lineage.terminal_artifact_ids.includes(node.node_id);

              return (
                <div
                  key={node.node_id}
                  onClick={() => setSelectedNode(node)}
                  className={`cursor-pointer rounded border p-2.5 transition-all ${
                    isSelected
                      ? "border-accent bg-surface-elevated shadow-sm"
                      : "border-border bg-surface hover:border-accent/40"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span className="font-mono text-xs font-medium text-foreground">{node.label}</span>
                      <span
                        className={`rounded px-1.5 py-0.5 text-[10px] font-semibold uppercase ${
                          node.lane === "COMMANDER"
                            ? "bg-purple-950/60 text-purple-300 border border-purple-700/50"
                            : node.lane === "COMPOSER"
                            ? "bg-blue-950/60 text-blue-300 border border-blue-700/50"
                            : node.lane === "ANALYST"
                            ? "bg-emerald-950/60 text-emerald-300 border border-emerald-700/50"
                            : "bg-amber-950/60 text-amber-300 border border-amber-700/50"
                        }`}
                      >
                        {node.lane}
                      </span>
                      {isRoot && (
                        <span className="rounded bg-teal-950/60 px-1.5 py-0.5 text-[10px] font-semibold text-teal-300 border border-teal-700/50">
                          ROOT EVIDENCE
                        </span>
                      )}
                      {isTerminal && (
                        <span className="rounded bg-emerald-950/60 px-1.5 py-0.5 text-[10px] font-semibold text-emerald-300 border border-emerald-700/50">
                          RELEASE ARTIFACT
                        </span>
                      )}
                    </div>
                    <span className="font-mono text-[11px] text-muted-foreground">{node.node_type}</span>
                  </div>

                  <div className="mt-1 flex items-center justify-between text-[11px] text-muted-foreground">
                    <span className="font-mono truncate max-w-xs" title={node.sha256}>
                      SHA: {node.sha256.slice(0, 16)}...
                    </span>
                    {node.receipt_ref && (
                      <span className="font-mono truncate max-w-[140px]" title={node.receipt_ref}>
                        Receipt: {node.receipt_ref.slice(0, 12)}...
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Edges Summary */}
          {lineage.edges.length > 0 && (
            <div className="pt-2">
              <div className="text-xs font-semibold text-muted-foreground mb-1.5">TRANSFORMATION EDGES</div>
              <div className="space-y-1 text-xs">
                {lineage.edges.map((edge) => (
                  <div key={edge.edge_id} className="flex items-center space-x-2 text-[11px] text-muted-foreground">
                    <span className="font-mono text-foreground">{edge.source_node_id.slice(0, 16)}...</span>
                    <span>&rarr;</span>
                    <span className="font-mono text-accent">{edge.transformation_op}</span>
                    <span>&rarr;</span>
                    <span className="font-mono text-foreground">{edge.target_node_id.slice(0, 16)}...</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Selected Node Inspector Pane */}
        <div className="rounded border border-border bg-surface-elevated p-3">
          <div className="text-xs font-semibold text-muted-foreground">NODE INSPECTOR</div>
          {selectedNode ? (
            <div className="mt-2 space-y-2 text-xs">
              <div>
                <span className="text-muted-foreground">Label: </span>
                <span className="font-medium text-foreground">{selectedNode.label}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Node ID: </span>
                <span className="font-mono break-all text-foreground">{selectedNode.node_id}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Type: </span>
                <span className="font-medium text-foreground">{selectedNode.node_type}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Authority Lane: </span>
                <span className="font-medium text-foreground">{selectedNode.lane}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Timestamp: </span>
                <span className="font-mono text-foreground">{selectedNode.timestamp}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Cryptographic SHA-256: </span>
                <p className="mt-0.5 break-all font-mono text-[11px] text-foreground bg-surface p-1.5 rounded border border-border">
                  {selectedNode.sha256}
                </p>
              </div>
              {selectedNode.receipt_ref && (
                <div>
                  <span className="text-muted-foreground">Receipt Ref: </span>
                  <p className="mt-0.5 break-all font-mono text-[11px] text-accent bg-surface p-1.5 rounded border border-border">
                    {selectedNode.receipt_ref}
                  </p>
                </div>
              )}
              {Object.keys(selectedNode.metadata).length > 0 && (
                <div>
                  <span className="text-muted-foreground">Metadata: </span>
                  <pre className="mt-1 max-h-40 overflow-y-auto rounded border border-border bg-surface p-1.5 font-mono text-[10px] text-foreground">
                    {JSON.stringify(selectedNode.metadata, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          ) : (
            <div className="mt-6 text-center text-xs text-muted-foreground">
              Click on any node in the DAG to inspect full cryptographic metadata and lineage provenance.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
