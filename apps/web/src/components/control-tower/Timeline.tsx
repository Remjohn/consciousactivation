// TS-APP-UI-003 / CAE-M0066 - native operator editing surface

import { useState } from "react";
import { Button } from "../ui/Button";
import type { TimelineProjection } from "../../api/campaigns";
import { useNativeEdit } from "../../hooks/useRevision";

interface TimelineProps {
  campaignId: string;
  timeline: TimelineProjection | null;
  stateVersion?: number;
}

export function Timeline({ campaignId, timeline, stateVersion = 1 }: TimelineProps) {
  const nativeEdit = useNativeEdit(campaignId);
  const [selectedItemId, setSelectedItemId] = useState<string | null>(null);
  const [deltaFrames, setDeltaFrames] = useState("0");
  const [assetRef, setAssetRef] = useState("");
  const [assetSha256, setAssetSha256] = useState("");
  const [assetVersion, setAssetVersion] = useState("1.0.0");
  const [previewedProgram, setPreviewedProgram] = useState<any>(null);
  const items = timeline?.items ?? [];

  if (!timeline) {
    return (
      <div className="control-tower-card">
        <div className="control-tower-card-header"><span>Timeline</span></div>
        <p className="text-ca-text-secondary">Nothing has been compiled yet for this campaign</p>
      </div>
    );
  }

  const durationSeconds = timeline.fps_numerator > 0 && timeline.fps_denominator > 0
    ? (timeline.duration_frames / (timeline.fps_numerator / timeline.fps_denominator)).toFixed(1)
    : "0.0";

  const selectedItem = items.find((item) => item.item_id === selectedItemId) ?? null;
  const currentRef = timeline.video_edit_program_ref;
  const operatorActor = {
    actor_id: "operator-web-001",
    actor_type: "human" as const,
    product_id: "conscious-activations-web" as const,
    workflow_role: "operator" as const,
  };

  const submitEdit = (manipulationType: "ADJUST_TIMING" | "SUBSTITUTE_ASSET") => {
    if (!selectedItem) return;
    const argumentsPayload = manipulationType === "ADJUST_TIMING"
      ? { delta_frames: Number(deltaFrames), source_start_delta_ms: 0, source_end_delta_ms: 0 }
      : {
          source_ref: {
            object_id: assetRef,
            version: assetVersion,
            sha256: assetSha256,
          },
        };
    nativeEdit.compile.mutate({
      delta_id: `delta-${selectedItem.item_id}-${Date.now()}`,
      run_ref: currentRef,
      target_ref: selectedItem.source_ref ?? currentRef,
      target_node_id: selectedItem.item_id,
      manipulation_type: manipulationType,
      arguments: argumentsPayload,
      current_state_ref: currentRef,
      operator_actor: operatorActor,
      expected_state_version: stateVersion,
    }, {
      onSuccess: (result: any) => setPreviewedProgram(result),
    });
  };

  return (
    <div className="control-tower-card space-y-4">
      <div className="control-tower-card-header">
        <span>Native Timeline Editor</span>
        <span className="text-xs text-ca-text-secondary">{durationSeconds}s · state v{stateVersion}</span>
      </div>

      <div className="rounded border border-ca-border p-3 text-xs text-ca-text-secondary">
        Changes are compiled, bounded, CAS-checked, persisted to canonical campaign state, and recorded as an immutable HumanResolutionEpisode. Release remains separate.
      </div>

      {items.length === 0 ? (
        <p className="text-ca-text-tertiary">No editable items in the canonical timeline.</p>
      ) : (
        <div className="space-y-2">
          {items.map((item: any) => {
            const selected = selectedItemId === item.item_id;
            const leftPct = timeline.duration_frames ? (item.start_frame / timeline.duration_frames) * 100 : 0;
            const widthPct = timeline.duration_frames ? ((item.end_frame - item.start_frame) / timeline.duration_frames) * 100 : 0;
            return (
              <button
                type="button"
                key={item.item_id}
                onClick={() => setSelectedItemId(item.item_id)}
                className={`relative block w-full rounded bg-ca-bg p-2 text-left ${selected ? "ring-2 ring-ca-gold-500" : ""}`}
                aria-label={`Edit ${item.item_id}`}
              >
                <div className="text-xs text-ca-text-secondary">{item.item_id} · {item.start_frame}-{item.end_frame}</div>
                <div className="relative mt-1 h-8 rounded bg-ca-surface-raised">
                  <div className="absolute top-1 bottom-1 rounded border border-ca-gold-500 bg-ca-gold-500/20" style={{ left: `${leftPct}%`, width: `${widthPct}%` }} />
                </div>
              </button>
            );
          })}
        </div>
      )}

      {selectedItem && (
        <div className="rounded border border-ca-border p-4 space-y-3">
          <div className="text-sm font-medium text-ca-text-primary">Selected: {selectedItem.item_id}</div>
          <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
            <label className="text-sm text-ca-text-secondary">
              Timing delta (frames)
              <input aria-label="Timing delta frames" value={deltaFrames} onChange={(e) => setDeltaFrames(e.target.value)} className="mt-1 w-full rounded bg-ca-surface-raised p-2 text-ca-text-primary" inputMode="numeric" />
            </label>
            <label className="text-sm text-ca-text-secondary">
              Replacement asset ID
              <input aria-label="Replacement asset ID" value={assetRef} onChange={(e) => setAssetRef(e.target.value)} className="mt-1 w-full rounded bg-ca-surface-raised p-2 text-ca-text-primary" />
              <input aria-label="Replacement asset version" value={assetVersion} onChange={(e) => setAssetVersion(e.target.value)} className="mt-2 w-full rounded bg-ca-surface-raised p-2 text-ca-text-primary" />
              <input aria-label="Replacement asset SHA256" value={assetSha256} onChange={(e) => setAssetSha256(e.target.value)} className="mt-2 w-full rounded bg-ca-surface-raised p-2 font-mono text-xs text-ca-text-primary" placeholder="64-character SHA-256" />
            </label>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button onClick={() => submitEdit("ADJUST_TIMING")} disabled={nativeEdit.compile.isPending || nativeEdit.execute.isPending || selectedItem.editable_operations?.includes("ADJUST_TIMING") !== true}>Adjust timing</Button>
            <Button onClick={() => submitEdit("SUBSTITUTE_ASSET")} disabled={nativeEdit.compile.isPending || nativeEdit.execute.isPending || !assetRef || assetSha256.length !== 64 || selectedItem.editable_operations?.includes("SUBSTITUTE_ASSET") !== true}>Substitute asset</Button>
          </div>
          {previewedProgram && <div className="rounded bg-ca-gold-500/10 p-3"><div className="text-sm font-medium text-ca-text-primary">Preview ready</div><div className="text-xs text-ca-text-secondary mt-1">{previewedProgram.interpretation}</div><Button className="mt-2" onClick={() => nativeEdit.execute.mutate(previewedProgram.program_id)} disabled={nativeEdit.execute.isPending}>{nativeEdit.execute.isPending ? "Saving…" : "Confirm & Save"}</Button></div>}
          {nativeEdit.compile.isError && <p className="text-sm text-ca-danger">Edit rejected: {(nativeEdit.compile.error as Error).message}</p>}
          {nativeEdit.execute.isError && <p className="text-sm text-ca-danger">Commit rejected: {(nativeEdit.execute.error as Error).message}</p>}
          {nativeEdit.execute.data && <p className="text-sm text-ca-success">Saved revision and HumanResolutionEpisode.</p>}
        </div>
      )}
    </div>
  );
}
