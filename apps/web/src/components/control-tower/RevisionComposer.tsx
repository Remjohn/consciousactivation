// TS-APP-UI-003 - RevisionComposer component
// Natural language revision compile + confirm + execute workflow

import { useState } from "react";
import { Textarea } from "../ui/Textarea";
import { Button } from "../ui/Button";
import { Badge } from "../ui/Badge";
import type { ControlTowerProjection, NaturalLanguageRevisionInput } from "../../api/campaigns";
import type { UseMutationResult } from "@tanstack/react-query";

interface RevisionComposerProps {
  campaignId: string;
  tower: ControlTowerProjection;
  compileMutation: UseMutationResult<any, Error, NaturalLanguageRevisionInput>;
  executeMutation: UseMutationResult<any, Error, string>;
}

export function RevisionComposer({
  campaignId,
  tower,
  compileMutation,
  executeMutation,
}: RevisionComposerProps) {
  const [revisionText, setRevisionText] = useState("");
  const [selectedNodeIds, setSelectedNodeIds] = useState<string[]>([]);
  const [compiledResult, setCompiledResult] = useState<any>(null);

  // Check if timeline exists (required for revision target)
  const hasTimeline = tower.timeline !== null;
  const targetRef = tower.timeline?.video_edit_program_ref;

  const handleCompile = () => {
    if (!hasTimeline || !targetRef) return;

    const input: NaturalLanguageRevisionInput = {
      mode: "natural_language",
      target_refs: [targetRef],
      target_node_ids: selectedNodeIds,
      category_id: tower.order?.category_id ?? "",
      natural_language_request: revisionText,
      current_state_ref: targetRef, // Source gap notice 3
    };

    compileMutation.mutate(input, {
      onSuccess: (data) => {
        setCompiledResult(data);
      },
    });
  };

  const handleExecute = (programId: string) => {
    executeMutation.mutate(programId, {
      onSuccess: () => {
        // Reset form on success
        setRevisionText("");
        setSelectedNodeIds([]);
        setCompiledResult(null);
      },
    });
  };

  // Filter run nodes for selection (only nodes with meaningful status)
  const selectableNodes = tower.run_nodes?.filter((n) =>
    ["RUNNING", "FAILED", "SUCCEEDED", "WAITING_HUMAN"].includes(n.status)
  ) ?? [];

  return (
    <div className="control-tower-card">
      <div className="control-tower-card-header">
        <span>Request Revision</span>
      </div>

      {/* Timeline check */}
      {!hasTimeline && (
        <div className="mb-4 rounded bg-ca-waiting/10 p-3 text-sm text-ca-waiting">
          Open the Timeline tab first — no edit program exists yet for this campaign
        </div>
      )}

      {/* Revision text input */}
      <div className="mb-4">
        <label className="mb-2 block text-sm text-ca-text-secondary">
          Describe the change you want
        </label>
        <Textarea
          value={revisionText}
          onChange={(e) => setRevisionText(e.target.value)}
          placeholder="e.g., trim the intro by 3 seconds, make the text larger..."
          disabled={!hasTimeline}
          rows={4}
          className="w-full"
        />
      </div>

      {/* Node selection (optional) */}
      {selectableNodes.length > 0 && (
        <div className="mb-4">
          <label className="mb-2 block text-sm text-ca-text-secondary">
            Target nodes (optional)
          </label>
          <div className="flex flex-wrap gap-2">
            {selectableNodes.map((node) => (
              <button
                key={node.node_id}
                onClick={() => {
                  setSelectedNodeIds((prev) =>
                    prev.includes(node.node_id)
                      ? prev.filter((id) => id !== node.node_id)
                      : [...prev, node.node_id]
                  );
                }}
                className={`rounded-full px-3 py-1 text-xs font-medium transition-colors ${
                  selectedNodeIds.includes(node.node_id)
                    ? "bg-ca-gold-500 text-white"
                    : "bg-ca-surface-raised text-ca-text-secondary hover:bg-ca-surface"
                }`}
              >
                {node.node_id.slice(0, 8)}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Compile button */}
      <Button
        onClick={handleCompile}
        disabled={!hasTimeline || !revisionText || compileMutation.isPending}
        className="mb-4"
      >
        {compileMutation.isPending ? "Compiling..." : "Preview"}
      </Button>

      {/* Compilation result */}
      {compiledResult && (
        <div className="mt-4 space-y-4">
          {compiledResult.compilation_status === "COMPILED" && (
            <div className="rounded-lg bg-ca-success/10 p-4">
              <h4 className="mb-2 font-medium text-ca-success">Compilation Successful</h4>
              <p className="text-sm text-ca-text-primary">{compiledResult.interpretation}</p>

              {/* Operations list */}
              {compiledResult.exact_operations?.length > 0 && (
                <div className="mt-3">
                  <div className="text-xs text-ca-text-secondary">Operations:</div>
                  <ul className="mt-1 list-inside list-disc text-sm text-ca-text-primary">
                    {compiledResult.exact_operations.map((op: any, idx: number) => (
                      <li key={idx}>
                        {op.tool_id}: {JSON.stringify(op.arguments).slice(0, 50)}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Confidence */}
              {compiledResult.confidence_micros && (
                <div className="mt-2 text-xs text-ca-text-secondary">
                  Confidence: {((compiledResult.confidence_micros / 10000)).toFixed(1)}%
                </div>
              )}

              {/* Confirm button */}
              <Button
                onClick={() => handleExecute(compiledResult.program_id)}
                disabled={executeMutation.isPending}
                className="mt-3"
              >
                {executeMutation.isPending ? "Executing..." : "Confirm & Run"}
              </Button>
            </div>
          )}

          {compiledResult.compilation_status === "NEEDS_CLARIFICATION" && (
            <div className="rounded-lg bg-ca-waiting/10 p-4">
              <h4 className="mb-2 font-medium text-ca-waiting">Needs Clarification</h4>
              <p className="text-sm text-ca-text-primary">{compiledResult.interpretation}</p>
              <p className="mt-2 text-xs text-ca-text-secondary">{compiledResult.escalation}</p>

              {/* Retry textarea */}
              <Textarea
                value={revisionText}
                onChange={(e) => setRevisionText(e.target.value)}
                placeholder="Please clarify your request..."
                rows={2}
                className="mt-3 w-full"
              />
            </div>
          )}

          {compiledResult.compilation_status === "DENIED" && (
            <div className="rounded-lg bg-ca-danger/10 p-4">
              <h4 className="mb-2 font-medium text-ca-danger">Revision Denied</h4>
              <p className="text-sm text-ca-text-primary">{compiledResult.escalation}</p>
            </div>
          )}
        </div>
      )}

      {/* Error display */}
      {(compileMutation.error || executeMutation.error) && (
        <div className="mt-4 rounded-lg bg-ca-danger/10 p-3 text-sm text-ca-danger">
          {compileMutation.error?.message ?? executeMutation.error?.message}
        </div>
      )}
    </div>
  );
}
